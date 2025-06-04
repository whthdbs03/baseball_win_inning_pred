from kbo_scraper import get_today_games
from datetime import date
games = get_today_games(date(2025, 6, 3))
print(games)
2025-06-04
2025-06-04
{'game_id': '20250604HTOB', 'away': 'KIA', 'home': '두산', 'stadium': '잠실', 'start_time': '18:30', 'status': '정규경기'}
{'game_id': '20250604SSSK', 'away': '삼성', 'home': 'SSG', 'stadium': '문학', 'start_time': '18:30', 'status': '정규경기'}
{'game_id': '20250604WOLT', 'away': '키움', 'home': '롯데', 'stadium': '사직', 'start_time': '18:30', 'status': '정규경기'}
{'game_id': '20250604LGNC', 'away': 'LG', 'home': 'NC', 'stadium': '창원', 'start_time': '18:30', 'status': '정규경기'}
{'game_id': '20250604KTHH', 'away': 'KT', 'home': '한화', 'stadium': '대전(신)', 'start_time': '18:30', 'status': '정규경기'}
