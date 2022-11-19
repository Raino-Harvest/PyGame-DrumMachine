import pygame
from pygame import mixer
pygame.init()

WIDTH = 1400
HEIGHT = 800

black = (0,0,0)
white = (255,255,255)
gray = (128,128,128)
darkGray = (50,50,50)
green = (0,255,0)
gold = (212,175,55)
blue = (0,255,255)

screen = pygame.display.set_mode([WIDTH,HEIGHT])
pygame.display.set_caption('Beat Maker')
labelFont = pygame.font.Font('freesansbold.ttf', 32)
mediumFont = pygame.font.Font('freesansbold.ttf', 24)

fps = 60    
timer = pygame.time.Clock()
beats = 8
instruments = 6
boxes = []
clicked = [[-1 for _ in range(beats)] for _ in range(instruments)]
bpm = 240
playing  = True
activeLength = 0
activeBeat = 0
beatChanged = True


# Load in Sounds

hiHat = mixer.Sound('808 Samples\hi hat.WAV') #hi hat(7)
snare = mixer.Sound('808 Samples\snare.WAV') #snare(44)
kick = mixer.Sound('808 Samples\kick.WAV')   #kick(17)
crash = mixer.Sound('808 Samples\cymbal.WAV')     #cymbal
clap = mixer.Sound('808 Samples\clap.WAV')   #clap(13)
tom = mixer.Sound('808 Samples\\tom.WAV')     #tom(1)
pygame.mixer.set_num_channels(instruments* 3)



def playNotes():
    for i in range(len(clicked)):
        if clicked[i][activeBeat] == 1:
            if i == 0:
                hiHat.play()
            if i == 1:
                snare.play()
            if i == 2:
                kick.play()
            if i == 3:
                crash.play()
            if i == 4:
                clap.play()
            if i == 5:
                tom.play()

def drawGrid(clicked, beat):
    leftBox = pygame.draw.rect(screen, gray, [0, 0, 200, HEIGHT-195], 5)
    bottomBox = pygame.draw.rect(screen, gray, [0, HEIGHT-200, WIDTH, 200],5)
    boxes = []
    colors = [gray, white, gray]
    hiHatText = labelFont.render('Hi Hat', True, white)
    screen.blit(hiHatText,(30,30))
    snareText = labelFont.render('Snare', True, white)
    screen.blit(snareText,(30,130))
    kickText = labelFont.render('Kick', True, white)
    screen.blit(kickText,(30,230))
    crashText = labelFont.render('Crash', True, white)
    screen.blit(crashText,(30,330))
    clapText = labelFont.render('Clap', True, white)
    screen.blit(clapText,(30,430))
    tomText = labelFont.render('Tom', True, white)
    screen.blit(tomText,(30,530))
    
    for i in range(instruments):
        pygame.draw.line(screen, gray, (0, (i*100) + 100), (195, (i*100) + 100) , 3 )

    for i in range(beats):
        for j in range(instruments):
            if clicked[j][i] == -1:
                color = gray
            else:
                color = green 
            rect = pygame.draw.rect(screen, color, [i* ((WIDTH - 200) // beats) + 205,
            (j * 100) + 5 , ((WIDTH-200) // beats) - 10 , ((HEIGHT - 200) // instruments) - 10 ], 0,3)
            
            pygame.draw.rect(screen, gold, [i* ((WIDTH - 200) // beats) + 200, 
            (j * 100), ((WIDTH-200) // beats), ((HEIGHT - 200) // instruments)], 5,5)

            pygame.draw.rect(screen, black, [i* ((WIDTH - 200) // beats) + 200, 
            (j * 100), ((WIDTH-200) // beats), ((HEIGHT - 200) // instruments)], 2,5)

            boxes.append((rect, (i, j)))
        
        active = pygame.draw.rect(screen, blue, [beat* ((WIDTH -200) // beats) + 200, 0 , ((WIDTH - 200)// beats), instruments * 100], 5 , 3)
    return boxes




run = True

while run:
    timer.tick(fps)
    screen.fill(black)
    boxes = drawGrid(clicked,activeBeat)

    #lower Menu buttons
    playPause = pygame.draw.rect(screen, gray, [50,HEIGHT-150, 200,100],0,5)
    playText = labelFont.render('Play/Pause', True, white)
    screen.blit(playText, (70,HEIGHT-130))

    if playing:
        playText2 = mediumFont.render('Playing', True, darkGray)
    else:
        playText2 = mediumFont.render('Pause', True, darkGray)
    screen.blit(playText2, (100, HEIGHT - 95))

    #bpm stuff
    bpmRect = pygame.draw.rect(screen, gray, [300, HEIGHT - 150, 220, 100], 5, 5)
    bpmText = mediumFont.render('Beats Per Minute', True, white)
    screen.blit(bpmText, (308,HEIGHT-130))
    bpmText2 = labelFont.render(f'{bpm}', True, white)
    screen.blit(bpmText2, (370,HEIGHT-100))

    bpmAddRect = pygame.draw.rect(screen,gray, [525,HEIGHT-150,48,48], 0, 5)
    bpmSubRect = pygame.draw.rect(screen,gray, [525,HEIGHT-100,48,48], 0, 5)
    addText = mediumFont.render('+ 5', True, white)
    subText = mediumFont.render('- 5', True, white)
    screen.blit(addText, (530, HEIGHT - 140))
    screen.blit(subText, (530, HEIGHT - 90))


    
    if beatChanged:
        playNotes()
        beatChanged = False


    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            for i in range(len(boxes)):
                if boxes[i][0].collidepoint(event.pos):
                    coords = boxes[i][1]
                    clicked [coords[1]] [coords[0]] *= -1

        if event.type == pygame.MOUSEBUTTONUP:
            if playPause.collidepoint(event.pos):
                if playing:
                    playing = False
                elif not playing:
                    playing = True
    
    beatLength = 3600 // bpm

    if playing:
        if activeLength < beatLength:
            activeLength += 1
        else:
            activeLength = 0
            if activeBeat < beats -1:
                activeBeat +=1
                beatChanged = True
            else:
                activeBeat = 0
                beatChanged = True



    pygame.display.flip()
pygame.quit() 
