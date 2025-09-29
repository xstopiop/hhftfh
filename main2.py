import pygame
import random
import math

pygame.init()

# Размеры окна
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Космическая миссия: Спасение станции")

# Цвета
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
SPACE_COLOR = (10, 10, 30)
SHIP_COLOR = (0, 255, 255)
ASTEROID_COLOR = (139, 69, 19)
ENEMY_COLOR = (255, 0, 0)
ENERGY_COLOR = (255, 255, 0)

# Шрифт
font = pygame.font.SysFont(None, 36)

clock = pygame.time.Clock()

# Функция для отображения текста
def draw_text(text, font, color, surface, x, y):
    textobj = font.render(text, True, color)
    textrect = textobj.get_rect()
    textrect.center = (x, y)
    surface.blit(textobj, textrect)

# Класс игрока (корабль)
class Ship:
    def __init__(self):
        self.x = WIDTH // 2
        self.y = HEIGHT - 50
        self.radius = 15
        self.speed = 5
        self.energy = 0
        self.alive = True

    def draw(self):
        pygame.draw.polygon(screen, SHIP_COLOR, [
            (self.x, self.y - self.radius),
            (self.x - self.radius, self.y + self.radius),
            (self.x + self.radius, self.y + self.radius)
        ])

    def move(self, keys):
        if keys[pygame.K_LEFT]:
            self.x -= self.speed
        if keys[pygame.K_RIGHT]:
            self.x += self.speed
        if keys[pygame.K_UP]:
            self.y -= self.speed
        if keys[pygame.K_DOWN]:
            self.y += self.speed

        # Ограничения по границам
        self.x = max(self.radius, min(WIDTH - self.radius, self.x))
        self.y = max(self.radius, min(HEIGHT - self.radius, self.y))

# Класс астероидов
class Asteroid:
    def __init__(self):
        self.x = random.randint(0, WIDTH)
        self.y = -20
        self.size = random.randint(20, 50)
        self.speed = random.uniform(1, 3)

    def update(self):
        self.y += self.speed

    def draw(self):
        pygame.draw.circle(screen, ASTEROID_COLOR, (int(self.x), int(self.y)), self.size)

# Вражеский корабль
class EnemyShip:
    def __init__(self):
        self.x = random.randint(0, WIDTH)
        self.y = -50
        self.size = 20
        self.speed = 2

    def update(self):
        self.y += self.speed
        self.x += random.choice([-1, 1]) * self.speed
        self.x = max(self.size, min(WIDTH - self.size, self.x))

    def draw(self):
        pygame.draw.rect(screen, ENEMY_COLOR, (self.x - self.size/2, self.y - self.size/2, self.size, self.size))

# Энергия
class Energy:
    def __init__(self):
        self.x = random.randint(20, WIDTH - 20)
        self.y = random.randint(20, HEIGHT // 2)
        self.size = 10

    def draw(self):
        pygame.draw.circle(screen, ENERGY_COLOR, (self.x, self.y), self.size)

# Инициализация
player = Ship()
asteroids = []
enemies = []
energies = [Energy() for _ in range(3)]
score = 0
game_over = False
mission_complete = False
start_time = pygame.time.get_ticks()

# Основной цикл
while True:
    clock.tick(60)
    current_time = pygame.time.get_ticks()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

    keys = pygame.key.get_pressed()
    if not game_over and not mission_complete:
        player.move(keys)

        # Создаем астероиды
        if len(asteroids) < 10:
            if random.random() < 0.02:
                asteroids.append(Asteroid())

        # Создаем врагов
        if len(enemies) < 3:
            if random.random() < 0.01:
                enemies.append(EnemyShip())

        # Обновляем астероиды
        for asteroid in asteroids:
            asteroid.update()

        # Обновляем врагов
        for enemy in enemies:
            enemy.update()

        # Проверка столкновений
        player_rect = pygame.Rect(player.x - player.radius, player.y - player.radius, player.radius*2, player.radius*2)

        # Астероиды
        for asteroid in asteroids:
            asteroid_rect = pygame.Rect(asteroid.x - asteroid.size, asteroid.y - asteroid.size, asteroid.size*2, asteroid.size*2)
            if player_rect.colliderect(asteroid_rect):
                game_over = True

        # Враги
        for enemy in enemies:
            enemy_rect = pygame.Rect(enemy.x - enemy.size/2, enemy.y - enemy.size/2, enemy.size, enemy.size)
            if player_rect.colliderect(enemy_rect):
                game_over = True

        # Энергия
        for energy in energies:
            energy_rect = pygame.Rect(energy.x - energy.size, energy.y - energy.size, energy.size*2, energy.size*2)
            if player_rect.colliderect(energy_rect):
                player.energy += 1
                energies.remove(energy)
                energies.append(Energy())

        # Условие завершения миссии
        if player.energy >= 5:
            mission_complete = True

        # Удаление вышедших за границу объектов
        asteroids = [a for a in asteroids if a.y < HEIGHT + a.size]
        enemies = [e for e in enemies if e.y < HEIGHT + e.size]

    # Рендеринг
    screen.fill(SPACE_COLOR)

    # Космический фон со звездами
    for _ in range(50):
        star_x = random.randint(0, WIDTH)
        star_y = random.randint(0, HEIGHT)
        star_radius = random.randint(1, 2)
        pygame.draw.circle(screen, WHITE, (star_x, star_y), star_radius)

    # Рисуем объекты
    player.draw()
    for asteroid in asteroids:
        asteroid.draw()
    for enemy in enemies:
        enemy.draw()
    for energy in energies:
        energy.draw()

    # Отображение очков и состояния
    if not game_over and not mission_complete:
        elapsed_time = (current_time - start_time) // 1000
        draw_text(f"Время: {elapsed_time} сек", font, WHITE, screen, 100, 20)
        draw_text(f"Энергия: {player.energy}", font, WHITE, screen, 700, 20)
        draw_text("Спасите станцию! Доберите 5 энергии.", font, WHITE, screen, WIDTH//2, 20)
    elif game_over:
        draw_text("Игра окончена! Вы погибли в космосе.", font, WHITE, screen, WIDTH//2, HEIGHT//2)
    elif mission_complete:
        draw_text("Миссия выполнена! Станиция спасена!", font, WHITE, screen, WIDTH//2, HEIGHT//2)

    pygame.display.flip()