import pandas as pd
import matplotlib.pyplot as plt
from scipy.stats import spearmanr

def get_actual_standings():
    # Actual UEFA Champions League 2025/26 Standings
    return {
        "Arsenal": 1, "Bayern": 2, "Liverpool": 3, "Tottenham": 4, "Barcelona": 5, 
        "Chelsea": 6, "Sporting CP": 7, "Man City": 8, "Real Madrid": 9, "Inter": 10,
        "PSG": 11, "Newcastle": 12, "Juventus": 13, "Atletico": 14, "Atalanta": 15, 
        "Leverkusen": 16, "Dortmund": 17, "Olympiacos": 18, "Club Brugge": 19, 
        "Galatasaray": 20, "Monaco": 21, "Qarabag": 22, "Bodo/Glimt": 23, "Benfica": 24,
        "Marseille": 25, "Pafos": 26, "Union": 27, "PSV": 28, "Atheletic Club": 29, 
        "Napoli": 30, "Copenhagen": 31, "Ajax": 32, "Frankfurt": 33, 
        "Slavia Praag": 34, "Villareal": 35, "Kairat Almaty": 36
    }

def get_df_compare():
    # 1. Load the simulated data
    try:
        df_sim = pd.read_csv('simulated_results.csv')
    except FileNotFoundError:
        print("Error: 'simulated_results.csv' not found. Please run your simulation script first.")
        return

    # 2. Process Predicted Ranks
    # Sort by AvgPoints descending to determine the predicted rank (1st, 2nd, etc.)
    df_sim = df_sim.sort_values(by='AvgPoints', ascending=False).reset_index(drop=True)
    df_sim['Predicted Rank'] = df_sim.index + 1

    # 3. Process Actual Ranks
    actual_data = get_actual_standings()
    df_actual = pd.DataFrame(list(actual_data.items()), columns=['Team', 'Actual Rank'])

    # 4. Merge DataFrames
    # This combines them into one table where we can compare rows
    df_compare = pd.merge(df_actual, df_sim, on='Team', how='left')
    
    # Fill NaN for teams that might have mismatched names (safety check)
    df_compare['Predicted Rank'] = df_compare['Predicted Rank'].fillna(37)
    df_compare['Error'] = abs(df_compare['Actual Rank'] - df_compare['Predicted Rank'])
    df_compare = df_compare.sort_values('Actual Rank')
    return df_compare
def main():
    df_compare = get_df_compare()

    # --- STATISTICS ---

    # Spearman Correlation: How well did you get the *order* right?
    rho, p_val = spearmanr(df_compare['Actual Rank'], df_compare['Predicted Rank'])

    # Mean Absolute Error: Average distance between prediction and reality
    mae = df_compare['Error'].mean()

    # Top 8 Accuracy
    actual_top8 = set(df_compare[df_compare['Actual Rank'] <= 8]['Team'])
    pred_top8 = set(df_compare[df_compare['Predicted Rank'] <= 8]['Team'])
    acc_top8 = len(actual_top8.intersection(pred_top8)) / 8 * 100

    # Top 24 Accuracy (The most critical metric for qualification)
    actual_top24 = set(df_compare[df_compare['Actual Rank'] <= 24]['Team'])
    pred_top24 = set(df_compare[df_compare['Predicted Rank'] <= 24]['Team'])
    acc_top24 = len(actual_top24.intersection(pred_top24)) / 24 * 100

    # --- OUTPUT REPORT ---
    print("="*40)
    print("      MODEL PERFORMANCE REPORT      ")
    print("="*40)
    print(f"Rank Correlation (Spearman): {rho:.4f}")
    print(f"Mean Absolute Error (MAE):   {mae:.2f} positions")
    print("-" * 40)
    print(f"Top 8 Accuracy:  {acc_top8:.1f}% ({len(actual_top8.intersection(pred_top8))}/8 teams)")
    print(f"Top 24 Accuracy: {acc_top24:.1f}% ({len(actual_top24.intersection(pred_top24))}/24 teams)")
    print("="*40)
    print("\nDetailed Comparison (Top 15 Actual):")
    print(df_compare[['Team', 'Actual Rank', 'Predicted Rank', 'Error']].head(15).to_string(index=False))

    # --- PLOTTING ---
    plt.style.use('seaborn-v0_8-darkgrid')
    plt.figure(figsize=(10, 8))
    
    # Scatter plot
    plt.scatter(df_compare['Actual Rank'], df_compare['Predicted Rank'], 
                alpha=0.8, c=df_compare['Error'], cmap='coolwarm', edgecolors='black', s=100)
    
    # Reference line (Perfect prediction)
    plt.plot([0, 37], [0, 37], 'k--', alpha=0.5, label='Perfect Prediction')
    
    # Labels
    plt.title(f'Actual vs Predicted Standings\n(Correlation: {rho:.2f}, MAE: {mae:.1f})', fontsize=14)
    plt.xlabel('Actual Rank (UEFA Official)', fontsize=12)
    plt.ylabel('Predicted Rank', fontsize=12)
    plt.gca().invert_yaxis() # Put Rank 1 at the top
    plt.gca().invert_xaxis()
    plt.legend()
    
    # Annotate the biggest outliers (teams with Error > 8 positions)
    for i, row in df_compare.iterrows():
        if row['Error'] > 8:
            plt.annotate(row['Team'], (row['Actual Rank'], row['Predicted Rank']), 
                         fontsize=9, xytext=(5, 5), textcoords='offset points')

    plt.tight_layout()
    plt.savefig('model_comparison.png', dpi=300)
    print("\nComparison chart saved to 'model_comparison.png'")
    plt.show()
