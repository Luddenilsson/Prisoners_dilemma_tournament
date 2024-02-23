import importlib
import os
import seaborn as sns
import matplotlib.pyplot as plt
import time

# Define a global figure object and color dict to be used for updating the plot
fig = None
color_dict = None

def execute_match(player1_module, player2_module):

    # Import player decision functions from modules
    player1_decision_func = importlib.import_module(player1_module).decide_move
    player2_decision_func = importlib.import_module(player2_module).decide_move

    # Initialize lists to store moves for each player in each round
    all_rounds_player1 = []
    all_rounds_player2 = []

    # Execute 100 rounds
    for round_num in range(100):
        # Get moves for the current round using decision functions
        player1_move = player1_decision_func(all_rounds_player1, all_rounds_player2)
        player2_move = player2_decision_func(all_rounds_player2, all_rounds_player1)

        # Append moves to the lists
        all_rounds_player1.append(player1_move)
        all_rounds_player2.append(player2_move)

    # Calculate total scores using the calculate_scores function
    total_scores = calculate_scores(all_rounds_player1, all_rounds_player2)

    return total_scores


def calculate_scores(all_rounds_player1, all_rounds_player2):
    total_score_player1 = 0
    total_score_player2 = 0

    for round_num in range(len(all_rounds_player1)):
        player1_move = all_rounds_player1[round_num]
        player2_move = all_rounds_player2[round_num]

        # Example scoring logic (you can replace this with your own)
        if player1_move == 'cooperate' and player2_move == 'cooperate':
            total_score_player1 += 3
            total_score_player2 += 3
        elif player1_move == 'defect' and player2_move == 'cooperate':
            total_score_player1 += 5
        elif player1_move == 'cooperate' and player2_move == 'defect':
            total_score_player2 += 5
        elif player1_move == 'defect' and player2_move == 'defect':
            total_score_player1 += 1
            total_score_player2 += 1

    return total_score_player1, total_score_player2


def visualize_tournament_colored_bar_chart(tournament_results, player_modules_list):
    global fig, color_dict  # Declare fig and color_palette as global variables
    
    # Convert tournament results to a DataFrame for easier plotting with Seaborn
    import pandas as pd
    df = pd.DataFrame(tournament_results, columns=['Player', 'Score'])

    # Add a 'Competitor' column based on the player module
    df['Competitor'] = df['Player'].apply(lambda x: x[:-1])

    # Sort the DataFrame by score in descending order
    df = df.sort_values(by='Score', ascending=False)

    # Set up Seaborn style
    sns.set(style="whitegrid")

    # Create a colored bar chart
    if fig is None or color_dict is None:
        global ax
        fig, ax = plt.subplots(figsize=(10, 6))
        color_palette = sns.color_palette('Set1', n_colors=len(df.Competitor.unique()))
        color_dict = {df.Competitor.unique()[i]: color_palette[i] for i in range(len(df.Competitor.unique()))}
        ax = sns.barplot(x='Player', y='Score', data=df, hue='Competitor', palette=color_dict)
        plt.title('Tournament Results with Colored Bars')
        plt.xlabel('Player')
        plt.ylabel('Score')
        plt.legend(title='Competitor', loc='upper right', bbox_to_anchor=(1.15, 1))
    else:
        # Clear the existing plot
        ax.clear()

        # Create a new colored bar chart with the same color palette
        ax = sns.barplot(x='Player', y='Score', data=df, hue='Competitor', palette=color_dict, ax=ax)

    # Add values on top of the bars
    for p in ax.patches:
        if p.xy != (0, 0):
            ax.annotate(format(p.get_height(), '.0f'),
                        (p.get_x() + p.get_width() / 2., p.get_height()),
                        ha='center', va='center',
                        xytext=(0, 9),
                        textcoords='offset points')

    plt.pause(7)  # Pause for 7 seconds
    plt.draw()  # Redraw the plot

# Function to run the tournament round-robin style
def run_tournament_round_robin(player_modules_list):
    # Initialize player scores
    player_scores = {player: 0 for player in player_modules_list}

    # Generate all possible pairs for matches
    schedule = round_schedule(player_modules_list)

    # Run matches and visualize results for each round
    for round_matches in schedule:
        # Execute matches for the current round
        for player1, player2 in round_matches:
            
            score1_lst = []
            score2_lst = []
            if player1 == 'Round off' or player2 == 'Round off':
                print(player1, player2)
                continue

            for i in range(10):
                score1, score2 = execute_match(player1, player2)
                score1_lst.append(score1)
                score2_lst.append(score2)
            player_scores[player1] += sum(score1_lst) / len(score1_lst)
            player_scores[player2] += sum(score2_lst) / len(score2_lst)

        # Visualize the results after each round
        visualize_tournament_colored_bar_chart(list(player_scores.items()), player_modules_list)

    # Return the final scores
    return list(player_scores.items())

def round_schedule(player_modules_list):
    
    if len(player_modules_list) % 2:
        player_modules_list.append('Round off')
    print(player_modules_list)
    n = len(player_modules_list)
    print(n)
    matchs = []
    fixtures = []
    for fixture in range(1, n):
        for i in range(n//2):
            matchs.append((player_modules_list[i], player_modules_list[n - 1 - i]))
        player_modules_list.insert(1, player_modules_list.pop())
        fixtures.insert(len(fixtures)//2, matchs)
        matchs = []

    return fixtures



if __name__ == "__main__":
    # Fill the list of the names of the files of the different players
    player_modules_list = ['Ludde1', 'Ludde2', 'Ingrid1','Mikael1', 'Mikael2', 'Axel1', 'David1', 'Mark1'] 
    #player_modules_list = ['Ludde1', 'Ludde2', 'Axel1', 'Axel2', 'Mikael1', 'Mikael2', 'Mark1', 'Mark2', 'David1', 'David2', 'Ingrid1', 'Ingrid2', 'Philip1', 'Philip2', 'Nora1', 'Nora2']
    # Run the tournament and get total scores
    tournament_results = run_tournament_round_robin(player_modules_list)

    # Print the results
    for player, score in tournament_results:
        print(f"{player}: {score} points")   
    
    visualize_tournament_colored_bar_chart(tournament_results, player_modules_list)
    plt.show()