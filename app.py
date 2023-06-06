import time
import random
import pygame
from modules.config import load_config
from modules.visuals import Colors, text_font, char_width

# create color object
colors = Colors()

# init and load config settings
pygame.init()
config_dict = load_config()

if config_dict["device_resolution"] == 'True':
    # use resolution of current device
    infoObject = pygame.display.Info()
    display_width = infoObject.current_w
    display_height = infoObject.current_h
else:
    # use manually set resolution in config //menu
    display_width = config_dict["display_width"]
    display_height = config_dict["display_height"]

    # 800x600 is the lowest resolution that can be set
    if display_width < 800:
        display_width = 800
    if display_height < 600:
        display_height = 600

gameDisplay = pygame.display.set_mode((display_width, display_height))

pygame.display.set_caption("Metal Pipe Dodge")
frames = pygame.time.Clock()

characterImg = pygame.image.load("character.png")
characterImg = pygame.transform.scale(characterImg, (54, 59))
pygame.display.set_icon(characterImg )

# background
background_image = pygame.image.load("bg.png").convert()
background_image = pygame.transform.scale(background_image, (display_width, display_height))

# things
thing_image = pygame.image.load("thing.png")
thing_image = pygame.transform.scale(thing_image, (100, 100))

intro_image = pygame.image.load("main_bg.png").convert()
intro_image = pygame.transform.scale(intro_image, (display_width, display_height))

# sound and music
gameover_sound = pygame.mixer.Sound("metal_pipe.mp3")
pygame.mixer.music.load("ost.mp3")


pause = False


def fps_counter():
    font = pygame.font.SysFont(None, 25)
    text = font.render(str(frames), True, colors.black)
    gameDisplay.blit(text, (650, 0))


def things_dodged(count):
    font = pygame.font.SysFont(None, 25)
    text = font.render("Очки: " + str(count), True, colors.black)
    gameDisplay.blit(text, (0, 0))


def things(thingx, thingy, image):
    gameDisplay.blit(image, (thingx, thingy))


def character(x, y):
    gameDisplay.blit(characterImg, (x, y))


def text_objects(text, font):
    textSurface = font.render(text, True, colors.black)
    return textSurface


def message_display(text):
    font = pygame.font.Font(text_font, 115)
    gameDisplay.blit(font.render(text, True, (0, 0, 0)), ((display_width / 2) - len(text) * 32, 0))

    pygame.display.update()

    time.sleep(1)

    game_loop()


def crash():
    pygame.mixer.music.stop()
    pygame.mixer.Sound.play(gameover_sound)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        gameDisplay.fill(colors.white)
        text = "Гру Завершено"
        font = pygame.font.Font(text_font, 80)
        gameDisplay.blit(font.render(text, True, (0, 0, 0)), (125, 100))
        gameDisplay.blit(characterImg, ((display_width * 0.475), (display_height * 0.8)))

        button("Почати", 125, 450, 150, 50, colors.green, colors.bright_green, game_loop)
        button("Вийти", 550, 450, 150, 50, colors.red, colors.bright_red, quitgame)

        fps_counter()
        pygame.display.update()
        frames.tick(15)


def button(msg, x, y, w, h, ic, ac, action = None):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()

    if x + w > mouse[0] > x and y + h > mouse[1] > y:
        pygame.draw.rect(gameDisplay, ac, (x, y, w, h))
        if click[0] == 1 and action != None:
            action()
    else:
        pygame.draw.rect(gameDisplay, ic, (x, y, w, h))

    font = pygame.font.Font(text_font, 30)
    gameDisplay.blit(font.render(msg, True, (0, 0, 0)), (x + 10, y + 10))


def quitgame():
    pygame.quit()
    quit()


def unpause():
    global pause
    pygame.mixer.music.unpause()
    pause = False


def paused():
    pygame.mixer.music.pause()

    while pause:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        gameDisplay.fill(colors.white)

        text = "Пауза"
        font = pygame.font.Font(text_font, 80)
        gameDisplay.blit(font.render(text, True, (0, 0, 0)), (300, 100))
        gameDisplay.blit(characterImg, ((display_width * 0.5), (display_height * 0.8)))

        button("Продовжити", 75, 450, 225, 50, colors.green, colors.bright_green, unpause)
        button("Вийти", 575, 450, 150, 50, colors.red, colors.bright_red, quitgame)

        fps_counter()
        pygame.display.update()
        frames.tick(15)


def game_intro():
    intro = True
    while intro:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        gameDisplay.fill(colors.lawngreen)
        gameDisplay.blit(intro_image, [0, 0])

        text = "Metal Pipe Dodge"
        font = pygame.font.Font(text_font, 80)
        gameDisplay.blit(font.render(text, True, (0, 0, 0)), (85, 100))
        gameDisplay.blit(characterImg, ((display_width * 0.475), (display_height * 0.75)))

        button("Почати", 100, 450, 150, 50, colors.green, colors.bright_green, game_loop)
        button("Вийти", 550, 450, 150, 50, colors.red, colors.bright_red, quitgame)

        fps_counter()
        pygame.display.update()
        frames.tick(15)


def game_loop():
    global pause
    pygame.mixer.music.play(-1)

    x = (display_width * 0.45)
    y = (display_height * 0.8)

    x_change = 0

    thing_startx = random.randrange(0, display_width)
    thing_starty = -600
    thing_speed = 3
    thing_width = 100
    thing_height = 100

    dodged = 0

    gameExit = False
    while not gameExit:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    x_change = -5
                elif event.key == pygame.K_RIGHT:
                    x_change = 5
                elif event.key == pygame.K_p:
                    pause = True
                    paused()

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    x_change = 0





        x += x_change
        gameDisplay.fill(colors.lawngreen)
        gameDisplay.blit(background_image, [0, 0])

        things(thing_startx, thing_starty, thing_image)

        thing_starty += thing_speed
        character(x, y)
        things_dodged(dodged)
        fps_counter()

        if x > display_width - char_width or x < 0:
            crash()

        if thing_starty > display_height:
            thing_starty = 0 - thing_height
            thing_startx = random.randrange(0, display_width)
            dodged += 1
            thing_speed += 0.5

        if y < thing_starty + thing_height:
            if thing_startx < x < thing_startx + thing_width or thing_startx < x + char_width < thing_startx + thing_width:
                crash()

        pygame.display.update()
        frames.tick(60)


game_intro()
game_loop()
pygame.quit()
quit()
