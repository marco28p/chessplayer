from renderer import ChessRenderer

START_POS = [
    ["br","bn","bb","bq","bk","bb","bn","br"],
    ["bp","bp","bp","bp","bp","bp","bp","bp"],
    [".",".",".",".",".",".",".","."],
    [".",".",".",".",".",".",".","."],
    [".",".",".",".",".",".",".","."],
    [".",".",".",".",".",".",".","."],
    ["wp","wp","wp","wp","wp","wp","wp","wp"],
    ["wr","wn","wb","wq","wk","wb","wn","wr"],
]

renderer = ChessRenderer("assets/pieces")

img = renderer.render(START_POS)

import cv2
cv2.imwrite("test_board.png", img)

print("saved test_board.png")