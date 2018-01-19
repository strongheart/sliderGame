# -*- coding: utf-8 -*-
import wx

class Tile(wx.Window):
	
	def __init__(self,P,id,txt, r,c,blank=False):
		super(Tile, self).__init__(P,id)
		self.id=id # =tile index
		self.text=txt
		self.row=r
		self.col=c
		self.blank=blank
		self.scale=.75
		self.tiles=None
		self.rex=[]
		self.Bind(wx.EVT_PAINT,self.paint)

	def isBlank(self):
		return self.blank

	def setBlank(self, b=True):
		self.blank=b

	def setRC(self, r,c):
		self.row=r
		self.col=c

	def getRC(self):
		return self.row, self.col

	def getId(self):
		return self.id

	def setText(self,t):
		self.text=t

	def placed(self, cols):
		"""True if placed in proper r,c cols=# of columns in the board"""
		x=self.row*cols+self.col
		if x==self.id :
			return True
		#else:
			#print('NOT PLACED %s x=%s'%(self,x))

	def __str__(self):
		T=self.text
		if self.isBlank():
			T='*'
		rc='(%s,%s)'%(self.getRC())
		x,y,w,h=self.GetRect()
		R='%s,%s,%s,%s'%(x,y,w,h)
		bg=hex(self.GetBackgroundColour().GetRGB())
		fg=hex(self.GetForegroundColour().GetRGB())
		C='(%s),(%s)'%(bg,fg)
		return '{T} {id},{rc}, [{R}]  {C}'.format(T=T, rc=rc, id=self.id, R=R,C=C  )

	def paint(self,e):
		W,H=self.GetSize()
		dc=wx.PaintDC(self)
		dc.SetBrush(wx.Brush(self.GetBackgroundColour()))
		dc.SetPen(wx.Pen(self.GetForegroundColour()))
		dc.DrawRectangle(0,0,W,H)
		def cent():
			
			if W*H<1 :
				print ('WTF!!!! ')
			f=self.GetFont()
			f.SetPixelSize((0,self.scale*H))
			dc.SetFont(f)
			w,h=dc.GetTextExtent(self.text)
			return (W-w)//2,(H-h)//2
		w,h=cent()
		dc.SetTextBackground(self.GetBackgroundColour())
		dc.SetTextForeground(self.GetForegroundColour())
		dc.DrawText(self.text,w,h)

















