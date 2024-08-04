import pygame

class SoundPlayer:
    def __init__(self,cols,rows):
        self.mute = False
        pygame.mixer.init()
        self.reelStopSound = None
        self.reelWildSound = None
        self.readyToPlaySoundREEL = []
        self.hasPlayedSoundREEL = []
        self.readyToPlaySoundWILD = [[False] * rows for _ in range(cols)]
        self.hasPlayedSoundWILD = [[False] * rows for _ in range(cols)]
        self.resetReelSounds(cols, rows)

    def setReelStopSound(self, soundFile):
        if soundFile != None:
            self.reelStopSound = soundFile

    def setWildSound(self, soundFile):
        if soundFile != None:
            self.reelWildSound = soundFile
        
    def resetReelSounds(self, cols, rows):
        self.readyToPlaySoundREEL = [False for _ in range(cols)]
        self.hasPlayedSoundREEL = [False for _ in range(cols)]
        
        self.readyToPlaySoundWILD = [[False] * rows for _ in range(cols)]
        self.hasPlayedSoundWILD = [[False] * rows for _ in range(cols)]
    
    def playReelStopSound(self, i):
        if self.readyToPlaySoundREEL[i] and not self.mute and self.reelStopSound != None:
            self.reelStopSound.play()
            self.readyToPlaySoundREEL[i] = False
            self.hasPlayedSoundREEL[i] = True

    def playWildSound(self,i,j, bonusOut):
        if self.readyToPlaySoundWILD[i][j] and not self.mute and self.reelWildSound != None and not bonusOut:
            self.reelWildSound.play()
            self.readyToPlaySoundWILD[i][j] = False
            self.hasPlayedSoundWILD[i][j] = True
    
    def checkIfReelStopped(self,j,rows,i):
        if j == rows-1:
            if not self.hasPlayedSoundREEL[i]:
                self.readyToPlaySoundREEL[i] = True
        return self.readyToPlaySoundREEL[i]

    def checkIfPlayedWildSound(self,i,j):
        if not self.hasPlayedSoundWILD[i][j]:
            self.readyToPlaySoundWILD[i][j] = True