import tkinter
import random

WHITE = "#ffffff"
NEON_GREEN = "#39FF14"
NEON_PINK = "#FF4FAE"
YELLOW = "#FFD34D"

FONT_TILE = ("Arial Black", 54)
FONT_H1 = ("Arial Black", 40)
FONT_HUD = ("Arial Black", 25)
FONT_BTN = ("Arial Black", 18)


ROWS = 25
COLS = 25
TILE_SIZE = 25
PAD=50 

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

canvas = tkinter.Canvas(window, bg ="black", width= WINDOW_WIDTH, height = WINDOW_HEIGHT, borderwidth = 0, highlightthickness=5)
canvas.pack()
window.update()

def draw_frame():
   canvas.create_rectangle(PAD,PAD, WINDOW_WIDTH - PAD, WINDOW_HEIGHT - PAD, outline="#39ff14", width=4)

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

game_state = "menu"

def change_direction(e): #e = event
   #print(e)
   #print(e.keysym)
   global velocityX, velocityY, velocity2X, velocity2Y
   if(game_over):
      return
   
    #player 1(WASD) 
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


def handle_keypress(e):
    global game_state
    #start game from menu
    if game_state == "menu" and e.keysym.lower() == "space":
       game_state = "playing"
       return
   #only allow movement while playing
    if game_state == "playing":
      change_direction(e)


def  move():
   global snake,snake2, food, snake_body, snake2_body, game_over, score, score2
   if (game_over):
      return

     #player 1 wall + neon green frame
   if(snake.x <= PAD or snake.x + TILE_SIZE >= WINDOW_WIDTH - PAD or snake.y <= PAD or snake.y +TILE_SIZE >= WINDOW_HEIGHT - PAD):
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

    # place food fully inside the neon frame
      min_col = PAD // TILE_SIZE
      max_col = (WINDOW_WIDTH  - PAD - TILE_SIZE)  // TILE_SIZE
      min_row = PAD // TILE_SIZE
      max_row = (WINDOW_HEIGHT - PAD - TILE_SIZE)  // TILE_SIZE
      food.x = random.randint(min_col, max_col) * TILE_SIZE
      food.y = random.randint(min_row, max_row) * TILE_SIZE
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

    #player 1 wall + neon green frame
   if(snake.x <= PAD or snake.x + TILE_SIZE >= WINDOW_WIDTH - PAD or snake.y <= PAD or snake.y +TILE_SIZE >= WINDOW_HEIGHT - PAD):
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

    # place food fully inside the neon frame
      min_col = PAD // TILE_SIZE
      max_col = (WINDOW_WIDTH  - PAD - TILE_SIZE)  // TILE_SIZE
      min_row = PAD // TILE_SIZE
      max_row = (WINDOW_HEIGHT - PAD - TILE_SIZE)  // TILE_SIZE
      food.x = random.randint(min_col, max_col) * TILE_SIZE
      food.y = random.randint(min_row, max_row) * TILE_SIZE
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

    #player 2 wall + neon green frame
   if(snake2.x <= PAD or snake2.x + TILE_SIZE >= WINDOW_WIDTH - PAD or snake2.y <= PAD or snake2.y +TILE_SIZE >= WINDOW_HEIGHT - PAD):
    game_over = True
    return

 #collision
 #Player 1 into P2 body
   for t in snake2_body:
    if snake.x == t.x and snake.y == t.y:
      game_over = True
      return

 #Player 2 into P1 body
   for t in snake_body:
    if snake2.x == t.x and snake2.y == t.y:
      game_over = True
      return
    
   #head-on
   if snake.x == snake2.x and snake.y == snake2.y:
      game_over = True
      return


def draw():
    global snake,snake2, food, snake_body, snake2_body, game_over, score, score2, game_state
    canvas.delete("all")
    draw_frame()

   # Menu state
    if game_state == "menu":
   #title text in center
     canvas.create_text(WINDOW_WIDTH//2, WINDOW_HEIGHT//2 - 40, text="SNAKE2", fill = NEON_GREEN, font=FONT_H1, anchor="center")
    # Hint text
     canvas.create_text(WINDOW_WIDTH//2, WINDOW_HEIGHT//2 + 10, text="Press SPACE to start", fill = WHITE, font= FONT_HUD, anchor="center")
    
     window.after(100,draw)
     return 

    (move)

    #draw food
    canvas.create_rectangle(food.x, food.y, food.x + TILE_SIZE, food.y + TILE_SIZE, fill= "#ffd34d",outline="")
   
    #draw player 1 snake 
    canvas.create_rectangle(snake.x, snake.y, snake.x + TILE_SIZE, snake.y + TILE_SIZE, fill = "lime green")
    for tile in snake_body:
     canvas.create_rectangle(tile.x, tile.y, tile.x +TILE_SIZE, tile.y + TILE_SIZE, fill="lime green" )
   
    #draw player 2 snake 
    canvas.create_rectangle(snake2.x, snake2.y, snake2.x + TILE_SIZE, snake2.y + TILE_SIZE, fill = "#ff4fae")
    for tile in snake2_body:
     canvas.create_rectangle(tile.x, tile.y, tile.x +TILE_SIZE, tile.y + TILE_SIZE, fill="#ff4fae")
    # scoreboard centered
   
    left_center_x= (PAD + WINDOW_WIDTH//2) //2
    right_center_x= (WINDOW_WIDTH//2 + (WINDOW_WIDTH - PAD)) //2
    canvas.create_text(left_center_x, 25, text=f"P1: {score}", fill=NEON_GREEN, font=FONT_HUD, anchor="center")
    canvas.create_text(right_center_x, 25, text= f"P2: {score2}", fill=NEON_PINK,font = FONT_HUD,anchor="center")
   
   
if(game_over):
      #winner text
      if score > score2:
         result = f"Player 1 wins!  {score}-{score2}"
      elif score2 > score:
         result = f"Player 2 wins!  {score2}-{score}"
      else: 
          result = f"It's a tie!  {score}-{score2}"

    
      canvas.create_text(window_width/2, WINDOW_HEIGHT/2 - 20, font =("Arial", 20, "bold"), text ="GAME OVER", fill="white") 
      canvas.create_text(window_width/2, WINDOW_HEIGHT/2 + 20, font =("Arial", 14, "bold"), text=result, fill="white") 
      
      window.after(100, draw) #100ms = 1/10 second, 10 frames/second

draw()

window.bind("<KeyRelease>", handle_keypress)
window.mainloop()