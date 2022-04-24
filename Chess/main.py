import pygame, time

pygame.init()


##################################################################################################################################################################################################################


black, green, light_green, brown, white = (0, 0, 0), (0, 100, 0), (0, 145, 0), (165, 42, 42), (245, 222, 179)

betuk = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']
feher_babu_nevek = ['Gyalog', 'Gyalog', 'Gyalog', 'Gyalog', 'Gyalog', 'Gyalog', 'Gyalog', 'Gyalog', 'Bástya', 'Futó', 'Huszár', 'Vezér', 'Király', 'Huszár', 'Futó', 'Bástya']
fekete_babu_nevek = ['Bástya', 'Futó', 'Huszár', 'Vezér', 'Király', 'Huszár', 'Futó', 'Bástya', 'Gyalog', 'Gyalog', 'Gyalog', 'Gyalog', 'Gyalog', 'Gyalog', 'Gyalog', 'Gyalog']
feher_idk = ['g1', 'g2', 'g3', 'g4', 'g5', 'g6', 'g7', 'g8', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'h7', 'h8']
fekete_idk = ['a1', 'a2', 'a3', 'a4', 'a5', 'a6', 'a7', 'a8', 'b1', 'b2', 'b3', 'b4', 'b5', 'b6', 'b7', 'b8']
feher_babuk, fekete_babuk = [], []

pygame.display.set_caption("Sakk")
WIDTH, HEIGHT = 1920, 1010
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
CENTERX, CENTERY = WIDTH / 2, HEIGHT / 2

sizes, text_position = [], []
for col in range(8):
    for row in range(8):
        text_position.append((CENTERX / 1.75 + row * (HEIGHT/10), CENTERY / 4 + col * (HEIGHT/10)))
        sizes.append((CENTERX / 1.75 + row * (HEIGHT/10), CENTERY / 4 + col * (HEIGHT/10), (HEIGHT/10), (HEIGHT/10)))

map_colors = [
    [white, brown, white, brown, white, brown, white, brown],
    [brown, white, brown, white, brown, white, brown, white],
    [white, brown, white, brown, white, brown, white, brown],
    [brown, white, brown, white, brown, white, brown, white],
    [white, brown, white, brown, white, brown, white, brown],
    [brown, white, brown, white, brown, white, brown, white],
    [white, brown, white, brown, white, brown, white, brown],
    [brown, white, brown, white, brown, white, brown, white]
]

font = pygame.font.Font('freesansbold.ttf', 20)
uj_jatek_text = font.render("Új játék", True, black)
uj_jatek_text_hover = font.render("Új játék", True, white)
textRect_uj_jatek = uj_jatek_text.get_rect()
uj_jatek_keret = pygame.draw.rect(WIN, black, ((CENTERX / 4), CENTERY, 150, 55))

turn = 'white'
lephet = ['', []]
FPS = 60


##################################################################################################################################################################################################################


