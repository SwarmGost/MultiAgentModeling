# Импорты

# import time

import random
import pygame as p
from pygame.locals import *


# Ввод данных о размере поля
# q = int(input("Вариант: "))

# Константы
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

# COLOR = (255, 0, 0)
pixel = 10                 # Размер отдельного квадратика
sleepTime = 50             # Количество пропускаемых циклов для самедления обсчета
sl = sleepTime             # Установка счетсика циклов на максимум
pause = True               # Пауза - True, обсчет - False
con = 0                    # Общий счетчик циклов (Печатается при остановке)
polex = 700                # Размер в пикселях окна по X
poley = 500                # Размер в пикселях окна по Y
lifeZ = 7                  # количество циклов голодной смерти
lifeD = 20                 # количество циклов смерти от старости
lifeTr = 0.8                 # Вероятногсть зарождения травы
edaRange = 5               # Радиус видимости еды
monsterSleep = 10          # Время бездействия хищника после еды

# Создаем окно
root = p.display.set_mode((polex, poley))
# 2х мерный список с помощью генераторных выражений
# cells = [[random.choice([False, True]) for j in range(root.get_width() // pixel)] for i in range(root.get_height() // pixel)]
# Обнуляем основной массив
cells = [[0 for i in range(poley // pixel)] for j in range(polex // pixel)]
cells[30][20] = 1
cells[31][21] = 1
cells[29][20] = 1
#cells[27][25] = 1

class Zver:
    zID = 0

    def __init__(self, x, y, M):
        self.x = x  # Расположение зверя x
        self.y = y  # Расположение зверя y
        self.M = M  # Тип зверя: False - травоядный, True - хищник
        self.ID = Zver.zID
        Zver.zID += 1
        self.sex = False  # Режим поиска False - поиск еды, True - размножение
        self.count = 0  # Счетчик времени со времени еды
        if M:
            self.old = lifeD + monsterSleep  # Циклов до смерти хищника
        else:
            self.old = lifeD # Циклы жизни травоядных
        self.move = 0  # Направление движения 1 - вверх-лево, а далее - по часовой, 0 - на месте

    def nextStep(self):
        if self.move == 0:
            return self.x, self.y
        nx, ny = 0, 0
        if self.y > 0 and self.move >= 1 and self.move <= 3:
            ny = self.y - 1
        if self.y < len(cells[self.x]) and self.move >= 5 and self.move <= 7:
            ny = self.y + 1
        if self.x > 0 and (self.move == 7 or self.move == 8 or self.move == 1):
            nx = self.x - 1
        if self.x < len(cells) and self.move >= 3 and self.move <= 5:
            nx = self.x + 1
        if nx == 0:
            nx = self.x
        if ny == 0:
            ny = self.y
        return nx, ny


    def search(self):
        navi = [0, 0, 0, 0, 0, 0, 0, 0, 0]
        for j in range(self.x, polex//pixel):
            for i in range(self.y, poley//pixel):
                if cells[j][i] > 0 and (self.x - j > 0 or self.y - i > 0):
                    navi[5] += edaRange/((self.x - j) ** 2 + (self.y - i) ** 2) ** 0.5
        for i in range(0, self.x):
            for j in range(self.y, poley//pixel):
                if cells[i][j] > 0 and (self.x - i > 0 or self.y - j > 0):
                    navi[7] += edaRange/((self.x - i) ** 2 + (self.y - j) ** 2) ** 0.5
        for i in range(self.x, polex//pixel):
            for j in range(0, self.y):
                if cells[i][j] > 0 and (self.x - i > 0 or self.y - j > 0):
                    navi[3] += edaRange/((self.x - i) ** 2 + (self.y - j) ** 2) ** 0.5
        for i in range(0, self.x):
            for j in range(0, self.y):
                if cells[i][j] > 0 and (self.x - i > 0 or self.y - j > 0):
                    navi[1] += edaRange/((self.x - i) ** 2 + (self.y - j) ** 2) ** 0.5
        navi[2] = (navi[1] + navi[3]) * 0.8
        navi[4] = (navi[3] + navi[5]) * 0.8
        navi[6] = (navi[5] + navi[7]) * 0.8
        navi[8] = (navi[1] + navi[7]) * 0.8
        napr = 0
        for i in range(1, 9):
            if navi[i] > navi[napr] or (navi[i] == navi[napr] and random.random() < 0.5):
                napr = i
        #print(navi, napr)
        self.move = napr

zvery = [Zver(28, 21, False), Zver(32, 19, False), Zver(25, 27, True), Zver(38, 15, True)]

def isZvery(nx, ny):
    for j in zvery:
        if j.x == nx and j.y == ny:
            return True
    return False

def printScr():
    # Заполняем экран белым цветом
    root.fill(WHITE)
    ct, cz, cm = 0, 0, 0
    # Проходимся по всем клеткам
    for i in range(0, len(cells)):
        for j in range(0, len(cells[i])):
            # Рисуем клетки
            p.draw.rect(root, GREEN if cells[i][j] > 0 else WHITE, [i * pixel, j * pixel, pixel-1, pixel-1])
            if cells[i][j] > 0:
                ct += 1
    # Рисуем зверей
    for i in zvery:
        if i.M:
            p.draw.rect(root, RED, [i.x * pixel, i.y * pixel, pixel - 1, pixel - 1])
            cz += 1
        else:
            p.draw.rect(root, BLUE, [i.x * pixel, i.y * pixel, pixel - 1, pixel - 1])
            cm += 1
    # Обновляем экран
    p.display.update()
    # Печатаем статистику
    print(con, ct, cz, cm)

def searchZver(x, y, isMonstr):
    navi = [0, 0, 0, 0, 0, 0, 0, 0, 0]
    for i in zvery:
        if i.M == isMonstr and x >= i.x and y >= i.y and (x - i.x > 0 or y - i.y > 0):
            navi[1] += lifeZ/((x - i.x) ** 2 + (y - i.y) ** 2) ** 0.5
        if i.M == isMonstr and x <= i.x and y >= i.y and (x - i.x > 0 or y - i.y > 0):
            navi[3] += lifeZ/((x - i.x) ** 2 + (y - i.y) ** 2) ** 0.5
        if i.M == isMonstr and x >= i.x and y <= i.y and (x - i.x > 0 or y - i.y > 0):
            navi[7] += lifeZ/((x - i.x) ** 2 + (y - i.y) ** 2) ** 0.5
        if i.M == isMonstr and x <= i.x and y <= i.y and (x - i.x > 0 or y - i.y > 0):
            navi[5] += lifeZ/((x - i.x) ** 2 + (y - i.y) ** 2) ** 0.5
    navi[2] = (navi[1] + navi[3]) * 0.8
    navi[4] = (navi[3] + navi[5]) * 0.8
    navi[6] = (navi[5] + navi[7]) * 0.8
    navi[8] = (navi[1] + navi[7]) * 0.8
    napr = 0
    for i in range(1, 9):
        if navi[i] > navi[napr] or (navi[i] == navi[napr] and random.random() < 0.5):
            napr = i
    #print(navi, napr)
    return napr

def isMonstEat(x, y):
    for i in zvery:
        if ((x - i.x) ** 2 + (y - i.y) ** 2) ** 0.5 < 1.7 and not i.M:
            zvery.remove(i)
            return True
    return False

def newZver(cx, xy, isMonster):
    for i in range(-1, 1):
        for j in range (-1, 1):
            if not isZvery(cx+i, xy+j) and cx+i >= 0 and cx+i < polex//pixel and xy+j >= 0 and xy+j < poley//pixel:
                zvery.append(Zver(cx+i, xy+j, isMonster))
                return


printScr()
# Основной цикл
while 1:

    # Если не стоим на паузе и не пропускаем циклы, то считаем следующий шаг
    if not pause and sl <= 0:
        for i in zvery:
            i.old -= 1
            if not i.M:
                if cells[i.x][i.y] > 0 and not i.sex:
                    i.move = 0
                    i.count = 0
                    cells2[i.x][i.y] = 0
                    i.sex = True
                elif not i.sex:
                    i.search()
                    i.count += 1
                else:
                    i.move = searchZver(i.x, i.y, False)
                    for j in zvery:
                        if not i.ID == j.ID and (i.x - j.x) ** 2 <= 1 and (i.y - j.y) ** 2 <= 1:
                            newZver(i.x, i.y, False)
                            i.sex = False
                            j.sex = False
                            break
            else:
                if not i.sex and i.count > 0:
                    if isMonstEat(i.x, i.y):
                        #print("Eat")
                        i.move = 0
                        i.count = -monsterSleep
                        i.sex = True
                    else:
                        i.move = searchZver(i.x, i.y, False)
                        i.count += 1
                elif not i.sex and i.count <= 0:
                    i.move = 0
                    i.count += 1
                elif i.sex:
                    i.move = searchZver(i.x, i.y, True)
                    for j in zvery:
                        if not i.ID == j.ID and (i.x - j.x) ** 2 <= 1 and (i.y - j.y) ** 2 <= 1:
                            newZver(i.x, i.y, True)
                            i.sex = False
                            j.sex = False
                            break
            if i.count > lifeZ or i.old <= 0:
                zvery.remove(i)
                break
            nx, ny = i.nextStep()
            #print(i.move, nx, ny, i.x, i.y)
            if not isZvery(nx, ny):
                i.x = nx
                i.y = ny
            #print (i.x, i.y)
        cells2 = [[0 for j in range(len(cells[0]))] for i in range(len(cells))]
        for i in range(len(cells)):
            for j in range(len(cells[0])):
                if cells[i][j] > 0:
                    cells2[i][j] = 1
                    if not random.random() < lifeTr:
                        break
                    r = random.randint(1, 4)
                    try :
                        if r == 1 and i > 0:
                            cells2[i - 1][j] = 1
                        elif r == 2 and i < len(cells):
                            cells2[i + 1][j] = 1
                        elif r == 3 and j > 0:
                            cells2[i][j - 1] = 1
                        elif r == 4 and j < len(cells[i]):
                            cells2[i][j + 1] = 1
                    except:
                        sl = sleepTime
        cells = cells2
        printScr()
        pause = True
        sl = sleepTime
        con += 1
    else:
        sl -= 1
    for event in p.event.get():
        if event.type == p.QUIT:
            p.quit()
            exit(0)

        if event.type == p.KEYDOWN:
            keys = p.key.get_pressed()
            if keys[p.K_SPACE]:
                pause = not pause
        if event.type == p.MOUSEBUTTONDOWN:
            m = p.mouse.get_pos()
            cells[m[0] // pixel][m[1] // pixel] = not cells[m[0] // pixel][m[1] // pixel]
        continue