import tkinter
import random

# hier heb ik alle kleuren en lettertypes gezet zodat ik ze later makkelijk kan gebruiken 
WHITE = "#ffffff"
NEON_GREEN = "#39FF14"
NEON_PINK = "#FF4FAE"
YELLOW = "#FFD34D"

FONT_TILE = ("Arial Black", 54, "bold")
FONT_H1 = ("Arial Black", 40, "bold")
FONT_HUD = ("Arial Black", 25, "bold")
FONT_BTN = ("Arial Black", 18, "bold")


# dit bepaalt hoe groot het speelveld is 
ROWS = 25
COLS = 25
TILE_SIZE = 25
PAD=50  # dit is de rand voor de groene ruimte
PAD2= 35

#hier bereken ik de totale grootte van het speelveld uit
WINDOW_WIDTH = TILE_SIZE * COLS
WINDOW_HEIGHT= TILE_SIZE * ROWS

#dit is een klein hulpje om een positie (x en y) op te slaan
class Tile:  
 def __init__(self, x,y):
     self.x = x
     self.y = y

def toggle_pause(): 
      global game_state
      if game_state =="playing":
         game_state = "paused"
      elif game_state == "paused":
         game_state = "playing"
      

#hier maak ik het venster van het spel
window = tkinter.Tk()
window.title("Snake")
window.resizable(False, False)

#hier maak ik een tekenbord waar alles op getekend zal worden
canvas = tkinter.Canvas(window, bg ="black", width= WINDOW_WIDTH, height = WINDOW_HEIGHT, borderwidth = 0, highlightthickness=5)
canvas.pack()

#teruggaan knopje
return_btn = tkinter.Button 
window,
text="◀️"
font=FONT_BTN
bg="black" 
fg="#39FF14",
activebackground="black",
activeforeground="#39FF14",
bd=0,
relief="flat",
highlightthickness=0,
padx=0, pady=4,



#pauze knop
pause_btn = tkinter.Button(
   window, 
   text="⏸",
   font=FONT_BTN,
   bg="black",
   fg="#39FF14",
   activebackground="black",
   activeforeground="#39FF14",
   bd=0,
   relief="flat",
   highlightthickness=0,
   padx=4, pady=0,
   command=toggle_pause
   )

window.update()

#dit tekent het groene kader 
def draw_frame():
   canvas.create_rectangle(PAD,PAD, WINDOW_WIDTH - PAD, WINDOW_HEIGHT - PAD, outline="#39ff14", width=4)


#dit zorgt ervoor dat het venster in het midden staat
window_width = window.winfo_width()
window_height= window.winfo_height()
screen_width = window.winfo_screenwidth()
screen_height = window.winfo_screenheight()
window_x = int((screen_width/2)- (window_width/2))
window_y = int((screen_height/2)- (window_height/2))

#format "(w)x(h)+(x)(y)"
window.geometry(f"{window_width}x{window_height}+{window_x}+{window_y}")

#startpositie van speler 1 en 2
#player 1 (WASD-green)
snake = Tile(4*TILE_SIZE, 4*TILE_SIZE) #single tile, snake's head
snake_body = [] #multiple snake tiles
velocityX = 0
velocityY = 0
score = 0

#player 2 (Arrows-pink)
snake2 = Tile(20*TILE_SIZE, 20*TILE_SIZE) #single tile, snake's head
snake2_body = [] #multiple snake tiles
velocity2X = 0
velocity2Y = 0
score2 = 0

high_score = 0

#startpositie eten
food = Tile(12*TILE_SIZE, 12*TILE_SIZE)
game_over = False

game_state = "menu" 


#dit verandert de richting van de slangen als je een toets indrukt 
def change_direction(e): #e = event
   #print(e)
   #print(e.keysym)
   global velocityX, velocityY, velocity2X, velocity2Y
   if(game_over):
      return
   
    #Player 1 stuurt met (WASD) 
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

    #Player 2 stuurt met (Arrows)
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

