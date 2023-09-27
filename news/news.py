import requests
from bs4 import BeautifulSoup
import pandas as pd
import yagmail

# 네이버 뉴스 크롤링 함수
def crawl_naver_news(keyword, num_articles):
    news_data = []

    # 네이버 뉴스 검색 URL
    url = f"https://search.naver.com/search.naver?where=news&query={keyword}"

    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    # 뉴스 기사 추출
    articles = soup.select('.news_area')

    for i, article in enumerate(articles[:num_articles]):
        title = article.select_one('.news_tit').text
        link = article.select_one('.news_tit a')['href']
        source = article.select_one('.info.press').text
        news_data.append({"뉴스 제목": title, "뉴스 기사 링크": link, "소스": source})

    return news_data

# 엑셀 파일 생성 함수
def create_excel(news_data, output_file):
    df = pd.DataFrame(news_data)
    df.index += 1  # 번호를 1부터 시작하도록 설정
    df.index.name = "번호"
    df.to_excel(output_file, index=True)

# 이메일 전송 함수
def send_email(receiver_email, subject, contents, attachment_path=None):
    yag = yagmail.SMTP('your_email@gmail.com', 'your_password')  # 보내는 이메일 계정 설정
    yag.send(
        to=receiver_email,
        subject=subject,
        contents=contents,
        attachments=attachment_path,
    )
    print("이메일을 전송했습니다.")

def main():
    keywords = [
        "삼성전자",
        "삼성화재",
        "삼성중공업",
        "삼성바이오로직스",
        "삼성엔지니어링",
        "삼성서울병원",
        "삼성생명",
        "삼성물산",
        "삼성디스플레이",
        "삼성SDS"
    ]
    num_articles = 3  # 가져올 기사 수

    for keyword in keywords:
        news_data = crawl_naver_news(keyword, num_articles)
        if news_data:
            output_file = f"{keyword}_news.xlsx"
            create_excel(news_data, output_file)
            email_contents = f"네이버 뉴스 크롤링 결과입니다.\n\n{output_file} 파일을 첨부합니다."
            send_email("recipient_email@example.com", "네이버 뉴스 크롤링 결과", email_contents, output_file)

if __name__ == "__main__":
    main()
