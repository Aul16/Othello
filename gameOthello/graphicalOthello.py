import tkinter as tk
from PIL import Image, ImageTk
import tkinter.font as font
import time
import random
from _thread import *
import os

#  Have to add a . in front of the module name for pytest
# Example:
# from .game import Game
from game import Game
from gridButton import GridButton
from network import Network


PATH = os.path.dirname(os.path.abspath(__file__))
PATH = PATH.replace("\\", "/")  # Handle windows case

GAME_BG = "#303030"
EMPTY = 0
BLACK = 1
WHITE = 2
BLUE = 3
PINK = 4
PLAYER_TURN_STR_LIST = [
    "Black's turn",
    "White's turn",
    "Blue's turn",
    "Pink's turn",
]  # List of shown string to let the player know whose turn it is
ONLINE = False
BLITZ = 0
ia_depth = {
    1: [1] * 64,
    2: [4] * 64,
    3: [5] * 50 + [6] * 10 + [8] * 5 + [9 - i for i in range(10)],
}


def showMenu(container) -> None:
    """
    Called from main code
    Function that shows the menu of the game
    Arguments:
        - container: tk.Frame object that will contain the menu
    Output: None
    """
    global niveau, ONLINE, BLITZ

    ONLINE = False
    BLITZ = 0

    # Create the frame that will contain all the menu
    f = font.Font(family="Times New Roman", size=35, weight="bold")
    frame = tk.Frame(container, bg=GAME_BG)
    frame.grid(row=0, column=0, sticky="nsew")

    # Title of the game
    label = tk.Label(frame, text="Othello", bg=GAME_BG, fg="#228B22", font=f)
    label.pack()

    ###############################################################################
    # Frame that will containt options for solo play
    solo_play_frame = tk.Frame(frame, bg=GAME_BG)
    solo_play_frame.pack(expand=True, fill=tk.X)
    solo_play_frame.columnconfigure(0, weight=1)
    solo_play_frame.columnconfigure(1, weight=1)
    solo_play_frame.columnconfigure(2, weight=1)
    solo_play_frame.columnconfigure(3, weight=1)

    # start the game with 1 player and a bot
    button = tk.Button(
        solo_play_frame,
        text="Start Game Solo",
        command=lambda: (frame.destroy(), startGame(container, color_choice.get(), 1)),
        bg="#228B22",
    )  # When clicked, destroy the menu and start the game
    button.grid(row=0, column=0, sticky="nsew", pady=5, padx=5)

    # Choice for the color
    color_choice = tk.IntVar(value=1)
    case1 = tk.Radiobutton(
        solo_play_frame,
        variable=color_choice,
        value=1,
        fg="#228B22",
        bg=GAME_BG,
        border=0,
        highlightbackground=GAME_BG,
        highlightthickness=0,
        activebackground=GAME_BG,
    )
    case2 = tk.Radiobutton(
        solo_play_frame,
        variable=color_choice,
        value=2,
        fg="#228B22",
        bg=GAME_BG,
        border=0,
        highlightbackground=GAME_BG,
        highlightthickness=0,
        activebackground=GAME_BG,
    )
    case1.config(text="Noir")
    case2.config(text="Blanc")
    case1.grid(row=0, column=1)
    case2.grid(row=0, column=2)

    # choice for the bot level
    niveau = tk.IntVar(value=1)
    level_label = tk.Label(
        solo_play_frame,
        text="Level of the AI",
        bg=GAME_BG,
        fg="#228B22",
        font=font.Font(family="Times New Roman", size=15, weight="bold"),
    )
    level_label.grid(row=1, column=0)
    niveau1 = tk.Radiobutton(
        solo_play_frame,
        variable=niveau,
        value=1,
        fg="#228B22",
        bg=GAME_BG,
        border=0,
        highlightbackground=GAME_BG,
        highlightthickness=0,
        activebackground=GAME_BG,
    )
    niveau2 = tk.Radiobutton(
        solo_play_frame,
        variable=niveau,
        value=2,
        fg="#228B22",
        bg=GAME_BG,
        border=0,
        highlightbackground=GAME_BG,
        highlightthickness=0,
        activebackground=GAME_BG,
    )
    niveau3 = tk.Radiobutton(
        solo_play_frame,
        variable=niveau,
        value=3,
        fg="#228B22",
        bg=GAME_BG,
        border=0,
        highlightbackground=GAME_BG,
        highlightthickness=0,
        activebackground=GAME_BG,
    )
    niveau1.config(text="Easy")
    niveau2.config(text="Medium")
    niveau3.config(text="Hard")
    niveau1.grid(row=1, column=1)
    niveau2.grid(row=1, column=2)
    niveau3.grid(row=1, column=3)
    ########################################################################

    ######################################################################################
    # Blitz mode menu
    ######################################################################################

    blitz_label = tk.Label(
        frame,
        text="Blitz (for duo only)",
        bg=GAME_BG,
        fg="#228B22",
        font=font.Font(family="Times New Roman", size=20, weight="bold"),
    )
    blitz_label.pack(expand=True, fill=tk.BOTH, pady=5, padx=5)

    blitz_choice_frame = tk.Frame(frame, bg=GAME_BG)
    blitz_choice_frame.pack(expand=True, fill=tk.X)
    blitz_choice_frame.columnconfigure(0, weight=1)
    blitz_choice_frame.columnconfigure(1, weight=1)
    blitz_choice_frame.columnconfigure(2, weight=1)
    blitz_choice_frame.columnconfigure(3, weight=1)

    blitz_choice = tk.IntVar(value=0)
    case1 = tk.Radiobutton(
        blitz_choice_frame,
        variable=blitz_choice,
        value=0,
        fg="#228B22",
        bg=GAME_BG,
        border=0,
        highlightbackground=GAME_BG,
        highlightthickness=0,
        activebackground=GAME_BG,
    )
    case2 = tk.Radiobutton(
        blitz_choice_frame,
        variable=blitz_choice,
        value=60,
        fg="#228B22",
        bg=GAME_BG,
        border=0,
        highlightbackground=GAME_BG,
        highlightthickness=0,
        activebackground=GAME_BG,
    )
    case3 = tk.Radiobutton(
        blitz_choice_frame,
        variable=blitz_choice,
        value=180,
        fg="#228B22",
        bg=GAME_BG,
        border=0,
        highlightbackground=GAME_BG,
        highlightthickness=0,
        activebackground=GAME_BG,
    )
    case4 = tk.Radiobutton(
        blitz_choice_frame,
        variable=blitz_choice,
        value=300,
        fg="#228B22",
        bg=GAME_BG,
        border=0,
        highlightbackground=GAME_BG,
        highlightthickness=0,
        activebackground=GAME_BG,
    )

    case1.config(text="No")
    case2.config(text="1min")
    case3.config(text="3min")
    case4.config(text="5min")
    case1.grid(row=0, column=0)
    case2.grid(row=0, column=1)
    case3.grid(row=0, column=2)
    case4.grid(row=0, column=3)
    ########################################################################

    # Start the game with 2 players
    button2 = tk.Button(
        frame,
        text="Start Game Duo",
        command=lambda: (
            frame.destroy(),
            startGame(container, BLACK, 2, Blitz=blitz_choice.get()),
        ),
        bg="#228B22",
    )  # When clicked, destroy the menu and start the game
    button2.pack(expand=True, fill=tk.X, pady=5, padx=5)

    # Start the game with 3 players
    button3 = tk.Button(
        frame,
        text="Start Game Trio",
        command=lambda: (frame.destroy(), startGame(container, BLACK, 3)),
        bg="#228B22",
    )  # When clicked, destroy the menu and start the game
    button3.pack(expand=True, fill=tk.BOTH, pady=5, padx=5)

    # Start the game with 4 players
    button4 = tk.Button(
        frame,
        text="Start Game Quadrio",
        command=lambda: (frame.destroy(), startGame(container, BLACK, 4)),
        bg="#228B22",
    )  # When clicked, destroy the menu and start the game
    button4.pack(expand=True, fill=tk.BOTH, pady=5, padx=5)

    ######################################################################################
    # start the game online
    online_frame = tk.Frame(frame, bg=GAME_BG)
    online_frame.pack(expand=True, fill=tk.X)
    online_frame.rowconfigure(0, weight=1)
    online_frame.rowconfigure(1, weight=1)
    online_frame.columnconfigure(0, weight=1)
    online_frame.columnconfigure(1, weight=1)

    online_label = tk.Label(
        online_frame,
        text="Online",
        bg=GAME_BG,
        fg="#228B22",
        font=font.Font(family="Times New Roman", size=20, weight="bold"),
    )
    online_label.grid(row=0, column=0, sticky="nsew", pady=5, padx=5)

    game_id_val = tk.StringVar(
        value="".join([str(random.randint(0, 9)) for i in range(6)])
    )
    online_id_entry = tk.Entry(
        online_frame,
        textvariable=game_id_val,
        bg="#228B22",
        fg="#FFFFFF",
        border=0,
        highlightbackground=GAME_BG,
        highlightthickness=0,
    )
    online_id_entry.grid(row=1, column=0, sticky="nsew", pady=5, padx=5)

    connect_button = tk.Button(
        online_frame,
        text="Join Game",
        command=lambda: (
            frame.destroy(),
            startGame(container, BLACK, 2, True, game_id_val.get()),
        ),
        bg="#228B22",
    )  # When clicked, destroy the menu and start the game
    connect_button.grid(row=1, column=1, sticky="nsew", pady=5, padx=5)
    ######################################################################################

    # button to quit
    button5 = tk.Button(frame, text="Quitter", command=lambda: exit(), bg="#228B22")
    button5.pack(expand=True, fill=tk.BOTH, pady=5, padx=5)


