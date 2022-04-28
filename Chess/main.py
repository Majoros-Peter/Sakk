import pygame, time

pygame.init()


##################################################################################################################################################################################################################


black, green, light_green, brown, white, red = (0, 0, 0), (0, 100, 0), (0, 145, 0), (165, 42, 42), (245, 222, 179), (255, 69, 0)

betuk = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']
fekete_babu_nevek = ['Bástya', 'Futó', 'Huszár', 'Vezér', 'Király', 'Huszár', 'Futó', 'Bástya', 'Gyalog', 'Gyalog', 'Gyalog', 'Gyalog', 'Gyalog', 'Gyalog', 'Gyalog', 'Gyalog']
feher_babu_nevek = ['Gyalog', 'Gyalog', 'Gyalog', 'Gyalog', 'Gyalog', 'Gyalog', 'Gyalog', 'Gyalog', 'Bástya', 'Futó', 'Huszár', 'Vezér', 'Király', 'Huszár', 'Futó', 'Bástya']
fekete_idk = ['a8', 'b8', 'c8', 'd8', 'e8', 'f8', 'g8', 'h8', 'a7', 'b7', 'c7', 'd7', 'e7', 'f7', 'g7', 'h7']
feher_idk = ['a2', 'b2', 'c2', 'd2', 'e2', 'f2', 'g2', 'h2', 'a1', 'b1', 'c1', 'd1', 'e1', 'f1', 'g1', 'h1']
feher_babuk, fekete_babuk = [], []

pygame.display.set_caption("Sakk")
WIDTH, HEIGHT = 1920, 1010
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
CENTERX, CENTERY = WIDTH / 2, HEIGHT / 2

sizes, text_position, map_colors, map_ids, mezok = [], [], [], [], []
for col in range(8):
    szin_sor = []
    for row in range(8):
        text_position.append((CENTERX / 1.75 + row * (HEIGHT/10), CENTERY / 4 + col * (HEIGHT/10)))
        sizes.append((CENTERX / 1.75 + row * (HEIGHT/10), CENTERY / 4 + col * (HEIGHT/10), (HEIGHT/10), (HEIGHT/10)))
        map_ids.append(betuk[row] + str(8-col))
        if (col % 2 == 0 and row % 2 == 0) or (col % 2 == 1 and row % 2 == 1):
            szin_sor.append(white)
        else:
            szin_sor.append(brown)
    map_colors.append(szin_sor)

font = pygame.font.Font('freesansbold.ttf', 20)
uj_jatek_text = font.render("Új játék", True, black)
uj_jatek_text_hover = font.render("Új játék", True, white)
textRect_uj_jatek = uj_jatek_text.get_rect()
uj_jatek_keret = pygame.draw.rect(WIN, black, ((CENTERX / 4), CENTERY, 150, 55))

lephet, ellenseg = ['', []], []
turn = 'white'
FPS = 60


##################################################################################################################################################################################################################


class Mezo:
    def __init__(self, id, color, size, text_position):
        self.id = id
        self.color = color
        self.size = size
        self.text = font.render(self.id, True, black)
        self.t_pos = text_position
        self.terulet = pygame.draw.rect(WIN, self.color, self.size)

    def build(self, child=None):
        self.child = child

        if self.id in ellenseg:
            pygame.draw.rect(WIN, red, self.size, False)
            WIN.blit(self.text, self.t_pos)
            if self.terulet.collidepoint(pygame.mouse.get_pos()):
                if pygame.mouse.get_pressed()[0]:
                    time.sleep(0.1)
                    self.on_click(True)
        elif self.id in lephet[1]:
            pygame.draw.rect(WIN, light_green, self.size, False)
            WIN.blit(self.text, self.t_pos)
            if self.terulet.collidepoint(pygame.mouse.get_pos()):
                if pygame.mouse.get_pressed()[0]:
                    time.sleep(0.1)
                    self.on_click()
        else:
            pygame.draw.rect(WIN, self.color, self.size, False)
            WIN.blit(self.text, self.t_pos)

    def on_click(self, remove_piece=False):
        global lephet, turn, ellenseg
        if turn == "white":
            if remove_piece:
                for babu in fekete_babuk:
                    if babu.id == self.id:
                        fekete_babuk.remove(babu)
            for babu in feher_babuk:
                if babu.id == lephet[0]:
                    turn = 'black'
                    break
        else:
            if remove_piece:
                for babu in feher_babuk:
                    if babu.id == self.id:
                        feher_babuk.remove(babu)
            for babu in fekete_babuk:
                if babu.id == lephet[0]:
                    turn = 'white'
                    break
        babu.id, babu.position, lephet, ellenseg = self.id, sizes[betuk.index(self.id[0]) + (8 - int(self.id[1])) * 8], ['', []], []
        babu.terulet, babu.text = pygame.draw.rect(WIN, babu.color, babu.position), font.render(babu.id, True, black)


