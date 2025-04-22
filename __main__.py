#!/usr/bin/env python3

#-# Colors #-#
class bcolors:
	ENDC = '\033[0m'
	BOLD = '\033[1m'
	UNDERLINE = '\033[4m'

Red = (255,0,0)
Blue = (0,0,255)
Yellow = (255,255,0)
Maroon = (128,0,0)
Green = (0,128,0)

### IMPORTING THE PACKAGES ###
try:
	from colorama import *
	import pygame, os, random, sys

except ImportError as e:
	print(Fore.YELLOW+bcolors.BOLD+"==> Error ==> "+str(e)+"\n==> You need the install 'pygame' package to use this application.\n==> Use 'sudo apt-get install python3-pip && pip3 install pygame' command to download and install this packages in the terminal."+bcolors.ENDC)
	exit()

### PLAYER CLASS ###
class Player(object):

	def __init__(self, game, location, control = "R", width = 64, height = 64):

		self.x = int(location[0])
		self.y = int(location[1])
		self.width = width
		self.height = height
		self.MaxJumpPoint = self.y - 180
		self.MaxFallPoint = self.y
		self.MovSpeed = 5
		self.Jump = False
		self.JumpSpeed = 10
		self.FallSpeed = 10
		self.left = False
		self.right = False
		self.walkCount = 0
		self.standing = True
		self.score = 0
		self.onThePlatform = False
		self.vampire = False
		self.facing = 0
		self.introJump = False
		if(game.TwoPlayers):
			self.control = control
		else:
			self.control = "RL"

	def beVampire(self):

		VampireWalkRight = [pygame.image.load('images/vampire/R1E.png'), pygame.image.load('images/vampire/R2E.png'), pygame.image.load('images/vampire/R3E.png'), pygame.image.load('images/vampire/R4E.png'), pygame.image.load('images/vampire/R5E.png'), pygame.image.load('images/vampire/R6E.png'), pygame.image.load('images/vampire/R7E.png'), pygame.image.load('images/vampire/R8E.png'), pygame.image.load('images/vampire/R9E.png')]
		VampireWalkLeft = [pygame.image.load('images/vampire/L1E.png'), pygame.image.load('images/vampire/L2E.png'), pygame.image.load('images/vampire/L3E.png'), pygame.image.load('images/vampire/L4E.png'), pygame.image.load('images/vampire/L5E.png'), pygame.image.load('images/vampire/L6E.png'), pygame.image.load('images/vampire/L7E.png'), pygame.image.load('images/vampire/L8E.png'), pygame.image.load('images/vampire/L9E.png')]
		self.MovSpeed = 6
		self.walkLeft = VampireWalkLeft
		self.walkRight = VampireWalkRight
		self.hitbox = (self.x + 17, self.y + 2, 31, 57)
		self.vampire = True

	def bePeasant(self):

		PeasantWalkRight = [pygame.image.load('images/peasant/R1.png'), pygame.image.load('images/peasant/R2.png'), pygame.image.load('images/peasant/R3.png'), pygame.image.load('images/peasant/R4.png'), pygame.image.load('images/peasant/R5.png'), pygame.image.load('images/peasant/R6.png'), pygame.image.load('images/peasant/R7.png'), pygame.image.load('images/peasant/R8.png'), pygame.image.load('images/peasant/R9.png')]
		PeasantWalkLeft = [pygame.image.load('images/peasant/L1.png'), pygame.image.load('images/peasant/L2.png'), pygame.image.load('images/peasant/L3.png'), pygame.image.load('images/peasant/L4.png'), pygame.image.load('images/peasant/L5.png'), pygame.image.load('images/peasant/L6.png'), pygame.image.load('images/peasant/L7.png'), pygame.image.load('images/peasant/L8.png'), pygame.image.load('images/peasant/L9.png')]
		self.MovSpeed = 5
		self.walkLeft = PeasantWalkLeft
		self.walkRight = PeasantWalkRight
		self.hitbox = (self.x + 17, self.y + 11, 29, 52)
		self.vampire = False

	def move(self):
		
		#-# MOVING  KEYS #-#		
		keys = pygame.key.get_pressed()
		if(self.control == "R" or self.control == "RL"):
			#-# Move Right #-#
			if(keys[pygame.K_RIGHT]):
				if(self.x < game.windowWidth - self.MovSpeed - 20):
					self.x += self.MovSpeed 
					self.left = False
					self.right = True
					self.standing = False
				else:
					self.x = -20
			#-# Move Left #-#
			elif(keys[pygame.K_LEFT]):
				if (self.x > -20):
					self.x -= self.MovSpeed 
					self.left = True
					self.right = False
					self.standing = False
				else:
					self.x = game.windowWidth - 20	
			else:
				self.standing = True
				self.walkCount = 0

		elif(self.control == "L" or self.control == "RL"):
			#-# Move Right #-#
			if(keys[ord('d')]):
				if(self.x < game.windowWidth - self.MovSpeed - 20):
					self.x += self.MovSpeed 
					self.left = False
					self.right = True
					self.standing = False
				else:
					self.x = -20
			#-# Move Left #-#
			elif(keys[ord('a')]):
				if (self.x > -20):
					self.x -= self.MovSpeed 
					self.left = True
					self.right = False
					self.standing = False
				else:
					self.x = game.windowWidth - 20	
			else:
				self.standing = True
				self.walkCount = 0

	def jump(self):
		keys = pygame.key.get_pressed()
		if((self.control == "R" and keys[pygame.K_UP]) or (self.control == "L" and keys[pygame.K_w]) or (self.control == "RL" and (keys[pygame.K_w] or keys[pygame.K_UP]))):
			if(self.Jump == False and not(self.y < self.MaxFallPoint and self.y >= self.MaxJumpPoint)):
				self.Jump = True
				self.walkCount = 0
				if(self.vampire == False):
					#-# Music #-#
					jumpSound = pygame.mixer.Sound('sounds/jump.wav')
					jumpSound.play()

		if((self.control == "R" and keys[pygame.K_DOWN]) or (self.control == "L" and keys[pygame.K_s])):
			if(self.Jump == False):
				self.MaxFallPoint = 490

	def jumpControl(self):	
		if(self.y == 490):
			self.MaxJumpPoint = 310

		if(self.Jump == True):
			if(self.y > self.MaxJumpPoint):
				self.y -= self.JumpSpeed
			elif(self.y <= self.MaxJumpPoint):
				self.Jump = False
		elif(self.y < self.MaxFallPoint and self.y >= self.MaxJumpPoint):
			self.y += self.FallSpeed

	def shoot(self):
		keys = pygame.key.get_pressed()
		if((self.control == "R" or self.control == "RL") and (keys[pygame.K_RCTRL] and self.vampire == False)):
			if(self.left):
				self.facing = -1
			else:
				self.facing = 1
		
			if(len(game.bullets) < 5):
				game.bullets.append(projectile(round(self.x + self.width//2), round(self.y + self.height//2), 6, (0,0,0), self.facing)) 

		if((self.control == "L" or self.control == "RL") and (keys[pygame.K_SPACE] and self.vampire == False)):
			if(self.left):
				self.facing = -1
			else:
				self.facing = 1
		
			if(len(game.bullets) < 5):
				game.bullets.append(projectile(round(self.x + self.width//2), round(self.y + self.height//2), 6, (0,0,0), self.facing)) 
	
	def platformControl(self):
		if(self.vampire):
			if(self.hitbox[0] + 31 >= game.Platform1.x and self.hitbox[0] <= game.Platform1.x + game.Platform1.width):	
				if(self.Jump == False and self.hitbox[1] + 58 == game.Platform1.y):
					self.MaxJumpPoint = self.y - 180
					self.MaxFallPoint = self.y
					self.onThePlatform = True

			elif(self.hitbox[0] + 31 >= game.Platform2.x and self.hitbox[0] <= game.Platform2.x + game.Platform2.width):	
				if(self.Jump == False and self.hitbox[1] + 58 == game.Platform2.y):
					self.MaxJumpPoint = self.y - 180
					self.MaxFallPoint = self.y
					self.onThePlatform = True

			else:
				self.MaxFallPoint = 490
				self.onThePlatform = False

			if(self.hitbox[0] + 31 >= game.Platform3.x and self.hitbox[0] <= game.Platform3.x + game.Platform3.width):	
				if(self.Jump == False and self.hitbox[1] + 58 == game.Platform3.y):
					self.MaxJumpPoint = self.y - 180
					self.MaxFallPoint = self.y
					self.onThePlatform = True
			elif(self.onThePlatform):
				self.MaxFallPoint = 340
				self.onThePlatform = False
		else:
			if(self.hitbox[0] + 29 >= game.Platform1.x and self.hitbox[0] <= game.Platform1.x + game.Platform1.width):	
				if(self.Jump == False and self.hitbox[1] + 49 == game.Platform1.y):
					self.MaxJumpPoint = self.y - 180
					self.MaxFallPoint = self.y
					self.onThePlatform = True

			elif(self.hitbox[0] + 29 >= game.Platform2.x and self.hitbox[0] <= game.Platform2.x + game.Platform2.width):	
				if(self.Jump == False and self.hitbox[1] + 49 == game.Platform2.y):
					self.MaxJumpPoint = self.y - 180
					self.MaxFallPoint = self.y
					self.onThePlatform = True

			else:
				self.MaxFallPoint = 490
				self.onThePlatform = False

			if(self.hitbox[0] + 29 >= game.Platform3.x and self.hitbox[0] <= game.Platform3.x + game.Platform3.width):	
				if(self.Jump == False and self.hitbox[1] + 49 == game.Platform3.y):
					self.MaxJumpPoint = self.y - 180
					self.MaxFallPoint = self.y
					self.onThePlatform = True
			elif(self.onThePlatform):
				self.MaxFallPoint = 340
				self.onThePlatform = False

	def draw(self, window):
		if self.walkCount + 1 >= len(self.walkLeft) * 3:
			self.walkCount = 0
		if not(self.standing):
			if self.left:
				window.blit(self.walkLeft[self.walkCount//3], (self.x,self.y))
				self.walkCount += 1
			elif self.right:
				window.blit(self.walkRight[self.walkCount//3], (self.x,self.y))
				self.walkCount +=1
		else:
			if (self.left):
				window.blit(self.walkLeft[0], (self.x, self.y))				
			else:
				window.blit(self.walkRight[0], (self.x, self.y))
		
		if(self.vampire):
			self.hitbox = (self.x + 17, self.y + 2, 31, 57)
			#pygame.draw.rect(window, (255,0,0), self.hitbox,2)
		else:
			self.hitbox = (self.x + 17, self.y + 11, 29, 52)
			#pygame.draw.rect(window, (255,0,0), self.hitbox,2)

	def IntroJump(self):
		if(self.introJump == False and not(self.y < self.MaxFallPoint and self.y >= self.MaxJumpPoint)):
			self.introJump = True

		if(self.introJump == True):
			if(self.y > self.MaxJumpPoint):
				self.y -= self.JumpSpeed
			elif(self.y <= self.MaxJumpPoint):
				self.introJump = False
		elif(self.y < self.MaxFallPoint and self.y >= self.MaxJumpPoint):
				self.y += self.FallSpeed

### PLATFORM CLASS ###########################################################################################################################			
class Platform(object):
	def __init__(self, location, width, height):
		self.x = location[0]
		self.y = location[1]
		self.width = width
		self.height = height
		self.image = pygame.image.load("images/platform.png")
		self.image = pygame.transform.scale(self.image, (self.width, self.height))
	
	def draw(self, window):
		#-# Drawing Platforms to the Screen #-#
		window.blit(self.image, (self.x, self.y))

### PROJECTILE CLASS #########################################################################################################################
class projectile(object):
	def __init__(self, x, y, radius, color, facing):
		self.x = x
		self.y = y
		self.radius = radius
		self.color = color
		self.facing = facing
		self.MovSpeed = 3 * facing

	def draw(self,window):

		#-# Drawing Bullets to the Screen #-#
		pygame.draw.circle(window, self.color, (self.x, self.y), self.radius)

### GAME CLASS ###############################################################################################################################
class Game(object):
	def __init__(self):
		#-# Window Settings #-#
		self.windowWidth = 800
		self.windowHeight =	600
		self.windowTitle = "START"
		self.windowBackground = pygame.image.load("images/bg.jpg")
		self.windowBackground = pygame.transform.scale(self.windowBackground, (self.windowWidth, self.windowHeight))

		#-# Setting the Window Center of the Screen #-#
		os.environ['SDL_VIDEO_CENTERED'] = '1'		

		#-# 3 Seconds Wait Setting #-#
		self.i = 100

		#-# Cusrsor Images #-#
		self.cursorN = [pygame.image.load("images/cursor/normal/N-0.png"), pygame.image.load("images/cursor/normal/N-1.png"), pygame.image.load("images/cursor/normal/N-2.png"), pygame.image.load("images/cursor/normal/N-3.png"), pygame.image.load("images/cursor/normal/N-4.png"), pygame.image.load("images/cursor/normal/N-5.png"), pygame.image.load("images/cursor/normal/N-6.png"), pygame.image.load("images/cursor/normal/N-7.png"), pygame.image.load("images/cursor/normal/N-8.png"), pygame.image.load("images/cursor/normal/N-9.png"), pygame.image.load("images/cursor/normal/N-10.png"), pygame.image.load("images/cursor/normal/N-11.png"), pygame.image.load("images/cursor/normal/N-12.png"), pygame.image.load("images/cursor/normal/N-13.png"), pygame.image.load("images/cursor/normal/N-14.png"), pygame.image.load("images/cursor/normal/N-15.png"), pygame.image.load("images/cursor/normal/N-16.png")]
		self.cursorC = [pygame.image.load("images/cursor/click/L-0.png"), pygame.image.load("images/cursor/click/L-1.png"), pygame.image.load("images/cursor/click/L-2.png"), pygame.image.load("images/cursor/click/L-3.png"), pygame.image.load("images/cursor/click/L-4.png"), pygame.image.load("images/cursor/click/L-5.png"), pygame.image.load("images/cursor/click/L-6.png"), pygame.image.load("images/cursor/click/L-7.png")]		
		self.cursorC2 = [pygame.image.load("images/cursor/click2/L2-0.png"), pygame.image.load("images/cursor/click2/L2-1.png"), pygame.image.load("images/cursor/click2/L2-2.png"), pygame.image.load("images/cursor/click2/L2-3.png"), pygame.image.load("images/cursor/click2/L2-4.png"), pygame.image.load("images/cursor/click2/L2-5.png"), pygame.image.load("images/cursor/click2/L2-6.png"), pygame.image.load("images/cursor/click2/L2-7.png"), pygame.image.load("images/cursor/click2/L2-8.png"), pygame.image.load("images/cursor/click2/L2-9.png"), pygame.image.load("images/cursor/click2/L2-10.png"), pygame.image.load("images/cursor/click2/L2-11.png"), pygame.image.load("images/cursor/click2/L2-12.png")]		
		self.cursorW = [pygame.image.load("images/cursor/writing/W-0.png"), pygame.image.load("images/cursor/writing/W-1.png"), pygame.image.load("images/cursor/writing/W-2.png"), pygame.image.load("images/cursor/writing/W-3.png")]
		self.cursorH = [pygame.image.load("images/cursor/help/H-0.png"), pygame.image.load("images/cursor/help/H-1.png"), pygame.image.load("images/cursor/help/H-2.png"), pygame.image.load("images/cursor/help/H-3.png"), pygame.image.load("images/cursor/help/H-4.png"), pygame.image.load("images/cursor/help/H-5.png"), pygame.image.load("images/cursor/help/H-6.png"), pygame.image.load("images/cursor/help/H-7.png"), pygame.image.load("images/cursor/help/H-8.png"), pygame.image.load("images/cursor/help/H-9.png")]
		self.cursor = self.cursorN		
		self.cursorTurn = 0

		#-# Setting the Platforms #-#
		self.Platform1 = Platform((0, 400), 300, 50)
		self.Platform2 = Platform((500, 400), 300, 50)
		self.Platform3 = Platform((250, 250), 300, 50)

		#-# Wait Text #-#
		self.wait = [pygame.image.load("images/wait/321-0-removebg-preview.png"), pygame.image.load("images/wait/321-1-removebg-preview.png"), pygame.image.load("images/wait/321-2-removebg-preview.png"), pygame.image.load("images/wait/321-3-removebg-preview.png"), pygame.image.load("images/wait/321-4-removebg-preview.png"), pygame.image.load("images/wait/321-5-removebg-preview.png"), pygame.image.load("images/wait/321-6-removebg-preview.png"), pygame.image.load("images/wait/321-7-removebg-preview.png"), pygame.image.load("images/wait/321-8-removebg-preview.png"), pygame.image.load("images/wait/321-9-removebg-preview.png"), pygame.image.load("images/wait/321-10-removebg-preview.png"), pygame.image.load("images/wait/321-11-removebg-preview.png"), pygame.image.load("images/wait/321-12-removebg-preview.png"), pygame.image.load("images/wait/321-13-removebg-preview.png"), pygame.image.load("images/wait/321-14-removebg-preview.png"), pygame.image.load("images/wait/321-15-removebg-preview.png"), pygame.image.load("images/wait/321-16-removebg-preview.png"), pygame.image.load("images/wait/321-17-removebg-preview.png"), pygame.image.load("images/wait/321-18-removebg-preview.png"), pygame.image.load("images/wait/321-19-removebg-preview.png"), pygame.image.load("images/wait/321-20-removebg-preview.png"), pygame.image.load("images/wait/321-21-removebg-preview.png"), pygame.image.load("images/wait/321-22-removebg-preview.png"), pygame.image.load("images/wait/321-23-removebg-preview.png"), pygame.image.load("images/wait/321-24-removebg-preview.png"), pygame.image.load("images/wait/321-25-removebg-preview.png"), pygame.image.load("images/wait/321-26-removebg-preview.png"), pygame.image.load("images/wait/321-27-removebg-preview.png"), pygame.image.load("images/wait/321-28-removebg-preview.png"), pygame.image.load("images/wait/321-29-removebg-preview.png"), pygame.image.load("images/wait/321-30-removebg-preview.png"), pygame.image.load("images/wait/321-31-removebg-preview.png"), pygame.image.load("images/wait/321-32-removebg-preview.png"), pygame.image.load("images/wait/321-33-removebg-preview.png"), pygame.image.load("images/wait/321-34-removebg-preview.png"), pygame.image.load("images/wait/321-35-removebg-preview.png"), pygame.image.load("images/wait/321-36-removebg-preview.png"), pygame.image.load("images/wait/321-37-removebg-preview.png"), pygame.image.load("images/wait/321-38-removebg-preview.png"), pygame.image.load("images/wait/321-39-removebg-preview.png"), pygame.image.load("images/wait/321-40-removebg-preview.png"), pygame.image.load("images/wait/321-41-removebg-preview.png"), pygame.image.load("images/wait/321-42-removebg-preview.png"), pygame.image.load("images/wait/321-43-removebg-preview.png"), pygame.image.load("images/wait/321-44-removebg-preview.png"), pygame.image.load("images/wait/321-45-removebg-preview.png"), pygame.image.load("images/wait/321-46-removebg-preview.png"), pygame.image.load("images/wait/321-47-removebg-preview.png"), pygame.image.load("images/wait/321-48-removebg-preview.png")]
						
		#-# Setting the Players #-#
		self.TwoPlayers = True
		self.P1 = Player(self, (self.Platform2.x - 64 + 18, 490), "R")
		self.P2 = Player(self, (self.Platform1.x + self.Platform1.width - 17, 490), "L")
		self.P1.left = True
		self.P1.right = False
		self.P1.bePeasant()
		self.P2.bePeasant()

		#-# Player Texts and Scores #-#
		pygame.font.init()
		self.font = pygame.font.SysFont("ComicSansMs", 20)
		self.font2 = pygame.font.SysFont("ComicSansMs", 50)
		self.font3 = pygame.font.SysFont("ComicSansMs", 70)
		self.vampireText = self.font.render("(Vampire)", 2, Green)
		self.peasantText = self.font.render("(Peasant)", 2, Red)
		self.P1Text = self.font.render("P1", 2, Blue)
		self.P2Text = self.font.render("P2", 2, Blue)
		self.scoreP1 = self.font2.render("Player 1 Score ==> " + str(self.P1.score), 2, Maroon)
		self.scoreP2 = self.font2.render("Player 2 Score ==> " + str(self.P2.score), 2, Maroon)
	
		#-# Button Images #-#
		self.startButton = pygame.image.load("images/button/start.png")
		self.startButton = pygame.transform.scale(self.startButton, (310, 100))
		self.oneplayer = [pygame.transform.scale(pygame.image.load("images/button/oneplayer.png"), (212, 44)), pygame.transform.scale(pygame.image.load("images/button/oneplayer2.png"), (212, 44)), pygame.transform.scale(pygame.image.load("images/button/oneplayer3.png"), (212, 44))]
		self.twoplayer = [pygame.transform.scale(pygame.image.load("images/button/twoplayer.png"), (212, 44)), pygame.transform.scale(pygame.image.load("images/button/twoplayer2.png"), (212, 44)), pygame.transform.scale(pygame.image.load("images/button/twoplayer3.png"), (212, 44))]

		### Settings of Buttons ###
		self.on1PlayerButton = False
		self.click1PlayerButton = False
		self.on2PlayerButton = False
		self.click2PlayerButton = False
		self.onStartButton = False
		self.clickStartButton = False

		#-# Bullets #-#
		self.bullets = []

		#-# Settings of Jumping Intro #-#
		self.a = False
		self.b = random.choice((1, 2, 3))

		#-# Setting the FPS #-#
		self.clock = pygame.time.Clock()
		self.FPS = 60

### MENU SETTINGS ############################################################################################################################
	def Menu(self):
		#-# Game Setting #-#
		self.Run = False

		#-# Set the Mixer #-#
		pygame.mixer.pre_init(44100,-16,2, 1024 * 3)
	
		#-# Starting Pygame and Setting the Window #-#			
		pygame.init()
		self.window = pygame.display.set_mode((self.windowWidth, self.windowHeight), 0, 32)
		pygame.display.set_caption(self.windowTitle)
		
		#-# Cursor Settings #-#
		pygame.mouse.set_visible(False)

		#-# Music #-#
		self.song = pygame.mixer.Sound('sounds/music.wav')
		self.song.play(-1)
		
		while not(self.Run):
			#-# Detecting Mouse If Gone to the Buttons #-#
			self.pos = pygame.mouse.get_pos()
			if(pygame.Rect(self.windowWidth // 2 - 106, (self.windowHeight // 2) - 130, 212, 44).collidepoint(self.pos)):	
				if(pygame.mouse.get_pressed()[0]):
					self.on1PlayerButton = False						
					self.click1PlayerButton = True
				else:
					self.click1PlayerButton = False		
					self.on1PlayerButton = True
			else:
				self.on1PlayerButton = False
				self.click1PlayerButton = False

			if(pygame.Rect(self.windowWidth // 2 - 106, (self.windowHeight // 2) - 66, 212, 44).collidepoint(self.pos)):	
				if(pygame.mouse.get_pressed()[0]):
					self.on2PlayerButton = False						
					self.click2PlayerButton = True
				else:
					self.click2PlayerButton = False
					self.on2PlayerButton = True
			else:
				self.on2PlayerButton = False
				self.click2PlayerButton = False

			if(pygame.Rect(self.windowWidth // 2 - 155, (self.windowHeight // 2) - 250, 310, 100).collidepoint(self.pos)):
				if(pygame.mouse.get_pressed()[0]):
					self.onStartButton = False						
					self.clickStartButton = True
				else:
					self.clickStartButton = False
					self.onStartButton = True
			else:
				self.onStartButton = False		
				self.clickStartButton = False		

			#-# Quit Keys #-#
			for event in pygame.event.get():
				if(event.type == pygame.QUIT):
					self.Exit()
				elif(event.type == pygame.KEYDOWN):
					if(event.key == pygame.K_ESCAPE):
						self.Exit()		

				elif(event.type == pygame.MOUSEBUTTONUP):
					if(pygame.Rect(self.windowWidth // 2 - 155, (self.windowHeight // 2) - 250, 310, 100).collidepoint(self.pos)):										
						self.i = 0	
					elif(pygame.Rect(self.windowWidth // 2 - 106, (self.windowHeight // 2) - 130, 212, 44).collidepoint(self.pos)):
						self.TwoPlayers = False
						self.P1.control = "RL"
					elif(pygame.Rect(self.windowWidth // 2 - 106, (self.windowHeight // 2) - 66, 212, 44).collidepoint(self.pos)):
						self.TwoPlayers = True

			#-# Jumping Intro #-#
			if(self.TwoPlayers):
				if(self.b == 1):
					self.P1.IntroJump()
					if(self.P1.y == 340):
						self.a = True
					if(self.a == True):
						self.P2.IntroJump()	
				elif(self.b == 2):
					self.P1.IntroJump()
					self.P2.IntroJump()
				elif(self.b == 3):
					self.P2.IntroJump()
					if(self.P2.y == 340):
						self.a = True
					if(self.a == True):
						self.P1.IntroJump()
			else:
				self.P1.IntroJump()

			#-# 3 Seconds Wait Image #-#
			if(self.i < 100):
				self.i += 1
				self.clock.tick(15)	
			if(self.i == 60):
				pygame.mixer.pause()
				self.Start()

			#-# Setting FPS #-#
			self.clock.tick(self.FPS)

			#-# Redrawing the Window #-#
			self.DrawMenu()
		
	#-# Start the Game #-#
	def Start(self):
		#-# Setting Players Location #-#
		self.P1.y = 490
		self.P2.y = 490

		#-# Music #-#
		self.song2 = pygame.mixer.Sound('sounds/music2.wav')
		self.song2.play(-1)		
	
		#-# Choosing Vampire #-#
		if(self.TwoPlayers):
			self.vampire = random.choice((self.P1, self.P2))
			self.vampire.beVampire()
			if(self.vampire == self.P1):
				self.peasant = self.P2
			elif(self.vampire == self.P2):
				self.peasant = self.P1

		### MAIN LOOP ###
		self.Run = True		
		while self.Run:
			### QUIT KEYS ###
			for event in pygame.event.get():
				if(event.type == pygame.QUIT):
					self.Exit()
				elif(event.type == pygame.KEYDOWN):
					if(event.key == pygame.K_ESCAPE):
						self.song2.stop()
						#-# Setting the Players #-#
						self.TwoPlayers = True
						self.P1 = Player(self, (self.Platform2.x - 64 + 18, 490), "R")
						self.P2 = Player(self, (self.Platform1.x + self.Platform1.width - 17, 490), "L")
						self.P1.left = True
						self.P1.right = False
						self.P1.bePeasant()
						self.P2.bePeasant()
						self.i = 100
						self.Menu()

			### VAMPIRE WINS THE GAME ### 
			if(self.TwoPlayers):
				if((self.peasant.hitbox[0] <= self.vampire.hitbox[0] <= self.peasant.hitbox[0] + 29 or self.peasant.hitbox[0] <= self.vampire.hitbox[0] + 29 <= self.peasant.hitbox[0] + 29) and (self.peasant.hitbox[1] <= self.vampire.hitbox[1] <= self.peasant.hitbox[1] + 63 or self.peasant.hitbox[1] <= self.vampire.hitbox[1] + 63 <= self.peasant.hitbox[1] + 63)):            
					self.Restart()
			
			#-# Moving the Bullets #-#
			for self.bullet in self.bullets:
				if 0 < self.bullet.x < self.windowWidth:
					self.bullet.x += self.bullet.MovSpeed
				else:
					self.bullets.pop(self.bullets.index(self.bullet))

			#-# Setting FPS #-#
			self.clock.tick(self.FPS)

			#-# Redrawing the Window #-#
			self.Draw()

	### RESTART GAME WHEN IT ENDS ###
	def Restart(self):
		self.vampire.score += 1
		self.vampire.bePeasant()
		self.scoreP1 = self.font2.render("Player 1 Score ==> " + str(self.P1.score), 2, Maroon)
		self.scoreP2 = self.font2.render("Player 2 Score ==> " + str(self.P2.score), 2, Maroon)
		self.P1.x, self.P1.y = ((self.windowWidth // 2) + 100, 490)
		self.P2.x, self.P2.y = ((self.windowWidth // 2) - 100, 490)
		self.P1.Jump = False
		self.P2.Jump = False
		self.P1.left = False
		self.P1.right = False
		self.P2.left = False
		self.P2.right = False
		self.vampire = random.choice((self.P1,self.P2))
		self.vampire.beVampire()

		if(self.vampire == self.P1):
			self.peasant = self.P2
		elif(self.vampire == self.P2):
			self.peasant = self.P1

	### DRAWING ALL THINGS TO THE WINDOW ###
	def Draw(self):
		#-# Draw Window and Platforms #-#
		self.window.blit(self.windowBackground, (0, 0))
		self.Platform1.draw(self.window)
		self.Platform2.draw(self.window)
		self.Platform3.draw(self.window)

		#-# Draw Player 1 and It's Settings #-#
		self.window.blit(self.scoreP1, (0, 0))
		self.window.blit(self.P1Text, (self.P1.x + int(self.P1.width // 4) + 8, self.P1.y - int(self.P1.height // 2)))
		self.P1.draw(self.window)
		self.P1.platformControl()
		self.P1.move()
		self.P1.shoot()
		self.P1.jump()
		self.P1.jumpControl()
		
		#-# Draw Player 2 and It's Settings #-#
		if(game.TwoPlayers):
			self.window.blit(self.scoreP2, (0, 50))
			self.window.blit(self.P2Text, (self.P2.x + int(self.P2.width // 4) + 8, self.P2.y - int(self.P2.height // 2)))
			self.P2.draw(self.window)			
			self.P2.platformControl()
			self.P2.move()
			self.P2.shoot()
			self.P2.jump()	
			self.P2.jumpControl()			
			if(self.vampire == self.P1):
				self.window.blit(self.vampireText, (self.P1.x + 5, self.P1.y - int(self.P1.height // 2) + 15))
				self.window.blit(self.peasantText, (self.P2.x, self.P2.y - int(self.P2.height // 2) + 15))		
			elif(self.vampire == self.P2):
				self.window.blit(self.vampireText, (self.P2.x + 5, self.P2.y - int(self.P2.height // 2) + 15))
				self.window.blit(self.peasantText, (self.P1.x, self.P1.y - int(self.P1.height // 2) + 15))	
		else:
			self.window.blit(self.peasantText, (self.P1.x, self.P1.y - int(self.P1.height // 2) + 15))
	
		#-# Draw Bullets #-#
		for self.bullet in self.bullets:
			self.bullet.draw(self.window)

		#-# Update All Things to the Screen #-#
		pygame.display.update()

	def DrawMenu(self):
		#-# Draw Window and Buttons #-#
		self.window.blit(self.windowBackground, (0, 0))
		if(self.i == 100):
			self.window.blit(self.startButton, (self.windowWidth // 2 - 155, (self.windowHeight // 2) - 250))		
			if(self.on1PlayerButton):
				self.window.blit(self.oneplayer[2], ((self.windowWidth // 2 - 106, (self.windowHeight // 2) - 130)))
			elif(self.click1PlayerButton):
				self.window.blit(self.oneplayer[1], ((self.windowWidth // 2 - 106, (self.windowHeight // 2) - 130)))
			else:
				self.window.blit(self.oneplayer[0], ((self.windowWidth // 2 - 106, (self.windowHeight // 2) - 130)))
		
			if(self.on2PlayerButton):
				self.window.blit(self.twoplayer[2], ((self.windowWidth // 2 - 106, (self.windowHeight // 2) - 66)))
			elif(self.click2PlayerButton):
				self.window.blit(self.twoplayer[1], ((self.windowWidth // 2 - 106, (self.windowHeight // 2) - 66)))
			else:
				self.window.blit(self.twoplayer[0], ((self.windowWidth // 2 - 106, (self.windowHeight // 2) - 66)))		
		
			if(self.on1PlayerButton or self.on2PlayerButton or self.onStartButton):
				self.cursotTurn = 0
				self.cursor = self.cursorC
			elif(self.click1PlayerButton or self.click2PlayerButton or self.clickStartButton):			
				self.cursor = self.cursorC2
			else:
				self.cursor = self.cursorN

		#-# Draw Player 1 and It's Settings #-#
		self.window.blit(self.P1Text, (self.P1.x + int(self.P1.width // 4) + 8, self.P1.y - int(self.P1.height // 2)))
		self.P1.draw(self.window)

		#-# Draw Player 1 and It's Settings #-#
		if(self.TwoPlayers):
			self.window.blit(self.P2Text, (self.P2.x + int(self.P2.width // 4) + 8, self.P2.y - int(self.P2.height // 2)))
			self.P2.draw(self.window)
		
		#-# Draw 3 Second Waiting #-#
		if(self.i > 0):
			if(self.i < 48):
				self.window.blit(pygame.transform.scale(self.wait[self.i], (300, 300)), (250, 30))	
			elif(60 > self.i):
				self.window.blit(pygame.transform.scale(self.wait[48], (300, 300)), (250, 30))			
			else:
				i = 100

		#-# Cursor #-#
		if(self.cursorTurn >= len(self.cursor) - 1):
			self.cursorTurn = 0
		if(self.cursorTurn < len(self.cursor)):
			self.window.blit(self.cursor[self.cursorTurn], (self.pos)) 	
			self.cursorTurn += 1
	
		#-# Update All Things to the Screen #-#
		pygame.display.update()

	#-# Exit #-#
	def Exit(self):
		self.Run = False		
		pygame.quit()
		sys.exit()		

#-# Starting Window #-#
if (__name__ == "__main__"):
	game = Game()
	game.Menu()

player = Player()
player.x 
