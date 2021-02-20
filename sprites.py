from settings import *


class Player(sprite.Sprite):
    def __init__(self, x, y):
        sprite.Sprite.__init__(self)

        self.x = 0  # скорость горизонтального перемещения. 0 - стоять на месте
        self.y = 0  # скорость вертикального перемещения

        self.onGround = False  # На земле ли я?

        self.startX = x  # Начальная позиция Х, пригодится когда будем переигрывать уровень
        self.startY = y

        self.image = Surface((PLAYER_WIDTH, PLAYER_HEIGHT))
        self.image.fill(Color(0, 0, 0))
        self.rect = Rect(x, y, PLAYER_WIDTH, PLAYER_HEIGHT)  # прямоугольный объект

    def update(self, left, right, up, platforms):
        if up:
            if self.onGround:  # прыгаем, только когда можем оттолкнуться от земли
                self.y = -JUMP_POWER
        if left:
            self.x = -MOVE_SPEED  # Лево = x- n

        if right:
            self.x = MOVE_SPEED  # Право = x + n

        if not (left or right):  # стоим, когда нет указаний идти
            self.x = 0

        if not self.onGround:
            self.y += GRAVITY

        self.onGround = False  # Мы не знаем, когда мы на земле((
        self.rect.y += self.y
        self.collide(0, self.y, platforms)

        self.rect.x += self.x  # переносим свои положение на xvel
        self.collide(self.x, 0, platforms)

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
