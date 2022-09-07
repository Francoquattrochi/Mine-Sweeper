import pygame
from random import randint
from time import time

pygame.init()
pygame.display.set_caption("Franco Mine Sweeper")
WIDTH, HEIGHT = 750, 750
ROWS = 25
COLS = 25
CELLSIZE = 25
SEP = 10
DIFF = 40
BACK = (99, 176, 224)
GREY = (220, 220, 220)
BLACK = (0, 0, 0)
ORANGE = (39, 123, 192)
BEIGE = (255, 149, 81)
GREEN = (0, 255, 0)

MW = pygame.display.set_mode((WIDTH, HEIGHT))

clock = pygame.time.Clock()

isRunning = True
allCells = []
lost = False
win = False
screen = 0
total_mines = 0
score = 0


class Label:
    def __init__(self, x, y, width, height, text, fsize, fill_color, text_color):
        self.rect = pygame.Rect(x, y, width, height)
        self.font = pygame.font.SysFont("verdana", fsize).render(text, True, text_color)
        self.fill_color = fill_color

    def drawLabel(self, shift_x, shift_y):
        pygame.draw.rect(MW, self.fill_color, self.rect)
        MW.blit(self.font, (self.rect.x + shift_x, self.rect.y + shift_y))

    def drawBorder(self):
        pygame.draw.rect(MW, BLACK, self.rect, 2)

    def drawBoth(self, shift_x, shift_y):
        self.drawLabel(shift_x, shift_y)
        self.drawBorder()


class Cell:
    def __init__(self, x, y, width, height):
        self.rect = pygame.Rect(x, y, width, height)
        self.fill_color = GREY
        self.val = None
        self.image = pygame.image.load("Block.png")
        self.clicked = False
        self.cellRow = (x - SEP) // CELLSIZE
        self.cellCol = (y - SEP) // CELLSIZE
        self.flag = False

    def __repr__(self):
        return str(self.val)

    def draw(self):
        MW.blit(self.image, (self.rect.x, self.rect.y))

    def handleClick(self):
        global lost
        self.clicked = True
        if self.val != "MINE":
            self.image = pygame.image.load(str(self.val) + ".png")
        else:
            self.image = pygame.image.load("Mine.png")
            for row in allCells:
                for cell in row:
                    if not cell.clicked:
                        cell.handleClick()
            lost = True

        adjacent = getAdjacentCells(self.cellRow, self.cellCol)
        for cell in adjacent:
            if cell.val == 0 and not cell.clicked:
                cell.handleClick()
        scan()

    def toggleFlag(self):
        if not self.clicked:
            if self.flag:
                self.image = pygame.image.load("Block.png")
            else:
                self.image = pygame.image.load("Flag.png")
        self.flag = not self.flag


def createGrid():
    for i in range(ROWS):
        row = []
        for j in range(COLS):
            row.append(Cell(i * COLS + SEP, j * ROWS + SEP, CELLSIZE, CELLSIZE))
        allCells.append(row)


def addMines():
    global total_mines
    total_mines = 0
    for row in allCells:
        for cell in row:
            if randint(1, DIFF) == 1:
                cell.val = "MINE"
                total_mines += 1


def addNums():
    for i in range(len(allCells)):
        for j in range(len(allCells[i])):
            if allCells[i][j].val == "MINE":
                continue
            adjacent = getAdjacentCells(i, j)
            mines = 0
            for cell in adjacent:
                if cell.val == "MINE":
                    mines += 1
            allCells[i][j].val = mines


def check_flags():
    global win
    score = 0
    clicked = 0
    for row in allCells:
        for cell in row:
            if cell.clicked == True:
                clicked += 1
            if cell.val == "MINE" and cell.flag:
                score += 1
    if score == total_mines and clicked == (ROWS * COLS) - total_mines:
        win = True


def scan():
    for i in range(ROWS):
        for j in range(COLS):
            if allCells[i][j].clicked and allCells[i][j].val == 0:
                crossCells = getCrossCells(i, j)
                for cell in crossCells:
                    if not cell.clicked and cell.val != "MINE":
                        cell.clicked = True
                        cell.image = pygame.image.load(str(cell.val) + ".png")


def getAdjacentCells(i, j):
    adjacent = []
    for a in range(i - 1, i + 2):
        for b in range(j - 1, j + 2):
            if a >= 0 and a <= ROWS - 1 and b >= 0 and b <= COLS - 1 and (a != i or b != j):
                adjacent.append(allCells[a][b])
    return adjacent


def getCrossCells(i, j):
    cross = []
    for a in range(i - 1, i + 2):
        for b in range(j - 1, j + 2):
            if a >= 0 and a <= ROWS - 1 and b >= 0 and b <= COLS - 1 and (a == i or b == j):
                cross.append(allCells[a][b])
    return cross


def drawAll():
    global win
    global lost
    MW.fill(BACK)
    for row in allCells:
        for cell in row:
            cell.draw()
    if lost or win:
        menuButton.drawBoth(8, 0)
    if win:
        winText.drawLabel(20, 0)


