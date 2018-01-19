# -*- coding: utf-8 -*-
import wx
from SlidePanel import SlidePanel
import Tools
from random import randint
from Score import Score, SessionScores

MIXES=12



class MoveSlider(SlidePanel):
	
	def __init__(self,P,r=4,c=4,m=0):
		super(MoveSlider, self).__init__(P,r,c)
		#self.shuffle(25)
		self.report=True
		self.session=None
		self.score=None
		if m==None or m<=0:
			m=(self.rows+1)*(self.cols+1)
		self.mixes=m
		self.gsize=self.rows*self.cols
		MoveSlider.MIXES=m


	def click(self,e):
		t=e.GetEventObject()
		if t==self.blank :
			if self.startable or self.win:
				self.start()
			return
		if self.win:
			self.blank.setText("WIN\nStart")
			return ### dont' move'
		else :
			br,bc=self.blank.getRC()
			r,c=t.getRC()
			if r==br:
				self.moveHoriz(t)
			if c==bc:
				self.moveVert(t)
			self.moves+=1
			win=self.isWin()
			if win or self.report :
				S='move:%s\n%s'%(self.moves,self.timeStr())
				if win:
					S="WIN\n"+S
				self.blank.setText(S)

	def timeStr(self,t=None):
		if t==None:
			t=self.watch.Time()
		s=t//1000
		m=s//60
		s-=60*m
		M='%s'%(m)
		S='00%s'%(s)
		return '%s:%s'%(M[-2:],S[-2:])
		
		

	def start(self):
		if self.win:
			self.startable=True
			self.win=False
		else:
			if not self.startable:
				if Tools.confirm(self,"Do you want to abort the game in progress? "):
					self.startable=True
				else:
					return
	
		self.setGame(self.rows,self.cols) ## toggle infomode
		self.colorTiles()
		self.shuffle(self.mixes)
		self.blank.setText("")
		self.moves=0
		self.startable=False
		if self.watch==None:
			self.watch=wx.StopWatch()
		self.watch.Start(0)

	def isWin(self):
		for t in self.tiles:
			if not t.placed(self.cols):
				return False
		print("WIN")
		self.win=True
		self.watch.Pause()
		self.doWin()
		return True


	def moveHoriz(self,t):
		br,bc=self.blank.getRC()
		r,c=t.getRC()
		d=bc-c
		if d>0:
			self.moveRight(d)
		else:
			self.moveLeft(-d)



	def moveVert(self,t):
		br,bc=self.blank.getRC()
		r,c=t.getRC()
		d=br-r
		if d>0:
			self.moveDown(d)
		else :
			self.moveUp(-d)

		self.Refresh()

	# blank
	def moveLeft (self,d):
		for n in range(d):
			br,bc=self.blank.getRC()
			t=self.tAtRC(br,bc+1)
			self.swapPlaces(t)
			self.swapRC(t)

	def moveRight (self,d):
		for n in range(d):
			br,bc=self.blank.getRC()
			t=self.tAtRC(br,bc-1)
			self.swapPlaces(t)
			self.swapRC(t)

	def moveUp (self,d):
		for n in range(d):
			br,bc=self.blank.getRC()
			t=self.tAtRC(br+1,bc)
			self.swapPlaces(t)
			self.swapRC(t)

	def moveDown (self,d):
		for n in range(d):
			br,bc=self.blank.getRC()
			t=self.tAtRC(br-1,bc)
			self.swapPlaces(t)
			self.swapRC(t)

	def swapRC(self,t):
		br,bc=self.blank.getRC()
		r,c=t.getRC()
		t.setRC(br,bc)
		self.blank.setRC(r,c)

	def swapPlaces(self,t):
		bR=self.blank.GetRect()
		tR=t.GetRect()
		t.SetRect(bR)
		self.blank.SetRect(tR)

	def shuffle(self, mixes=MIXES):
		print("MIXES=%s"%(mixes))
		for n in range (mixes):
			r,c=self.blank.getRC()
			d=randint(0,self.rows-1)
			d%=self.rows +1
			#d+=1
			#print ('D=%s'%(d))
			t=self.tAtRC(d,c)
			self.moveVert(t)
			d=randint(0,self.cols-1)
			d%=self.cols+1
			#d+=1
			#print ('D=%s'%(d))
			t=self.tAtRC(r,d)
			self.moveHoriz(t)

	def doWin(self):
		t=self.watch.Time()
		#rcmtp
		score=Score(self.rows, self.cols, self.moves, self.timeStr(t))
		if self.session==None:
			self.session=SessionScores()
		self.session.add(score)
		self.score=score ### maybe get rid of self.score
		print('%s'%(self.session))
		am=self.session.avgMoves(self.gsize)
		at=self.session.avgTime(self.gsize)
		print("avg m={0} avg T={1}".format(am,at) )
		










class App(wx.App):
	
	def __init__(self):
		super(App, self).__init__()
		F=wx.Frame(None)
		sp=MoveSlider(F,4,4)
		box=wx.BoxSizer(wx.VERTICAL)
		box.Add(sp, 1, wx.EXPAND, wx.ALL)
		F.SetSizer(box)
		F.Fit()
		F.Show()
		

if __name__=='__main__':
	App().MainLoop()