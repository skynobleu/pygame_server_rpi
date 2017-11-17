from tkinter import *
import socket
import sys
import server_auth
import random
import time
import threading
import os
import pandas as pd
import pygame
import random

class server:
    def __init__(self, ip_addr, port_num):
        global action
        global action_set_time
        global state
        global change
        global connected
        global move_made
        global wrong_move

        wrong_move = False
        change = False
        state = 0
        connected = False
        move_made = False
        # init server
        self.auth = server_auth.server_auth()
        # Create a TCP/IP socket
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # Bind the socket to the port
        server_address = (ip_addr, port_num)
        print('starting up on %s port %s' % server_address, file=sys.stderr)
        self.sock.bind(server_address)
        # Listen for incoming connections
        self.sock.listen(3)
        self.actions = ['wavehands', 'busdriver', 'frontback', 'sidestep', 'jumping','jumpingjack', 'turnclap', 'squatturnclap', 'windowcleaning', 'windowcleaner360']
        self.filename = "logServer.csv"
        self.columns = ['timestamp', 'action',
                'goal', 'time_delta',
                'correct', 'voltage', 'current', 'power', 'cumpower']
        self.df = pd.DataFrame(columns=self.columns)
        self.df = self.df.set_index('timestamp')
        action = None
        action_set_time = None
        self.timeout = 20
        self.no_response = False
        
    def start_server(self):
        self.timer = threading.Timer(self.timeout, self.getAction)
        self.timer.start()
        print ("No actions for 10 seconds to give time to connect")
        while True:
            # Wait for a connection
            print('waiting for a connection', file=sys.stderr)
            connection, client_address = self.sock.accept()
            #self.secret_key = input("Enter the secret key: ")
            print("Enter the secret key: ")
            self.secret_key = sys.stdin.readline().strip()

            print('connection from', client_address, file=sys.stderr)
            global connected, change, movemade
            if len(self.secret_key) == 16 or len(self.secret_key) == 24 or len(self.secret_key) == 32:

              connected = True
              change = True

            else:
              print ("AES key must be either 16, 24, or 32 bytes long")
              break

            # Receive the data in small chunks and retransmit it
            while True: #Change to 20 actions
            #for x in range(21):
                data = connection.recv(1024)
                if data:
                        try:
                            msg = data.decode()
                            decodedmsg = self.auth.decryptText(msg,self.secret_key)
                            if decodedmsg['action'] == "logout  ":
                                print("bye bye")
                            elif len(decodedmsg['action']) == 0:
                                pass
                            elif action == None: # Ignore if no action has been set yet
                                pass
                            else:   # If action is available log it, and then...
                                self.no_response = False
                                self.logMoveMade(decodedmsg['action'], decodedmsg['voltage'],decodedmsg['current'],decodedmsg['power'],decodedmsg['cumpower'])
                                print("{} :: {} :: {} :: {} :: {}".format(decodedmsg['action'], decodedmsg['voltage'],decodedmsg['current'],decodedmsg['power'],decodedmsg['cumpower']))
                                if movemade and state == 2:
                                    self.getAction() # ...get new action
                                    movemade = False
                        except Exception as e:
                            print(e)
                else:
                     print('no more data from', client_address, file=sys.stderr)
                     connection.close()
                     connected = False
                     break


    def getAction(self):
        self.timer.cancel()
        if self.no_response: # If no response was sent
            self.logMoveMade("None", 0,0,0,0)
            print("ACTION TIMEOUT")
        
        global action
        global action_set_time
        action = random.choice(self.actions)
        action_set_time = time.time()
        print("NEW ACTION :: {}".format(action))
        self.timer = threading.Timer(self.timeout, self.getAction)
        self.no_response = True
        self.timer.start()

    def logMoveMade(self, action_made, voltage, current, power, cumpower):
        file = "log"+str(groupID)+".csv";
        if not os.path.isfile(file):
            with open(file, 'w') as f:
                self.df.to_csv(f)
        with open(file, 'a') as f:
            data = {}
            data['timestamp'] = time.time()
            data['action'] = action_made
            data['goal'] = action
            data['time_delta'] = data['timestamp'] - action_set_time
            data['voltage'] = voltage
            data['current'] = current
            data['power'] = power
            data['cumpower'] = cumpower
            data['correct'] = (action == action_made)
            global movemade, wrong_move
            movemade = action == action_made
            if action != None:
                if action != action_made:
                    wrong_move = True
            if action == "logout":
                sys.exit(1)
            self.df = pd.DataFrame(data, index=[0])[self.columns].set_index('timestamp')
            self.df.to_csv(f, header=False)

if len(sys.argv) != 4:
    print('Invalid number of arguments')
    print('python server.py [IP address] [Port] [groupID]')
    sys.exit()

ip_addr = sys.argv[1]
port_num = int(sys.argv[2])
groupID = sys.argv[3]

#IP address = 'x.x.x.x'
#Port = 8888

global state
my_server = server(ip_addr,port_num)

threading.Thread(target=my_server.start_server).start()

global action, change, movemade, wrong_move
#initialize pygame
movemade = False
wrong_move = False
pygame.init()
pygame.display.set_caption("CG3002 GROUP 5")
size = width, height = 800, 600
speed = [2, 0]
diagonal_speed = [2, 2]
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

