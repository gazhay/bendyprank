/*
    Bendy and the Ink Machine, BATIM, and all grpahics and sounds are © The Meatly
    NOT AN OFFICIAL BENDY AND THE INK MACHINE PRODUCT. NOT APPROVED BY OR ASSOCIATED WITH THEMEATLY GAMES, LTD.

    Code below released under GPLv2
*/

import wx
import subprocess
from random import randint
from time   import sleep

IMAGE_PATH    = 'Bendy.png'
WAKE_SPEAKERS = True

class ShapedFrame(wx.Frame):
    def __init__(self):
        wx.Frame.__init__(self, None, -1, "Shaped Window", style = wx.FRAME_SHAPED | wx.SIMPLE_BORDER)
        self.hasShape = False
        self.delta    = wx.Point(0,0)
        image = wx.Image(IMAGE_PATH, wx.BITMAP_TYPE_PNG)
        self.bmp = wx.BitmapFromImage(image)
        self.SetClientSize((self.bmp.GetWidth(), self.bmp.GetHeight()))
        dc = wx.ClientDC(self)
        dc.DrawBitmap(self.bmp, 0,0, True)
        self.SetWindowShape()
        self.hider  = wx.Timer(self)
        self.shower = wx.Timer(self)
        self.Bind(wx.EVT_RIGHT_UP,         self.OnExit             )
        self.Bind(wx.EVT_PAINT,            self.OnPaint            )
        self.Bind(wx.EVT_WINDOW_CREATE,    self.SetWindowShape     )
        self.Bind(wx.EVT_ERASE_BACKGROUND, self.OnEraseBackground  )
        self.Bind(wx.EVT_TIMER,            self.timertrigger, self.hider )
        self.Bind(wx.EVT_TIMER,            self.showagain   , self.shower)
        (w,h) = wx.GetDisplaySize()
        self.SetPosition(wx.Point( (w-self.bmp.GetWidth())/2, (h-self.bmp.GetHeight())/2 ))
        self.hider.Start(500, True)

    def OnEraseBackground(self,evt=None):
        pass

    def SetWindowShape(self, evt=None):
        r = wx.RegionFromBitmap(self.bmp)
        self.hasShape = self.SetShape(r)

    def OnPaint(self, evt):
        dc = wx.PaintDC(self)
        dc.DrawBitmap(self.bmp, 0,0, True)

    def OnExit(self, evt):
        self.Close()

    def timertrigger(self, evt):
        self.hider.Stop()
        self.Show(False)
        self.shower.Start(randint(300,1500)*1000, True)

    def showagain(self, evt):
        self.shower.Stop()
        # Wake up speakers too
        if WAKE_SPEAKERS:
            cmdstr = "aplay Silent.wav"
            subprocess.call(cmdstr, shell=True)
        cmdstr = "aplay SFX_Jumpscare_01.wav".split()
        subprocess.Popen(cmdstr, stdin=None, stdout=None, stderr=None, close_fds=True)
        self.Show(True)
        self.hider.Start(500, True)

if __name__ == '__main__':
    try:
        app    = wx.App(False)
        if WAKE_SPEAKERS:
            cmdstr = "aplay Silent.wav"
            subprocess.call(cmdstr, shell=True)
        cmdstr = "aplay SFX_Jumpscare_01.wav".split()
        subprocess.Popen(cmdstr, stdin=None, stdout=None, stderr=None, close_fds=True)
        ShapedFrame().Show()
        app.MainLoop()

    except KeyboardInterrupt:
        exit(0)
