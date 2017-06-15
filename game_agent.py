"""Finish all TODO items in this file to complete the isolation project, then
test your agent's strength against a set of known agents using tournament.py
and include the results in your report.
"""
import random


class SearchTimeout(Exception):
    """Subclass base exception for code clarity. """
    pass


def custom_score(game, player):
    """Calculate the heuristic value of a game state from the point of view
    of the given player.

    This should be the best heuristic function for your project submission.

    Note: this function should be called from within a Player instance as
    `self.score()` -- you should not need to call this function directly.

    Parameters
    ----------
    game : `isolation.Board`
        An instance of `isolation.Board` encoding the current state of the
        game (e.g., player locations and blocked cells).

    player : object
        A player instance in the current game (i.e., an object corresponding to
        one of the player objects `game.__player_1__` or `game.__player_2__`.)

    Returns
    -------
    float
        The heuristic value of the current game state to the specified player.
    """
    # TODO: finish this function!
    # raise NotImplementedError
    opponent = game.get_opponent(player)
    util = float(len(game.get_legal_moves(player)) - len(game.get_legal_moves(opponent)))
    return util


def custom_score_2(game, player):
    """Calculate the heuristic value of a game state from the point of view
    of the given player.

    Note: this function should be called from within a Player instance as
    `self.score()` -- you should not need to call this function directly.

    Parameters
    ----------
    game : `isolation.Board`
        An instance of `isolation.Board` encoding the current state of the
        game (e.g., player locations and blocked cells).

    player : object
        A player instance in the current game (i.e., an object corresponding to
        one of the player objects `game.__player_1__` or `game.__player_2__`.)

    Returns
    -------
    float
        The heuristic value of the current game state to the specified player.
    """
    # TODO: finish this function!
    raise NotImplementedError


def custom_score_3(game, player):
    """Calculate the heuristic value of a game state from the point of view
    of the given player.

    Note: this function should be called from within a Player instance as
    `self.score()` -- you should not need to call this function directly.

    Parameters
    ----------
    game : `isolation.Board`
        An instance of `isolation.Board` encoding the current state of the
        game (e.g., player locations and blocked cells).

    player : object
        A player instance in the current game (i.e., an object corresponding to
        one of the player objects `game.__player_1__` or `game.__player_2__`.)

    Returns
    -------
    float
        The heuristic value of the current game state to the specified player.
    """
    # TODO: finish this function!
    raise NotImplementedError


class IsolationPlayer:
    """Base class for minimax and alphabeta agents -- this class is never
    constructed or tested directly.

    ********************  DO NOT MODIFY THIS CLASS  ********************

    Parameters
    ----------
    search_depth : int (optional)
        A strictly positive integer (i.e., 1, 2, 3,...) for the number of
        layers in the game tree to explore for fixed-depth search. (i.e., a
        depth of one (1) would only explore the immediate sucessors of the
        current state.)

    score_fn : callable (optional)
        A function to use for heuristic evaluation of game states.

    timeout : float (optional)
        Time remaining (in milliseconds) when search is aborted. Should be a
        positive value large enough to allow the function to return before the
        timer expires.
    """
    def __init__(self, search_depth=3, score_fn=custom_score, timeout=10.):
        self.search_depth = search_depth
        self.score = score_fn
        self.time_left = None
        self.TIMER_THRESHOLD = timeout

        self.move_index = 0


