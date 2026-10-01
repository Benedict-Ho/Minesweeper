import random

def create(l):
    arr = [["#" for _ in range(l)] for _ in range(l)]
    arr[0][0] = "  "
    for _ in range(1, l):
        arr[0][_] = f"{_:>2}"
        arr[_][0] = f"{_:>2}"
    return arr

def draw(arr):
    print()
    for row in arr:
        print(" ".join(f"{cell:>2}" for cell in row))
    print()

def bomb(b, l):
    global bombs
    bombs = []
    for _ in range(b):
        bombx = random.randint(1, l-1)
        bomby = random.randint(1, l-1)
        while [bombx, bomby] in bombs:
            bombx = random.randint(1, l-1)
            bomby = random.randint(1, l-1)
        bombs.append([bombx, bomby])
    return bombs

def first(arr):
    firstClickX = int(input("Enter x of click: "))
    firstClickY = int(input("Enter y of click: "))
    
    for _ in range(firstClickX-1, firstClickX+2):
        for __ in range(firstClickY-1, firstClickY+2):
            if [_, __] in bombs:
                bombs.remove([_, __])
                bx = random.randint(1, l-1)
                by = random.randint(1, l-1)
                while [bx, by] in bombs or (abs(bx - firstClickX) <= 1 and abs(by - firstClickY) <= 1):
                    bx = random.randint(1, l-1)
                    by = random.randint(1, l-1)
                bombs.append([bx, by])

    arr = scan(arr, firstClickX, firstClickY, bombs, l)
    return arr

def scan(arr, x, y, bombs, l):
    if x <= 0 or x >= l or y <= 0 or y >= l:
        return arr
    if arr[y][x] != "#":
        return arr
    c = 0
    for _ in range(x-1, x+2):
        for __ in range(y-1, y+2):
            if 0 < _ < l and 0 < __ < l:
                if [_, __] in bombs:
                    c += 1
    if c == 0:
        arr[y][x] = "."
        for _ in range(x-1, x+2):
            for __ in range(y-1, y+2):
                if 0 < _ < l and 0 < __ < l:
                    if arr[__][_] == "#":
                        scan(arr, _, __, bombs, l)
    else:
        arr[y][x] = str(c)
    return arr

def chord(arr, x, y, bombs, l):
    global over
    flags = 0
    for _ in range(x-1, x+2):
        for __ in range(y-1, y+2):
            if 0 < _ < l and 0 < __ < l:
                if arr[__][_] == "F":
                    flags += 1

    if flags == int(arr[y][x]):
        for _ in range(x-1, x+2):
            for __ in range(y-1, y+2):
                if 0 < _ < l and 0 < __ < l:
                    if arr[__][_] == "#":
                        if [_, __] in bombs:
                            print("Game over")
                            over = True
                            return over
                        else:
                            scan(arr, _, __, bombs, l)
    return over

def win(arr, bombs, l):
    for _ in range(1, l):
        for __ in range(1, l):
            if [_, __] not in bombs and (arr[__][_] == "#" or arr[__][_] == "F"):
                return False
    return True

bombs = []
over = False

mode = input("Would you like to play easy, medium or hard: ")

if mode == "easy":
    l = 10
    b = 10
elif mode == "medium":
    l = 17
    b = 40
elif mode == "hard":
    l = 26
    b = 120

arr = create(l)

bombs = bomb(b, l)
arr = first(arr)
draw(arr)

while over == False:
    if win(arr, bombs, l) == True:
        print("🎉 You win!")
        break

    x = int(input("input x axis: "))
    y = int(input("input y axis: "))
    flag = input("would you like to flag this coord, y/n: ")

    if flag == "y":
        if arr[y][x] == "F":
            arr[y][x] = "#"
        elif arr[y][x] == "#":
            arr[y][x] = "F"
    else:
        if [x, y] in bombs and arr[y][x] != "F":
            over = True
            print("game over")
        else:
            if arr[y][x].isdigit() == True:
                chord(arr, x, y, bombs, l)
            elif arr[y][x] == "#":
                arr = scan(arr, x, y, bombs, l)

    draw(arr)