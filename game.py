from random import randint, choice

from src.board import ComputerBoard, PlayerBoard, ShipDirection


class EasyStrategy:
    def __init__(self, computer_board: ComputerBoard, player_board: PlayerBoard):
        self.__computer_board = computer_board
        self.__player_board = player_board
        self.__fired_positions = set()
        self.place_ships()

    def place_ships(self):
        """
        Place the ships on the board
        :return:
        """
        ships_to_place = 2
        while ships_to_place > 0:
            x = randint(0, 5)
            y = randint(0, 5)
            direction = choice(list(ShipDirection))
            try:
                self.__computer_board.place_ship(x, y, direction)
                ships_to_place -= 1
            except ValueError:
                pass

    def fire(self):
        """
        Fire at a random position
        :return:
        """
        while True:
            row = randint(0, 5)
            column = randint(0, 5)
            if (row, column) not in self.__fired_positions:
                self.__fired_positions.add((row, column))
                self.__player_board.fire(row, column)
                return row, column

class HardStrategy:
    def __init__(self, computer_board: ComputerBoard, player_board: PlayerBoard):
        self.__computer_board = computer_board
        self.__player_board = player_board
        self.__fired_positions = set()
        self.__hit_positions = []
        self.place_ships()

    def place_ships(self):
        """
        Place the ships on the board
        :return:
        """
        ships_to_place = 2
        while ships_to_place > 0:
            x = randint(0, 5)
            y = randint(0, 5)
            direction = choice(list(ShipDirection))
            try:
                self.__computer_board.place_ship(x, y, direction)
                ships_to_place -= 1
            except ValueError:
                pass

    def fire(self):
        """
        Fire at a position
        :return:
        """
        if self.__hit_positions:
            row, column = self.__hit_positions.pop(0)
        else:
            while True:
                row = randint(0, 5)
                column = randint(0, 5)
                if (row, column) not in self.__fired_positions:
                    break
        self.__fired_positions.add((row, column))
        self.__player_board.fire(row, column)
        if self.__player_board._data[row][column] < 0:
            self.__hit_positions.extend(self.__get_adjacent_positions(row, column))
        return row, column

    def __get_adjacent_positions(self, row, column):
        """
        Get the adjacent positions to a hit position
        :param row:
        :param column:
        :return:
        """
        positions = []
        if row > 0 and (row - 1, column) not in self.__fired_positions:
            positions.append((row - 1, column))
        if row < 5 and (row + 1, column) not in self.__fired_positions:
            positions.append((row + 1, column))
        if column > 0 and (row, column - 1) not in self.__fired_positions:
            positions.append((row, column - 1))
        if column < 5 and (row, column + 1) not in self.__fired_positions:
            positions.append((row, column + 1))
        return positions


class Battleships:
    def __init__(self, difficulty='easy'):
        self.__computer_board = ComputerBoard()
        self.__player_board = PlayerBoard()
        self.__strategy = self.__select_strategy(difficulty)
        self.__player_fired_positions = set()

    def __select_strategy(self, difficulty):
        """
        Select the strategy based on the difficulty level
        :param difficulty:
        :return:
        """
        if difficulty == 'easy':
            return EasyStrategy(self.__computer_board, self.__player_board)
        elif difficulty == 'hard':
            return HardStrategy(self.__computer_board, self.__player_board)
        else:
            raise ValueError("Invalid difficulty level")

    @property
    def computer_board(self):
        """
        Get the computer board
        :return:
        """
        return self.__computer_board

    @property
    def player_board(self):
        """
        Get the player board
        :return:
        """
        return self.__player_board

    def fire_human_player(self, row: int, column: int):
        """
        Fire at a position on the computer's board
        :param row:
        :param column:
        :return:
        """
        if (row, column) in self.__player_fired_positions:
            raise ValueError("Position already fired at")
        self.__player_fired_positions.add((row, column))
        self.__computer_board.fire(row, column)

    def fire_computer_player(self):
        """
        Fire at a position on the player's board
        :return:
        """
        return self.__strategy.fire()
