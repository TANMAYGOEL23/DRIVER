import pygame, random
from sys import exit

pygame.init()
clock = pygame.time.Clock()

# SCREEN
window_width = 406
window_height = 720
window = pygame.display.set_mode((window_width, window_height))
pygame.display.set_caption("THE RACER PROJECT")
font = pygame.font.SysFont("Arial", 36)

# GAME VARIABLES
run = True
fps = 60
speed = 11
car_timer = random.randint(120, 180)
car_alive = True
start_ = False
start_timer = 33
temp = False
score = 0

# LOAD ASSETS
car_img = [pygame.image.load("assets\\car_1.png").convert_alpha(),
           pygame.image.load("assets\\car_2.png").convert_alpha(),
           pygame.image.load("assets\\car_3.png").convert_alpha(),
           pygame.image.load("assets\\car_4.png").convert_alpha(),
           pygame.image.load("assets\\car_5.png").convert_alpha(),
           pygame.image.load("assets\\car_6.png").convert_alpha(),
           pygame.image.load("assets\\car_7.png").convert_alpha(),
           pygame.image.load("assets\\car_8.png").convert_alpha()]
road_img = pygame.image.load("assets\\road.png").convert_alpha()
start_img = pygame.image.load("assets\\start-button.png")
end_img = pygame.image.load("assets\\dead.png")

start_rect = start_img.get_rect()
start_rect.center = (window_width // 2, window_height // 2)
end_rect = end_img.get_rect()
end_rect.center = (window_width // 2, window_height // 2)


# CLASS
class Road(pygame.sprite.Sprite):
    global speed

    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = road_img
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = x, y

    def update(self):
        self.rect.y += speed
        if self.rect.y >= window_height:
            self.kill()


class Player(pygame.sprite.Sprite):
    def __init__(self, car_num):
        pygame.sprite.Sprite.__init__(self)
        self.x, self.y = window_width // 2, 540
        self.car_num = car_num - 1
        self.image = car_img[self.car_num]
        self.rect = self.image.get_rect()
        self.rect.center = (self.x, self.y)
        self.speed = 4
        self.angle = 0

    def update(self):
        user_input = pygame.key.get_pressed()
        action_left = user_input[pygame.K_a] or user_input[pygame.K_LEFT]
        action_right = user_input[pygame.K_d] or user_input[pygame.K_RIGHT]

        # Rotation
        if action_left and self.angle <= 4:
            self.angle += 0.5
        if action_right and self.angle >= -4:
            self.angle -= 0.5
        if (not action_left and not action_right) or (action_left and action_right) and self.angle != 0:
            if self.angle > 0:
                self.angle -= 0.5
            else:
                self.angle += 0.5

        # MOVEMENT
        self.image = car_img[self.car_num]
        if user_input[pygame.K_a] or user_input[pygame.K_LEFT]:
            self.x -= self.speed
            self.image = pygame.transform.rotate(self.image, self.angle)
        if user_input[pygame.K_d] or user_input[pygame.K_RIGHT]:
            self.x += self.speed
            self.image = pygame.transform.rotate(self.image, self.angle)

        # BOOST
        if user_input[pygame.K_SPACE]:
            pass

        self.rect = self.image.get_rect()
        self.rect.center = (self.x, self.y)

        # Solid line
        if self.x <= 82:
            self.x = 82
            self.angle = 0
        if self.x >= 322:
            self.x = 322
            self.angle = 0


class Cars(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = car_img[random.randint(0, 7)]
        self.x = random.choice([322, 160, 82, 244])
        self.y = -self.image.get_height()
        self.rect = self.image.get_rect()
        self.rect.midbottom = (self.x, self.y)
        self.speed = 7

    def update(self):
        self.rect = self.image.get_rect()
        self.rect.midbottom = (self.x, self.y)
        self.y += self.speed
        if self.rect.y - self.image.get_height() >= window_height:
            self.kill()


# FUNCTION
def quit_game():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()


def main():
    global run, car_timer, car_alive, score
    while run:
        quit_game()
        window.fill((255, 255, 255))

        # DRAW
        road.draw(window)
        player.draw(window)
        car.draw(window)

        # UPDATE ROAD
        if car_alive:
            road.update()
            if len(road) <= 2:
                road.add(Road(0, -window_height + 35))

        # UPDATE PLAYER
        if car_alive:
            player.update()

        # CARS spawner
        if car_alive:
            if car_timer <= 0:
                car.add(Cars())
                car_timer = random.randint(30, 90)
            car_timer -= 1
            car.update()

        # COLLISIONS
        collision = pygame.sprite.spritecollide(player.sprites()[0], car, False, pygame.sprite.collide_mask)
        if collision:
            car_alive = False

        # SCORE
        score += 1
        text = font.render("Km : " + str(score // 360), True, "red")
        text_area = text.get_rect()
        text_area.center = (120, 30)
        window.blit(text, text_area)

        # LOST
        if not car_alive:
            car_alive = True
            break

        # CLOCK
        clock.tick(fps)
        pygame.display.update()


def start():
    global start_, start_timer
    while not start_:
        window.fill((117, 107, 219))
        user_input_keyboard = pygame.key.get_pressed()

        if user_input_keyboard[pygame.K_SPACE]:
            start_ = True
            break

        window.blit(start_img, start_rect)
        pygame.display.update()

        quit_game()
        # CLOCK
        clock.tick(fps)
        pygame.display.update()

        start_timer -= 1
        if start_timer <= 22:
            start_rect.center = ((window_width // 2) + 3, (window_height // 2) - 3)
        if start_timer <= 11:
            start_rect.center = ((window_width // 2) + 6, (window_height // 2) - 6)
        if start_timer <= 0:
            start_timer = 33
            start_rect.center = ((window_width // 2), (window_height // 2))


def end():
    while True:
        quit_game()
        window.blit(end_img, end_rect)
        pygame.display.update()

        user_input = pygame.key.get_pressed()
        if user_input[pygame.K_SPACE] or user_input[pygame.K_DOWN]:
            break


while True:
    road = pygame.sprite.Group()
    road.add(Road(0, 0))
    player = pygame.sprite.GroupSingle()
    player.add(Player(2))
    car = pygame.sprite.Group()

    score = 0
    start()
    main()
    end()
    quit_game()
