import pygame
import model
import view 

BLACK = (0,0,0)
WHITE = (255,255,255)
GRAY = (127, 127, 127)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
MAGENTA = (255, 0, 255)
CYAN = (0, 255, 255)

class Button:
		
	def __init__(self, text, rect):
		self.text = text
		self.rect = rect
	
	
		self.color_top=RED
		self.color_bot=GRAY

	def draw(self, surface):
		

		self.surface=surface
		
		pygame.draw.rect(surface, self.color_top, pygame.Rect(self.rect.x, self.rect.y,self.rect.width, self.rect.height))
		pygame.draw.rect(surface, self.color_bot, pygame.Rect(self.rect.x, self.rect.y+self.rect.height/2,self.rect.width, self.rect.height/2))
	
		font = pygame.font.Font(None, 18)
		label_view = font.render(self.text[0], False, BLACK)
		label_pos = label_view.get_rect()
		label_pos.centery = self.rect.centery-self.rect.height*1/4
		label_pos.centerx = self.rect.centerx
		surface.blit(label_view, label_pos)
											
		font = pygame.font.Font(None, 18)
		label_view = font.render(self.text[1], False, BLACK)
		label_pos = label_view.get_rect()
		label_pos.centery = self.rect.centery+self.rect.height*1/4
		label_pos.centerx = self.rect.centerx
		surface.blit(label_view, label_pos)
	
	def switch_color(self):
		color_bot, color_top =self.color_top, self.color_bot
		
		pygame.draw.rect(self.surface, color_top, pygame.Rect(self.rect.x, self.rect.y,self.rect.width, self.rect.height/2))
		pygame.draw.rect(self.surface, color_bot, pygame.Rect(self.rect.x, self.rect.y+self.rect.height/2,self.rect.width, self.rect.height/2))
		self.color_top, self.color_bot = color_top, color_bot
	


	def handle_event(self, event):
		if event.type == pygame.MOUSEBUTTONDOWN:
			(x, y) = pygame.mouse.get_pos()
			if x >= self.rect.x and \
				x <= self.rect.x + self.rect.width and \
				y >= self.rect.y and \
				y <= self.rect.y + self.rect.height:
				self.on_click(event)

	def on_click(self, event):
			print("clicked")

class DataChangeButton1(Button):


	
	def __init__(self, text, rect, chart):
		Button.__init__(self, text, rect)
		self.chart = chart
		self.sorted = False
	
	
	def on_click(self, event):
		self.switch_color()
		
		if model.PARTY == 'dem':
			data = model.get_data(party = 'gop', raw= model.RAW, sort_ascending =model.SORT_ASC)

		else:
			data = model.get_data(party = 'dem', raw= model.RAW, sort_ascending =model.SORT_ASC)


		self.chart.set_values(data)


class DataChangeButton2(Button):
	
	def __init__(self, text, rect, chart):
		Button.__init__(self, text, rect)
		self.chart = chart
		self.sorted = False
	
	def on_click(self, event):
		self.switch_color()

		data = model.get_data(party = model.PARTY, raw= model.RAW, sort_ascending = not model.SORT_ASC)
		self.chart.set_values(data)

class DataChangeButton3(Button):
	
	def __init__(self, text, rect, chart):
		Button.__init__(self, text, rect)
		self.chart = chart
		self.sorted = False
	
	def on_click(self, event):
		self.switch_color()
		
		if model.RAW :
			data = model.get_data(party = model.PARTY, raw= not model.RAW, sort_ascending = model.SORT_ASC)
			self.chart.set_values(data)
			self.chart.set_decimal(True)
			self.chart.set_max_val(1)
		else:
			data = model.get_data(party = model.PARTY, raw= not model.RAW, sort_ascending = model.SORT_ASC)
			self.chart.set_values(data)
			self.chart.set_decimal(False)
			self.chart.set_max_val(10000000)
		



def main():

	pygame.init()

	screen = pygame.display.set_mode((1200, 800))

	pygame.display.set_caption("Election Data Viewer")
	pygame.display.update()

	data = model.get_data()

	bc = view.BarChart(rect=pygame.Rect(0,0,screen.get_width()-200,screen.get_height()),
					   plot_area_width_ratio=0.9,
					   plot_area_height_ratio=0.8,
					   values=data, ticks=5,
					   max_val=10000000)

	bc.set_rotate(True)
	bc.set_decimal(False)

	button1 = DataChangeButton1(["dem","gop"],pygame.Rect(screen.get_width()-200, 70, 150, 60),bc)

	button2 = DataChangeButton2(["up","down"],pygame.Rect(screen.get_width()-200, 170, 150, 60),bc)

	button3 = DataChangeButton3(["raw","%"],pygame.Rect(screen.get_width()-200, 270, 150, 60),bc)


	# display loop
	done = False
	while not done:
		screen.fill(view.BLACK)
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				done = True

			else:
				button1.handle_event(event)
				button2.handle_event(event)
				button3.handle_event(event)


		bc.draw(screen)
		button1.draw(screen)
		button2.draw(screen)
		button3.draw(screen)
		pygame.display.update()	


main()