import random

def adaptive_pavlov(history):
    """
    uses Adaptive Pavlov Strategy for Iterated Prisoner's Dilemma
    Tit-for-tat (TFT) for first six rounds, places opponent into one of five categories
    according to its responses & plays an optimal strategy for each.
    Tit-for-tat (TFT) = cooperates on 1st round and imitates its opponent's previous move thereafter.

    args:
        history: list of tuples representing history of game, where each tuple
        contains actions of both players in a single round.

    returns:
        action to take in next round (cooperate or defect).
    """

    # init cooperation probability & memory size
    cooperation_prob = 1.0 # I'm fully cooperative
    rounds = 5 # number of goes before making a decision

    # if there is no history, cooperate
    if not history:
        return "cooperate"

    # get opponent's actions from history
    #opponent_actions = [action for _, action in history]
    opponent_actions = []
    for round_history in history:
        opponent_action = round_history[1]
        # add opponent's action to list
        opponent_actions.append(opponent_action)

    # calc number of times opponent cooperated after I cooperated
    cooperate_after_cooperate = sum(1 for i in range(len(opponent_actions) - 1)
    if opponent_actions[i] == "cooperate" and opponent_actions[i + 1] == "cooperate")

    # calc number of times opponent defected after I cooperated
    defect_after_cooperate = sum(1 for i in range(len(opponent_actions) - 1)
    if opponent_actions[i] == "cooperate" and opponent_actions[i + 1] == "defect")

    # update cooperation probability based on recent history
    if len(opponent_actions) >= rounds:
        recent_history = opponent_actions[-rounds:]
        cooperation_prob = sum(1 for action in recent_history if action == "cooperate") / len(recent_history)

    # cooperate with some probability based on recent history
    if random.random() < cooperation_prob:
        return "cooperate"
    else:
        return "defect"

def decide_move(my_moves, opponent_moves):
    # decision logic based on last move of both players
    if len(my_moves) > 0 and my_moves[-1] == "cooperate" and opponent_moves[-1] == "defect":
        return "defect"  # defect if opponent defects after we cooperate
    else:
        return adaptive_pavlov(list(zip(my_moves, opponent_moves)))  # use Adaptive Pavlov otherwise

# usage
my_moves = ["cooperate", "cooperate", "defect", "cooperate", "defect", "defect"]
opponent_moves = ["cooperate", "defect", "cooperate", "cooperate", "cooperate", "cooperate"]

action = decide_move(my_moves, opponent_moves)
print(f"action: {action}")