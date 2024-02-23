def decide_move(my_moves, opponent_moves):
    num_rounds = len(my_moves)
    forgiveness_round = 5  
    
    if num_rounds == 0:
        return 'cooperate'

    last_opponent_move = opponent_moves[-1]
    
    if last_opponent_move == 'defect':
        return 'defect' 
    
    if num_rounds >= forgiveness_round:
        if all(move == 'cooperate' for move in opponent_moves[-forgiveness_round:]):
            return 'cooperate'
    
    return last_opponent_move