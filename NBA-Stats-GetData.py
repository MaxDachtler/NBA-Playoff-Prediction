import os
from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeout
import time

seasons = list(range(2015, 2023))

data_dir = "data2"
standings_dir = os.path.join(data_dir, "standings")
scores_dir = os.path.join(data_dir, "scores")

def get_html(url, selector, sleep=5, retries=5):
    html = None
    for i in range(1, retries+1):
        time.sleep(sleep*i)

        try:
            with sync_playwright() as p:
                browser = p.firefox.launch()
                page = browser.new_page()
                page.goto(url)
                print(page.title())
                html = page.inner_html(selector)

        except PlaywrightTimeout:
            print(f"Timeout error on {url}")
            continue
        else:
            break
    return html

def scrape_season(season):
    url = f"https://www.basketball-reference.com/leagues/NBA_{season}_games.html"
    html = get_html(url, "#content .filter")
    soup = BeautifulSoup(html)
    links = soup.find_all("a")
    href = [l["href"] for l in links]
    standing_pages = [f"https://basketball-reference.com{l}" for l in href]

    for url in standing_pages:
        save_path = os.path.join(standings_dir, url.split("/")[-1])
        if os.path.exists(save_path):
            continue

        html = get_html(url, "#all_schedule")
        with open(save_path, "w+") as f:
            f.write(html)

for season in seasons:
    scrape_season(season)




