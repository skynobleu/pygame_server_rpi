import sys, pygame
import random
pygame.init()
pygame.display.set_caption("CG3002 GROUP 5")
size = width, height = 800, 600
speed = [2, 0]
black = 0, 0, 0
diagonal_speed = [2, 2]

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

doge = pygame.image.load("assets/doge.png")
dogerect = doge.get_rect()
dogerect.center = (300, 200)
doge = pygame.transform.scale(doge, (1200,900))

galaxy = pygame.image.load("assets/galaxy.jpeg")
galaxyrect = galaxy.get_rect()
galaxyrect.center = (400,300)


waiting = pygame.image.load("assets/waiting.png")
waitingrect = waiting.get_rect()
waitingrect.center = (400, 500)

trigger = pygame.image.load("assets/trigger.png")
triggerrect = waiting.get_rect()
triggerrect.center = (300, 500)

thisisit = pygame.image.load("assets/thisisit.png")
thisisitrect = thisisit.get_rect()
thisisitrect.center = (400,300)

excel = pygame.image.load("assets/excellent2.png")
excelrect = excel.get_rect()
excelrect.center = (400, 300)

handstand = pygame.image.load("assets/wavehands1.png")
hs_rect = handstand.get_rect()
hs_rect.center = (400, 300)

load = pygame.image.load("assets/thisisitwords.png")
load_rect = load.get_rect()
load_rect.center = (400, 500)

connected = False
state = 0

font = pygame.font.Font('assets/runescape_uf.ttf', 30)
counter, text = 10, '10'.rjust(3)

gamefont = pygame.font.Font('assets/runescape_uf.ttf', 100)

index = int(random.randrange(0, 9))

pygame.mixer.pre_init(44100, -16, 2, 2048) # setup mixer to avoid sound lag

pygame.mixer.init()
actions = ['wavehands', 'busdriver', 'frontback', 'sidestep', 'jumping', 'jumpingjack', 'turnclap', 'squatturnclap', 'windowcleaning', 'windowcleaner360']
# pygame.mixer.music.load('assets/background.mp3')
#
# pygame.mixer.music.play(-1)
delay = 0
move_timeout = False
#sounds
connect = pygame.mixer.Sound('assets/connected.ogg')
#connect.play()
excellent_sound = pygame.mixer.Sound('assets/excellent.ogg')
while True:
    for event in pygame.event.get():
        #print(event.type)
        if event.type == pygame.QUIT: sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN:


            if event.button == 3 and not connected:
                connected = not connected
                #pygame.mixer.music.stop()
                #pygame.mixer.music.load('assets/connected.mp3')
                connect.play()
                #pygame.mixer.music.play(0)

            elif event.button == 3 and connected and state == 0:
                pygame.mixer.music.stop()
                pygame.mixer.music.load('assets/cheering.mp3')
                pygame.mixer.music.play(0)
                state = 1
                font = pygame.font.SysFont('Consolas', 100)

            elif event.button == 3 and connected and state == 2:
                index = int(random.randrange(0, 9))
                excellent_sound.play()
                #pygame.mixer.music.stop()
                #pygame.mixer.music.load('assets/excellent.mp3')
                #pygame.mixer.music.play(0)
                state = 3
                #delay = 0



    if not pygame.mixer.music.get_busy():
        if state == 0:
            pygame.mixer.music.load('assets/background.mp3')
            pygame.mixer.music.play(0)
        elif state == 1:
            pygame.mixer.music.load('assets/shootingstars.mp3')
            pygame.mixer.music.play(0)
            state = 2

        elif state == 2:
            pygame.mixer.music.load('assets/shootingstars.mp3')
            pygame.mixer.music.play(0)
            index = int(random.randrange(0, 9))
            move_timeout = True


        elif state == 3:
            pygame.mixer.music.load('assets/shootingstars.mp3')
            pygame.mixer.music.play(0)
            state = 2

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
        screen.blit(welcome, welcomerect)
        text = "Time:  "+ str(counter).rjust(3)
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
            screen.blit(load, load_rect)
            #screen.blit(font.render("THIS IS IT", True, (255, 255, 255)), (220, 500))
                #screen.blit(trigger, triggerrect)

        counter += 1
        frames += 1
        pygame.display.flip()

    if state == 2:
        screen.fill(black)
        screen.blit(doge, dogerect)

        hs_rect = hs_rect.move(diagonal_speed)
        if hs_rect.left < 0 or hs_rect.right > width:
            diagonal_speed[0] = -diagonal_speed[0]
        if hs_rect.top < 0 or hs_rect.bottom > height:
            diagonal_speed[1] = -diagonal_speed[1]

        screen.blit(handstand, hs_rect)
        if frames == image_on and image_display:
            image_display = not image_display
            frames = 0
            handstand = pygame.transform.flip(handstand, True, False)
            doge = pygame.transform.scale(doge, (800, 600))

        if frames == image_off and not image_display:
            image_display = not image_display
            frames = 0
            doge = pygame.transform.scale(doge, (1200, 900))

        if image_display:
            screen.blit(gamefont.render(actions[index], True, (255, 255, 0)), (220, 500))

        counter += 1
        frames += 1
        pygame.display.flip()

    if state ==3:
        screen.fill(black)
        screen.blit(galaxy, galaxyrect)
        screen.blit(excel, excelrect)
        if frames == image_on and image_display:
            image_display = not image_display
            frames = 0
            excel = pygame.transform.flip(excel, True, False)
            #galaxy = pygame.transform.scale(galaxy, (1000, 800))

        if frames == image_off and not image_display:
            image_display = not image_display
            frames = 0
            #galaxy = pygame.transform.scale(galaxy, (1200, 900))

        if image_display:
            screen.blit(gamefont.render("Excellent!", True, (255, 255, 255)), (200, 500))
            # screen.blit(trigger, triggerrect)

        counter += 1
        frames += 1
        pygame.display.flip()
        delay += 1
        if delay > 300:
            delay = 0
            state = 2
   

