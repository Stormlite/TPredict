import pandas as pd
import numpy as np

def compute_rolling_features(df: pd.DataFrame) -> pd.DataFrame:
    """Computes Head-to-Head ratios and 5-match win streaks chronologically."""
    # Ensure rows are sorted by date
    df = df.sort_values(by='tourney_date').reset_index(drop=True)
    
    h2h_winner_adv = []
    w_streak = []
    l_streak = []
    
    # Dictionaries to keep state up to that point in time
    player_history = {} # tracking recent match results [1=win, 0=loss]
    h2h_tracker = {}     # tracking matchups (playerA, playerB) -> wins
    
    for idx, row in df.iterrows():
        w_name = row['winner_name']
        l_name = row['loser_name']
        
        # 1. H2H Feature Calculation
        match_key = tuple(sorted([w_name, l_name]))
        if match_key not in h2h_tracker:
            h2h_tracker[match_key] = {w_name: 0, l_name: 0}
            
        w_h2h_wins = h2h_tracker[match_key][w_name]
        l_h2h_wins = h2h_tracker[match_key][l_name]
        
        # H2H advantage calculation
        h2h_diff = w_h2h_wins - l_h2h_wins
        h2h_winner_adv.append(h2h_diff)
        
        # 2. Rolling Form Streaks (Last 5 matches)
        w_strk = sum(player_history.get(w_name, [])[-5:])
        l_strk = sum(player_history.get(l_name, [])[-5:])
        w_streak.append(w_strk)
        l_streak.append(l_strk)
        
        # Update trackers for subsequent matches
        h2h_tracker[match_key][w_name] += 1
        if w_name not in player_history: player_history[w_name] = []
        if l_name not in player_history: player_history[l_name] = []
        player_history[w_name].append(1)
        player_history[l_name].append(0)
        
    df['h2h_winner_edge'] = h2h_winner_adv
    df['winner_streak'] = w_streak
    df['loser_streak'] = l_streak
    return df
