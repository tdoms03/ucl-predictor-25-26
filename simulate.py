import pandas as pd 
import numpy as np
from main import Team, simulate_match
import matplotlib.pyplot as plt
from scipy.stats import spearmanr
import os

# Create the teams
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

# Home Opponents for each team
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

def play_tournament(teams):
    for team in teams:
        # Simulate the home matches of the team
        for opponent in team.opponents:
            simulate_match(team, opponent)

# Print the leaderboard
def print_leaderboard(teams):
    # Sort teams by points, then by goal difference, then by goals for
    sorted_teams = sorted(teams, key=lambda x: (x.points, x.goal_difference(), x.goals_for), reverse=True)
    print(f"{'Team':<20} {'Points':<6} {'GF':<4} {'GA':<4} {'GD':<4}")
    for team in sorted_teams:
        print(f"{team.name:<20} {team.points:<6} {team.goals_for:<4} {team.goals_against:<4} {team.goal_difference():<4}")


def monte_carlo_simulation(teams, num_simulations=100000):
    results = {team.name: [] for team in teams}
    cutoff8_list = []
    cutoff24_list = []
    for i in range(num_simulations):
        # Reset team stats
        for team in teams:
            team.reset_stats()
        play_tournament(teams)
        # Collect final points for each team
        for team in teams:
            results[team.name].append(team.points)
        # Statistics
        standings = sorted(teams, key=lambda x: (x.points, x.goal_difference(), x.goals_for), reverse=True)
        all_points = [team.points for team in standings]

        # store cutoffs
        cutoff8_list.append(all_points[7])   # 8th place = index 7
        cutoff24_list.append(all_points[23]) # 24th place = index 23

    return results, cutoff8_list, cutoff24_list

def simulate_matchups(team1,team2,num_matches=1000):
    team1_wins = 0
    team2_wins = 0
    draws = 0
    for _ in range(num_matches):
        result = simulate_match(team1,team2)
        if result == 0:
            team1_wins += 1
        elif result == 1:
            team2_wins += 1
        else:
            draws += 1
    return team1_wins, team2_wins, draws

