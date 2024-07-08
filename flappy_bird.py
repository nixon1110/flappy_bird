import random
import sys
import pygame
from pygame.locals import *

# All the Game Variables
window_width = 600
window_height = 499

# set height and width of window
window = pygame.display.set_mode((window_width, window_height))
elevation = window_height * 0.8
game_images = {}
framepersecond = 32
pipeimage = 'pipe.png'
background_image = 'background.png'
birdplayer_image = 'bird.png'
sealevel_image = 'sealevel.png'


def resize_image(image_path, new_width, new_height):
    original_image = pygame.image.load(image_path).convert_alpha()
    resized_image = pygame.transform.scale(original_image, (new_width, new_height))
    return resized_image


def flappy_game():
    your_score = 0
    horizontal = int(window_width / 5)
    vertical = int(window_width / 2)
    ground = 0
    mytempheight = 100

    # Generating two pipes for blitting on window
    first_pipe = create_pipe()
    second_pipe = create_pipe()

    # List containing lower pipes
    down_pipes = [{'x': window_width + 300 - mytempheight, 'y': first_pipe[1]['y']},
                  {'x': window_width + 300 - mytempheight + (window_width / 2), 'y': second_pipe[1]['y']}]

    # List Containing upper pipes
    up_pipes = [{'x': window_width + 300 - mytempheight, 'y': first_pipe[0]['y']},
                {'x': window_width + 200 - mytempheight + (window_width / 2), 'y': second_pipe[0]['y']}]

    # pipe velocity along x
    pipeVelX = -4

    # bird velocity
    bird_velocity_y = -9
    bird_Max_Vel_Y = 10
    bird_Min_Vel_Y = -8
    birdAccY = 1

    bird_flap_velocity = -8
    bird_flapped = False

    while True:
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN and (event.key == K_SPACE or event.key == K_UP):
                if vertical > 0:
                    bird_velocity_y = bird_flap_velocity
                    bird_flapped = True

        # This function will return true if the flappy bird is crashed
        game_over = is_game_over(horizontal, vertical, up_pipes, down_pipes)
        if game_over:
            print(f"Your your_score is {your_score}")

            # Display the final score
            font = pygame.font.SysFont(None, 55)
            text = font.render(f"Your Score: {your_score}", True, (255, 255, 255))
            text_rect = text.get_rect(center=(window_width / 2, window_height / 2))
            window.blit(text, text_rect)
            pygame.display.update()

            # Wait for a few seconds before exiting
            pygame.time.delay(3000)

            return

        # check for your_score
        playerMidPos = horizontal + game_images['flappybird'].get_width() / 2
        for pipe in up_pipes:
            pipeMidPos = pipe['x'] + game_images['pipeimage'][0].get_width() / 2
            if pipeMidPos <= playerMidPos < pipeMidPos + 4:
                your_score += 1

        if bird_velocity_y < bird_Max_Vel_Y and not bird_flapped:
            bird_velocity_y += birdAccY

        if bird_flapped:
            bird_flapped = False

        playerHeight = game_images['flappybird'].get_height()
        vertical = vertical + min(bird_velocity_y, elevation - vertical - playerHeight)

        # move pipes to the left
        for upperPipe, lowerPipe in zip(up_pipes, down_pipes):
            upperPipe['x'] += pipeVelX
            lowerPipe['x'] += pipeVelX

        # Add a new pipe when the first is about to cross the leftmost part of the screen
        if 0 < up_pipes[0]['x'] < 5:
            new_pipe = create_pipe()
            up_pipes.append(new_pipe[0])
            down_pipes.append(new_pipe[1])

        # if the pipe is out of the screen, remove it
        if up_pipes[0]['x'] < -game_images['pipeimage'][0].get_width():
            up_pipes.pop(0)
            down_pipes.pop(0)

        # Lets blit our game images now
        window.blit(game_images['background'], (0, 0))
        for upperPipe, lowerPipe in zip(up_pipes, down_pipes):
            window.blit(game_images['pipeimage'][0], (upperPipe['x'], upperPipe['y']))
            window.blit(game_images['pipeimage'][1], (lowerPipe['x'], lowerPipe['y']))

        window.blit(game_images['sea_level'], (ground, elevation))
        window.blit(game_images['flappybird'], (horizontal, vertical))

        # Fetching the digits of score.
        numbers = [int(x) for x in list(str(your_score))]
        width = 0

        # finding the width of score images from numbers.
        for num in numbers:
            width += game_images['scoreimages'][num].get_width()

        Xoffset = (window_width - width) / 1.1

        # Blitting the images on the window.
        for num in numbers:
            window.blit(game_images['scoreimages'][num], (Xoffset, window_width * 0.02))
            Xoffset += game_images['scoreimages'][num].get_width()

        # Refreshing the game window and displaying the score.
        pygame.display.update()
        framepersecond_clock.tick(framepersecond)


