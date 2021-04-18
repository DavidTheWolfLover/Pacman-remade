class Pause(object):
    def __init__(self, paused=False):
        self.check_pause = paused
        self.timer = 0
        self.pauseTime = 0
        self.playerPaused = paused
        self.pauseType = None 
        
    def update(self, t):
        if not self.playerPaused and self.check_pause:
                self.timer += t
                if self.timer >= self.pauseTime:
                    self.timer = 0
                    self.check_pause = False
                
    def start(self, pauseTime, pauseType=None):
        self.pauseTime = pauseTime
        self.pauseType = pauseType
        self.timer = 0
        self.check_pause = True
        
    def player(self):
        self.playerPaused = not self.playerPaused
        if self.playerPaused:
            self.check_pause = True
        else:
            self.check_pause = False

    def force(self, pause):
        self.check_pause = pause
        self.playerPaused = pause
        self.timer = 0
        self.pauseTime = 0