def showGrid(container, color_choosed: int, whose_player: int) -> None:
    """
    Called by: StartGame(container, color_choosed)
    Function that shows the game grid
    Arguments:
        - container: tk.Frame object that will contain the menu
    Output: None
    """
    global game, game_frame, ONLINE, graph_grid, BLITZ
    global black_piece, white_piece, blue_piece, pink_piece, pixel, red_dot
    global black_piece_raw, white_piece_raw, blue_piece_raw, pink_piece_raw, red_dot_raw
    global player_turn_var, black_scores, white_scores, blue_scores, pink_scores, chrono_label_var

    # Load the images
    ###########################################################################################
    # Initialize images
    ###########################################################################################
    pixel = tk.PhotoImage(width=1, height=1)

    # Possible move image
    red_dot_raw = Image.open(
        rf"{PATH}/data/red_dot.png"
    )  # Keep the raw image to be able to resize it
    resize_img = red_dot_raw.resize((10, 10))  # Resize the image to fit the button
    red_dot = ImageTk.PhotoImage(resize_img)  # Image shown in buttons

    # White piece image
    white_piece_raw = Image.open(
        rf"{PATH}/data/white_piece.png"
    )  # Keep the raw image to be able to resize it
    resize_img = white_piece_raw.resize((50, 50))  # Resize the image to fit the button
    white_piece = ImageTk.PhotoImage(resize_img)  # Image shown in buttons

    # Black piece image
    black_piece_raw = Image.open(
        rf"{PATH}/data/black_piece.png"
    )  # Keep the raw image to be able to resize it
    resize_img = black_piece_raw.resize((50, 50))  # Resize the image to fit the button
    black_piece = ImageTk.PhotoImage(resize_img)  # Image shown in buttons

    # Blue piece image
    blue_piece_raw = Image.open(
        rf"{PATH}/data/blue_piece.png"
    )  # Keep the raw image to be able to resize it
    resize_img = blue_piece_raw.resize((50, 50))  # Resize the image to fit the button
    blue_piece = ImageTk.PhotoImage(resize_img)  # Image shown in buttons

    # Pink piece image
    pink_piece_raw = Image.open(
        rf"{PATH}/data/pink_piece.png"
    )  # Keep the raw image to be able to resize it
    resize_img = pink_piece_raw.resize((50, 50))  # Resize the image to fit the button
    pink_piece = ImageTk.PhotoImage(resize_img)  # Image shown in buttons

    #################################################################################################

    #################################################################################################
    # Frame containing the grid and the scores
    #################################################################################################
    game_frame = tk.Frame(container, bg=GAME_BG)
    game_frame.grid(row=0, column=0, sticky="nsew")

    ##################################################################################################
    # Frame containing the scores and other information / buttons
    info_frame = tk.Frame(game_frame, bg=GAME_BG)
    info_frame.pack(
        fill="x", side="top"
    )  # Want the frame to take all the space available
    info_frame.grid_rowconfigure(0, weight=1)
    info_frame.grid_columnconfigure(0, weight=1)
    info_frame.grid_columnconfigure(1, weight=1)
    info_frame.grid_columnconfigure(2, weight=1)
    info_frame.grid_columnconfigure(3, weight=1)
    info_frame.grid_columnconfigure(4, weight=1)
    info_frame.grid_rowconfigure(1, weight=1)

    # Show the score of the white player
    white_scores = tk.StringVar(
        info_frame,
        value="White : " + str(game.count_player_points(game.grid)[WHITE - 1]),
    )  # global StringVar to be able to change the value of the label
    white_scores_label = tk.Label(
        info_frame, textvariable=white_scores, bg=GAME_BG, fg="#FFFFFF"
    )  # Label that will show the score
    white_scores_label.grid(row=0, column=0)

    # Show the score of the black player
    black_scores = tk.StringVar(
        info_frame,
        value="Black : " + str(game.count_player_points(game.grid)[BLACK - 1]),
    )  # global StringVar to be able to change the value of the label
    black_scores_label = tk.Label(
        info_frame, textvariable=black_scores, bg=GAME_BG, fg="#FFFFFF"
    )  # Label that will show the score
    black_scores_label.grid(row=1, column=0)

    # Show the score of the blue player
    if game.nb_players >= 3:
        blue_scores = tk.StringVar(
            info_frame,
            value="Blue : " + str(game.count_player_points(game.grid)[BLUE - 1]),
        )  # global StringVar to be able to change the value of the label
        blue_scores_label = tk.Label(
            info_frame, textvariable=blue_scores, bg=GAME_BG, fg="#FFFFFF"
        )  # Label that will show the score
        blue_scores_label.grid(row=0, column=1)

    # Show the score of the pink player
    if game.nb_players == 4:
        pink_scores = tk.StringVar(
            info_frame,
            value="Pink : " + str(game.count_player_points(game.grid)[PINK - 1]),
        )  # global StringVar to be able to change the value of the label
        pink_scores_label = tk.Label(
            info_frame, textvariable=pink_scores, bg=GAME_BG, fg="#FFFFFF"
        )  # Label that will show the score
        pink_scores_label.grid(row=1, column=1)

    # Show whose turn it is
    player_turn = (
        BLACK  # Global variable to know whose turn it is : Default first one is BLACK
    )
    player_turn_var = tk.StringVar(
        info_frame, value=PLAYER_TURN_STR_LIST[player_turn - 1]
    )  # global StringVar to be able to change the value of the label
    player_turn_label = tk.Label(
        info_frame, textvariable=player_turn_var, bg=GAME_BG, fg="#FFFFFF"
    )  # Label that will show whose turn it is
    player_turn_label.grid(row=0, column=2)

    # Show chrono if no AI
    if BLITZ > 0:
        chrono_label_var = tk.StringVar(info_frame, value=f"Chrono : {BLITZ}")
        chrono_label = tk.Label(
            info_frame, textvariable=chrono_label_var, bg=GAME_BG, fg="#FFFFFF"
        )
        chrono_label.grid(row=0, column=3)

    # Undo button
    if not ONLINE and BLITZ == 0:
        undo_button = tk.Button(
            info_frame,
            text="Undo",
            command=lambda: (game.undo_move(), update_grid_gui()),
            bg="#228B22",
        )
        undo_button.grid(row=0, column=4)

    # Quit button
    quit_button = tk.Button(
        info_frame,
        text="Quit",
        command=lambda: (game_frame.destroy(), showMenu(container)),
        bg="#228B22",
    )
    quit_button.grid(row=1, column=4)

    # Show whose player it is
    if ONLINE:
        if int(whose_player) == 1:
            string_val = "You're the Black pieces"
        else:
            string_val = "You're the White pieces"
        player_number_label = tk.Label(
            info_frame, text=string_val, bg=GAME_BG, fg="#FFFFFF"
        )
        player_number_label.grid(row=1, column=2)
    ###############################################################################################################

    ###############################################################################################################
    # Handle if the player is playing alone -> Play for the bot
    if (
        game.nb_players == 1 and color_choosed == WHITE and not ONLINE
    ):  # If the player is playing alone and chose white, play for the bot first
        game.jouer_coup(
            BLACK, random.choice(list(game.moves_possible.keys()))
        )  # Play for the bot
        player_turn_var.set(
            PLAYER_TURN_STR_LIST[:2][game.player_turn - 1]
        )  # Update the label

        # Update the scores
        scores = game.count_player_points(
            game.grid
        )  # Get the scores according to the number of players
        black_scores.set("Black : " + str(scores[BLACK - 1]))
        white_scores.set("White : " + str(scores[WHITE - 1]))
    #################################################################################################################

    #################################################################################################################
    # Frame containing the grid
    grid_frame = tk.Frame(game_frame, bg=GAME_BG)
    grid_frame.pack(expand=True, fill="both")

    # Create the grid (list containing all the buttons)
    graph_grid = []
    for row in range(len(game.grid)):
        line = []
        grid_frame.rowconfigure(row, weight=1, minsize=25)
        grid_frame.columnconfigure(row, weight=1, minsize=25)
        for col in range(len(game.grid)):  #  Iterate on all the grid
            # Create the button
            line.append(
                GridButton(master=grid_frame, coordinates=(row, col), image=pixel)
            )
            line[col].grid(row=row, column=col, padx=1, pady=1, sticky="nsew")
        graph_grid.append(line)
    graph_grid[0][0].bind(
        "<Configure>", resize_image
    )  # Resize the images when the window is resized : one button is enough
    #################################################################################################################

    # Show the grid
    update_grid_gui()


