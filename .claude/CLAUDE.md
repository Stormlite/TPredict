# Tennis Predictor - Coding Rules

## Stack
- Python 3.10+, pandas, scikit-learn, joblib, argparse
- NO neural networks. NO pytorch. NO tensorflow.
- Use only stdlib + the above packages.

## Style Rules
- Write functions, NOT classes, unless asked.
- Keep each function under 30 lines.
- Add a docstring to every function.
- Use type hints on all function signatures.
- Never write more than 60 lines per response.

## File Structure
- src/ingest.py      - data loading
- src/preprocess.py  - cleaning + features
- src/train.py       - model training
- src/predict.py     - CLI prediction
- data/raw/          - raw CSVs
- data/processed/    - cleaned CSVs
- models/            - saved .pkl files
