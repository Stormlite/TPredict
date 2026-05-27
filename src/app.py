# import sys
# import os
# import pandas as pd
# import joblib
# import streamlit as st

# # Force Python to recognize the current directory folders correctly
# sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# import src.scraper as scraper
# import src.strategy as strategy

# # Page configurations
# st.set_page_config(page_title="Tennis ML Predictor", page_icon="🎾", layout="wide")

# st.title("🎾 Advanced Tennis ML Predictor & Betting Bot")
# st.markdown("This dashboard scans active tournament matches, computes win probabilities using historical ranking trends, and isolates optimized 2x–5x SportyBet tickets.")

# # Sidebar Controls
# st.sidebar.header("🎯 Ticket Parameters")
# min_odds = st.sidebar.slider("Minimum Accumulator Odds", 1.5, 3.0, 2.0, 0.1)
# max_odds = st.sidebar.slider("Maximum Accumulator Odds", 3.1, 10.0, 5.0, 0.1)

# if st.button("🚀 Scan Matches & Generate Ticket"):
#     try:
#         model = joblib.load("models/rf_model.pkl")
#         expected_features = model.feature_names_in_
#     except FileNotFoundError:
#         st.error("❌ Model file not found! Please run 'python src/train.py' in your terminal first to train the machine learning model.")
#         st.stop()

#     st.write("⏳ Scanning live tournament schedules and calculating features...")
#     fixtures = scraper.fetch_live_fixtures()
#     predicted_pool = []
    
#     # Run data parsing
#     for f in fixtures:
#         input_data = {
#             'rank_diff': [f['p1_rank'] - f['p2_rank']],
#             'h2h_diff': [0.0],
#             'p1_streak': [2.0],
#             'p2_streak': [2.0],
#             'surf_Clay': [1 if f['surface'] == 'Clay' else 0],
#             'surf_Grass': [1 if f['surface'] == 'Grass' else 0],
#             'surf_Hard': [1 if f['surface'] == 'Hard' else 0]
#         }
        
#         df_input = pd.DataFrame(input_data)
#         for col in expected_features:
#             if col not in df_input.columns:
#                 df_input[col] = 0
#         df_input = df_input[expected_features]
        
#         prob = model.predict_proba(df_input)[0]
#         p1_conf, p2_conf = prob[1], prob[0]
        
#         if p1_conf >= p2_conf:
#             chosen_winner, chosen_odds, confidence = f['p1_name'], f['p1_odds'], p1_conf
#         else:
#             chosen_winner, chosen_odds, confidence = f['p2_name'], f['p2_odds'], p2_conf
            
#         predicted_pool.append({
#             'match_desc': f"{f['p1_name']} vs {f['p2_name']} ({f['surface']})",
#             'p1': f['p1_name'], 'p1_odds': f['p1_odds'],
#             'p2': f['p2_name'], 'p2_odds': f['p2_odds'],
#             'winner': chosen_winner, 'odds': chosen_odds, 'confidence': confidence
#         })

#     # Layout: Split into two columns on the web page
#     col1, col2 = st.columns([3, 2])

#     with col1:
#         st.subheader("📋 Today's Match Predictions")
#         for p in predicted_pool:
#             with st.container(border=True):
#                 st.markdown(f"**{p['match_desc']}**")
#                 st.write(f"🟢 Predicted Winner: **{p['winner']}** (Odds: {p['odds']})")
#                 st.progress(float(p['confidence']))
#                 st.caption(f"Model Confidence: {p['confidence']*100:.1f}%")

#     with col2:
#         st.subheader("💰 SportyBet Accumulator Slip")
#         legs, slip_odds = strategy.generate_optimized_slip(predicted_pool, min_odds, max_odds)
        
#         if legs:
#             for idx, leg in enumerate(legs, 1):
#                 st.info(f"**Leg {idx}:** {leg['match_desc']}\n\nSelection: **{leg['winner']}** | Odds: {leg['odds']}")
#             st.success(f"### 📈 Combined Slip Odds: {slip_odds:.2f}x")
#         else:
#             st.warning("No combinations found matching your slider range filters. Try widening your odds parameters.")


import sys
import os
import pandas as pd
import joblib
import streamlit as st

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import src.scraper as scraper
import src.strategy as strategy
import src.predict as predict

st.set_page_config(page_title="Tennis ML Predictor", page_icon="🎾", layout="wide")
st.title("🎾 Advanced Tennis ML Predictor & Betting Bot")

st.sidebar.header("🎯 Ticket Parameters")
min_odds = st.sidebar.slider("Minimum Accumulator Odds", 1.5, 3.0, 2.0, 0.1)
max_odds = st.sidebar.slider("Maximum Accumulator Odds", 3.1, 10.0, 5.0, 0.1)

if st.button("🚀 Scan Matches & Generate Ticket"):
    try:
        model = joblib.load("models/rf_model.pkl")
        expected_features = model.feature_names_in_
        df_raw = pd.concat([pd.read_csv(f"data/raw/{f}") for f in os.listdir("data/raw") if f.endswith('.csv')])
    except Exception as e:
        st.error("❌ Pre-requisites missing. Make sure your models and data folder are ready.")
        st.stop()

    fixtures = scraper.fetch_live_fixtures()
    predicted_pool = []
    
    for f in fixtures:
        p1_rank, p1_streak = predict.get_live_player_stats(df_raw, f['p1_name'])
        p2_rank, p2_streak = predict.get_live_player_stats(df_raw, f['p2_name'])
        h2h_diff = predict.get_h2h_edge(df_raw, f['p1_name'], f['p2_name'])
        
        input_data = {
            'rank_diff': [p1_rank - p2_rank], 'h2h_diff': [h2h_diff], 'p1_streak': [p1_streak], 'p2_streak': [p2_streak],
            'surf_Clay': [1 if f['surface'] == 'Clay' else 0], 'surf_Grass': [1 if f['surface'] == 'Grass' else 0], 'surf_Hard': [1 if f['surface'] == 'Hard' else 0]
        }
        
        df_input = pd.DataFrame(input_data)
        for col in expected_features:
            if col not in df_input.columns: df_input[col] = 0
        df_input = df_input[expected_features]
        
        prob = model.predict_proba(df_input)[0]
        p1_conf, p2_conf = prob[1], prob[0]
        
        chosen_winner, chosen_odds, confidence = (f['p1_name'], f['p1_odds'], p1_conf) if p1_conf >= p2_conf else (f['p2_name'], f['p2_odds'], p2_conf)
            
        predicted_pool.append({
            'match_desc': f"{f['p1_name']} vs {f['p2_name']} ({f['surface']})",
            'winner': chosen_winner, 'odds': chosen_odds, 'confidence': confidence
        })

    col1, col2 = st.columns(2)
    with col1:
        st.subheader("📋 Match Preds")
        for p in predicted_pool:
            with st.container(border=True):
                st.markdown(f"**{p['match_desc']}**")
                st.write(f"🟢 Pick: **{p['winner']}** | Odds: {p['odds']} | Confidence: {p['confidence']*100:.1f}%")
                st.progress(float(p['confidence']))

    with col2:
        st.subheader("💰 Generated Bet Slip")
        legs, slip_odds = strategy.generate_optimized_slip(predicted_pool, min_odds, max_odds)
        if legs:
            for idx, leg in enumerate(legs, 1):
                st.info(f"**Leg {idx}:** {leg['match_desc']}\n\nSelection: **{leg['winner']}** | Odds: {leg['odds']}")
            st.success(f"### 📈 Combined Slip Odds: {slip_odds:.2f}x")
