from random import random, choice, randint
 
C = "C"
D = "D"

S = 0
P = 1
R = 3
T = 5

rewards = {(C, C): R, (C, D): S, (D, C): T, (D, D): P}


class OpponentStrategy:
    @classmethod
    def random(cls):
        return choice([D, C])

    @classmethod
    def always_d(cls):
        return D

    @classmethod
    def always_c(cls):
        return C

    @classmethod
    def tit_for_tat(cls, moves):
        if (moves is None) or (len(moves) == 0):
            return cls.random()

        return moves[-1][0]

    @classmethod
    def strategy(cls, name="random", moves=[]):
        if name == "random":
            return cls.random()
        elif name == "always_c":
            return cls.always_c()
        elif name == "always_d":
            return cls.always_d()
        elif name == "tit_for_tat":
            return cls.tit_for_tat(moves)


def my_strategy(moves, epsilon=0.05):
    # Initialize by trying different things
    if moves is None or len(moves) <= 5:
        return choice([C, D])

    # exploration
    if random() < epsilon:
        return choice([C, D])

    proba_play_next = compute_reaction_probability(moves)
    proba_will_c_if_c = proba_play_next[C][C]
    proba_will_d_if_d = proba_play_next[D][D]

    if (random() <= proba_will_c_if_c) and (random() <= proba_will_d_if_d):
        return C
    return D


def compute_reaction_probability(moves):
    played_after = {C: {C: 0, D: 0}, D: {C: 0, D: 0}}
    for i in range(len(moves) - 1):
        my_move = moves[i][0]
        their_next_move = moves[i + 1][1]
        played_after[my_move][their_next_move] += 1

    # Normalize
    normalize_proba(played_after[C])
    normalize_proba(played_after[D])
    return played_after


def normalize_proba(played_after):
    if (played_after[C] + played_after[D]) == 0:
        return
    played_after[C] = played_after[C] / (played_after[C] + played_after[D])
    played_after[D] = 1 - played_after[C]


def compute_overall_reward(moves):
    scores = 0
    for move in moves:
        scores += rewards[move]
    return scores


if __name__ == "__main__":
    NUM_GAME = 5
    STRATEGIES = ["tit_for_tat", "always_c", "always_d", "random"]

    strat_scores = []
    for strategy_name in STRATEGIES:
        scores = []
        for game in range(NUM_GAME):

            num_iteration = randint(50, 200)
            moves = []
            for i in range(num_iteration):
                my_move = my_strategy(moves)
                their_move = OpponentStrategy.strategy(strategy_name, moves)
                moves.append((my_move, their_move))
            current_game_score = compute_overall_reward(moves)
            scores.append(current_game_score/num_iteration)
            strat_scores.append(current_game_score/num_iteration)

        print(f"Strategy: {strategy_name}. Average score: {scores}")

    average_score = 0
    for score in strat_scores:
        average_score += score
    print(f"Final score: {average_score/len(strat_scores)}")