def play(event) -> None:
    """
    Called by: buttons from showGrid() when clicked
    Function that is called when a player plays
    Arguments:
        - event: tk.Event object that contains the information about the event
    Output: None
    """
    global game, player_turn_var, black_scores, white_scores, blue_scores, pink_scores
    global game_frame, ONLINE, BLITZ, connection, niveau

    clicked_button = event.widget

    coordonnees = (
        clicked_button.coordinates
    )  # Get coordinates of the button that was clicked

    if ONLINE:
        game = connection.send(f"{coordonnees[0]},{coordonnees[1]}")
        update_grid_gui()

    # Play only if the move is possible
    if coordonnees in game.moves_possible.keys() and not ONLINE:
        # Update the grid
        player = (
            game.player_turn
        )  # Keep the player number to skip the bot turn if it cannot play
        game.past_grids.append([[e for e in line] for line in game.grid])
        game.jouer_coup(
            game.player_turn, clicked_button.coordinates
        )  # Update the grid                                                    # Change the player turn
        player_turn_var.set(
            PLAYER_TURN_STR_LIST[game.player_turn - 1]
        )  # Update the label

        # Update the scores
        scores = game.count_player_points(
            game.grid
        )  # Get the scores according to the number of players
        black_scores.set("Black : " + str(scores[BLACK - 1]))
        white_scores.set("White : " + str(scores[WHITE - 1]))
        try:
            blue_scores.set(
                "Blue : " + str(scores[BLUE - 1])
            )  # Will show the 3rd player score if is present
            pink_scores.set(
                "Pink : " + str(scores[PINK - 1])
            )  # Will show the 3rd player score if is present
        except (
            IndexError,
            NameError,
        ):  # If there are less than 4 players, the scores of the other players are not shown
            pass

        if BLITZ > 0:  # Variable Blitz
            start_new_thread(threaded_chrono, (game,))

        update_grid_gui()  # Update the grid

        # If solo mode, play for the bot
        if (
            game.nb_players == 1
            and not game.is_grid_full(game.grid)
            and player != game.player_turn
        ):
            time.sleep(
                0.5
            )  # Wait half a second to let the player see the move of the bot
            game.jouer_coup(
                game.player_turn,
                game.minmax(
                    game.grid, game.player_turn, ia_depth[niveau.get()][sum(scores)]
                )[1],
            )
            player_turn_var.set(PLAYER_TURN_STR_LIST[game.player_turn - 1])

            # Update the scores
            scores = game.count_player_points(
                game.grid
            )  # Get the scores according to the number of players
            black_scores.set("Black : " + str(scores[BLACK - 1]))
            white_scores.set("White : " + str(scores[WHITE - 1]))

            update_grid_gui()  # Update the grid

    ####################################################################################
    # Check if the grid is full -> End game
    ####################################################################################
    if game.is_grid_full(game.grid):
        end_game()
    ####################################################################################################


