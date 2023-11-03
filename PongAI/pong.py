import pygame, sys, random
import numpy as np
from pongAI import AI
import json

ai = AI()
# Population: 50
# Population for players on left side - Size: 50, Inputs: 5, Outputs: 3, Hidden_layer_width: 0, Hidden_layer_height: 0
population = ai.create_population(50, 5, 3, 0, 0)
# Population for players on right side - Size: 50, Inputs: 5, Outputs: 3, Hidden_layer_width: 0, Hidden_layer_height: 0
population2 = ai.create_population(50, 5, 3, 0, 0)

control = random.choice(population)
control2 = random.choice(population2)
view = 0
mode = 0
allow = 0

# Initializing Pygame - Basically getting it ready
pygame.init()
clock = pygame.time.Clock()

# Screen size - Can be changed
screen_height = 500
screen_width = 1000
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Pong AI")

# ball, paddle1 for right side - Population: 50, paddle2 for right side - Population: 50
ball = pygame.Rect(screen_width/2 - 10, screen_height/2 - 10, 20, 20)
paddle1 = []
paddleAI = pygame.Rect(screen_width - 20, random.randint(0, screen_height), 10, 120)
paddleU = pygame.Rect(10, random.randint(0, screen_height), 10, 120)
for i in range(50):
    paddle1.append(pygame.Rect(screen_width - 20, random.randint(0, screen_height), 10, 120))
paddle2 = []
for i in range(50):
    paddle2.append(pygame.Rect(10, random.randint(0, screen_height), 10, 120))

# Colors
background = pygame.Color("black")
light_grey = (200, 200, 200)
grey = (120, 120, 120)

# Speed of our ball
ball_speed_x, ball_speed_y = 7 * random.choice((1, -1)), 7 * random.choice((1, -1))

# Scores
paddle1_score = 0
paddle2_score = 0

# Font
game_font = pygame.font.Font("freesansbold.ttf", 22)

def ball_animation():
    # getting the global stuff
    global ball_speed_x, ball_speed_y, paddle1_score, paddle2_score
    # Add the speed to ball's position to move it
    ball.x += ball_speed_x
    ball.y += ball_speed_y

    # Checking if ball collided with walls - If yes change direction and add a score
    if ball.top <= 0 or ball.bottom >= screen_height:
        ball_speed_y *= -1
    if ball.left <= 0:
        paddle1_score += 1
        ball_speed_x *= -1
    if ball.right >= screen_width:
        paddle2_score += 1
        ball_speed_x *= -1

def paddle1_animation(paddle):
    # Globals Again
    global ball_speed_x, ball_speed_y
    # Checking if paddle collided with the walls - If yes stop
    if paddle.top <= 0:
        paddle.top = 0
    if paddle.bottom >= screen_height:
        paddle.bottom = screen_height

    # Checking if ball collided with the paddle - If yes change direction
    if mode == 1 and allow == 1:
        if ball.colliderect(paddle) and ball_speed_x > 0:
            if abs(ball.right - paddle.left)  < 10:
                ball_speed_x *= -1
            elif abs(ball.bottom - paddle.top) < 10 and ball_speed_y > 0:
                ball_speed_y *= -1
            elif abs(ball.top - paddle.bottom) < 10 and ball_speed_y < 0:
                ball_speed_y *= -1

def paddleAI_animation(paddle):
    # Globals Again
    global ball_speed_x, ball_speed_y
    # Checking if paddle collided with the walls - If yes stop
    if paddle.top <= 0:
        paddle.top = 0
    if paddle.bottom >= screen_height:
        paddle.bottom = screen_height

    # Checking if ball collided with the paddle - If yes change direction
    if ball.colliderect(paddle) and ball_speed_x > 0:
        if abs(ball.right - paddle.left)  < 10:
            ball_speed_x *= -1
        elif abs(ball.bottom - paddle.top) < 10 and ball_speed_y > 0:
            ball_speed_y *= -1
        elif abs(ball.top - paddle.bottom) < 10 and ball_speed_y < 0:
            ball_speed_y *= -1

def paddle2_animation(paddle):
    # Same thing with side being changed
    global ball_speed_x, ball_speed_y
    if paddle.top <= 0:
        paddle.top = 0
    if paddle.bottom >= screen_height:
        paddle.bottom = screen_height

    if mode == 1 and allow == 1:
        if ball.colliderect(paddle) and ball_speed_x < 0:
            if abs(ball.left - paddle.right)  < 10:
                ball_speed_x *= -1
            elif abs(ball.bottom - paddle.top) < 10 and ball_speed_y > 0:
                ball_speed_y *= -1
            elif abs(ball.top - paddle.bottom) < 10 and ball_speed_y < 0:
                ball_speed_y *= -1

