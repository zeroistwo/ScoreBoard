from bs4 import BeautifulSoup as bs
from selenium import webdriver
import csv
import datetime
import time

# URL 변수
results_url = "https://www.scoreboard.com/kr/soccer/"

# 기타 변수
NATION = "Input nation name: "
LEAGUE = "Input league name: "
DATAFRAME = ['Round', 'Date', 'Time', 'Home_Team', 'Home_Score', 'Away_Score', 'Away_Team']
FILEROUTE = '/Users/admin/chromedriver'
results_more = '#tournament-page-results-more > tbody > tr > td > a'
year = '2018'
filename = 'ScoreBoard'

def crawlResults(nation_name, league_name):
    driver = webdriver.Chrome(FILEROUTE)
    url = results_url + nation_name + '/' + league_name + '/results/'
    driver.get(url)
    try:
        while True:
            # 전체 경기 결과 가져오기 위해 '더 많은 경기 보기' href 클릭
            driver.find_element_by_css_selector(results_more).click()
            time.sleep(10) # loading하는 시간 필요
    except Exception as e:
        print(e)
    page = driver.page_source
    league_soup = bs(page, 'html.parser')
    tr_list = league_soup.find('tbody').findAll('tr')
    game_list = []
    for tr_index in range(len(tr_list)):
        raw_data = []
        get_class = tr_list[tr_index].get('class')[0]
        if get_class == 'event_round':
            round_list = tr_list[tr_index].td.get_text().split(' ')[0]
        elif get_class == 'even' or 'odd':
            daytime = tr_list[tr_index].find('td', class_='cell_ad')
            home_team = tr_list[tr_index].find('td', class_='cell_ab')
            away_team = tr_list[tr_index].find('td', class_='cell_ac')
            home_score = tr_list[tr_index].find('td', class_='cell_sa').get_text().split('\xa0')[0]
            away_score = tr_list[tr_index].find('td', class_='cell_sa').get_text().split('\xa0')[2]
            month = daytime.get_text().split('. ')[0].split('.')[1]
            day = daytime.get_text().split('. ')[0].split('.')[0]
            hour = daytime.get_text().split('. ')[1].split(':')[0]
            minute = daytime.get_text().split('. ')[1].split(':')[1]
            raw_data.append(round_list)
            raw_data.append(datetime.date(int(year), int(month), int(day)))
            raw_data.append(datetime.time(int(hour), int(minute)))
            raw_data.append(home_team.span.get_text().split('\xa0')[0])
            raw_data.append(home_score)
            raw_data.append(away_score)
            raw_data.append(away_team.span.get_text().split('\xa0')[0])
            game_list.append(raw_data)
        else:
            pass
    driver.close()
    return game_list

def saveAsCsv(game_list, league_name):
    with open('{}_{}.csv'.format(filename, league_name), "w") as output:  # 크롤링한 결과물들을 csv파일의 형태로 저장
        writer = csv.writer(output, lineterminator='\n')
        writer.writerow(DATAFRAME)
        for index, val in enumerate(game_list):
            try:
                writer.writerow(val)
            except Exception as e:
                print('index: ', index)
                print(e)

if __name__ == "__main__":
    while True:
        nation_name = input(NATION)
        league_name = input(LEAGUE)
        game_list = crawlResults(nation_name, league_name)
        saveAsCsv(game_list, league_name)