def startGame():
    global allCells
    global win
    global lost
    allCells = []
    win = False
    lost = False
    createGrid()
    addMines()
    addNums()


def drawMenu():
    MW.fill(BACK)
    for cell in allCells:
        cell.draw()
    titleText.drawBoth(20, 8)
    outlineBox.drawBoth(0, 0)
    playButton.drawBoth(60, 10)
    diffButton.drawBoth(2, 12)
    exitButton.drawBoth(60, 15)


def menuAnimation():
    for cell in allCells:
        cell.rect.y += 5


def drawDiffMenu():
    diff1Button.fill_color = ORANGE
    diff2Button.fill_color = ORANGE
    diff3Button.fill_color = ORANGE
    if DIFF == 10:
        diff1Button.fill_color = (255, 255, 0)
    elif DIFF == 6:
        diff2Button.fill_color = (255, 255, 0)
    elif DIFF == 3:
        diff3Button.fill_color = (255, 255, 0)
    MW.fill(BACK)
    diffText.drawBoth(30, 8)
    outlineBox.drawBoth(0, 0)
    diff1Button.drawBoth(45, 10)
    diff2Button.drawBoth(12, 12)
    diff3Button.drawBoth(45, 15)
    menuButton.drawBoth(8, 0)


titleText = menuButton = Label(125, 50, 500, 100, "Mine Sweeper", 65, ORANGE, BEIGE)
menuButton = Label(25, 725, 100, 20, "Main Menu", 15, ORANGE, BEIGE)
outlineBox = Label(WIDTH / 2 - 125, HEIGHT / 2 - 150, 300, 400, "", 0, ORANGE, BEIGE)
playButton = Label(outlineBox.rect.x + 50, outlineBox.rect.y + 50, outlineBox.rect.width - 100, 75, "Play", 45, ORANGE,
                   BEIGE)
diffButton = Label(outlineBox.rect.x + 50, playButton.rect.y + 100, outlineBox.rect.width - 100, 75, "Difficulty", 44,
                   ORANGE, BEIGE)
exitButton = Label(outlineBox.rect.x + 50, diffButton.rect.y + 100, outlineBox.rect.width - 100, 75, "Exit", 45, ORANGE,
                   BEIGE)

diffText = Label(125, 50, 500, 100, "Set Difficulty", 65, ORANGE, BEIGE)
diff1Button = Label(outlineBox.rect.x + 50, outlineBox.rect.y + 50, outlineBox.rect.width - 100, 75, "Easy", 45, ORANGE,
                    BEIGE)
diff2Button = Label(outlineBox.rect.x + 50, playButton.rect.y + 100, outlineBox.rect.width - 100, 75, "Medium", 44,
                    ORANGE, BEIGE)
diff3Button = Label(outlineBox.rect.x + 50, diffButton.rect.y + 100, outlineBox.rect.width - 100, 75, "Hard", 45,
                    ORANGE, BEIGE)

winText = Label(200, -5, 500, 25, "You Win!", 60, BACK, GREEN)
start_time = time()
while isRunning:
    pygame.display.update()
    clock.tick(40)

    for event in pygame.event.get():
        x, y = pygame.mouse.get_pos()
        cellRow = (x - SEP) // CELLSIZE
        cellCol = (y - SEP) // CELLSIZE
        if event.type == pygame.QUIT:
            isRunning = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            if screen == 0:
                if playButton.rect.collidepoint(x, y):
                    screen = 1
                    startGame()
                elif diffButton.rect.collidepoint(x, y):
                    screen = 2
                elif exitButton.rect.collidepoint(x, y):
                    isRunning = False
            elif screen == 1:
                if SEP <= x <= COLS * CELLSIZE + SEP and SEP <= y <= ROWS * CELLSIZE + SEP:
                    if event.button == 1:
                        allCells[cellRow][cellCol].handleClick()
                elif menuButton.rect.collidepoint(x, y):
                    screen = 0
                    allCells = []
            elif screen == 2:
                drawDiffMenu()
                if menuButton.rect.collidepoint(x, y):
                    screen = 0
                    allCells = []
                if diff1Button.rect.collidepoint(x, y):
                    DIFF = 10
                elif diff2Button.rect.collidepoint(x, y):
                    DIFF = 6
                elif diff3Button.rect.collidepoint(x, y):
                    DIFF = 3
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_f:
                allCells[cellRow][cellCol].toggleFlag()

    if screen == 0:
        drawMenu()
        menuAnimation()
        if (time() - start_time) > 0.25:
            bomb = Cell(randint(0, 975), -25, 25, 25)
            bomb.fill_color = BACK
            bomb.image = pygame.image.load("Mine.png")

            allCells.append(bomb)
            start_time = time()
    elif screen == 1:
        drawAll()
        check_flags()

    elif screen == 2:
        drawDiffMenu()