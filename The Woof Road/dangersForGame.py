import pygame, sys
from pygame.locals import *
import random


#Hog class
class Hog(pygame.sprite.Sprite):
    # init function gets called everytime a new object is created with the values passed for it.
    def __init__(self, speed, dog_group, dog, images, width, height, dogyelp_fx, hog_fx): #initializes the base Sprite class so the object works with Pygame`s sprite system.
        pygame.sprite.Sprite.__init__(self)
        # initialize "self" object with all the values that has been passed for it
        self.images = images
        self.WIDTH = width
        self.HEIGHT = height
        self.current_frame = 0
        self.animation_speed = 0.15

        self.direction = random.choice(['left', 'right']) #randomly chooses the direction the hog will run to
        self.speed = speed if self.direction == 'right' else -speed #initialize the speed according to direction
        self.dog_group = dog_group
        self.dog = dog
        self.hog_fx = hog_fx
        self.dogyelp_fx = dogyelp_fx


        y = random.randint( 100, self.HEIGHT - 100) #spawn hog at a random Y coordination

        # self.direction changes between 'right' and 'left', [0] = first image of the list!
        hog_width = self.images[self.direction][0].get_width()

        if self.direction == 'left': #hog moves from right to left
            x = self.WIDTH + hog_width # hog spawns off-screen

        else: #hog moves from the right
            x = -hog_width # hog will spawn off-screen


        self.image = self.images[self.direction][int(self.current_frame)] #update hog`s sprite image.
        self.rect = self.image.get_rect(center=(x, y)).inflate(-40,-35)

        hog_fx.play()


    def update(self):

        self.rect.x += self.speed #set movement speed

        self.current_frame += self.animation_speed #calculate which animation to use, depending on frame

        #reset when current_frame exceeds amount of image list
        if self.current_frame >= len(self.images[self.direction]):
            self.current_frame = 0

        self.image = self.images[self.direction][int(self.current_frame)]

        # Remove when off-screen
        if self.rect.right < -100 or self.rect.left > self.WIDTH +100:
            self.kill()

        #detect collision between hog and main character.
        hit_player = pygame.sprite.spritecollide(self, self.dog_group, False)
        if hit_player:
            self.kill()
            self.dogyelp_fx.play()
            self.dog.health_remaining -= 1


#Dangers class
class Dangers(pygame.sprite.Sprite):
    # init function gets called everytime a new object is created with the values passed for it.
    def __init__(self, image, x, y, speed, dog_group, dog, dogyelp_fx): #initializes the base Sprite class so the object works with Pygame`s sprite system.
        pygame.sprite.Sprite.__init__(self)
        # initialize "self" object with all the values that has been passed for it
        self.image = image
        self.rect = self.image.get_rect(center=(x, y))
        self.speed = speed
        self.dog_group = dog_group
        self.dog = dog
        self.dogyelp_fx = dogyelp_fx

    def update(self): # update object each frame
        self.rect.y -= self.speed
        if self.rect.y < -100:
            self.kill()

        # detect collisions
        hit_player = pygame.sprite.spritecollide(self, self.dog_group, False)
        if hit_player:
            self.kill()
            self.dogyelp_fx.play()
            self.dog.health_remaining -= 1
