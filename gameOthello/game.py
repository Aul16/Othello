import random as rd
import time
from typing import List


class Game:
    def __init__(self, nb_players: int, total_time=0) -> None:
        """
        Game Object Generator
        """
        self.nb_players = nb_players  # Convention : 1 for the mode player VS CPU
        self.grid = self.create_board()
        self.ready = False
        self.scores = self.count_player_points(self.grid)
        self.player_turn = 1  # BLACK begins
        self.moves_possible = self.coups_possibles(self.grid, self.player_turn)
        self.past_grids = []
        self.time_total = total_time
        self.timers = [
            self.time_total for _ in range(self.nb_players)
        ]  # Initialize timers
        self.start_time = time.time()
        self.memo_minmax = {}

    def create_board(self) -> List[List[int]]:
        """
        2 players grid : 8x8
        3 players grid : 9x9
        4 players grid : 10x10
        """
        tailles_grid = [8, 8, 8, 9, 10]
        size = tailles_grid[self.nb_players]

        # Creates an empty list to represent the board game
        board = []
        for row in range(size):
            line = []
            for col in range(size):
                line.append(0)  # Add an empty square on every column
            board.append(line)  # Add a line on the board game
        # Place the pieces at the beginning
        if self.nb_players in [1, 2]:
            board[3][3] = 2  # White Piece
            board[4][4] = 2  # White Piece
            board[3][4] = 1  # Black Piece
            board[4][3] = 1  # Black Piece
        elif self.nb_players == 3:
            board[3][3] = 3  # Blue Piece
            board[4][4] = 3  # Blue Piece
            board[5][5] = 3  # Blue Piece
            board[4][3] = 2  # White Piece
            board[5][4] = 2  # White Piece
            board[3][5] = 2  # White Piece
            board[5][3] = 1  # Black Piece
            board[3][4] = 1  # Black Piece
            board[4][5] = 1  # Black Piece
        elif self.nb_players == 4:
            board[3][3] = 4  # Pink Piece
            board[4][4] = 4  # Pink Piece
            board[5][5] = 4  # Pink Piece
            board[6][6] = 4  # Pink Piece
            board[4][3] = 3  # Blue Piece
            board[5][4] = 3  # Blue Piece
            board[6][5] = 3  # Blue Piece
            board[3][6] = 3  # Blue Piece
            board[5][3] = 2  # White Piece
            board[6][4] = 2  # White Piece
            board[3][5] = 2  # White Piece
            board[4][6] = 2  # White Piece
            board[6][3] = 1  # Black Piece
            board[3][4] = 1  # Black Piece
            board[4][5] = 1  # Black Piece
            board[5][6] = 1  # Black Piece

        return board

    def count_player_points(self, grid: List[List[int]]) -> List[int]:
        """
        Input : Game grid
        Return a list with the scores (sum of pieces on the board) of the players
        """
        # initialization of the player's point list to 0.
        self.scores = [0] * max(2, self.nb_players)
        # for each player of the list, we check each square to see if they have a piece .
        # if yes, we give them one point
        for i in range(max(2, self.nb_players)):
            self.scores[i] = sum([1 for line in grid for e in line if e == i + 1])
        return self.scores

    def who_won(self) -> list:
        """
        Return the list of the winner(s)
        """
        # If end of the timer in blitz, other player win
        if self.time_total > 0 and not self.is_grid_full(self.grid):
            return [self.timers.index(max(self.timers)) + 1]

        # each player's point are counted
        self.scores = self.count_player_points(self.grid)
        # search for best score and associated player(s).
        list_winner = []
        winner_points = 0
        for i in range(len(self.scores)):
            if self.scores[i] > winner_points:
                list_winner = [i + 1]
                winner_points = self.scores[i]
            elif self.scores[i] == winner_points:  # If Equality
                list_winner.append(i + 1)

        return list_winner

    def coups_possibles(self, grid: list, player: int) -> dict:
        """
        Input : Game Grid + the player who will play the turn
        Return a dictionnary of the possible moves for this player :
            - Key : tuple of a possible moves
            - Value : list of tuples : the position of the pieces to be flipped
        """
        coups_pos = {}  # Create a dictionary containing the possible moves
        for k in range(len(grid)):
            for l in range(len(grid)):
                if grid[k][l] == 0:  # Go through the empty squares of the grid
                    if k != 0:
                        # Top hand route
                        L = []  # List of the pieces to be flipped
                        i = k
                        j = l  # Hints on the path of the squares
                        pion_a_verifier = grid[i - 1][j]
                        # As long as the pawn is an enemy, we add the coordinates of the piece to be checked
                        # (here in the top direction) in the list
                        while pion_a_verifier not in [-1, 0, player] and i in range(
                            len(grid)
                        ):
                            L.append((i - 1, j))
                            i -= 1
                            try:
                                assert i > 0  # Bug side of the board
                                # The next piece is retrieved in the top direction
                                pion_a_verifier = grid[i - 1][j]
                            except:  # Next piece not defined => End of course
                                pion_a_verifier = -1
                        # If the last piece is an ally, the move is possible => pawn storage to be returned to the dictionary
                        if pion_a_verifier == player and len(L) != 0:
                            coups_pos[(k, l)] = L

                        if l != len(grid) - 1:
                            # Top left-hand route
                            L = []
                            i = k
                            j = l
                            pion_a_verifier = grid[i - 1][j + 1]
                            while (
                                pion_a_verifier not in [-1, 0, player]
                                and i in range(len(grid))
                                and j in range(len(grid))
                            ):
                                L.append((i - 1, j + 1))
                                i -= 1
                                j += 1
                                try:
                                    assert i > 0
                                    pion_a_verifier = grid[i - 1][j + 1]
                                except:
                                    pion_a_verifier = -1
                            if pion_a_verifier == player and len(L) != 0:
                                if (k, l) in coups_pos.keys():
                                    coups_pos[(k, l)] = coups_pos[(k, l)] + L
                                else:
                                    coups_pos[(k, l)] = L

                    if l != len(grid) - 1:
                        # Right-hand route
                        L = []
                        i = k
                        j = l
                        pion_a_verifier = grid[i][j + 1]
                        while pion_a_verifier not in [-1, 0, player] and j in range(
                            len(grid)
                        ):
                            L.append((i, j + 1))
                            j += 1
                            try:
                                pion_a_verifier = grid[i][j + 1]
                            except:
                                pion_a_verifier = -1
                        if pion_a_verifier == player and len(L) != 0:
                            if (k, l) in coups_pos.keys():
                                coups_pos[(k, l)] = coups_pos[(k, l)] + L
                            else:
                                coups_pos[(k, l)] = L

                        if k != len(grid) - 1:
                            # Bottom right hand route
                            L = []
                            i = k
                            j = l
                            pion_a_verifier = grid[i + 1][j + 1]
                            while (
                                pion_a_verifier not in [-1, 0, player]
                                and j in range(len(grid))
                                and i in range(len(grid))
                            ):
                                L.append((i + 1, j + 1))
                                i += 1
                                j += 1
                                try:
                                    pion_a_verifier = grid[i + 1][j + 1]
                                except:
                                    pion_a_verifier = -1
                            if pion_a_verifier == player and len(L) != 0:
                                if (k, l) in coups_pos.keys():
                                    coups_pos[(k, l)] = coups_pos[(k, l)] + L
                                else:
                                    coups_pos[(k, l)] = L

                    if k != len(grid) - 1:
                        # Right-hand route
                        L = []
                        i = k
                        j = l
                        pion_a_verifier = grid[i + 1][j]
                        while pion_a_verifier not in [-1, 0, player] and i in range(
                            len(grid)
                        ):
                            L.append((i + 1, j))
                            i += 1
                            try:
                                pion_a_verifier = grid[i + 1][j]
                            except:
                                pion_a_verifier = -1
                        if pion_a_verifier == player and len(L) != 0:
                            if (k, l) in coups_pos.keys():
                                coups_pos[(k, l)] = coups_pos[(k, l)] + L
                            else:
                                coups_pos[(k, l)] = L

                        if l != 0:
                            # Bottom right-hand route
                            L = []
                            i = k
                            j = l
                            pion_a_verifier = grid[i + 1][j - 1]
                            while (
                                pion_a_verifier not in [-1, 0, player]
                                and i in range(len(grid))
                                and j in range(len(grid))
                            ):
                                L.append((i + 1, j - 1))
                                i += 1
                                j -= 1
                                try:
                                    assert j > 0
                                    pion_a_verifier = grid[i + 1][j - 1]
                                except:
                                    pion_a_verifier = -1
                            if pion_a_verifier == player and len(L) != 0:
                                if (k, l) in coups_pos.keys():
                                    coups_pos[(k, l)] = coups_pos[(k, l)] + L
                                else:
                                    coups_pos[(k, l)] = L

                    if l != 0:
                        # Left-hand route
                        L = []
                        i = k
                        j = l
                        pion_a_verifier = grid[i][j - 1]
                        while pion_a_verifier not in [-1, 0, player] and j in range(
                            len(grid)
                        ):
                            L.append((i, j - 1))
                            j -= 1
                            try:
                                assert j > 0
                                pion_a_verifier = grid[i][j - 1]
                            except:
                                pion_a_verifier = -1
                        if pion_a_verifier == player and len(L) != 0:
                            if (k, l) in coups_pos.keys():
                                coups_pos[(k, l)] = coups_pos[(k, l)] + L
                            else:
                                coups_pos[(k, l)] = L

                        if k != 0:
                            # Top left-hand route
                            L = []
                            i = k
                            j = l
                            pion_a_verifier = grid[i - 1][j - 1]
                            while (
                                pion_a_verifier not in [-1, 0, player]
                                and i in range(len(grid))
                                and j in range(len(grid))
                            ):
                                L.append((i - 1, j - 1))
                                i -= 1
                                j -= 1
                                try:
                                    assert i > 0 and j > 0
                                    pion_a_verifier = grid[i - 1][j - 1]
                                except:
                                    pion_a_verifier = -1
                            if pion_a_verifier == player and len(L) != 0:
                                if (k, l) in coups_pos.keys():
                                    coups_pos[(k, l)] = coups_pos[(k, l)] + L
                                else:
                                    coups_pos[(k, l)] = L

        return coups_pos
        # Does not use self.moves_possible so that minmax does not modify the game during his calculations

    # Undo the move
    def undo_move(self) -> None:
        """
        Undo a move. When playing against CPU, it "undoes" your move and the CPU's move
        """
        if self.nb_players != 1:  # With bot, the player stay the same
            for _ in range(self.nb_players - 1):  # Get the previous player
                self.player_turn = self.player_turn % self.nb_players + 1
        if self.past_grids != []:
            self.grid = self.past_grids.pop()  # Get the previous grid
            self.moves_possible = self.coups_possibles(
                self.grid, self.player_turn
            )  # Get the previous moves possible

    def jouer_coup(self, player: int, move: tuple) -> None:
        """
        Input : the player and the move chosen
        Update the grid after playing the move (put the piece + flip pieces following the rules)

        THIS CODE DOESN'T MODIFY THE PLAYER'S TURN
        """
        if move in self.moves_possible.keys():
            # For Blitz mode
            if (
                self.time_total > 0 and len(self.past_grids) != 1
            ):  # Start counting time after the first move
                self.timers[self.player_turn - 1] -= time.time() - self.start_time
                if self.time_total == 60:
                    self.timers[
                        self.player_turn - 1
                    ] += 1  # Add 1 second when the player play if the blitz is with 60 seconds
                self.timers[self.player_turn - 1] = min(
                    self.time_total, self.timers[self.player_turn - 1]
                )

            # Save the grid and apply move
            x, y = move
            self.grid[x][y] = player
            for pion in self.moves_possible[move]:
                k, l = pion
                self.grid[k][l] = player

            # Change player turn and moves possible
            self.player_turn = (
                self.player_turn % max(2, self.nb_players) + 1
            )  # Max needed with bot
            self.moves_possible = self.coups_possibles(self.grid, self.player_turn)
            for _ in range(3):
                if self.moves_possible == {}:
                    self.player_turn = self.player_turn % max(2, self.nb_players) + 1
                    self.moves_possible = self.coups_possibles(
                        self.grid, self.player_turn
                    )

            self.start_time = time.time()

    def is_grid_full(self, grid: List[List[int]]) -> bool:
        """
        Input : Game Grid
        Return True if no one can play, else False
        """
        player = 1
        while player <= max(2, self.nb_players):
            if self.coups_possibles(grid, player) == {}:
                player += 1
            else:
                return False
        return True

    def minmax(self, grid: List[List[int]], player: int, coup_avance: int):
        """
        Input : Game Grid, the CPU player and the depth
        Minmax algorithm : choose the best move minimizing CPU's gain with the utility function, and a variable depth
        """
        starting = True
        ending = False
        if (
            self.count_player_points(grid)[player - 1]
            + self.count_player_points(grid)[player % 2]
            > 20
        ):
            starting = False
        if (
            self.count_player_points(grid)[player - 1]
            + self.count_player_points(grid)[player % 2]
            > 55
        ):
            ending = True

        def utility(grid: List[List[int]], player: int) -> tuple:
            """
            Utility function of the Minmax Algorithm
            Returns the score quality of the move
            """
            # utilité is the difference of scores between the two players
            ut = (
                self.count_player_points(grid)[player - 1]
                - self.count_player_points(grid)[player % 2]
            )
            # enhancing the pieces on the side of the board
            for i in range(8):
                if grid[0][i] == player:
                    ut += 1
                elif grid[0][i] == 3 - player:
                    ut -= 1
                if grid[i][0] == player:
                    ut += 1
                elif grid[i][0] == 3 - player:
                    ut -= 1
                if grid[7][i] == player:
                    ut += 1
                elif grid[7][i] == 3 - player:
                    ut -= 1
                if grid[i][7] == player:
                    ut += 1
                elif grid[i][7] == 3 - player:
                    ut -= 1
            # eliminates the need for more pieces and avoid edges
            if starting:
                ut = 0
                for i in range(8):
                    if grid[0][i] == player:
                        ut -= 1
                    if grid[i][0] == player:
                        ut -= 1
            if player == 2:
                ut = (
                    ut
                    + (
                        grid[0][0] * (3 - 2 * player)
                        + grid[7][0] * (3 - 2 * player)
                        + grid[0][7] * (3 - 2 * player)
                        + grid[7][7] * (3 - 2 * player)
                    )
                    * 7
                )
            else:
                ut = (
                    ut
                    - (
                        grid[0][0] * (3 - 2 * player)
                        + grid[7][0] * (3 - 2 * player)
                        + grid[0][7] * (3 - 2 * player)
                        + grid[7][7] * (3 - 2 * player)
                    )
                    * 7
                )
            ut = ut * 3

            # value pack of pieces rather than scattered pieces
            for i in range(1, 7):
                for j in range(1, 7):
                    if grid[i][j] == player:
                        if grid[i - 1][j - 1] == player:
                            ut += 0.75
                        if grid[i + 1][j + 1] == player:
                            ut += 0.75
                        if grid[i][j - 1] == player:
                            ut += 0.75
                        if grid[i - 1][j] == player:
                            ut += 0.75
                        if grid[i + 1][j] == player:
                            ut += 0.75
                        if grid[i][j + 1] == player:
                            ut += 0.75
                        if grid[i - 1][j + 1] == player:
                            ut += 0.75
                        if grid[i + 1][j - 1] == player:
                            ut += 0.75
                    if grid[i][j] == 3 - player:
                        if grid[i - 1][j - 1] == 3 - player:
                            ut -= 0.75
                        if grid[i + 1][j + 1] == 3 - player:
                            ut -= 0.75
                        if grid[i][j - 1] == 3 - player:
                            ut -= 0.75
                        if grid[i - 1][j] == 3 - player:
                            ut -= 0.75
                        if grid[i + 1][j] == 3 - player:
                            ut -= 0.75
                        if grid[i][j + 1] == 3 - player:
                            ut -= 0.75
                        if grid[i - 1][j + 1] == 3 - player:
                            ut -= 0.75
                        if grid[i + 1][j - 1] == 3 - player:
                            ut -= 0.75
            # at the end the winner is the one with the most pieces
            if ending:
                ut = (
                    self.count_player_points(grid)[player - 1]
                    - self.count_player_points(grid)[player % 2]
                )
                ut = ut * 2
            return ut

        def play_move_CPU(
            grid, player: int, coup: tuple, moves_possible: dict
        ) -> List[List[int]]:
            """
            Update the grid with the CPU move
            """
            if coup in moves_possible.keys():
                x, y = coup
                grid[x][y] = player
                for pion in moves_possible[coup]:
                    k, l = pion
                    grid[k][l] = player
            return grid

        L = self.coups_possibles(grid, player)
        if (coup_avance == 0) or (self.is_grid_full(grid)):
            return (utility(grid, player), None)
        Uopt = -float("inf")
        copt = []
        # si le joueur ne peut pas jouer, faire rejouer le dernier joueur et ne pas changer le signe de l'utilité
        if len(L.keys()) == 0:
            U, c0 = self.minmax(grid, player % 2 + 1, coup_avance - 1)
            return (-U, c0)
        else:
            for coup in L.keys():
                grid2 = [[e for e in line] for line in grid]
                if str(grid2) in self.memo_minmax.keys() and ending:
                    U, c0 = self.memo_minmax[str(grid2)]
                else:
                    U, c0 = self.minmax(
                        play_move_CPU(grid2, player, coup, L),
                        player % 2 + 1,
                        coup_avance - 1,
                    )
                    if ending:
                        self.memo_minmax[str(grid2)] = (U, c0)
                x, y = coup
                # enhancing the value of the squares on the side of the board
                if x == 0 or x == 7:
                    U += 6
                if y == 0 or y == 7:
                    U += 6
                U = -U
                if Uopt == U:
                    copt.append(coup)
                    grid2 = play_move_CPU(grid2, player, coup, L)
                elif Uopt < U:
                    Uopt = U
                    copt = []
                    copt.append(coup)
            n = len(copt)
            if n == 1:
                return (Uopt, copt[0])
            else:
                nb = rd.randint(0, n - 1)
                c = copt[nb]
                return (Uopt, c)