class MinimaxPlayer(IsolationPlayer):
    """Game-playing agent that chooses a move using depth-limited minimax
    search. You must finish and test this player to make sure it properly uses
    minimax to return a good move before the search time limit expires.
    """

    def get_move(self, game, time_left):
        """Search for the best move from the available legal moves and return a
        result before the time limit expires.

        **************  YOU DO NOT NEED TO MODIFY THIS FUNCTION  *************

        For fixed-depth search, this function simply wraps the call to the
        minimax method, but this method provides a common interface for all
        Isolation agents, and you will replace it in the AlphaBetaPlayer with
        iterative deepening search.

        Parameters
        ----------
        game : `isolation.Board`
            An instance of `isolation.Board` encoding the current state of the
            game (e.g., player locations and blocked cells).

        time_left : callable
            A function that returns the number of milliseconds left in the
            current turn. Returning with any less than 0 ms remaining forfeits
            the game.

        Returns
        -------
        (int, int)
            Board coordinates corresponding to a legal move; may return
            (-1, -1) if there are no available legal moves.
        """
        self.time_left = time_left

        # Initialize the best move so that this function returns something
        # in case the search fails due to timeout
        best_move = (-1, -1)

        try:
            # The try/except block will automatically catch the exception
            # raised when the timer is about to expire.
            return self.minimax(game, self.search_depth)

        except SearchTimeout:
            pass  # Handle any actions required after timeout as needed

        # Return the best move from the last completed search iteration
        return best_move

    def minimax(self, game, depth):
        """Implement depth-limited minimax search algorithm as described in
        the lectures.

        This should be a modified version of MINIMAX-DECISION in the AIMA text.
        https://github.com/aimacode/aima-pseudocode/blob/master/md/Minimax-Decision.md

        **********************************************************************
            You MAY add additional methods to this class, or define helper
                 functions to implement the required functionality.
        **********************************************************************

        Parameters
        ----------
        game : isolation.Board
            An instance of the Isolation game `Board` class representing the
            current game state

        depth : int
            Depth is an integer representing the maximum number of plies to
            search in the game tree before aborting

        Returns
        -------
        (int, int)
            The board coordinates of the best move found in the current search;
            (-1, -1) if there are no legal moves

        Notes
        -----
            (1) You MUST use the `self.score()` method for board evaluation
                to pass the project tests; you cannot call any other evaluation
                function directly.

            (2) If you use any helper functions (e.g., as shown in the AIMA
                pseudocode) then you must copy the timer check into the top of
                each helper function or else your agent will timeout during
                testing.
        """
        self.move_index += 1
        opponent = game.get_opponent(game.active_player)
        print("==== BEGIN  FN CALL=====")
        print("player 1 at: {} || player 2 at: {}"
                .format(game.get_player_location(opponent),game.get_player_location(game.active_player)))
        print("MOVE ({})".format(self.move_index))
        print("====---------------=====")

        best_move = (-1, -1)
        best_util = float("-inf")

        if self.time_left() < self.TIMER_THRESHOLD:
            # print("out of time... Available best move: {}".format(best_move))
            return best_move

        # print("minimax called by {}".format(game.active_player))

        possible_moves = game.get_legal_moves()
        print("Player {} moves: {}".format(game.active_player, possible_moves))

        if len(possible_moves) == 0:
            return best_move

        for move in possible_moves:
            forecasted_game = game.forecast_move(move)
            print("player 1 at: {} || player 2 at: {}"
                    .format(forecasted_game.get_player_location(opponent), forecasted_game.get_player_location(forecasted_game.inactive_player)))
            new_util = self._minimax_min(forecasted_game, depth-1, game.active_player)

            if new_util == float("inf"):
                print("found winning move...")
                return best_move

            print("new_util: {} current best:{}".format(new_util, best_util))
            if new_util > best_util:
                print("new best...")
                best_util = new_util
                best_move = move

        print("best move is: {}".format(move))
        print("= = = =  = = = = = = = = = = = = = = = = = =")
        return best_move


    def _minimax_max(self, game, depth, player):
        # print("_minimax_max, the player passed is: {} and active player is : {}".format(player, game.active_player))
        best_util = float("-inf")

        if self.time_left() < self.TIMER_THRESHOLD:
            return best_util

        if depth == 0 and self.time_left() > self.TIMER_THRESHOLD:
            print("reached depth 0 at minimax_max with time to estimate score!")
            t = self.score(game, player)
            print(t)
            return t
        elif depth == 0 and self.time_left() <= self.TIMER_THRESHOLD:
            print("reached depth 0 at minimax_max BUT NO TIME to estimate score!")
            print(best_util)
            return best_util

        legal_moves = game.get_legal_moves()
        print("legal moves in _minimax_max of player {} @ loc {}: {}".format(
            game.active_player, game.get_player_location(game.active_player),legal_moves ))

        if len(legal_moves) == 0:
            return game.utility(player)

        for move in legal_moves:
            f_game = game.forecast_move(move)
            move_util = self._minimax_min(f_game, depth - 1, player)
            if move_util > best_util:
                best_util = move_util

        return best_util

    def _minimax_min(self, game, depth, player):
        # print("_minimax_min, the player passed is: {} and active player is : {}".format(player, game.active_player))
        opponent = game.get_opponent(player)

        # print("At depth {},  _minimax_min player is: {}".format(depth, player))
        # print("active player is: {}".format(game.active_player))
        best_util = float("inf")

        if self.time_left() < self.TIMER_THRESHOLD:
            print("no time left - returning best util")
            return best_util

        if depth == 0 and self.time_left() > self.TIMER_THRESHOLD:
            print("reached depth 0 at minimax_min with time to estimate score!")
            t = self.score(game, player)
            print(t)
            return t
        elif depth == 0 and self.time_left() <= self.TIMER_THRESHOLD:
            print("reached depth 0 at minimax_min BUT NO TIME to estimate score!")
            print(best_util)
            return best_util

        legal_moves = game.get_legal_moves()
        print("legal moves in _minimax_min of player {} @ loc {}: {}".format(
            game.active_player, game.get_player_location(game.active_player),legal_moves ))

        if len(legal_moves) == 0:
            return game.utility(player)

        for move in legal_moves:
            f_game = game.forecast_move(move)
            move_util = self._minimax_max(f_game, depth - 1, player)
            if move_util < best_util:
                best_util = move_util

        return best_util






