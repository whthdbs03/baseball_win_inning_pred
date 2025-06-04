from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from datetime import datetime
import time
from datetime import date
from realtime_crawling.get_log import get_driver

def get_today_games(today_date):
    driver = get_driver() # webdriver.Chrome()
    date_str = today_date.strftime('%Y-%m-%d')
    url = f"https://www.koreabaseball.com/Schedule/GameCenter/Main.aspx?seriesId=0&gameDate={date_str}"
    # https://www.koreabaseball.com/Schedule/GameCenter/Main.aspx
    driver.get(url)
    wait = WebDriverWait(driver, 10)

    # 예시: 각 경기의 시작 시각과 game_id 파싱
    games = []
    try:
        # 열린 페이지의 날짜와 입력받은 날짜가 같은지 확인: 예정된 경기가 아예 없으면 경기가 존재하는 다른 날짜 페이지가 뜨기 때문
        # //*[@id="lblGameDate"]
        # /html/body/form/div[3]/section/div/div/div[2]/ul/li[2]/span
        # <span id="lblGameDate" class="date-txt">2025.06.03(화)</span>
        lbl = driver.find_element(By.ID, "lblGameDate").text  # 예: "2025.06.03(화)"
        lbl_date = datetime.strptime(lbl.split('(')[0], '%Y.%m.%d').date()
        if lbl_date != today_date:
            print(f"📛 날짜 불일치: {lbl_date} != {today_date}")
            driver.quit()
            return []
        # print("날짜 일치")


        # 예정된 경기 5개의 gameID와 예정시각을 따기
        # /html/body/form/div[3]/section/div/div/div[3]/div/div[1]/ul 의 하위
        # for 문
        # /html/body/form/div[3]/section/div/div/div[3]/div/div[1]/ul/li[1]/div[1]/ul/li[3]
        # 위 위치로 접근하면 <li>14:00</li> 라고 써진 게 보임
        # /html/body/form/div[3]/section/div/div/div[3]/div/div[1]/ul/li[1]/div[2]/div[2]/div[1]/div[1]/img
        # /html/body/form/div[3]/section/div/div/div[3]/div/div[1]/ul/li[1]/div[2]/div[2]/div[3]/div[1]/img
        # 위 두 경로는 한 경기의 양 팀의 이미지임. 여기에 뭐라 써있냐면 :
        # <img src="//6ptotvmi5753.edge.naverncp.com/KBO_IMAGE/emblem/regular/2025/emblem_LG.png" alt="LG">
        # <img src="//6ptotvmi5753.edge.naverncp.com/KBO_IMAGE/emblem/regular/2025/emblem_NC.png" alt="NC">
        # 이렇게 쓰여있음. 내 생각엔 여기서 alt를 읽어와야함.
        # 이들을 다 읽어서 game_id : '20250603LGNC'와 시작시간 14:00 을 가져오면 됨.

        # 이렇게 하려했는데? /html/body/form/div[3]/section/div/div/div[3]/div/div[1]/ul/li[1] 이 위치에 다 있어.

        game_list = driver.find_elements(By.XPATH, '/html/body/form/div[3]/section/div/div/div[3]/div/div[1]/ul/li')
        # print(game_list)
        for li in game_list:
            try:
                game_id_raw = li.get_attribute("g_id")  # ex: 20250603LGNC0
                start_time_text = li.find_element(By.XPATH, './/ul/li[3]').text.strip()  # ex: '14:00'

                # ▶ game_id는 뒤에 0 붙어있는데 그냥 쓰든가 자르면 됨
                game_id = game_id_raw[:12]  # '20250603LGNC'

                start_time = datetime.strptime(start_time_text, "%H:%M").time()
                full_start = datetime.combine(today_date, start_time)

                games.append({
                    'game_id': game_id,
                    'start_time': full_start
                })
            except Exception as e:
                print(f"⚠️ 경기 파싱 중 오류: {e}")
                continue

    except Exception as e:
        print(f"❌ 전체 파싱 실패: {e}")

    driver.quit()
    return games

# games = get_today_games(date(2025, 6, 3))
# print(games)
