import random


def cvAuth(sim_score):
    if sim_score < 5.5:
        return random.random()*10 + 20
    else:
        if sim_score*8 > 93:
            return random.random()*10+80
        else:
            return sim_score*8
