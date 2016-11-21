####################################################
#                                                  #
#                  -Crossfire-                     #
#                                                  #
#           bcho04, (C)2015-2016                   #
#                                                  #
####################################################

# Crossfire, by bcho04, is licensed under the Apache License 2.0. ALL RIGHTS RESERVED.
# Dependencies:
# - Pygame (1.9.1+)
# - Python 2.7.x (Python 3 not tested)


version = "1.4.b8-3" #Client version - DO NOT CHANGE!
import logging, sys, os, platform, datetime, time
logging.basicConfig(filename="../data/logs/" + str(datetime.datetime.now()) + ".log", format='%(asctime)s %(message)s', datefmt='%m-%d-%y %I:%M:%S %p:', level=logging.DEBUG)
sys.exit(133)
logging.info('--------------------------')
logging.debug('DEBUG: OS Name: ' + os.name)
logging.debug('DEBUG: PID: ' + str(os.getpid()))
logging.debug('DEBUG: Processor: ' + str(platform.processor()))
logging.debug('DEBUG: Python Version: ' + str(sys.version_info[0]) + "." + str(sys.version_info[1]) + "." + str(sys.version_info[2]) + str(sys.version_info[3]) + '\n')
load_profile = open('config.txt', "r")
enableconfig = load_profile.read().splitlines()[1]
logging.debug('INFO: Config Enabled: ' + str(enableconfig))
try:
    import pygame, time, random, urllib2
    from pygame.locals import *    
    start_time=time.time()#Start time
    logging.info('INFO: Importing modules...')
    logging.info('INFO: Initializing Pygame...')
    try:
        pygame.init()
    except UnboundLocalError:
        logging.error("ERROR: Pygame failed to initialize - UnboundLocalError: local variable fonts referenced before assignment.")
        sys.exit(135)
        pygame.quit()
   
    #Get config information:
    if(enableconfig == 'true'): 
        logging.info('INFO: Querying config information...')   

        load_profile = open('config.txt', "r") #Set load source
        load_profile_read = load_profile.read().splitlines()
        p1sh = load_profile_read[3]
        p1sh = int(p1sh)

        p2sh = load_profile_read[5]
        p2sh = int(p2sh)
        
        p1dmi = load_profile_read[7]
        p1dmi = int(p1dmi)

        p1dma = load_profile_read[9]
        p1dma = int(p1dma)

        p2dmi = load_profile_read[15]
        p2dmi = int(p2dmi)

        p2dma = load_profile_read[17]
        p2dma = int(p2dma)
        
        p12xmin = load_profile_read[11]
        p12xmin = int(p12xmin)

        p12xmax = load_profile_read[13]
        p12xmax = int(p12xmax)

        p22xmin = load_profile_read[19]
        p22xmin = int(p22xmin)

        p22xmax = load_profile_read[21]
        p22xmax = int(p22xmax)

        p1shielddamage = load_profile_read[23]
        p1shielddamage = int(p1shielddamage)

        p2shielddamage = load_profile_read[25]
        p2shielddamage = int(p2shielddamage)

        openwebpage = load_profile_read[27]

        autodownload = load_profile_read[29]
    #------
    
    logging.info('INFO: Defining variables...')
    screen = pygame.display.set_mode([640,500]) #Best res. - 640,500
    pygame.display.set_caption('Crossfire (' + str(version) + ')')
    player = pygame.Rect(40,190,20,20)#Player 1
    player2 = pygame.Rect(580,190,20,20)#Player 2
    wall1 = pygame.Rect(0, 0, 10, 460) #The wall on the left
    wall2 = pygame.Rect(630, 0, 10, 460) #The wall on the right
    wall3 = pygame.Rect(0,0,640,10) #The wall on top
    wall4 = pygame.Rect(0,450,640,10) #The wall on bottom
    p1bullet = pygame.Rect(700,700,5,5)#P1's bullet
    p2bullet = pygame.Rect(705,705,5,5)#P2's bullet
    consoleclear = pygame.Rect(0, 465, 640, 90)#console clear rect
    
    #Game Variables
    p1_bullet_fired = False
    p1_bullet_dir = "right"
    p1dir = "right"
    p2_bullet_fired = False
    p2_bullet_dir = "left"
    p2dir = "left"
    if(enableconfig == 'true'):
        p1life = p1sh
        p2life = p2sh
    else:
        p1life = 100
        p2life = 100
    p1boost = False
    p2boost = False
    p1shield = 0
    p2shield = 0
    if(enableconfig == "false"):
        p1shielddamage = 1
        p2shielddamage = 1
    #FONT DEFINITIONS
    font = pygame.font.SysFont(None, 24)
    fontsmall = pygame.font.SysFont(None, 18)
    #END FONT DEFINITIONS
    p1chp = False
    p2chp = False
    p1cdp = False
    p2cdp = False
    
    randomnumber = random.randint(10000,99999)

    #movement vars
    p1right = False
    p1left = False
    p1up = False
    p1down = False
    p2right = False
    p2left = False
    p2up = False
    p2down = False
    HPCollected = False
    DMGCollected = False
    p1username = ""
    p2username = ""
    
    #Arrays
    healthpacks = []
    dmgpacks = []
    shieldpacks = []
    
    main_clock = pygame.time.Clock()
    logging.info('INFO: Defining functions and classes...')
    def draw_screen():
        screen.fill((255,255,255))

    def draw_text(display_string, font, surface, x, y, r, g, b):
        text_display = font.render(display_string, 1, (r, g, b))
        text_rect = text_display.get_rect()
        text_rect.topleft = (x, y)
        surface.blit(text_display, text_rect)

    #This is the blueprint of a healthpack
    class healthpack():
        #rect = pygame.Rect(random.randrange(50,600),random.randrange(30,430),10,10)
        def __init__(self):
            self.x = random.randrange(50,600)
            self.y = random.randrange(30,430)
            self.rect = pygame.Rect(self.x, self.y,10,10)
            self.collected = False
        def drawHP(self):
            if(self.collected == False):
                pygame.draw.rect(screen, (255,0,255), self.rect)
        def randHP(self):
            self.x = random.randrange(50,600)
            self.y = random.randrange(30,430)
        def collectHP(self):
            if(self.collected == False):
                self.collected = True
    #This is the blueprint of a damagepack
    class dmgpack():
        def __init__(self):
            self.x = random.randrange(50,600)
            self.y = random.randrange(30,430)
            self.rect = pygame.Rect(self.x, self.y, 10, 10)
            self.collected = False
        def drawdmg(self):
            if (self.collected == False):
                pygame.draw.rect(screen, (0,100,0), self.rect)
        def randdmg(self):
            self.x = random.randrange(50,600)
            self.y = random.randrange(30,430)
        def collectdmg(self):
            if(self.collected == False):
                self.collected = True
    #This is the blueprint of a shieldpack.
    class shieldpack():
        def __init__(self):
            self.x = random.randrange(50,600)
            self.y = random.randrange(30,430)
            self.rect = pygame.Rect(self.x, self.y, 10, 10)
            self.collected = False
        def drawshield(self):
            if (self.collected == False):
                pygame.draw.rect(screen, (0,128,128), self.rect)
        def randshield(self):
            self.x = random.randrange(50,600)
            self.y = random.randrange(30,430)
        def collectshield(self):
            if(self.collected == False):
                self.collected = True

    #These are  specific healthpacks, shieldpacks, and damagepacks created from the blueprint.
    hp = healthpack()
    healthpacks.append(hp)
    dmg = dmgpack()
    dmgpacks.append(dmg)
    shd = shieldpack()
    shieldpacks.append(shd)

    logging.info('INFO: Getting version data...')
    logging.info('INFO: Creating connection to server for version data.')
    try:
        for line in urllib2.urlopen("https://raw.githubusercontent.com/bcho04/Crossfire-version/master/version.txt"):
            crossfireversion = line
    except:
        logging.warning('WARN: There was an error in retrieving version data. Please check your Internet connection.')
        crossfireversion = "-1"
    logging.debug('INFO: Starting Crossfire version ' + str(version))
    logging.debug('INFO: Initialization of Crossfire ' + version + ' is complete! Finished in %s seconds.' % (time.time() - start_time))
    print("Copyright 2015-2016 Brandon C.. All rights reserved.\nGame information: \nVersion: " + str(version) + "\nLatest Version: " + str(crossfireversion) + "\n")

    updatefilemaker = open("../tempfiles/version.txt", "w+")
    updatefilemaker.write(version)
    updatefilemaker.close()
    updatefilemaker = open("../tempfiles/crossfireversion.txt", "w+")
    updatefilemaker.write(crossfireversion)
    updatefilemaker.close()
        
    if(crossfireversion == '-1'):
        print("Unable to connect to the internet. Please check your internet to recieve version checks.")
        logging.warn("WARN: Unable to retrieve version data due to an error with the connection.")
    logging.info("INFO: Version: " + version + ", Latest Version: " + crossfireversion)
    if(crossfireversion > version):
        print("This version is outdated. Please update your client at https://github.com/bcho04/Crossfire/releases.\n")
        logging.warn("WARNING: Your client is out of date. Update at https://github.com/bcho04/Crossfire/releases.")
        if(enableconfig == "true"):
            if(openwebpage == "true"):
                if(crossfireversion != "-1"):
                    print("Opening webpage... (https://github.com/bcho04/Crossfire/releases)")
                    logging.info("INFO: Opening http://github.com/bcho04/Crossfire/releases...")
                    os.system("open https://github.com/bcho04/Crossfire/releases")
            if(autodownload == "true"):
                if(crossfireversion != "-1"):
                    print("Automatically downloading Crossfire version %s, and transferring current stat and log files.") % (str(crossfireversion))
                    logging.info("INFO: Downloading Crossfire version " + crossfireversion + " from http://github.com/bcho04/Crossfire.")
                    print("Copied version and internet version data to tempfiles.")
                    os.system("open assets/update.command")
                    print("Successfully downloaded Crossfire version %s.") % (str(crossfireversion))

                    

    elif(crossfireversion <= version):
        print("Your client is up to date.\n")
        logging.info("INFO: Your client is up to date.")
    logging.info('INFO: Querying username from users.')
    if(sys.version_info[0] == 3):
        p1username = input("Blue, Please enter your username: ")
        p2username = input("Red, Please enter your username: ")
    elif(sys.version_info[0] == 2):
        p1username = raw_input("Blue, Please enter your username: ")
        p2username = raw_input("Red, Please enter your username: ")
    
    print("\nP1: Use WASD to move and (space) to fire. \nP2: use arrow keys to move and / to fire.")

    logging.info('INFO: Initializing game loop.')
    #Game Loop

    if(os.path.exists("../data/stats/" + p1username + ".txt")):
        file_var = open("../data/stats/" + p1username + ".txt", "r+")
        s = file_var.read()
        print(p1username + "\'s Rating: " + s)
        file_var.close()
    else:
        print(p1username + "\'s rating file does not exist. The file will be created at the end.")
        print(p1username + "\'s Rating: 0\n")

    if(os.path.exists("../data/stats/" + p2username + ".txt")):
        file_var = open("../data/stats/" + p2username + ".txt", "r+")
        s = file_var.read()
        print(p2username + "\'s Rating: " + s)
        file_var.close()
    else:
        print(p2username + "\'s rating file does not exist. The file will be created at the end.")
        print(p2username + "\'s Rating: 0\n")


    while(True):
        main_clock.tick(200)
        #CHECK USER INPPUT
        for event in pygame.event.get():
            if(event.type == QUIT):
                pygame.quit()
                sys.exit(1)


            if event.type == KEYDOWN:
                if(event.key == K_w):
                    player.y = player.y-5
                    p1dir = "up"
                    p1up = True
                if(event.key == K_s):
                    player.y = player.y+5
                    p1dir = "down"
                    p1down = True
                if(event.key == K_a):
                    player.x = player.x-5
                    p1dir = "left"
                    p1left = True
                if(event.key == K_d):
                    player.x = player.x+5
                    p1dir = "right"
                    p1right = True
                if(event.key == K_SPACE):
                    p1_bullet_fired = True

        #Check movement booleans and initiate movement

            if(p1up == True):
                player.y = player.y-5
            if(p1down == True):
                player.y = player.y+5
            if(p1left == True):
                player.x = player.x-5
            if(p1right == True):
                player.x = player.x+5


            if event.type == KEYUP:
                if(event.key == K_w):
                    p1up = False
                if(event.key == K_a):
                    p1left = False
                if(event.key == K_s):
                    p1down = False
                if(event.key == K_d):
                    p1right = False
            #CHECK P1 COLLISION
            if(player.colliderect(wall1)):
                player.x = player.x+10
            if(player.colliderect(wall2)):
                player.x = player.x-10
            if(player.colliderect(wall3)):
                player.y = player.y+10
            if(player.colliderect(wall4)):
                player.y = player.y-10
            if(p1life <= 50 or p2life <= 50):
                hp.randHP()
                hp.drawHP()
            #CHECK USER INPUT FOR P2
            if(event.type == KEYDOWN):
                if(event.key == K_UP):
                    player2.y = player2.y-5
                    p2dir = "up"
                    p2up = True
                if(event.key == K_DOWN):
                    player2.y = player2.y+5
                    p2dir = "down"
                    p2down = True
                if(event.key == K_LEFT):
                    player2.x = player2.x-5
                    p2dir = "left"
                    p2left = True
                if(event.key == K_RIGHT):
                    player2.x = player2.x+5
                    p2dir = "right"
                    p2right = True
                if(event.key == K_SLASH):
                    p2_bullet_fired = True

        #Check movement booleans and initiate movement
            if(p2up == True):
                player2.y = player2.y-5
            if(p2down == True):
                player2.y = player2.y+5
            if(p2left == True):
                player2.x = player2.x-5
            if(p2right == True):
                player2.x = player2.x+5

            if(event.type == KEYUP):
                if(event.key == K_UP):
                    p2up = False
                if(event.key == K_LEFT):
                    p2left = False
                if(event.key == K_DOWN):
                    p2down = False
                if(event.key == K_RIGHT):
                    p2right = False

            #CHECK COLLISION FOR P2
            if(player2.colliderect(wall1)):
                player2.x = player2.x+10
            if (player2.colliderect(wall2)):
                player2.x = player2.x-10
            if (player2.colliderect(wall3)):
                player2.y = player2.y+10
            if (player2.colliderect(wall4)):
                player2.y = player2.y-10

        #DRAW THINGS

        if(random.randrange(0, 4000) == 2000):
            hp2 = healthpack()
            healthpacks.append(hp2)
            
        if(random.randrange(0, 4000) == random.randrange(0,4000)):
            dmg2 = dmgpack()
            dmgpacks.append(dmg2)

        if(random.randrange(0, 2500) == random.randrange(0,2500)):
            shield2 = shieldpack()
            shieldpacks.append(shield2)

        draw_screen()

        if(p1_bullet_fired == True):
            pygame.draw.rect(screen, (0,0,0), p1bullet)
            if(p1dir == "right"):
                p1bullet.x += 3
            if(p1dir == "left"):
                p1bullet.x -= 3
            if(p1dir == "up"):
                p1bullet.y -= 3
            if(p1dir == "down"):
                p1bullet.y += 3
            if(p1bullet.colliderect(wall1) or p1bullet.colliderect(wall2) or p1bullet.colliderect(wall3) or p1bullet.colliderect(wall4)):
                p1_bullet_fired = False
            if(p1bullet.colliderect(player2)):
                p1_bullet_fired = False
                if(enableconfig == 'true'):
                    if(p1boost == True):
                        if(p2shield <= 0):
                            ctp12x = int(random.randint(p12xmin, p12xmax))
                            p2life -= ctp12x
                        else:
                            p2shield -= p1shielddamage
                    else:
                        if(p2shield <= 0):
                            ctp1 = int(random.randint(p1dmi, p2dma))
                            p2life -= ctp1
                        else:
                            p2shield -= p1shielddamage
                else:
                    if(p1boost == True):
                        if(p2shield <= 0):
                            cfp12x = int(random.randint(12 ,16))
                            p2life -= cfp12x
                        else:
                            p2shield -= 1
                    else:
                        if(p2shield <= 0):
                            cfp1 = int(random.randint(6,8))
                            p2life -= cfp1
                        else:
                            p2shield -= 1
                print(p1username + "\'s life: " + str(p1life) + "\n" + p2username+ "\'s life: " + str(p2life) + "\n\n\n\n")
                if (p2life <= 0):
                    draw_text("Blue Wins!", font, screen, 320, 230, 255, 255, 255)
                    print(p2username + " died. " + p1username + " is the winner of the match!")
                    #####OPEN FILEMAKE
                    if(os.path.exists("../data/stats/" + p1username + ".txt")):
                        file_var = open("../data/stats/" + p1username + ".txt", "r+")
                        s = file_var.read()
                        s = int(s) + 1
                        file_var.close()
                        file_var = open("../data/stats/" + p1username + ".txt", "w+")
                        file_var.write(str(s))
                        file_var.close()
                        print(p1username + "\'s rating:" + str(s))
                    else:
                        file_var = open("../data/stats/" + p1username + ".txt", "w+")
                        file_var.write("1")
                        file_var.close()
                        print(p1username + "\'s rating: 1")

                    if(os.path.exists("../data/stats/" + p2username + ".txt")):
                        file_var2 = open("../data/stats/" + p2username + ".txt", "r+")
                        s2 = file_var2.read()
                        file_var2.close()
                        print(p2username + "\'s rating:" + str(s2))
                    else:
                        file_var2 = open("../data/stats/" + p2username + ".txt", "w+")
                        s2 = file_var2.read()
                        file_var2.write("0")
                        file_var2.close()
                        print(p2username + "\'s rating: 0")
                    draw_text("Blue Wins!", font, screen, 320, 230, 255, 255, 255)
                    print("You may now close this window. All changes have been saved, and all files have been created.")
                    logging.info('INFO: Successfully terminated program with exit code 0.')
                    pygame.quit()
                    sys.exit(0)
                    #####CLOSE FILEMAKE
        else:
            p1bullet.x = player.x
            p1bullet.y = player.y

        if(p2_bullet_fired == True):
            pygame.draw.rect(screen, (0,0,0), p2bullet)
            if(p2dir == "right"):
                p2bullet.x += 3
            if(p2dir == "left"):
                p2bullet.x -= 3
            if(p2dir == "up"):
                p2bullet.y -= 3
            if(p2dir == "down"):
                p2bullet.y += 3

            if(p2bullet.colliderect(wall1) or p2bullet.colliderect(wall2) or p2bullet.colliderect(wall3) or p2bullet.colliderect(wall4)):
                p2_bullet_fired = False
            if(p2bullet.colliderect(player)):
                p2_bullet_fired = False
                if(enableconfig == 'true'):
                    if(p2boost == True):
                        if(p1shield <= 0):
                            ctp22x = int(random.randint(p22xmin, p22xmax))
                            p1life -= ctp22x
                        else:
                            p1shield -= p2shielddamage
                    else:
                        if(p1shield <= 0):
                            ctp2 = int(random.randint(p2dmi, p2dma))
                            p1life -= ctp2
                        else:
                            p1shield -= p2shielddamage
                else:
                    if(p2boost == True):
                        if(p1shield <= 0):
                            cfp22x = int(random.randint(12 ,16))
                            p1life -= cfp22x
                        else:
                            p1shield -= 1
                    else:
                        if(p1shield <= 0):
                            cfp2 = int(random.randint(6,8))
                            p1life -= cfp2
                        else:
                            p1shield -= 1
                print(p1username + "\'s life: " + str(p1life) + "\n" + p2username+ "\'s life: " + str(p2life) + "\n\n\n\n")
                if(p1life <= 0):
                    draw_text("Red Wins!", font, screen, 320, 230, 255, 255, 255)
                    print(p1username + " died. " + p2username + " is the winner of the match!")
                    ######OPEN FILEMAKE
                    if(os.path.exists("../data/stats/" + p2username + ".txt")):
                        file_var = open(p2username + ".txt", "r+")
                        s = file_var.read()
                        s = int(s) + 1
                        file_var.close()
                        file_var = open("../data/stats/" + p2username + ".txt", "w+")
                        file_var.write(str(s))
                        file_var.close()
                        print(p2username + "'s rating:" + str(s))
                    else:
                        file_var = open("../data/stats/" + p2username + ".txt", "w+")
                        file_var.write("1")
                        file_var.close()
                        print(p2username + "'s rating: 1")

                    if(os.path.exists("../data/stats/" + p1username + ".txt")):
                        file_var2 = open("../data/stats/" + p1username + ".txt", "r+")
                        s2 = file_var2.read()
                        file_var2.close()
                        print(p1username + "'s rating:" + str(s2))
                    else:
                        file_var2 = open("../data/stats/" + p1username + ".txt", "w+")
                        s2 = file_var2.read()
                        file_var2.write("0")
                        file_var2.close()
                        print(p1username + "'s rating: 0")

                    draw_text("Red Wins!", font, screen, 320, 230, 255, 255, 255)
                    print("You may now close this window. All changes have been saved.")
                    logging.info('INFO: Successfully terminated program with exit code 0.')
                    pygame.quit()
                    sys.exit(0)
                    #####CLOSE FILEMAKE


        else:
            p2bullet.x = player2.x
            p2bullet.y = player2.y

        draw_text(str((p1life)), fontsmall, screen, (player.x), (player.y-12), 0, 0, 200)
        draw_text(str((p2life)), fontsmall, screen, (player2.x),(player2.y-12), 200, 0, 0)
        draw_text(p1username, font, screen, (player.x-(len(p1username)*2.5)),(player.y-25), 0, 0, 0)
        draw_text(p2username, font, screen, (player2.x-(len(p2username)*2.5)), (player2.y-25), 0, 0, 0)

        for h in healthpacks:
            if(h.rect.colliderect(player)):
                if(h.collected == False):
                    p1life += 15
                    p1chp = True
                    h.collectHP()
            if(h.rect.colliderect(player2)):
                if(h.collected == False):
                    p2life += 15
                    p1chp = True
                    h.collectHP()
            h.drawHP()
            
        for d in dmgpacks:
            if(d.rect.colliderect(player)):
                if(d.collected == False):
                    p1boost = True
                    p1cdp = True
                    d.collectdmg()
            if(d.rect.colliderect(player2)):
                if(d.collected == False):
                    p2boost = True
                    p2cdp = True
                    d.collectdmg()
            d.drawdmg()

        for s in shieldpacks:
            if(s.rect.colliderect(player)):
                if(s.collected == False):
                    p1shield += 1
                    s.collectshield()
            if(s.rect.colliderect(player2)):
                if(s.collected == False):
                    p2shield += 1
                    s.collectshield()
            s.drawshield()
        pygame.draw.rect(screen, (0, 0, 100), player)
        pygame.draw.rect(screen, (100, 0, 0), player2)
        pygame.draw.rect(screen, (0, 0, 0), wall1)
        pygame.draw.rect(screen, (0, 0, 0), wall2)
        pygame.draw.rect(screen, (0, 0, 0), wall3)
        pygame.draw.rect(screen, (0, 0, 0), wall4)
        main_clock.tick()
        pygame.display.update()
except ImportError:
    print("Error (132): Module pygame doesn\'t exist.\nPygame is required to run this game.\nPlease install pygame from: \nhttp://www.pygame.org/download.shtml")
    logging.error('ERROR: Pygame does not exist!')
    logging.error('ERROR: This game requires pygame to run.')
    logging.critical('CRITICAL: Force shutting down with exit code 132.')
    sys.exit(132)