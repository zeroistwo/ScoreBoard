from bs4 import BeautifulSoup as bs
from selenium import webdriver
import csv
import datetime
import time

# URL 변수
results_url = "https://www.scoreboard.com/kr/soccer/{nation}/{league}/results"
stnading_url = "https://www.scoreboard.com/kr/soccer/{nation}/{league}/standings"

# 기타 변수
NATION = "Input nation name: "
LEAGUE = "Input league name: "
RESULTSDATAFRAME = ['Round', 'Date', 'Time', 'Home_Team', 'Home_Score', 'Away_Score', 'Away_Team']
STANDINGSDATAFRAME = ['Position', 'Team', 'Played', 'Won', 'Drawn', 'Loss', 'Goals_For', 'Goals_Against', 'Points']
FILEROUTE = '/Users/admin/chromedriver'
results_more = '#tournament-page-results-more > tbody > tr > td > a'
year = '2018'
result_filename = 'ScoreBoard'
standing_filename = 'Position'

def crawlResults(nation_name, league_name):
    driver = webdriver.Chrome(FILEROUTE)
    url = results_url.format(nation = nation_name, league = league_name)
    driver.get(url)
    try:
        while True:
            # 전체 경기 결과 가져오기 위해 '더 많은 경기 보기' href 클릭
            driver.find_element_by_css_selector(results_more).click()
            time.sleep(10) # loading하는 시간 필요
    except Exception as e:
        print(e)
    try:
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
                raw_data.append(round_list)                                         # 1. Round
                raw_data.append(datetime.date(int(year), int(month), int(day)))     # 2. Date
                raw_data.append(datetime.time(int(hour), int(minute)))              # 3. Time
                raw_data.append(home_team.span.get_text().split('\xa0')[0])         # 4. Home_Team
                raw_data.append(home_score)                                         # 5. Home_Score
                raw_data.append(away_score)                                         # 6. Away_Score
                raw_data.append(away_team.span.get_text().split('\xa0')[0])         # 7. Away_Team
                game_list.append(raw_data)
            else:
                pass
        driver.close()
        return game_list
    except Exception as e:
        print(e)

def crawlStandings(nation_name, league_name):
    try:
        driver = webdriver.Chrome(FILEROUTE)
        url = results_url.format(nation = nation_name, league = league_name)
        driver.get(url)
        page = driver.page_source
        rank_soup = bs(page, 'html.parser')
        tr_list = rank_soup.find('table', id='table-type-1').find('tbody').findAll('tr')
        rank_list = []
        for tr_index in range(len(tr_list)):
            raw_data = []
            get_class = tr_list[tr_index].get('class')[0]
            if get_class == 'even' or 'odd':
                rank = tr_list[tr_index].find('td', class_='rank').get_text().split('.')[0]
                team_name = tr_list[tr_index].find('span', class_='team_name_span').get_text()
                played = tr_list[tr_index].find('td', class_='matches_played').get_text()
                won = tr_list[tr_index].find('td', class_='wins_regular').get_text()
                drawn = tr_list[tr_index].find('td', class_='draws').get_text()
                loss = tr_list[tr_index].find('td', class_='losses_regular').get_text()
                goals_for = tr_list[tr_index].findAll('td', class_='goals')[0].get_text().split(':')[0]
                goals_against = tr_list[tr_index].findAll('td', class_='goals')[0].get_text().split(':')[1]
                points = tr_list[tr_index].findAll('td', class_='goals')[1].get_text()
                raw_data.append(rank)
                raw_data.append(team_name)
                raw_data.append(played)
                raw_data.append(won)
                raw_data.append(drawn)
                raw_data.append(loss)
                raw_data.append(goals_for)
                raw_data.append(goals_against)
                raw_data.append(points)
                rank_list.append(raw_data)
            else:
                pass
        driver.close()
        return rank_list
    except Exception as e:
        print(e)

def saveAsCsv(list, league_name, filename, DATAFRAME):
    with open('{}_{}.csv'.format(filename, league_name), "w") as output:  # 크롤링한 결과물들을 csv파일의 형태로 저장
        writer = csv.writer(output, lineterminator='\n')
        writer.writerow(DATAFRAME)
        for index, val in enumerate(list):
            try:
                writer.writerow(val)
            except Exception as e:
                print('index: ', index)
                print(e)

if __name__ == "__main__":
    while True:
        nation_name_list = ('england', 'spain', 'germany', 'italy')
        league_name_list = ('premier-league', 'laliga', 'bundesliga', 'serie-a')

        for i in range(0, 4):
            nation_name = nation_name_list[i]
            league_name = league_name_list[i]

            print(nation_name, league_name)
            game_list = crawlResults(nation_name, league_name)
            rank_list = crawlStandings(nation_name, league_name)
            saveAsCsv(game_list, league_name, result_filename, RESULTSDATAFRAME)
            saveAsCsv(rank_list, league_name, standing_filename, STANDINGSDATAFRAME)
