from tkinter import *
import random
import time


class Ball:
    def __init__(self, canvas, paddle, score, color):
        self.canvas = canvas
        self.paddle = paddle
        self.score = score
        self.id = canvas.create_oval(10, 10, 25, 25, fill=color)
        self.canvas.move(self.id, 245, 250)
        self.x = random.choice((-3, -2, -1, 1, 2, 3))
        self.y = -3
        self.canvas_height = self.canvas.winfo_height()
        self.canvas_width = self.canvas.winfo_width()
        self.hit_bottom = False

    def hit_paddle(self, pos):
        paddle_pos = self.canvas.coords(self.paddle.id)
        if pos[2] >= paddle_pos[0] and pos[0] <= paddle_pos[2]:
            if pos[3] >= paddle_pos[1] and pos[3] <= paddle_pos[3]:
                self.x += self.paddle.x
                self.score.hit()
                return True

        return False

    def draw(self):
        self.canvas.move(self.id, self.x, self.y)
        pos = self.canvas.coords(self.id)
        if pos[1] <= 0:
            self.y = abs(self.y)
        if pos[3] >= self.canvas_height:
            # self.y = abs(self.y) * -1
            self.hit_bottom = True
        if pos[0] <= 0:
            self.x = abs(self.x)
        if pos[2] >= self.canvas_width:
            self.x = abs(self.x) * -1
        if self.hit_paddle(pos):
            self.y = abs(self.x) * -1


class Paddle:
    def __init__(self, canvas, color):
        self.canvas = canvas
        self.id = canvas.create_rectangle(0, 0, 100, 10, fill=color)
        self.canvas.move(self.id, 200, 300)
        self.x = 0
        self.canvas_width = self.canvas.winfo_width()
        self.started = False
        self.canvas.bind_all('<KeyPress-Left>', self.turn_left)
        self.canvas.bind_all('<KeyPress-Right>', self.turn_right)
        self.canvas.bind_all('<KeyPress-space>', self.start_game)

    def draw(self):
        self.canvas.move(self.id, self.x, 0)
        pos = self.canvas.coords(self.id)

        if pos[0] <= 0:
            self.x = 0
            self.canvas.bind_all('<KeyPress-Left>', self.turn_right)
        elif self.x >= 1:
            self.canvas.bind_all('<KeyPress-Left>', self.turn_left)

        if pos[2] >= self.canvas_width:
            self.x = 0
            self.canvas.bind_all('<KeyPress-Right>', self.turn_left)

        elif self.x <= -1:
            self.canvas.bind_all('<KeyPress-Right>', self.turn_right)

    def turn_left(self, event):
        self.x = -3

    def turn_right(self, event):
        self.x = 3

    def start_game(self, event):
        self.started = True


class Block:
    def __init__(self, canvas, x, y, color):
        self.canvas = canvas
        self.pos_x = x
        self.pos_y = y
        self.id = canvas.create_rectangle(0, 0, 50, 20, fill=color)
        self.canvas.move(self.id, 25 + self.pos_x * 50, 25 + self.pos_y * 20)

    def delete(self):
        self.canvas.delete(self.id)


class Score:
    def __init__(self, canvas, color):
        self.score = 0
        self.canvas = canvas
        self.id = canvas.create_text(450, 10, text=self.score, fill=color)

    def hit(self):
        self.score += 1
        self.canvas.itemconfig(self.id, text=self.score)


tk = Tk()
tk.title("Game")
tk.resizable(0, 0)
tk.wm_attributes("-topmost", 1)
c = Canvas(tk, width=500, height=400, bd=0, highlightthickness=0)
c.create_rectangle(0, 0, 500, 400, fill='green')
c.pack()
tk.update()

colors = ('white', 'aqua', 'pink')
blocks = []
for y in range(5):
    for x in range(9):
        blocks.append(Block(c, x, y, random.choice(colors)))
score = Score(c, 'orange')
p = Paddle(c, 'blue')
ball = Ball(c, p, score,'red')

game_over_text = c.create_text(250, 200, font = ('FixedSys', 40),  text='GAME OVER', state='hidden',)
def update():
    ball.draw()
    p.draw()


tk.after(10, update)
while True:
    if ball.hit_bottom == False and p.started == True:
        ball.draw()
        p.draw()
    if ball.hit_bottom == True:
        time.sleep(1)
        c.itemconfig(game_over_text, state='normal')
    tk.update_idletasks()
    tk.update()
    time.sleep(0.01)
