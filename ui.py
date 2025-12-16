from src.board import ShipDirection, ShipWasSunkException, GameOverException
from src.game import Battleships


class UI:
    __directions = {'LEFT': ShipDirection.LEFT, 'UP': ShipDirection.UP, 'RIGHT': ShipDirection.RIGHT, 'DOWN': ShipDirection.DOWN}

    def __init__(self):
        try:
            difficulty = input("Select difficulty (easy, hard): ").strip().lower()
            self.__game = Battleships(difficulty)
        except ValueError:
            print("Invalid difficulty")

    def __place_player_ships(self):
        ships_to_place = 2
        while ships_to_place > 0:
            ship_location = input("where to place ship (e.g., C3 left) >").upper().strip()
            tokens = ship_location.split(' ')
            try:
                column = ord(tokens[0][0]) - ord('A')
                row = int(tokens[0][1]) - 1
                direction = UI.__directions[tokens[1]]
                self.__game.player_board.place_ship(row, column, direction)
                ships_to_place -= 1
            except Exception as e:
                print("Problem with placing ships - " + str(e))

    def start(self):
        self.__place_player_ships()
        while True:
            print("My board")
            print(self.__game.player_board)
            print("Targeting board")
            print(self.__game.computer_board)
            try:
                fire_coordinates = input("fire>").strip()
                column = ord(fire_coordinates[0].upper()) - ord('A')
                row = int(fire_coordinates[1]) - 1
                try:
                    self.__game.fire_human_player(row, column)
                    computer_row, computer_column = self.__game.fire_computer_player()
                    print(f"Computer fired at {chr(computer_column + ord('A'))}{computer_row + 1}")
                except ValueError as e:
                    print(e)
                except ShipWasSunkException:
                    print("A ship was sunk!")
                    computer_row, computer_column = self.__game.fire_computer_player()
                    print(f"Computer fired at {chr(computer_column + ord('A'))}{computer_row + 1}")
                except GameOverException as e:
                    print(e)
                    print("Game over!")
                    break
            except IndexError:
                print("Move out of range")
            except ValueError:
                print("Invalid move")


ui = UI()
ui.start()
