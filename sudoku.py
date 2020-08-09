import math

board = [
    [1,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0]
]

board1 = [
    [1,1,0,0],
    [0,0,0,0],
    [0,0,0,0],
    [0,0,0,0]
]

def print_board(bo):
    x = (int(math.sqrt(len(bo))))
    for i in range(len(bo)):
        if i>0 and i%x==0:
            print('- - - - - - - - - - - ')

        for j in range(len(bo[0])):
            if j>0 and j%x==0:
                print('|', bo[i][j], sep= ' ', end=' ')
            else:
                print(bo[i][j], end=' ')
        print()

def findempty(myboard):
    for i in range(len(myboard)):
        for j in range(len(myboard[0])):
            if(myboard[i][j]==0):
                return i,j
    
    return len(myboard),len(myboard)

def is_valid(i, j, n, bo):
    if n==0:
        return False
    
    x = (int(math.sqrt(len(bo))))
    if(bo[i].count(n)==0 and [rows[j] for rows in bo].count(n)==0):
        for p in range(i-(i%x),i+x-(i%x)):
            for q in range(j-(j%x),j+x-(j%x)):
                if bo[p][q]==n:
                    return False

        return True

    return False

def solve(bo):
    i,j = findempty(bo)
    if (i==len(bo) and j==len(bo)):
        return True
    for k in range(1,len(bo)+1):
        if(is_valid(i, j, k, bo)):
            bo[i][j] = k
            if solve(bo):
                return True
            bo[i][j] = 0
    return False
