import requests
from bs4 import BeautifulSoup

# 페이지에 출력되는 게시물의 개수
LIMIT = 50
# 현재 페이지
URL = f"https://www.indeed.com/jobs?q=python&limit={LIMIT}"

# 현재 페이지에서 가장 마지막 페이지 번호를 알려주는 함수
def get_last_page():
  # url 변수
  result = requests.get(URL)

  # BeautifulSoup를 이용하여 파싱
  soup = BeautifulSoup(result.text, 'html.parser')

  # find 함수로 페이지 번호클래스를 찾기
  pagination = soup.find("div", {"class": "pagination"})

  # find_all 함수로 번호클래스(pagination) 안에 a태그를 모두 가져오기, 리스트로 저장된다.
  links = pagination.find_all('a')

  # links에 저장된 a태그 안의 문자열(페이지 넘버)을 int형으로 pages 배열에 넣어줌
  # 배열의 맨 마지막은 Next 버튼이므로 제외 시켜줌 -> links[:-1]
  pages = []
  for link in links[:-1]:
    pages.append(int(link.string))

  # 페이지의 마지막 번호를 리턴
  max_page = pages[-1]
  return max_page

# get_jobs 함수에서 가져온 구인 게시물에서 정보를 추출하는 함수
# html인자는 페이지의 구인 게시물들 중 1개를 의미한다.
def extract_job(html):
  title = html.find("h2", {"class": "title"}).find("a")["title"]
  company = html.find("span", {"class": "company"})
  company_anchor = company.find("a")
  if company:
    if company_anchor is not None:
      company = str(company_anchor.string)
    else:
      company = str(company.string)
  else:
    company = None
  company = company.strip()
  location = html.find("div", {"class": "recJobLoc"})["data-rc-loc"]
  job_id = html["data-jk"]
  return {
    'title': title,
    'company': company,
    'location': location,
    'link': f'https://www.indeed.com/viewjob?jk={job_id}'
  }

# 페이지의 구인 게시물들을 가져와 정보를 리턴하는 함수
# extract_job 함수를 사용, 구인 게시물에서 타이틀, 회사, 위치, 링크를 jobs 배열에 저장
def extract_jobs(last_page):    
  jobs = []
  for page in range(last_page):
    print(f"Scrapping indeed page : {page}")
    result = requests.get(f"{URL}&start = {page * LIMIT}")
    soup = BeautifulSoup(result.text, 'html.parser')
    results = soup.find_all("div", {"class": "jobsearch-SerpJobCard"})
    for result in results:
      job = extract_job(result)
      jobs.append(job)
  return jobs

def get_jobs():
  # get_last_page = 마지막 페이지 번호를 리턴
  last_page = get_last_page()

  # get_jobs = 특정 문자열과 값을 50 곱해 출력
  jobs = extract_jobs(last_page)

  return jobs