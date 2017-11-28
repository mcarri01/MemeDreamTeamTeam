import pygame, pySprites
pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((640, 480))

def main(): 
    pygame.display.set_caption("Super Break")

    background = pygame.Surface(screen.get_size()) 
    background = background.convert() 
    background.fill((255, 255, 255)) 
    screen.blit(background, (0, 0))

    score_keeper = pySprites.ScoreKeeper() 
    ball = pySprites.Ball(screen) 
    player1 = pySprites.Player(screen, 1)
    allSprites = pygame.sprite.Group(score_keeper,ball, player1)

    clock = pygame.time.Clock() 
    keepGoing = True

    pygame.mouse.set_visible(False)

    while keepGoing:
        clock.tick(30)
        for event in pygame.event.get():
            if event.type == pygame.QUIT: 
                keepGoing = False
            elif event.type == pygame.JOYHATMOTION: 
                player1.change_direction(event.value) 
            elif event.type == pygame.KEYDOWN: 
                if event.key == pygame.K_UP: 
                    player2.change_direction((0, 1)) 
                if event.key == pygame.K_DOWN: 
                    player2.change_direction((0, -1))


        allSprites.clear(screen, background) 
        allSprites.update() 
        allSprites.draw(screen)        
        pygame.display.flip()            

    pygame.mouse.set_visible(True)
    pygame.quit()
main()