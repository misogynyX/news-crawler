import csv
import itertools
import json
import os
import sys
from datetime import date, datetime, timedelta
from multiprocessing import Pool
from urllib import request

import fire

import crawl

DATA_DIR = 'data'

CAP = date(2016, 1, 1)
OVERWRAP = 3


class CLI:
    """News crawler"""
    def fetch_missings(self):
        """해당 일자의 파일이 없는 경우에만 새로 받아오기"""
        os.makedirs(DATA_DIR, exist_ok=True)
        pool = Pool(16)

        existing_files = {line[:8] for line in sys.stdin}
        today = crawl.get_kst_today()
        n_days = (today - CAP).days + 1

        for day in range(n_days):
            filename = (CAP + timedelta(days=day)).strftime('%Y%m%d')
            overwraps = day >= n_days - OVERWRAP
            exists = filename in existing_files
            if not overwraps and exists:
                continue
            print(f'{filename}.csv', end=' ', flush=True)
            articles = fetch_a_day(filename, pool)
            print(len(articles))
            with open(os.path.join(DATA_DIR, f'{filename}.csv'), 'w') as f:
                write_csv(articles, f)

        pool.terminate()

    def fetch(self, date, out=sys.stdout):
        articles = fetch_a_day(date)
        write_csv(articles, out)


def fetch_a_day(yyyymmdd, pool):
    page_size = 200  # max page size allowed by api

    # fetch first page to calculate total_pages
    first_page, total_articles = fetch(yyyymmdd, 0, page_size)
    total_pages = round(total_articles / page_size + 0.5)

    # fetch rest pages
    params = [(yyyymmdd, index, page_size) for index in range(1, total_pages)]
    results = pool.starmap(fetch, params)
    rest_pages = [r[0] for r in results]

    # cleanse
    all_articles = []
    for page in [first_page] + rest_pages:
        for article in page:
            all_articles.append(article)
    return crawl.cleanse(all_articles)


def fetch(yyyymmdd, page_index, page_size):
    """Fetches news articles"""
    # fetch
    url = (
        f'http://m.media.daum.net/proxy/api/mc2/contents/ranking.json?' \
        f'service=news&pageSize={page_size}&regDate={yyyymmdd}&page={page_index + 1}'
    )
    with request.urlopen(url) as f:
        data = json.loads(f.read().decode('utf-8'))
        return data['data'], data['totalCount']


def write_csv(articles, out):
    # write as csv
    fields = [
        'article_id', 'cp_name', 'title', 'description', 'authors', 'keywords'
    ]
    csvw = csv.DictWriter(out, fields)
    csvw.writeheader()
    for article in articles:
        keywords = ';'.join(article['keywords'])
        authors = ';'.join(article['authors'])
        csvw.writerow({**article, 'keywords': keywords, 'authors': authors})


if __name__ == '__main__':
    fire.Fire(CLI())