class Mezo:
    def __init__(self, id, color, size, frame, text_position):
        self.id = id
        self.color = color
        self.size = size
        self.frame = frame
        self.text = font.render(self.id, True, black)
        self.t_pos = text_position

    def build(self, terulet, hover_keret, hover_color):
        global lephet

        if self.id in lephet[1]:
            pygame.draw.rect(WIN, hover_color, self.size, hover_keret)
            WIN.blit(self.text, self.t_pos)
            if terulet.collidepoint(pygame.mouse.get_pos()):
                if pygame.mouse.get_pressed()[0]:
                    time.sleep(0.1)
                    self.on_click()
        else:
            pygame.draw.rect(WIN, self.color, self.size, hover_keret)
            WIN.blit(self.text, self.t_pos)

    def on_click(self):
        global lephet, turn
        if turn == "white":
            for elem in feher_babuk:
                if elem.id == lephet[0]:
                    babu, turn = elem, 'black'
                    break
        else:
            for elem in fekete_babuk:
                if elem.id == lephet[0]:
                    babu, turn = elem, 'white'
                    break
        index = betuk.index(self.id[0])
        babu.id, babu.position, lephet = self.id, sizes[index * 8 + int(self.id[1]) - 1], ['', []]
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

    def build(self, hover_keret, hover_color, size):
        if self.terulet.collidepoint(pygame.mouse.get_pos()) and turn == self.color:
            pygame.draw.rect(WIN, hover_color, size, hover_keret)
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
        global lephet
        y, x, lephet = betuk.index(self.id[0]), int(self.id[1]), ['', []]
        egyik = van_ellenfel(self.color)
        masik = van_azonos_szinu(self.color)
        if self.color == "white":
            if y == 6 and not (betuk[y - 2] + str(x) in egyik or betuk[y - 2] + str(x) in masik):
                lephet[1].append(betuk[y - 2] + str(x))
            for babu in fekete_babuk:
                if babu.id == betuk[y - 1] + str(x + 1):
                    lephet[1].append(betuk[y - 1] + str(x + 1))
                if babu.id == betuk[y - 1] + str(x - 1):
                    lephet[1].append(betuk[y - 1] + str(x - 1))
            lephet[1].append(betuk[y - 1] + str(x))
        else:
            if y == 1:
                lephet[1].append(betuk[y + 2] + str(x))
            for babu in feher_babuk:
                if babu.id == betuk[y + 1] + str(x + 1):
                    lephet[1].append(betuk[y + 1] + str(x + 1))
                if babu.id == betuk[y + 1] + str(x - 1):
                    lephet[1].append(betuk[y + 1] + str(x - 1))
            lephet[1].append(betuk[y + 1] + str(x))
        lephet[0] = self.id

    def bastya(self):
        global lephet
        y, x, lephet = betuk.index(self.id[0]), self.id[1], ['', []]
        for index in range(8):
            lephet[1].append(betuk[index] + x)
            lephet[1].append(betuk[y] + str(index + 1))
        lephet[1].remove(self.id)
        lephet[1].remove(self.id)
        lephet[0] = self.id

    def futo(self):
        global lephet
        y, x, lephet = betuk.index(self.id[0]), int(self.id[1]), ['', []]
        for index in range(8):
            if 8 > y + index > -1:
                if 9 > (x + index) > 0:
                    lephet[1].append(betuk[y + index] + str(x + index))
                if 9 > (x - index) > 0:
                    lephet[1].append(betuk[y + index] + str(x - index))
            if 8 > y - index > -1:
                if 9 > (x + index) > 0:
                    lephet[1].append(betuk[y - index] + str(x + index))
                if 9 > (x - index) > 0:
                    lephet[1].append(betuk[y - index] + str(x - index))
            if self.id in lephet[1]:
                lephet[1].remove(self.id)
        lephet[0] = self.id

    def huszar(self):
        global lephet
        y, x, lephet = betuk.index(self.id[0]), int(self.id[1]), ['', []]
        if 8 > y + 2 > -1:
            if 9 > x + 1 > 0:
                lephet[1].append(betuk[y + 2] + str(x + 1))
            if 9 > x - 1 > 0:
                lephet[1].append(betuk[y + 2] + str(x - 1))
        if 8 > y - 2 > -1:
            if 9 > x + 1 > 0:
                lephet[1].append(betuk[y - 2] + str(x + 1))
            if 9 > x - 1 > 0:
                lephet[1].append(betuk[y - 2] + str(x - 1))
        if 8 > y + 1 > -1:
            if 9 > x + 2 > 0:
                lephet[1].append(betuk[y + 1] + str(x + 2))
            if 9 > x - 2 > 0:
                lephet[1].append(betuk[y + 1] + str(x - 2))
        if 8 > y - 1 > -1:
            if 9 > x + 2 > 0:
                lephet[1].append(betuk[y - 1] + str(x + 2))
            if 9 > x - 2 > 0:
                lephet[1].append(betuk[y - 1] + str(x - 2))
        lephet[0] = self.id

    def vezer(self):
        global lephet
        y, x, lephet = betuk.index(self.id[0]), int(self.id[1]), ['', []]
        for index in range(8):
            if 8 > y + index > -1:
                if 9 > (x + index) > 0:
                    lephet[1].append(betuk[y + index] + str(x + index))
                if 9 > (x - index) > 0:
                    lephet[1].append(betuk[y + index] + str(x - index))
            if 8 > y - index > -1:
                if 9 > (x + index) > 0:
                    lephet[1].append(betuk[y - index] + str(x + index))
                if 9 > (x - index) > 0:
                    lephet[1].append(betuk[y - index] + str(x - index))
            lephet[1].append(betuk[index] + str(x))
            lephet[1].append(betuk[y] + str(index + 1))
            if self.id in lephet[1]:
                lephet[1].remove(self.id)
        lephet[0] = self.id

    def kiraly(self):
        global lephet
        y, x, lephet = betuk.index(self.id[0]), int(self.id[1]), ['', []]
        if 8 > y + 1 > -1:
            if 9 > x + 1 > 0:
                lephet[1].append(betuk[y + 1] + str(x + 1))
            if 9 > x - 1 > 0:
                lephet[1].append(betuk[y + 1] + str(x - 1))
            lephet[1].append(betuk[y + 1] + str(x))
        if 8 > y - 1 > -1:
            if 9 > x + 1 > 0:
                lephet[1].append(betuk[y - 1] + str(x + 1))
            if 9 > x - 1 > 0:
                lephet[1].append(betuk[y - 1] + str(x - 1))
            lephet[1].append(betuk[y - 1] + str(x))
        if 9 > x + 1 > 0:
            lephet[1].append(betuk[y] + str(x + 1))
        if 9 > x - 1 > 0:
            lephet[1].append(betuk[y] + str(x - 1))
        lephet[0] = self.id


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
        global lephet
        pygame.draw.rect(WIN, self.color, self.size, self.frame, self.br)
        self.textRect.center = self.t_pos
        pygame.draw.rect(WIN, black, self.size, 2, self.br)
        WIN.blit(self.text, self.textRect.center)
        if terulet.collidepoint(pygame.mouse.get_pos()):
            pygame.draw.rect(WIN, self.color, self.size, hover_keret, self.br)
            WIN.blit(hover_text, self.textRect.center)
            pygame.draw.rect(WIN, black, self.size, 2, self.br)
            if pygame.mouse.get_pressed()[0]:
                time.sleep(0.1)
                create_babuk()
                lephet = ['', []]



