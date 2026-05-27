import sys
import os
import pandas as pd
import joblib
import streamlit as st

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import src.scraper as scraper
import src.strategy as strategy
import src.predict as predict

# Securely bind the active data feed attributes from the local environment or the Cloud panel vault
if "API_KEY" in st.secrets:
    scraper.API_KEY = st.secrets["API_KEY"]
if "TWILIO_ACCOUNT_SID" in st.secrets:
    import src.notifier as notifier
    notifier.TWILIO_ACCOUNT_SID = st.secrets["TWILIO_ACCOUNT_SID"]
    notifier.TWILIO_AUTH_TOKEN = st.secrets["TWILIO_AUTH_TOKEN"]

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
    if not fixtures:
        st.warning("No active matches found matching the current selections.")
        st.stop()
        
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
        st.subheader("📋 Match Predictions")
        for p in predicted_pool:
            with st.container(border=True):
                st.markdown(f"**{p['match_desc']}**")
                st.write(f"🟢 Pick: **{p['winner']}** | Odds: {p['odds']} | Confidence: {p['confidence']*100:.1f}%")
                st.progress(float(p['confidence']))

    with col2:
        st.subheader("💰 Generated Bet Slip")
        legs, slip_odds = strategy.generate_optimized_slip(predicted_pool, min_odds, max_odds)
        if legs:
            report_lines = ["=============================================", "💰 AUTOMATED DAILY TICKET (SPORTYBET BASIS) 💰", "============================================="]
            for idx, leg in enumerate(legs, 1):
                st.info(f"**Leg {idx}:** {leg['match_desc']}\n\nSelection: **{leg['winner']}** | Odds: {leg['odds']}")
                report_lines.append(f"Leg {idx}: {leg['match_desc']}\n       👉 Pick: {leg['winner']} | Odds: {leg['odds']}")
            
            st.success(f"### 📈 Combined Slip Odds: {slip_odds:.2f}x")
            report_lines.append("---------------------------------------------")
            report_lines.append(f"📈 Total Ticket Accumulator Odds: {slip_odds:.2f}x\n=============================================")
            
            # Forward the finalized accumulator output onto your phone if keys exist
            if "TWILIO_ACCOUNT_SID" in st.secrets:
                import src.notifier as notifier
                notifier.send_whatsapp_ticket("\n".join(report_lines))
        else:
            st.warning("No combinations found matching your slider range filters. Try widening your odds parameters.")
