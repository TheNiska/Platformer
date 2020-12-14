import pygame, os 

os.environ['SDL_VIDEO_CENTERED'] = '1'
pygame.init()
win_size = (1100, 600)
win = pygame.display.set_mode(win_size)
pygame.display.set_caption('!Game!')

wrathNum = 3

img_path_walk = 'PNG\\Wraith_0' + str(wrathNum) + '\\PNG Sequences\\Walking\\Wraith_0' + str(wrathNum) + '_Moving Forward_00'

walkRight = [pygame.image.load(img_path_walk + '0.png'), pygame.image.load(img_path_walk + '1.png'),
            pygame.image.load(img_path_walk + '2.png'), pygame.image.load(img_path_walk + '3.png'),
            pygame.image.load(img_path_walk + '4.png'), pygame.image.load(img_path_walk + '5.png'),
            pygame.image.load(img_path_walk + '6.png'), pygame.image.load(img_path_walk + '7.png'),
            pygame.image.load(img_path_walk + '8.png'), pygame.image.load(img_path_walk + '9.png')]

img_path_stand = 'PNG\\Wraith_0' + str(wrathNum) + '\\PNG Sequences\\Idle\\Wraith_0' + str(wrathNum) + '_Idle_00'

standingRight = [pygame.image.load(img_path_stand + '0.png'), pygame.image.load(img_path_stand + '1.png'),
            pygame.image.load(img_path_stand + '2.png'), pygame.image.load(img_path_stand + '3.png'),
            pygame.image.load(img_path_stand + '4.png'), pygame.image.load(img_path_stand + '5.png'),
            pygame.image.load(img_path_stand + '6.png'), pygame.image.load(img_path_stand + '7.png'),
            pygame.image.load(img_path_stand + '8.png'), pygame.image.load(img_path_stand + '9.png')]

img_path_cast = 'PNG\\Wraith_0' + str(wrathNum) + '\\PNG Sequences\\Casting Spells\\Wraith_0' + str(wrathNum) + '_Casting Spells_0'

cast_right = [pygame.image.load(img_path_cast + '00.png'), pygame.image.load(img_path_cast + '01.png'),
              pygame.image.load(img_path_cast + '02.png'), pygame.image.load(img_path_cast + '03.png'),
              pygame.image.load(img_path_cast + '04.png'), pygame.image.load(img_path_cast + '05.png'),
              pygame.image.load(img_path_cast + '06.png'), pygame.image.load(img_path_cast + '07.png'),
              pygame.image.load(img_path_cast + '08.png'), pygame.image.load(img_path_cast + '09.png'),
              pygame.image.load(img_path_cast + '10.png'), pygame.image.load(img_path_cast + '11.png'),
              pygame.image.load(img_path_cast + '12.png'), pygame.image.load(img_path_cast + '13.png'),
              pygame.image.load(img_path_cast + '14.png'), pygame.image.load(img_path_cast + '15.png'),
              pygame.image.load(img_path_cast + '16.png'), pygame.image.load(img_path_cast + '17.png')]

walkLeft = []
standingLeft = []
cast_left = []

bg = pygame.image.load('PNG\\Battleground1\\Bright\\Battleground1.png')
bg = pygame.transform.scale(bg, (win_size[0], win_size[1] ))

for i in range(len(walkRight)):
    wR_size = walkRight[i].get_size()
    st_size = standingRight[i].get_size()
    walkRight[i] = pygame.transform.scale(walkRight[i], (int(wR_size[0]*0.4), int(wR_size[1]*0.4) ))
    standingRight[i] = pygame.transform.scale(standingRight[i], (int(st_size[0]*0.4), int(st_size[1]*0.4) ))
    walkLeft.append(pygame.transform.flip(walkRight[i], True, False))
    standingLeft.append(pygame.transform.flip(standingRight[i], True, False))
    sp_size = standingRight[i].get_size()

for i in range(len(cast_right)):
    cast_size = cast_right[i].get_size()
    cast_right[i] = pygame.transform.scale(cast_right[i], (int(cast_size[0]*0.4), int(cast_size[1]*0.4) ))
    cast_left.append(pygame.transform.flip(cast_right[i], True, False))


