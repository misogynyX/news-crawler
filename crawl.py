import re
from datetime import date, datetime, timedelta
from itertools import groupby
from typing import List, Optional, Iterable


def get_kst_today(now: Optional[datetime] = None) -> date:
    now = now or datetime.utcnow()
    return (now + timedelta(hours=9)).date()


def cleanse(articles):
    articles = (a for a in articles if is_meaningful(a))
    articles = (cleanse_article(a) for a in articles)
    articles = remove_duplications(articles)
    return sorted(articles, key=lambda a: a['article_id'])


def remove_duplications(articles):
    articles = sorted(articles, key=lambda a: a['title'])
    grouped = groupby(articles, key=lambda a: a['title'])
    return (list(group)[-1] for key, group in grouped)


def cleanse_article(article):
    article_id = article['_id']['key']
    cp_name = article['cpInfo'].get('korName', None)
    title = cleanse_title(article['title'])
    description = article.get('description', '')
    authors = cleanse_authors(article['author'].get('reporter', None))
    keywords = article.get('keyword', [])

    return {
        'article_id': article_id,
        'cp_name': cp_name,
        'title': title,
        'description': description,
        'authors': authors,
        'keywords': keywords,
    }


def is_meaningful(article):
    # 본문이 지나치게 짧은 기사
    if len(article.get('description', '')) < 160:
        return False

    # 특정 언론사 제외
    cp_exclusions = {
        'bnt뉴스',
        'SBSCNBC',
        '더 트래블러',
        '동아사이언스',
        '디지털타임즈',
        '머니s',
        '매경이코노미',
        '스냅',
        '엘르',
        '연합뉴스 보도자료',
        '월간 아웃도어',
        '월간 전원속의 내집',
        '월간산',
        '웨딩21뉴스',
        '이코노미조선',
        '전자신문',
        '조선비즈',
        '코메디닷컴',
        '키즈맘',
        '투어코리아',
        '트래비',
        '하이닥',
        '한경비즈니스',
        '한국경제TV',
        '헬스조선',
    }
    if article['cpInfo'].get('korName', None) in cp_exclusions:
        return False

    # 경제 기사 제외
    category_exclusions = {'economic', 'digital'}
    if article.get('cateInfo', {}).get('category',
                                       None) in category_exclusions:
        return False

    # 제목에 특정 키워드가 있는 기사
    if not is_meaningful_title(article['title']):
        return False

    return True


def is_meaningful_title(title):
    keywords = [
        '그래픽',
        '날씨',
        '단신',
        '사진',
        '영상',
        '전문',
        '포토',
        '카드뉴스',
        '헤드라인',
    ]
    p = r'속보|\d보|^.(' + '|'.join(keywords) + ')'
    return not re.search(p, title)


def cleanse_title(raw):
    return re.sub(r'[\[\<\(]종합[\]\>\)]\s?', '', raw)


def cleanse_authors(raw):
    if not raw:
        return []

    # "기자" 빼기
    raw = re.sub(r'\s?기자\b', '', raw)

    # 구분자로 나누기
    authors = [a.strip() for a in re.split(r'[^\w\s]+', raw)]

    # 언론사 이름 빼기
    authors = [extract_person_name(a) for a in authors]

    # 빈 값, 영문만 있는 값 빼기
    authors = [a for a in authors if not re.match(r'[A-Za-z\s]+', a)]

    return authors


def extract_person_name(raw):
    # 띄어쓰기가 없으면 사람 이름만 있는걸로 간주
    if raw.find(' ') == -1:
        return raw

    # '아무개의 무슨쇼', '아무개입니다' 형식
    m = re.search(r'([^\s]{2,4})(의 |입니다)', raw)
    if m:
        return m[1]

    # 띄어쓰기가 있으면, "팀", "뉴스", "일보" 등이 들어있는 단어를 제외
    excludes = r'^(.+(팀|뉴스|일보|컨설턴트|논설|주간|평론)|.|.{5,})$'
    candidates = [
        t for t in re.split(r'[\s]+', raw) if not re.match(excludes, t)
    ]
    if len(candidates):
        return candidates[0]

    # 다 실패하면 원래값을 반환
    return raw