class Babu:
    def __init__(self, id, color, type, position):
        self.id = id
        self.color = color
        self.type = type
        self.position = position
        self.img = pygame.image.load('Images/' + self.color + '/' + self.type + '.png')
        self.text = font.render(self.id, True, black)
        self.terulet = pygame.draw.rect(WIN, self.color, self.position)

    def build(self, size):
        if self.terulet.collidepoint(pygame.mouse.get_pos()) and turn == self.color:
            pygame.draw.rect(WIN, light_green, size, False)
            WIN.blit(self.text, self.position)
            if pygame.mouse.get_pressed()[0]:
                time.sleep(0.3)
                self.on_click()
        WIN.blit(self.img, self.position)

    def on_click(self):
        lephet.clear()
        if self.type == "Gyalog":
            self.gyalog()
        if self.type == "Bástya":
            self.bastya()
        if self.type == "Futó":
            self.futo()
        if self.type == "Huszár":
            self.huszar()
        if self.type == "Vezér":
            self.vezer()
        if self.type == "Király":
            self.kiraly()

    def gyalog(self):
        global lephet, ellenseg
        x, y, lephet, ellenseg = betuk.index(self.id[0]), int(self.id[1]), [self.id, []], []
        if self.color == 'white':
            if self.id.endswith('2'):
                test_1([x, y+2])
            test_1([x-1, y+1])
            test_1([x+1, y+1])
            test_1([x, y+1])
        else:
            if self.id.endswith('7'):
                test_1([x, y-2])
            test_1([x-1, y-1])
            test_1([x+1, y-1])
            test_1([x, y-1])
        lephet[1] = test_2(lephet)

    def bastya(self):
        global lephet, ellenseg
        x, y, lephet, ellenseg = betuk.index(self.id[0]), int(self.id[1]), [self.id, []], []
        for index in range(1, 8):
            if test_1([x + index, y]):
                break
        for index in range(1, 8):
            if test_1([x - index, y]):
                break
        for index in range(1, 8):
            if test_1([x, y - index]):
                break
        for index in range(1, 8):
            if test_1([x, y + index]):
                break
        lephet[1] = test_2(lephet)

    def futo(self):
        global lephet, ellenseg
        x, y, lephet, ellenseg = betuk.index(self.id[0]), int(self.id[1]), [self.id, []], []
        for index in range(1, 8):
            if test_1([x + index, y + index]):
                break
        for index in range(1, 8):
            if test_1([x + index, y - index]):
                break
        for index in range(1, 8):
            if test_1([x - index, y + index]):
                break
        for index in range(1, 8):
            if test_1([x - index, y - index]):
                break
        lephet[1] = test_2(lephet)

    def huszar(self):
        global lephet, ellenseg
        x, y, lephet, ellenseg = betuk.index(self.id[0]), int(self.id[1]), [self.id, []], []
        test_1([x + 2, y + 1])
        test_1([x + 2, y - 1])
        test_1([x - 2, y + 1])
        test_1([x - 2, y - 1])
        test_1([x + 1, y + 2])
        test_1([x + 1, y - 2])
        test_1([x - 1, y + 2])
        test_1([x - 1, y - 2])
        lephet[1] = test_2(lephet)

    def vezer(self):
        global lephet, ellenseg
        x, y, lephet, ellenseg = betuk.index(self.id[0]), int(self.id[1]), [self.id, []], []
        for index in range(8):
            if test_1([x + index, y + index]):
                break
        for index in range(8):
            if test_1([x + index, y - index]):
                break
        for index in range(8):
            if test_1([x - index, y + index]):
                break
        for index in range(8):
            if test_1([x - index, y - index]):
                break
        for index in range(8):
            if test_1([index, y]):
                break
        for index in range(8):
            if test_1([x, index + 1]):
                break
        lephet[1] = test_2(lephet)

    def kiraly(self):
        global lephet, ellenseg
        x, y, lephet, ellenseg = betuk.index(self.id[0]), int(self.id[1]), [self.id, []], []
        test_1([x + 1, y + 1])
        test_1([x + 1, y - 1])
        test_1([x + 1, y])
        test_1([x - 1, y + 1])
        test_1([x - 1, y - 1])
        test_1([x - 1, y])
        test_1([x, y + 1])
        test_1([x, y - 1])
        lephet[1] = test_2(lephet)


