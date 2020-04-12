import crawl
from datetime import datetime as dt, date as d


class TestDatesToFetch:
    def test_get_kst_today(self):
        two_pm = dt(2012, 3, 4, 14, 0, 0)
        assert crawl.get_kst_today(two_pm) == d(2012, 3, 4)

        three_pm = dt(2012, 3, 4, 15, 0, 0)
        assert crawl.get_kst_today(three_pm) == d(2012, 3, 5)

    def test_normal(self):
        cap = d(2016, 1, 1)
        overwrap = 2
        files = []
        now = dt(2016, 1, 4, 0, 0, 0)
        actual = list(crawl.files_to_fetch(cap, overwrap, files, now))
        expected = ['20160101', '20160102', '20160103', '20160104']
        assert expected == actual

    def test_existing_file(self):
        cap = d(2016, 1, 1)
        overwrap = 2
        files = ['20160102']
        now = dt(2016, 1, 4, 0, 0, 0)
        actual = list(crawl.files_to_fetch(cap, overwrap, files, now))
        expected = ['20160101', '20160103', '20160104']
        assert expected == actual

    def test_existing_file_but_in_overwrapped_range(self):
        cap = d(2016, 1, 1)
        overwrap = 2
        files = ['20160101', '20160102', '20160103']
        now = dt(2016, 1, 4, 0, 0, 0)
        actual = list(crawl.files_to_fetch(cap, overwrap, files, now))
        expected = ['20160103', '20160104']
        assert expected == actual


class TestCleansing:
    def test_remove_duplications(self):
        sources = [
            {
                'title': 't0',
                'cp_name': 'c0'
            },
            {
                'title': 't1',
                'cp_name': 'c0'
            },
            {
                'title': 't1',
                'cp_name': 'c1'
            },
            {
                'title': 't0',
                'cp_name': 'c0'
            },
            {
                'title': 't2',
                'cp_name': 'c2'
            },
            {
                'title': 't3',
                'cp_name': 'c2'
            },
            {
                'title': 't2',
                'cp_name': 'c2'
            },
        ]
        expected = [
            {
                'title': 't0',
                'cp_name': 'c0'
            },
            {
                'title': 't1',
                'cp_name': 'c1'
            },
            {
                'title': 't2',
                'cp_name': 'c2'
            },
            {
                'title': 't3',
                'cp_name': 'c2'
            },
        ]
        actual = list(crawl.remove_duplications(sources))
        assert expected == actual

    def test_cleanse_article(self):
        raw = {
            '_id': {
                'key': '2020010299999'
            },
            'cpInfo': {
                'korName': 'CP_NAME'
            },
            'title': 'TITLE',
            'description': 'DESCRIPTION',
            'author': {
                'reporter': '김뫄뫄 기자, 이솨솨 기자'
            },
            'keyword': ['KW_A', 'KW_B'],
            'SOME_EXTRA_KEY': 'SOME_EXTRA_VALUE',
        }
        expected = {
            'article_id': '2020010299999',
            'title': 'TITLE',
            'description': 'DESCRIPTION',
            'cp_name': 'CP_NAME',
            'authors': ['김뫄뫄', '이솨솨'],
            'keywords': ['KW_A', 'KW_B'],
        }
        actual = crawl.cleanse_article(raw)
        assert expected == actual

    def test_is_meaningful(self):
        assert crawl.is_meaningful_title('어쩌고')
        assert not crawl.is_meaningful_title('[영상] 어쩌고')

    def test_cleanse_authors(self):
        cases = [
            ('', [], '빈 값이면 빈 배열'),
            ('CBS', [], '영문만 있는 경우'),
            ('김뫄뫄', ['김뫄뫄'], '이름만 있으면 그대로 출력'),
            ('김뫄뫄 기자', ['김뫄뫄'], '"기자" 빼기'),
            ('김뫄뫄기자', ['김뫄뫄'], '띄어쓰기 없는 "기자" 빼기'),
            ('김뫄뫄, 이솨솨', ['김뫄뫄', '이솨솨'], '쉼표 처리'),
            ('김뫄뫄·이솨솨', ['김뫄뫄', '이솨솨'], '중간점 처리'),
            ('김뫄뫄 기자;이솨솨 기자', ['김뫄뫄', '이솨솨'], '기자 빼고 구분자 처리'),
            ('CBS노컷뉴스 김뫄뫄 기자', ['김뫄뫄'], '언론사 이름 빼기 1'),
            ('김뫄뫄 CBS노컷뉴스 기자', ['김뫄뫄'], '언론사 이름 빼기 2'),
            ('CBS 김현정의 뉴스쇼', ['김현정'], '특수한 경우 1'),
        ]
        for before, after, description in cases:
            assert crawl.cleanse_authors(before) == after, description