class Player(object):
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.v = 10
        self.isJump = False
        self.isCast = False
        self.jumpCount = 10
        self.castCount = 0
        self.left = False
        self.right = False
        self.prevLR = [False, False]
        self.walkCount = 0
        self.direction = ''
        self.hitbox = (self.x + 56, self.y + 10, 90, 122)

    def draw(self, win):
        if self.isCast:
            if self.direction == 'right':
                win.blit(cast_right[self.castCount], (self.x,self.y))
            elif self.direction == 'left':
                win.blit(cast_left[self.castCount], (self.x,self.y))
            else:
                win.blit(cast_right[self.castCount], (self.x,self.y))
            self.hitbox = (self.x + 56, self.y + 10, 90, 122)   
            pygame.draw.rect(win, (0, 0, 0), self.hitbox, 2)
            return True

        if self.walkCount + 1 >= 27:
            self.walkCount = 0
        if self.right:
            if self.prevLR[1] == False: # если мы не шли вправо, то надо знаново рисовать спрайт
                self.walkCount = 0
            win.blit(walkRight[self.walkCount//3], (self.x,self.y))
            self.walkCount += 1
        elif self.left:
            if self.prevLR[0] == False:
                self.walkCount = 0
            win.blit(walkLeft[self.walkCount//3], (self.x,self.y))
            self.walkCount += 1  
        else:
            if self.prevLR[0] or self.prevLR[1]:
                self.walkCount = 0
            if self.direction == 'left':
                win.blit(standingLeft[self.walkCount//3], (self.x,self.y))
            elif self.direction == 'right':
                win.blit(standingRight[self.walkCount//3], (self.x,self.y))
            else:
                win.blit(standingRight[self.walkCount//3], (self.x,self.y))
            self.walkCount += 1

        self.hitbox = (self.x + 56, self.y + 10, 90, 122)
        pygame.draw.rect(win, (0, 0, 0), self.hitbox, 2)

    def cast_break(self):
        self.isCast = False
        self.castCount = 0

class Bullet(object):
    def __init__(self, x, y, radius, color, facing):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.facing = facing
        self.v = 20 * facing

    def draw(self, win):
        pygame.draw.circle(win, self.color, (self.x, self.y), self.radius)

class Enemy(object):
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.vel = 10
        self.color = (255, 244, 123)
        self.radius = 34
        self.forward = True

    def draw(self, win):
        self.move()
        pygame.draw.circle(win, self.color, (self.x, self.y), self.radius)

    def move(self):
        if self.forward:
            self.x += self.vel
            if self.x > win_size[0]:
                self.forward = False
        else:
            self.x -= self.vel
            if self.x < 0:
                self.forward = True
    def hit(self):
        pass
    


width = sp_size[0]
height = sp_size[1]

clock = pygame.time.Clock()

x = 0
y = win_size[1] - height + 20

def redrawGameWindow():
    win.fill((0,0,0))
    win.blit(bg, (0,0))
    player.draw(win)
    enemy.draw(win)
    for bullet in bullets:
        bullet.draw(win)
    pygame.display.update()

player = Player(x, y, width, height)
enemy = Enemy(win_size[0]+100, 400, 50, 50)
bullets = []

run = True
while run:
    clock.tick(50)

    for bullet in bullets:
        if bullet.x < win_size[0] and bullet.x > 0:
            bullet.x += bullet.v
        else:
            bullets.pop(bullets.index(bullet))

    for event in pygame.event.get(): # в список сохряняет все события
        if event.type == pygame.QUIT:
            run = False


    keys = pygame.key.get_pressed()


    if keys[pygame.K_LEFT]:
        player.cast_break()
        player.direction = 'left'
        player.prevLR = [player.left, player.right]
        player.left = True
        player.right = False
        if player.hitbox[0] > 0: player.x -= player.v
    elif keys[pygame.K_RIGHT]:
        player.cast_break()
        player.direction = 'right'
        player.prevLR = [player.left, player.right]
        player.left = False
        player.right = True
        if (player.hitbox[0] + player.hitbox[2]) < win_size[0]: player.x += player.v
    else:
        player.prevLR = [player.left, player.right]
        player.right = False
        player.left = False
        
    if not player.isJump:    
        if keys[pygame.K_SPACE]:
            player.isJump = True
            player.right = False
            player.left = False
            player.walkCount = 0       
    else:
        if player.jumpCount >= - 10:
            neg = 1
            if player.jumpCount < 0:
                neg = -1
            player.y -= (player.jumpCount**2) * 0.5 * neg
            player.jumpCount -= 1
        else:
            player.isJump = False
            player.jumpCount = 10

    if not player.isCast:
        if keys[pygame.K_z]:
            player.isCast = True
            player.walkCount = 0
    else:
        if player.castCount <= 16:
            player.castCount += 1
            if player.castCount == 7:
                if player.left:
                    facing = -1
                    bullet_pos = player.width/2 - 40
                elif player.right:
                    facing = 1
                    bullet_pos = player.width/2 + 40
                else:
                    if player.direction == 'left':
                        facing = -1
                        bullet_pos = player.width/2 - 40
                    else:
                        facing = 1
                        bullet_pos = player.width/2 + 40

                if len(bullets) < 5:
                    bullets.append(Bullet(round(player.x + bullet_pos), round(player.y + player.height/2), 25, (200, 200, 0), facing))
        else:
            player.isCast = False
            player.castCount = 0



    redrawGameWindow()
pygame.quit()