class Button:
    def __init__(self, color, size, frame, border_radius, textRect, text_position, text):
        self.color = color
        self.size = size
        self.frame = frame
        self.br = border_radius
        self.textRect = textRect
        self.t_pos = text_position
        self.text = text

    def build(self, terulet, hover_keret, hover_text):
        global lephet, turn
        pygame.draw.rect(WIN, self.color, self.size, self.frame, self.br)
        pygame.draw.rect(WIN, black, self.size, 2, self.br)
        WIN.blit(self.text, self.t_pos)
        if terulet.collidepoint(pygame.mouse.get_pos()):
            pygame.draw.rect(WIN, self.color, self.size, hover_keret, self.br)
            WIN.blit(hover_text, self.t_pos)
            pygame.draw.rect(WIN, black, self.size, 2, self.br)
            if pygame.mouse.get_pressed()[0]:
                time.sleep(0.1)
                create_babuk()
                lephet, turn = ['', []], 'white'


##################################################################################################################################################################################################################
uj_jatek_gomb = Button(light_green, (CENTERX / 4, CENTERY, 150, 55), False, 10, textRect_uj_jatek, (CENTERX / 3.5, CENTERY * 1.02), uj_jatek_text)


def test_1(id):
    global lephet
    if 8 > id[0] > -1 and 0 < id[1] < 9:
        for mezo in mezok:
            if mezo.id == betuk[id[0]] + str(id[1]):
                if mezo.child == None:
                    lephet[1].append(betuk[id[0]] + str(id[1]))
                    return False
                elif mezo.child != turn:
                    lephet[1].append(betuk[id[0]] + str(id[1]))
                    ellenseg.append(betuk[id[0]] + str(id[1]))
                return True


def test_2(lista):
    for id in lista[1]:
        if id == lista[0]:
            lista[1].remove(id)
    for mezo in mezok:
        if mezo.id in lista[1] and mezo.child == turn:
            lista[1].remove(mezo.id)
    return lista[1]


def child(col, row):
    for babu in fekete_babuk:
        if babu.id == map_ids[col * 8 + row]:
            return babu.color

    for babu in feher_babuk:
        if babu.id == map_ids[col * 8 + row]:
            return babu.color
    return None


def create_babuk():
    fekete_babuk.clear()
    feher_babuk.clear()
    for index in range(8):
        feher_babuk.append(Babu(feher_idk[index], 'white', feher_babu_nevek[index], sizes[6 * 8 + index]))
        feher_babuk.append(Babu(feher_idk[8 + index], 'white', feher_babu_nevek[8 + index], sizes[7 * 8 + index]))
        fekete_babuk.append(Babu(fekete_idk[index], 'black', fekete_babu_nevek[index], sizes[index]))
        fekete_babuk.append(Babu(fekete_idk[8 + index], 'black', fekete_babu_nevek[8 + index], sizes[8 + index]))


def tabla(first=False):
    for col in range(8):
        for row in range(8):
            index = col * 8 + row

            if first:
                mezok.append((Mezo(map_ids[col * 8 + row], map_colors[col][row], sizes[index], text_position[index])))

            mezok[index].build(child(col, row))


def draw():
    WIN.fill(green)
    tabla()

    for babu in fekete_babuk:
        babu.build(sizes[map_ids.index(babu.id)])
    for babu in feher_babuk:
        babu.build(sizes[map_ids.index(babu.id)])


    uj_jatek_gomb.build(uj_jatek_keret, False, uj_jatek_text_hover)
    pygame.display.update()


def main():

    clock = pygame.time.Clock()
    run = True
    create_babuk()
    tabla(True)

    while run:
        draw()
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()


main()
