class Piece:
    def __init__(self, piece_type, color):
        self.piece_type = piece_type # k, n, q, r, p, b, -
        self.color = color # w or b

class Pawn(Piece):

    def __init__(self, piece_type, color):
        super().__init__(self, piece_type, color)
        self.moved = False # pawn first step (can be 2)

    def make_move(self, x, y):
        # incomplete
        return (x, y)


# class 



    