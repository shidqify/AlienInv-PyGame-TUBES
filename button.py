import pygame.font

class Button:

    def __init__(self, ai_game, msg):
        '''
        Initialize Button
        '''
        self.screen = ai_game.screen
        self.screen_rect = self.screen.get_rect()

        # Set the button properties
        self.width, self.height = 200, 50
        self.button_color = "#e94560"
        self.text_color = "#16213e"
        self.font = pygame.font.SysFont(None, 48)

        # Build a button and place it
        self.rect = pygame.Rect(0, 0, self.width, self.height)
        self.rect.center = self.screen_rect.center
        
        # The massages in the button
        self._prep_msg(msg)


    def _prep_msg(self, msg):
        '''
        Show massage
        '''
        self.msg_image = self.font.render(msg, True, self.text_color, self.button_color)
        self.msg_image_rect = self.msg_image.get_rect()
        self.msg_image_rect.center = self.rect.center

    
    def draw_button(self):
        self.screen.fill(self.button_color, self.rect)
        self.screen.blit(self.msg_image, self.msg_image_rect)

