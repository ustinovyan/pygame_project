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
        self.dy = -(target.rect.y + target.rect.h - SCREEN_HEIGHT + 40)


class Game:
    SPLASH = 0
    START = 1
    PLAYING = 2
    PAUSED = 3
    LEVEL_COMPLETED = 4
    GAME_OVER = 5

    def __init__(self):
        # Размер экрана, а также иконка и название приложения
        pygame.display.set_caption(CAPTION)
        icon = pygame.image.load(ICON_IMAGE)
        pygame.display.set_icon(icon)

        self.running = True
        self.playing = True
        self.make_jump = self.press_left = self.press_right = self.make_hit = False
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

    def new(self):
        self.all_sprites = pygame.sprite.Group()  # Все объекты
        self.platforms = []  # то, во что мы будем врезаться или опираться
        self.coins = pygame.sprite.Group()  # Монеты
        self.enemies = pygame.sprite.Group()  # Противники
        self.flag = pygame.sprite.Group()  # Флаг(цель уровня)
        self.spikes = pygame.sprite.Group()  # Шипы
        self.food = pygame.sprite.Group()

        self.level_completed = False

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
                elif col == "p":
                    self.hero = Player(x, y)
                elif col == "e":
                    enemy = Enemy(x, y)
                    self.all_sprites.add(enemy)
                    self.enemies.add(enemy)
                elif col == "f":
                    flag = Target(x, y)
                    self.flag.add(flag)
                    self.all_sprites.add(flag)
                elif col == "s":
                    spikes = DangerPlatform(x, y)
                    self.all_sprites.add(spikes)
                    self.spikes.add(spikes)
                elif col == "h":
                    food = Food(x, y)
                    self.all_sprites.add(food)
                    self.food.add(food)

                x += PLATFORM_WIDTH  # блоки платформы ставятся на ширине блоков
            y += PLATFORM_HEIGHT  # то же самое и с высотой
            x = 0  # на каждой новой строчке начинаем с нуля

        self.all_sprites.add(self.hero)
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
        score_text = FONT_INFO.render("Score: " + str(self.hero.score), 1, BLUE)

        surface.blit(score_text, (SCREEN_WIDTH - score_text.get_width() - 32, 32))
        surface.blit(hearts_text, (32, 32))

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

                elif event.key == pygame.K_e:
                    self.make_hit = True

                elif event.key == pygame.K_SPACE:
                    self.make_jump = True

                elif event.key == pygame.K_ESCAPE:
                    if self.stage == Game.PLAYING:
                        self.stage = Game.PAUSED
                        pygame.mixer.music.pause()
                    elif self.stage == Game.PAUSED:
                        self.stage = Game.PLAYING
                        pygame.mixer.music.unpause()

                elif event.key == pygame.K_r:
                    if self.stage == Game.GAME_OVER or self.stage == Game.LEVEL_COMPLETED:
                        self.stage = Game.PLAYING
                        play_music()
                        self.new()
                        self.hero.respawn()

            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_SPACE:
                    self.make_jump = False

                elif event.key == pygame.K_e:
                    self.make_hit = False

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
        if self.stage == Game.PLAYING or self.stage == Game.SPLASH:
            self.hero.update(self.press_left, self.press_right, self.make_jump, self.platforms, self.enemies,
                             self.coins, self.flag, self.make_hit, self.spikes, self.food)
            self.coins.update()
            self.flag.update()
            self.enemies.update(self.platforms, self.hero, self.stage)
            # изменяем ракурс камеры
            camera.update(self.hero)
            # обновляем положение всех спрайтов
            for sprite in self.all_sprites:
                camera.apply(sprite)
        pygame.display.update()
        if self.hero.level_completed:
            self.level_completed = True

        if self.level_completed:
            self.stage = Game.LEVEL_COMPLETED
            pygame.mixer.music.stop()

        elif self.hero.hearts == 0:
            self.stage = Game.GAME_OVER
            pygame.mixer.music.stop()

    def draw(self):
        self.screen.blit(self.background, (0, 0))
        self.all_sprites.draw(self.screen)  # отображение
        self.display_stats(self.screen)

        if self.stage == Game.SPLASH:
            self.display_splash(self.screen)
        elif self.stage == Game.START:
            self.display_message(self.screen, "Ready?!!!", "Press any key to start.")
        elif self.stage == Game.PAUSED:
            self.display_message(self.screen, "Game paused!", "press Esc to continue.")
        elif self.stage == Game.LEVEL_COMPLETED:
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
