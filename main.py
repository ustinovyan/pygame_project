from sprites import *
from levels import *


def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    # если файл не существует, то выходим
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    pygame_image = pygame.image.load(fullname)
    if colorkey is not None:
        pygame_image = pygame_image.convert()
        if colorkey == -1:
            colorkey = pygame_image.get_at((0, 0))
        pygame_image.set_colorkey(colorkey)
    else:
        pygame_image = pygame_image.convert_alpha()
    return pygame_image


all_sprites = pygame.sprite.Group()
tiles_group = pygame.sprite.Group()
player_group = pygame.sprite.Group()

if __name__ == '__main__':
    pygame.init()

    # Размер экрана, а также иконка и название приложения
    pygame.display.set_caption(CAPTION)
    icon = pygame.image.load(ICON_IMAGE)
    pygame.display.set_icon(icon)

    # Создание дисплея, заднего фона и менеджера pygame_gui

    screen = pygame.display.set_mode(SIZE)  # screen = pygame.display.set_mode((size), pygame.FULLSCREEN)

    # background = pygame.transform.scale(pygame.image.load('data/town.png').convert(), SIZE)

    background = pygame.Surface(SIZE)  # Заменить на вышестоящую строчку
    background.fill(pygame.Color(WHITE))  # Заменить на вышестоящую строчку

    manager = pygame_gui.UIManager(SIZE)

    clock = pygame.time.Clock()

    player_x_pos = SCREEN_WIDTH // 3
    player_y_pos = SCREEN_HEIGHT - PLAYER_HEIGHT - 100

    hero = Player(player_x_pos, player_y_pos)  # создаем героя по (x,y) координатам
    entities = pygame.sprite.Group()  # Все объекты
    platforms = []  # то, во что мы будем врезаться или опираться
    entities.add(hero)

    running = True
    make_jump = press_left = press_right = False
    while running:
        time_delta = clock.tick(FPS) / 1000.0
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                confirmation_dialog = pygame_gui.windows.UIConfirmationDialog(
                    rect=pygame.Rect((250, 200), (300, 200)),
                    manager=manager,
                    window_title='Подтверждение',
                    action_long_desc='Вы уверены, что хотите выйти?',
                    action_short_name='OK',
                    blocking=True
                )
            if event.type == pygame.USEREVENT:
                if event.user_type == pygame_gui.UI_CONFIRMATION_DIALOG_CONFIRMED:
                    running = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                make_jump = True
            if event.type == pygame.KEYDOWN and event.key == pygame.K_LEFT:
                press_left = True
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RIGHT:
                press_right = True
            if event.type == pygame.KEYUP and event.key == pygame.K_RIGHT:
                press_right = False
            if event.type == pygame.KEYUP and event.key == pygame.K_LEFT:
                press_left = False
            if event.type == pygame.KEYUP and event.key == pygame.K_SPACE:
                make_jump = False

            manager.process_events(event)

        manager.update(time_delta)
        # Отрисовка фона
        screen.blit(background, (0, 0))
        #
        #
        #
        x = y = 0  # координаты
        for row in level:  # вся строка
            for col in row:  # каждый символ
                if col == "#":
                    pf = Platform(x, y)
                    entities.add(pf)
                    platforms.append(pf)

                x += PLATFORM_WIDTH  # блоки платформы ставятся на ширине блоков
            y += PLATFORM_HEIGHT  # то же самое и с высотой
            x = 0  # на каждой новой строчке начинаем с нуля
        #
        #
        #
        hero.update(press_left, press_right, make_jump, platforms)  # передвижение
        entities.draw(screen)  # отображение
        manager.draw_ui(screen)
        pygame.display.update()
    pygame.quit()
