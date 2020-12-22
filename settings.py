class Settings:
    '''A class to store all settings for Alien Invasion'''

    def __init__(self):
        '''
        initialize the game's setting
        '''
        #screen Settings
        self.screen_width = 960
        self.screen_height = 720
        self.bg_color = (230, 230, 230) # warna background

        # ship settings
        self.ship_speed = 1.5
        self.ship_limit = 3

        # bullet settings
        self.bullet_speed = 1.0
        self.bullet_width = 3
        self.bullet_height = 15
        self.bullet_color = (60, 60, 60)
        self.bullet_allowed = 3

        # Alien settings
        self.alien_speed = 1.0
        self.fleet_drop_speed = 10
        # fleet_direction of 1 represents right; -1 represents left.
        self.fleet_direction = 1
