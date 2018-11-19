from bs4 import BeautifulSoup as bs
from selenium import webdriver
import csv
import datetime
import time

# 기타 변수
DATAFRAME = ['Date', 'Time', 'Home_Team', 'Home_Score', 'Away_Score', 'Away_Team']
FILEROUTE = '/Users/admin/chromedriver'
results_more = '#tournament-page-results-more > tbody > tr > td > a'
year = '2018'
filename = 'ScoreBoard_Laliga'

def compareLength(factor_one, factor_two):
    if len(factor_one) > len(factor_two):
        return len(factor_two)
    else:
        return len(factor_one)

def crawlScoreBoard():
    laliga_url = "https://www.scoreboard.com/kr/soccer/spain/laliga/results/"
    driver = webdriver.Chrome(FILEROUTE)
    driver.get(laliga_url)
    driver.find_element_by_css_selector(results_more).click()
    time.sleep(10)
    page = driver.page_source
    laliga_soup = bs(page, 'html.parser')
    # round = laliga_soup.findAll('tr', class_='event_round')
    # round_list = []
    # for i in range(len(round)):
    #     round_list.append(round[i].get_text())
    odd_class = laliga_soup.findAll('tr', class_='odd')
    even_class = laliga_soup.findAll('tr', class_='even')
    class_length = compareLength(odd_class, even_class)

    try:
        game_list = []
        for index in reversed(range(class_length)):
            odd_daytime = odd_class[index].findAll('td', class_='cell_ad')
            odd_home_team = odd_class[index].findAll('td', class_='cell_ab')
            odd_away_team = odd_class[index].findAll('td', class_='cell_ac')
            odd_home_score = odd_class[index].find('td', class_='cell_sa').get_text().split('\xa0')[0]
            odd_away_score = odd_class[index].find('td', class_='cell_sa').get_text().split('\xa0')[2]

            even_daytime = even_class[index].findAll('td', class_='cell_ad')
            even_home_team = even_class[index].findAll('td', class_='cell_ab')
            even_away_team = even_class[index].findAll('td', class_='cell_ac')
            even_home_score = even_class[index].find('td', class_='cell_sa').get_text().split('\xa0')[0]
            even_away_score = even_class[index].find('td', class_='cell_sa').get_text().split('\xa0')[2]

            daytime_length = compareLength(odd_daytime, even_daytime)
            for raw_index in range(daytime_length):
                raw_data = []
                even_month = even_daytime[raw_index].get_text().split('. ')[0].split('.')[1]
                even_day = even_daytime[raw_index].get_text().split('. ')[0].split('.')[0]
                even_hour = even_daytime[raw_index].get_text().split('. ')[1].split(':')[0]
                even_minute = even_daytime[raw_index].get_text().split('. ')[1].split(':')[1]
                raw_data.append(datetime.date(int(year), int(even_month), int(even_day)))
                raw_data.append(datetime.time(int(even_hour), int(even_minute)))
                raw_data.append(even_home_team[raw_index].span.get_text().split('\xa0')[0])
                raw_data.append(even_home_score)
                raw_data.append(even_away_score)
                raw_data.append(even_away_team[raw_index].span.get_text().split('\xa0')[0])
                game_list.append(raw_data)

                raw_data = []
                odd_month = odd_daytime[raw_index].get_text().split('. ')[0].split('.')[1]
                odd_day = odd_daytime[raw_index].get_text().split('. ')[0].split('.')[0]
                odd_hour = odd_daytime[raw_index].get_text().split('. ')[1].split(':')[0]
                odd_minute = odd_daytime[raw_index].get_text().split('. ')[1].split(':')[1]
                raw_data.append(datetime.date(int(year), int(odd_month), int(odd_day)))
                raw_data.append(datetime.time(int(odd_hour), int(odd_minute)))
                raw_data.append(odd_home_team[raw_index].span.get_text().split('\xa0')[0])
                raw_data.append(odd_home_score)
                raw_data.append(odd_away_score)
                raw_data.append(odd_away_team[raw_index].span.get_text().split('\xa0')[0])
                game_list.append(raw_data)

    except Exception as e:
        print(e)

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