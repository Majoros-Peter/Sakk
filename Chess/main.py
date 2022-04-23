import pygame, time

pygame.init()


##################################################################################################################################################################################################################


black, green, light_green, brown, white = (0, 0, 0), (0, 100, 0), (0, 145, 0), (165, 42, 42), (245, 222, 179)

betuk = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']
feher_babu_nevek = ['Bástya', 'Futó', 'Huszár', 'Király', 'Vezér', 'Huszár', 'Futó', 'Bástya', 'Gyalog', 'Gyalog', 'Gyalog', 'Gyalog', 'Gyalog', 'Gyalog', 'Gyalog', 'Gyalog']
fekete_babu_nevek = ['Gyalog', 'Gyalog', 'Gyalog', 'Gyalog', 'Gyalog', 'Gyalog', 'Gyalog', 'Gyalog', 'Bástya', 'Futó', 'Huszár', 'Király', 'Vezér', 'Huszár', 'Futó', 'Bástya']
feher_babuk = []
fekete_babuk = []

pygame.display.set_caption("Sakk")
WIDTH, HEIGHT = 1920, 1010
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
CENTERX, CENTERY = WIDTH / 2, HEIGHT / 2

sizes, text_position = [], []
for col in range(8):
    for row in range(8):
        text_position.append((CENTERX / 1.75 + row * (HEIGHT/10), CENTERY / 4 + col * (HEIGHT/10)))
        sizes.append((CENTERX / 1.75 + row * (HEIGHT/10), CENTERY / 4 + col * (HEIGHT/10), (HEIGHT/10), (HEIGHT/10)))

map = [
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

FPS = 60


##################################################################################################################################################################################################################


class Mezo():
    def __init__(self, id, lephet, color, size, frame, has_child=False, text_position=None):
        self.id = id
        self.lephet = lephet
        self.color = color
        self.size = size
        self.frame = frame
        self.has_child = has_child

        font = pygame.font.Font('freesansbold.ttf', 20)
        self.text = font.render(self.id, True, black)
        self.t_pos = text_position

    def build(self, terulet, hover_keret, hover_color):
        pygame.draw.rect(WIN, self.color, self.size, self.frame)
        WIN.blit(self.text, self.t_pos)
        if terulet.collidepoint(pygame.mouse.get_pos()) and self.has_child or self.lephet:
            pygame.draw.rect(WIN, hover_color, self.size, hover_keret)
            WIN.blit(self.text, self.t_pos)


class Babu():
    def __init__(self, id, color, type, position):
        self.id = id
        self.color = color
        self.type = type
        self.position = position
        self.img = pygame.image.load('Images/' + self.color + '/' + self.type + '.png')

    def build(self):
        WIN.blit(self.img, self.position)

    def on_click(self):
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
        pass

    def bastya(self):
        pass

    def futo(self):
        pass

    def huszar(self):
        pass

    def vezer(self):
        pass

    def kiraly(self):
        pass


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


##################################################################################################################################################################################################################


def create_babuk():
    for index in range(8):
        feher_babuk.append(Babu(betuk[0] + str(index + 1), 'white', feher_babu_nevek[index], (CENTERX / 1.75 + index * (HEIGHT/10), CENTERY / 4 + 0 * (HEIGHT/10))))
        feher_babuk.append(Babu(betuk[1] + str(index + 1), 'white', feher_babu_nevek[8 + index], (CENTERX / 1.75 + index * (HEIGHT/10), CENTERY / 4 + 1 * (HEIGHT/10))))
        fekete_babuk.append(Babu(betuk[6] + str(index + 1), 'black', fekete_babu_nevek[index], (CENTERX / 1.75 + index * (HEIGHT / 10), CENTERY / 4 + 6 * (HEIGHT / 10))))
        fekete_babuk.append(Babu(betuk[7] + str(index + 1), 'black', fekete_babu_nevek[8 + index], (CENTERX / 1.75 + index * (HEIGHT / 10), CENTERY / 4 + 7 * (HEIGHT / 10))))


def tabla():
    for col in range(8):
        for row in range(8):
            has_child = False
            color = map[col][row]

            for elem_1, elem_2 in zip(feher_babuk, fekete_babuk):
                if elem_1.id == betuk[col] + str(row + 1) or elem_2.id == betuk[col] + str(row + 1):
                    has_child = True

            mezo, keret = Mezo(betuk[col] + str(row + 1), None, color, sizes[col * 8 + row], True, has_child, text_position[col * 8 + row]), pygame.draw.rect(WIN, color, sizes[col * 8 + row])
            mezo.build(keret, False, light_green)


def draw():
    WIN.fill(green)
    tabla()

    uj_jatek_gomb = Button(light_green, (CENTERX / 4, CENTERY, 150, 55), False, 10, textRect_uj_jatek, (CENTERX / 3.5, CENTERY * 1.02), uj_jatek_text)
    uj_jatek_gomb.build(uj_jatek_keret, False, uj_jatek_text_hover)

    for elem_1, elem_2 in zip(feher_babuk, fekete_babuk):
        elem_1.build()
        elem_2.build()

    pygame.display.update()


def main():

    clock = pygame.time.Clock()
    run = True

    while run:
        draw()
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()


##################################################################################################################################################################################################################


create_babuk()
main()