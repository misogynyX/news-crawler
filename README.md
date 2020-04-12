# 신문 기사 수집

![Update data](https://github.com/misogynyX/news/workflows/Update%20data/badge.svg)

일자별 조회수 높은 신문 기사 모음입니다. 저작권 문제로 인해 본문은 제외하고 제목, 링크, 키워드, 게시일 등 메타 정보만 저장합니다.

## 수집 기준

- 2018년 1월 1일부터 수집
- 다음 뉴스 일별 조회수, 댓글수 기준 각각 상위 200개 기사를 읽어온 후 병합
- 매일 0시(UTC 기준)에 전일 데이터를 추가
- `docs/data` 폴더에 `yyyymmdd.csv` 형식으로 저장

## 데이터 설명

- `article_id`: 기사 고유 번호
- `cp_name`: 언론사 이름
- `title`: 기사 제목
- `description`: 기사 본문 앞부분 발췌
- `authors`: 기자. 구분자는 `;`
- `keywords`: 키워드 목록. 구분자는 `;`

## 개발하기

Python 3.8과 [poetry](https://python-poetry.org)를 설치해주세요. [pyenv](https://github.com/pyenv/pyenv)를 쓴다면 아래와 같이 초기화하시면 됩니다.

```
# 프로젝트 디렉토리로 이동하기
cd news-crawler

# 'news'라는 이름으로 가상환경 만들기
pyenv virtualenv 3.8.2 news-crawler

# 이 디렉토리에서는 자동으로 'news-crawler' 가상환경을 사용하도록 설정하기
pyenv local news-crawler

# poetry 설치하기
pip install poetry

# 프로젝트 라이브러리 설치하기
poetry install
```

단위 테스트는 이렇게 실행하세요.

```
# 테스트 1회 실행하기
pytest

# 코드가 수정되면 자동으로 테스트가 실행되도록 하기
ptw
```
