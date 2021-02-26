from sprites import *
from levels import *


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
    def __init__(self):
        pygame.init()

        # Размер экрана, а также иконка и название приложения
        pygame.display.set_caption(CAPTION)
        icon = pygame.image.load(ICON_IMAGE)
        pygame.display.set_icon(icon)

        self.running = True
        self.playing = True
        self.make_jump = self.press_left = self.press_right = False

        # Создание дисплея, заднего фона и менеджера pygame_gui

        self.screen = pygame.display.set_mode(SIZE)  # screen = pygame.display.set_mode((SIZE), pygame.FULLSCREEN)

        # background = pygame.transform.scale(pygame.image.load('data/town.png').convert(), SIZE)

        self.background = pygame.Surface(SIZE)  # Заменить на вышестоящую строчку
        self.background.fill(pygame.Color(WHITE))  # Заменить на вышестоящую строчку

        self.manager = pygame_gui.UIManager(SIZE)

        self.clock = pygame.time.Clock()
        self.time_delta = self.clock.tick(FPS) / 1000.0

        self.player_x_pos = SCREEN_WIDTH // 3
        self.player_y_pos = SCREEN_HEIGHT - PLAYER_HEIGHT - 100

    def new(self):
        self.hero = Player(self.player_x_pos, self.player_y_pos)  # создаем героя по (x,y) координатам
        self.all_sprites = pygame.sprite.Group()  # Все объекты
        self.platforms = []  # то, во что мы будем врезаться или опираться
        self.all_sprites.add(self.hero)

        x = y = 0  # координаты
        for row in level:  # вся строка
            for col in row:  # каждый символ
                if col == "#":
                    pf = Platform(x, y)
                    self.all_sprites.add(pf)
                    self.platforms.append(pf)
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

            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                self.make_jump = True
            if event.type == pygame.KEYDOWN and event.key == pygame.K_LEFT:
                self.press_left = True
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RIGHT:
                self.press_right = True
            if event.type == pygame.KEYUP and event.key == pygame.K_RIGHT:
                self.press_right = False
            if event.type == pygame.KEYUP and event.key == pygame.K_LEFT:
                self.press_left = False
            if event.type == pygame.KEYUP and event.key == pygame.K_SPACE:
                self.make_jump = False

            self.manager.process_events(event)

    def update(self):
        self.hero.update(self.press_left, self.press_right, self.make_jump, self.platforms)  # передвижение
        # изменяем ракурс камеры
        camera.update(self.hero)
        # обновляем положение всех спрайтов
        for sprite in self.all_sprites:
            camera.apply(sprite)
        pygame.display.update()

    def draw(self):
        # Отрисовка фона
        self.screen.blit(self.background, (0, 0))
        self.all_sprites.draw(self.screen)  # отображение
        self.manager.draw_ui(self.screen)


if __name__ == "__main__":
    game = Game()
    camera = Camera()
    while game.running:
        game.new()
    pygame.quit()
