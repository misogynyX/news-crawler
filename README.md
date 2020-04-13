# 신문 기사 수집

![Update data](https://github.com/misogynyX/news-crawler/workflows/Update%20data/badge.svg)

일자별 신문 기사를 모읍니다. 저작권 문제로 인해 본문은 제외하고 제목, 링크닏
키워드, 게시일 등 메타 정보만 저장합니다.

## 수집 기준

- 2016년 1월 1일부터 수집
- 일부 전문지(경제/레포츠/취미 등) 제외
- 일부 기사 제외(주식 기사, 포토 뉴스, 단신 등)

## 데이터 다운로드

수집한 데이터는 AWS S3에 일자별로 저장되며 웹을 통해 다운로드 받을 수 있습니다.
예를 들어 2017년 3월 12일 데이터를 받으려면 다음 URL로 접속하세요:

```https://misogynyx.s3.ap-northeast-2.amazonaws.com/news/20170312.csv.gz```

## 데이터 설명

- `article_id`: 기사 고유 번호. `https://news.v.daum.net/v/` 뒤에 붙이면 url
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

## 데이터 수집하기

환경 변수:

* `AWS_ACCESS_KEY_ID`: AWS access key id
* `AWS_SECRET_ACCESS_KEY`: AWS secret key
* `AWS_S3_BUCKET`: 데이터를 동기화할 버킷 이름

새로 추가된 뉴스를 수집해서 S3에 저장하기:

```
./update.sh
```

다음 명령을 실행하면 기타 CLI 명령들을 확인할 수 있습니다.

```
python cli.py
```
