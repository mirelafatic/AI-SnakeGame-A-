from Snake import Snake
import random
import numpy as np
import time

rand = random.Random()


class AStar(Snake):

    #konstruktor
    def __init__(self):
        super().__init__()

    #3 heuristike
    #Eucliden distance
    def heuristic1(self, head):
        d0 = self.food[0] - head[0]
        d1 = self.food[1] - head[1]
        return np.sqrt(d0**2 + d1**2)

    # Manhattan distance
    def heuristic2(self, head):
        return abs(self.food[0]-head[0]) + abs(self.food[1]-head[1])

    #Diagonal Distance
    def heuristic3(self, head):
        dx = abs(head[0] - self.food[0])
        dy = abs(head[1] - self.food[1])
        D = 1
        D2 = np.sqrt(2)
        return  D * (dx + dy) + (D2 - 2 * D) * min(dx, dy)

    #pomocna funkcija koja vrsi posjecivanje\obilazenje
    def astar_pom(self, temp_head):
        self.explored.append(temp_head)
        self.explored_num += 1
        moves = self.get_safe_moves(temp_head)   #sigurni potezi

        for move in moves:
            head = temp_head.copy()
            head[0] += move[0]
            head[1] += move[1]
            h = self.heuristic1(head)        ################## 3 heuristike

            if str(head) not in self.parents.keys():
                self.parents[str(head)] = temp_head

            if head in self.explored:
                continue

            if self.isOnFood(head):      #pronadjena hrana
                self.food_found = True
                return
            if [h, head] not in self.not_explored:
                self.not_explored.insert(0, [h, head])   #dodamo u neposjecene
                self.not_explored.sort()                 #sortiramo neposjecene

    #glavna funkcija algoritma A star search
    def astar(self):
        self.food_found = False
        self.not_explored = []    #lista neposjecenih
        self.explored = []        #lista posjecenih
        self.parents = dict()     #dictionary roditelja

        temp_head = self.head.copy()
        orig_head = temp_head.copy()
        moves = self.get_safe_moves(temp_head)   #sigurni moves

        for move in moves:
            head = temp_head.copy()
            head[0] += move[0]
            head[1] += move[1]
            h = self.heuristic1(head)        ################### imam 3 heuristike

            if str(head) not in self.parents.keys():
                self.parents[str(head)] = temp_head
            if self.isOnFood(head):
                return move
            else:
                self.not_explored.insert(0, [h, head])   #ako nije, dodaj u neposjecene
                self.not_explored.sort()                 #sortiraj neposjecene

        while len(self.not_explored) > 0:          #dok je duzina neposjecenih veca od 0, tj dok ima neposjecenih
            nex = self.not_explored.pop(0)        #u nex uzmi prvog od sortiranih neposjecenih
            self.astar_pom(nex[1])              #za njega uradi astar_pom
            if self.food_found:                 #ako je food_found true izadji iz petlje
                break

        if self.food_found:         #hrana pronadjena
            curr = self.food         #indeksi food-a
            while self.parents[str(curr)] != orig_head:     #vracam se unazad do orig_head-a jer smo nasli put do hrane i treba nam samo prvi move sa puta
                curr = self.parents[str(curr)]
            return [curr[0] - orig_head[0], curr[1] - orig_head[1]]  #vrati potez

        elif len(self.explored) > 0:    #nije pronadjena, ima posjecenih
            curr = self.explored[-1]                       #pocinjem od poslednjeg posjecenog i
            while self.parents[str(curr)] != orig_head:    #i vracam se unazad
                curr = self.parents[str(curr)]
            return [curr[0] - orig_head[0], curr[1] - orig_head[1]]       #vratim buduci potez

        else: #nije pronadjena, nema posjecenih
            return rand.choice([[1, 0], [-1, 0], [0, 1], [0, -1]])


    def run_game(self, algorithm):
        while not self.terminal_test():
                vel = algorithm()    #vel mi je izabrani move od strane algoritma A* u ovom slucaju
                self.result(vel)
                self.display()
                #time.sleep(1/100)
