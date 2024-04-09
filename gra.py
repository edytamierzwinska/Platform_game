'''
"Mashroomland" is a platform game created in Python using the Pygame package.
The player takes on the role of a hero who, due to a mistake in a space-time portal, lands in a mysterious land called Mashroomland.
The goal of the game is to reach the portal located in the top right corner of the screen, collect as many mushrooms as possible, and avoid enemies.
Almost all of the graphics are created by me using the AI Copilot Designer tool,
an online character generator (https://www.avatarsinpixels.com), Gimp, and Canva.
'''

import pygame

pygame.init()

screen_width = 600
screen_height = 600
FPS = 60

screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Mashroomland')

tile_size = 40
game_over = 0
main_menu = True
score = 0

pygame.mixer.music.load('sounds/man_mega.mp3')
pygame.mixer.music.play(-1, 0.0, 5000)


logo = pygame.image.load('images/logo.png')
bg_img = pygame.image.load('images/background.png')
over = pygame.image.load('images/over.png')
start_img = pygame.image.load('images/start.png')
exit_img = pygame.image.load('images/exit.png')
youwin= pygame.image.load('images/youwin.png')
frame_img = pygame.image.load('images/frame.png')
grass_img = pygame.image.load('images/grass.png')
clock = pygame.time.Clock()

class Button():
    def __init__(self, x, y, image):
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.clicked = False

    def draw(self):
        action = False


        pos = pygame.mouse.get_pos()


        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
                action = True
                self.clicked = True

        if pygame.mouse.get_pressed()[0] == 0:
            self.clicked = False


        screen.blit(self.image, self.rect)

        return action

class Player():
    def __init__(self, x, y):
        self.player_img_right = pygame.image.load('images/player1.png')
        self.player_img_left = pygame.image.load('images/player2.png')
        self.image = self.player_img_right
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.vel_y = 0
        self.width = 30
        self.height = 30
        self.jumped = False
        self.is_dead = False
        self.jump_count =0

    def update(self):
        dx = 0
        dy = 0

        key = pygame.key.get_pressed()
        if key[pygame.K_SPACE] and self.jumped == False and self.jump_count < 2:
            self.vel_y = -15
            self.jumped = True
            self.jump_count += 1
        if key[pygame.K_SPACE] == False:
            self.jumped = False
        if key[pygame.K_LEFT]:
            dx -= 5
            self.image = self.player_img_left
        if key[pygame.K_RIGHT]:
            dx += 5
            self.image = self.player_img_right

        self.vel_y += 1
        if self.vel_y > 10:
            self.vel_y = 10
        dy += self.vel_y * 0.5

        for tile in world.tile_list:
            if tile[1].colliderect(self.rect.x + dx, self.rect.y, self.width, self.height):
                dx = 0
            if tile[1].colliderect(self.rect.x, self.rect.y + dy, self.width, self.height):
                if self.vel_y < 0:
                    dy = tile[1].bottom - self.rect.top
                    self.vel_y = 0
                elif self.vel_y >= 0:
                    dy = tile[1].top - self.rect.bottom
                    self.vel_y = 0

        grounded = False
        for tile in world.tile_list:
            if tile[1].colliderect(self.rect.x, self.rect.y + 40, self.width, self.height):
                grounded = True
                if tile[0] == grass_img and self.jump_count >= 2:
                    self.jump_count = 0

        if grounded:
            self.jump_count = 0

        if pygame.sprite.spritecollide(self, enemy_group, False):
            self.is_dead = True

        self.rect.x += dx
        self.rect.y += dy
        screen.blit(self.image, self.rect)


class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('images/enemy.png')
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.move_direction = 1
        self.move_counter = 0

    def update(self):
        self.rect.x += self.move_direction
        self.move_counter += 1
        if abs(self.move_counter) > 50:
            self.move_direction *= -1
            self.move_counter *= -1

