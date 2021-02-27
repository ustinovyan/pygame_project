from sprites import *
from levels import *

# Используемые шрифты
FONT_CAPTION = pygame.font.Font("fonts/title.ttf", 72)
FONT_INFO = pygame.font.Font("fonts/info.ttf", 32)
FONT_START = pygame.font.Font("fonts/info.ttf", 64)


class Camera:
    # зададим начальный сдвиг камеры
    def __init__(self):
        self.dx = 0
        self.dy = 0

    # сдвинуть объект obj на смещение камеры
    def apply(self, obj):
        obj.rect.x += self.dx
        obj.rect.y += self.dy

    # позиционировать камеру на объекте target
    def update(self, target):
        self.dx = -(target.rect.x + target.rect.w // 2 - SCREEN_WIDTH // 2)
        self.dy = -(target.rect.y + target.rect.h - SCREEN_HEIGHT + 100)


class Game:
    SPLASH = 0
    START = 1
    PLAYING = 2
    PAUSED = 3
    LEVEL_COMPLETED = 4
    GAME_OVER = 5
    VICTORY = 6

    def __init__(self):
        # Размер экрана, а также иконка и название приложения
        pygame.display.set_caption(CAPTION)
        icon = pygame.image.load(ICON_IMAGE)
        pygame.display.set_icon(icon)

        self.running = True
        self.playing = True
        self.make_jump = self.press_left = self.press_right = False
        self.stage = Game.SPLASH

        # Создание дисплея, заднего фона и менеджера pygame_gui

        self.screen = pygame.display.set_mode(SIZE)  # screen = pygame.display.set_mode((SIZE), pygame.FULLSCREEN)

        self.background = pygame.transform.scale(pygame.image.load('data/background/fon1.jpg').convert(), SIZE)
        # self.background_images = load_images(path='data/background', size=SIZE)
        # self.cur_background = 0
        # self.last_update = pygame.time.get_ticks()

        # self.background = pygame.Surface(SIZE)  # Заменить на вышестоящую строчку
        # self.background.fill(pygame.Color(WHITE))  # Заменить на вышестоящую строчку

        self.manager = pygame_gui.UIManager(SIZE)

        self.clock = pygame.time.Clock()
        self.time_delta = self.clock.tick(FPS) / 1000.0

        self.player_x_pos = SCREEN_WIDTH // 3
        self.player_y_pos = SCREEN_HEIGHT - PLAYER_HEIGHT - 100

    def new(self):
        self.hero = Player(self.player_x_pos, self.player_y_pos)  # создаем героя по (x,y) координатам
        self.all_sprites = pygame.sprite.Group()  # Все объекты
        self.platforms = []  # то, во что мы будем врезаться или опираться
        self.coins = pygame.sprite.Group()  # Монеты
        self.all_sprites.add(self.hero)

        x = y = 0  # координаты
        for row in level:  # вся строка
            for col in row:  # каждый символ
                if col == "#":
                    pf = Platform(x, y)
                    self.all_sprites.add(pf)
                    self.platforms.append(pf)
                elif col == "c":
                    coin = Coin(x, y)
                    self.all_sprites.add(coin)
                    self.coins.add(coin)
                x += PLATFORM_WIDTH  # блоки платформы ставятся на ширине блоков
            y += PLATFORM_HEIGHT  # то же самое и с высотой
            x = 0  # на каждой новой строчке начинаем с нуля

        self.run()

    def run(self):
        while self.playing:
            self.clock.tick()
            self.manager.update(self.time_delta)
            self.events()
            self.update()
            self.draw()

    def display_splash(self, surface):
        line1 = FONT_CAPTION.render(CAPTION, 1, BLUE)
        line2 = FONT_INFO.render("Press any key to start.", 1, BLACK)

        x1 = SCREEN_WIDTH / 2 - line1.get_width() / 2
        y1 = SCREEN_HEIGHT / 3 - line1.get_height() / 2

        x2 = SCREEN_WIDTH / 2 - line2.get_width() / 2
        y2 = y1 + line1.get_height() + 16

        surface.blit(line1, (x1, y1))
        surface.blit(line2, (x2, y2))

    def display_message(self, surface, primary_text, secondary_text):
        line1 = FONT_START.render(primary_text, 1, BLUE)
        line2 = FONT_INFO.render(secondary_text, 1, BLUE)

        x1 = SCREEN_WIDTH / 2 - line1.get_width() / 2
        y1 = SCREEN_HEIGHT / 3 - line1.get_height() / 2

        x2 = SCREEN_WIDTH / 2 - line2.get_width() / 2
        y2 = y1 + line1.get_height() + 16

        surface.blit(line1, (x1, y1))
        surface.blit(line2, (x2, y2))

    def display_stats(self, surface):
        hearts_text = FONT_INFO.render("Hearts: " + str(self.hero.hearts), 1, BLUE)
        lives_text = FONT_INFO.render("Lives: " + str(self.hero.lives), 1, BLUE)
        score_text = FONT_INFO.render("Score: " + str(self.hero.score), 1, BLUE)

        surface.blit(score_text, (SCREEN_WIDTH - score_text.get_width() - 32, 32))
        surface.blit(hearts_text, (32, 32))
        surface.blit(lives_text, (32, 64))

    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                confirmation_dialog = pygame_gui.windows.UIConfirmationDialog(
                    rect=pygame.Rect((SCREEN_WIDTH // 3, SCREEN_HEIGHT // 3), (300, 200)),
                    manager=self.manager,
                    window_title='Подтверждение',
                    action_long_desc='Вы уверены, что хотите выйти?',
                    action_short_name='OK',
                    blocking=True
                )
            if event.type == pygame.USEREVENT:
                if event.user_type == pygame_gui.UI_CONFIRMATION_DIALOG_CONFIRMED:
                    if self.playing:
                        self.playing = False
                    self.running = False

            elif event.type == pygame.KEYDOWN:
                if self.stage == Game.SPLASH or self.stage == Game.START:
                    self.stage = Game.PLAYING
                    play_music()

                elif event.key == pygame.K_SPACE:
                    self.make_jump = True
            elif event.type == pygame.KEYUP:
                if event.type == pygame.KEYUP and event.key == pygame.K_SPACE:
                    self.make_jump = False

            self.manager.process_events(event)

        pressed = pygame.key.get_pressed()

        if self.stage == Game.PLAYING:
            if pressed[pygame.K_LEFT]:
                self.press_left = True
            elif pressed[pygame.K_RIGHT]:
                self.press_right = True
            else:
                self.press_right = self.press_left = False

    def update(self):
        self.hero.update(self.press_left, self.press_right, self.make_jump, self.platforms)  # передвижение
        self.hero.process_coins(self.coins)
        self.coins.update()
        # изменяем ракурс камеры
        camera.update(self.hero)
        # обновляем положение всех спрайтов
        for sprite in self.all_sprites:
            camera.apply(sprite)
        pygame.display.update()

    def draw(self):
        # now = pygame.time.get_ticks()
        # if now - self.last_update >= FPS * 20:
        #     self.last_update = now
        #     self.cur_background += 1
        # if self.cur_background >= len(self.background_images):
        #     self.cur_background = 0
        # self.image = self.background_images[self.cur_background]

        self.screen.blit(self.background, (0, 0))
        self.all_sprites.draw(self.screen)  # отображение
        self.display_stats(self.screen)

        if self.stage == Game.SPLASH:
            self.display_splash(self.screen)
        elif self.stage == Game.START:
            self.display_message(self.screen, "Ready?!!!", "Press any key to start.")
        elif self.stage == Game.PAUSED:
            pass
        elif self.stage == Game.LEVEL_COMPLETED:
            self.display_message(self.screen, "Level Complete", "Press any key to continue.")
        elif self.stage == Game.VICTORY:
            self.display_message(self.screen, "You Win!", "Press 'R' to restart.")
        elif self.stage == Game.GAME_OVER:
            self.display_message(self.screen, "Game Over", "Press 'R' to restart.")

        self.manager.draw_ui(self.screen)


if __name__ == "__main__":
    game = Game()
    camera = Camera()
    while game.running:
        game.new()
    pygame.quit()
