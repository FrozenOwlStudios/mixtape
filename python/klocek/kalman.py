import numpy as np

class KalmanFilter:

    STATE_X = 0
    STATE_Y = 1
    STATE_DX = 2
    STATE_DY = 3
    STATE_DDX = 4
    STATE_DDY = 5


    def __init__(self):
        pass

    def process(self, s, z):
        s_new = np.copy(s)
        s_new[self.STATE_X] =  s[self.STATE_X] + z[self.STATE_DX]
        s_new[self.STATE_Y] =  s[self.STATE_Y] + z[self.STATE_DY]
        s_new[self.STATE_DX] = z[self.STATE_DX]
        s_new[self.STATE_DY] = z[self.STATE_DY]
        return s_new
