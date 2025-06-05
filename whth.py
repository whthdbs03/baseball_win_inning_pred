# from kbo_scraper import get_today_games
# from datetime import date
# games = get_today_games(date(2025, 6, 4))
# print(games)
# 2025-06-04
# 2025-06-04
# game_list = [{'game_id': '20250604HTOB', 'away': 'KIA', 'home': '두산', 'stadium': '잠실', 'start_time': '18:30', 'status': '정규경기'}, {'game_id': '20250604SSSK', 'away': '삼성', 'home': 'SSG', 'stadium': '문학', 'start_time': '18:30', 'status': '정규경기'}, {'game_id': '20250604WOLT', 'away': '키움', 'home': '롯데', 'stadium': '사직', 'start_time': '18:30', 'status': '정규경기'}, {'game_id': '20250604LGNC', 'away': 'LG', 'home': 'NC', 'stadium': '창원', 'start_time': '18:30', 'status': '정규경 기'}, {'game_id': '20250604KTHH', 'away': 'KT', 'home': '한화', 'stadium': '대전(신)', 'start_time': '18:30', 'status': '정규경기'}]
game_list = [{'game_id': '20250605HTOB', 'away': 'KIA', 'home': '두산', 'stadium': '잠실', 'start_time': '18:30', 'status': '정규경기'}, {'game_id': '20250605SSSK', 'away': '삼성', 'home': 'SSG', 'stadium': '문학', 'start_time': '18:30', 'status': '정규경기'}, {'game_id': '20250605WOLT', 'away': '키움', 'home': '롯데', 'stadium': '사직', 'start_time': '18:30', 'status': '정규경기'}, {'game_id': '20250605LGNC', 'away': 'LG', 'home': 'NC', 'stadium': '창원', 'start_time': '18:30', 'status': '정규경기'}, {'game_id': '20250605KTHH', 'away': 'KT', 'home': '한화', 'stadium': '대전(신)', 'start_time': '18:30', 'status': '정규 경기'}]
# [0.3073, 0.3481, 0.6772, 0.3678, 0.7572]
from db_utils import get_win_probability

win_prob = []
for i in range(5):
    
    win_prob.append(0.01*get_win_probability(game_list[i]['home'], game_list[i]['away']))
print(win_prob)

from inference import inference
for i in range(5):
    for j in range(8):
        print(i,j)
        inference(j+1, game_list[i]['game_id'], win_prob[i])
