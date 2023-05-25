import threading
from concurrent.futures import ThreadPoolExecutor

from app.main.helper.request_factory import RequestFactory
from lxml import etree
import pandas as pd
from requests.models import Response
from tqdm import tqdm
from bs4 import BeautifulSoup

from app.main.model.channel import Channel
from app.main.model.item import Item

TAG_CLASS = "article__body-text"
COLUMNS = ['title', 'description', 'body', 'publish_date']
THREAD_POOL_SIZE = 10


def scrape(url: str, is_multi_thread: bool = False):
    result = []
    page: Response = RequestFactory.get(url)
    root = etree.fromstring(page.content)
    channel_node = root.find('channel')
    channel: Channel = Channel.from_xml(etree.tostring(channel_node))
    progress_bar = tqdm(total=len(channel.items), desc="Scraping")
    if is_multi_thread:
        lock = threading.Lock()
        with ThreadPoolExecutor(max_workers=THREAD_POOL_SIZE) as executor:
            futures = [executor.submit(__scrape_single_item, items, progress_bar, lock) for items in channel.items]
            result = [future.result() for future in futures]
    else:
        for item in channel.items:
            single_item_result = __scrape_single_item(item, progress_bar, None)
            result.append(single_item_result)
    progress_bar.close()
    data_frame: pd.DataFrame = pd.DataFrame(result, columns=COLUMNS)
    file_name = f'{channel.title}_{channel.publish_date}.csv'
    data_frame.to_csv(file_name)


def __scrape_single_item(item: Item, progress_bar, lock) -> ():
    article_page: Response = RequestFactory.get(item.link)
    soup = BeautifulSoup(article_page.content, "html.parser")
    article_body_text: str = '\n'.join([r.text for r in soup.find_all("p", class_=TAG_CLASS)])
    if lock:
        with lock:
            progress_bar.update(1)
    else:
        progress_bar.update(1)
    return item.title, item.description, article_body_text, item.publish_date
