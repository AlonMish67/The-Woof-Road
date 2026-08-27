import pygame, random

#Good stuff class
class Goods(pygame.sprite.Sprite):
    # init function gets called everytime a new object is created with the values passed for it.
    def __init__(self, image, x, y, speed, dog_group, dog,chewing_fx,game_data):
        pygame.sprite.Sprite.__init__(self) #initializes the base Sprite class so the object works with Pygame`s sprite system.
        #initialize "self" object with all the values that has been passed for it
        self.image = image
        self.rect = self.image.get_rect(center=(x, y))
        self.speed = speed
        self.dog_group = dog_group
        self.dog = dog
        self.chewing_fx = chewing_fx
        self.game_data = game_data

    def update(self): #this function defines what the MetKit does every frame of the game.
        self.rect.y -= self.speed #move the item upward
        if self.rect.y < -100: #when the item got out of the screen - remove it
            self.kill()
        #check for collision between item and the character (dog)
        hit_player = pygame.sprite.spritecollide(self, self.dog_group, False)
        if hit_player:
            self.kill()  #remove stuff after collision
            self.chewing_fx.play()
            self.game_data.score += 50

#medkit class
class MedKit(pygame.sprite.Sprite):
    #init function gets called everytime a new object is created with the values passed for it.
    def __init__(self, image, x, y, speed, dog_group, dog, game_data, medkit_fx):
        pygame.sprite.Sprite.__init__(self) #initializes the base Sprite class so the object works with Pygame`s sprite system.
        # initialize "self" object with all the values that has been passed for it
        self.image = image
        self.rect = self.image.get_rect(center=(x, y))
        self.speed = speed
        self.dog_group = dog_group
        self.dog = dog
        self.game_data = game_data
        self.medkit_fx = medkit_fx


    def update(self): #this function defines what the MetKit does every frame of the game.
        self.rect.y -= self.speed #move upward
        if self.rect.y < -100: #when the item got out of the screen - remove it
            self.kill()
        # check for collision between medkit and the character (dog)
        hit_player = pygame.sprite.spritecollide(self, self.dog_group, False)
        if hit_player:
            self.medkit_fx.play()
            if self.dog.health_remaining < 3:
                self.dog.health_remaining += 1
            else:  #if health is already full
                self.game_data.score += 100

            self.kill() #remove medkit after collision
