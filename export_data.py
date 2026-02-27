import pandas as pd
import numpy as np
import json
import os
from main import Team, simulate_match

# --- 1. SETUP TEAMS (Copy from main.py or simulate.py) ---
# (Ideally, you should move this team creation to main.py to avoid duplication,
# but for now, we can redefine them here to keep it simple)

psg = Team('PSG', 1981)
real_madrid = Team('Real Madrid', 1945)
man_city = Team('Man City', 1947)
bayern = Team('Bayern', 1933)
liverpool = Team('Liverpool', 2015)
inter = Team('Inter', 1912)
chelsea = Team('Chelsea', 1915)
dortmund = Team('Dortmund', 1827)
barcelona = Team('Barcelona', 1950)
arsenal = Team('Arsenal', 2006)
leverkusen = Team('Leverkusen', 1841)
atletico = Team('Atletico', 1838)
benfica = Team('Benfica', 1800)
atalanta = Team('Atalanta', 1833)
villareal = Team('Villareal', 1782)
juventus = Team('Juventus', 1823)
frankfurt = Team('Frankfurt', 1757)
club_brugge = Team('Club Brugge', 1743)
tottenham = Team('Tottenham', 1812)
psv = Team('PSV', 1771)
ajax = Team('Ajax', 1661)
napoli = Team('Napoli', 1885)
sporting_cp = Team('Sporting CP', 1793)
olympiacos = Team('Olympiacos', 1692)
slavia_praag = Team('Slavia Praag', 1681)
bodo_glimt = Team('Bodo/Glimt', 1658)
marseille = Team('Marseille', 1749)
copenhagen = Team('Copenhagen', 1653)
monaco = Team('Monaco', 1768)
galatasaray = Team('Galatasaray', 1714)
union = Team('Union', 1754)
qarabag = Team('Qarabag', 1538)
atheletic_club = Team('Atheletic Club', 1786)
newcastle = Team('Newcastle', 1867)
pafos = Team('Pafos', 1525)
kairat_almaty = Team('Kairat Almaty', 1302)

teams = [psg,real_madrid,man_city,bayern,liverpool,inter,chelsea,dortmund,barcelona,arsenal,leverkusen,
        atletico,benfica,atalanta,villareal,juventus,frankfurt,club_brugge,tottenham,psv,ajax,napoli,
        sporting_cp,olympiacos,slavia_praag,bodo_glimt,marseille,copenhagen,monaco,galatasaray,union,
        qarabag,atheletic_club,newcastle,pafos,kairat_almaty]

# --- 2. SETUP OPPONENTS ---
psg.opponents = [bayern, atalanta, tottenham,newcastle]
real_madrid.opponents = [man_city,juventus,marseille,monaco]
man_city.opponents = [dortmund,leverkusen,napoli,galatasaray]
bayern.opponents = [chelsea,club_brugge,sporting_cp,union]
liverpool.opponents = [real_madrid,atletico, psv, qarabag]
inter.opponents = [liverpool, arsenal, slavia_praag, kairat_almaty]
chelsea.opponents = [barcelona,benfica,ajax,pafos]
dortmund.opponents = [inter,villareal,bodo_glimt,atheletic_club]
barcelona.opponents = [psg, frankfurt,olympiacos,copenhagen]
arsenal.opponents = [bayern, atletico, olympiacos,kairat_almaty]
leverkusen.opponents = [psg,villareal,psv,newcastle]
atletico.opponents = [inter,frankfurt,bodo_glimt,union]
benfica.opponents = [real_madrid,leverkusen,napoli,qarabag]
atalanta.opponents = [chelsea,club_brugge,slavia_praag,atheletic_club]
villareal.opponents = [man_city,juventus,ajax,copenhagen]
juventus.opponents = [dortmund,benfica,sporting_cp,pafos]
frankfurt.opponents = [liverpool,atalanta,tottenham,galatasaray]
club_brugge.opponents = [barcelona,arsenal,marseille,monaco]
tottenham.opponents = [dortmund,villareal,slavia_praag,copenhagen]
psv.opponents = [bayern,atletico,napoli,union]
ajax.opponents = [inter,benfica,olympiacos,galatasaray]
napoli.opponents = [chelsea,frankfurt,sporting_cp,qarabag]
sporting_cp.opponents = [psg,club_brugge,marseille,kairat_almaty]
olympiacos.opponents = [real_madrid,leverkusen,psv,pafos]
slavia_praag.opponents = [barcelona,arsenal,bodo_glimt,atheletic_club]
bodo_glimt.opponents = [man_city,juventus,tottenham,monaco]
marseille.opponents = [liverpool,atalanta,ajax,newcastle]
copenhagen.opponents = [dortmund,leverkusen,napoli,kairat_almaty]
monaco.opponents= [man_city,juventus,tottenham,galatasaray]
galatasaray.opponents = [liverpool,atletico,bodo_glimt,union]
union.opponents = [inter,atalanta,marseille,newcastle]
qarabag.opponents = [chelsea,frankfurt,ajax,copenhagen]
atheletic_club.opponents = [psg,arsenal,sporting_cp,qarabag]
newcastle.opponents = [barcelona,benfica,psv,atheletic_club]
pafos.opponents = [bayern,villareal,slavia_praag,monaco]
kairat_almaty.opponents = [real_madrid,club_brugge,olympiacos,pafos]

