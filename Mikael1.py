import numpy as np

def decide_move(my_moves, opponent_moves):
    
    defect_max = 5
    defect_min = 1
    coop_max = 3
    coop_min = 0
    
    temp = []
    
    for i in opponent_moves: # p cooperate
        if i == 'defect':
            temp.append(0)
        else:
            temp.append(1)
            
    p_coop = np.mean(temp) if temp else 0.5
            
    ev_defect = p_coop * defect_max + (1 - p_coop) * defect_min
    ev_cooperate = p_coop * coop_max + (1 - p_coop) * coop_min
    
    if ev_defect > ev_cooperate:
        return 'defect'
    else:
        return 'cooperate'