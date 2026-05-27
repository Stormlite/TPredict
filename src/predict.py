import sys
import os
import pandas as pd
import joblib

# Force Python to recognize the current directory folders correctly
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import src.scraper as scraper
import src.strategy as strategy
import src.notifier as notifier # Imported the notification module

def get_live_player_stats(df_raw, player_name):
    """Finds the most recent rank and rolling win streak for a player from data."""
    p_matches = df_raw[(df_raw['winner_name'] == player_name) | (df_raw['loser_name'] == player_name)]
    if p_matches.empty:
        return 100, 2
        
    latest_match = p_matches.sort_values('tourney_date').iloc[-1]
    
    if latest_match['winner_name'] == player_name:
        rank = latest_match['winner_rank']
    else:
        rank = latest_match['loser_rank']
        
    recent_5 = p_matches.sort_values('tourney_date').tail(5)
    wins = sum(1 for _, m in recent_5.iterrows() if m['winner_name'] == player_name)
    
    return int(rank) if pd.notna(rank) else 100, wins

def get_h2h_edge(df_raw, p1, p2):
    """Calculates historical head-to-head win differential between two players."""
    p1_wins = len(df_raw[(df_raw['winner_name'] == p1) & (df_raw['loser_name'] == p2)])
    p2_wins = len(df_raw[(df_raw['winner_name'] == p2) & (df_raw['loser_name'] == p1)])
    return p1_wins - p2_wins

def main():
    model = joblib.load("models/rf_model.pkl")
    expected_features = model.feature_names_in_
    
    try:
        df_raw = pd.concat([pd.read_csv(f"data/raw/{f}") for f in os.listdir("data/raw") if f.endswith('.csv')])
    except:
        print("❌ Historical data folder empty. Run src/train.py first.")
        return

    print("⏳ Scanning live tournament schedules and calculating real-time player states...")
    
    # This safely uses the clean scraper module function we fixed!
    fixtures = scraper.fetch_live_fixtures()
    predicted_pool = []
    
    for f in fixtures:
        p1_rank, p1_streak = get_live_player_stats(df_raw, f['p1_name'])
        p2_rank, p2_streak = get_live_player_stats(df_raw, f['p2_name'])
        h2h_diff = get_h2h_edge(df_raw, f['p1_name'], f['p2_name'])
        
        input_data = {
            'rank_diff': [p1_rank - p2_rank],
            'h2h_diff': [h2h_diff],
            'p1_streak': [p1_streak],
            'p2_streak': [p2_streak],
            'surf_Clay': [1 if f['surface'] == 'Clay' else 0],
            'surf_Grass': [1 if f['surface'] == 'Grass' else 0],
            'surf_Hard': [1 if f['surface'] == 'Hard' else 0]
        }
        
        df_input = pd.DataFrame(input_data)
        for col in expected_features:
            if col not in df_input.columns:
                df_input[col] = 0
        df_input = df_input[expected_features]
        
        prob = model.predict_proba(df_input)[0]
        p1_conf = prob[1]
        p2_conf = prob[0]
        
        if p1_conf >= p2_conf:
            chosen_winner = f['p1_name']
            chosen_odds = f['p1_odds']
            confidence = p1_conf
        else:
            chosen_winner = f['p2_name']
            chosen_odds = f['p2_odds']
            confidence = p2_conf
            
        predicted_pool.append({
            'match_desc': f"{f['p1_name']} (Rank {p1_rank}) vs {f['p2_name']} (Rank {p2_rank}) [{f['surface']}]",
            'winner': chosen_winner, 
            'odds': chosen_odds, 
            'confidence': confidence
        })
        
    legs, slip_odds = strategy.generate_optimized_slip(predicted_pool, 2.0, 5.0)
    
    report_lines = [
        "=============================================", 
        "💰 AUTOMATED DAILY TICKET (SPORTYBET BASIS) 💰", 
        "============================================="
    ]
    for idx, leg in enumerate(legs, 1):
        report_lines.append(f"Leg {idx}: {leg['match_desc']}\n       👉 Pick: {leg['winner']} | Odds: {leg['odds']} (Confidence: {leg['confidence']*100:.1f}%)")
    report_lines.append("---------------------------------------------")
    report_lines.append(f"📈 Total Ticket Accumulator Odds: {slip_odds:.2f}x\n=============================================")
    
    report_output = "\n".join(report_lines)
    print(report_output)
    
    with open("daily_prediction_report.txt", "w", encoding="utf-8") as out_file:
        out_file.write(report_output)
        
    # Hooked up the WhatsApp delivery action directly below the file save
    print("📱 Forwarding generated ticket slips to your WhatsApp...")
    notifier.send_whatsapp_ticket(report_output)

if __name__ == "__main__":
    main()
