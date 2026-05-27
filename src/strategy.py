def generate_optimized_slip(predicted_matches, min_odds=2.0, max_odds=5.0):
    """Assembles a composite accumulator bet slip targeting a 2x-5x valuation."""
    # Sort from highest confidence to lowest confidence
    sorted_matches = sorted(predicted_matches, key=lambda x: x['confidence'], reverse=True)
    
    slip_legs = []
    total_odds = 1.0
    
    for match in sorted_matches:
        if total_odds >= max_odds:
            break
            
        # Prevent appending ultra-high-risk selections
        if match['odds'] > 3.5:
            continue
            
        slip_legs.append(match)
        total_odds *= match['odds']
        
        if min_odds <= total_odds <= max_odds:
            return slip_legs, total_odds
            
    return slip_legs, total_odds
