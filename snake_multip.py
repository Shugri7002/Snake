import tkinter
import random

ROWS = 25
COLS = 25
TILE_SIZE = 25

WINDOW_WIDTH = TILE_SIZE * COLS
WINDOW_HEIGHT= TILE_SIZE * ROWS

class Tile:  
 def __init__(self, x,y):
     self.x = x
     self.y = y

#game window
window = tkinter.Tk()
window.title("Snake")
window.resizable(False, False)

canvas = tkinter.Canvas(window, bg ="black", width= WINDOW_WIDTH, height = WINDOW_HEIGHT, borderwidth = 0, highlightthickness=0)
canvas.pack()
window.update()

#center the window
window_width = window.winfo_width()
window_height= window.winfo_height()
screen_width = window.winfo_screenwidth()
screen_height = window.winfo_screenheight()
window_x = int((screen_width/2)- (window_width/2))
window_y = int((screen_height/2)- (window_height/2))
#format "(w)x(h)+(x)(y)"
window.geometry(f"{window_width}x{window_height}+{window_x}+{window_y}")

#initialize game
#player 1 (WASD-green)
snake = Tile(5*TILE_SIZE, 5*TILE_SIZE) #single tile, snake's head
snake_body = [] #multiple snake tiles
velocityX = 0
velocityY = 0
score = 0

#player 2 (Arrows-pink)
snake2 = Tile(15*TILE_SIZE, 15*TILE_SIZE) #single tile, snake's head
snake2_body = [] #multiple snake tiles
velocity2X = 0
velocity2Y = 0
score2 = 0

#shared objects
food = Tile(10*TILE_SIZE, 10*TILE_SIZE)
game_over = False

def change_direction(e): #e = event
   #print(e)
   #print(e.keysym)
   global velocityX, velocityY, velocity2X, velocity2Y
   if(game_over):
      return

    #player 1(WASD)
    #Player 2 (Arrows)
   if((e.keysym == "w" or e.keysym =="W") and velocityY != 1):
      velocityX = 0
      velocityY = -1
   elif((e.keysym == "s" or e.keysym =="S") and velocityY != -1):
      velocityX = 0
      velocityY = 1
   elif((e.keysym == "a" or e.keysym =="A") and velocityX != 1):
      velocityX = -1
      velocityY = 0
   elif((e.keysym == "d" or e.keysym =="D") and velocityX != -1):
      velocityX = 1
      velocityY = 0

    #Player 2 (Arrows)
   if(e.keysym == "Up" and velocity2Y != 1):
      velocity2X = 0
      velocity2Y = -1
   elif(e.keysym == "Down" and velocity2Y != -1):
      velocity2X = 0
      velocity2Y = 1
   elif(e.keysym == "Left" and velocity2X != 1):
      velocity2X = -1
      velocity2Y = 0
   elif(e.keysym == "Right" and velocity2X != -1):
      velocity2X = 1
      velocity2Y = 0

def  move():
   global snake,snake2, food, snake_body, snake2_body, game_over, score, score2
   if (game_over):
      return

    #player 1 wall
   if(snake.x < 0 or snake.x >= WINDOW_WIDTH or snake.y < 0 or snake.y >= WINDOW_HEIGHT):
    game_over = True
    return
   
   #player 1 self
   for tile in snake_body:
      if(snake.x== tile.x and snake.y == tile.y):
          game_over = True
          return

   #player 1 eats
   if (snake.x == food.x and snake.y == food.y):
      snake_body.append(Tile(food.x, food.y))
      food.x = random.randint(0, COLS-1) * TILE_SIZE
      food.y = random.randint(0, ROWS-1) * TILE_SIZE
      score += 1

   #player tail follow   
   for i in range (len(snake_body)-1, -1, -1):
      tile = snake_body[i]
      if(i == 0):
         tile.x = snake.x 
         tile.y = snake.y
      else:
         prev_tile=snake_body[i-1]
         tile.x = prev_tile.x
         tile.y = prev_tile.y

     #player 1 move head
      snake.x += velocityX * TILE_SIZE
      snake.y += velocityY * TILE_SIZE


    #player 2 wall
   if(snake2.x < 0 or snake2.x >= WINDOW_WIDTH or snake2.y < 0 or snake2.y >= WINDOW_HEIGHT):
     game_over = True
     return
   
   #player 2 self
   for tile in snake2_body:
      if(snake2.x== tile.x and snake2.y == tile.y):
          game_over = True
          return

   #player 2 eats
   if (snake2.x == food.x and snake2.y == food.y):
      snake2_body.append(Tile(food.x, food.y))
      food.x = random.randint(0, COLS-1) * TILE_SIZE
      food.y = random.randint(0, ROWS-1) * TILE_SIZE
      score2 += 1

   #player 2 tail follow   
   for i in range (len(snake2_body)-1, -1, -1):
      tile = snake2_body[i]
      if(i == 0):
         tile.x = snake2.x 
         tile.y = snake2.y
      else:
         prev_tile=snake2_body[i-1]
         tile.x = prev_tile.x
         tile.y = prev_tile.y

     #player 2 move head
      snake2.x += velocity2X * TILE_SIZE
      snake2.y += velocity2Y * TILE_SIZE



    #Player 2(Arrow)
   if(snake2.x < 0 or snake2.x >= WINDOW_WIDTH or snake2.y < 0 or snake2.y >= WINDOW_HEIGHT):
     game_over = True
     return

   for tile in snake2_body:
      if(snake2.x== tile.x and snake2.y == tile.y):
          game_over = True
          return

   #collision
   if (snake2.x == food.x and snake2.y == food.y):
      snake2_body.append(Tile(food.x, food.y))
      food.x = random.randint(0, COLS-1) * TILE_SIZE
      food.y = random.randint(0, ROWS-1) * TILE_SIZE
      score2 += 1

   #update snake body    
   for i in range (len(snake2_body)-1, -1, -1):
      tile = snake2_body[i]
      if(i == 0):
         tile.x = snake2.x 
         tile.y = snake2.y
      else:
         prev_tile=snake2_body[i-1]
         tile.x = prev_tile.x
         tile.y = prev_tile.y

   snake2.x += velocity2X * TILE_SIZE
   snake2.y += velocity2Y * TILE_SIZE

def draw():
   global snake,snake2, food, snake_body, snake2_body, game_over, score, score2
   move()
 
   canvas.delete("all")

   #draw food
   canvas.create_rectangle(food.x, food.y, food.x + TILE_SIZE, food.y + TILE_SIZE, fill= "red")
   
   #draw snake 
   canvas.create_rectangle(snake.x, snake.y, snake.x + TILE_SIZE, snake.y + TILE_SIZE, fill = "lime green")
 
   for tile in snake_body:
    canvas.create_rectangle(tile.x, tile.y, tile.x +TILE_SIZE, tile.y + TILE_SIZE, fill="lime green" )
   
   if(game_over):
      canvas.create_text(window_width/2, WINDOW_HEIGHT/2, font = "Arial 20", text = f"Game Over: {score}", fill="white") 
   else:
      canvas.create_text(30, 20, font= "Arial 10", text = f"Score: {score}", fill= "white")
   window.after(100, draw) #100ms = 1/10 second, 10 frames/second

draw()

window.bind("<KeyRelease>", change_direction)
window.mainloop()