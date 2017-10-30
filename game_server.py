import sys, pygame
pygame.init()
pygame.display.set_caption("CG3002 GROUP 5")
size = width, height = 800, 600
speed = [2, 0]
black = 0, 0, 0

frames = 0
image_on = 30
image_off = 30

image_display = True

screen = pygame.display.set_mode(size)

frontguy = pygame.image.load("assets/break-dance.png")
frontguyrect = frontguy.get_rect()
frontguyrect.center = (400 , 200)

welcome = pygame.image.load("assets/startup.png")
welcomerect = welcome.get_rect()
welcomerect.center = (400, 300)

waiting = pygame.image.load("assets/waiting.png")
waitingrect = waiting.get_rect()
waitingrect.center = (400, 500)

trigger = pygame.image.load("assets/trigger.png")
triggerrect = waiting.get_rect()
triggerrect.center = (300, 500)

thisisit = pygame.image.load("assets/thisisit.png")
thisisitrect = thisisit.get_rect()
thisisitrect.center = (400,300)

connected = False
state = 0

font = pygame.font.SysFont('Consolas', 30)
counter, text = 10, '10'.rjust(3)


pygame.mixer.pre_init(44100, -16, 2, 2048) # setup mixer to avoid sound lag

pygame.mixer.init()

# pygame.mixer.music.load('assets/background.mp3')
#
# pygame.mixer.music.play(-1)



while True:
    for event in pygame.event.get():
        #print(event.type)
        if event.type == pygame.QUIT: sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 3 and not connected:
                connected = not connected
                pygame.mixer.music.stop()
                pygame.mixer.music.load('assets/johncena.mp3')
                pygame.mixer.music.play(0)
            if event.button == 3 and connected and state == 0:
                pygame.mixer.music.stop()
                pygame.mixer.music.load('assets/cheering.mp3')
                pygame.mixer.music.play(0)
                state = 1



    if not pygame.mixer.music.get_busy():
        pygame.mixer.music.load('assets/background.mp3')
        pygame.mixer.music.play(0)

    if state == 0:
        welcomerect = welcomerect.move(speed)
        if welcomerect.left < 100 or welcomerect.right > width - 100:
            speed[0] = -speed[0]
        # if welcomerect.top < 0 or welcomerect.bottom > height:
        #     speed[1] = -speed[1]

        screen.fill(black)
        screen.blit(frontguy, frontguyrect)
        if frames == image_on and image_display:
            image_display = not image_display
            frames = 0
            frontguy = pygame.transform.flip(frontguy, True, False)

        if frames == image_off and not image_display:
            image_display = not image_display
            frames = 0
            
        if image_display:
            if not connected:
                screen.blit(waiting, waitingrect)
            else:
                screen.blit(trigger, triggerrect)
        counter += 1

        text = "Time:  "+ str(counter).rjust(3)
        screen.blit(welcome, welcomerect)

        screen.blit(font.render(text, True, (255, 255, 255)), (600, 30))
        frames += 1
        pygame.display.flip()

    if state == 1:
        screen.fill(black)
        screen.blit(thisisit, thisisitrect)
        if frames == image_on and image_display:
            image_display = not image_display
            frames = 0
            thisisit = pygame.transform.flip(thisisit, True, False)

        if frames == image_off and not image_display:
            image_display = not image_display
            frames = 0

        if image_display:
            if not connected:
                #screen.blit(waiting, waitingrect)
                pass
            else:
                pass
                #screen.blit(trigger, triggerrect)
        counter += 1
   

