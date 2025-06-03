from app import launch_scheduler_for_game
from datetime import datetime

launch_scheduler_for_game('20250603HTOB',datetime(2025, 6, 3, 19, 20))
launch_scheduler_for_game('20250603SSSK',datetime(2025, 6, 3, 19, 20))
launch_scheduler_for_game('20250603WOLT',datetime(2025, 6, 3, 19, 20))
launch_scheduler_for_game('20250603LGNC',datetime(2025, 6, 3, 19, 20))
launch_scheduler_for_game('20250603KTHH',datetime(2025, 6, 3, 19, 20))
'''
[{'game_id': '20250603LGNC', 'start_time': datetime.datetime(2025, 6, 3, 14, 0)}, {'game_id': '20250603KTHH', 'start_time': datetime.datetime(2025, 6, 3, 14, 0)}, {'game_id': '20250603HTOB', 'start_time': datetime.datetime(2025, 6, 3, 17, 0)}, {'game_id': '20250603SSSK', 'start_time': datetime.datetime(2025, 6, 3, 17, 0)}, {'game_id': '20250603WOLT', 'start_time': datetime.datetime(2025, 6, 3, 17, 0)}]
✅ 20250603HTOB 예약됨 @ 2025-06-03 19:00:00
✅ 20250603SSSK 예약됨 @ 2025-06-03 19:00:00
✅ 20250603WOLT 예약됨 @ 2025-06-03 19:00:00
✅ 20250603LGNC 예약됨 @ 2025-06-03 19:00:00
✅ 20250603KTHH 예약됨 @ 2025-06-03 19:00:00
왜 예약거는데 리스트를 따오지?
'''

# from inning_scheduler import get_current_inning
# print(get_current_inning('20250603HTOB')) # 5 얘도 동작 잘 함

# from inning_scheduler import run_inference
# run_inference(5, '20250603HTOB', 0.6777)
'''
🎯 [5회 종료] 추론 시작 (game_id=20250603HTOB)

DevTools listening on ws://127.0.0.1:54028/devtools/browser/809fa65d-cb13-4c42-93fa-9e971ec3a8c1
5회까지 어웨이 누적점수: 6
5회까지 홈 누적점수: 2
df추출완
모델 세팅완
현재 시점 예측 → 확률: 0.9668, 예측: 패배
DEBUG: Using DB URI: mysql+pymysql://root:****@dugout-dev.cn6mm486utfi.ap-northeast-2.rds.amazonaws.com:3306/dugoutDB?charset=utf8
✅ 실시간 예측 결과 저장 완료: 20250603HTOB, 5회, 0.903
잘돌아가는듯
'''