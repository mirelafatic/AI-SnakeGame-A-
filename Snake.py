import numpy as np
import random

rand = random.Random()

class Snake:

    #konstruktor
    def __init__(self):
        self.height = 15    #visina board-a
        self.width = 30     #sirina board-a
        self.size = [self.height, self.width]
        self.board = np.zeros(self.size)    #board nam je matrica na kojoj ce biti:
                                                      # 0 na praznim poljima/mjestima
                                                      # 1 na poljima gdje je tijelo zmije
                                                      # 2 na polju na kome se nalazi glava zmije
                                                      #-1 na polju na kome se nalzi hrana
        self.score = 0  #score je broj pojedene hrane
        self.head = [self.height//2, self.width//2]   #glava se generise na sredini boarda (startna pozicija)
        self.vel = rand.choice([[0, 1], [0, -1], [1, 0], [-1, 0]])
        self.snake = [[self.head[0] - i*self.vel[0], self.head[1] - i*self.vel[1]] for i in range(2)]    #generisanje zmije, imace glavu i jedan segment tijela
        self.food = self.rand_food()    #hranu generisemo na random nacin
        #popunjavanje boarda:
        for s in self.snake:
            self.board[s[0], s[1]] = 1               #tijelo zmije
        self.board[self.head[0], self.head[1]] = 2   #glava zmije
        self.board[self.food[0], self.food[1]] = -1   #hrana
        self.explored_num = 0;  #za potrebe analize

    #funkcija za prikaz / stampu
    def display(self):
        disp_board = " " + "_"*self.width  + " "
        disp_board += "\n" + "|"
        for i in range(self.height):
            for j in range(self.width):
                if self.board[i, j] == 2:
                    #ako je na [i, j] glava zmije (oznacavamo je sa D)
                    disp_board += "D"
                elif self.board[i,j] == 1:
                    #ako je na [i, j] tijelo zmije (oznacavamo ga sa x)
                    disp_board += "#"
                elif self.board[i, j] == -1:
                    #ako je na [i, j] hrana (oznacavamo je sa O)
                    disp_board += "O"
                else:
                    #ako na polju nije ni zmijina glava ni tijelo ni hrana onda je polje prazno tj na njemu je blanko
                    disp_board += " "
            disp_board += "|\n"
            disp_board += "|"
        disp_board += "_"*self.width  + "|"
        disp_board += "\n"
        disp_board += f"Score: {self.score}\n "
        print(disp_board)


    #funkcija koja generise hranu (random na neko prazno polje)
    def rand_food(self):
        empty_spaces = [[i, j] for i in range(self.height) for j in range(self.width) if self.board[i, j] == 0]
        return rand.choices(empty_spaces)[0]

    #promijena vel-a
    def update_vel(self, vel):
        temp_head = [self.head[0] + vel[0], self.head[1] + vel[1]]
        if temp_head != self.snake[1]:   #provjeriti da to nije neki dio tijela zmije
            self.vel = vel

    #funkcija kojom updatujemo trenutno stanje
    def update_state(self):
        self.head[0] += self.vel[0]
        self.head[1] += self.vel[1]

        if self.head == self.food:   #ako je na hranu, pojede je, poraste, i generise se nova hrana
            self.score += 1
            self.snake.insert(0, self.head.copy())
            self.board[self.snake[1][0], self.snake[1][1]] = 1
            self.board[self.head[0], self.head[1]] = 2
            self.food = self.rand_food()
            self.board[self.food[0], self.food[1]] = -1
        else:    #samo pomjeri zmiju, nije na hranu nego na prazno
            self.snake.insert(0, self.head.copy())
            self.board[self.snake[1][0], self.snake[1][1]] = 1
            self.board[self.head[0], self.head[1]] = 2
            rem = self.snake.pop()
            self.board[rem[0], rem[1]] = 0


    #provjera da li je trenutno stanje terminalno
    def terminal_test(self):
        if self.head[0] < 0 or self.head[0] >= self.height: #van boarda
            self.head = self.snake[0].copy()
            return True
        elif self.head[1] < 0 or self.head[1] >= self.width: #van boarda
            self.head = self.snake[0].copy()
            return True
        elif self.head in self.snake[2::]: #zmija je udarila u tijelo
            self.head = self.snake[0].copy()
            return True

    #funkcija koja vraca sve dozvoljene move-s iz odredjenog stanja
    def get_safe_moves(self, temp_head = None):
        moves = [[-1, 0], [1, 0], [0, -1], [0, 1]]
        unsafe_moves = []

        if temp_head == None:
            temp_head_orig = self.head.copy()
        else:
            temp_head_orig = temp_head.copy()
        # remove unsafe moves
        for move in moves:
            temp_head = temp_head_orig.copy()
            temp_head[0] += move[0]
            temp_head[1] += move[1]

            if temp_head[0] < 0 or temp_head[0] >= self.height:
                unsafe_moves.append(move)
            elif temp_head[1] < 0 or temp_head[1] >= self.width:
                unsafe_moves.append(move)
            elif temp_head in self.snake:
                unsafe_moves.append(move)

        for move in unsafe_moves:
            moves.remove(move)

        return moves

    #funkcija koja vraca tacno jedno od sigurnih koraka
    def safe_move(self):
        moves = self.get_safe_moves()
        if len(moves) == 0: # no safe moves
            moves = [[-1, 0], [1, 0], [0, -1], [0, 1]]
        return rand.choice(moves)


    #rezultat nakon jedong move-a generisanog algoritmom
    def result(self, vel):
        self.update_vel(vel)
        self.update_state()


    #true ako se data pozicija (loc) poklapa sa food-om
    def isOnFood(self, loc):
        if self.food[0] == loc[0] and self.food[1] == loc[1]:
            return True
        else:
            return False

    #funkcija koja vraca prazna polja
    def empty_spaces(self):
        return [[i, j] for i in range(self.height) for j in range(self.width) if self.board[i, j] == 0 or self.board[i, j] == -1]
