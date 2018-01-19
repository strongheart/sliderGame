#!/usr/bin/python
# -*- coding: utf-8 -*-

import wx
from MoveSlider import MoveSlider
from SlideFrame import SlideFrame


class MyFrame(wx.Frame):
	def __init__(self, P = None):
		super(MyFrame, self).__init__(P)
		self.SetTitle("Strongheart's Slider Puzzle")
		pane = MoveSlider(self)
		sizer = wx.BoxSizer(wx.VERTICAL)
		sizer.Add(pane, 1, wx.EXPAND, wx.ALL)
		self.SetBackgroundColour(wx.CYAN)
		self.SetSizer(sizer)
		self.pane = pane
		self.sizer = sizer
		self.SetSize(wx.GetDisplaySize())


class App(wx.App):
	def __init__(self):
		super(App, self).__init__()
		#frame = MyFrame(None)
		frame = SlideFrame(None,4,5,20)
		frame.Show(True)


if __name__ == '__main__':
	app = App()
	app.MainLoop()




