import pygame, random, sys
from pygame.locals import *
from pygame import mixer
from dangersForGame import Dangers, Hog
from dogForGame import Dog
from goodsForGame import Goods, MedKit

pygame.mixer.pre_init(44100, -16, 1, 512)
pygame.init()
# init screen size, name, clock
WIDTH, HEIGHT = 600, 800
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('The woof road')
clock = pygame.time.Clock()

#define fonts
font = pygame.font.SysFont("Trebuchet MS", 30, bold=True)

# sound variables
music_volume = 0.1
intro_volume = 0.15
sfx_volume = 0.4
is_muted = False
intro_played = False

#define spawn timers
spawn_timer_dangers = 0
spawn_timer_goods = 0
spawn_timer_hogs = 0
spawn_timer_medkit = 0

#define spawn rate
dangers_spawn_rate = 90
goods_spawn_rate = 140
hogs_spawn_rate = 280
medkit_spawn_rate = 340

#define game variables
game_over = 0
spawn_medkit = False
spawn_hogs = False
min_goods_speed = 2
min_dangers_speed = 2
medkit_speed = 2
hogs_speed = 5
paused = False
game_state = "menu"


# load sounds
chewing_fx = pygame.mixer.Sound("game assets/GameSounds/chewing sound.wav")

intro_fx = pygame.mixer.Sound("game assets/GameSounds/intro song.mp3")
intro_fx.set_volume(music_volume)

medkit_fx = pygame.mixer.Sound("game assets/GameSounds/medkit_pickup.ogg")

dogyelp_fx = pygame.mixer.Sound("game assets/GameSounds/dogyelp.wav")

hog_fx = pygame.mixer.Sound("game assets/GameSounds/HogOink.mp3")

game_over_fx = pygame.mixer.Sound("game assets/GameSounds/game_over_fx.wav")

menu_music = "game assets/GameSounds/Main Menu Song.mp3"
game_play_music = "game assets/GameSounds/game play song.mp3"


def set_volume():
    #Set the volume for sound effects and music based on mute state
    vol = 0 if is_muted else sfx_volume #if muted, vol is 0, else vol is sfx_volume
    chewing_fx.set_volume(vol)
    intro_fx.set_volume(0 if is_muted else intro_volume) #if muted, vol is 0 else, use intro volume
    medkit_fx.set_volume(vol)
    dogyelp_fx.set_volume(vol)
    hog_fx.set_volume(vol)
    game_over_fx.set_volume(vol)

def play_music(music_file, volume=music_volume):
    # play music with optional volume control (mute or not)
    pygame.mixer.music.stop() # stop any currently palying music
    pygame.mixer.music.load(music_file) #load the new music file
    pygame.mixer.music.set_volume(0 if is_muted else volume) #volume 0 if muted, else use given volume
    pygame.mixer.music.play(-1) #keep playing music in a loop

def toggle_mute():
    global is_muted
    if is_muted: #switch between mute and umute
        is_muted = False
    else:
        is_muted = True

    set_volume() #Update all SFX volume
    pygame.mixer.music.set_volume(0 if is_muted else music_volume) #update music volume

    #redraw the mute/unmute icon
    icon_rect = pygame.Rect(550,750, mute_img.get_width(), mute_img.get_height())
    screen.blit(background, icon_rect, icon_rect) #clear the are where the icon is

    if is_muted:
        screen.blit(mute_img, (550, 750)) #show muted icon
    else:
        screen.blit(unmute_img, (550, 750)) #show unmuted icon

    pygame.display.update()

#set initial variables.
class GameData:
    def __init__(self):
        self.score = 0
        self.level = 1
        self.previous_level = 1
        self.max_danger_speed = 2
        self.max_goods_speed = 2
        self.max_dangers_spawn_rate = 90

game_data = GameData()


#timer variables
countdown = 3
last_count = 0
countdown_start_time = None
clock = pygame.time.Clock()
fps = 60


#load background image:
background = pygame.image.load("game assets/Background/ForestBGscaled.png")
menu_bg = pygame.image.load("game assets/MainMenu/MainMenuPicScaled.png")
gameOver_bg = pygame.image.load("game assets/Game Over/gameover.png")
instructions_bg = pygame.image.load("game assets/Instructions/InstructionsBG.png")

def draw_bg():
    screen.blit(background, (0, 0))

#print text function
def draw_text(text, font, text_col, x, y, border_col = None, border_thickness = 2):
    img = font.render(text, True, text_col)
    rect = img.get_rect(topleft=(x, y))
    screen.blit(img, (x, y))

