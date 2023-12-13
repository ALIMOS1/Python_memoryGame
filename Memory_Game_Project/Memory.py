import pygame
import random
import time 
# User-defined functions

def main():
   # initialize all pygame modules (some need initialization)
   pygame.init()
   # create a pygame display window
   pygame.display.set_mode((500, 400))
   # set the title of the display window
   pygame.display.set_caption('Memory')   
   # get the display surface
   w_surface = pygame.display.get_surface() 
   # create a game object
   game = Game(w_surface)
   # start the main game loop by calling the play method on the game object
   game.play() 
   # quit pygame and clean up the pygame window
   pygame.quit() 


# User-defined classes

class Game:
   # An object in this class represents a complete game.

   def __init__(self, surface):
      # Initialize a Game.
      # - self is the Game to initialize
      # - surface is the display window surface object

      # === objects that are part of every game that we will discuss
      self.surface = surface
      self.bg_color = pygame.Color('black')
      
      self.FPS = 60
      self.game_Clock = pygame.time.Clock()
      self.close_clicked = False
      self.continue_game = True
      
      # === game specific objects
      self.board_size = 4
      self.image_list = []
      self.load_images()
      self.board = [] # a list of lists
      self.create_board()
      self.filled =  []
      self.matched = []
      self.score = 0



   def load_images(self):
      # Do the following steps 8 times image1 - image 8 
      all_pic=['image1.bmp','image2.bmp','image3.bmp','image4.bmp','image5.bmp','image6.bmp','image7.bmp','image8.bmp']
      for i in all_pic:
         image = pygame.image.load(i)
         self.image_list.append(image)
         self.image_list.append(image)
      random.shuffle(self.image_list)
      




   def create_board(self):
      #width = self.surface.get_width()//self.board_size
      #height= self.surface.get_height()//self.board_size
      image_index = 0
      for row_index in range(0,self.board_size):
            row = []
            for col_index in range(0, self.board_size):
               image = self.image_list[image_index]
               image_index +=1
               width  = image.get_width()
               height = image.get_height()
               x= col_index*width
               y= row_index*height
               tile = Tile(x,y,width,height,image,self.surface)
               row.append(tile)
            self.board.append(row)
       


   def play(self):
      # Play the game until the player presses the close box.
      # - self is the Game that should be continued or not.

      while not self.close_clicked:  # until player clicks close box
         # play frame
         self.handle_events()
         self.draw()            
         if self.continue_game:
            self.update()
            self.decide_continue()
         self.game_Clock.tick(self.FPS) # run at most with FPS Frames Per Second 

   def handle_events(self):
      # Handle each user event by changing the game state appropriately.
      # - self is the Game whose events will be handled

      events = pygame.event.get()
      for event in events:
         if event.type == pygame.QUIT:
            self.close_clicked = True
         if event.type == pygame.MOUSEBUTTONUP and self.continue_game:
            self.handle_mouse_up(event.pos) # even.pos is (x,y) tuple ---> position of click    
            
            
   def handle_mouse_up(self,position):
      # position is the location of the click
      for row in self.board:
         for tile in row:
            if tile.select(position): # select method is in Tile Class
               if tile not in self.filled :
                  self.filled.append(tile)
                  print(len(self.filled))
               
               
               
   def draw(self):
      # Draw all game objects.
      # - self is the Game to draw
      
      self.surface.fill(self.bg_color) # clear the display surface first
      self.draw_score()

      
      # Draw the board
      for row in self.board:
         for tile in row:
            tile.draw()
      
      pygame.display.update() # make the updated surface appear on the display
   
   def draw_score(self): # draws a text into the surface 
   
      score_string = str(self.score)
      # step 1 create a font object
      font_size = 80
      fg_color = pygame.Color('white')
      font = pygame.font.SysFont('', font_size)
      # step 2 render the font
      text_box = font.render(score_string,True, fg_color, self.bg_color)
      # step 3 compute the location
      location=(400,0)
      # step 4 blit the source surface on the target surface
      self.surface.blit(text_box,location)   
   
   def update(self):
      self.score = pygame.time.get_ticks()//1000
      
      if len(self.filled) == 2:
         first = self.filled[0]
         second = self.filled[1]
         # important for memory 
         if first.is_equal(second):
            self.matched.append(second)
            self.matched.append(first)
            self.filled = []
         else:
            self.filled = []
            time.sleep(1)
      

      
   def decide_continue(self):
      if len(self.matched) == self.board_size**2:
         self.continue_game = False 
      



class Tile:
    
   def __init__(self,x,y,width,height,image,surface):
         self.rect = pygame.Rect(x,y,width,height)
         self.color = pygame.Color('white')
         self.border_width = 3 # This is how bold the tile is 
         self.surface = surface
         self.content = image
         self.hidden_image = pygame.image.load('image0.bmp')
         self.hidden = True # Show the question mark image if false show the content
         
   
   def select(self, position):
      
      if self.rect.collidepoint(position): # is there a click
         self.hidden = False
         return True 
   
   
   def is_equal(self, other):
      
      if self.content == other.content:
         self.hidden = False
         other.hidden = False
         return True 
      
      else: 
         self.hidden = True
         other.hidden = True 
         return False
   
   
   
   def draw(self):
      location = (self.rect.x, self.rect.y)
      
      if self.hidden == True: # Draw the question mark 
         self.surface.blit(self.hidden_image,location)
      else:
         self.surface.blit(self.content,location)
      pygame.draw.rect(self.surface,self.color,self.rect,self.border_width)



               
      #self.draw_content()
   def draw_content(self):
      font = pygame.font.SysFont(' ',133) #height of surface is 400//3=133
      # text_box is a pygame.Surface object - get the rectangle from the surface
      text_box = font.render(self.content, True, self.color)
      # here we will get the rect coordinates 
      rect1 = text_box.get_rect()
      
      rect1.center =  self.rect.center
      location = (rect1.x, rect1.y)
      self.surface.blit(text_box,location)
      
      
      

      
main()
