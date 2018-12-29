# James Yun (jy2gm) and Jian Ouyang (jo2bs)

# Credits:
# Back Arrow from https://image.flaticon.com/icons/png/512/0/340.png


import gamebox
import pygame

width = 800
height = 600
camera = gamebox.Camera(width, height)
gamestate = "menu"
punchcount1 = 0
punchcount2 = 0
orientation = True
winner = 0

health1 = 100
health2 = 100
gravity = .7
resistance = 1.05
tock = 0

timer = 100

# uncopyrighted music
music = gamebox.load_sound("http://www.tannerhelland.com/dmusic/Retribution.ogg")


# sprite sheet
Goku_sheet = gamebox.load_sprite_sheet('https://i.imgur.com/YGg1Zcr.png?1', 6, 13)
p1_neutral = Goku_sheet[1]
p1_jump_1 = Goku_sheet[12]
p1_jump_2 = Goku_sheet[13]
p1_right_punch_1 = Goku_sheet[14]
p1_right_punch_2 = Goku_sheet[15]
p1_left_punch_1 = Goku_sheet[16]
p1_left_punch_2 = Goku_sheet[17]
p1_knockback = Goku_sheet[26]
p1_kick = Goku_sheet[10]
p1_block = Goku_sheet[18]

Goku_2_sheet = gamebox.load_sprite_sheet('https://i.imgur.com/n0AxuuL.png?1', 6, 13)
#Goku_2_sheet_flip = Goku_2_sheet.flip()
#Goku_2_sheet = Goku_2_sheet_flip
p2_neutral = Goku_2_sheet[1]
p2_jump_1 = Goku_2_sheet[12]
p2_jump_2 = Goku_2_sheet[13]
p2_right_punch_1 = Goku_2_sheet[14]
p2_right_punch_2 = Goku_2_sheet[15]
p2_left_punch_1 = Goku_2_sheet[16]
p2_left_punch_2 = Goku_2_sheet[17]
p2_knockback = Goku_2_sheet[26]
p2_kick = Goku_2_sheet[10]
p2_block = Goku_2_sheet[18]

ground = gamebox.from_color(400, 550, "brown", 800, 100)
p1 = gamebox.from_image(200, 300, p1_right_punch_2)
p2 = gamebox.from_image(600, 300, p2_right_punch_2)
p2.flip()
music.play(-1)