def reset_game(): 
 global snake,snake2, food, snake_body, snake2_body, game_over, score, score2, game_state, high_score, velocityX, velocityY, velocity2X, velocity2Y 
 snake = Tile(4*TILE_SIZE, 4*TILE_SIZE)
 snake_body = [] 
 velocityX = 0
 velocityY = 0
 score = 0

 #player 2 (Arrows-pink)
 snake2 = Tile(20*TILE_SIZE, 20*TILE_SIZE) 
 snake2_body = []
 velocity2X = 0
 velocity2Y = 0
 score2 = 0

 food = Tile(12*TILE_SIZE, 12*TILE_SIZE)
 game_over = False
 game_state= "playing"
 draw()

   # dit regelt wat er gebeurt als je een toets indrukt
def handle_keypress(e):
    global game_state
    #start game from menu
    if game_state == "menu" and e.keysym.lower() == "space":
       game_state = "uitleg" 
       return
    # go from uitleg to rules
    if game_state == "uitleg" and e.keysym.lower() == "space":
       game_state = "rules"
       return
   # go from rules to playing
    if game_state == "rules" and e.keysym.lower() == "space":
       game_state = "playing"
       return
   # go from uitleg to playing
    if game_over and e.keysym.lower() == "space":
       reset_game()
       return
   #only allow movement while playing
    if game_state == "playing":
      change_direction(e)

def update_pause_button():
   #weergave pauze knop
   if game_over:
      pause_btn.place_forget()
      return
   
   if game_state == "playing":
      pause_btn.config(text="⏸")
      pause_btn.place(relx=1.0, x=-10, y=-2, anchor ="ne")
   elif game_state =="paused":
      pause_btn.config(text="▶")
      pause_btn.place(relx=1.0, x=-10, y=-2, anchor="ne")
   else: 
      pause_btn.place_forget()



# zorgt ervoor dat de slangen bewegen en wat er gebeurt als ze botsen of eten
def  move():
   global snake,snake2, food, snake_body, snake2_body, game_over, score, score2, high_score
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
      margin= 5
      min_col = PAD2 // TILE_SIZE + margin
      max_col = (WINDOW_WIDTH  - PAD2 - TILE_SIZE)  // TILE_SIZE -margin
      min_row = PAD2 // TILE_SIZE + margin
      max_row = (WINDOW_HEIGHT - PAD2 - TILE_SIZE)  // TILE_SIZE - margin
      food.x = random.randint(min_col, max_col) * TILE_SIZE
      food.y = random.randint(min_row, max_row) * TILE_SIZE
      score += 1
      high_score = max(high_score, score, score2)

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

   #player 2 self
   for tile in snake2_body:
      if(snake2.x== tile.x and snake2.y == tile.y):
          game_over = True
          return

   #player 2 eats
   if (snake2.x == food.x and snake2.y == food.y):
      snake2_body.append(Tile(food.x, food.y))

    # place food fully inside the neon frame
      margin= 5
      min_col = PAD2 // TILE_SIZE + margin
      max_col = (WINDOW_WIDTH  - PAD2 - TILE_SIZE)  // TILE_SIZE -margin
      min_row = PAD2 // TILE_SIZE + margin
      max_row = (WINDOW_HEIGHT - PAD2 - TILE_SIZE)  // TILE_SIZE - margin
      food.x = random.randint(min_col, max_col) * TILE_SIZE
      food.y = random.randint(min_row, max_row) * TILE_SIZE
      score2 += 1
      high_score = max(high_score, score, score2)

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

