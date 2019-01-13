#Pygame Crossing Game
#This game wants you to simply cross the road while avoiding obsticles
#Learning Python by writing this game.
#Jacalyn Boggs AKA Lady Ozma

#Import PyGame for libraries
import pygame

#The size of the play screen
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 800
SCREEN_TITLE = 'Crossing Game'
#RGB Colours
WHITE_COLOR = (255, 255, 255)
BLACK_COLOR = (0, 0, 0)
#The Clock usedto update game events and frames
clock = pygame.time.Clock()
pygame.font.init()
font = pygame.font.SysFont('papyrus', 75)

class Game:
    #Typical FPS rate of 60
    TICK_RATE = 60

    #Initializer for the game class - set up with width, height, title
    def __init__(self, image_path, width, height, title):
        self.width = width
        self.height = height
        self.title = title

        #Create  the window to specified size, in white, to display the game
        self.game_screen = pygame.display.set_mode((width, height))
        #Set window color to white
        self.game_screen.fill(WHITE_COLOR)
        #Set the window title
        pygame.display.set_caption(title)
        #Load and set the bckground imag
        background_image = pygame.image.load(image_path)
        self.image = pygame.transform.scale(background_image, (width, height))

    #Define the main game loop
    def run_game_loop(self, level_speed):
        #Set Game Is Not Over
        is_game_over = False
        did_win = False
        direction = 0

        #Set Player Character
        player_character = PlayerCharacter('player.png', 375, 700, 50, 50)
        #set Enemy Character
        enemy_0 = EnemyCharacter('enemy.png', 20, 600, 50, 50)
        enemy_0.SPEED *= level_speed
        enemy_1 = EnemyCharacter('enemy.png', self.width - 40, 400, 50, 50)
        enemy_1.SPEED *= level_speed
        enemy_2 = EnemyCharacter('enemy.png', 20, 200, 50, 50)
        enemy_2.SPEED *= level_speed
        #Set Treasure 
        treasure = GameObject('treasure.png', 375, 50, 50, 50)

        
        #This will run until the game ends
        while not is_game_over:

            #A loop to get all the events occuring at any single time
            #Events are most often mouse movement, mouse/button clicks, or exit events
            for event in pygame.event.get():
                #If we have a quit event, exit out of the game
                if event.type == pygame.QUIT:
                    is_game_over = True
                #Detect when a key is pressed down
                elif event.type == pygame.KEYDOWN:
                    #Move up if the key pressed
                    if event.key == pygame.K_UP:
                        direction = 1
                    #Move down if down key pressed
                    elif event.key == pygame.K_DOWN:
                        direction = -1
                #Detect whne key is released
                elif event.type == pygame.KEYUP:
                    #Stop movement when key is no longer pressed
                    if event.key == pygame.K_UP or event.key ==pygame.K_DOWN:
                        direction = 0
                print(event)
                
            #Redraw the screen to be a blank white window
            self.game_screen.fill(WHITE_COLOR)
            #Draw the image on to the background
            self.game_screen.blit(self.image, (0, 0))
            #Draw the treasure on the background
            treasure.draw(self.game_screen)

            #Update the player position
            player_character.move(direction, self.height)
            #Draw the player on the new position
            player_character.draw(self.game_screen)

            #Draw the Enemy character
            enemy_0.move(self.width)
            enemy_0.draw(self.game_screen)

            if level_speed > 2:
                enemy_1.move(self.width)
                enemy_1.draw(self.game_screen)
            if level_speed > 4:
                enemy_2.move(self.width)
                enemy_2.draw(self.game_screen)
                

            #Detect the Collision of Player with other objects
            #Collision ends the game
            #Collision with Enemy = Lose
            #Collision with Treasure = Win
            if player_character.detect_collision(enemy_0):
                is_game_over = True
                did_win = False
                text = font.render('LOSER :(', True, BLACK_COLOR)
                self.game_screen.blit(text, (300, 350))
                pygame.display.update()
                clock.tick(1)
                break
            elif player_character.detect_collision(treasure):
                is_game_over = True
                did_win = True
                text = font.render('WINNER :)', True, BLACK_COLOR)
                self.game_screen.blit(text, (300, 350))
                pygame.display.update()
                clock.tick(1)
                break

            #Update all the game graphics
            pygame.display.update()
            #Tick the clock to update everything within in the game
            clock.tick(self.TICK_RATE)

        #If player wins, they get to play again. If they lose, the game closes.
        if did_win:
            self.run_game_loop(level_speed + 0.5)
        else:
            return 

#This is a generic game object class. Other objects will subclass
class GameObject:

    def __init__(self, image_path, x, y, width, height):
        #Import Object
        object_image = pygame.image.load(image_path)
        #Scale Image
        self.image = pygame.transform.scale(object_image, (width, height))
        #Location of image
        self.x_pos = x
        self.y_pos = y
        self.width = width
        self.height = height

    #Draw the object with blit on the background of game screen
    def draw(self, background):
        background.blit(self.image, (self.x_pos, self.y_pos))

#This class is for the character controlled by the player
class PlayerCharacter(GameObject):
    #How many tiles the character moves per second 
    SPEED = 10
    def __init__(self, image_path, x, y, width, height):
        super().__init__(image_path, x, y, width, height)
        
    #This move function will move the character up or down               
    def move(self, direction, max_height):
        if direction > 0:
            self.y_pos -= self.SPEED
        elif direction < 0:
            self.y_pos += self.SPEED
        if self.y_pos >= max_height - 40:
            self.y_pos = max_height - 40

    #Detect collision on y access and the height/width of enemy
    def detect_collision(self, other_char):
        if self.y_pos > other_char.y_pos + other_char.height:
            return False
        elif self.y_pos + self.height < other_char.y_pos:
            return False
        
        if self.x_pos > other_char.x_pos + other_char.width:
            return False
        elif self.x_pos + self.width < other_char.x_pos:
            return False
        
        return True
        

class EnemyCharacter(GameObject):
    #How many tiles the enemy moves per second 
    SPEED = 10
    def __init__(self, image_path, x, y, width, height):
        super().__init__(image_path, x, y, width, height)
        
    #This move function will move the enemy left or right and turn from edge of screen              
    def move(self, max_width):
        if self.x_pos <= 20:
            self.SPEED = abs(self.SPEED)
        elif self.x_pos >= max_width - 40:
            self.SPEED = -abs(self.SPEED)
        self.x_pos += self.SPEED
    
#Initialize PyGame
pygame.init()

new_game = Game('background.png', SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)

new_game.run_game_loop(1)

#Quit pygame and the program
pygame.quit()
quit()