def tick(keys):
    global health1
    global health2
    global gamestate
    global punchcount1
    global punchcount2
    global orientation
    global timer
    global tock
    global winner

    punchcount1 += 1
    punchcount2 += 1
    tock += 1

    if gamestate == "menu":
        camera.clear("black")
        title = gamebox.from_text(400, 200, "Fight Club", "Arial", 60, "red", bold=True)
        single_player = gamebox.from_text(400, 350, "Single Player", "Arial", 40, "red")
        single_player_box = gamebox.from_color(400, 350, "Orange", 200, 50)
        two_player = gamebox.from_text(400, 425, "Two Player", "Arial", 40, "red")
        two_player_box = gamebox.from_color(400, 425, "Orange", 200, 50)
        instructions = gamebox.from_text(400, 500, "Instructions", "Arial", 40, "red")
        instructions_box = gamebox.from_color(400, 500, "orange", 200, 50)
        mouse = gamebox.from_color(camera.mouse[0], camera.mouse[1], "white", 1, 1)
        if mouse.touches(single_player_box):
            single_player_box = gamebox.from_color(400, 350, "Yellow", 200, 50)
        if mouse.touches(single_player_box) and camera.mouseclick:
            gamestate = "single_player"
            winner = 0
        if mouse.touches(two_player_box):
            two_player_box = gamebox.from_color(400, 425, "Yellow", 200, 50)
        if mouse.touches(two_player_box) and camera.mouseclick:
            gamestate = "two_player"
            winner = 0
        if mouse.touches(instructions_box):
            instructions_box = gamebox.from_color(400, 500, "Yellow", 200, 50)
        if mouse.touches(instructions_box) and camera.mouseclick:
            gamestate = "instructions"

        camera.draw(title)
        camera.draw(single_player_box)
        camera.draw(single_player)
        camera.draw(two_player_box)
        camera.draw(two_player)
        camera.draw(instructions_box)
        camera.draw(instructions)

    # instructions
    if gamestate == "instructions":
        camera.clear("dark grey")
        instructions = gamebox.from_text(400, 100, "Instructions", "Arial", 60, "red", bold=True)
        line1 = gamebox.from_text(400, 250, "Player 1: WASD to move. V to punch.", "Arial", 40, "red")
        line2 = gamebox.from_text(400, 350, "Player 2: Arrow Keys to move. Period to punch.", "Arial", 40, "red")
        back = gamebox.from_image(100, 60, "https://image.flaticon.com/icons/png/512/0/340.png")
        mouse = gamebox.from_color(camera.mouse[0], camera.mouse[1], "white", 1, 1)
        back.scale_by(.1)
        if mouse.touches(back):
            back.scale_by(1.5)
        if mouse.touches(back) and camera.mouseclick:
            gamestate = "menu"

        camera.draw(instructions)
        camera.draw(line1)
        camera.draw(line2)
        camera.draw(back)

    # single player
    if gamestate == "single_player":
        camera.clear("black")
        #p1 motion
        if pygame.K_d in keys:
            p1.x += 6
        if pygame.K_a in keys:
            p1.x -= 6
        p1.yspeed += gravity

        if p1.touches(ground):
            p1.yspeed = 0
            p1.move_to_stop_overlapping(ground)
            if pygame.K_w in keys:
                p1.yspeed -= 14
        if p1.bottom_touches(p2):
            p1.yspeed = 0
            p1.move_to_stop_overlapping(p2)
            if pygame.K_w in keys:
                p1.yspeed -= 14

        if p1.right_touches(p2) and pygame.K_d in keys:
            p2.x += 10
        if p1.left_touches(p2) and pygame.K_a in keys:
            p2.x -= 10

        # punch
        if abs(p1.x - p2.x) < 60 and abs(p1.y - p2.y) < 105 and pygame.K_v in keys and p1.x < p2.x:
            health2 -= 3
            p2.xspeed += 5
            punchcount1 = 0
            p1.image = p1_left_punch_1

        if abs(p1.x - p2.x) < 60 and abs(p1.y - p2.y) < 105 and pygame.K_v in keys and p1.x > p2.x:
            health2 -= 3
            p2.xspeed -= 5
            punchcount1 = 0
            p1.image = p1_left_punch_1

        p1.x += p1.xspeed
        p1.y += p1.yspeed
        p1.xspeed /= resistance
        if p1.x < 25:
            p1.x = 25
            p1.xspeed *= -1
        if p1.x > 775:
            p1.x = 775
            p1.xspeed *= -1

        # computer motion



        if p2.x > p1.x:
            p2.x -= 4
        if p2.x < p1.x:
            p2.x += 4

        if p2.touches(ground):
            p2.yspeed = 0
            p2.move_to_stop_overlapping(ground)
            if pygame.K_UP in keys:
                p2.yspeed -= 14
        if p2.bottom_touches(p1):
            p2.yspeed = 0
            p2.move_to_stop_overlapping(p1)
            if pygame.K_UP in keys:
                p2.yspeed -= 14

        if p2.left_touches(p1) and pygame.K_LEFT in keys:
            p1.x -= 10
        if p2.right_touches(p1) and pygame.K_RIGHT in keys:
            p1.x += 10
        # punch
        if abs(p2.x - p1.x) < 60 and abs(p1.y - p2.y) < 105 and p1.x < p2.x and punchcount1 % 30 == 10:
            health1 -= 3
            p1.xspeed -= 5
            punchcount2 = 0
            p2.image = p2_left_punch_1
        if abs(p2.x - p1.x) < 60 and abs(p1.y - p2.y) < 105 and p2.x < p1.x and punchcount1 % 30 == 10:
            health1 -= 3
            p1.xspeed += 5
            punchcount2 = 0
            p2.image = p2_left_punch_1


        p2.yspeed += gravity
        p2.x += p2.xspeed
        p2.y += p2.yspeed
        p2.xspeed /= resistance
        if p2.x < 25:
            p2.x = 25
            p2.xspeed *= -1
        if p2.x > 775:
            p2.x = 775
            p2.xspeed *= -1

        camera.draw(p1)
        camera.draw(p2)
        camera.draw(ground)
        healthborder1 = gamebox.from_color(200, 50, "Red", 200, 20)
        camera.draw(healthborder1)
        healthcam1 = gamebox.from_color(200, 50, "Green", 2 * health1, 20)
        camera.draw(healthcam1)
        healthborder2 = gamebox.from_color(600, 50, "Red", 200, 20)
        camera.draw(healthborder2)
        healthcam2 = gamebox.from_color(600, 50, "Green", 2 * health2, 20)
        camera.draw(healthcam2)
        timerbox = gamebox.from_text(400, 50, str(timer), "Arial", 40, "Yellow")
        if tock / 30 > 1:
            timer -= 1
            tock = 0
        camera.draw(timerbox)


    # two player
    if gamestate == "two_player":
        camera.clear("black")

        # p1 motion
        if pygame.K_d in keys:
            p1.x += 6
        if pygame.K_a in keys:
            p1.x -= 6
        p1.yspeed += gravity

        if p1.touches(ground):
            p1.yspeed = 0
            p1.move_to_stop_overlapping(ground)
            if pygame.K_w in keys:
                p1.yspeed -= 14
        if p1.bottom_touches(p2):
            p1.yspeed = 0
            p1.move_to_stop_overlapping(p2)
            if pygame.K_w in keys:
                p1.yspeed -= 14

        if p1.right_touches(p2, -15) and pygame.K_d in keys:
            p2.x += 10

        if p1.left_touches(p2, -15) and pygame.K_a in keys:
            p2.x -= 10

        # punch
        if abs(p1.x - p2.x) < 60 and abs(p1.y - p2.y) < 105 and pygame.K_v in keys and p1.x < p2.x:
            health2 -= 3
            p2.xspeed += 5
            punchcount1 = 0
            p1.image = p1_left_punch_1

        if abs(p1.x - p2.x) < 60 and abs(p1.y - p2.y) < 105 and pygame.K_v in keys and p1.x > p2.x:
            health2 -= 3
            p2.xspeed -= 5
            punchcount1 = 0
            p1.image = p1_left_punch_1



        p1.x += p1.xspeed
        p1.y += p1.yspeed
        p1.xspeed /= resistance
        if p1.x < 25:
            p1.x = 25
            p1.xspeed *= -1
        if p1.x > 775:
            p1.x = 775
            p1.xspeed *= -1

        # p2 motion

        if pygame.K_RIGHT in keys:
            p2.x += 6
        if pygame.K_LEFT in keys:
            p2.x -= 6

        if p2.touches(ground):
            p2.yspeed = 0
            p2.move_to_stop_overlapping(ground)
            if pygame.K_UP in keys:
                p2.yspeed -= 14
        if p2.bottom_touches(p1):
            p2.yspeed = 0
            p2.move_to_stop_overlapping(p1)
            if pygame.K_UP in keys:
                p2.yspeed -= 14

        if p2.left_touches(p1, -15) and pygame.K_LEFT in keys:
            p1.x -= 10
        if p2.right_touches(p1, -15) and pygame.K_RIGHT in keys:
            p1.x += 10
        # punch
        if abs(p2.x - p1.x) < 60 and abs(p1.y - p2.y) < 105 and pygame.K_PERIOD in keys and p1.x < p2.x:
            health1 -= 3
            p1.xspeed -= 5
            punchcount2 = 0
            p2.image = p2_left_punch_1

        if abs(p2.x - p1.x) < 60 and abs(p1.y - p2.y) < 105 and pygame.K_PERIOD in keys and p2.x < p1.x:
            health1 -= 3
            p1.xspeed += 5
            punchcount2 = 0
            p2.image = p2_left_punch_1



        p2.yspeed += gravity
        p2.x += p2.xspeed
        p2.y += p2.yspeed
        p2.xspeed /= resistance
        if p2.x < 25:
            p2.x = 25
            p2.xspeed *= -1
        if p2.x > 775:
            p2.x = 775
            p2.xspeed *= -1

        camera.draw(p1)
        camera.draw(p2)
        camera.draw(ground)
        healthborder1 = gamebox.from_color(200, 50, "Red", 200, 20)
        camera.draw(healthborder1)
        healthcam1 = gamebox.from_color(200, 50, "Green", 2 * health1, 20)
        camera.draw(healthcam1)
        healthborder2 = gamebox.from_color(600, 50, "Red", 200, 20)
        camera.draw(healthborder2)
        healthcam2 = gamebox.from_color(600, 50, "Green", 2 * health2, 20)
        camera.draw(healthcam2)

    if orientation != (p1.x < p2.x):
        p1.flip()
        p2.flip()
        orientation = not orientation
    if punchcount1 > 10:
        p1.image = p1_neutral
    elif punchcount1 > 1:
        p1.image = p1_left_punch_2
    if punchcount2 > 10:
        p2.image = p2_neutral
    elif punchcount2 > 1:
        p2.image = p2_left_punch_2
    if health2 < 0:
        winner = 1
        camera.clear("black")
        gamestate = "end"
    elif health1 < 0:
        winner = 2
        camera.clear("black")
        gamestate = "end"
    elif timer == 0:
        winner = 0
        camera.clear("black")
        gamestate = "end"


    # endgame

    if gamestate == "end":
        camera.clear("black")
        health1 = 100
        health2 = 100
        timer = 100
        if winner == 0:
            end = gamebox.from_text(400, 200, "You Ran Out of Time", "Arial", 60, "red", bold=True)
        elif winner == 1:
            end = gamebox.from_text(400, 200, "Player 1 wins", "Arial", 60, "red", bold=True)
        elif winner == 2:
            end = gamebox.from_text(400, 200, "Player 2 loses", "Arial", 60, "red", bold=True)
        mouse = gamebox.from_color(camera.mouse[0], camera.mouse[1], "white", 1, 1)
        playagain = gamebox.from_text(200, 400, "Play Again", "Arial", 40, "red")
        playagain_box = gamebox.from_color(200, 400, "Orange", 200, 50)
        if mouse.touches(playagain_box):
            playagain_box = gamebox.from_color(200, 400, "Yellow", 200, 50)
        if mouse.touches(playagain_box) and camera.mouseclick:
            gamestate = "menu"

        camera.draw(end)
        camera.draw(playagain_box)
        camera.draw(playagain)

    camera.display()



ticks_per_second = 60
gamebox.timer_loop(ticks_per_second, tick)
