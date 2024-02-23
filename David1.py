def decide_move(my_moves, opponent_moves):
    # Example decision-making logic. my_moves and opponent_moves are lists with all previous moves. All
    # elements in them are either 'cooperate' or 'defect'. You can use them to create your decision logic.
    # The function must return either 'cooperate' or 'defect'
    if len(opponent_moves) == 0:
        return 'cooperate'
    elif opponent_moves[-1] == 'defect':
        return 'defect'
    else:
        return 'cooperate'