from bs4 import BeautifulSoup as bs
from selenium import webdriver
import csv
import datetime
import time
import sys

# URL 변수
results_url = "https://www.scoreboard.com/kr/soccer/{nation}/{league}/{source}"
stnading_url = "https://www.scoreboard.com/kr/soccer/{nation}/{league}/standings"

# 기타 변수
RESULTSDATAFRAME = ['Round', 'Date', 'Time', 'Home_Team', 'Home_Score', 'Away_Score', 'Away_Team', 'Has_Extra', 'Extra_Home_Score', 'Extra_Away_Score']
FIXTURESDATAFRAME = ['Round', 'Date', 'Time', 'Home_Team', 'Away_Team']
STANDINGSDATAFRAME = ['Position', 'Team', 'Played', 'Won', 'Drawn', 'Loss', 'Goals_For', 'Goals_Against', 'Points']
FILEROUTE = '/Users/admin/chromedriver'
results_more = '#tournament-page-results-more > tbody > tr > td > a'
year = '2018'
result_filename = 'ScoreBoard'
standing_filename = 'Position'

def crawlResults(nation_name, league_name, source_name):
    # 서버 실행 시 필요
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    browser = webdriver.Chrome(chrome_options=chrome_options)

    driver = webdriver.Chrome()

    url = results_url.format(nation=nation_name, league=league_name, source=source_name)
    driver.get(url)
    try:
        for_loop = True
        while True:
            # 전체 경기 결과 가져오기 위해 '더 많은 경기 보기' href 클릭
            elem = driver.find_element_by_css_selector(results_more)
            if elem:
                driver.find_element_by_css_selector(results_more).click()
                for_loop = True
                time.sleep(10) # loading하는 시간 필요
            else:
                for_loop = False
                time.sleep(10) # loading하는 시간 필요
    except Exception as e:
        print(e)
    try:
        time.sleep(5) # loading하는 시간 필요
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
                if source_name == 'results':
                    daytime = tr_list[tr_index].find('td', class_='cell_ad')
                    home_team = tr_list[tr_index].find('td', class_='cell_ab')
                    away_team = tr_list[tr_index].find('td', class_='cell_ac')

                    score_str = tr_list[tr_index].find('td', class_='cell_sa').get_text()
                    score_str2 = score_str.replace('\xa0', '')
                    score_str3 = score_str2.split('(')

                    if len(score_str3) > 1:
                        score_str4 = score_str3[1].split(')')
                        scores = score_str3[0].split(':')
                        home_score = scores[0]
                        away_score = scores[1]
                        scores2 = score_str4[0].split(':')
                        extra_home_score = scores2[0]
                        extra_away_score = scores2[1]
                        has_extra = '1'
                    else:
                        scores = score_str3[0].split(':')
                        home_score = scores[0]
                        away_score = scores[1]
                        has_extra = '0'
                        extra_home_score = '0'
                        extra_away_score = '0'

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
                    raw_data.append(has_extra)                                          # 8. 연장전 여부
                    raw_data.append(extra_home_score)                                   # 9. 연장전 홈팀 점수
                    raw_data.append(extra_away_score)                                   # 10. 연장전 어웨이팀 점수
                    game_list.append(raw_data)
                else:
                    daytime = tr_list[tr_index].find('td', class_='cell_ad')
                    home_team = tr_list[tr_index].find('td', class_='cell_ab')
                    away_team = tr_list[tr_index].find('td', class_='cell_ac')
                    month = daytime.get_text().split('. ')[0].split('.')[1]
                    day = daytime.get_text().split('. ')[0].split('.')[0]
                    hour = daytime.get_text().split('. ')[1].split(':')[0]
                    minute = daytime.get_text().split('. ')[1].split(':')[1]
                    raw_data.append(round_list)                                         # 1. Round
                    raw_data.append(datetime.date(int(year), int(month), int(day)))     # 2. Date
                    raw_data.append(datetime.time(int(hour), int(minute)))              # 3. Time
                    raw_data.append(home_team.span.get_text().split('\xa0')[0])         # 4. Home_Team
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

        # 서버 실행 시 필요
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        browser = webdriver.Chrome(chrome_options=chrome_options)

        driver = webdriver.Chrome()
        url = stnading_url.format(nation=nation_name, league=league_name)
        driver.get(url)
        time.sleep(20)  # loading하는 시간 필요
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

def saveAsCsv(list, nation_name, league_name, source_name, year, filename, DATAFRAME):
    with open('c:\\dev\\temp\\{}_{}_{}_{}_{}.csv'.format(nation_name, filename, league_name, source_name, year), "w", newline='', encoding='utf-8') as output:  # 크롤링한 결과물들을 csv파일의 형태로 저장
        writer = csv.writer(output, lineterminator='\n')
        writer.writerow(DATAFRAME)
        for index, val in enumerate(list):
            try:
                writer.writerow(val)
            except Exception as e:
                print('index: ', index)
                print(e)

if __name__ == "__main__":
    nation_name_list = ('south-korea', 'england', 'england', 'spain', 'germany', 'italy')
    league_name_list = ('korean-cup', 'fa-cup', 'premier-league', 'laliga', 'bundesliga', 'serie-a')
    source_name_list = ('results', 'fixtures')

    nation_name = nation_name_list[int(sys.argv[1])]
    league_name = league_name_list[int(sys.argv[2])]
    source_name = source_name_list[int(sys.argv[3])]
    year = sys.argv[4]

    game_result_list = crawlResults(nation_name, league_name, source_name)
    if source_name == 'results':
        saveAsCsv(game_result_list, nation_name, league_name, source_name, year, result_filename, RESULTSDATAFRAME)
    elif source_name == 'fixtures':
        saveAsCsv(game_result_list, nation_name, league_name, source_name, year, result_filename, FIXTURESDATAFRAME)

    #rank_list = crawlStandings(nation_name, league_name)
    #saveAsCsv(rank_list, league_name, standing_filename, STANDINGSDATAFRAME)