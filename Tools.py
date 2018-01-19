# -*- coding: utf-8 -*-
import wx
from Score import decode
from Score import SessionScores

HISCORE="highScores"

def confirm(parent,Q):
	qd= wx.MessageDialog(parent,Q,'warning', wx.ICON_EXCLAMATION | wx.YES_NO | wx.NO_DEFAULT)
	return qd.ShowModal() == wx.ID_YES


def saveScores(scores, fn=HISCORE):
	f = open(fn, 'w')
	for s in scores():
		f.write('%s\n'%(s))
	f.close()

def loadScores(session=None,fn=HISCORE):
	f = open(fn, 'w')
	line=''
	if session ==None:
		session=SessionScores()
	while (line != None) :
		line=f.readLine()
		s=decode(line)
		session.add(s)
	return session

class RCPane(wx.Panel):
	
	def __init__(self,P,r=4,c=4):
		super(RCPane, self).__init__()
		self.rows=r
		self.cols=c
		labR=wx.StaticText("Rows: ")
		labC=wx.StaticText("  Cols: ")
		
		self.tfRows=wx.TextCtrl(self,-1,'%s'%(r) )
		self.tfCols=wx.TextCtrl(self,-1,'%s'%(c) )
		self.brc=wx.Button(self,-1,'Set')
		hz=wx.BoxSizer(wx.HORIZONTAL)
		hz.Add(labR)
		hz.Add(self.tfRows)
		hz.Add(labC)
		hz.Add(self.tfCols)
		Z=wx.BoxSizer(wx.VERTICAL)
		Z.Add(hz)
		Z.Add(self.brc)
		self.SetSizer(Z)
		self.Fit()




