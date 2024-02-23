

def decide_move(my_moves, opponent_moves):
    # Example decision-making logic (you can replace this with your own)
    if len(my_moves) < 3:
        return 'cooperate'
    elif my_moves[-2] == 'defect' and opponent_moves[-1] == 'cooperate':
        return 'defect'
    elif my_moves[-3] == 'defect' and opponent_moves[-2:] == ['cooperate', 'cooperate']:
        return 'defect'
    elif my_moves[-2:] == ['defect', 'defect'] or opponent_moves[-1] == 'defect':
        return 'defect'
    elif len(my_moves) == 10:
        return 'defect'
    else:
        return 'cooperate'