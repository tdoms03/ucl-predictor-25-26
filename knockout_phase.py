import numpy as np
import json
import os
import pandas as pd

# --- 1. SETUP TEAMS ---
class Team:
    def __init__(self, name, elo):
        self.name = name
        self.strength = elo # ELO score

# CREATE THE TEAMS
psg = Team('PSG', 2288)
chelsea = Team('Chelsea', 2219)
galatasaray = Team('Galatasaray', 2051)
liverpool = Team('Liverpool', 2214)
real_madrid = Team('Real Madrid', 2232)
man_city = Team('Man City', 2264)
atalanta = Team('Atalanta', 2109)
bayern = Team('Bayern', 2351)
newcastle = Team('Newcastle', 2129)
barcelona = Team('Barcelona', 2336)
atletico = Team('Atletico', 2194)
tottenham = Team('Tottenham', 2090)
bodo_glimt = Team('Bodo/Glimt', 1988)
sporting_cp = Team('Sporting CP', 2176)
leverkusen = Team('Leverkusen', 2148)
arsenal = Team('Arsenal', 2381)

# BRACKETS
remaining_teams = [psg, chelsea, galatasaray, liverpool, real_madrid, man_city, atalanta, bayern, newcastle, barcelona, atletico, tottenham, bodo_glimt, sporting_cp, leverkusen, arsenal]
left_bracket = [psg, chelsea, galatasaray, liverpool, real_madrid, man_city, atalanta, bayern]
right_bracket = [newcastle, barcelona, atletico, tottenham, bodo_glimt, sporting_cp, leverkusen, arsenal]

lookup_table = {t.name: t for t in remaining_teams}

# --- 2. MATCH SIMULATION ENGINE (POISSON) ---

def generate_score(team_elo, opp_elo, home_advantage=True):
    """
    Calculates goals based on ELO difference.
    Standard Elo formula: Expected Score = 1 / (1 + 10^((opp - team)/400))
    """
    # Elo difference plus home advantage bonus (approx 100 points)
    elo_diff = (team_elo + (100 if home_advantage else 0)) - opp_elo
    
    # Expected goals (Base average ~1.5 goals per game)
    # Every 400 points diff = 10x likelihood, scaled down for realistic scores
    mu = 1.55 * (10 ** (elo_diff / 4000)) # 4000 divisor flattens the curve for football randomness
    
    return np.random.poisson(mu)

def simulate_tie(team1, team2, neutral=False):
    """
    Simulates a 2-legged tie or single neutral final.
    Returns: (Winner_Object, Score_String)
    """
    if neutral:
        # Single match (Final)
        g1 = generate_score(team1.strength, team2.strength, False)
        g2 = generate_score(team2.strength, team1.strength, False)
        
        if g1 > g2: return team1
        if g2 > g1: return team2
        # Penalties (Coin flip)
        return team1 if np.random.random() > 0.5 else team2

    # Leg 1: Team 2 is Home (Lower seed usually hosts first)
    t2_g1 = generate_score(team2.strength, team1.strength, True)
    t1_g1 = generate_score(team1.strength, team2.strength, False)

    # Leg 2: Team 1 is Home
    t1_g2 = generate_score(team1.strength, team2.strength, True)
    t2_g2 = generate_score(team2.strength, team1.strength, False)

    # Aggregates
    t1_agg = t1_g1 + t1_g2
    t2_agg = t2_g1 + t2_g2

    if t1_agg > t2_agg: return team1
    if t2_agg > t1_agg: return team2
    return team1 if np.random.random() > 0.5 else team2

# --- 3. TOURNAMENT LOGIC ---

def run_simulation(num_sims=50000):
    global remaining_teams, lookup_table
    all_teams = remaining_teams.copy()
    team_lookup = lookup_table.copy()
    r16_draw = [('PSG', 'Chelsea'),
                ('Galatasaray', 'Liverpool'),
                ('Real Madrid', 'Man City'),
                ('Atalanta', 'Bayern'),
                ('Newcastle', 'Barcelona'),
                ('Atletico', 'Tottenham'),
                ('Bodo/Glimt', 'Sporting CP'),
                ('Leverkusen', 'Arsenal')
                ]
    # We no longer need to track "R16" since all these teams are already in it.
    stats = {t.name: {"QF": 0, "SF": 0, "Final": 0, "Winner": 0} for t in all_teams}

    for sim in range(num_sims):
        if sim % 2000 == 0: print(f"Simulating tournament {sim}/{num_sims}...")

        # --- STEP B: ROUND OF 16 ---
        r16_winners = []
        for home_team_name, away_team_name in r16_draw:
            team1 = team_lookup[home_team_name]
            team2 = team_lookup[away_team_name]
            
            winner = simulate_tie(team1, team2)
            r16_winners.append(winner)
            stats[winner.name]["QF"] += 1

        # --- STEP C: QUARTER FINALS ---
        # Bracket pairs sequentially: Match 0 vs Match 1, Match 2 vs Match 3...
        qf_winners = []
        for i in range(0, 8, 2):
            winner = simulate_tie(r16_winners[i], r16_winners[i+1])
            qf_winners.append(winner)
            stats[winner.name]["SF"] += 1

        # --- STEP D: SEMI FINALS ---
        # Bracket pairs sequentially: QF 0 vs QF 1, QF 2 vs QF 3
        sf_winners = []
        for i in range(0, 4, 2):
            winner = simulate_tie(qf_winners[i], qf_winners[i+1])
            sf_winners.append(winner)
            stats[winner.name]["Final"] += 1

        # --- STEP E: FINAL ---
        champion = simulate_tie(sf_winners[0], sf_winners[1], neutral=True)
        stats[champion.name]["Winner"] += 1

    # --- NORMALIZE STATS ---
    for t_name in stats:
        for stage in stats[t_name]:
            stats[t_name][stage] = round((stats[t_name][stage] / num_sims) * 100, 2)

    return stats

