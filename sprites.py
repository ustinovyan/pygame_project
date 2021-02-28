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

def load_images(path, size):  # Загрузка всех картинок из какой-либо папки
    images = []
    for i in os.listdir(path):
        img = pygame.transform.scale(pygame.image.load(path + os.sep + i).convert_alpha(), size)
        images.append(img)
    return images


def play_sound(sound, loops=0, maxtime=0, fade_ms=0):
    if sound_on:
        sound.play(loops, maxtime, fade_ms)


def play_music():
    if sound_on:
        songs = []
        for i in os.listdir("theme_music"):
            songs.append("theme_music" + os.sep + i)
            pygame.mixer.music.load(random.choice(songs))
        pygame.mixer.music.play(-1)


class Platform(sprite.Sprite):
    def __init__(self, x, y):
        sprite.Sprite.__init__(self)
        self.image = Surface((PLATFORM_WIDTH, PLATFORM_HEIGHT))
        self.image = image.load("data/blocks/platform1.png")
        self.rect = Rect(x, y, PLATFORM_WIDTH, PLATFORM_HEIGHT)


class Player(sprite.Sprite):
    def __init__(self, x, y):
        sprite.Sprite.__init__(self)

        # Загрузка картинок для анимации героя
        self.images_idle_right = load_images(path='data/Hero_Knight/Idle', size=PLAYER_SIZE)
        self.images_idle_left = [pygame.transform.flip(image, True, False) for image in self.images_idle_right]
        self.images_right = load_images(path='data/Hero_Knight/Run', size=PLAYER_SIZE)
        self.images_left = [pygame.transform.flip(image, True, False) for image in self.images_right]
        self.images_jump_right = load_images(path='data/Hero_Knight/Jump', size=PLAYER_SIZE)
        self.images_jump_left = [pygame.transform.flip(image, True, False) for image in self.images_jump_right]

        self.x = 0  # скорость горизонтального перемещения. 0 - стоять на месте
        self.y = 0  # скорость вертикального перемещения

        self.onGround = False  # На земле ли я?

        self.score = 0
        self.lives = 3
        self.hearts = 3
        self.max_hearts = 3
        self.invincibility = 0

        try:
            if self.current_images_group:
                pass
        except Exception:
            self.current_images_group = self.images_idle_right
        self.cur_frame = 0
        self.image = self.current_images_group[self.cur_frame]
        self.rect = self.image.get_rect()

        self.rect.x = x  # Начальная позиция Х, пригодится когда будем переигрывать уровень
        self.rect.y = y

        self.last_update = pygame.time.get_ticks()

    def process_enemies(self, enemies):
        hit_list = pygame.sprite.spritecollide(self, enemies, False)

        if len(hit_list) > 0 and self.invincibility == 0:
            play_sound(HURT_SOUND)
            self.hearts -= 1
            self.invincibility = FPS * 3

    def update(self, left, right, up, platforms, enemies, coins):
        if up:
            self.rect.y += 1

            hit_list = pygame.sprite.spritecollide(self, platforms, False)

            if len(hit_list) > 0:
                self.y = -1 * JUMP_POWER
                play_sound(JUMP_SOUND)

            self.rect.y -= 1
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

        self.process_enemies(enemies)

        if self.hearts > 0:
            self.process_coins(coins)

            if self.invincibility > 0:
                self.invincibility -= 1
        else:
            self.die()

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

    def process_coins(self, coins):
        hit_list = pygame.sprite.spritecollide(self, coins, True)

        for coin in hit_list:
            play_sound(COIN_SOUND)
            self.score += coin.value

    def die(self):
        self.lives -= 1

        if self.lives > 0:
            play_sound(DIE_SOUND)
        else:
            play_sound(GAMEOVER_SOUND)


class Coin(sprite.Sprite):
    def __init__(self, x, y):
        sprite.Sprite.__init__(self)

        self.value = 1

        self.current_images_group = load_images(path='data/coin', size=COIN_SIZE)
        self.cur_frame = 0
        self.image = self.current_images_group[self.cur_frame]
        self.rect = self.image.get_rect()
        self.last_update = pygame.time.get_ticks()
        self.rect.x = x
        self.rect.y = y - COIN_HEIGHT // 2

    def update(self):
        now = pygame.time.get_ticks()
        if now - self.last_update >= FPS:
            self.last_update = now
            self.cur_frame += 1
        if self.cur_frame >= len(self.current_images_group):
            self.cur_frame = 0
        self.image = self.current_images_group[self.cur_frame]


class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y):
        sprite.Sprite.__init__(self)
        images = load_images(path='data/monsters', size=ENEMY_SIZE)
        self.image = random.choice(images)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y - ENEMY_HEIGHT // 1.5

        self.start_x = -1
        self.start_y = 0

        self.x = self.start_x
        self.y = self.start_y

    def reverse(self):
        self.x *= -1

    def move_and_process_blocks(self, blocks):
        reverse = False

        self.rect.x += self.x
        hit_list = pygame.sprite.spritecollide(self, blocks, False)

        for block in hit_list:
            if self.x > 0:
                self.rect.right = block.rect.left
                self.reverse()
            elif self.x < 0:
                self.rect.left = block.rect.right
                self.reverse()

        self.rect.y += self.y + 1
        hit_list = pygame.sprite.spritecollide(self, blocks, False)

        reverse = True

        for block in hit_list:
            if self.y >= 0:
                self.rect.bottom = block.rect.top
                self.y = 0

                if self.x > 0 and self.rect.right <= block.rect.right:
                    reverse = False

                elif self.x < 0 and self.rect.left >= block.rect.left:
                    reverse = False

            elif self.vy < 0:
                self.rect.top = block.rect.bottom
                self.vy = 0

        if reverse:
            self.reverse()

    def is_near(self, hero):
        return abs(self.rect.x - hero.rect.x) < 2 * SCREEN_WIDTH

    def update(self, platforms, hero):
        if self.is_near(hero):
            self.move_and_process_blocks(platforms)


class Target(sprite.Sprite):
    def __init__(self, x, y):
        sprite.Sprite.__init__(self)

        self.current_images_group = load_images(path='data/coin', size=COIN_SIZE)
        self.cur_frame = 0
        self.image = self.current_images_group[self.cur_frame]
        self.rect = self.image.get_rect()
        self.last_update = pygame.time.get_ticks()
        self.rect.x = x
        self.rect.y = y - COIN_HEIGHT // 2

    def update(self):
        now = pygame.time.get_ticks()
        if now - self.last_update >= FPS:
            self.last_update = now
            self.cur_frame += 1
        if self.cur_frame >= len(self.current_images_group):
            self.cur_frame = 0
        self.image = self.current_images_group[self.cur_frame]
