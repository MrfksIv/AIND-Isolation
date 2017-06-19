import random
from random import randint
from multiprocessing import Pool
from scipy.stats import norm
import numpy as np
import pickle

class SearchTimeout(Exception):
    """Subclass base exception for code clarity. """
    pass

def estimate_true_probability_range(prob, sample_size, confidence_level):
    """
    For large samples, we can approximate the binomial distribution's error by 
    a standard normal distribution
    """
    x = 1.96*np.sqrt(( (1/sample_size) * prob * (1-prob)) )
    return (prob -x , prob + x)


def drange(start, stop, step):
    res = start
    while res < stop:
        yield res
        res += step


def custom_score(game, player):
    
    opponent = game.get_opponent(player)
    util = float(len(game.get_legal_moves(player)) - len(game.get_legal_moves(opponent)))
    return util

def custom_score_with_weights(game, player, own_weight, opp_weight):
    opponent = game.get_opponent(player)
    util = float(own_weight * len(game.get_legal_moves(player)) - opp_weight* len(game.get_legal_moves(opponent)))
    return util

class IsolationPlayer:
    def __init__(self, player_type="standard", search_depth=3, score_fn=custom_score, timeout=10., own_weight=1., opp_weight=1.):
        self.search_depth = search_depth
        self.score = custom_score_with_weights
        self.time_left = None
        self.TIMER_THRESHOLD = timeout
        self.own_weight = own_weight
        self.opp_weight = opp_weight
        self.move_index = 0
        self.player_type = player_type

class AlphaBetaPlayer(IsolationPlayer):
   
    def get_move(self, game, time_left):
        
        self.time_left = time_left
        best_move = (-1, -1)

        try:
            depth = 1
            while True:
                best_move = self.alphabeta(game, depth)
                depth += 1
        except SearchTimeout:
            pass

        return best_move

    def alphabeta(self, game, depth, alpha=float("-inf"), beta=float("inf")):
      
        if self.time_left() < self.TIMER_THRESHOLD:
            raise SearchTimeout()

        self.move_index += 1
        opponent = game.get_opponent(game.active_player)
        best_move = (-1, -1)
        best_util = float("-inf")

        if self.time_left() < self.TIMER_THRESHOLD:
            return best_move

        possible_moves = game.get_legal_moves()

        if len(possible_moves) == 0:
            return best_move

        for move in possible_moves:
            forecasted_game = game.forecast_move(move)
            new_util = self.alphabeta_min(forecasted_game,
                depth-1, alpha, beta, game.active_player)

            if new_util > best_util:
                best_util = new_util
                best_move = move

            alpha = max(alpha, best_util)
        return best_move

    def alphabeta_max(self, game, depth, alpha, beta, player):
        best_util = float("-inf")

        if self.time_left() < self.TIMER_THRESHOLD:
            raise SearchTimeout()

        if depth == 0:
            t = self.score(game, player, self.own_weight , self.opp_weight)
            return t

        legal_moves = game.get_legal_moves()

        if len(legal_moves) == 0:
            return game.utility(player)

        for move in legal_moves:
            forecasted_game = game.forecast_move(move)
            move_util = self.alphabeta_min(forecasted_game, depth-1, alpha, beta, player)
            if move_util > best_util:
                best_util = move_util
            if move_util >= beta:
                return move_util

            alpha = max(alpha, best_util)

        return best_util


    def alphabeta_min(self, game, depth, alpha, beta, player):
        best_util = float("inf")
        if self.time_left() < self.TIMER_THRESHOLD:
            raise SearchTimeout()

        if depth == 0:
            t = self.score(game, player, self.own_weight , self.opp_weight)
            return t

        legal_moves = game.get_legal_moves()

        if len(legal_moves) == 0:
            return game.utility(player)

        for move in legal_moves:
            forecasted_game = game.forecast_move(move)
            move_util = self.alphabeta_max(forecasted_game, depth-1, alpha, beta, player)
            if move_util < best_util:
                best_util = move_util
            if move_util <= alpha:
                return move_util

            
            beta = min(beta, best_util)

        return best_util

        self.move_index = 0


