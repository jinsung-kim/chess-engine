class Piece:
    def __init__(self, piece_type):
        self.piece_type = piece_type


class Pawn(Piece):
    def __init__(self, piece_type):
        super(self)