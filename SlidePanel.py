# -*- coding: utf-8 -*-
import wx
from Tile import Tile
import Tools

class SlidePanel(wx.Panel):
	
	def __init__(self,P,rows=4,cols=4):
		super(SlidePanel, self).__init__(P)
		if rows<2:
			rows=4
		if cols<3:
			cols=4
		self.rows=rows
		self.cols=cols
		self.SetMinSize( (cols*50, rows*40 ))
		self.tiles=None
		self.rex=None
		
		self.won=True
		self.moves=0
		self.watch=None
		self.startable=True
		self.win=False

		self.blank=None
		self.initTiles()
		self.setGame(self.rows,self.cols)
		self.colorTiles()

		self.Bind(wx.EVT_SIZE, self.resize)
		print ("rows={0} cols={1}".format(self.rows,self.cols))


	def setGame(self,rows,cols):
		"""set game board size"""
		if not self.startable:
			if not Tools.confirm(self,'Game In Progress!! Quit Game?'):
				return False
		self.rows=rows
		self.cols=cols
		self.initTiles()

		return True
		
	def initTiles(self):
		rr=[]
		tt=[]
		n=0
		W,H=self.GetSize()
		w=W/self.cols
		h=H/self.rows
		
		for r in range(self.rows):
			y=r*h
			for c in range(self.cols):
				x=c*w
				R=x,y,w,h
				t=Tile(self,n,'%s'%(n+1), r, c )
				n+=1
				t.SetRect(R)
				tt.append(t)
				rr.append(r)
				t.Bind(wx.EVT_LEFT_UP, self.click)
		tt[-1].setBlank()
		tt[-1].scale=.25
		tt[-1].setText('Click\n\  to \n start')
		self.blank=tt[-1]
		self.startable=True
		self.tiles=tt
		self.rex=rr
		self.startable=True

	def colorTiles(self,bg=wx.CYAN,fg=wx.BLUE):
		print ('Setting Colors bg=%s fg=%s'%(bg,fg ))
		for t in self.tiles:
			t.SetBackgroundColour(bg)
			t.SetForegroundColour(fg)
		self.Refresh()

	def tAtRC(self,r,c):
		"""return the tile at r,c"""
		for t in self.tiles:
			tr,tc=t.getRC()
			if r==tr and c==tc:
				return t
		print ('Nothing at %s,%s'%(r,c))
		return None

	def rAtRC(self, r,c):
		"""return the rectangle at r,c"""
		i=r*self.cols+c
		return self.rex[i]

	def resize(self,e):
		W,H=self.GetSize()
		w=W/self.cols
		h=H/self.rows
		n=0
		for r in range(self.rows):
			y=r*h
			for c in range(self.cols):
				x=c*w
				self.rex[n]=x,y,w,h
				t=self.tAtRC(r,c)
				t.SetRect(self.rex[n])


	def click(self,e):
		t=e.GetEventObject()
		print('%s'%(t))





class App(wx.App):
	
	def __init__(self):
		super(App, self).__init__()
		F=wx.Frame(None)
		sp=SlidePanel(F,4,4)
		box=wx.BoxSizer(wx.VERTICAL)
		box.Add(sp, 1, wx.EXPAND, wx.ALL)
		F.SetSizer(box)
		F.Fit()
		F.Show()

if __name__=='__main__':
	App().MainLoop()