def end_game() -> None:
    global game_frame, game, container

    dic = {
        1: "BLACK",
        2: "WHITE",
        3: "BLUE",
        4: "PINK",
    }  # For a better message with player color

    game_frame.destroy()
    end_frame = tk.Frame(container, bg=GAME_BG)
    end_frame.grid(row=0, column=0, sticky="nsew")
    if len(game.who_won()) == 1:  # One winner
        winner_text = f"Player {dic[game.who_won()[0]]} won"
    else:  # Several winners
        winner_text = f"Players {dic[game.who_won()[0]]}"
        for k in range(1, len(game.who_won())):
            winner_text = winner_text + f" and {dic[game.who_won()[k]]}"
        winner_text = winner_text + f" won"

    end_label = tk.Label(
        end_frame,
        text=winner_text,
        bg=GAME_BG,
        fg="#228B22",
        font=font.Font(family="Times New Roman", size=35, weight="bold"),
    )
    end_label.pack()

    score_title_label = tk.Label(
        end_frame,
        text="Score : ",
        bg=GAME_BG,
        fg="#228B22",
        font=font.Font(family="Times New Roman", size=20, weight="bold"),
    )
    score_title_label.pack(expand=True, fill=tk.X)

    scores = game.scores
    # Display scores for players who have only played
    score_end = f"Black: {scores[BLACK-1]} - White: {scores[WHITE-1]}"
    try:
        score_end = (
            score_end + f" - Blue: {scores[BLUE-1]}"
        )  # Will show the 3rd player score if is present
        score_end = (
            score_end + f" - Pink: {scores[PINK-1]}"
        )  # Will show the 3rd player score if is present
    except (
        IndexError,
        NameError,
    ):  # If there are less than 4 players, the scores of the other players are not shown
        pass

    score_label = tk.Label(
        end_frame,
        text=score_end,
        bg=GAME_BG,
        fg="#228B22",
        font=font.Font(family="Times New Roman", size=15, weight="bold"),
    )
    score_label.pack(expand=True, fill=tk.X)

    button = tk.Button(
        end_frame,
        text="Menu",
        command=lambda: (end_frame.destroy(), showMenu(container)),
        bg="#228B22",
    )
    button.pack(expand=True, fill=tk.BOTH, pady=30, padx=50)

    button2 = tk.Button(
        end_frame, text="Quitter", command=lambda: (exit()), bg="#228B22"
    )
    button2.pack(expand=True, fill=tk.BOTH, pady=30, padx=50)