def analyze_lowlands():
    df_compare = get_df_compare()
    # Define the specific teams of interest
    # specific_teams = ['Club Brugge', 'Union', 'PSV', 'Ajax', 'Feyenoord'] 
    # (Note: Feyenoord wasn't in your original simulation list, so we stick to the 4 you had)
    bene_teams = ['Club Brugge', 'Union', 'PSV', 'Ajax']
    
    # Filter the main dataframe
    df_bene = df_compare[df_compare['Team'].isin(bene_teams)].copy()
    
    # Sort by Actual Rank to make the chart readable
    df_bene = df_bene.sort_values('Actual Rank')

    # --- TEXT REPORT ---
    print("\n" + "="*40)
    print("      LOWLANDS (BE/NL) ANALYSIS      ")
    print("="*40)
    print(df_bene[['Team', 'Actual Rank', 'Predicted Rank', 'Error']].to_string(index=False))
    
    # Calculate Average Error for this region
    avg_error = df_bene['Error'].mean()
    print("-" * 40)
    print(f"Average Regional Error: {avg_error:.2f} positions")

    # --- VISUALIZATION: Grouped Bar Chart ---
    plt.figure(figsize=(10, 6))
    
    # Set up bar positions
    x = range(len(df_bene))
    width = 0.35
    
    # Create bars
    # Actual Ranks (Orange)
    plt.bar([i - width/2 for i in x], df_bene['Actual Rank'], width, 
            label='Actual Rank', color='#FF8C00', alpha=0.9, edgecolor='black')
    
    # Predicted Ranks (Blue)
    plt.bar([i + width/2 for i in x], df_bene['Predicted Rank'], width, 
            label='Predicted Rank', color='#1f77b4', alpha=0.9, edgecolor='black')
    
    # Formatting
    plt.xlabel('Team', fontsize=12, fontweight='bold')
    plt.ylabel('Rank (Lower is Better)', fontsize=12)
    plt.title('BeNe League Analysis: Reality vs Expectation', fontsize=14, fontweight='bold')
    plt.xticks(x, df_bene['Team'], fontsize=11)
    
    # Invert Y-axis because Rank 1 is "Higher" visually
    plt.ylim(37, 0) 
    
    # Add a cutoff line for Top 24 (Qualification)
    plt.axhline(y=24.5, color='r', linestyle='--', alpha=0.5, linewidth=2)
    plt.text(len(df_bene)-0.5, 23, 'Qualification Cutoff (24th)', color='r', ha='right', fontsize=9)
    
    plt.legend()
    plt.grid(axis='y', linestyle='--', alpha=0.3)
    
    plt.tight_layout()
    plt.savefig('lowlands_analysis.png', dpi=300)
    print("Lowlands analysis chart saved to 'lowlands_analysis.png'")
    plt.show()
    