#player images:
player_images = {
    #list of 4 frames for each side of movement
    #convert alpha preserves transparency
    'up': [pygame.image.load(f'game assets/dog/dogUp{i}.png').convert_alpha() for i in range(1, 5)],
    'down': [pygame.image.load(f'game assets/dog/dogDown{i}.png').convert_alpha() for i in range(1, 5)],
    'left': [pygame.image.load(f'game assets/dog/dogLeft{i}.png').convert_alpha() for i in range(1, 5)],
    'right': [pygame.image.load(f'game assets/dog/dogRight{i}.png').convert_alpha() for i in range(1, 5)],
}


#Hog images
hog_images = {
    #list of 2 frames for each side of movement
    #convert alpha preserves transparency
    'right' : [pygame.image.load(f'game assets/hog/HogRight{i}.png').convert_alpha() for i in range(1, 5)],
    'left' : [pygame.image.load(f'game assets/hog/HogLeft{i}.png').convert_alpha() for i in range(1, 5)],
}


#load heart images
full_heart = pygame.image.load('game assets/Health/FullHeart.png')
empty_heart = pygame.image.load('game assets/Health/EmptyHeart.png')

#load mute/unmute images
mute_img = pygame.image.load('game assets/Mute Icons/mute.png')
unmute_img = pygame.image.load('game assets/Mute Icons/unmute.png')

# define heart size
heart_size = 32
#scale resizes an image
full_heart = pygame.transform.scale(full_heart, (heart_size, heart_size))
empty_heart = pygame.transform.scale(empty_heart, (heart_size, heart_size))


#dangers images:
danger_images = [pygame.image.load(f'game assets/dangers/danger{i}.png').convert_alpha() for i in range(1, 4)]

#Goods images:
goods_images = [pygame.image.load(f'game assets/Good Stuff/Good{i}.png').convert_alpha() for i in range(1, 4)]
medkit_image = pygame.image.load('game assets/Health/AidKit.png')

#define colors
WHITE = (255, 255, 255)
RED = (255, 50, 50)
GREEN = (50, 255, 50)
BLUE = (50, 50, 255)
BLACK = (0, 0, 0)

class TextButton():
    #initialize botton`s pisition, text, font, color
    def __init__(self, x, y, text, font, text_color):
        self.text = text                #text displayed on the botton
        self.font = font                #text`s font
        self.text_color = text_color    #text`s color
        self.clicked = False            #tracks if the botton has been clicked

        # Render text into an image surface
        self.image = self.font.render(self.text, True, self.text_color)
        #get the rectangle of the rendered text image and define the position of rect based on the center x,y
        self.rect = self.image.get_rect(center=(x, y))

    def draw(self):
        action = False                #variable to track whether button is clicked
        pos = pygame.mouse.get_pos()  #get current mouse position

        # Draw text
        screen.blit(self.image, self.rect)

        # Click detection
        if self.rect.collidepoint(pos):
            #check if the left mouse button[0] is clicked and was not before
            if pygame.mouse.get_pressed()[0] == 1 and not self.clicked:
                self.clicked = True #mark the button as clicked
                action = True       #set action to true when clicked detected
        if pygame.mouse.get_pressed()[0] == 0:
            self.clicked = False #reset the clicked variable, to be clicked again in the future.

        return action #return true if button is clicked


 # create button images
startGame_button = TextButton(105, 687.5, "Start game", font, WHITE)
try_again_button = TextButton(93, 690, "Try Again", font, WHITE)
exit_button = TextButton(60, 750, "Exit", font, WHITE)
instructions_button = TextButton(112, 630, "Instructions", font, WHITE)
back_button = TextButton(60, 750, "Back", font, WHITE)

def get_level(score): #calculate level. every 500 points = 1 level
    return score // 100+1

def draw_volume_icon(screen, is_muted, mute_img, unmute_img):
    if is_muted: #if mute is true, draw mute icon. else draw unmute icon
        screen.blit(mute_img, (550, 750))
    else:
        screen.blit(unmute_img, (550, 750))


