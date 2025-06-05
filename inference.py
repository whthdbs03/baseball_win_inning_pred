from realtime_crawling.get_realtimelog_df import get_realtimelog_df
import torch
import torch.nn as nn
import argparse
from db_utils import save_live_win_prediction
import math

def inference_prob(model, game_df, feature_cols, home_win_pred):
    """
    지금까지의 경기 데이터를 기반으로 최종 승리 확률 하나 예측.

    Parameters:
        - model: 훈련된 GRU 모델
        - game_df: 현재까지 이닝 데이터를 담은 DataFrame
        - feature_cols: GRU에 넣을 feature 목록

    Returns:
        - pred_prob: 승리 확률 (float)
        - pred_label: 승/패 예측 (0 또는 1)
    """
    model.eval()

    game_df = game_df.sort_values(by=['inning', 'home_away'])
    X = game_df[feature_cols].astype('float32').values
    x_tensor = torch.tensor(X[None, :, :])  # (1, 시퀀스길이, feature_dim)

    with torch.no_grad():
        prob = model(x_tensor).item()
        pred = int(prob >= 0.5)
        # Sorry
        prob = prob*0.5 + home_win_pred*0.3 + 0.1

    return prob, pred

class GRUWinPredictor(nn.Module):
    def __init__(self, input_dim, hidden_dim=64):
        super().__init__()
        self.gru = nn.GRU(input_dim, hidden_dim, batch_first=True)
        self.fc = nn.Linear(hidden_dim, 1)
        self.sigmoid = nn.Sigmoid()

    def forward(self, x):
        out, _ = self.gru(x)
        out = out[:, -1, :]  # 마지막 timestep만
        return self.sigmoid(self.fc(out))
    
def setmodel():
    # torch.serialization.add_safe_globals({"GRUWinPredictor": GRUWinPredictor})
    # model = torch.load("model/gru_model_full.pt", weights_only=False)
    # model.eval()
    # return model
    model = GRUWinPredictor(input_dim=19)  # 실제 구조대로
    model.load_state_dict(torch.load("model/gru_model_full.pt"))
    model.eval()
    return model

def adjust_win_prob(P, score_diff, inning, total_innings=9, k=0.8):
    """
    P: 모델이 예측한 홈팀 승률 (0~1)
    score_diff: 홈 - 어웨이 점수차
    inning: 현재 이닝 (1~9)
    total_innings: 총 이닝 수 (기본은 9회)
    k: 점수차 반영 강도 (0.5~1 사이가 적당)
    """
    # 회차 진행에 따라 점수차 영향력 증가
    inning_weight = inning / total_innings
    # 점수차 기반 보정값 (시그모이드)
    score_factor = 1 / (1 + math.exp(-k * score_diff * inning_weight))
    # 예측값 보정
    adjusted = P * score_factor + (1 - P) * (1 - score_factor)
    return adjusted


def inference(inning, game_id, home_win_pred):
    realtimedf = get_realtimelog_df(inning, game_id)
    # inning = 1
    # game_id = "20250525NCOB0"
    # realtimedf 아래처럼 생김
    # inning  away_score  home_score  score_diff  home_away  res_2루타  ...  res_실책  res_안타  res_직선타아웃  res_파울  res_홈런  res_희생
    # 0       1           2           0          -2          1        0  ...       0       1          0       0       0       0
    # 1       1           2           0          -2          0        0  ...       0       2          0       0       0       0
    # [2 rows x 19 columns]
    print("df추출완")
    feature_cols = [
        'inning', 'away_score','home_score',  'score_diff', 'home_away', 
        'res_2루타','res_3루타','res_기타','res_땅볼아웃','res_뜬공아웃',
        'res_병살','res_볼넷사구','res_삼진','res_실책','res_안타',
        'res_직선타아웃','res_파울','res_홈런','res_희생'
    ]

    model = setmodel()
    print("모델 세팅완")
    prob, pred = inference_prob(model, realtimedf, feature_cols, home_win_pred)
    print(f"현재 시점 예측 → 확률: {prob:.4f}, 예측: {'승리' if pred >=0.5 else '패배'}")

    whth_prob = adjust_win_prob(prob,realtimedf['score_diff'].iloc[-1], inning)
    print(whth_prob)
    save_live_win_prediction(game_id=game_id, inning=inning, win_prob=whth_prob, 
                             home_accum_score=realtimedf['home_score'].iloc[-1],
                             away_accum_score=realtimedf['away_score'].iloc[-1])
    print(f"🏠 홈 최종 점수: {realtimedf['home_score'].iloc[-1]}")
    print(f"🧳 어웨이 최종 점수: {realtimedf['away_score'].iloc[-1]}")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--inning', type=int, required=True)
    parser.add_argument('--game_id', type=str, required=True)
    parser.add_argument('--home_win_pred', type=float, required=True, help='ex) 0.657')
    args = parser.parse_args()

    print(f"▶ 추론 중... {args.inning}회차 / 경기: {args.game_id}")
    
    
    inference(inning=args.inning, game_id=args.game_id, home_win_pred=args.home_win_pred)

# if __name__ == '__main__':
#     main()