# -*- coding: utf-8 -*-
import sys
import getpass
from datetime import datetime, date, time


def decode(S):
	ss=S.strip().split(',')
	print("Decoding:{0} len.ss={1}".format(S,len(ss)))
	D=dict()
	for s in ss:
		k,v=s.strip().split('=')
		k=k.strip().lower()
		D[k]=v.strip()
	R=D['rows']
	C=D['cols']
	M=D['moves']
	T=D['time']
	P=D['player']
	D=D['date']
	r=int(R)
	c=int(C)
	m=int(M)
	t=int(T)
	return Score(r,c,m,t,P,D)

class Score(object):
	
	ID=0
		
	def __init__(self,r,c,m,t,p=None, dt=None):
		"""r=rows, c=cols, m=moves t=time (string 'm:ss') player if None look up username, date y-m-d-H:M:S
		types:
			r, c, m, t=int
			dt= datetime or str (always converted to str)
		"""
		self.gsize=r*c
		self.grid='%sx%s'%(r,c)
		Score.ID+=1
		self.id=Score.ID
		self.rows=r
		self.cols=c	
		self.size=r*c
		self.moves=m
		self.time=t
		self.player=p
		if dt==None:
			dt=datetime.now()
		self.date=str(dt)

	def __eq__(self,s):
		return self.id==s.id and self.moves==s.moves and self.time==s.time
		

	def __gt__(self,s):
		return not self.__le__(s)
	
	def __lt__(self,s):
		return not self.__ge__(s) #self.moves<s.moves
	
	def __ge__(self,s):
		return not self.moves<s.moves and self.time>=s.time
	
	def __le__(self,s):
		return not self.moves>s.moves and self.time<=s.time
	
	def __str__(self):
		p=self.player
		m='%s'%(self.moves)
		#t=self.time
		#r=self.rows
		#c=self.cols
		#d=self.date
		g='rows=%s, cols=%s'%(self.rows, self.cols)
		i='id=%s'%(self.id)
		return 'player={P}, moves={M}, time={T}, {G}, {I}, date={D}  '.format(I=i, P=p,M=m,G=g, T=self.time , D=self.date )





class SessionScores(object):
	
	def __init__(self):
		self.scores=[]
		self.date=datetime.date(datetime.now())
		self.grids=dict()

	def __len__(self):
		return len(self.scores)

	def add(self,score):
		z=len(self.scores)
		if z<1:
			self.scores.append(score)
			return
		else:
			for n in range(z):
				s=self.scores[n]
				if score <=s:
					self.scores.insert(n,score)
					return
		self.scores.append(score)

	def addMany(self,scores):
		for s in scores:
			self.add(s)

	def enum(self):
		for s in self.scores:
			yield s

	def __split(self):
		D=self.grids
		for s in self.scores:
			x=s.size
			if not x in D:
				D[x]=[]
			if len(D[x])==0 or s not in D[x]:
				D[x].append(s)
		for k in D:
			g=D[k]
			D[k]=sorted(g)
		self.grids=D

	def getGrids(self):
		'''grids is a dictionary keys=sizes of boards 3x3,3x4,4x4 etc '''
		self.__split()
		return self.grids

	def __str__(self):
		g=self.getGrids()
		kk=sorted(g.keys())
		S=''
		for k in kk:
			ss=g[k]
			i=1
			print ("grid -%s"%(k) )
			for s in ss:
				S+=('%s. %s\n'%(i,s))
				i+=1
		return S

	def getGrid4Key(self,k):
		g=self.getGrids()
		return g[k]

	def avgMoves(self,k):
		ss=None
		t=0
		if k<=0:
			ss=self.scores
		else :
			g=self.getGrids()
			ss=g[k]
			if not ss:
				return self.avgMoves(0)
		i=0
		for s in ss:
			t+=s.moves
			i+=1
		if i==0:
			return -1,''
		return t/i #, '{:.2}'.format(t/i)


	def avgTime(self,k):
		ss=self.getGrid4Key(k)
		if not ss:
			ss=self.scores
		v=0
		i=0
		def _dt(T):
			M,S=T.split(':')
			m=int(M)
			s=int(S)
			return 60.0*m+s
			
		for s in ss:
			t=_dt(s.time)
			v+=t
			i+=1
		return v/i #, '{:.2}.format(v/i)'



	#def save(self):


	#def decode(self, S):
		
		