def start_game(game_data):
    global dog, dog_group, dangers_group, goods_group, hog_group, medkit_group
    global spawn_timer_dangers, spawn_timer_goods, spawn_timer_hogs, spawn_timer_medkit
    global countdown, last_count, intro_played

    # Reset spawn timers
    spawn_timer_dangers = 0
    spawn_timer_goods = 0
    spawn_timer_hogs = 0
    spawn_timer_medkit = 0

    # Reset game variables
    game_data.score = 0
    game_data.level = 1
    game_data.previous_level = 1
    game_data.max_danger_speed = 2
    game_data.max_goods_speed = 2
    countdown = 3
    last_count = pygame.time.get_ticks()
    intro_played = False

    # Reset sprite groups
    dangers_group = pygame.sprite.Group()
    goods_group = pygame.sprite.Group()
    hog_group = pygame.sprite.Group()
    medkit_group = pygame.sprite.Group()
    dog_group = pygame.sprite.Group()

    # Create the player dog sprite and add it to its group
    dog = Dog(x=WIDTH//2, y=100, health=3, player_images=player_images, screen_width=WIDTH, screen_height=HEIGHT)
    dog_group.add(dog)

    #set game volume
    set_volume()

def handle_menu():
    #when game state = "menu"
    screen.blit(menu_bg, (0, 0)) #draw background
    #draw buttons
    startGame_button.draw()
    exit_button.draw()
    instructions_button.draw()

    draw_volume_icon(screen, is_muted, mute_img, unmute_img)

    pygame.display.update()

def handle_gameover():
    #when game state = "gameover"
    screen.blit(gameOver_bg, (0, 0)) #draw background
    #draw buttons
    exit_button.draw()
    try_again_button.draw()

    score_text = font.render(f"Your Score: {game_data.score}", True, WHITE)
    screen.blit(score_text, (WIDTH//2 - 100, 150)) #draw player`s score on gameover background

    draw_volume_icon(screen, is_muted, mute_img, unmute_img)

    pygame.display.update()

def handle_instructions():
    #when game state = "instructions"
    screen.blit(instructions_bg, (0, 0)) #draw background
    #draw back button
    back_button.draw()

    draw_volume_icon(screen, is_muted, mute_img, unmute_img)
    pygame.display.update()

def handle_playing():
    #when game state = "playing"
    if not paused: #if paused == False
        global spawn_timer_dangers, spawn_timer_goods, spawn_timer_hogs, spawn_timer_medkit
        global countdown, last_count, max_danger_speed, game_state, intro_played

        draw_bg() #draw gameplay background
        draw_volume_icon(screen, is_muted, mute_img, unmute_img)

        # count down logic
        if countdown > 0: #when countdown > 0 print txts and start countdown
            draw_text("GET READY!", font, WHITE, WIDTH // 2 - 80, HEIGHT // 2 - 25)
            draw_text(str(countdown), font, WHITE, WIDTH // 2 - 5, HEIGHT // 2 + 5)
            count_timer = pygame.time.get_ticks() #get the current time in milliseconds

            if countdown == 3 and not intro_played: #play intro when countdown starts
                intro_fx.play()
                intro_played = True

            if count_timer - last_count > 1000: #check if 1000 milliseconds (1 sec) has passed
                countdown -= 1 #decrease countdown by 1
                last_count = count_timer #update the last counter tick time

            dog_group.draw(screen)
            draw_text(f"Level {game_data.level}", font, WHITE, WIDTH - 130, 10)
            score_text = font.render(f"Score: {game_data.score}", True, WHITE)
            screen.blit(score_text, (10, 10))
            #draw dog`s hearts icon
            dog.draw_hearts(screen, full_heart, empty_heart, heart_size)
            pygame.display.update()
            play_music(game_play_music)

            return #makes sure the game logic does not start until count down is complete.

        else: #after count down - game logic will begin.
            #increament timers every frame
            spawn_timer_dangers += 1
            spawn_timer_goods += 1
            spawn_timer_hogs += 1
            spawn_timer_medkit += 1

            # get a random speed between min speed and max speed
            # random.uniform - returns a float in range
            danger_current_speed = random.uniform(min_dangers_speed, game_data.max_danger_speed)
            goods_current_speed = random.uniform(min_goods_speed, game_data.max_goods_speed)

            # update key pressed - for dog movement logic
            key = pygame.key.get_pressed()

            # objects spawn logic
            # if timer >= spawn_rate - an object will spawn. after; the timer resets
            if spawn_timer_dangers >= dangers_spawn_rate:
                image = random.choice(danger_images)
                x = random.randint(25, 570) #random X position

                new_danger = Dangers(image, x, y=HEIGHT, speed=danger_current_speed,
                                     dog_group=dog_group, dog=dog, dogyelp_fx=dogyelp_fx)

                dangers_group.add(new_danger)
                spawn_timer_dangers = 0 #reset spawn timer

            if spawn_timer_goods >= goods_spawn_rate:
                image = random.choice(goods_images)
                x = random.randint(25, 570) #random X position
                new_goods = Goods(image, x, y=HEIGHT, speed=goods_current_speed, dog_group=dog_group, dog=dog,
                                  chewing_fx=chewing_fx, game_data=game_data)

                goods_group.add(new_goods)
                spawn_timer_goods = 0 #reset spawn timer

            # at level 5 hogs will start apearing
            if game_data.level >= 5 and spawn_timer_hogs >= hogs_spawn_rate:

                hog = Hog(speed=hogs_speed, dog_group=dog_group, dog=dog, images=hog_images,
                          width=WIDTH, height=HEIGHT, dogyelp_fx=dogyelp_fx, hog_fx=hog_fx)
                hog_group.add(hog)
                spawn_timer_hogs = 0 #reset spawn timer

            # at level 3, medkits will start apearing
            if game_data.level >= 3 and spawn_timer_medkit >= medkit_spawn_rate:
                image = medkit_image
                x = random.randint(25, 570) #random X position
                new_med = MedKit(image, x, y=HEIGHT, speed=medkit_speed, dog_group=dog_group,
                                 dog=dog, game_data=game_data, medkit_fx=medkit_fx)

                medkit_group.add(new_med)
                spawn_timer_medkit = 0 #reset spawn timer

            # update groups - according to update functions of the groups.
            dangers_group.update()
            dog_group.update(key) #update key to get dog`s movement direction

            if dog.dead:
                game_state = "gameover"

            goods_group.update()
            hog_group.update()
            medkit_group.update()

            # draw objects
            dangers_group.draw(screen)
            dog_group.draw(screen)
            goods_group.draw(screen)
            hog_group.draw(screen)
            dog.draw_hearts(screen, full_heart, empty_heart, heart_size)
            medkit_group.draw(screen)

            # draw score
            score_text = font.render(f"Score: {game_data.score}", True, WHITE)
            screen.blit(score_text, (10, 10))

            # draw current level
            game_data.level = get_level(game_data.score)
            draw_text(f"Level {game_data.level}", font, WHITE, WIDTH - 130, 10)

            # update game difficulty each level
            if game_data.level > game_data.previous_level:
                game_data.max_danger_speed += 0.5
                game_data.max_goods_speed += 0.1
                if game_data.level % 2 == 0: # every even number level dog speed will increase
                    dog.speed += 0.1
                    if dog.speed == 7:
                        dog.speed = 7 #max speed.

                game_data.previous_level = game_data.level #track the previouse level

            pygame.display.update()
    else: #else -> if game is pause
        draw_text("PAUSED", font, WHITE,WIDTH // 2 - 50, HEIGHT // 2- 50)
        pygame.display.update()


def main():
    global run, last_game_state
    global dangers_group, dog_group, hog_group, medkit_group, goods_group
    global startGame_botton, try_again_button, exit_button, instructions_button, back_button
    global paused, game_state


    # create sprite groups
    dangers_group = pygame.sprite.Group()
    dog_group = pygame.sprite.Group()
    goods_group = pygame.sprite.Group()
    hog_group = pygame.sprite.Group()
    medkit_group = pygame.sprite.Group()
    #keep track of the previous game state
    last_game_state = None

    run = True
    while run: #main game loop
        clock.tick(fps)

        # control music according to game state
        if game_state != last_game_state:
            if game_state == "menu" and last_game_state != "instructions":
                play_music(menu_music)

            elif game_state == "playing":
                play_music(game_play_music)

            elif game_state == "gameover":
                 pygame.mixer.music.stop() #stop any song playing
                 game_over_fx.play() #play sound effect

            last_game_state = game_state

        # EVENT HANDELING SECTION
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False #quit if window is closed

            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mouse_pos = event.pos #get mouse position when left-click

                #handle mouse interaction in "menu" state
                if game_state == "menu":
                    if startGame_button.rect.collidepoint(mouse_pos): #if play button is clicked
                        start_game(game_data)
                        game_state = "playing"


                    elif instructions_button.rect.collidepoint(mouse_pos): #if instructions button is clicked
                        game_state = "instructions"

                    elif exit_button.rect.collidepoint(mouse_pos): #if exit button is clicked
                        run = False

                elif game_state == "gameover":
                    if try_again_button.rect.collidepoint(mouse_pos): #if try again button is clicked
                        start_game(game_data)
                        game_over_fx.stop()
                        game_state = "playing"
                    elif exit_button.rect.collidepoint(mouse_pos): #if exit button is clicked
                        run = False

                elif game_state == "instructions":
                    if back_button.rect.collidepoint(mouse_pos): #if back button is clicked
                        game_state = "menu"

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_m: #if M button is clicked
                    toggle_mute()
                elif event.key == pygame.K_ESCAPE and game_state == "playing": #if ESC is clicked
                    paused = not paused
                    toggle_mute()

        # MAIN MENU SECTION
        if game_state == "menu":
            handle_menu()

        # GAME RUNNING SECTION
        elif game_state == "playing":
            handle_playing()

        # GAME OVER SECTION
        elif game_state == "gameover":
            handle_gameover()

        elif game_state == "instructions":
            handle_instructions()

    pygame.quit()
    sys.exit()

if __name__ == '__main__':
    main()