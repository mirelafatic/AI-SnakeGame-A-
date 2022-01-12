from AStar import AStar
from Ucost import Ucost

def main():
    game = AStar()
    game.run_game(game.astar)
    #game = Ucost()
    #game.run_game( game.ucost)
    print(game.explored_num)

main()
