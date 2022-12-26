#This is a change

import pygame
import random
from threading import Timer

pygame.init()

FONT = pygame.font.SysFont('Consolas',30,True)
FONT1 = pygame.font.SysFont('Consolas',25,True)
FONT2 = pygame.font.SysFont('Gabriola',26,True)


def check_for_winner(grid):

	xcount = 0
	ocount = 0
	for i in range(3):
		for j in range(3):
			if grid[i][j] == "X":
				xcount += 1
			elif grid[i][j]=="O":
				ocount += 1

		if xcount == 3:
			return {"Winner":"X","Row":i}
		elif ocount == 3:
			return {"Winner":"O","Row":i}

		xcount = 0
		ocount = 0

	for i in range(3):
		for j in range(3):
			if grid[j][i] == "X":
				xcount += 1
			elif grid[j][i]=="O":
				ocount += 1

		if xcount == 3:
			return {"Winner":"X","Column":i}
		elif ocount == 3:
			return {"Winner":"O","Column":i}

		xcount = 0
		ocount = 0


	for i in range(3):
		if grid[i][i] == "X":
			xcount += 1
		elif grid[i][i] == "O":
			ocount += 1

	if xcount == 3:
			return {"Winner":"X","Diagonal":1}
	elif ocount == 3:
		return {"Winner":"O","Diagonal":1}

	xcount = 0
	ocount = 0
	i = 0
	j = 2

	while i<3:
		if grid[i][j] == "X":
			xcount += 1
		elif grid[i][j] == "O":
			ocount += 1

		i += 1
		j -= 1

	if xcount == 3:
			return {"Winner":"X","Diagonal":2}
	elif ocount == 3:
		return {"Winner":"O","Diagonal":2}

	for i in range(3):
		for j in range(3):
			if not grid[i][j]:
				return {"Winner":None}

	return {"Winner":None,"Draw":True}



class game:

	def __init__(self,screen,clock):

		self.screen = screen
		self.clock = clock
		self.X_img = pygame.image.load("X.png")
		self.O_img = pygame.image.load("O.png")
		self.State_texts = {"O":FONT.render("O's Turn",True,(255,255,255)),
					        "X":FONT.render("X's Turn",True,(255,255,255)),
					        "XWon":FONT.render("X Won",True,(255,255,255)),
					        "OWon":FONT.render("O Won",True,(255,255,255)),
					        "Draw":FONT.render("Draw",True,(255,255,255))}

		self.text_adjustments = {"O":(0,0),"X":(0,0),"XWon":(30,0),"OWon":(30,0),"Draw":(40,0)}
		#self.init_objects()

	def init_objects(self):

		self.grid = []
		for i in range(3):
			self.grid.append([])
			for j in range(3):
				self.grid[i].append(0)

		self.State = random.choice(["X","O"])
		self.running = True
		self.ended = False
		self.result = None
		self.win_type = None
		self.restarted = True

	def start(self):

		while self.running:
			screen.fill((43,42,43))
			pos = pygame.mouse.get_pos()
			column = pos[0]//101
			row = pos[1]//101

			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					self.running = False
				elif event.type == pygame.MOUSEBUTTONDOWN and self.State not in ["XWon","OWon","Draw"] and event.button == 1:
					pos = pygame.mouse.get_pos()
					column = pos[0] //101
					row = pos[1] //101

					if (row >= 0 and row <= 2) and (column >= 0 and column <= 2) and not self.grid[row][column]:
						self.grid[row][column] = self.State
						self.result = check_for_winner(self.grid)
						self.State = "O" if self.State == "X" else "X"	
						#print(self.result)
						#print(grid)
						if self.result["Winner"] == "X":
							self.State = "XWon"
						elif self.result["Winner"] == "O":
							self.State = "OWon"
						elif "Draw" in self.result.keys():
							self.State = "Draw"


			for i in range(3):
				for j in range(3):
					pygame.draw.rect(self.screen,(255,255,255),[101*j+5,101*i+5,96,96])

			if (row >= 0 and row <= 2) and (column >= 0 and column <= 2) and not self.grid[row][column] and self.State not in ["XWon","OWon","Draw"]:
				pygame.draw.rect(self.screen,(0,255,0),[101*column+5,101*row+5,96,96])

			for i in range(3):
				for j in range(3):
					if self.grid[i][j] == "X":
						self.screen.blit(self.X_img,(101*j-3,101*i))
					elif self.grid[i][j] == "O":
						self.screen.blit(self.O_img,(101*j-3,101*i))

			pygame.draw.rect(self.screen,"#9147ff",[5,308,298,87])
			self.screen.blit(self.State_texts[self.State],(80+self.text_adjustments[self.State][0],340+self.text_adjustments[self.State][1]))

			if self.State in ["XWon","OWon","Draw"] and not self.ended:
				self.ended = True
				self.restarted = False
				self.endgame = Timer(3.0,self.end_game)
				self.endgame.start()

			if self.result:
				if self.result['Winner']:
					if 'Row' in self.result:
						row_num = self.result['Row']
						if row_num == 0:
							pygame.draw.line(self.screen,(0,255,0),(10,51),(298,51),5)
						elif row_num == 1:
							pygame.draw.line(self.screen,(0,255,0),(10,157),(298,157),5)
						elif row_num == 2:
							pygame.draw.line(self.screen,(0,255,0),(10,253),(298,253),5)

					elif 'Column' in self.result:
						col_num = self.result['Column']
						if col_num == 0:
							pygame.draw.line(self.screen,(0,255,0),(51,10),(51,298),5)
						elif col_num == 1:
							pygame.draw.line(self.screen,(0,255,0),(157,10),(157,298),5)
						elif col_num == 2:
							pygame.draw.line(self.screen,(0,255,0),(253,10),(253,298),5)

					elif 'Diagonal' in self.result:
						diag_num = self.result['Diagonal']
						if diag_num == 1:
							pygame.draw.line(self.screen,(0,255,0),(10,10),(298,298),5)
						elif diag_num == 2:
							pygame.draw.line(self.screen,(0,255,0),(10,298),(298,10),5)



			self.clock.tick(60)
			pygame.display.flip()

		return

	def end_game(self):
		if not self.restarted:
			self.running = False


width,height = 308,400
screen = pygame.display.set_mode((width,height))
clock = pygame.time.Clock()
pygame.display.set_caption("OX")
icon = pygame.image.load("icon1.png")
pygame.display.set_icon(icon)
newgame = game(screen,clock)

def main(screen,clock):
	done = False
	mainpage = pygame.transform.scale(pygame.image.load("MainPage.png"),(308,400))

	text = FONT2.render("Press any key to continue :)",True,(0,0,0))
	delay = 800
	current_time = pygame.time.get_ticks()
	change_time = current_time + delay
	text_visible = True

	while not done:
		pos = pygame.mouse.get_pos()
		screen.blit(mainpage,(0,0))
		for event in pygame.event.get():
			if (event.type == pygame.MOUSEBUTTONDOWN or event.type == pygame.KEYDOWN):
				done = True
			elif event.type == pygame.QUIT:
				return "quit"

		current_time = pygame.time.get_ticks()
		if current_time >= change_time:
		    change_time = current_time + delay
		    text_visible = not text_visible

		if text_visible:
			screen.blit(text,(20,50))

		clock.tick(60)
		pygame.display.flip()


def run():
	while True:
		if main(screen,clock) == "quit":
			print("Closing .......\n\nBye ...........")
			break
		newgame.init_objects()
		newgame.start()

run()

pygame.quit()
