from settings import *


# def load_image(name, colorkey=None):
#     fullname = os.path.join('data', name)
#     # если файл не существует, то выходим
#     if not os.path.isfile(fullname):
#         print(f"Файл с изображением '{fullname}' не найден")
#         sys.exit()
#     pygame_image = pygame.image.load(fullname)
#     if colorkey is not None:
#         pygame_image = pygame_image.convert()
#         if colorkey == -1:
#             colorkey = pygame_image.get_at((0, 0))
#         pygame_image.set_colorkey(colorkey)
#     else:
#         pygame_image = pygame_image.convert_alpha()
#     return pygame_image

def load_images(path, size):
    images = []
    for i in os.listdir(path):
        img = pygame.transform.scale(pygame.image.load(path + os.sep + i).convert_alpha(), size)
        images.append(img)
    return images


class Player(sprite.Sprite):
    def __init__(self, x, y):
        sprite.Sprite.__init__(self)

        self.images_idle_right = load_images(path='data/Hero_Knight/Idle', size=(144, 144))
        self.images_idle_left = [pygame.transform.flip(image, True, False) for image in self.images_idle_right]
        self.images_right = load_images(path='data/Hero_Knight/Run', size=(144, 144))
        self.images_left = [pygame.transform.flip(image, True, False) for image in self.images_right]
        self.images_jump_right = load_images(path='data/Hero_Knight/Jump', size=(144, 144))
        self.images_jump_left = [pygame.transform.flip(image, True, False) for image in self.images_jump_right]

        self.x = 0  # скорость горизонтального перемещения. 0 - стоять на месте
        self.y = 0  # скорость вертикального перемещения

        self.onGround = False  # На земле ли я?
        self.startX = x  # Начальная позиция Х, пригодится когда будем переигрывать уровень
        self.startY = y

        try:
            if self.current_images_group:
                pass
        except Exception:
            self.current_images_group = self.images_idle_right
        self.cur_frame = 0
        self.image = self.current_images_group[self.cur_frame]
        self.rect = self.image.get_rect()

        self.last_update = pygame.time.get_ticks()

    def update(self, left, right, up, platforms):
        if up:
            if self.onGround:  # прыгаем, только когда можем оттолкнуться от земли
                self.y = -JUMP_POWER
            if self.current_images_group == self.images_idle_right or \
                    self.current_images_group == self.images_right:
                self.current_images_group = self.images_jump_right
            elif self.current_images_group == self.images_idle_left or \
                    self.current_images_group == self.images_left:
                self.current_images_group = self.images_jump_left
        if left:
            if up:
                self.current_images_group = self.images_jump_left
            else:
                self.current_images_group = self.images_left
            self.x = -MOVE_SPEED  # Лево = x- n

        if right:
            if up:
                self.current_images_group = self.images_jump_right
            else:
                self.current_images_group = self.images_right
            self.x = MOVE_SPEED  # Право = x + n

        if not (left or right):  # стоим, когда нет указаний идти
            if self.onGround:
                if self.current_images_group == self.images_left or \
                        self.current_images_group == self.images_jump_left:
                    self.current_images_group = self.images_idle_left
                elif self.current_images_group == self.images_right or \
                        self.current_images_group == self.images_jump_right:
                    self.current_images_group = self.images_idle_right
            self.x = 0

        if not self.onGround:
            self.y += GRAVITY

        self.onGround = False  # Мы не знаем, когда мы на земле((
        self.rect.y += self.y
        self.rect.y += self.y
        self.collide(0, self.y, platforms)

        self.rect.x += self.x  # переносим свои положение на xvel
        self.collide(self.x, 0, platforms)

        now = pygame.time.get_ticks()
        if now - self.last_update >= FPS:
            self.last_update = now
            self.cur_frame += 1
        if self.cur_frame >= len(self.current_images_group):
            self.cur_frame = 0
        self.image = self.current_images_group[self.cur_frame]

    def collide(self, x, y, platforms):
        for p in platforms:
            if sprite.collide_rect(self, p):  # если есть пересечение платформы с игроком

                if x > 0:  # если движется вправо
                    self.rect.right = p.rect.left  # то не движется вправо

                if x < 0:  # если движется влево
                    self.rect.left = p.rect.right  # то не движется влево

                if y > 0:  # если падает вниз
                    self.rect.bottom = p.rect.top  # то не падает вниз
                    self.onGround = True  # и становится на что-то твердое
                    self.y = 0  # и энергия падения пропадает

                if y < 0:  # если движется вверх
                    self.rect.top = p.rect.bottom  # то не движется вверх
                    self.y = 0  # и энергия прыжка пропадает