def run_game(args):
    global wins
    global var_weight_player

    player1, player2, game_number = args

    if game_number % 2 == 0:
        game = Board(player1, player2)
    else:
        game = Board(player2, player1)
                
    winner, history, outcome = game.play()

    del game
    if(game_number % 10 == 0): 
        print("played {} games...".format(game_number))
    if winner.player_type == "variable_w_player":
        return 1
    else:
        return 0      


if __name__ == "__main__":
    
    from isolation import Board

    own_weight_list_generator = drange(1.3, 1.4, 0.05)
    

    results_dict = {}
    results_list = []
    total_games_to_play = 250000

    best_score = 0.
    best_weights = (1, 1)

    p = Pool(8)

    for own_w in own_weight_list_generator:

        opponent_weight_list_generator = drange(1.6, 1.7, 0.05)
        
        for opp_w in opponent_weight_list_generator:
            print("own weight: {} , opponent weight: {}".format(own_w, opp_w))
            if own_w == opp_w:
                print("weights are equal. Skipping...")
                continue
            if own_w % 2 == 0 and opp_w % 2 == 0:
                print("weights are the equivalent to {}. Skipping...".format((own_w/2, opp_w/2)))

            if own_w % 3 == 0 and opp_w % 3 == 0:
                print("weights are the equivalent to {}. Skipping...".format((own_w/3, opp_w/3)))
            wins = 0
            
            std_weight_player = AlphaBetaPlayer()
            var_weight_player = AlphaBetaPlayer(player_type="variable_w_player", search_depth=3, score_fn=custom_score, 
                    timeout=10., own_weight=own_w, opp_weight=opp_w)
            
            # print("standard player is at: {}".format(std_weight_player))
            # print("varying weight player is at: {}".format(var_weight_player))
            
            results = p.map(run_game, [(std_weight_player, var_weight_player, game_i ) for  game_i in range(1, total_games_to_play + 1)])
            wins = sum(results)
            # for game_i in range(1, total_games_to_play + 1):  

            #     run_game((std_weight_player, var_weight_player, game_i))
                        
            current_score = float(wins/total_games_to_play)
            
            print("won {} of {}".format(wins, total_games_to_play))
            print("current score of {}. Previous best score of {}".format(current_score, best_score))
            if current_score > best_score:
                print("new score is better. Updating best_weights and score...")
                best_weights = (own_w, opp_w)
                print("new best weights: {}".format(best_weights))
                best_score = current_score
            results_dict["own_w_{%d}_VS_opp_w_{%d}"%(own_w, opp_w)]= current_score
            results_list.append((own_w, opp_w, current_score))
    
    pickle.dump( results_dict, open( "results_dict_13-16.p", "wb" ) )
    pickle.dump( results_list, open( "results_list_13-16.p", "wb" ) )

    # place player 1 on the board at row 2, column 3, then place player 2 on
    # the board at row 0, column 5; display the resulting board state.  Note
    # that the .apply_move() method changes the calling object in-place.
    # game.apply_move((2, 3))
    # game.apply_move((0, 5))
    # print(game.to_string())

    # # players take turns moving on the board, so player1 should be next to move
    # assert(player1 == game.active_player)

    # # get a list of the legal moves available to the active player
    # print(game.get_legal_moves())

    # # get a successor of the current state by making a copy of the board and
    # # applying a move. Notice that this does NOT change the calling object
    # # (unlike .apply_move()).
    # new_game = game.forecast_move((1, 1))
    # assert(new_game.to_string() != game.to_string())
    # print("\nOld state:\n{}".format(game.to_string()))
    # print("\nNew state:\n{}".format(new_game.to_string()))

    # # play the remainder of the game automatically -- outcome can be "illegal
    # # move", "timeout", or "forfeit"
    # winner, history, outcome = game.play()


    # print("\nWinner: {}\nOutcome: {}".format(winner, outcome))
    # print(game.to_string())
    # print("Move history:\n{!s}".format(history))
    # print("My player won: {}".format(game.is_winner(player2)))