if __name__ == "__main__":
    num_simulations = 100000
    results, cutoff8_list, cutoff24_list = monte_carlo_simulation(teams, num_simulations=num_simulations)
    
    # --- Average points calculation ---
    avg_points = {team: sum(points_list) / len(points_list) for team, points_list in results.items()}
    sorted_teams = sorted(avg_points.items(), key=lambda x: x[1], reverse=True)
    team_names = [team for team, _ in sorted_teams]
    points = [pts for _, pts in sorted_teams]

    # --- Qualification probabilities ---
    prob_df = pd.DataFrame(results)  # rows = simulations, cols = teams
    ranks = prob_df.rank(axis=1, ascending=False, method='min')

    prob_table = {}
    for team in prob_df.columns:
        top8 = (ranks[team] <= 8).mean()
        top24 = (ranks[team] <= 24).mean()
        prob_table[team] = {
            "Top 8": top8,
            "9-24": top24 - top8,
            "25-36": 1 - top24
        }

    prob_table = pd.DataFrame(prob_table).T.loc[team_names]

    # Create a DataFrame from the average points and save it
    df_results = pd.DataFrame(list(avg_points.items()), columns=['Team', 'AvgPoints'])
    df_results.to_csv('simulated_results.csv', index=False)
    print("Results saved to simulated_results.csv")

    predicted_leaderboard = False
    if predicted_leaderboard:
        # --- Plot 1: Average points leaderboard ---
        plt.style.use('seaborn-v0_8-darkgrid')
        fig, ax = plt.subplots(figsize=(12, 8), dpi=120)
        bar_colors = [
            '#2E8B57' if i < 8 else '#FFA500' if i < 24 else '#B0B0B0'
            for i in range(len(points))
        ]
        bars = ax.barh(team_names, points, color=bar_colors, edgecolor='black', height=0.65)
        for i, bar in enumerate(bars):
            ax.text(bar.get_width() + 0.3, bar.get_y() + bar.get_height() / 2,
                    f'{points[i]:.2f}', va='center', fontsize=10, fontweight='bold', color='#333')
        ax.invert_yaxis()
        ax.tick_params(axis='y', labelsize=11)
        ax.tick_params(axis='x', labelsize=11)
        for spine in ax.spines.values():
            spine.set_visible(False)
        legend_handles = [
            plt.Line2D([0], [0], color='#2E8B57', lw=4, label='Top 8: Qualified'),
            plt.Line2D([0], [0], color='#FFA500', lw=4, label='9-24: Knock-out'),
            plt.Line2D([0], [0], color='#B0B0B0', lw=4, label='25-36: Eliminated')
        ]
        ax.legend(handles=legend_handles, loc='lower right', fontsize=11, frameon=True, edgecolor='gray')
        plt.tight_layout(pad=2)
        plt.savefig('predicted_leaderboard.png', dpi=300)
        plt.show()

    prob_prediction = False
    if prob_prediction:
        # --- Plot 2: Qualification probabilities ---
        fig, ax = plt.subplots(figsize=(12, 6), dpi=120)
        bars = prob_table.plot(kind="barh", stacked=True,
                            color=["#2E8B57", "#FFA500", "#B0B0B0"],
                            ax=ax, edgecolor="black", width=0.8)
        ax.set_xlabel("Probability", fontsize=13, fontweight="bold", labelpad=12)
        # ax.set_title("Champions League Qualification Probabilities", fontsize=16, fontweight="bold", pad=18)
        ax.invert_yaxis()
        ax.legend(title="Outcome", fontsize=11, frameon=True, edgecolor="gray")
        ax.tick_params(axis='y', labelsize=11)
        ax.tick_params(axis='x', labelsize=11)
        for spine in ax.spines.values():
            spine.set_visible(False)
        # Add percentage labels inside each bar, always in white
        for i, (idx, row) in enumerate(prob_table.iterrows()):
            left = 0
            for j, (col, value) in enumerate(row.items()):
                bar_width = value
                if bar_width > 0.04:
                    ax.text(left + bar_width/2, i, f"{value*100:.1f}%", va='center', ha='center',
                            color='white', fontsize=10, fontweight='bold')
                left += bar_width
        plt.tight_layout(pad=2)
        plt.savefig('qualification_probabilities.png', dpi=300)
        plt.show()

    violin = False
    if violin:
        # --- Plot 3: Point distributions (violin plot) ---
        fig, ax = plt.subplots(figsize=(12, 14), dpi=120)
        # Reorder results in the same team order as avg points
        ordered_results = [results[team] for team in team_names]
        ax.violinplot(ordered_results, vert=False, showmeans=True, showextrema=False)
        ax.set_yticks(range(1, len(team_names)+1))
        ax.set_yticklabels(team_names, fontsize=11)
        ax.set_xlabel("Points", fontsize=13, fontweight="bold", labelpad=12)
        ax.set_title("Distribution of Points (Monte Carlo Simulation)", fontsize=16, fontweight="bold", pad=18)
        ax.grid(True, linestyle="--", alpha=0.6)
        plt.tight_layout(pad=2)
        plt.show()

    cutoff = False
    
    # --- Cutoff statistics ---
    # cutoff8_list and cutoff24_list are Python lists of integers
    cutoff8 = np.array(cutoff8_list, dtype=int)
    cutoff24 = np.array(cutoff24_list, dtype=int)

    # Compute min/max safely
    min_points = int(min(min(cutoff8_list), min(cutoff24_list)))
    max_points = int(max(max(cutoff8_list), max(cutoff24_list)))

    plt.figure(figsize=(12, 6))

    # Histogram (distribution view) with visibly separated bins
    bins8 = np.arange(min(cutoff8_list) - 0.5, max(cutoff8_list) + 1.5, 1)
    bins24 = np.arange(min(cutoff24_list) - 0.5, max(cutoff24_list) + 1.5, 1)
    hist8, bins8_edges, _ = plt.hist(
        cutoff8, bins=bins8, alpha=0.5, label="TOP 8 cutoff (distribution)", density=True,
        edgecolor='black', linewidth=1.5, rwidth=0.8
    )
    hist24, bins24_edges, _ = plt.hist(
        cutoff24, bins=bins24, alpha=0.5, label="TOP 24 cutoff (distribution)", density=True,
        edgecolor='black', linewidth=1.5, rwidth=0.8
    )
    if cutoff:
        plt.xlabel("Points")
        plt.ylabel("Probability / Density")
        plt.title("Probability Distribution of Cutoff Points")
        plt.legend()
        plt.grid(alpha=0.3)
        plt.savefig('cutoff_probabilities.png', dpi=300)
        plt.show()
    spec_questions = True
    if spec_questions:
        ### Specific Questions ---
        # 1. What is the chance for each of the 5 biggest leagues that all their teams qualify (top 24)?
        english_teams = ["Liverpool", "Chelsea", "Arsenal", "Tottenham", "Newcastle", "Man City"]
        # For each simulation, check if all English teams are in top 24
        english_qualify = (
            (ranks[english_teams] <= 24).all(axis=1)
        )
        prob_all_english_qualify = english_qualify.mean()
        print(f"Chance all English teams qualify (top 24): {prob_all_english_qualify:.4%}")

        spanish_teams = ["Real Madrid", "Barcelona", "Atletico", "Villareal", "Atheletic Club"]
        spanish_qualify = (
            (ranks[spanish_teams] <= 24).all(axis=1)
        )
        prob_all_spanish_qualify = spanish_qualify.mean()
        print(f"Chance all Spanish teams qualify (top 24): {prob_all_spanish_qualify:.4%}")

        german_teams = ["Bayern", "Dortmund", "Leverkusen", "Frankfurt"]
        german_qualify = (
            (ranks[german_teams] <= 24).all(axis=1)
        )   
        prob_all_german_qualify = german_qualify.mean()
        print(f"Chance all German teams qualify (top 24): {prob_all_german_qualify:.4%}")

        italian_teams = ["Inter", "Juventus", "Atalanta", "Napoli"]
        italian_qualify = (
            (ranks[italian_teams] <= 24).all(axis=1)
        )
        prob_all_italian_qualify = italian_qualify.mean()
        print(f"Chance all Italian teams qualify (top 24): {prob_all_italian_qualify:.4%}")

        french_teams = ["PSG", "Marseille", "Monaco"]
        french_qualify = (
            (ranks[french_teams] <= 24).all(axis=1)
        )
        prob_all_french_qualify = french_qualify.mean()
        print(f"Chance all French teams qualify (top 24): {prob_all_french_qualify:.4%}")
        print('--------------------------------------------------------------------------')
        # 2. Which teams have the lowest chance of surviving the league phase and what is that chance?
        # Find the 3 teams with the lowest qualification probability (top 24)
        qualification_probs = prob_table["Top 8"] + prob_table["9-24"]
        lowest_teams = qualification_probs.nsmallest(3)
        for team, prob in lowest_teams.items():
            print(f"Lowest qualification chance: {team} with {prob:.2%}")

        # 3. What is the chance that both Club Brugge and Union Saint-Gilloise qualify?
        club_belgique_qualify = (
            (ranks["Club Brugge"] <= 24) & (ranks["Union"] <= 24)
        )
        prob_club_belgique_qualify = club_belgique_qualify.mean()
        print('--------------------------------------------------------------------------')
        print(f"Chance both Club Brugge and Union Saint-Gilloise qualify (top 24): {prob_club_belgique_qualify:.4%}")

        # 4. What is the chance that both Ajax and PSV qualify?
        ajax_psv_qualify = (
            (ranks["Ajax"] <= 24) & (ranks["PSV"] <= 24)
        )
        prob_ajax_psv_qualify = ajax_psv_qualify.mean()
        print('--------------------------------------------------------------------------')
        print(f"Chance both Ajax and PSV qualify (top 24): {prob_ajax_psv_qualify:.4%}")
        print('--------------------------------------------------------------------------')
        # 5. What is the chance that you can qualify with 8 points, 9 points, 10 points and 11 points?
        for points in range(8, 12):
            prob_qualify_with_x_points = (cutoff24 < points).mean()
            print(f"Chance to qualify with {points} points (top 24): {prob_qualify_with_x_points:.4%}")

        

    # Ensure the directory exists
    os.makedirs('static/data', exist_ok=True)

    # 1. Save the Probability Table (Top 8, 9-24, Eliminated)
    # We use orient='index' to keep the team names as keys
    prob_table.to_json('static/data/qualification_probs.json', orient='index')

    # 2. Save the Leaderboard (Avg Points)
    # We use orient='records' to make it a list of objects: [{"Team": "City", "AvgPoints": 20}, ...]
    df_results.to_json('static/data/leaderboard.json', orient='records')
    
    # 3. Save the "Specific Questions" answers (Optional)
    # You can bundle the specific answers into a dictionary and save that too
    special_stats = {
        "english_chance": prob_all_english_qualify,
        "spanish_chance": prob_all_spanish_qualify,
        "club_brugge_union": prob_club_belgique_qualify,
        "ajax_psv": prob_ajax_psv_qualify
    }
    pd.Series(special_stats).to_json('static/data/special_stats.json')

    print("✅ Data successfully saved to static/data/ folder.")

    # ... (Calculations from your script) ...

    # 1. Prepare "Team Details" (Distribution of points)
    # We calculate how often a team hits specific point totals (0 to 24)
    team_distributions = {}
    for team_name, points_list in results.items():
        # Count frequency of each point total
        counts = pd.Series(points_list).value_counts().sort_index()
        # Normalize to percentage
        probs = (counts / num_simulations).to_dict()
        team_distributions[team_name] = probs

    # 2. Prepare "Scenario Insights" (Your specific questions)
    insights = [
        {
            "title": "Premier League Dominance",
            "desc": "Chance all 6 English teams reach Top 24",
            "value": f"{prob_all_english_qualify:.1%}",
            "color": "blue"
        },
        {
            "title": "La Liga Sweep",
            "desc": "Chance all Spanish teams reach Top 24",
            "value": f"{prob_all_spanish_qualify:.1%}",
            "color": "yellow"
        },
        {
            "title": "The Belgian Duo",
            "desc": "Chance Brugge & Union both qualify",
            "value": f"{prob_club_belgique_qualify:.1%}",
            "color": "red"
        },
        {
            "title": "Dutch Rivals",
            "desc": "Chance Ajax & PSV both qualify",
            "value": f"{prob_ajax_psv_qualify:.1%}",
            "color": "orange"
        }
    ]

    # 3. Save everything to JSON
    import json
    with open('static/data/team_distributions.json', 'w') as f:
        json.dump(team_distributions, f)

    with open('static/data/insights.json', 'w') as f:
        json.dump(insights, f)

    # (Keep your existing leaderboard/probability saves here too)
    print("✅ Extended data saved.")