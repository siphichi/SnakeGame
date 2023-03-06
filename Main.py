import pygame, random, sys
from pygame.math import Vector2

class PROTEIN:
    def __init__(self):
        self.body = [Vector2(5, 10), Vector2(4, 10), Vector2(3, 10)]
        self.direction = Vector2(0,0)
        self.new_block = False
        
        self.head_up = pygame.image.load('graphics2/head_up.png').convert_alpha()
        self.head_down = pygame.image.load('graphics2/head_down.png').convert_alpha()
        self.head_right = pygame.image.load('graphics2/head_right.png').convert_alpha()
        self.head_left = pygame.image.load('graphics2/head_left.png').convert_alpha()

        self.tail_up = pygame.image.load('graphics2/tail_up.png').convert_alpha()
        self.tail_down = pygame.image.load('graphics2/tail_down.png').convert_alpha()
        self.tail_right = pygame.image.load('graphics2/tail_right.png').convert_alpha()
        self.tail_left = pygame.image.load('graphics2/tail_left.png').convert_alpha()

        self.body_vertical = pygame.image.load('graphics2/body_vertical.png').convert_alpha()
        self.body_horizontal = pygame.image.load('graphics2/body_horizontal.png').convert_alpha()

        self.body_tr = pygame.image.load('graphics2/body_tr.png').convert_alpha()
        self.body_tl = pygame.image.load('graphics2/body_tl.png').convert_alpha()
        self.body_br = pygame.image.load('graphics2/body_br.png').convert_alpha()
        self.body_bl = pygame.image.load('graphics2/body_bl.png').convert_alpha()
        
        self.crunch_sound = pygame.mixer.Sound('Sound/Sound_crunch.wav')
        
    def draw_protein(self):
        self.update_head_graphics()
        self.update_tail_graphics()

        for index, block in enumerate(self.body):
            block_rect = pygame.Rect(int(block.x * cell_size), int(block.y * cell_size), cell_size, cell_size)
            if index == 0:
                screen.blit(self.head,block_rect)
            elif index == len(self.body) -1:
                screen.blit(self.tail, block_rect)
            else:
                previous_block = self.body[index + 1] - block
                next_block = self.body[index -1] - block
                
                if previous_block.x == next_block.x:
                    screen.blit(self.body_vertical, block_rect)
                elif previous_block.y == next_block.y:
                    screen.blit(self.body_horizontal, block_rect)
                else:
                    if previous_block.x == -1 and next_block.y == -1 or previous_block.y == -1 and next_block.x == -1:
                        screen.blit(self.body_tl, block_rect)
                    if previous_block.x == -1 and next_block.y == 1 or previous_block.y == 1 and next_block.x == -1:
                        screen.blit(self.body_bl, block_rect)
                    if previous_block.x == 1 and next_block.y == -1 or previous_block.y == -1 and next_block.x == 1:
                        screen.blit(self.body_tr, block_rect)
                    if previous_block.x == 1 and next_block.y == 1 or previous_block.y == 1 and next_block.x == 1:
                        screen.blit(self.body_br, block_rect)
                
    def update_head_graphics(self):
        head_relation = self.body[1] - self.body[0]
        if head_relation == Vector2(1, 0):
            self.head = self.head_left
        elif head_relation == Vector2(-1, 0):
            self.head = self.head_right
        elif head_relation == Vector2(0, 1):
            self.head = self.head_up
        elif head_relation == Vector2(0, -1):
            self.head = self.head_down
            
    def update_tail_graphics(self):
        tail_relation = self.body[-2] - self.body[-1]
        if tail_relation == Vector2(1, 0):
            self.tail = self.tail_left
        elif tail_relation == Vector2(-1, 0):
            self.tail = self.tail_right
        elif tail_relation == Vector2(0, 1):
            self.tail = self.tail_up
        elif tail_relation == Vector2(0, -1):
            self.tail = self.tail_down
    
    def move_protein(self):
        if self.new_block:
            body_copy = self.body[:]
            self.new_block = False
        else:
            body_copy = self.body[:-1]
            
        body_copy.insert(0, body_copy[0] + self.direction)
        self.body = body_copy[:]

    def add_block(self):
        self.new_block = True
        
    def play_crunch_sound(self):
        self.crunch_sound.play()
        
    def reset(self):
        self.body = [Vector2(5, 10), Vector2(4, 10), Vector2(3, 10)]
        self.direction = Vector2(0,0)
    
