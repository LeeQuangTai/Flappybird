import pygame, sys, random, os

WHITE = (255, 255, 255)
PINK = (235, 4, 80)
GREEN = (38, 236, 81)

def draw_floor():
	screen.blit(floor_surface, (floor_position,600)) #screen.blit(<variable>,postion{x,y})
	screen.blit(floor_surface, (floor_position + 396,600)) #screen.blit(<variable>,postion{x,y})
def draw_background():
	screen.blit(bg_surface,(bg_postion,0)) #screen.blit(<variable>, postion{x,y})
	screen.blit(bg_surface,(bg_postion + 996,0)) #screen.blit(<variable>,postion{x,y})
def create_pipe():
	position = random.choice(pipe_height)
	top_pipe =  pipe_surface.get_rect(midtop = (400,position))# ??
	bottom_pipe = pipe_surface.get_rect(midbottom = (400,position - 150)) #???
	return bottom_pipe, top_pipe
def move_pipe(pipes): # array of pipe 
	for pipe in pipes:
		pipe.centerx -= 2 #speed of pipes
	return pipes
def draw_pipe(pipes):
	for pipe in pipes: 
		if pipe.bottom >= 600:
			screen.blit(pipe_surface, pipe)
		else: 
			flip_pipe = pygame.transform.flip(pipe_surface, False, True)
			screen.blit(flip_pipe, pipe)
def kill_pipe(pipe_list):
	for pipe in pipe_list:
		if pipe.centerx < -50:
			pipe_list.pop(0)
def check_collision(pipe_list): 
	for pipe in pipe_list: 
		if bird_rectangle.colliderect(pipe) or bird_rectangle.top <= -100 or bird_rectangle.bottom >= 600 :
			collision_sound.play()
			pygame.time.delay(1000)
			return 	False 
	return True
def rotate_bird(bird): # rotate the character
	new_bird = pygame.transform.rotozoom(bird, - bird_movement *3, 100/100)
	return new_bird
def gameover_display(game_status):
	if game_status == "main_game":
		score_surface = game_font.render(str(int(score)), True, WHITE)
		score_rect = score_surface.get_rect(center = (200,100))
		screen.blit(score_surface,score_rect)

	elif game_status == "game_over":
		score_surface1 = game_font.render(('score'),True,WHITE)
		score_surface = game_font.render(str(int(score)),True,WHITE)
		score_rect = score_surface.get_rect(center = (200,100))
		screen.blit(score_surface,score_rect)
		screen.blit(score_surface1,(150, 10))

		#high score
		high_score_surface1 = game_font.render(('HIGH SCORE'),True,GREEN)
		high_score_surface = game_font.render(str(int(high_score)),True,GREEN)
		high_score_rect = high_score_surface.get_rect(center = (200,540))
		screen.blit(high_score_surface,high_score_rect)
		screen.blit(high_score_surface1,(100, 440))
def score_update(score, high_score):
	if high_score < score:
		high_score = score
	return high_score
def score_check(): 
	global score
	if pipe_list:
		for pipe in pipe_list: 
			if 145 < pipe.centerx < 148: 
				score += 0.5
				pygame.mixer.Sound.play(score_up_sound)

def sound_change():
	rand_music = random.choice(list_bg_music)
	music = pygame.mixer.music.load(rand_music)
	pygame.mixer.music.play(-1)
#high score file
def Read_high_score():
	read_high_score = open("assets/high_score_file.txt",'r')
	high_score = read_high_score.read()
	return high_score
def Save_high_score():
	global high_score
	if int(Read_high_score()) < high_score: 
		save_high_score = open("assets/high_score_file.txt", "w")
		save_high_score.write(str(int(high_score)))

#define the scale of the screen
screen_scale = (396,704)
pygame.init()#init pygame lib
pygame.mixer.init()


screen = pygame.display.set_mode(screen_scale) 
pygame.display.set_caption("Flapin Da City")
clock = pygame.time.Clock()

