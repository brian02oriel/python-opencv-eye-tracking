from screeninfo import get_monitors
import math

class PanelInfo:
    def __init__(self):
        self.screen_width, self.screen_height = get_monitors()[0].width, get_monitors()[0].height
        
    def get_screen_resolution(self):
        return self.screen_width, self.screen_height
    def get_frame_center(self, width, heigh):
        self.frame_width, self.frame_height = width, heigh
        return self.frame_width // 2, self.frame_height // 2
