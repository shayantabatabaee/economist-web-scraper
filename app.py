import time

from app.main.web_scraper import scrape

if __name__ == '__main__':
    print("Starting scraping economist.com ...")
    tick = time.time()
    SECTION: str = 'the-world-this-week'
    URL: str = f"https://www.economist.com/{SECTION}/rss.xml"
    IS_MULTI_THREAD: bool = False
    print(f"is_multi_thread:{IS_MULTI_THREAD}, URL:{URL}")
    scrape(url=URL, is_multi_thread=IS_MULTI_THREAD)
    print(f"Finished Scraping, elapsed time {(time.time() - tick):.2f}s")
