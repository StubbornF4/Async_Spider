import asyncio
from urllib.parse import urlencode
import aiohttp
import logging
import json

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s: %(message)s')

INDEX_URL = 'https://dynamic5.scrape.cuiqingcai.com/api/book/?'
CONCURRENCY = 5
session = None
article_id = []
#定义信号量，最大的并发抓取数
semaphore = asyncio.Semaphore(CONCURRENCY)

async def scrape_index(page):
    params = {
        'limit': 18,
        'offset': int(page) * 18,
    }
    url = INDEX_URL + urlencode(params)
    async with semaphore:
        try:
            logging.info('scraping %s', url)
            async with session.get(url) as response:
                result = await response.text()
                logging.info('page %s result %s ', page, result)
                #将Str类型的数据转成Dict
                result = json.loads(result)
                return result
        except aiohttp.ClientError:
            logging.error('error occurred while scraping %s', url, exc_info=True)

async def scrape_detail(id):
    url = "https://dynamic5.scrape.cuiqingcai.com/api/book/" + str(id)
    async with semaphore:
        try:
            logging.info('scraping %s', url)
            async with session.get(url) as response:
                result = await response.json()
        except aiohttp.ClientError:
            logging.error('error occurred while scraping %s', url, exc_info=True)


async def main():
    global session, article_id
    session = aiohttp.ClientSession()
    #抓取索引页，获取每页所有书的ID，以进行进一步的抓取
    scrape_index_tasks = [asyncio.ensure_future(scrape_index(page))for page in range(1, 3)]
    results = await asyncio.gather(*scrape_index_tasks)
    for result in results:
        for item in result["results"]:
            article_id.append((item["id"]))
    print(article_id)
    #对详情页进行抓取
    scrape_detail_tasks = [asyncio.ensure_future(scrape_detail(id))for id in article_id]
    await asyncio.gather(*scrape_detail_tasks)

    await session.close()

if __name__ == '__main__':
    asyncio.get_event_loop().run_until_complete(main())