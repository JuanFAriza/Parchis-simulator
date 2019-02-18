import random
from tkinter import Tk, Label, Button
from PIL import Image, ImageTk


class Board:
    # This object controls gameplay
    # Attributes:
    # @num_players
    # @num_boxes
    # @pieces_pos
    # @pieces_status : 0 = jail; 1 = home; 2 = danger; 3 = safe; 4 = other home; 5 = stairs; 6 = arrival
    # @game_in_progress
    # @current_player : empieza el jugador , termina la ronda el jugador "-1"
    # @dice_roll
    #
    # Methods:
    #

    def __init__(self, players=4):
        self.num_players = players
        self.num_boxes = 17*players
        self.pieces_status = [[0]*4]
        for i in range(1,players):
            self.pieces_status += [[0]*4]
        
        self.pieces_pos = [[0]*4]
        for i in range(1,players):
            self.pieces_pos += [[17*i]*4]

        self.current_player = 0
        self.game_in_progress = True
        self.dice_roll = [0, 0]
        

    def play_turn(self, player):
        player.pieces_pos = self.pieces_pos
        player.pieces_status = self.pieces_status
        dice = [random.randint(1,6), random.randint(1,6)]
        self.dice_roll = dice
        player.play(dice)

    def display_board(self):
        # puedo usar imshow de matplotlib.plt y matplotlib.image
        # img = matplotlib.image.imread('foto')
        # plt.imshow(img)
        # plt.scatter()
        # plt.show()
        return None


class Player:
    # Esta es la clase que actúa como jugador
    # Attributes:
    # @num_players
    # @num_boxes
    # @player_num
    # @pieces_pos
    # @pieces_status
    #
    # Methods:
    #
    
    def __init__(self, playboard):
        self.num_players = playboard.num_players
        self.num_boxes = playboard.num_boxes
        self.pieces_status = playboard.pieces_status
        self.pieces_pos = playboard.pieces_pos
        self.player_num = playboard.current_player

    def play(self, dice):
        if dice[0] == dice[1]: # got a pair
            if self.pieces_status[self.player_num][0]*self.pieces_status[self.player_num][1]*self.pieces_status[self.player_num][2]*self.pieces_status[self.player_num][3] == 0: # there are pieces in jail that can be freed
                if dice[0] == 1 | dice[0] == 6: # can free all pieces from jail
                    freed_pieces = 0
                    for i in range(4):
                        if self.pieces_status[self.player_num][i] == 0:
                            self.pieces_status[self.player_num][i] = 1
                            self.pieces_pos[self.player_num][i] = 17*self.player_num
                            freed_pieces += 1
                    dice[1] = 0
                    if freed_pieces > 3:
                        dice[0] = 0
                else: # can free at most 2 pieces
                    freed_pieces = 0
                    for i in range(4):
                        if freed_pieces < 2:
                            if self.pieces_status[self.player_num][i] == 0:
                                self.pieces_status[self.player_num][i] = 1
                                self.pieces_pos[self.player_num][i] = 17*self.player_num
                                freed_pieces += 1
                        else: # has freed all pieces
                            i = 5
                    dice[1] = 0
                    if freed_pieces > 1:
                        dice[0] = 0
        move(dice)

    def move(self, dice):
        return None
        

class BoardGUI:
    def __init__(self, master):
        self.master = master
        
        self.dims_board = [800, 800]
        self.dims_bttn = [28, 28]

        self.colors = ["yellow", "red", "green", "blue"]
        
        master.title("Parchis Simulator.  El mejor parqués")
        master.geometry(str(self.dims_board[0]) + "x" + str(self.dims_board[1]))

        board_image = Image.open("board.png")
        copy_of_image = board_image.copy()
        board_image = copy_of_image.resize((self.dims_board[0], self.dims_board[1]))

        button_image = Image.open("board.png")
        copy_of_image = button_image.copy()
        button_image = copy_of_image.resize((self.dims_bttn[0], self.dims_bttn[1]))
        
        board_photo = ImageTk.PhotoImage(board_image)
        button_photo = ImageTk.PhotoImage(button_image)
        
        self.background = Label(image=board_photo)
        self.background.image = board_photo
        
        self.background.pack()

        self.pieces = self.create_pieces()

        self.piece_1 = Label(image=button_photo)
        self.piece_1.image = button_photo

        self.piece_1.place(x=510,y=10)

        self.show_pieces()
    
    def create_piece(self, color):
        # por ahora voy a crear piezas sin color
        button_image = Image.open("board.png")
        copy_of_image = button_image.copy()
        button_image = copy_of_image.resize((self.dims_bttn[0], self.dims_bttn[1]))

        button_photo = ImageTk.PhotoImage(button_image)
        piece = Label(image=button_photo)
        piece.image = button_photo
        
        return piece

    def create_pieces(self):
        pieces = []
        
        for color in self.colors:
            player_pieces = []
            for j in range(4):
                player_pieces += [self.create_piece("blue")]
            pieces += [player_pieces]

        return pieces

    def show_pieces(self):
        width = self.dims_board[0]
        height = self.dims_board[1]
        
        posx = [[50,100,50,100],[width - 50,width - 100,width - 50,width - 100],[50,100,50,100],[width - 50,width - 100,width - 50,width - 100]]
        posy = [[50,50,100,100],[50,50,100,100],[height - 50,height - 50,height - 100,height - 100],[height - 50,height - 50,height - 100,height - 100]]
        for i in range(4):
            for j in range(4):
                self.pieces[i][j].place(x=posx[i][j],y=posy[i][j])
        
        return None


board = Board()
players = [Player(board)]

root = Tk()
gui = BoardGUI(root)
root.mainloop()

#while board.game_in_progress == true:
#    board.play_turn(players[board.current_player%len(players)])
    