class Mushroom(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        img = pygame.image.load('images/mushroom.png')
        self.image = pygame.transform.scale(img, (tile_size // 2, tile_size // 2))
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

class Portal(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        img = pygame.image.load('images/portal.png')
        self.image = pygame.transform.scale(img, (tile_size*1.5 , tile_size*1.5))
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

class World():
    def __init__(self, data):
        self.tile_list = []
        self.portal_group = pygame.sprite.Group()


        row_count = 0
        for row in data:
            col_count = 0
            for tile in row:
                if tile == 1:
                    img = pygame.transform.scale(frame_img, (tile_size, tile_size))
                    img_rect = img.get_rect()
                    img_rect.x = col_count * tile_size
                    img_rect.y = row_count * tile_size
                    tile = (img, img_rect)
                    self.tile_list.append(tile)
                if tile == 2:
                    img = pygame.transform.scale(grass_img, (tile_size, tile_size))
                    img_rect = img.get_rect()
                    img_rect.x = col_count * tile_size
                    img_rect.y = row_count * tile_size
                    tile = (img, img_rect)
                    self.tile_list.append(tile)

                if tile == 3:
                    enemy = Enemy(col_count * tile_size, row_count * tile_size + 15)
                    enemy_group.add(enemy)
                if tile == 4:
                    mushroom = Mushroom(col_count * tile_size + tile_size // 2, row_count * tile_size + tile_size // 2)
                    mushroom_group.add(mushroom)
                if tile == 5:
                    portal = Portal(col_count*tile_size + tile_size // 2, row_count * tile_size + tile_size //2)
                    self.portal_group.add(portal)
                col_count += 1
            row_count += 1

    def draw(self):
        for tile in self.tile_list:
            screen.blit(tile[0], tile[1])
        self.portal_group.draw(screen)


enemy_group = pygame.sprite.Group()
mushroom_group = pygame.sprite.Group()

world_data = [
[1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
[1, 0, 0, 0, 4, 0, 0, 0, 0, 0, 0, 4, 4, 5, 1],
[1, 0, 0, 0, 2, 0, 0, 0, 2, 2, 2, 2, 2, 2, 1],
[1, 0, 0, 4, 0, 3, 0, 4, 0, 0, 0, 4, 0, 0, 1],
[1, 0, 0, 2, 2, 2, 2, 2, 0, 2, 2, 2, 0, 0, 1],
[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 4, 0, 1],
[1, 7, 0, 0, 0, 0, 0, 0, 4, 4, 2, 2, 2, 2, 1],
[1, 0, 0, 0, 4, 0, 0, 2, 2, 2, 0, 0, 0, 0, 1],
[1, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
[1, 0, 4, 4, 0, 4, 3, 0, 0, 4, 0, 0, 0, 0, 1],
[1, 0, 2, 2, 0, 2, 2, 2, 0, 2, 0, 0, 4, 0, 1],
[1, 0, 0, 0, 0, 0, 0, 0, 0, 4, 0, 2, 2, 2, 1],
[1, 0, 0, 0, 4, 0, 2, 2, 2, 2, 2, 2, 2, 2, 1],
[1, 0, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 1],
[1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 1]
]

player = Player(40, 80)
world = World(world_data)

start_button = Button(screen_width // 2 - 240, screen_height // 1.5, start_img)
exit_button = Button(screen_width // 2 + 40, screen_height // 1.5, exit_img)

run = True
while run:
    screen.blit(bg_img, (0, 0))

    if main_menu == True:
        screen.blit(logo, (30, 0))
        if exit_button.draw():
            run = False
        if start_button.draw():
            main_menu = False
    else:
        world.draw()
        enemy_group.update()
        enemy_group.draw(screen)
        mushroom_group.draw(screen)
        player.update()


        if pygame.sprite.spritecollide(player, world.portal_group, False):

            screen.blit(youwin, (0, 0))
            play_button = Button(screen_width // 2 - 240, screen_height // 1.5, start_img)
            exit_button = Button(screen_width // 2 + 40, screen_height // 1.5, exit_img)
            if start_button.draw():
                player.rect.x = 40
                player.rect.y = 80
                world.draw()
                enemy_group.update()
                enemy_group.draw(screen)
                mushroom_group = pygame.sprite.Group()

                for row_count, row in enumerate(world_data):
                    for col_count, tile in enumerate(row):
                        if tile == 4:
                            mushroom = Mushroom(col_count * tile_size + tile_size // 2,
                                                row_count * tile_size + tile_size // 2)
                            mushroom_group.add(mushroom)
                player.update()
                player.is_dead = False
                score = 0
            if exit_button.draw():
                run = False

        collected_mushrooms = pygame.sprite.spritecollide(player, mushroom_group, True)
        if collected_mushrooms:
            score += len(collected_mushrooms)

        if player.is_dead:
            screen.blit(over, (0, 0))

            if start_button.draw():
                player.rect.x = 40
                player.rect.y = 80
                world.draw()
                enemy_group.update()
                enemy_group.draw(screen)
                mushroom_group = pygame.sprite.Group()

                for row_count, row in enumerate(world_data):
                    for col_count, tile in enumerate(row):
                        if tile == 4:
                            mushroom = Mushroom(col_count * tile_size + tile_size // 2,
                                                row_count * tile_size + tile_size // 2)
                            mushroom_group.add(mushroom)
                player.update()
                player.is_dead = False

                score = 0

            if exit_button.draw():
                run = False


        font = pygame.font.Font(None, 36)
        text = font.render('Score: ' + str(score), True, (255, 255, 255))
        screen.blit(text, (10, 10))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    pygame.display.update()
    clock.tick(FPS)

pygame.quit()