##################################################################################################################################################################################################################


def van_ellenfel(szin):
    ids = []
    if szin == 'white':
        ellenfel_lista = fekete_babuk
    else:
        ellenfel_lista = feher_babuk
    for babu in ellenfel_lista:
        ids.append(babu.id)
    return ids


def van_azonos_szinu(szin):
    ids = []
    if szin == 'white':
        ellenfel_lista = feher_babuk
    else:
        ellenfel_lista = fekete_babuk
    for babu in ellenfel_lista:
        ids.append(babu.id)
    return ids


def create_babuk():
    fekete_babuk.clear()
    feher_babuk.clear()
    for index in range(8):
        feher_babuk.append(Babu(feher_idk[index], 'white', feher_babu_nevek[index], sizes[6 * 8 + index]))
        feher_babuk.append(Babu(feher_idk[8 + index], 'white', feher_babu_nevek[8 + index], sizes[7 * 8 + index]))
        fekete_babuk.append(Babu(fekete_idk[index], 'black', fekete_babu_nevek[index], sizes[index]))
        fekete_babuk.append(Babu(fekete_idk[8 + index], 'black', fekete_babu_nevek[8 + index], sizes[8 + index]))


def tabla():
    for col in range(8):
        for row in range(8):
            mezo, keret = (Mezo(betuk[col] + str(row + 1), map_colors[col][row], sizes[col * 8 + row], True, text_position[col * 8 + row])), pygame.draw.rect(WIN, map_colors[col][row], sizes[col * 8 + row])
            mezo.build(keret, False, light_green)


def draw():
    WIN.fill(green)
    tabla()

    uj_jatek_gomb = Button(light_green, (CENTERX / 4, CENTERY, 150, 55), False, 10, textRect_uj_jatek, (CENTERX / 3.5, CENTERY * 1.02), uj_jatek_text)
    uj_jatek_gomb.build(uj_jatek_keret, False, uj_jatek_text_hover)

    for babu in fekete_babuk:
        babu.build(False, light_green, sizes[betuk.index(babu.id[0]) * 8 + int(babu.id[1]) - 1])
    for babu in feher_babuk:
        babu.build(False, light_green, sizes[betuk.index(babu.id[0]) * 8 + int(babu.id[1]) - 1])

    pygame.display.update()


def main():

    clock = pygame.time.Clock()
    run = True
    create_babuk()

    while run:
        draw()
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()


main()
