import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
import src.features as features

def clean_matches(df: pd.DataFrame) -> pd.DataFrame:
    """Keeps columns and drops rows missing critical rankings."""
    cols = ['tourney_date', 'winner_name', 'loser_name', 'surface', 'winner_rank', 'loser_rank']
    df_clean = df[cols].dropna(subset=['winner_rank', 'loser_rank']).copy()
    return df_clean.reset_index(drop=True)

def engineer_features(df: pd.DataFrame) -> pd.DataFrame:
    """Calculates chronological trends, then randomly balances matchups."""
    # 1. Compute advanced rolling histories chronologically
    df_advanced = features.compute_rolling_features(df)
    
    np.random.seed(42)
    p1_rank, p2_rank, rank_diff = [], [], []
    h2h_diff, p1_streak, p2_streak = [], [], []
    labels = []
    
    # 2. Balanced data-flipping loop
    for _, row in df_advanced.iterrows():
        if np.random.rand() > 0.5:
            p1_rank.append(row['winner_rank'])
            p2_rank.append(row['loser_rank'])
            rank_diff.append(row['winner_rank'] - row['loser_rank'])
            h2h_diff.append(row['h2h_winner_edge'])
            p1_streak.append(row['winner_streak'])
            p2_streak.append(row['loser_streak'])
            labels.append(1)
        else:
            p1_rank.append(row['loser_rank'])
            p2_rank.append(row['winner_rank'])
            rank_diff.append(row['loser_rank'] - row['winner_rank'])
            h2h_diff.append(-row['h2h_winner_edge'])
            p1_streak.append(row['loser_streak'])
            p2_streak.append(row['winner_streak'])
            labels.append(0)
            
    df_balanced = pd.DataFrame({
        'rank_diff': rank_diff,
        'h2h_diff': h2h_diff,
        'p1_streak': p1_streak,
        'p2_streak': p2_streak,
        'surface': df_advanced['surface'],
        'label': labels
    })
    
    return pd.get_dummies(df_balanced, columns=['surface'], prefix='surf')

def split_data(df: pd.DataFrame) -> tuple:
    """Splits columns safely into training and verification sets."""
    X = df.drop(columns=['label'])
    y = df['label']
    return train_test_split(X, y, test_size=0.2, random_state=42)
