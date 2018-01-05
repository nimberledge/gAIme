import pygame

class BoardSlot(object):

    def __init__(self, side, position, index, value = None):
        '''
        Constructor
        '''
        self.side = side
        self.width = 0
        self.height = 0
        self.radius = side / 2
        self.pos = position
        self.x = position[0]
        self.y = position[1]
        self.color = (255, 255, 255)
        self.thickness = 5
        self.val = value
        self.indx = index

    def update(self, value):
        #all this method does is update the variable which stores x,o, or None value
        self.val = value


    def draw(self, screen):
        screen_size = screen.get_size()
        pygame.draw.rect(screen, self.color, (self.pos[0], self.pos[1], self.side, self.side), self.thickness) # call the pygame draw rectangle method

        # now drawing text on gridslot
        font = pygame.font.SysFont('arial', int((self.side * 5) / 8))
        if self.val is not None:
            text = font.render(self.val, True, (255, 255, 255))
            screen.blit(text, (self.pos[0] + (self.side / 3.25), self.pos[1] + (self.side / 6)))
            pygame.display.flip()

    def get_symbol(self):
        return self.val

    def is_clicked(self, mpos):
        if self.x < mpos[0] < self.x + self.side and self.y < mpos[1] < self.y + self.side:
            return True
        return False
