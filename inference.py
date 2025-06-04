from realtime_crawling.get_realtimelog_df import get_realtimelog_df
import torch
import torch.nn as nn
import argparse
from db_utils import save_live_win_prediction

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
    
    save_live_win_prediction(game_id=game_id, inning=inning, win_prob=prob, 
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