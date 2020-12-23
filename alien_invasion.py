import sys
from time import sleep
import pygame
from pygame import mixer
from settings import Settings
from game_stats import GameStats
from scoreboard import Scoreboard
from button import Button
from ship import Ship
from bullet import Bullet
from alien import Alien


class AlienInvasion:
    '''
    Overall class to manage game assets and behavior.
    '''
    def __init__(self):
        '''
        initialize the game, and create game resources.
        '''
        pygame.init()
        self.settings = Settings()

        self.screen = pygame.display.set_mode(
            (self.settings.screen_width, self.settings.screen_height)
        )

        # Icon
        ico = pygame.image.load("images/nintendo.ico")
        pygame.display.set_icon(ico)
        
        #Fullscreen
        # self.screen = pygame.display.set_mode((0,0), pygame.FULLSCREEN)
        # self.settings.screen_width = self.screen.get_rect().width
        # self.settings.screen_height = self.screen.get_rect().height
        
        pygame.display.set_caption("Alien Invasion")

        # Crate an instance to store game statistic.
        self.stats = GameStats(self)
        self.sb = Scoreboard(self)

        self.ship = Ship(self)
        self.bullet = pygame.sprite.Group()
        self.aliens = pygame.sprite.Group()
        self.play_button = Button(self, "START")
        
        self._create_fleet()



    def run_game(self):
        '''
        Start the main loop for the game.
        '''
        while True:
            self._check_events()

            if self.stats.game_active:
                self.ship.update()
                self.bullet.update()
                self._update_bullets()
                self._update_aliens()
                
            self._update_screen()
            

    def _check_events(self):
        '''
        Respond to keypress and mouse events
        '''
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)
            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                self._check_play_button(mouse_pos)

    
    def _check_play_button(self, mouse_pos):
        '''
        Start a new game when the player clicks play
        '''
        button_clicked = self.play_button.rect.collidepoint(mouse_pos)
        if button_clicked and not self.stats.game_active:
            # reset the game
            self.settings.initialize_dynamic_settings()

            # Music plays
            mixer.music.load("images/ff7.wav")
            mixer.music.play(-1)
            mixer.music.set_volume(0.5)

            # Reset the game statistic
            self.stats.reset_stats()
            self.stats.game_active = True
            self.sb.prep_score()
            self.sb.prep_level()
            self.sb.prep_ships()

            # get rid of any remaining aliens and bullets
            self.aliens.empty()
            self.bullet.empty()

            # Create a new fleet and center the ships
            self._create_fleet()
            self.ship.center_ship()

            # Hide mouse cursor
            pygame.mouse.set_visible(False)
        

    def _check_keydown_events(self, event):
        '''
        respond to keypress
        '''
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = True
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = True
        elif event.key == pygame.K_q:
            sys.exit()
        elif event.key == pygame.K_SPACE:
            self._fire_bullet()
            shoot= mixer.Sound("images/shootbull.wav")
            shoot.set_volume(0.1)
            shoot.play()


    def _check_keyup_events(self, event):
        '''
        respond to key released.
        '''
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = False
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = False


    def _fire_bullet(self):
        '''
        Create a new bullet and add it to the bullets group
        '''
        if len(self.bullet) < self.settings.bullet_allowed:
            new_bullet = Bullet(self)
            self.bullet.add(new_bullet)


    def _update_bullets(self):
        '''
        Update position of bullets and get rid of old bullets
        '''
        # Update bullet position.
        self.bullet.update()

        # Get rid of bullets that have dissapeared.
        for bullet in self.bullet.copy():
            if bullet.rect.bottom <= 0:
                self.bullet.remove(bullet)

        self._check_bullet_alien_collisions()


    def _check_bullet_alien_collisions(self):
        '''
        respond to bullet-alien collisions.
        '''
        collisions = pygame.sprite.groupcollide(
            self.bullet, self.aliens, True, True
        )

        if collisions:
            for aliens in collisions.values():
                self.stats.score += self.settings.alien_points * len(aliens)
            self.sb.prep_score()
            self.sb.check_high_score()
            hit= mixer.Sound("images/hitalien.wav")
            hit.set_volume(0.2)
            hit.play()

        if not self.aliens:
            # Destroy existing bullets and create new fleet
            self.bullet.empty()
            self._create_fleet()
            self.settings.increase_speed()

            # Increase level
            self.stats.level += 1
            levelup = mixer.Sound("images/levelup.wav")
            levelup.set_volume(0.2)
            levelup.play()
            self.sb.prep_level()


    def _update_aliens(self):
        '''
        Check if the fleet is at edge, then update the positions of all aliens in the fleet.
        '''
        self._check_fleet_edges()
        self.aliens.update()

        # Look for alien-ship collisions.
        if pygame.sprite.spritecollideany(self.ship, self.aliens):
            self._ship_hit()

        # Look for aliens hitting the bottom of the screen
        self._check_aliens_bottom()


    def _check_aliens_bottom(self):
        '''
        check if any aliens have reached the bottom of the screen
        '''
        screen_rect = self.screen.get_rect()
        for alien in self.aliens.sprites():
            if alien.rect.bottom >= screen_rect.bottom:
                #Treat this the same as if the ship got hit
                self._ship_hit()
                break
    

    def _ship_hit(self):
        '''
        respond to the ship being hit by an alien
        '''
        if self.stats.ships_left > 0:
            # Decrement ships_left.
            self.stats.ships_left -= 1
            self.sb.prep_ships()

            #get rid of any remaining aliens and bullets.
            self.aliens.empty()
            self.bullet.empty()

            # Create a new fleet and center the ship.
            self._create_fleet()
            self.ship.center_ship()

            # sound when lost
            loselife = mixer.Sound("images/loselife.wav")
            loselife.set_volume(0.2)
            loselife.play()

            #pause
            sleep(0.5)
        else:
            self.stats.game_active = False
            pygame.mouse.set_visible(True)
            lost = mixer.Sound("images/lost.wav")
            lost.set_volume(1)
            lost.play()
            mixer.music.stop()



    def _create_fleet(self):
        '''
        Create the fleet of aliens
        '''
        #Create an alien and fine the number of aliens in a row
        # create between each alien is equal to one alien width
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size
        available_space_x = self.settings.screen_width - (2 * alien_width)
        number_aliens_x = available_space_x // (2 * alien_width)

        # Determine the number of rows of aliens that fit on the screen.
        ship_height = self.ship.rect.height
        available_space_y = (self.settings.screen_height - 
                                (3 * alien_height) - ship_height)
        number_rows = available_space_y // (2 * alien_height)

        # Create the full fleet of aliens
        for row_number in range(number_rows):
            for alien_number in range(number_aliens_x):
                self._create_alien(alien_number, row_number)
    

    def _create_alien(self, alien_number, row_number):
        '''
        create an alien and place it in the row
        '''
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size
        alien.x =  alien_width + 2 * alien_width * alien_number
        alien.rect.x = alien.x
        alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_number
        self.aliens.add(alien)


    def _check_fleet_edges(self):
        '''
        Respond appropriately if any aliens have reached an edge
        '''
        for alien in self.aliens.sprites():
            if alien.check_edges():
                self._change_fleet_direction()
                break
    

    def _change_fleet_direction(self):
        '''
        Drop the entire fleet and change the fleet's direction
        '''
        for alien in self.aliens.sprites():
            alien.rect.y += self.settings.fleet_drop_speed
        self.settings.fleet_direction *= -1


    def _update_screen(self):
        # Update images on the screen and flip to the new screen
        self.screen.blit(self.settings.background_image, (self.settings.rect))
        self.ship.blitme()
        for bullet in self.bullet.sprites():
            bullet.draw_bullet()
        self.aliens.draw(self.screen)

        # Draw the score information
        self.sb.show_score()

        # Draw the play button if the game is inactive
        if not self.stats.game_active:
            self.play_button.draw_button()

        pygame.display.flip()


if __name__ == '__main__':
    # make a game instance, and run the game.
    ai = AlienInvasion()
    ai.run_game()
  

