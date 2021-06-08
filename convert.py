import numpy as np

gameState = {'a1': 0, 'a2': None, 'a3': 1, 'a4': None, 'a5': 0, 'a6': None, 'a7': 2, 'a8': None, 'b1': None, 'b2': 0,
             'b3': None, 'b4': 0, 'b5': None, 'b6': 2, 'b7': None, 'b8': 2, 'c1': 0, 'c2': None, 'c3': 1, 'c4': None,
             'c5': 2, 'c6': None, 'c7': 2, 'c8': None, 'd1': None, 'd2': 0, 'd3': None, 'd4': 0, 'd5': None, 'd6': 0,
             'd7': None, 'd8': 2, 'e1': 0, 'e2': None, 'e3': 0, 'e4': None, 'e5': 0, 'e6': None, 'e7': 2, 'e8': None,
             'f1': None, 'f2': 1, 'f3': None, 'f4': 0, 'f5': None, 'f6': 2, 'f7': None, 'f8': 2, 'g1': 0, 'g2': None,
             'g3': 0, 'g4': None, 'g5': 0, 'g6': None, 'g7': 2, 'g8': None, 'h1': None, 'h2': 0, 'h3': None, 'h4': 0,
             'h5': None, 'h6': 2, 'h7': None, 'h8': 0}

boardKeys = list(gameState.keys())
boardValues = list(gameState.values())

lastLetter = 'a'
i = 0
for boardKey in boardKeys:
    if boardKey[0] != lastLetter:
        lastLetter = boardKey[0]
        i = i + 1
    if i % 2 == 0:
        if ((int(boardKey[1]) % 2) == 0):
            del gameState[boardKey]
    else:
        if ((int(boardKey[1]) % 2) > 0):
            del gameState[boardKey]

filteredGameState = gameState.copy()
print(filteredGameState)

ai = np.array(
    [[0, 0, 0, 0], [0, 0, 1, 0], [1, 1, 0, 0], [0, 0, 0, 0], [0, 2, 0, 0], [2, 0, 2, 2], [2, 2, 2, 2], [2, 2, 2, 0]])

aiToBoard = {}

for a in ai:
    print(a)
print("=============")

odd = ai[::2]
even = ai[1:8:2]
final = []
for i in range(4):
    final.append(odd[:, i])
    final.append(even[:, i])

final = np.array(final).flatten()

converted = filteredGameState.copy()
convertedKeys = list(converted.keys())
for i in range(len(final)):
    converted[convertedKeys[i]] = final[i]

print(converted)

board = {}
letters = ["a", "b", "c", "d", "e", "f", "g", "h"]
numbers = [1, 2, 3, 4, 5, 6, 7, 8]
lastLetter = letters[0]
i = 0
for letter in letters:
    if letter != lastLetter:
        lastLetter = letter
        i = i + 1
    for number in numbers:
        if i % 2 == 0:
            if (number % 2) == 0:
                continue
        else:
            if (number % 2) > 0:
                continue
        board[letter + str(number)] = 0

print("board", board)