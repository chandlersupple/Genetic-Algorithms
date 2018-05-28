import math
import pygame
import random
from pygame.locals import *

pygame.init()

master = pygame.display.set_mode((1000,500))
pygame.display.set_caption('Creature Feature')

clock = pygame.time.Clock()

green = (67, 255, 0)
blue = (0, 208, 255)
black = (0, 0, 0)
white = (254, 255, 239)

food_dict = {}
bot_dict = {}

consumed_sorted = []

consumed_size_min = 5
consumed_size_max = 50
consumed_perspective_min = 0
consumed_perspective_max = 600
consumed_speed_min = 0
consumed_speed_max = 8

food_once = 0
bot_once = 0
game_over_once = 0

game_num = 1

def reset():
    global food_dict, bot_dict, food_once, bot_once, game_over_once, consumed_sorted
    global consumed_size_min, consumed_perspective_min, consumed_speed_min
    consumed_size_min = bot_dict[((consumed_sorted[2])[1])].size
    consumed_perspective_min = math.sqrt(bot_dict[((consumed_sorted[2])[1])].perspective)
    consumed_speed_min = bot_dict[((consumed_sorted[2])[1])].speed
    food_dict = {}
    bot_dict = {}
    consumed_sorted = []
    food_once = 0
    bot_once = 0
    game_over_once = 0
    
class Food:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        
    def update(self):
        pygame.draw.circle(master, blue, (self.x, self.y), 5, 0)
    
class Bot:
    def __init__(self, x, y, name):
        global consumed_size_min, consumed_perspective_min, consumed_speed_min
        self.x = x
        self.y = y
        self.name = name
        self.size = random.randint(consumed_size_min, 50)
        self.perspective = (random.randint(consumed_perspective_min, 600)**2)
        self.speed = random.randint(consumed_speed_min, 8)
        self.consumed = 0
                
    def distance(self):
        global game_over_once, game_num, consumed_sorted
        distance_list = []
        for food in range (0, 200):
            if ('food%s' %food) in food_dict:
                distance = (((self.x - (food_dict[('food%s' %food)].x))**2) + ((self.y - (food_dict[('food%s' %food)].y))**2))
                distance_list.append((distance, ('food%s' %food)))
            else:
                food = food + 1
        sorted_distance = sorted(distance_list, key=lambda tup: tup[0])
        if (len(sorted_distance) > 0):
            closest_num, closest_name = sorted_distance[0]
            if (self.perspective >= closest_num):
                if (((food_dict[closest_name].x) - self.x) < 0):
                    self.x = self.x - self.speed
                if (((food_dict[closest_name].x) - self.x) > 0):
                    self.x = self.x + self.speed
                if (((food_dict[closest_name].y) - self.y) < 0):
                    self.y = self.y - self.speed
                if (((food_dict[closest_name].y) - self.y) > 0):
                    self.y = self.y + self.speed

            if ((abs((food_dict[closest_name].y) - self.y)) <= self.size and abs((food_dict[closest_name].x) - self.x) <= self.size):
                self.consumed = self.consumed + 1
                del food_dict[closest_name]
        else:
            if (game_over_once == 0):
                print('Epoch %s' %game_num)
                game_num = game_num + 1
                game_over_once = 1
                consumed = []
                consumed_sorted = []
                for bot in range (0, 20):
                    consumed.append((bot_dict[('bot%s' %bot)].consumed, bot_dict[('bot%s' %bot)].name))
                consumed_sorted = sorted(consumed, key=lambda tup: tup[0])
                print(consumed_sorted)
                reset()
            
    def update(self):
        pygame.draw.circle(master, green, (self.x, self.y), self.size, 0)
                
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
    
    master.fill(white)
    
    if (food_once == 0):
        for food in range (0, 200):
            food_x_init = random.randint(0,1000)
            food_y_init = random.randint(0,500)
            food_dict[('food{0}').format(food)] = Food(food_x_init, food_y_init)
        food_once = 1
        
    for food in range (0, 200):
        if ('food%s' %food) in food_dict:
            food_dict[('food%s' %food)].update()
        else:
            food = food + 1
        
    if (bot_once == 0):
        for bot in range (0, 20):
            bot_x_init = random.randint(0,1000)
            bot_y_init = random.randint(0,500)
            bot_dict[('bot{0}').format(bot)] = Bot(bot_x_init, bot_y_init, ('bot%s' %bot))
        bot_once = 1
    
    for bot in range (0, 20):
        if (len(bot_dict) > 1):
            bot_dict[('bot%s' %bot)].distance()
            if (len(bot_dict) > 1):
                bot_dict[('bot%s' %bot)].update()
        
    pygame.display.flip()
    clock.tick(30)
