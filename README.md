# baseball_win_inning_pred

## <경기중 승률 예측 모델> live_win_predictions Table 사용
id INT PRIMARY KEY,
game_id VARCHAR(20), (20250603LGKT)
inning INT, (1~9…에서 12)
win_probability FLOAT, (현이닝기준home승률예측값)
home_accum_score INT, (현이닝누적스코어값)
away_accum_score INT, (현이닝누적스코어값)
predicted_at DATETIME

- 매일 3시(KST)에 자동으로 오늘의 경기들과 시작 시간을 확인하여 해당 시간이 되면 1분 간격으로 이닝이 업데이트됨을 확인하고 경기중 승률 예측값을 돌려 DB에 적재함
    - 경기전 승률 예측값이 충분히 DB에 적재되었음을 가정한 시각(3시)
- 웹서버: https://baseball-win-inning-pred.onrender.com/

### 1. GitHub Actions: 당일 경기 확인하고 스케줄러 예약

- 역할: 매일 정해진 시간(한국 시간 자정 03시 0분)에 KBO 사이트에서 경기 여부를 확인하고, 각 경기마다의 id와 시작 시간을 확인함. 시작 시간에 맞춰 inning_scheduler(경기 중 이닝이 끝남을 확인하고, 끝나면 추론 결과를 DB에 적재하는 함수)를 호출하도록 예약함
- 실행 과정:
    1. GitHub Actions는 force-register.yml 파일에 정의된 schedule 이벤트에 따라 주기적으로 워크플로우를 트리거함
    2. 워크플로우가 트리거되면, 렌더 서버를 깨우고(free 플랜이라 깨우는 과정 필요) /force_register 엔드포인트 호출(토큰 존재)
    3. 이때 GitHub Secrets에 저장된 DB_URI가 환경 변수로 주입됨
    4. /force_register는 get_today_games()로 그날 경기를 확인, 이후 경기마다 launch_scheduler_for_game()로 스케줄러 예약(시작 시간이 되면 경기전 승률 예측값을 DB에서 받아옴) . 이닝 스케줄러가 실행되면(경기가 시작하면) run_inference_if_inning_finished()으로 이닝이 끝났는지 확인, 끝났으면 run_inference()로 추론 코드 실행(이때 모델pt파일 등을 불러와서 적절히 추론값 도출).
    5. 최종적으로 db_utils.py를 사용하여 가공 및 예측된 데이터를 MySQL 데이터베이스에 갱신 및 적재

### 2. Work Flow

1. GitHub: 코드 푸시 (app.py, tasks.py, db_utils.py, yml 등)
2. Render: GitHub에서 최신 app.py를 받아 웹 API 서버로 배포 및 실행 (API 요청 처리)
3. GitHub Actions:
    - yml 파일의 schedule에 따라 특정 시각에 워크플로우 트리거
    - tasks.py 실행 (크롤링 → 데이터 처리 → 예측 모델링 → DB 적재)
    - Secrets의 DB_URI를 사용하여 DB에 연결