def is_game_over(horizontal, vertical, up_pipes, down_pipes):
    if vertical > elevation - 25 or vertical < 0:
        return True

    for pipe in up_pipes:
        pipeHeight = game_images['pipeimage'][0].get_height()
        if (vertical < pipeHeight + pipe['y'] and
                abs(horizontal - pipe['x']) < game_images['pipeimage'][0].get_width()):
            return True

    for pipe in down_pipes:
        if (vertical + game_images['flappybird'].get_height() > pipe['y']) and \
                abs(horizontal - pipe['x']) < game_images['pipeimage'][0].get_width():
            return True
    return False


def create_pipe():
    offset = window_height / 3
    pipeHeight = game_images['pipeimage'][0].get_height()
    y2 = offset + random.randrange(
        0, int(window_height - game_images['sea_level'].get_height() - 1.2 * offset))
    pipeX = window_width + 10
    y1 = pipeHeight - y2 + offset
    pipe = [
        # upper Pipe
        {'x': pipeX, 'y': -y1},

        # lower Pipe
        {'x': pipeX, 'y': y2}
    ]
    return pipe


# program where the game starts
if __name__ == "__main__":
    pygame.init()
    framepersecond_clock = pygame.time.Clock()

    # Sets the title on top of the game window
    pygame.display.set_caption('Flappy Bird Game')

    # Load all the images which we will use in the game
    game_images['scoreimages'] = (
        resize_image('0.jpg', 30, 30),
        resize_image('1.jpg', 30, 30),
        resize_image('2.jpg', 30, 30),
        resize_image('3.jpg', 30, 30),
        resize_image('4.jpg', 30, 30),
        resize_image('5.jpg', 30, 30),
        resize_image('6.jpg', 30, 30),
        resize_image('7.jpg', 30, 30),
        resize_image('8.jpg', 30, 30),
        resize_image('9.jpg', 30, 30)
    )
    game_images['flappybird'] = resize_image(birdplayer_image, 50, 38)
    game_images['sea_level'] = resize_image(sealevel_image, window_width, int(window_height * 0.2))
    game_images['background'] = resize_image(background_image, window_width, window_height)
    game_images['pipeimage'] = (
        resize_image(pipeimage, 50, 320),
        resize_image(pipeimage, 50, 320)
    )

    print("WELCOME TO THE FLAPPY BIRD GAME")
    print("Press space or enter to start the game")

    while True:
        horizontal = int(window_width / 5)
        vertical = int((window_height - game_images['flappybird'].get_height()) / 2)
        ground = 0
        while True:
            for event in pygame.event.get():
                if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                    pygame.quit()
                    sys.exit()
                elif event.type == KEYDOWN and (event.key == K_SPACE or event.key == K_UP):
                    flappy_game()
                else:
                    window.blit(game_images['background'], (0, 0))
                    window.blit(game_images['flappybird'],
                                (horizontal, vertical))
                    window.blit(game_images['sea_level'], (ground, elevation))
                    pygame.display.update()
                    framepersecond_clock.tick(framepersecond)