def paddleU_animation(paddle):
    # Same thing with side being changed
    global ball_speed_x, ball_speed_y
    if paddle.top <= 0:
        paddle.top = 0
    if paddle.bottom >= screen_height:
        paddle.bottom = screen_height

    if ball.colliderect(paddle) and ball_speed_x < 0:
        if abs(ball.left - paddle.right)  < 10:
            ball_speed_x *= -1
        elif abs(ball.bottom - paddle.top) < 10 and ball_speed_y > 0:
            ball_speed_y *= -1
        elif abs(ball.top - paddle.bottom) < 10 and ball_speed_y < 0:
            ball_speed_y *= -1

# To keep track of the generations
gen = 0
gen2 = 0

paddle_speed = 0
emFlag = 1
emFlag2 = 1

# To check if ball collided with paddle
collided = False
collided2 = False

# getting the population that survived the crash
safe = []
safe2 = []

# Getting paddles who are alive
safe_paddle = []
safe_paddle2 = []

# Fit Guys
fit = []
fit2 = []

# In case no one survived
emergency = []
emergency2 = []

# Main stuff
while True:

    # Deciding the action based on position and speed of ball and paddle
    if mode == 1:
        result = ai.run_network(control, [paddleU.y, ball.x, ball.y, ball_speed_x, ball_speed_y])
        action = max(result)
        index = result.index(action)
        if index == 0:
            paddleU.y -= 7
        elif index == 1:
            paddleU.y += 7
        else:
            paddleU.y = paddleU.y

        for i in range(len(paddle2)):
            result = ai.run_network(population[i], [paddle2[i].y, ball.x, ball.y, ball_speed_x, ball_speed_y])
            action = max(result)
            index = result.index(action)
            if index == 0:
                paddle2[i].y -= 7
                #print("P2: Up")
            elif index == 1:
                paddle2[i].y += 7
                #print("P2: Stop")
            else:
                paddle2[i].y = paddle2[i].y
                #print("P2: Down")
    else:
        paddleU.y += paddle_speed

    # Deciding the action based on position and speed of ball and paddle

    result = ai.run_network(control2, [paddleAI.y, ball.x, ball.y, ball_speed_x, ball_speed_y])
    action = max(result)
    index = result.index(action)
    if index == 0:
        paddleAI.y -= 7
    elif index == 1:
        paddleAI.y += 7
    else:
        paddleAI.y = paddleAI.y

    for i in range(len(paddle1)):
        result = ai.run_network(population2[i], [paddle1[i].y, ball.x, ball.y, ball_speed_x, ball_speed_y])
        action = max(result)
        index = result.index(action)
        if index == 0:
            paddle1[i].y -= 7
            #print("P2: Up")
        elif index == 1:
            paddle1[i].y += 7
            #print("P2: Stop")
        else:
            paddle1[i].y = paddle1[i].y
            #print("P2: Down")

    # Exiting the game
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            # Saving the current population in a json file for future use
            file = open("save.json", "w")
            toSave = json.dumps({
                'population': population,
                'population2': population2
            })
            file.write(toSave)
            pygame.quit()
            sys.exit()
        # In case you wanna control a paddle
        if event.type == pygame.KEYDOWN:
            if mode == 0:
                if event.key == pygame.K_w:
                    paddle_speed = -7
                if event.key == pygame.K_s:
                    paddle_speed = 7
            if event.key == pygame.K_v:
                if view == 0:
                    view = 1
                else:
                    view = 0
            if event.key == pygame.K_c:
                if mode == 0:
                    mode = 1
                else:
                    mode = 0
            if event.key == pygame.K_a:
                if allow == 0:
                    allow = 1
                else:
                    allow = 0
            if event.key == pygame.K_k:
                population = ai.create_population(50, 5, 3, 0, 0)
                gen = 0
            if event.key == pygame.K_l:
                population2 = ai.create_population(50, 5, 3, 0, 0)
                gen2 = 0
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_w or event.key == pygame.K_s:
                paddle_speed = 0

    # Getting the animation done
    ball_animation()
    for i in range(len(paddle1)):
        paddle1_animation(paddle1[i])
    if mode == 1:
        for i in range(len(paddle2)):
            paddle2_animation(paddle2[i])
    paddleAI_animation(paddleAI)
    paddleU_animation(paddleU)

    # Rendering the stuff we are doing
    screen.fill(background)
    if view == 1:
        for i in range(len(paddle1)):
            pygame.draw.rect(screen, grey, paddle1[i])
        if mode == 1:
            for i in range(len(paddle2)):
                pygame.draw.rect(screen, grey, paddle2[i])
    pygame.draw.rect(screen, light_grey, paddleAI)
    pygame.draw.rect(screen, light_grey, paddleU)
    pygame.draw.ellipse(screen, light_grey, ball)
    pygame.draw.aaline(screen, light_grey, (screen_width/2, 0), (screen_width/2, screen_height))

    # Displaying the scores, generations and alive population
    paddle1_text = game_font.render(f"{paddle1_score}", False, light_grey)
    paddle2_text = game_font.render(f"{paddle2_score}", False, light_grey)
    gen_text = game_font.render(f"Gen: {gen}", False, light_grey)
    alive_text = game_font.render(f"Alive: {len(population)}", False, light_grey)
    gen2_text = game_font.render(f"Gen: {gen2}", False, light_grey)
    alive2_text = game_font.render(f"Alive: {len(population2)}", False, light_grey)
    screen.blit(paddle1_text, (510, 240))
    screen.blit(paddle2_text, (470, 240))
    screen.blit(gen_text, (250, 0))
    screen.blit(alive_text, (250, 50))
    screen.blit(gen2_text, (600, 0))
    screen.blit(alive2_text, (600, 50))

    if mode == 1:
        # Killing those who fail to collide with the ball
        emFlag = 1
        for i in range(len(paddle2)):
            if paddle2[i].colliderect(ball):
                emFlag = 0
                if collided == False:
                    collided = True

                if collided == True:
                    safe.append(population[i])
                    safe_paddle.append(paddle2[i])
                    collided == False

        # Checking who survived and making them the fit guys
        if safe != []:
            fit = []
            for i in range(3):
                fit.append(random.choice(population))
            population = []
            for i in range(len(safe)):
                fit.append(safe[i])
                population.append(safe[i])
            control = random.choice(fit)
            safe = []

        if safe_paddle != []:
            paddle2 = []
            for i in range(len(safe_paddle)):
                paddle2.append(safe_paddle[i])
            safe_paddle = []

        # If no one survived then get random guys
        if ball.left <= 0 and emFlag == 1:
            emergency = []
            for i in range(3):
                emergency.append(random.choice(population))
            population = []
            paddle2 = []

        # Once the ball is gone and every one is dead start the new generation
        if population == [] and paddle2 == [] and ball.left > 15:
            gen += 1
            if len(fit) == 0:
                new_population = ai.cross_mating(emergency, 50, 45)
                population = ai.mutate(new_population, 2)
                for i in range(50):
                    paddle2.append(pygame.Rect(10, random.randint(0, screen_height), 10, 120))
            else:
                new_population = ai.cross_mating(fit, 50, 10)
                population = ai.mutate(new_population, 2)
                for i in range(50):
                    paddle2.append(pygame.Rect(10, random.randint(0, screen_height), 10, 120))

    # Do the same for the right side
    emFlag2 = 1
    for i in range(len(paddle1)):
        if paddle1[i].colliderect(ball):
            emFlag2 = 0
            if collided2 == False:
                collided2 = True

            if collided2 == True:
                safe2.append(population2[i])
                safe_paddle2.append(paddle1[i])
                collided2 == False

    if safe2 != []:
        fit2 = []
        for i in range(3):
            fit2.append(random.choice(population2))
        population2 = []
        for i in range(len(safe2)):
            fit2.append(safe2[i])
            population2.append(safe2[i])
        control2 = random.choice(fit2)
        safe2 = []

    if safe_paddle2 != []:
        paddle1 = []
        for i in range(len(safe_paddle2)):
            paddle1.append(safe_paddle2[i])
        safe_paddle2 = []

    if ball.right >= screen_width and emFlag2 == 1:
        emergency2 = []
        for i in range(3):
            emergency2.append(random.choice(population2))
        population2 = []
        paddle1 = []

    if population2 == [] and paddle1 == [] and ball.right < screen_width - 15:
        gen2 += 1
        if len(fit2) == 0:
            new_population2 = ai.cross_mating(emergency2, 50, 45)
            population2 = ai.mutate(new_population2, 2)
            for i in range(50):
                paddle1.append(pygame.Rect(screen_width - 20, random.randint(0, screen_height), 10, 120))
        else:
            new_population2 = ai.cross_mating(fit2, 50, 20)
            population2 = ai.mutate(new_population2, 2)
            for i in range(50):
                paddle1.append(pygame.Rect(screen_width - 20, random.randint(0, screen_height), 10, 120))

    # Update the game
    pygame.display.flip()
    clock.tick(60)
