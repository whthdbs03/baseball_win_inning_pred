from flask import Flask, jsonify
from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime, timedelta
# import subprocess
from kbo_scraper import get_today_games
from db_utils import get_win_probability
from inning_scheduler import start_scheduler

app = Flask(__name__)
scheduler = BackgroundScheduler()
scheduler.start()

TEAM_CODE_MAP = {
    'LG': 'LG',
    'OB': '두산',
    'SS': '삼성',
    'SK': 'SSG',
    'WO': '키움',
    'KT': 'KT',
    'HH': '한화',
    'HT': 'KIA',
    'NC': 'NC',
    'LT': '롯데'
}


def launch_scheduler_for_game(game_id, start_time):
    def run():
        print(f"🎯 [{game_id}] 경기 시작됨 → 스케줄러 실행")
        home_win_pred = 0.5  # 초기화

        # game_id에서 팀명매핑
        away_code = game_id[8:10]
        home_code = game_id[10:12]
        away_team = TEAM_CODE_MAP.get(away_code)
        home_team = TEAM_CODE_MAP.get(home_code)
        if away_team and home_team: # 잘 들어왔을 경우 예측값 db에서 받아오기
            home_win_pred = get_win_probability(home_team, away_team) # 경기 전 예측 값 (team1 == home 일 때 받아오기)

        # subprocess.Popen([
        #     'python', 'inning_scheduler.py',
        #     '--game_id', game_id,
        #     '--home_win_pred', str(home_win_pred)
        # ])
        start_scheduler(game_id, home_win_pred)

    scheduler.add_job(run, trigger='date', run_date=start_time)
    print(f"✅ {game_id} 예약됨 @ {start_time}")

# ✅ 매일 새벽 3시에 실행되는 함수
def register_today_games():
    today = datetime.now().date()
    games = get_today_games(today)  # [{'game_id': '20250603LGOB', 'start_time': datetime(...)}, ...]
    
    for game in games:
        launch_scheduler_for_game(game['game_id'], game['start_time'])

# 🕓 매일 새벽 3시 예약
scheduler.add_job(register_today_games, trigger='cron', hour=3, minute=0)

@app.route('/health')
def health():
    return jsonify({'jobs': len(scheduler.get_jobs())})

@app.route('/force_register', methods=['GET'])
def force_register():
    register_today_games()
    return "강제 경기 등록 하셨어요(테스트 또는 수동)"


@app.route('/')
def home():
    return "KBO 경기 중 승률 예측 API입니다. /force_register (GET) : 수동 스케줄러 호출을 원하시면 사용하세요."

# if __name__ == '__main__':
#     app.run(port=8080)
    
if __name__ == '__main__':
    # from waitress import serve
    # serve(app, host='0.0.0.0', port=8080)
    # register_today_games() # 크론 잡으로 app.py 을 3시마다 실행시키자 그냥 
    # 크론 잡 유료임 미친 것
    import os
    port = int(os.environ.get("PORT", 10000)) 
    app.run(host="0.0.0.0", port=port)