# dit tekent alles opnieuw op het scherm
def draw():
    global snake,snake2, food, snake_body, snake2_body, game_over, score, score2, game_state, high_score
    
    #beweegt alleen tijdens spelen
    if game_state =="playing" and not game_over:
     move()

    canvas.delete("all")
    canvas.create_rectangle(0, 0, WINDOW_WIDTH, WINDOW_HEIGHT, fill="black")
    draw_frame()
   
    # dit is het menu scherm 
    if (game_state) == "menu":
      # title text in center
      canvas.create_rectangle(PAD,PAD, WINDOW_WIDTH - PAD, WINDOW_HEIGHT - PAD, outline="#39ff14", width=4)
      canvas.create_text(WINDOW_WIDTH//2, WINDOW_HEIGHT//2 - 40, text="SNAKE2", fill=NEON_GREEN, font=FONT_TILE, anchor="center")
      canvas.create_text(WINDOW_WIDTH//2, WINDOW_HEIGHT//2 + 100, text="Press SPACE to start", fill=WHITE, font=FONT_HUD, anchor="center")
      update_pause_button()
      window.after(100, draw)
      return

    canvas.delete("all")
    canvas.create_rectangle(0, 0, WINDOW_WIDTH, WINDOW_HEIGHT, fill="black")
    # uitleg pagina (tweede pagina)
    if (game_state)== "uitleg": 
      #tekst uitleg
      canvas.create_text(WINDOW_WIDTH//2, WINDOW_HEIGHT//2 + -180, text="INSTRUCTIONS", fill= WHITE, font=FONT_H1, anchor="center")
      canvas.create_text(WINDOW_WIDTH//2, WINDOW_HEIGHT//2 + 20, text="Player 1: W A S D keys", fill=NEON_GREEN, font=FONT_HUD, anchor="center")
      canvas.create_text(WINDOW_WIDTH//2, WINDOW_HEIGHT//2 + 80, text="Player 2: Arrow keys", fill=NEON_PINK, font=FONT_HUD, anchor="center")
      canvas.create_text(WINDOW_WIDTH//2, WINDOW_HEIGHT//2 + 230, text="Press SPACE to continue", fill=WHITE, font=FONT_HUD, anchor="center")
      update_pause_button()
      window.after(100, draw)
      return

    canvas.delete("all")
    canvas.create_rectangle(0, 0, WINDOW_WIDTH, WINDOW_HEIGHT, fill="black")
    # uitleg pagina (tweede pagina)
    if (game_state)== "rules": 
      #tekst uitleg
      canvas.create_text(WINDOW_WIDTH//2, WINDOW_HEIGHT//2 + -180, text="Rules", fill= WHITE, font=FONT_H1, anchor="center")
      canvas.create_text(WINDOW_WIDTH//2, WINDOW_HEIGHT//2 + -60, text="1. COLLECT FOOD --> +1P", fill=NEON_GREEN, font=FONT_HUD, anchor="center")
      canvas.create_text(WINDOW_WIDTH//2, WINDOW_HEIGHT//2 + -10, text="2. HIT THE WALL--> DEAD", fill=NEON_PINK, font=FONT_HUD, anchor="center")
      canvas.create_text(WINDOW_WIDTH//2, WINDOW_HEIGHT//2 + 40, text="3. HIT YOURSELF --> DEAD", fill=NEON_GREEN, font=FONT_HUD, anchor="center")
      canvas.create_text(WINDOW_WIDTH//2, WINDOW_HEIGHT//2 + 90, text="4. HIT OPPONENT --> DEAD", fill=NEON_PINK, font=FONT_HUD, anchor="center")
      canvas.create_text(WINDOW_WIDTH//2, WINDOW_HEIGHT//2 + 140, text="MOST POINTS WIN", fill=NEON_GREEN, font=FONT_HUD, anchor="center")
      canvas.create_text(WINDOW_WIDTH//2, WINDOW_HEIGHT//2 + 230, text="Press SPACE to continue", fill=WHITE, font=FONT_HUD, anchor="center")
      update_pause_button()
      window.after(100, draw)
      return

    #draw neon groen kader
    canvas.create_rectangle(PAD,PAD, WINDOW_WIDTH - PAD, WINDOW_HEIGHT - PAD, outline="#39ff14", width=4)

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
    canvas.create_text(WINDOW_WIDTH // 2, 25, text=f"High Score: {high_score}", fill=YELLOW, font=("Arial Black", 10), anchor="center")
   
   
    if(game_over):
      #winner text
      if score > score2:
         result = f"Player 1 wins!  {score}-{score2}"
      elif score2 > score:
         result = f"Player 2 wins!  {score2}-{score}"
      else: 
          result = f"It's a tie!  {score}-{score2}"
          

       # Game over and result
      canvas.create_text(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 + -80, font=("Arial", 40, "bold"), text="GAME OVER", fill="white")
      canvas.create_text(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 + 50, font=("Arial", 30), text=result, fill= NEON_GREEN if score > score2 else NEON_PINK if score2 > score else "yellow")
      canvas.create_text(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 + 180, font=("Arial", 12), text="Press SPACE to play again", fill="white")
      return 
    
  #pauzeknop
    update_pause_button()
    window.after(100, draw) #100ms = 1/10 second, 10 frames/second

draw()

window.bind("<KeyRelease>", handle_keypress)
window.mainloop()