class DOMAINS:
    def __init__(self):
        self.randomise()
        
    def draw_domain(self):
        domain_rect = pygame.Rect(int(self.pos.x * cell_size), int(self.pos.y * cell_size), cell_size, cell_size)
        screen.blit(apple, domain_rect)
        #pygame.draw.rect(screen, 'Green', domain_rect)
        
    def randomise(self):
        self.x = random.randint(0, cell_number - 1)
        self.y = random.randint(0, cell_number - 1)
        self.pos = Vector2(self.x, self.y)
        
class MAIN:
    def __init__(self):
        self.protein = PROTEIN()
        self.domain = DOMAINS()
    
    def update(self):
        self.protein.move_protein()
        self.check_collision()
        self.check_fail()

    def draw_elements(self):
        self.draw_grass()
        self.domain.draw_domain()
        self.protein.draw_protein()
        self.draw_score()
        
    def check_collision(self):
        if self.domain.pos == self.protein.body[0]:
            self.domain.randomise()
            self.protein.add_block()
            self.protein.play_crunch_sound()
        
        for block in self.protein.body[1:]:
            if block == self.domain.pos:
                self.domain.randomise()
    
    def check_fail(self):
        if not 0 <= self.protein.body[0].x < cell_number or not 0 <= self.protein.body[0].y < cell_number:
            self.game_over()
    
        for block in self.protein.body[1:]:
            if block == self.protein.body[0]:
                self.game_over()
    
    def game_over(self):
        self.protein.reset()
        
    def draw_grass(self):
        grass_color = (167, 209, 61)
        for row in range(0, cell_number, 2):
            for col in range(0, cell_number, 2):
                grass_rect = pygame.Rect(col*cell_size, row*cell_size, cell_size, cell_size)
                pygame.draw.rect(screen, grass_color, grass_rect)
        for row in range(1, cell_number, 2):
            for col in range(1, cell_number, 2):
                grass_rect = pygame.Rect(col*cell_size, row*cell_size, cell_size, cell_size)
                pygame.draw.rect(screen, grass_color, grass_rect)
                
    def draw_score(self):
        score_text = str(len(self.protein.body) - 3)
        score_surf = game_font.render(score_text, True, (56, 74, 12))
        score_x = int(cell_size * cell_number - 60)
        score_y = int(cell_size * cell_number - 40)
        score_rect = score_surf.get_rect(center = (score_x, score_y))
        apple_rect = apple.get_rect(midright = (score_rect.left, score_rect.centery))
        bg_rect = pygame.Rect(apple_rect.left, apple_rect.top, (apple_rect.width + score_rect.width +6), apple_rect.height)

        pygame.draw.rect(screen, (167, 209, 61), bg_rect)
        screen.blit(score_surf, score_rect)
        screen.blit(apple, apple_rect)
        pygame.draw.rect(screen, (56, 74, 12), bg_rect, 6)

pygame.mixer.pre_init(44100, -16, 2, 512)
pygame.init()
cell_size = 40
cell_number = 20
screen = pygame.display.set_mode((cell_number*cell_size, cell_number*cell_size))
pygame.display.set_caption('Protein Maker')
clock = pygame.time.Clock()
apple = pygame.image.load('graphics2/apple.png').convert_alpha()
game_font = pygame.font.Font('Font/PoetsenOne-Regular.ttf', 25)

SCREEN_UPDATE = pygame.USEREVENT
pygame.time.set_timer(SCREEN_UPDATE, 150)

main_game = MAIN()

while True:
    for event in pygame.event.get():     
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
            
        if event.type == SCREEN_UPDATE:
            main_game.update()
        
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and main_game.protein.direction.y != 1:
                main_game.protein.direction = Vector2(0, -1)
            if event.key == pygame.K_DOWN and main_game.protein.direction.y != -1:
                main_game.protein.direction = Vector2(0, 1)
            if event.key == pygame.K_LEFT and main_game.protein.direction.x != 1:
                main_game.protein.direction = Vector2(-1, 0)
            if event.key == pygame.K_RIGHT and main_game.protein.direction.x != -1:
                main_game.protein.direction = Vector2(1, 0)
                
                
                
    screen.fill((175, 215, 70))
    main_game.draw_elements()
    pygame.display.update()
    clock.tick(60)
   