def resize_image(event) -> None:
    """
    Called by : button at (0,0) when resized
    Function that is called when the window is resized. Resize the images to fit the new button size
    Arguments:
        - event: tk.Event object that contains the information about the event
    Output: None
    """
    global black_piece_raw, white_piece_raw, blue_piece_raw, pink_piece_raw, white_piece, black_piece, blue_piece, pink_piece
    global red_dot, red_dot_raw

    new_width = event.width  # Get the new width and height of the button
    new_height = event.height  ######

    size_img = min(
        new_width, new_height
    )  # Get the new size of the image to keep the right ratio

    ################################
    # Resize the images
    ################################
    black_piece = ImageTk.PhotoImage(black_piece_raw.resize((size_img, size_img)))
    white_piece = ImageTk.PhotoImage(white_piece_raw.resize((size_img, size_img)))
    blue_piece = ImageTk.PhotoImage(blue_piece_raw.resize((size_img, size_img)))
    pink_piece = ImageTk.PhotoImage(pink_piece_raw.resize((size_img, size_img)))
    red_dot = ImageTk.PhotoImage(red_dot_raw.resize((size_img // 5, size_img // 5)))

    update_grid_gui()  # Update the grid


# If Online, we have to update the grid every time the other player plays and the server sends the new grid
# Other thread to let the game continue
# The loop is stopped at every send message to wait for the server response
def threaded_update(connection) -> None:
    global game, ONLINE
    while True:
        if ONLINE:
            try:
                game = connection.send("get")
                if game.is_grid_full(game.grid):
                    ONLINE = False
                    end_game()
                else:
                    update_grid_gui()
            except:  # If the server is not responding, try again
                pass
        else:  # Stop the loop if the player returned to the menu
            break


def threaded_chrono(game) -> None:
    global chrono_label_var, BLITZ
    player = game.player_turn
    chrono = game.timers[game.player_turn - 1]
    start_time = time.time()
    while (
        player == game.player_turn and BLITZ > 0
    ):  # Second condition for when quit the game: break the thread
        timer = chrono - (time.time() - start_time)
        chrono_label_var.set(f"Chrono : {round(timer, 1)}")
        if chrono - (time.time() - start_time) < 0:
            game.timers[game.player_turn - 1] = timer
            end_game()
            break
        time.sleep(0.05)


def update_grid_gui():
    """
    Called by : play(event), resize_image(event), showGrid(container, color_choosed, player_count)
    Function that updates the grid when a player plays
    Arguments:
        - coordinates: tuple containing the coordinates of the button that was clicked
    Output: None
    """
    global graph_grid, black_piece, white_piece, blue_piece, pink_piece, pixel, red_dot
    global root, ONLINE, connection, game

    # If online, the game object is updated by the server
    if ONLINE:
        game = connection.send("get")

        # Update the scores
        scores = game.count_player_points(game.grid)
        black_scores.set("Black : " + str(scores[BLACK - 1]))
        white_scores.set("White : " + str(scores[WHITE - 1]))

        player_turn_var.set(PLAYER_TURN_STR_LIST[game.player_turn - 1])

    # Update the grid according to the game object
    for row in range(len(game.grid)):
        for col in range(len(game.grid)):  # Iterate on all the grid
            # Update the command of the button
            graph_grid[row][col].deactivate()

            # Update the image of the button
            if game.grid[row][col] == BLACK:
                btn_img = black_piece

            elif game.grid[row][col] == WHITE:
                btn_img = white_piece

            elif game.grid[row][col] == BLUE:
                btn_img = blue_piece

            elif game.grid[row][col] == PINK:
                btn_img = pink_piece

            # Update the command of the button if authorized move for next player (already changed by the function play)
            elif (row, col) in game.moves_possible.keys():
                btn_img = red_dot
                graph_grid[row][col].activate(play)

            else:  # Empty case -> No image
                btn_img = pixel

            # Update the button image (I don't knoy why but it doesn't work without using 2 lines)
            graph_grid[row][col].configure(image=btn_img)
            graph_grid[row][col].image = btn_img

    root.update()  # Update the GUI


def startGame(
    container, color_choosed=1, player_count=2, Online=False, gameId=None, Blitz=0
) -> None:
    """
    Called by: buttons from showMenu()
    Begin the game and start the GUI
    Arguments:
        - container: tk.Frame object that will contain the menu
    Output: None
    """
    global ONLINE, BLITZ, connection, game

    ONLINE = Online  # Handle if the game is online
    BLITZ = Blitz

    player_number = None

    # Connect to the server if online and start the update thread
    if ONLINE:
        connection = Network()
        player_number = connection.connect(
            gameId
        )  # Connect to the server and get the player number (black or white)
        game = connection.send("get")
        start_new_thread(threaded_update, (connection,))
    else:
        game = Game(player_count, total_time=BLITZ)  # Create the game object

    showGrid(container, color_choosed, player_number)  # Show the grid


def game_window() -> None:
    """
    Settings for the main window
    """
    global container, root
    root = tk.Tk()
    root.geometry("500x500")
    root.title("Othello")

    container = tk.Frame(root)

    container.pack(side="top", fill="both", expand=True)

    container.grid_rowconfigure(0, weight=1)
    container.grid_columnconfigure(0, weight=1)

    showMenu(container)

    root.mainloop()
