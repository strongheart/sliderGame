# -*- coding: utf-8 -*-
import wx
from MoveSlider import MoveSlider
import Tools


class SlideFrame(wx.Frame):
	
	def __init__(self,P,rows=4, cols=4, mixes=0):
		super(SlideFrame, self).__init__(P)
		slider=MoveSlider(self,rows,cols,mixes)
		
		Z= wx.BoxSizer()
		Z.Add(slider,flag=wx.EXPAND,proportion=1)
		mbar=wx.MenuBar()
		mengame=wx.Menu()
		menstyle=wx.Menu()
		miRC=mengame.Append(wx.NewId(),'Size','Change rows and columns')
		#miSep=mengrid.Append(wx.NewId(),'','')
		miNumbers=menstyle.Append(wx.NewId(),'Numbers','Change Numbers/Letters', wx.ITEM_RADIO)
		miLetters=menstyle.Append(wx.NewId(),'Letters','Change Numbers/Letters', wx.ITEM_RADIO)
		miPictures=menstyle.Append(wx.NewId(),'Pictures','Change Numbers/Letters', wx.ITEM_RADIO)
		miColors=menstyle.Append(wx.NewId(),'Color Prefs','Change BG, FG Colors')
		mbar.Append(mengame,'&Game')
		mbar.Append(menstyle,'&Style') 	 	
		self.SetMenuBar(mbar)
		self.Bind(wx.EVT_MENU, self.setRC, miRC)
		
		self.slider=slider
		self.SetSizer(Z)
		self.Fit()
		self.SetSize( (700,500) )
		
	def setRC(self,e):
		pass

	def setImg(self,e):
		'''change to a picture puzzle -open browser'''
		pass

	def setAlpha(self,e):
		'''change to a alphabet puzzle '''
		pass

	def setNum(self,e):
		'''change to a Number puzzle (default) '''
		pass

	def setText(self,e):
		''' write a message into the tile  open editor'''
		pass
		







class App(wx.App):
	def __init__(self):
		super(App, self).__init__()
		frame = SlideFrame(None,4,5,25)
		frame.Show(True)


if __name__ == '__main__':
	app = App()
	app.MainLoop()






