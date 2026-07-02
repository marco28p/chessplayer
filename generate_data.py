import os
import random
import chess
from renderer import ChessRenderer

renderer = ChessRenderer("assets/pieces")

piece_map = {
    "wp": 0, "wn": 1, "wb": 2, "wr": 3, "wq": 4, "wk": 5,
    "bp": 6, "bn": 7, "bb": 8, "br": 9, "bq": 10, "bk": 11
}

SQUARE_SIZE = 640 // 8


def random_position():
    board = chess.Board()

    # play random legal moves
    for _ in range(random.randint(10, 40)):
        if board.is_game_over():
            break
        board.push(random.choice(list(board.legal_moves)))

    return board


def board_to_matrix(board):
    matrix = [["." for _ in range(8)] for _ in range(8)]

    for square in chess.SQUARES:
        piece = board.piece_at(square)
        if not piece:
            continue

        symbol = piece.symbol()

        mapping = {
            "P":"wp","N":"wn","B":"wb","R":"wr","Q":"wq","K":"wk",
            "p":"bp","n":"bn","b":"bb","r":"br","q":"bq","k":"bk"
        }

        row = 7 - chess.square_rank(square)
        col = chess.square_file(square)

        matrix[row][col] = mapping[symbol]

    return matrix


def matrix_to_labels(matrix):
    labels = []

    for r in range(8):
        for c in range(8):
            piece = matrix[r][c]
            if piece == ".":
                continue

            class_id = piece_map[piece]

            x = (c * SQUARE_SIZE + SQUARE_SIZE / 2) / 640
            y = (r * SQUARE_SIZE + SQUARE_SIZE / 2) / 640

            w = SQUARE_SIZE / 640
            h = SQUARE_SIZE / 640

            labels.append(f"{class_id} {x} {y} {w} {h}")

    return labels


def generate_dataset(n=2000):
    os.makedirs("dataset/images/train", exist_ok=True)
    os.makedirs("dataset/labels/train", exist_ok=True)

    for i in range(n):
        board = random_position()
        matrix = board_to_matrix(board)

        img = renderer.render(matrix)

        img_path = f"dataset/images/train/{i}.png"
        label_path = f"dataset/labels/train/{i}.txt"

        import cv2
        cv2.imwrite(img_path, img)

        labels = matrix_to_labels(matrix)

        with open(label_path, "w") as f:
            f.write("\n".join(labels))

    print("DONE")


if __name__ == "__main__":
    generate_dataset()