import random

def fetch_live_fixtures():
    """Generates mock professional tournament pairings for validation without API keys."""
    players = [
        ("Novak Djokovic", 1), ("Carlos Alcaraz", 2), ("Jan-Lennard Struff", 25),
        ("Daniil Medvedev", 4), ("Alexander Zverev", 5), ("Adrian Mannarino", 30),
        ("Andrey Rublev", 6), ("Holger Rune", 7), ("Christopher Eubanks", 42)
    ]
    surfaces = ['Clay', 'Hard', 'Grass']
    fixtures = []
    
    # Shuffle matches
    random.seed(101)
    random.shuffle(players)
    
    for i in range(0, len(players) - 1, 2):
        p1, p1_rank = players[i]
        p2, p2_rank = players[i+1]
        
        # Calculate algorithmic bookie odds based roughly on rank differential
        base_odds_p1 = 1.85 + ((p1_rank - p2_rank) / 50.0)
        p1_odds = round(max(1.15, min(4.50, base_odds_p1)), 2)
        p2_odds = round(max(1.15, min(4.50, 3.7 - p1_odds)), 2)
        
        fixtures.append({
            'p1_name': p1, 'p1_rank': p1_rank, 'p1_odds': p1_odds,
            'p2_name': p2, 'p2_rank': p2_rank, 'p2_odds': p2_odds,
            'surface': random.choice(surfaces)
        })
    return fixtures
