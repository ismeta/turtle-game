import pygame
from random import randint

pygame.init()

WIDTH = 640
HEIGHT = 512
FRAMERATE = 10
TILE_SIZE = 64
GRID_WIDTH = WIDTH/TILE_SIZE
GRID_HEIGHT = HEIGHT/TILE_SIZE
NUMBER_OF_OBSTACLES = 10
CUSTOM_EVENT = 25

lucida = pygame.font.SysFont("Ubuntu", 36)

# loading multiple bitmaps for animation
whirlpool = []
for i in xrange(8):
   filepath = 'strudel bitmaps/strudel clockwise 000%d.bmp' % i
   image = pygame.image.load(filepath)
   image.set_colorkey(image.get_at((0, 0)))
   whirlpool.append(image)
time = 0

screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock  = pygame.time.Clock()

bg_image = pygame.image.load('water.bmp').convert()
y = bg_image.get_height()
x = bg_image.get_width()

player_image = pygame.image.load('brachiosaurus.bmp').convert()
player_image.set_colorkey(player_image.get_at((0, 0)))
player_x = 0
player_y = 0

prize_image = pygame.image.load('berries.bmp').convert()
prize_image.set_colorkey(prize_image.get_at((0, 0)))
prize_x = randint(0, GRID_WIDTH - 1) * TILE_SIZE
prize_y = randint(0, GRID_HEIGHT - 1) * TILE_SIZE

obstacles = []
obstacle_image = pygame.image.load('strudel bitmaps/strudel clockwise 0000.bmp').convert()
obstacle_image.set_colorkey(obstacle_image.get_at((0, 0)))

for i in xrange(NUMBER_OF_OBSTACLES):
   new_rect = obstacle_image.get_rect()
   grid_x = randint(0, GRID_WIDTH - 1) * TILE_SIZE
   grid_y = randint(0, GRID_HEIGHT - 1) * TILE_SIZE
   
   # making sure that the obstacles aren't on the same square as the prize
   while grid_x == prize_x and grid_y == prize_y:
      grid_x = randint(0, GRID_WIDTH - 1) * TILE_SIZE
      grid_y = randint(0, GRID_HEIGHT - 1) * TILE_SIZE
   new_rect.move_ip(grid_x, grid_y)
   obstacles.append(new_rect)

lava = pygame.image.load('iceberg.bmp').convert()
lava.set_colorkey(lava.get_at((0, 0)))

lava_rect = lava.get_rect(left=64*4, top=0)   
prize_rect = prize_image.get_rect(left=prize_x, top=prize_y)
player_rect = player_image.get_rect(left=player_x, top=player_y)

# setting events to go off at certain times
pygame.time.set_timer(pygame.USEREVENT, 100)

die = 0
quit = False

while quit != True:
   for event in pygame.event.get():
      new_pos = player_rect
      
      if event.type == pygame.QUIT:
         quit = True
         
      elif event.type == pygame.KEYDOWN:
         key = event.key
         if key == pygame.K_ESCAPE:
            quit = True
         elif key == pygame.K_RIGHT:
            new_pos = player_rect.move(TILE_SIZE, 0)
         elif key == pygame.K_LEFT:
            new_pos = player_rect.move(-TILE_SIZE, 0)            
         elif key == pygame.K_DOWN:
            new_pos = player_rect.move(0, TILE_SIZE)
         elif key == pygame.K_UP:
            new_pos = player_rect.move(0, -TILE_SIZE)
         if new_pos.x > WIDTH:
            new_pos.x = 0
         if new_pos.y > HEIGHT:
            new_pos.y = 0
         if new_pos.x < 0:
            new_pos.x = WIDTH - TILE_SIZE
         if new_pos.y < 0:
            new_pos.y = HEIGHT - TILE_SIZE
         player_rect = new_pos
         
      if event.type == pygame.USEREVENT:
         time = (time + 1) % 8
         obstacle_image = whirlpool[time]
         lava_rect.move_ip(randint(-10, 10), randint(-10, 10))
         if lava_rect.y >= HEIGHT:
            lava_rect.y = 0
         if lava_rect.x >= WIDTH:
            lava_rect.x = 0
   
         if new_pos.collidelistall(obstacles):
            player_image = pygame.transform.rotozoom(player_image, -5.0, 0.99)
            player_image = pygame.transform.smoothscale(player_image, (TILE_SIZE, TILE_SIZE))
            player_image.set_colorkey(player_image.get_at((0, 0)))
            die += 1
   
   for i in xrange(HEIGHT/y + 1):
      for j in xrange(WIDTH/x + 1):
         screen.blit(bg_image, (j*x, i*y))
         
   for obstacle in obstacles:
      screen.blit(obstacle_image, obstacle)
      
   if prize_rect.colliderect(player_rect):
      font = lucida
      text = font.render("You won! Press ESC to exit", True, (10, 10, 10))
      textpos = text.get_rect(centerx = WIDTH/2)
      screen.blit(text, textpos)
   
   if lava_rect.colliderect(player_rect):
      text = lucida.render("OUCH", True, (10, 10, 10))
      textpos = text.get_rect(centerx = WIDTH/2)
      screen.blit(text, textpos)

   if die > 20:
      text = lucida.render("you lost the game", True, (10, 10, 10))
      textpos = text.get_rect(centerx = WIDTH/2)
      screen.blit(text, textpos)
      clock.tick(5000)
      quit = True      
      
   screen.blit(prize_image, prize_rect)
   screen.blit(lava, lava_rect)
   screen.blit(player_image, player_rect)
   
   pygame.display.update()
   clock.tick(FRAMERATE)

