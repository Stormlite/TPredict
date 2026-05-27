# 🎾 TPredict: Advanced Tennis ML Predictor & Automated Betting Bot

An end-to-end Machine Learning pipeline and automated cloud engine that scans real-world professional ATP tennis tournament fixtures, evaluates match probabilities using historical chronological player profiles, and algorithmically isolates optimized 2x–5x accumulator bet slips delivered directly to your phone.

---

## ⚡ Key System Features

* **🧠 Advanced ML Engine:** Random Forest Classifier trained on years of historical ATP performance data.
* **📈 Rolling Feature Engineering:** Tracks deep chronological trends including historical Head-to-Head (H2H) records and 5-match rolling form streaks before predicting any fixture.
* **📡 Real-Time Sports Feed:** Integrates directly with live global betting markets via **The Odds API** to scrape authentic SportyBet, 1XBet, and Bet365 match prices.
* **💰 Automated Slip Combinator:** Sorts highest-confidence predictions and calculates composite multi-leg accumulator slips locked inside a precise **2x–5x odds sweet spot**.
* **📱 WhatsApp Alert Integration:** Leverages the **Twilio API Gateway** to broadcast the daily generated betting tickets straight to your phone.
* **☁️ Cloud Autopilot (GitHub Actions):** Runs completely hands-free on virtual Linux servers every single morning at exactly **12:10 AM Ghana Time (00:10 UTC)**—no local hardware required.
* **📊 Visual Web Dashboard:** Includes an elegant, lightweight interactive front-end web portal powered by **Streamlit Cloud**.

---

## 📂 System Architecture Folder Structure

```text
tennis_predictor/
│
├── .github/workflows/
│   └── daily_bot.yml           # GitHub Actions cron scheduler pipeline (12:10 AM GMT)
│
├── data/
│   └── raw/                    # Local historical multi-year ATP datasets (2022–2025)
│
├── models/
│   └── rf_model.pkl            # Trained binary Random Forest classification model
│
├── src/
│   ├── ingest.py               # Optimized offline-first local dataset manager
│   ├── features.py             # Feature extractor (Rolling win-streaks & H2H trends)
│   ├── preprocess.py           # Balanced matchup data-flipper and cleaner
│   ├── train.py                # Model training, diagnostic reporting, and serialization
│   ├── scraper.py              # Live bookmaker API scripter with Grand Slam fallbacks
│   ├── strategy.py             # Algorithmic bet slip consolidation and risk manager
│   ├── notifier.py             # Twilio WhatsApp payload delivery module
│   └── app.py                  # Live Streamlit front-end visualization web app
│
├── .gitignore                  # Prevents accidental security/dependency repository leaks
├── requirements.txt            # System environment package dependencies
└── README.md                   # System documentation handbook
```

---

## 🚀 Local Installation & Configuration Setup

Follow these simple instructions to initialize and launch this predictive pipeline on your local machine:

### 1. Initialize Project & Active Environment
Clone your repository, navigate to your root folder, and initialize a secure virtual Python environment:
```powershell
cd D:\CCTP\tennis_predictor
python -m venv .venv
```
Activate the environment:
```powershell
# On Windows (PowerShell)
.venv\Scripts\activate

# On Mac / Linux
source .venv/bin/activate
```

### 2. Download Core System Requirements
Install all required network packages, machine learning engines, and front-end tools directly into your environment:
```powershell
python -m pip install -r requirements.txt
```

### 3. Initialize Training Pipeline
Run the training module to read your local datasets, extract rolling features, run performance diagnostics, and save your trained model brain binary:
```powershell
python src/train.py
```

### 4. Fire Up the Visual Browser Web App
Launch your front-end Streamlit dashboard layer onto your local network:
```powershell
streamlit run src/app.py
```
Your default browser will pop open automatically at `http://localhost:8501`, allowing you to adjust parameters and trigger predictions visually!

---

## 🔒 Cloud Automation Secrets Setup

To run your betting bot completely on autopilot in the cloud without leaking secure account credentials, add these keys under your online repository dashboard panel:

1. Head to your repository page at `https://github.com`.
2. Click **Settings ⚙️** -> **Secrets and variables** -> **Actions**.
3. Add the following two **Repository Secrets**:
   * **`TWILIO_ACCOUNT_SID`** : Your Twilio dashboard account identifier string.
   * **`TWILIO_AUTH_TOKEN`** : Your secret Twilio authentication protocol token key.
4. Go to **Actions** -> **Daily Tennis Predictor Bot** -> **Run workflow** to trigger an instant cloud test!

---

## 📈 Model Performance Verification Metrics

The pipeline incorporates a random data-flipping preprocessor to eliminate bookmaker favoritism and player selection bias, achieving a statistically realistic precision matrix for ranking-based tennis models:

```text
🚀 Enhanced Model Accuracy: 0.6459

              precision    recall  f1-score   support

           0       0.69      0.64      0.66       314
           1       0.60      0.66      0.63       265

    accuracy                           0.65       579
   macro avg       0.65      0.65      0.65       579
weighted avg       0.65      0.65      0.65       579
```

---

## 📝 Project License & Disclaimer

This project is open-source and intended entirely for **educational, data-science research, and recreational software programming simulation purposes**. Past performance does not guarantee future results. Always practice responsible management with any live sports bookmaker system.
