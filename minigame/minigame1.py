import pygame
from sprites import *
from config import *
import sys

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
        self.clock = pygame.time.Clock()
        self.running = True
        self.font = pygame.font.Font("minigame/Arial.ttf", 32)

        pygame.mixer.music.load("minigame/birdsong.wav")
        pygame.mixer.music.play(-1)

        self.character_spritesheet = Spritesheet("minigame/images/character.png")
        self.terrain_spritesheet = Spritesheet("minigame/images/terrain.png")
        self.clean_spritesheet = Spritesheet("minigame/images/clean.png")
        self.intro_background = pygame.image.load("minigame/images/introbackground.png")
        self.go_background = pygame.image.load("minigame/images/gameover.png")

    def createTilemap(self):
        for i, row in enumerate(tilemap):
            for j, column in enumerate(row):
                Ground(self, j, i)
                if column == "B":
                    Block(self, j, i)
                if column == "P":
                    self.player = Player(self, j, i)
                if column == "X":
                    BananaPeel(self, j, i)
                
                

    def new(self):
        #a new game starts
        self.playing = True

        self.all_sprites = pygame.sprite.LayeredUpdates()
        self.blocks = pygame.sprite.LayeredUpdates()
        self.trash = pygame.sprite.LayeredUpdates()
        self.clean = pygame.sprite.LayeredUpdates()

        self.createTilemap()
        
    

    def events(self):
        #game loop events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.playing = False
                self.running = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    if self.player.facing == "up":
                        Clean(self, self.player.rect.x+10, self.player.rect.y-7)
                    if self.player.facing == "down":
                        Clean(self, self.player.rect.x+10, self.player.rect.y+7)
                    if self.player.facing == "left":
                        Clean(self, self.player.rect.x-7, self.player.rect.y)
                    if self.player.facing == "right":
                        Clean(self, self.player.rect.x+7, self.player.rect.y-10)

    
    def update(self):
        self.all_sprites.update()
        
    def draw(self):
        self.screen.fill(BLACK)
        self.all_sprites.draw(self.screen)
        self.clock.tick(FPS)
        pygame.display.update()

    def main(self):
        #game loop
        while self.playing:
            self.events()
            self.update()
            self.draw()

    def game_over(self):
        text = self.font.render("Game Over", True, WHITE)
        text_rect = text.get_rect()

        restart_button = Button(10, 50, 120, 50, WHITE, BLACK, "Restart", 32)

        for sprite in self.all_sprites:
            sprite.kill()

        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
            mouse_pos = pygame.mouse.get_pos()
            mouse_pressed = pygame.mouse.get_pressed()
            
            if restart_button.is_pressed(mouse_pos, mouse_pressed):
                self.new()
                self.main()

            self.screen.blit(self.go_background, (0,0))
            self.screen.blit(text, text_rect)
            self.screen.blit(restart_button.image, restart_button.rect)
            self.clock.tick(FPS)
            pygame.display.update()




    def intro_screen(self):
        intro = True

        title = self.font.render("College Cleanup", True, BLUE)
        title_rect = title.get_rect(x=90, y=100)
        
        play_button = Button(160, 150, 70, 30, WHITE, BLACK, "Play", 25)

        while intro:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    intro = False
                    self.running = False

            mouse_pos = pygame.mouse.get_pos()
            mouse_pressed = pygame.mouse.get_pressed()

            if play_button.is_pressed(mouse_pos, mouse_pressed):
                intro = False

            self.screen.blit(self.intro_background, (0,0))
            self.screen.blit(title, title_rect)
            self.screen.blit(play_button.image, play_button.rect)
            self.clock.tick(FPS)
            pygame.display.update()

g = Game()
g.intro_screen()
g.new()
while g.running:
    g.main()
    g.game_over()

pygame.quit()
sys.exit()