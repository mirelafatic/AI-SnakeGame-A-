from Snake import Snake
import random
import numpy as np
import time

rand = random.Random()


class Ucost(Snake):

    #konstruktor
    def __init__(self):
        super().__init__()

    #pomocna funkcija koja vrsi posjecivanje
    def ucost_pom(self, temp_head):
        self.explored.append(temp_head)
        self.explored_num += 1
        moves = self.get_safe_moves(temp_head)

        for move in moves:
            head = temp_head.copy()
            head[0] += move[0]
            head[1] += move[1]
            if head in self.explored:
                continue

            self.parents[str(head)] = temp_head
            if self.isOnFood(head):
                self.food_found = True
                return
            elif head not in self.explored:
                if head not in self.not_explored:
                    self.not_explored.insert(0, head)

    #glavnafunkcija uniform cost search
    def ucost(self):
        self.food_found = False
        self.not_explored = []
        self.explored = []
        self.parents = dict()

        temp_head = self.head.copy()
        orig_head = temp_head.copy()
        moves = self.get_safe_moves(temp_head)

        for move in moves:
            head = temp_head.copy()
            head[0] += move[0]
            head[1] += move[1]
            if self.isOnFood(head):
                return move
            else:
                self.not_explored.insert(0, head)
                self.parents[str(head)] = temp_head

        while len(self.not_explored) > 0:
            temp_head = self.not_explored.pop()
            self.ucost_pom(temp_head)
            if self.food_found:
                break

        if self.food_found:
            curr = self.food
            while self.parents[str(curr)] != orig_head:
                curr = self.parents[str(curr)]
            return [curr[0] - orig_head[0], curr[1] - orig_head[1]]

        else:
            return rand.choice([[1, 0], [-1, 0], [0, 1], [0, -1]])



    def run_game(self, algorithm):
        while not self.terminal_test():
                vel = algorithm()
                self.result(vel)
                self.display()
                #time.sleep(1/100)