excel = pygame.image.load("assets/excellent2.png")
excelrect = excel.get_rect()
excelrect.center = (400, 300)

handstand = pygame.image.load("assets/wavehands1.png")
hs_rect = handstand.get_rect()
hs_rect.center = (400, 300)

load = pygame.image.load("assets/thisisitwords.png")
load_rect = load.get_rect()
load_rect.center = (400, 500)

doge = pygame.image.load("assets/doge.png")
dogerect = doge.get_rect()
dogerect.center = (300, 200)
doge = pygame.transform.scale(doge, (1200,900))

galaxy = pygame.image.load("assets/galaxy.jpeg")
galaxyrect = galaxy.get_rect()
galaxyrect.center = (400,300)

font = pygame.font.Font('assets/runescape_uf.ttf', 30)
counter, text = 10, '10'.rjust(3)

gamefont = pygame.font.Font('assets/runescape_uf.ttf', 100)

index = int(random.randrange(0, 9))

pygame.mixer.pre_init(44100, -16, 2, 2048) # setup mixer to avoid sound lag

pygame.mixer.init()
actions = ['wavehands', 'busdriver', 'frontback', 'sidestep', 'jumping', 'jumpingjack', 'turnclap', 'squatturnclap', 'windowcleaning', 'windowcleaner360']

pygame.mixer.music.load('assets/background.mp3')

pygame.mixer.music.play(-1)

move_timeout = False
# Create action display window
# display_window = Tk()
# display_label = Label(display_window, text = str(action))
# display_label.config(font=('times', 150, 'bold'))
# display_label.pack(expand=True)
# display_window.update()

#sounds
connect = pygame.mixer.Sound('assets/connected.ogg')
#connect.play()
excellent_sound = pygame.mixer.Sound('assets/excellent.ogg')
delay = 0
buzzer = pygame.mixer.Sound('assets/buzzer.ogg')

while True: #Display new task
    # display_label.config(text=str(action))
    # display_window.update()
    # time.sleep(0.2)
    for event in pygame.event.get():
        # print(event.type)
        if event.type == pygame.QUIT: sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN:

            if event.button == 3 and not connected:
                connected = not connected
                connect.play()

            elif event.button == 3 and connected and state == 0:
                pygame.mixer.music.stop()
                pygame.mixer.music.load('assets/cheering.mp3')
                pygame.mixer.music.play(0)
                state = 1
                #font = pygame.font.SysFont('Consolas', 100)

            elif event.button == 3 and connected and state == 2:
                index = int(random.randrange(0, 9))
                pygame.mixer.music.stop()
                pygame.mixer.music.load('assets/excellent.mp3')
                pygame.mixer.music.play(0)
                state = 3

    if wrong_move:
        buzzer.play()
        wrong_move = False

    if connected and change:
        pygame.mixer.music.stop()
        pygame.mixer.music.load('assets/connected.mp3')
        pygame.mixer.music.play(0)
        change = False

    elif connected and state == 0:
        pygame.mixer.music.stop()
        pygame.mixer.music.load('assets/cheering.mp3')
        pygame.mixer.music.play(0)
        state = 1
        #font = pygame.font.SysFont('Consolas', 100)

    elif connected and movemade and state == 2:
        #index = int(random.randrange(0, 9))
        excellent_sound.play()
        state = 3
        movemade = False


    if not pygame.mixer.music.get_busy():
        if state == 0:
            pygame.mixer.music.load('assets/background.mp3')
            pygame.mixer.music.play(0)
        elif state == 1:
            pygame.mixer.music.load('assets/shootingstars.mp3')
            pygame.mixer.music.play(0)
            state = 2

        elif state == 2 and move_timeout:
            pygame.mixer.music.load('assets/buzzer.mp3')
            pygame.mixer.music.play(0)
            move_timeout = False

        elif state == 2:
            pygame.mixer.music.load('assets/shootingstars.mp3')
            pygame.mixer.music.play(0)
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

        text = "Time:  " + str(counter).rjust(3)
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
            screen.blit(load, load_rect)
            # screen.blit(font.render("THIS IS IT", True, (255, 255, 255)), (220, 500))
            # screen.blit(trigger, triggerrect)

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
            screen.blit(gamefont.render(action, True, (255, 255, 0)), (220, 500))

        text = "Time:  " + str(counter).rjust(3)
        screen.blit(font.render(text, True, (255, 255, 255)), (600, 30))
        counter += 1
        frames += 1
        pygame.display.flip()

    if state == 3:
        screen.fill(black)
        screen.blit(galaxy, galaxyrect)
        screen.blit(excel, excelrect)
        if frames == image_on and image_display:
            image_display = not image_display
            frames = 0
            excel = pygame.transform.flip(excel, True, False)

        if frames == image_off and not image_display:
            image_display = not image_display
            frames = 0

        if image_display:
            screen.blit(gamefont.render("Excellent!", True, (255, 255, 0)), (200, 500))
            # screen.blit(trigger, triggerrect)

        counter += 1
        frames += 1
        pygame.display.flip()

        delay += 1
        if delay > 210:
            delay = 0
            state = 2
