from selenium import webdriver
from bs4 import BeautifulSoup as bs
import pandas as pd

'''
갱년기 증상 > 몸 증상
menuid=8
https://cafe.naver.com/ArticleList.nhn?search.clubid=29349320&search.menuid=8&userDisplay=50&search.boardtype=L&search.specialmenutype=&search.questionTab=A&search.totalCount=430&search.page=1

갱년기 증상 > 마음 증상
menuid=3
https://cafe.naver.com/ArticleList.nhn?search.clubid=29349320&search.menuid=3&userDisplay=50&search.boardtype=L&search.specialmenutype=&search.questionTab=A&search.totalCount=102&search.page=1

4050 대나무숲 > 딸아들이야기
menuid=5
https://cafe.naver.com/ArticleList.nhn?search.clubid=29349320&search.menuid=5&userDisplay=30&search.boardtype=L&search.specialmenutype=&search.questionTab=A&search.totalCount=266&search.page=1

4050 대나무숲 > 남편이야기
menuid=6
https://cafe.naver.com/ArticleList.nhn?search.clubid=29349320&search.menuid=6&userDisplay=40&search.boardtype=L&search.specialmenutype=&search.questionTab=A&search.totalCount=175&search.page=1

4050 대나무숲 > 시댁이야기
menuid=21
https://cafe.naver.com/ArticleList.nhn?search.clubid=29349320&search.menuid=21&userDisplay=30&search.boardtype=L&search.specialmenutype=&search.questionTab=A&search.totalCount=141&search.page=1

4050 대나무숲 > 일터이야기
menuid=7
https://cafe.naver.com/ArticleList.nhn?search.clubid=29349320&search.menuid=7&userDisplay=20&search.boardtype=L&search.specialmenutype=&search.questionTab=A&search.totalCount=64&search.page=1

4050 대나무숲 > 돈이야기
menuid=32
https://cafe.naver.com/ArticleList.nhn?search.clubid=29349320&search.menuid=32&userDisplay=20&search.boardtype=L&search.specialmenutype=&search.questionTab=A&search.totalCount=68&search.page=1
'''


def opening(id, pw):
    driver = webdriver.Chrome('/Volumes/bkm_sd/chromedriver')
    driver.implicitly_wait(3)

    #네이버 로그인
    driver.get('https://nid.naver.com/nidlogin.login')
    driver.find_element_by_name('id').send_keys(id) #본인 아이디
    driver.find_element_by_name('pw').send_keys(pw) #본인 비밀번호
    driver.find_element_by_css_selector('#frmNIDLogin > fieldset > input').click()



def crawling_articles(num, menuid):
    #카테고리와 무관하게 동일한 앞부분 주소
    base_url = 'https://cafe.naver.com/ArticleList.nhn?search.clubid=29349320&search.'

    #1~8페이지 게시글 추출
    total_article_urls = []
    for page in range(1,num): #현재 예시는 갱년기 증상 > 몸 증상
        page_url = '&userDisplay=50&search.boardtype=L&search.specialmenutype=&search.questionTab=A&search.totalCount=430&search.page=' + str(page)
        driver.get(base_url + menuid + page_url)
        driver.switch_to_frame('cafe_main')
        article_list = driver.find_elements_by_css_selector('a.article')
        article_urls = [ i.get_attribute('href') for i in article_list]
        for article_url in article_urls:
            total_article_urls.append(article_url)
    return total_article_urls[3:]


def exportCSV(res_list, filename):
    # 결과 데이터프레임화
    cafe_df = pd.DataFrame(res_list)
    # csv파일로 추출
    name = 'raw_csv/' + filename + '.csv'
    cafe_df.to_csv(name, index=False)


def main(category):
    id = input("네이버 아이디를 입력하세요.")
    pw = input("네이버 비밀번호를 입력하세요.")

    driver = webdriver.Chrome('/Volumes/bkm_sd/chromedriver')
    driver.implicitly_wait(3)

    # 네이버 로그인
    driver.get('https://nid.naver.com/nidlogin.login')
    driver.find_element_by_name('id').send_keys(id)  # 본인 아이디
    driver.find_element_by_name('pw').send_keys(pw)  # 본인 비밀번호
    driver.find_element_by_css_selector('#frmNIDLogin > fieldset > input').click()


    cate = int(input("원하는 카테고리를 선택하세요.\n1. 갱년기 증상 > 몸 증상\n2. 갱년기 증상 > 마음 증상\n3. 4050 대나무숲 > 딸아들이야기\n4. 4050 대나무숲 > 남편이야기\n5. 4050 대나무숲 > 시댁이야기\n6. 4050 대나무숲 > 일터이야기\n7. 4050 대나무숲 > 돈이야기"))-1
    menuid = category[cate][1]
    total_count = category[cate][2]
    page_count = total_count//15 #네이버 카페는 페이지당 게시물이 15개씩 존재함

    opening(id, pw)
    total = crawling_articles(page_count, menuid)
    print("크롤링 한 게시물은 {}개 입니다.".format(len(total)))  # 크롤링한 게시글 수 확인

    filename = category[cate][0]

    res_list = []
    # Beautifulsoup 활용
    for article in total:
        driver.get(article)
        # article도 switch_to_frame이 필수
        driver.switch_to_frame('cafe_main')
        soup = bs(driver.page_source, 'html.parser')
        # 게시글에서 제목 추출
        title = soup.select('span.b')[0].get_text()
        # 내용을 하나의 텍스트로 만든다. (띄어쓰기 단위)
        content_tags = soup.select('#tbody')[0].select('p')
        content = ' '.join([tags.get_text() for tags in content_tags])
        # dict형태로 만들어 결과 list에 저장
        res_list.append({'title': title, 'content': content})


    exportCSV(res_list, filename)










category = [['wgang_symptom_body','menuid=8', 430], ['wgang_symptom_mind', 'menuid=3', 102], ['wgang_bamboogrove_children', 'menuid=5', 266], ['wgang_bamboogrove_husband', 'menuid=6', 175], ['wgang_bamboogrove_family', 'menuid=21', 141], ['wgang_bamboogrove_workplace', 'menuid=7', 64], ['wgang_bamboogrove_money', 'menuid=32', 68]]
main(category)