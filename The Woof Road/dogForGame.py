import pygame

#dog class
class Dog(pygame.sprite.Sprite):
    # init function gets called everytime a new object is created with the values passed for it.
    def __init__(self, x, y, health, player_images, screen_width, screen_height):
        pygame.sprite.Sprite.__init__(self) #initializes the base Sprite class so the object works with Pygame`s sprite system.
        # dictionary of direction: list of frames {'left': [...], 'right: [...]...}
        self.images = player_images
        self.direction = 'down' #default starting direction
        self.current_frame = 0 #control animation timing
        self.animation_speed = 0.15 #controls how fast the animation is

        # set the initial image depending on direction
        self.image = self.images[self.direction][0]

        self.speed = 5
        self.dead = False

        # get full sprite rectangle
        full_rect = self.image.get_rect(center=(x, y))

        # make the collision box smaller for better hit-box
        collision_width = full_rect.width * 0.8
        collision_height = full_rect.height * 0.8

        # sets collision Rect from top left, then centers it on the character`s image
        self.rect = pygame.Rect(0, 0, collision_width, collision_height)
        self.rect.center = full_rect.center


        self.health_start = health
        self.health_remaining = health

        #inits screen bounds for movement limits.
        self.screen_width = screen_width
        self.screen_height = screen_height

    def update(self, key): #this function defines what the MetKit does every frame of the game.

        moving = False
        # Movement logic and boundry checking
        if key[pygame.K_LEFT] and self.rect.left > 0:
            self.rect.x -= self.speed
            self.direction = 'left'
            moving = True
        elif key[pygame.K_RIGHT] and self.rect.right < self.screen_width:
            self.rect.x += self.speed
            self.direction = 'right'
            moving = True
        elif key[pygame.K_UP] and self.rect.top > 0:
            self.rect.y -= self.speed
            self.direction = 'up'
            moving = True
        elif key[pygame.K_DOWN] and self.rect.bottom < self.screen_height -10:
            self.rect.y += self.speed
            self.direction = 'down'
            moving = True

        #Animation update
        if moving: #when character is moving
            self.current_frame += self.animation_speed #increment current_frame by animation_speed every frame in the game
            # when current frame is higher then the number of frames - reset it (create a loop)
            if self.current_frame >= len(self.images[self.direction]):
                self.current_frame = 0

            # sets characters`s image to the current frame image from the list for the current movement direction
            # int(): when current_frame is incremented by 0.15 the int() will floor it to 0. so we stay on image number 0
            # when the current_frame is above 1, int() will floor it to 1, so we stay on image number 1.
            self.image = self.images[self.direction][int(self.current_frame)]
        else:
            # Standing still — use first frame of current direction
            self.image = self.images[self.direction][0]

        if self.health_remaining <= 0:
            self.dead = True

    # HEALTH LOGIC - draws a row of hearts
    def draw_hearts(self, surface,full_heart,empty_heart,heart_size):
        max_hearts = int(self.health_start)
        current_health = int(self.health_remaining)

        for i in range(max_hearts):
            x = 6 + i * (heart_size + 5)  # position hearts with spacing
            y = 50
            if i < current_health:
                surface.blit(full_heart, (x, y)) #draw full heart
            else:
                surface.blit(empty_heart, (x, y)) #draw empty heart