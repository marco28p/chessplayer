import cv2
import numpy as np
import os

BOARD_SIZE = 640
SQ_SIZE = BOARD_SIZE // 8


class ChessRenderer:
    def __init__(self, piece_dir):
        self.piece_dir = piece_dir
        self.pieces = self.load_pieces()

    def load_pieces(self):
        pieces = {}
        for file in os.listdir(self.piece_dir):
            if file.endswith(".png"):
                key = file.split(".")[0]  # wp, bn, etc.
                img = cv2.imread(os.path.join(self.piece_dir, file), cv2.IMREAD_UNCHANGED)
                pieces[key] = img
        return pieces

    def draw_board(self):
        board = np.zeros((BOARD_SIZE, BOARD_SIZE, 3), dtype=np.uint8)

        light = (240, 217, 181)
        dark = (181, 136, 99)

        for r in range(8):
            for c in range(8):
                color = light if (r + c) % 2 == 0 else dark
                cv2.rectangle(
                    board,
                    (c*SQ_SIZE, r*SQ_SIZE),
                    ((c+1)*SQ_SIZE, (r+1)*SQ_SIZE),
                    color,
                    -1
                )

        return board

    def place_piece(self, board_img, piece, row, col):
        if piece == ".":
            return board_img

        piece_img = self.pieces[piece]

        # resize piece to fit square (slightly smaller for padding)
        size = int(SQ_SIZE * 0.85)
        piece_img = cv2.resize(piece_img, (size, size), interpolation=cv2.INTER_AREA)

        x = col * SQ_SIZE + (SQ_SIZE - size) // 2
        y = row * SQ_SIZE + (SQ_SIZE - size) // 2

        alpha = piece_img[:, :, 3] / 255.0 if piece_img.shape[2] == 4 else None
        rgb = piece_img[:, :, :3]

        for c in range(3):
            board_img[y:y+size, x:x+size, c] = (
                    alpha * rgb[:, :, c] +
                    (1 - alpha) * board_img[y:y+size, x:x+size, c]
            )

        return board_img

    def render(self, board_state):
        img = self.draw_board()

        for r in range(8):
            for c in range(8):
                img = self.place_piece(img, board_state[r][c], r, c)

        return img