'''



s1 = Score(4,4,40,'3:21','Dude')
s2= Score(4,4,45,'3:31','Dude')
s3= Score(4,4,35,'3:21','Dude')
s4= Score(4,4,45,'3:11','Dude')

S1 = Score(5,4,40,'4:21','Dude')
S2= Score(3,3,45,'2:31','Dude')
S3= Score(5,5,35,'4:21','Dude')
S4= Score(4,4,45,'3:11','Dude')

ss=[s1,s2,s3,s4,S1,S2,S3,S4]

ses=SessionScores()
ses.addMany(ss)
for s in ses.enum():
	print('score %s'%(s))

print ('\n++++++++++++++')
g=ses.getGrids()
kk=sorted(g.keys())
for k in kk:
	ss=g[k]
	for s in ss:
		print ('%s score=%s'%(k,s))

print ('++++++++++++++')

for k in kk:
	print ('k="%s"'%(k))

print ('+++  k=20  +++')
k=16
ss=g[k]
for s in ss:
	print ('%s score=%s'%(k,s))




grid -16
1. player=None, moves=8, time=0:23, rows=4, cols=4, id=13, date=2018-01-08 06:24:49.686973
2. player=None, moves=13, time=0:28, rows=4, cols=4, id=11, date=2018-01-08 06:22:52.535058
3. player=None, moves=33, time=0:37, rows=4, cols=4, id=15, date=2018-01-08 06:26:26.835485
4. player=None, moves=45, time=0:53, rows=4, cols=4, id=10, date=2018-01-08 06:22:19.467719
5. player=None, moves=54, time=0:53, rows=4, cols=4, id=14, date=2018-01-08 06:25:45.663811
6. player=None, moves=58, time=1:02, rows=4, cols=4, id=9, date=2018-01-08 06:21:20.923289


1. player=None, moves=2, time=0:04, rows=4, cols=4, id=26, date=2018-01-08 06:37:19.060172
2. player=None, moves=8, time=0:23, rows=4, cols=4, id=13, date=2018-01-08 06:24:49.686973
3. player=None, moves=11, time=0:13, rows=4, cols=4, id=21, date=2018-01-08 06:33:57.487039
4. player=None, moves=11, time=2:39, rows=4, cols=4, id=17, date=2018-01-08 06:31:29.121844
5. player=None, moves=15, time=0:19, rows=4, cols=4, id=18, date=2018-01-08 06:31:50.543360
6. player=None, moves=21, time=0:22, rows=4, cols=4, id=24, date=2018-01-08 06:36:10.932833
7. player=None, moves=13, time=0:28, rows=4, cols=4, id=11, date=2018-01-08 06:22:52.535058
8. player=None, moves=40, time=0:36, rows=4, cols=4, id=22, date=2018-01-08 06:34:35.345028
9. player=None, moves=33, time=0:37, rows=4, cols=4, id=15, date=2018-01-08 06:26:26.835485
10. player=None, moves=45, time=0:49, rows=4, cols=4, id=19, date=2018-01-08 06:32:42.073843
11. player=None, moves=45, time=0:53, rows=4, cols=4, id=10, date=2018-01-08 06:22:19.467719
12. player=None, moves=47, time=0:57, rows=4, cols=4, id=20, date=2018-01-08 06:33:42.089856
13. player=None, moves=54, time=0:53, rows=4, cols=4, id=14, date=2018-01-08 06:25:45.663811
14. player=None, moves=39, time=0:54, rows=4, cols=4, id=23, date=2018-01-08 06:35:45.143388
15. player=None, moves=46, time=0:58, rows=4, cols=4, id=25, date=2018-01-08 06:37:12.379997
16. player=None, moves=58, time=1:02, rows=4, cols=4, id=9, date=2018-01-08 06:21:20.923289
17. player=None, moves=65, time=1:28, rows=4, cols=4, id=12, date=2018-01-08 06:24:23.451334
18. player=None, moves=78, time=1:30, rows=4, cols=4, id=30, date=2018-01-08 06:43:38.737253
19. player=None, moves=81, time=1:30, rows=4, cols=4, id=27, date=2018-01-08 06:38:50.871235
20. player=None, moves=90, time=1:33, rows=4, cols=4, id=28, date=2018-01-08 06:40:25.627050
21. player=None, moves=109, time=2:16, rows=4, cols=4, id=16, date=2018-01-08 06:28:46.705076
22. player=None, moves=112, time=1:36, rows=4, cols=4, id=29, date=2018-01-08 06:42:05.214436



'''
