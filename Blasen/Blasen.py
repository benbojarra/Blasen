import pygame
from pygame.constants import MOUSEBUTTONDOWN, MOUSEBUTTONUP
from pygame.version import PygameVersion
import os
from random import randint

class Settings():
    window = {'width':700, 'height':800}
    window_width = 700
    window_height = 800
    path_file = os.path.dirname(os.path.abspath(__file__))
    path_image = os.path.join(path_file, "images")
    inner_rect = pygame.Rect(20, 20, window['width'] - 40, window['height'] - 40)
    fps = 60
    caption = "Blasen"
    max_nof_blasen = 5
    punktestand = 0
    hit = False

class Background(object):
    def __init__(self, filename) -> None:
        self.image = pygame.image.load(os.path.join(Settings.path_image, filename)).convert()
        self.image = pygame.transform.scale(self.image, (Settings.window_width, Settings.window_height))

    def draw(self, screen):
        screen.blit(self.image, (0, 0))

class Cursor(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image_orig = pygame.image.load(os.path.join(Settings.path_image, "Nadel.png")).convert_alpha()
        self.image = self.image_orig
        self.image = pygame.transform.scale(self.image, (20, 20))
        self.rect = self.image.get_rect()
        self.scale = {'width':self.rect.width, 'height':self.rect.height}

    def update(self):
        if self.rect.left < Settings.inner_rect.left:
            self.rect.left = Settings.inner_rect.left
        if self.rect.right > Settings.inner_rect.right:
            self.rect.right = Settings.inner_rect.right
        if self.rect.top < Settings.inner_rect.top:
            self.rect.top = Settings.inner_rect.top
        if self.rect.bottom > Settings.inner_rect.bottom:
            self.rect.bottom = Settings.inner_rect.bottom

        cx = self.rect.centerx
        cy = self.rect.centery
        self.image = pygame.transform.scale(self.image_orig,(self.scale['width'], self.scale['height']))

    def scale_up(self):
        self.scale['width'] += 3
        self.scale['height'] += 3

    def scale_down(self):
        self.scale['width'] -= 3
        self.scale['height'] -= 3

    def draw(self, screen):
        screen.blit(self.image, self.rect)

class Blase(pygame.sprite.Sprite):
    def __init__(self) -> None:
        super().__init__()
        self.image_orig = pygame.image.load(os.path.join(Settings.path_image, "Blase.png")).convert_alpha()
        self.image = self.image_orig
        self.image = pygame.transform.scale(self.image, (10, 10))
        self.rect = self.image.get_rect()
        self.rect.centerx = randint(50, 650)
        self.rect.centery = randint(50, 750)
        self.scale = {'width':self.rect.width, 'height':self.rect.height}
        self.is_to_remove = False

    def update(self):
        cx = self.rect.centerx
        cy = self.rect.centery
        self.image = pygame.transform.scale(self.image_orig,(self.scale['width'], self.scale['height']))

    def scale_up(self):
        self.scale['width'] += 1
        self.scale['height'] += 1

    def draw(self, screen):
        screen.blit(self.image, self.rect)

class Losescreen(object):
    def __init__(self, filename) -> None:
        self.image = pygame.image.load(os.path.join(Settings.path_image, filename)).convert()
        self.image = pygame.transform.scale(self.image, (Settings.window_width, Settings.window_height))
        self.lose = 500

    def draw(self, screen):
        screen.blit(self.image, (self.lose, 0))

class Game(object):
    def __init__(self) -> None:
        super().__init__()
        os.environ['SDL_VIDEO_WINDOW_POS'] = "50,30"
        pygame.init()
        pygame.display.set_caption(Settings.caption)
        self.font = pygame.font.Font(pygame.font.get_default_font(), 24)
        self.screen = pygame.display.set_mode((Settings.window_width,Settings.window_height))
        self.clock = pygame.time.Clock()
        self.timer_stamp = pygame.time.get_ticks()
        self.timer_duration = 500
        self.running = False
        self.background = Background("Hintergrund.png")
        #self.losescreen = Losescreen("Hintergrund2.png")
        self.nadel = pygame.sprite.GroupSingle(Cursor())
        self.all_blasen = pygame.sprite.Group()

    def run(self):
        self.running = True
        while self.running:
            self.clock.tick(Settings.fps)
            self.nadel.sprite.rect.centerx, self.nadel.sprite.rect.centery = pygame.mouse.get_pos()
            pygame.mouse.set_visible(not Settings.inner_rect.collidepoint(self.nadel.sprite.rect.centerx, self.nadel.sprite.rect.centery))
            self.watch_for_events()
            self.update()
            self.draw()

        pygame.quit()

    def draw(self):
        self.background.draw(self.screen)
        self.all_blasen.draw(self.screen)
        self.nadel.draw(self.screen)
        #self.losescreen.draw(self.screen)
        text_surface_punktestand = self.font.render("Punktestand: {0}".format(Settings.punktestand), True, (0, 0, 0))
        self.screen.blit(text_surface_punktestand, dest=(10, 10)) 
        pygame.display.flip()

    def check_for_collision(self):
        pygame.sprite.groupcollide(self.all_blasen, self.nadel, True, False)

    def mehr_blasen(self):
        if pygame.time.get_ticks() >= self.timer_stamp + self.timer_duration:
            if len(self.all_blasen) < Settings.max_nof_blasen:
                self.blase = Blase()
                self.all_blasen.add(self.blase)
                self.timer_stamp = pygame.time.get_ticks()

    def update(self):
        self.mehr_blasen()
        self.all_blasen.update()
        self.nadel.update()

    def watch_for_events(self):
        for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.running = False
                elif event.type == MOUSEBUTTONDOWN:
                    if event.button == 1:
                        self.nadel.sprite.scale_down()
                        self.check_for_collision()
                    if event.button == 3:
                        self.all_blasen.sprite.scale_up()
                elif event.type == MOUSEBUTTONUP:
                    if event.button == 1:
                        self.nadel.sprite.scale_up()

if __name__ == "__main__":

    game = Game()
    game.run()