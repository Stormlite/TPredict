import requests

API_KEY = "202bfd9d562a5763686659a3380ab14e"
# 'upcoming' is universally valid and returns the next 8 active matches across all sports
SPORT = "upcoming"
REGION = "eu"

def fetch_live_fixtures():
    """Fetches real-world scheduled tennis matches and live bookmaker odds."""
    url = f"https://api.the-odds-api.com/v4/sports/{SPORT}/odds/?apiKey={API_KEY}&regions={REGION}&markets=h2h"
    try:
        response = requests.get(url)
        if response.status_code != 200:
            print(f"⚠️ API Error Status: {response.status_code}")
            return []
            
        data = response.json()
        real_fixtures = []
        
        for match in data:
            # Drop entries that do not map down to tennis match events
            if "tennis" not in match.get("sport_key", "").lower():
                continue
                
            p1_name = match.get("home_team")
            p2_name = match.get("away_team")
            p1_odds, p2_odds = 1.85, 1.85
            
            if match.get("bookmakers"):
                for b in match["bookmakers"]:
                    if b["key"] in ["sportybet", "onexbet", "bet365"]:
                        for m in b.get("markets", []):
                            if m["key"] == "h2h":
                                for out in m.get("outcomes", []):
                                    if out["name"] == p1_name: p1_odds = out["price"]
                                    if out["name"] == p2_name: p2_odds = out["price"]
                        break
            
            real_fixtures.append({
                "p1_name": p1_name, 
                "p1_rank": 50, 
                "p1_odds": p1_odds, 
                "p2_name": p2_name, 
                "p2_rank": 100, 
                "p2_odds": p2_odds, 
                "surface": "Hard"
            })
        return real_fixtures
    except Exception as e:
        print(f"⚠️ Network error encountered: {e}")
        return []