def plot_surprises():
    df_compare = get_df_compare()
    # Calculate the "Surprise" factor
    # Positive diff = Predicted 20th, Actual 10th = +10 (Overperformed)
    # Negative diff = Predicted 5th, Actual 15th = -10 (Underperformed)
    df_compare['Diff'] = df_compare['Predicted Rank'] - df_compare['Actual Rank']
    
    # Sort by the magnitude of the surprise so the biggest bars are at the top
    df_sorted = df_compare.sort_values('Diff', ascending=True)

    # Create the plot
    plt.figure(figsize=(12, 10))
    
    # Color logic: Green for positive (Overperformed), Red for negative (Underperformed)
    colors = ['#d62728' if x < 0 else '#2ca02c' for x in df_sorted['Diff']]
    
    plt.barh(df_sorted['Team'], df_sorted['Diff'], color=colors, alpha=0.8)
    
    plt.title('Overperformers vs Underperformers', fontsize=16)
    plt.xlabel('Rank Difference (Predicted - Actual)', fontsize=12)
    
    # Add annotation text
    # plt.text(1, len(df_sorted)-2, "Better than expected\n(Overperformed)", color='black', fontweight='bold')
    # plt.text(-1, 2, "Worse than expected\n(Underperformed)", color='black', fontweight='bold', ha='right')
    
    plt.grid(axis='x', linestyle='--', alpha=0.5)
    plt.tight_layout()
    plt.savefig('model_surprises.png', dpi=300)
    print("Surprises chart saved to 'model_surprises.png'")
    plt.show()

def plot_qualification_matrix(df_compare):
    df_compare = get_df_compare()
    # Define "Qualified" as Top 24
    # Create 4 buckets
    tp = df_compare[(df_compare['Predicted Rank'] <= 24) & (df_compare['Actual Rank'] <= 24)]
    tn = df_compare[(df_compare['Predicted Rank'] > 24) & (df_compare['Actual Rank'] > 24)]
    fp = df_compare[(df_compare['Predicted Rank'] <= 24) & (df_compare['Actual Rank'] > 24)] # Predicted In, Actually Out
    fn = df_compare[(df_compare['Predicted Rank'] > 24) & (df_compare['Actual Rank'] <= 24)] # Predicted Out, Actually In

    # Print the detailed lists
    print("\n--- QUALIFICATION ANALYSIS (Top 24) ---")
    print(f"Correctly Predicted Qualified ({len(tp)}): {', '.join(tp['Team'].values)}")
    print(f"Correctly Predicted Eliminated ({len(tn)}): {', '.join(tn['Team'].values)}")
    print(f"\nFALSE HOPES (Predicted In, Actually Out): {', '.join(fp['Team'].values)}")
    print(f"SURPRISE QUALIFIERS (Predicted Out, Actually In): {', '.join(fn['Team'].values)}")

    # Simple Visual Matrix
    matrix_data = [[len(tp), len(fp)], [len(fn), len(tn)]]
    
    fig, ax = plt.subplots(figsize=(6, 6))
    ax.imshow(matrix_data, cmap='Blues', alpha=0.3)
    
    # Add text labels
    labels = [[f"Correctly Qualified\n{len(tp)}", f"False Hopes\n{len(fp)}"],
              [f"Surprise Qualifiers\n{len(fn)}", f"Correctly Eliminated\n{len(tn)}"]]
    
    for i in range(2):
        for j in range(2):
            ax.text(j, i, labels[i][j], ha='center', va='center', fontsize=12, fontweight='bold', color='black')
            
    ax.set_xticks([0, 1])
    ax.set_xticklabels(['Predicted: IN', 'Predicted: OUT'])
    ax.set_yticks([0, 1])
    ax.set_yticklabels(['Actual: IN', 'Actual: OUT'])
    
    plt.title("Qualification Prediction Accuracy (Top 24)")
    plt.tight_layout()
    plt.savefig('qualification_matrix.png', dpi=300)
    plt.show()

if __name__ == "__main__":
    main()
    plot_surprises()
    analyze_lowlands()