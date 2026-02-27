import numpy as np

def expected_goals(elo_a, elo_b, avg_goal_per_team=1.35, home_adv_elo=60):
    power_a = 10 ** ((elo_a + home_adv_elo) / 400)
    power_b = 10 ** (elo_b / 400)
    share_a = power_a / (power_a + power_b)
    share_b = power_b / (power_a + power_b)
    lam_a = avg_goal_per_team * share_a
    lam_b = avg_goal_per_team * share_b
    return lam_a, lam_b

def simulate_match(home_team, away_team):
    lam_home, lam_away = expected_goals(home_team.elo, away_team.elo)
    gh = np.random.poisson(lam_home)
    ga = np.random.poisson(lam_away)
    # Update the points
    # Update the goals
    home_team.goals_for += gh
    home_team.goals_against += ga
    away_team.goals_for += ga
    away_team.goals_against += gh
    if gh > ga:
        home_team.points += 3
        return 0
    elif gh == ga:
        home_team.points += 1
        away_team.points += 1
        return 1
    else:
        away_team.points += 3
        return 2

class Team:
    def __init__(self, name, elo):
        self.name = name
        self.elo = elo
        self.points = 0
        self.goals_for = 0
        self.goals_against = 0
        self.opponents = []

    def goal_difference(self):
        return self.goals_for - self.goals_against

    @property
    def opponents_list(self):
        return self.opponents

    @opponents_list.setter
    def opponents_list(self, opponents):
        self.opponents = opponents
    @property
    def get_name(self):
        return self.name

    def __str__(self):
        return f"{self.name} (ELO: {self.elo}, Points: {self.points}, GF: {self.goals_for}, GA: {self.goals_against})"
    
    def reset_stats(self):
        self.points = 0
        self.goals_for = 0
        self.goals_against = 0
        