import argparse
from sudoku import solve
from tkinter import Tk, Canvas, Frame, Button, BOTH, BOTTOM, TOP

boards = ['n00b', 'pr0', 'debug', 'error']
margin = 20
cellSide = 50
WIDTH = HEIGHT = margin*2 + cellSide*9

class SudokuError(Exception):
    """
        An Exception Occured!
    """
    pass

class SudokuBoard(object):
    """Board Representation"""
    def __init__(self, sudFile):
        self.board = self.__createBoard(sudFile)

    def __createBoard(self, sudFile):
        board = []

        for line in sudFile:
            line = line.strip()
            if len(line) != 9:
                raise SudokuError(f"{line} contains more or less than 9 characters!")

            board.append([])

            for char in line:
                if char.isdigit():
                    board[-1].append(int(char))
                else:
                    raise SudokuError(f"{char} in {line} is not a Number")
        
        if len(board)!=9:
            raise SudokuError("Board does not contain 9 lines")

        return board

class SudokuGame(object):
    """Stores state of game and checks if it has won!"""
    def __init__(self, boardFile):
        self.boardFile = boardFile
        self.startPuzzle = SudokuBoard(boardFile).board

    def start(self):
        self.gameOver = False
        self.puzzle = []
        for i in range(9):
            self.puzzle.append([])
            for j in range(9):
                self.puzzle[i].append(self.startPuzzle[i][j])

    def is_valid(self, i, j, n, bo):
        if n==0:
            return False
        
        x = 3
        if(bo[i].count(n)==0 and [rows[j] for rows in bo].count(n)==0):
            for p in range(i-(i%x),i+x-(i%x)):
                for q in range(j-(j%x),j+x-(j%x)):
                    if bo[p][q]==n:
                        return False

            return True

        return False

    def check_win(self):
        for row in range(9):
            if not self.__check_row(row):
                return False
        for column in range(9):
            if not self.__check_column(column):
                return False
        for row in range(3):
            for column in range(3):
                if not self.__check_square(row, column):
                    return False
        self.gameOver = True
        return True

    def __check_block(self, block):
        return set(block) == set(range(1, 10))

    def __check_row(self, row):
        return self.__check_block(self.puzzle[row])

    def __check_column(self, column):
        return self.__check_block(
            [self.puzzle[row][column] for row in range(9)]
        )

    def __check_square(self, row, column):
        return self.__check_block(
            [
                self.puzzle[r][c]
                for r in range(row * 3, (row + 1) * 3)
                for c in range(column * 3, (column + 1) * 3)
            ]
        )
    
class SudokuUI(Frame):
    """This will draw UI and accept user input"""
    def __init__(self, parent, game):
        self.game = game
        self.parent = parent
        Frame.__init__(self, parent)
        self.row = 0
        self.col = 0
        
        self.__initUI()
    
    def __initUI(self):
        self.parent.title("Sudoku")
        self.pack(fill=BOTH, expand=1)
        self.canvas = Canvas(self, width=WIDTH, height=HEIGHT)
        self.canvas.pack(fill=BOTH, side=TOP)

        clearButton = Button(self, text="Clear ALL", command=self.__clearAnswers)
        clearButton.pack(side=BOTTOM, fill=BOTH)

        solveButton = Button(self, text="Solve?", command=self.__solve)
        solveButton.pack(side=BOTTOM, fill=BOTH)

        self.__drawGrid()
        self.__drawPuzzle()

        self.canvas.bind("<Button-1>", self.__cellClicked)
        self.canvas.bind("<Key>", self.__keyPressed)

    def __solve(self):
        self.__clearAnswers()
        solve(self.game.puzzle)
        self.__drawPuzzle()
        self.__drawSolved()


    def __drawGrid(self):
        for x in range(10):
            color = 'red' if x%3==0 else 'black'

            x0 = margin + x * cellSide
            y0 = margin
            x1 = margin + x * cellSide
            y1 = HEIGHT - margin

            p0 = margin
            q0 = margin + x * cellSide
            p1 = WIDTH - margin
            q1 = margin + x * cellSide

            self.canvas.create_line(x0, y0, x1, y1, fill=color)
            self.canvas.create_line(p0, q0, p1, q1, fill=color)

    def __drawPuzzle(self):
        self.canvas.delete("numbers")
        for i in range(9):
            for j in range(9):
                answer = self.game.puzzle[i][j]
                if answer!=0:
                    x = margin + j * cellSide + cellSide/2
                    y = margin + i * cellSide + cellSide/2
                    original = self.game.startPuzzle[i][j]
                    color = "black" if answer==original else "sea green"
                    self.canvas.create_text(x, y, text=answer, tags="numbers", fill=color)

    def __clearAnswers(self):
        self.game.start()
        self.canvas.delete("victory")
        self.canvas.delete("solved")
        self.__drawPuzzle()

    def __cellClicked(self, event):
        if self.game.gameOver:
            return
        x, y = event.x, event.y
        
        if (margin < x < WIDTH - margin and margin < y < HEIGHT - margin):
            self.canvas.focus_set()

            row, col = int((y - margin) / cellSide), int((x - margin) / cellSide)

            if (row, col) == (self.row, self.col):
                self.row, self.col = -1, -1
            elif self.game.startPuzzle[row][col] == 0:
                self.row, self.col = row, col
        else:
            self.row, self.col = -1, -1

        self.__drawCursor()

    def __drawCursor(self):
        self.canvas.delete("cursors")

        if(self.row>=0 and self.col>=0):
            x0 = margin + self.col * cellSide
            y0 = margin + self.row * cellSide
            self.canvas.create_rectangle(x0, y0, x0 + cellSide, y0 + cellSide, outline = "red", tags = "cursors")


    def __keyPressed(self, event):
        if self.game.gameOver:
            print(1)
            return

        if self.row>=0 and self.col>=0 and event.char in "1234567890":
            self.game.puzzle[self.row][self.col] = int(event.char)
            self.row, self.col = -1, -1
            self.__drawPuzzle()
            self.__drawCursor()
            if self.game.check_win():
                self.__drawVictory()

    def __drawVictory(self):
        x0 = y0 = margin + cellSide
        x1 = y1 = margin + cellSide * 8

        self.canvas.create_oval(x0, y0, x1, y1, tags = "victory", fill="black", outline="red")

        x = y = margin + cellSide * 4 + cellSide/2
        self.canvas.create_text(x, y, text="YOU WON!", tags="victory", fill="red", font=("Arial", 32))

    def __drawSolved(self):
        y0 = margin + HEIGHT - cellSide
        y1 = margin + HEIGHT - cellSide/2
        x0 = margin + cellSide
        x1 = WIDTH - cellSide

        self.canvas.create_rectangle(x0, y0, x1, y1, tags = "solved", fill="black", outline="red")

        x = (x0+x1)/2
        y = (y0+y1)/2
        self.canvas.create_text(x, y, text="I solved IT!! Not YOU!!", tags="solved", fill="red", font=("Arial", 14))


def parse_arguments():
    """
        Parses arguments of the form:
            sudoku_gui.py <board name>
    """
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument("--board", help="desired board name", type=str, choices=boards, required=True)

    args =  arg_parser.parse_args()
    return args.board


if __name__ == "__main__":
    boardSelected = parse_arguments()

    with open("%s.sudoku" % boardSelected, 'r') as boardFile:
        game = SudokuGame(boardFile)
        game.start()

        root = Tk()
        SudokuUI(root, game)
        root.geometry("%dx%d" % (WIDTH, HEIGHT+100))
        root.mainloop()



