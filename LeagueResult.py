from bs4 import BeautifulSoup as bs
from selenium import webdriver
import csv
import datetime
import time

# URL 변수
laliga_url = "https://www.scoreboard.com/kr/soccer/spain/laliga/results/"

# 기타 변수
DATAFRAME = ['Date', 'Time', 'Home_Team', 'Home_Score', 'Away_Score', 'Away_Team']
FILEROUTE = '/Users/admin/chromedriver'
results_more = '#tournament-page-results-more > tbody > tr > td > a'
year = '2018'
filename = 'ScoreBoard'

def crawlScoreBoard():
    driver = webdriver.Chrome(FILEROUTE)
    driver.get(laliga_url)
    driver.find_element_by_css_selector(results_more).click()
    time.sleep(10)
    page = driver.page_source
    laliga_soup = bs(page, 'html.parser')

    tr_list = laliga_soup.find('tbody').findAll('tr')
    game_list = []
    for tr_index in range(len(tr_list)):
        raw_data = []
        get_class = tr_list[tr_index].get('class')[0]
        if get_class == 'event_round':
            raw_data.append(tr_list[tr_index].td.get_text().split(' ')[0])
            game_list.append(raw_data)
        elif get_class == 'even':
            even_daytime = tr_list[tr_index].find('td', class_='cell_ad')
            even_home_team = tr_list[tr_index].find('td', class_='cell_ab')
            even_away_team = tr_list[tr_index].find('td', class_='cell_ac')
            even_home_score = tr_list[tr_index].find('td', class_='cell_sa').get_text().split('\xa0')[0]
            even_away_score = tr_list[tr_index].find('td', class_='cell_sa').get_text().split('\xa0')[2]
            even_month = even_daytime.get_text().split('. ')[0].split('.')[1]
            even_day = even_daytime.get_text().split('. ')[0].split('.')[0]
            even_hour = even_daytime.get_text().split('. ')[1].split(':')[0]
            even_minute = even_daytime.get_text().split('. ')[1].split(':')[1]
            raw_data.append(datetime.date(int(year), int(even_month), int(even_day)))
            raw_data.append(datetime.time(int(even_hour), int(even_minute)))
            raw_data.append(even_home_team.span.get_text().split('\xa0')[0])
            raw_data.append(even_home_score)
            raw_data.append(even_away_score)
            raw_data.append(even_away_team.span.get_text().split('\xa0')[0])
            game_list.append(raw_data)
        elif get_class == 'odd':
            odd_daytime = tr_list[tr_index].find('td', class_='cell_ad')
            odd_home_team = tr_list[tr_index].find('td', class_='cell_ab')
            odd_away_team = tr_list[tr_index].find('td', class_='cell_ac')
            odd_home_score = tr_list[tr_index].find('td', class_='cell_sa').get_text().split('\xa0')[0]
            odd_away_score = tr_list[tr_index].find('td', class_='cell_sa').get_text().split('\xa0')[2]
            odd_month = odd_daytime.get_text().split('. ')[0].split('.')[1]
            odd_day = odd_daytime.get_text().split('. ')[0].split('.')[0]
            odd_hour = odd_daytime.get_text().split('. ')[1].split(':')[0]
            odd_minute = odd_daytime.get_text().split('. ')[1].split(':')[1]
            raw_data.append(datetime.date(int(year), int(odd_month), int(odd_day)))
            raw_data.append(datetime.time(int(odd_hour), int(odd_minute)))
            raw_data.append(odd_home_team.span.get_text().split('\xa0')[0])
            raw_data.append(odd_home_score)
            raw_data.append(odd_away_score)
            raw_data.append(odd_away_team.span.get_text().split('\xa0')[0])
            game_list.append(raw_data)
        else:
            pass
    return game_list

def saveAsCsv(game_list):
    with open('{}.csv'.format(filename), "w") as output:  # 크롤링한 결과물들을 csv파일의 형태로 저장
        writer = csv.writer(output, lineterminator='\n')
        writer.writerow(DATAFRAME)
        for index, val in enumerate(game_list):
            try:
                writer.writerow(val)
            except Exception as e:
                print('index: ', index)
                print(e)

if __name__ == "__main__":
    game_list = crawlScoreBoard()
    saveAsCsv(game_list)