#init a file to save the high score
if(os.path.isfile('assets/high_score_file.txt') == False):
	file = open("assets/high_score_file.txt", 'w')
	file.write('0')
	file.close()
#game sound
list_bg_music = ["assets/crazyforyou.mp3", "assets/bg_sound.mp3","assets/sound1.mp3","assets/sound2.mp3","assets/sound3.mp3","assets/sound4.mp3"]
rand_music = random.choice(list_bg_music)
music = pygame.mixer.music.load(rand_music)
collision_sound = pygame.mixer.Sound("assets/collision.wav")
score_up_sound = pygame.mixer.Sound("assets/score-up.wav")
flap_sound = pygame.mixer.Sound("assets/flap_sound.wav")

#game variable
gravity = 0.25  
bird_movement = 0
game_active = False
score = 0
high_score = int(Read_high_score());
game_font = pygame.font.Font('assets/game.ttf', 50)
check_start = True


#back ground
bg_surface = pygame.image.load("assets/back-ground.jpg").convert()
#bg_surface = pygame.transform.scale(bg_surface,(396,996))#adjust to fit background image with the screen
bg_postion = 0

#message
message = pygame.image.load('assets/message.png').convert_alpha()

#character
#bird = pygame.image.load("assets/bluebird-upflap.png").convert_alpha()
bird = pygame.transform.scale(pygame.image.load("assets/bluebird-upflap.png").convert_alpha(), (45,35))
bird_positionY = 300
bird_rectangle = bird.get_rect(center = (150,bird_positionY))

#pipe

pipe_surface = pygame.transform.scale(pygame.image.load("assets/pipe-red.png").convert(),(70, 350))
pipe_list = []
SPAWNPIPE = pygame.USEREVENT
pygame.time.set_timer(SPAWNPIPE, 1200)
pipe_height = [250, 300, 400, 450]

#floor of the game
floor_surface = pygame.image.load("assets/floor-surface.png").convert_alpha()#convert is the way that make python read image faster
floor_surface = pygame.transform.scale(floor_surface, (396,150)) #adjust to fit floor-surface image with the screen
floor_position  = 0 # define

# loop to built the game
while True:  
	for	event in pygame.event.get():
		if event.type == pygame.QUIT:
			pygame.quit()
			sys.exit() #quit program in console
		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_SPACE and game_active:
				flap_sound.play()
				bird_movement = 0
				bird_movement -= 5 #mức độ nảy của nhân vật
			if event.key == pygame.K_SPACE and game_active == False:
				game_active = True
				pipe_list.clear()
				bird_rectangle.center = (150, 300)
				bird_movement = 0
				score = 0

		if event.type == SPAWNPIPE: 
			pipe_list.extend(create_pipe())
	draw_background()

	bg_postion -= 0.8 #0.8 is the speed of floor movement
	if bg_postion < -996:
		bg_postion = 0
	if check_start == True: 
		#message
		screen.blit(message,(106,150))
		check_start = False

	
	if game_active and check_start == False:
		#bird
		bird_movement +=  gravity 
		rotated_bird = rotate_bird(bird)
		screen.blit(rotated_bird,bird_rectangle)
		bird_rectangle.centery += bird_movement # this is bird_rectangle.center y if you want to drop from the high
		game_active = check_collision(pipe_list)
		#pipes
		pipe_list = move_pipe(pipe_list)
		draw_pipe(pipe_list)
		kill_pipe(pipe_list)
		#score		
		score_check()  
		gameover_display("main_game")
	else:
		#pygame.mixer.music.play(-1)
		sound_change()
		high_score = score_update(score,high_score) 
		Save_high_score()
		gameover_display("game_over")
		screen.blit(message,(106,150))
	#floor 	
	draw_floor()
	floor_position -= 1 #0.8 is the speed of floor movement
	if floor_position < -396:
		floor_position = 0

	pygame.display.update()
	clock.tick(120)# limit movement of the screen per second	