# --- 3. SIMULATION LOGIC ---
def play_tournament(teams):
    for team in teams:
        for opponent in team.opponents:
            simulate_match(team, opponent)

def run_simulation(teams, num_simulations=100000):
    results = {team.name: [] for team in teams}
    print(f"Starting {num_simulations} simulations for web export...")
    
    for i in range(num_simulations):
        if i % 10000 == 0: print(f"Processing... {i}/{num_simulations}")
        
        # Reset team stats
        for team in teams:
            team.reset_stats()
        
        play_tournament(teams)
        
        # Collect final points for each team
        for team in teams:
            results[team.name].append(team.points)

    return results

# --- 4. EXPORT DATA ---
if __name__ == "__main__":
    num_simulations = 100000
    results = run_simulation(teams, num_simulations)

    # A. Leaderboard Data (Average Points)
    avg_points = {team: sum(points_list) / len(points_list) for team, points_list in results.items()}
    # Create list of dicts for JSON: [{"Team": "Name", "AvgPoints": 12.5}, ...]
    leaderboard_data = [{"Team": k, "AvgPoints": v} for k, v in avg_points.items()]
    
    # B. Probabilities (Top 8, Top 24)
    prob_df = pd.DataFrame(results)
    ranks = prob_df.rank(axis=1, ascending=False, method='min')

    prob_data = {}
    for team in prob_df.columns:
        top8 = (ranks[team] <= 8).mean()
        top24 = (ranks[team] <= 24).mean()
        prob_data[team] = {
            "Top 8": top8,
            "9-24": top24 - top8,
            "25-36": 1 - top24
        }
    
    # C. Insights (Specific Questions)
    english_teams = ["Liverpool", "Chelsea", "Arsenal", "Tottenham", "Newcastle", "Man City"]
    prob_english = ((ranks[english_teams] <= 24).all(axis=1)).mean()

    spanish_teams = ["Real Madrid", "Barcelona", "Atletico", "Villareal", "Atheletic Club"]
    prob_spanish = ((ranks[spanish_teams] <= 24).all(axis=1)).mean()

    prob_belgian = ((ranks[["Club Brugge", "Union"]] <= 24).all(axis=1)).mean()
    prob_dutch = ((ranks[["Ajax", "PSV"]] <= 24).all(axis=1)).mean()

    insights_data = [
        {"title": "Premier League Dominance", "desc": "Chance all 6 English teams qualify (Top 24)", "value": f"{prob_english:.1%}", "color": "blue"},
        {"title": "La Liga Sweep", "desc": "Chance all 5 Spanish teams qualify (Top 24)", "value": f"{prob_spanish:.1%}", "color": "yellow"},
        {"title": "Belgian Duo", "desc": "Chance Brugge & Union both qualify", "value": f"{prob_belgian:.1%}", "color": "red"},
        {"title": "Dutch Rivals", "desc": "Chance Ajax & PSV both qualify", "value": f"{prob_dutch:.1%}", "color": "orange"}
    ]

    # D. Distributions (Histograms)
    distributions_data = {}
    for team_name, points_list in results.items():
        counts = pd.Series(points_list).value_counts().sort_index()
        probs = (counts / num_simulations).to_dict()
        distributions_data[team_name] = probs

    # --- SAVE FILES ---
    # Create directory if it doesn't exist
    os.makedirs('static/data', exist_ok=True)

    with open('static/data/leaderboard.json', 'w') as f:
        json.dump(leaderboard_data, f)
    
    with open('static/data/qualification_probs.json', 'w') as f:
        json.dump(prob_data, f)

    with open('static/data/insights.json', 'w') as f:
        json.dump(insights_data, f)

    with open('static/data/team_distributions.json', 'w') as f:
        json.dump(distributions_data, f)

    print("✅ Export complete! Data saved to 'static/data/'.")