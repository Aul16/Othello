import tkinter as tk
import unittest
from unittest.mock import patch
from gameOthello.graphicalOthello import *

class TestShowMenu(unittest.TestCase):
    def setUp(self):
        self.container = tk.Frame()
        self.container.grid(row=0, column=0)


    def tearDown(self):
        self.container.destroy()


    @patch('gameOthello.graphicalOthello.startGame')
    def test_start_game_solo(self, mock_start_game):
        # Simulate clicking the "Start Game Solo" button
        showMenu(self.container)
        solo_play_frame = self.container.winfo_children()[0].winfo_children()[1]
        start_game_button = solo_play_frame.winfo_children()[0]
        start_game_button.invoke()

        # Check that the startGame function is called with the correct arguments
        mock_start_game.assert_called_once_with(self.container, 1, 1)


    @patch('gameOthello.graphicalOthello.startGame')
    def test_start_game_duo_no_blitz(self, mock_start_game):
        # Simulate clicking the "Start Game Duo" button
        showMenu(self.container)
        start_game_button = self.container.winfo_children()[0].winfo_children()[4]
        start_game_button.invoke()

        # Check that the startGame function is called with the correct arguments
        mock_start_game.assert_called_once_with(self.container, 1, 2, Blitz=0)


    @patch('gameOthello.graphicalOthello.startGame')
    def test_start_game_trio(self, mock_start_game):
        # Simulate clicking the "Start Game Trio" button
        showMenu(self.container)
        start_game_button = self.container.winfo_children()[0].winfo_children()[5]
        start_game_button.invoke()

        # Check that the startGame function is called with the correct arguments
        mock_start_game.assert_called_once_with(self.container, 1, 3)

    @patch('gameOthello.graphicalOthello.startGame')
    def test_start_game_quadrio(self, mock_start_game):
        # Simulate clicking the "Start Game Quadrio" button
        showMenu(self.container)
        start_game_button = self.container.winfo_children()[0].winfo_children()[6]
        start_game_button.invoke()

        # Check that the startGame function is called with the correct arguments
        mock_start_game.assert_called_once_with(self.container, 1, 4)

    @patch('gameOthello.graphicalOthello.startGame')
    def test_join_game(self, mock_start_game):
        # Simulate clicking the "Join Game" button
        showMenu(self.container)
        online_frame = self.container.winfo_children()[0].winfo_children()[7]
        game_id_entry = online_frame.winfo_children()[1]
        gameID = game_id_entry.getvar(game_id_entry.cget("textvariable"))
        join_game_button = online_frame.winfo_children()[2]
        join_game_button.invoke()

        # Check that the startGame function is called with the correct arguments
        mock_start_game.assert_called_once_with(self.container, 1, 2, True, gameID)


class TestStartGame(unittest.TestCase):
    def setUp(self):
        self.container = tk.Frame()

    def tearDown(self):
        self.container.destroy()

    @patch('gameOthello.graphicalOthello.showGrid')
    @patch('gameOthello.graphicalOthello.Game')
    def test_start_game_offline(self, mock_Game, mock_showGrid):
        # Call the startGame function with offline mode
        startGame(self.container, color_choosed=1, player_count=2, Online=False, gameId=None)

        # Check that the Game object is created with the correct player count
        mock_Game.assert_called_once_with(2, total_time=0)

        # Check that the showGrid function is called with the correct arguments
        mock_showGrid.assert_called_once_with(self.container, 1, None)

    @patch('gameOthello.graphicalOthello.showGrid')
    @patch('gameOthello.graphicalOthello.Network')
    def test_start_game_online(self, mock_Network, mock_showGrid):
        # Mock the Network class and its methods
        mock_connection = mock_Network.return_value
        mock_connection.connect.return_value = 1
        mock_connection.send.return_value = "game_state"

        # Call the startGame function with online mode
        startGame(self.container, color_choosed=1, player_count=2, Online=True, gameId="123")

        # Check that the Network class is instantiated
        mock_Network.assert_called_once()

        # Check that the connect method is called with the correct game ID
        mock_connection.connect.assert_called_once_with("123")

        # Check that the send method is called with "get"
        mock_connection.send.assert_called_once_with("get")

        # Check that the showGrid function is called with the correct arguments
        mock_showGrid.assert_called_once_with(self.container, 1, 1)