class AlphaBetaPlayer(IsolationPlayer):
    """Game-playing agent that chooses a move using iterative deepening minimax
    search with alpha-beta pruning. You must finish and test this player to
    make sure it returns a good move before the search time limit expires.
    """
    global_alpha = float("-inf")
    global_beta=float("inf")

    def get_move(self, game, time_left):
        """Search for the best move from the available legal moves and return a
        result before the time limit expires.

        Modify the get_move() method from the MinimaxPlayer class to implement
        iterative deepening search instead of fixed-depth search.

        **********************************************************************
        NOTE: If time_left() < 0 when this function returns, the agent will
              forfeit the game due to timeout. You must return _before_ the
              timer reaches 0.
        **********************************************************************

        Parameters
        ----------
        game : `isolation.Board`
            An instance of `isolation.Board` encoding the current state of the
            game (e.g., player locations and blocked cells).

        time_left : callable
            A function that returns the number of milliseconds left in the
            current turn. Returning with any less than 0 ms remaining forfeits
            the game.

        Returns
        -------
        (int, int)
            Board coordinates corresponding to a legal move; may return
            (-1, -1) if there are no available legal moves.
        """
        self.time_left = time_left

        # Initialize the best move so that this function returns something
        # in case the search fails due to timeout
        best_move = (-1, -1)

        try:
            # The try/except block will automatically catch the exception
            # raised when the timer is about to expire.
            return self.alphabeta(game, self.search_depth, self.global_alpha, self.global_beta)

        except SearchTimeout:
            pass  # Handle any actions required after timeout as needed

        # Return the best move from the last completed search iteration
        return best_move

    global_alpha = float("-inf")
    global_beta=float("inf")

    def alphabeta(self, game, depth, alpha=float("-inf"), beta=float("inf")):
        """Implement depth-limited minimax search with alpha-beta pruning as
        described in the lectures.

        This should be a modified version of ALPHA-BETA-SEARCH in the AIMA text
        https://github.com/aimacode/aima-pseudocode/blob/master/md/Alpha-Beta-Search.md

        **********************************************************************
            You MAY add additional methods to this class, or define helper
                 functions to implement the required functionality.
        **********************************************************************

        Parameters
        ----------
        game : isolation.Board
            An instance of the Isolation game `Board` class representing the
            current game state

        depth : int
            Depth is an integer representing the maximum number of plies to
            search in the game tree before aborting

        alpha : float
            Alpha limits the lower bound of search on minimizing layers

        beta : float
            Beta limits the upper bound of search on maximizing layers

        Returns
        -------
        (int, int)
            The board coordinates of the best move found in the current search;
            (-1, -1) if there are no legal moves

        Notes
        -----
            (1) You MUST use the `self.score()` method for board evaluation
                to pass the project tests; you cannot call any other evaluation
                function directly.

            (2) If you use any helper functions (e.g., as shown in the AIMA
                pseudocode) then you must copy the timer check into the top of
                each helper function or else your agent will timeout during
                testing.
        """
        if self.time_left() < self.TIMER_THRESHOLD:
            raise SearchTimeout()

        self.move_index += 1
        opponent = game.get_opponent(game.active_player)
        print("==== BEGIN  FN CALL=====")
        print("player 1 at: {} || player 2 at: {}"
                .format(game.get_player_location(opponent),game.get_player_location(game.active_player)))
        print("MOVE ({})".format(self.move_index))
        print("====---------------=====")

        best_move = (-1, -1)
        best_util = float("-inf")

        if self.time_left() < self.TIMER_THRESHOLD:
            # print("out of time... Available best move: {}".format(best_move))
            return best_move

        # print("minimax called by {}".format(game.active_player))

        possible_moves = game.get_legal_moves()
        print("Player {} moves: {}".format(game.active_player, possible_moves))

        if len(possible_moves) == 0:
            return best_move


        for move in possible_moves:
            forecasted_game = game.forecast_move(move)
            print("player 1 at: {} || player 2 at: {}"
                    .format(forecasted_game.get_player_location(opponent), forecasted_game.get_player_location(forecasted_game.inactive_player)))
            new_util = self.alphabeta_min(forecasted_game,
                depth-1, alpha, beta, game.active_player)


            print("new_util: {} current best:{}".format(new_util, best_util))
            if new_util > best_util:
                print("new best...")
                best_util = new_util
                best_move = move

            # if new_util >= self.global_beta:
            #     print("pruning rest of moves at the top...:{}".format(possible_moves[possible_moves.index(move)+1:]))
            #     return best_move

            alpha = max(alpha, best_util)
        print("best move is: {}".format(move))
        print("= = = =  = = = = = = = = = = = = = = = = = =")
        return best_move

        # TODO: finish this function!
        # return game.get_legal_moves()[0]

    def alphabeta_max(self, game, depth, alpha, beta, player):
        print("In alphabeta_max, player is: {}".format(player))
        best_util = float("-inf")
        if self.time_left() < self.TIMER_THRESHOLD:
            raise SearchTimeout()

        if depth == 0:
            print("reached depth 0 at minimax_max with time to estimate score!")
            t = self.score(game, player)
            print(t)
            return t

        legal_moves = game.get_legal_moves()
        print("legal moves in alphabeta_max of player {} @ loc {}: {}".format(
            game.active_player, game.get_player_location(game.active_player),legal_moves ))

        if len(legal_moves) == 0:
            print("{} ran out of moves. Utility is:{}".format(player, game.utility(player)))
            return game.utility(player)

        for move in legal_moves:
            forecasted_game = game.forecast_move(move)
            move_util = self.alphabeta_min(forecasted_game, depth-1, alpha, beta, player)
            if move_util > best_util:
                best_util = move_util
            if move_util >= beta:
                print("pruning rest of moves...:{}".format(legal_moves[legal_moves.index(move)+1:]))
                return move_util

            print("alpha:{}, best_util: {}".format(alpha, best_util))
            if alpha > best_util:
                print("alpha is smaller, updating alpha...")
            alpha = max(alpha, best_util)

        return best_util


    def alphabeta_min(self, game, depth, alpha, beta, player):
        print("In alphabeta_min, player is: {}".format(player))
        best_util = float("inf")
        if self.time_left() < self.TIMER_THRESHOLD:
            raise SearchTimeout()

        if depth == 0:
            print("reached depth 0 at minimax_max with time to estimate score!")
            t = self.score(game, player)
            print(t)
            return t

        legal_moves = game.get_legal_moves()
        print("legal moves in alphabeta_min of player {} @ loc {}: {}".format(
            game.active_player, game.get_player_location(game.active_player),legal_moves ))

        if len(legal_moves) == 0:
            print("{} has no more moves Utility is:{}".format(player, game.utility(player)))
            return game.utility(player)

        for move in legal_moves:
            forecasted_game = game.forecast_move(move)
            move_util = self.alphabeta_max(forecasted_game, depth-1, alpha, beta, player)
            if move_util < best_util:
                best_util = move_util
            if move_util <= alpha:
                print("pruning rest of moves...: {}".format(legal_moves[legal_moves.index(move)+1:]))
                return move_util

            print("beta:{}, best_util: {}".format(beta, best_util))
            if beta < best_util:
                print("beta is smaller, updating beta...")
            beta = min(beta, best_util)

        return best_util
