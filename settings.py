import pygame

class Settings:
    '''A class to store all settings for Alien Invasion'''

    def __init__(self):
        '''
        initialize the game's setting
        '''
        #screen Settings
        self.screen_width = 1280
        self.screen_height = 680
        self.bg_color = "#00084D" # warna background

        # Background setting
        self.background_image = pygame.image.load("images/bg.bmp")
        self.background_image = pygame.transform.scale(self.background_image, (self.screen_width, self.screen_height))
        self.rect = self.background_image.get_rect()

        # ship settings
        self.ship_speed = 1
        self.ship_limit = 3

        # bullet settings
        self.bullet_speed = 1.0
        self.bullet_width = 3
        self.bullet_height = 15
        self.bullet_color = "#eae7af"
        self.bullet_allowed = 3

        # Alien settings
        self.alien_speed = 1.0
        self.fleet_drop_speed = 10
        # fleet_direction of 1 represents right; -1 represents left.
        self.fleet_direction = 1

        # how quickly the game speeds up
        self.speedup_scale = 1.1

        # How quickly the alien point values increase
        self.score_scale = 1.5

        self.initialize_dynamic_settings()

    
    def initialize_dynamic_settings(self):
        self.ship_speed = 1.0
        self.bullet_speed = 1.0
        self.alien_speed = 1.0

        self.fleet_direction = 1 # Nentuin gerak kanan(1) atau kiri(-1) duluan

        # Scoring
        self.alien_points = 50


    def increase_speed(self):
        self.ship_speed *= self.speedup_scale
        self.bullet_speed *= self.speedup_scale
        self.alien_speed *= self.speedup_scale

        self.alien_points = int(self.alien_points * self.score_scale)

