import pygame
import sys

# Inicjalizacja Pygame
pygame.init()

# Definiowanie kolorów
BIAŁY = (255, 255, 255)
CZARNY = (0, 0, 0)
CZERWONY = (255, 0, 0)
ZIELONY = (0, 255, 0)
NIEBIESKI = (0, 0, 255)
KOLORY = {'biały': BIAŁY, 'czarny': CZARNY, 'czerwony': CZERWONY, 'zielony': ZIELONY, 'niebieski': NIEBIESKI}

# Ustawienia okna gry
SZEROKOŚĆ_OKNA = 800
WYSOKOŚĆ_OKNA = 600

# Ustawienia paletek i piłki
SZEROKOŚĆ_PALETKI = 10
WYSOKOŚĆ_PALETKI = 100
SZEROKOŚĆ_PIŁKI = 10
WYSOKOŚĆ_PIŁKI = 10

# Szybkość ruchu paletek
PRĘDKOŚĆ_PALETKI = 6

# Wybór koloru paletki
def wybierz_kolor(paletka):
    print(f"Wybierz kolor paletki {paletka}: biały, czarny, czerwony, zielony, niebieski")
    kolor = input().lower()
    if kolor in KOLORY:
        return KOLORY[kolor]
    else:
        print("Niepoprawny kolor, ustawiam biały.")
        return BIAŁY

KOLOR_LEWEJ_PALETKI = wybierz_kolor('lewej')
KOLOR_PRAWEJ_PALETKI = wybierz_kolor('prawej')

# Tworzenie okna gry
okno = pygame.display.set_mode((SZEROKOŚĆ_OKNA, WYSOKOŚĆ_OKNA))
pygame.display.set_caption("8-bitowy Ping Pong")

# Klasa reprezentująca paletkę
class Paletka(pygame.sprite.Sprite):
    def __init__(self, x, y, kolor):
        super().__init__()
        self.image = pygame.Surface([SZEROKOŚĆ_PALETKI, WYSOKOŚĆ_PALETKI])
        self.image.fill(kolor)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def move_up(self):
        if self.rect.y > 0:
            self.rect.y -= PRĘDKOŚĆ_PALETKI

    def move_down(self):
        if self.rect.y < WYSOKOŚĆ_OKNA - WYSOKOŚĆ_PALETKI:
            self.rect.y += PRĘDKOŚĆ_PALETKI

# Klasa reprezentująca piłkę
class Pilka(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface([SZEROKOŚĆ_PIŁKI, WYSOKOŚĆ_PIŁKI])
        self.image.fill(BIAŁY)
        self.rect = self.image.get_rect()
        self.rect.x = SZEROKOŚĆ_OKNA // 2
        self.rect.y = WYSOKOŚĆ_OKNA // 2
        self.speed_x = 4
        self.speed_y = 4

    def update(self):
        self.rect.x += self.speed_x
        self.rect.y += self.speed_y

        # Sprawdzanie kolizji z górną i dolną krawędzią
        if self.rect.y <= 0 or self.rect.y >= WYSOKOŚĆ_OKNA - WYSOKOŚĆ_PIŁKI:
            self.speed_y = -self.speed_y

        # Sprawdzanie kolizji z paletkami
        if pygame.sprite.spritecollide(self, paletki, False):
            self.speed_x = -self.speed_x

        # Sprawdzanie czy piłka wyleciała poza ekran
        if self.rect.x <= 0:
            global prawa_punkty
            prawa_punkty += 1
            self.reset()
        elif self.rect.x >= SZEROKOŚĆ_OKNA:
            global lewa_punkty
            lewa_punkty += 1
            self.reset()

    def reset(self):
        self.rect.x = SZEROKOŚĆ_OKNA // 2
        self.rect.y = WYSOKOŚĆ_OKNA // 2
        self.speed_x = -self.speed_x

# Tworzenie obiektów paletek i piłki
lewa_paletka = Paletka(50, WYSOKOŚĆ_OKNA // 2 - WYSOKOŚĆ_PALETKI // 2, KOLOR_LEWEJ_PALETKI)
prawa_paletka = Paletka(SZEROKOŚĆ_OKNA - 50 - SZEROKOŚĆ_PALETKI, WYSOKOŚĆ_OKNA // 2 - WYSOKOŚĆ_PALETKI // 2, KOLOR_PRAWEJ_PALETKI)
pilka = Pilka()

# Grupa sprite'ów
paletki = pygame.sprite.Group()
paletki.add(lewa_paletka)
paletki.add(prawa_paletka)

pilka_grupa = pygame.sprite.Group()
pilka_grupa.add(pilka)

# Punkty
lewa_punkty = 0
prawa_punkty = 0

# Czcionka do wyświetlania punktów
czcionka = pygame.font.Font(None, 74)

# Główna pętla gry
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Odczytanie stanu klawiszy
    keys = pygame.key.get_pressed()
    if keys[pygame.K_w]:
        lewa_paletka.move_up()
    if keys[pygame.K_s]:
        lewa_paletka.move_down()
    if keys[pygame.K_UP]:
        prawa_paletka.move_up()
    if keys[pygame.K_DOWN]:
        prawa_paletka.move_down()

    # Aktualizacja pozycji piłki
    pilka_grupa.update()

    # Rysowanie obiektów
    okno.fill(CZARNY)
    paletki.draw(okno)
    pilka_grupa.draw(okno)

    # Wyświetlanie punktów
    lewa_tekst = czcionka.render(str(lewa_punkty), True, BIAŁY)
    okno.blit(lewa_tekst, (250, 10))
    prawa_tekst = czcionka.render(str(prawa_punkty), True, BIAŁY)
    okno.blit(prawa_tekst, (SZEROKOŚĆ_OKNA - 250, 10))

    # Odświeżenie ekranu
    pygame.display.flip()

    # Ustawienie prędkości gry
    pygame.time.Clock().tick(60)

# Zakończenie Pygame
pygame.quit()
sys.exit()