# --- 4. EXECUTION ---
if __name__ == "__main__":
    # 1. Run the main tournament simulation (your existing code)
    results = run_simulation(num_sims=50000)
    
    os.makedirs('static/data', exist_ok=True)
    with open('static/data/winner_predictions.json', 'w') as f:
        json.dump(results, f)
        
    print("✅ R16 Knockout simulation complete. Data saved.")

    # --- NEW CODE: GENERATE H2H MATRIX & EXACT SCORES ---
    print("⏳ Generating exact Head-to-Head probabilities and Exact Scores...")
    
    all_teams = list(lookup_table.values())
    h2h_matrix = {t.name: {} for t in all_teams}
    score_matrix = {t.name: {} for t in all_teams}
    
    # Loop through every unique pair of teams
    for i, t1 in enumerate(all_teams):
        for t2 in all_teams[i+1:]:
            t1_wins = 0
            h2h_sims = 10000
            scores_t1_t2 = {} 
            
            # Use your pre-defined brackets to check if they can only meet in the final
            is_neutral_final = (t1 in left_bracket and t2 in right_bracket) or \
                               (t2 in left_bracket and t1 in right_bracket)
            
            for _ in range(h2h_sims):
                if is_neutral_final:
                    # ONE-OFF FINAL: Neutral ground, 1 match
                    g1 = generate_score(t1.strength, t2.strength, home_advantage=False)
                    g2 = generate_score(t2.strength, t1.strength, home_advantage=False)
                    t1_agg, t2_agg = g1, g2
                else:
                    # 2-LEGGED TIE: Home and Away
                    t2_g1 = generate_score(t2.strength, t1.strength, home_advantage=True)
                    t1_g1 = generate_score(t1.strength, t2.strength, home_advantage=False)
                    
                    t1_g2 = generate_score(t1.strength, t2.strength, home_advantage=True)
                    t2_g2 = generate_score(t2.strength, t1.strength, home_advantage=False)
                    
                    t1_agg = t1_g1 + t1_g2
                    t2_agg = t2_g1 + t2_g2
                
                # Winner logic
                if t1_agg > t2_agg:
                    t1_wins += 1
                elif t2_agg > t1_agg:
                    pass
                else:
                    # Penalties
                    if np.random.random() > 0.5: t1_wins += 1 
                
                # Record the scoreline
                score_str = f"{t1_agg}-{t2_agg}"
                scores_t1_t2[score_str] = scores_t1_t2.get(score_str, 0) + 1
            
            # Save H2H Win Percentages
            t1_prob = round((t1_wins / h2h_sims) * 100, 1)
            t2_prob = round(100.0 - t1_prob, 1)
            h2h_matrix[t1.name][t2.name] = t1_prob
            h2h_matrix[t2.name][t1.name] = t2_prob
            
            # Process Top 3 Exact Scores
            top_scores = sorted(scores_t1_t2.items(), key=lambda x: x[1], reverse=True)[:3]
            score_matrix[t1.name][t2.name] = [{"score": k, "prob": round((v/h2h_sims)*100, 1)} for k, v in top_scores]
            score_matrix[t2.name][t1.name] = [{"score": f"{k.split('-')[1]}-{k.split('-')[0]}", "prob": round((v/h2h_sims)*100, 1)} for k, v in top_scores]

    # Save to files
    with open('static/data/h2h_matrix.json', 'w') as f:
        json.dump(h2h_matrix, f)
    with open('static/data/exact_scores.json', 'w') as f:
        json.dump(score_matrix, f)
        
    print("⏳ Exporting Team ELO ratings...")
    elo_data = {t.name: t.strength for t in all_teams}
    with open('static/data/team_elo.json', 'w') as f:
        json.dump(elo_data, f)
        
    print("✅ All data successfully saved!")