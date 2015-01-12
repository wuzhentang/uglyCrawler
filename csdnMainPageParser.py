#! /usr/bin/env python
# coding: UTF-8

import sgmllib 

__all__=["listToDict","getCsdnHeadlines"]

def listToDict(list):
	dict={}
	for item in list:
		dict[item[0]]= item[1]
	return dict
	
	
class CsdnMainPageParser(sgmllib.SGMLParser):
	def __init__(self):
		sgmllib.SGMLParser.__init__(self)
		self.is_a=False
		self.is_news_left=False
		self.is_news_list=False
		self.is_news_left_dl=False
		self.is_news_list_ul=False
		self.is_nav=0  #0:before nav; 1:in nav; 2:after nav
		self.headlines={}
#		self.name=[]
		
	def start_div(self,attrs):
		if  self.is_nav==1:
			#print "In nav"
			attrs_dict=listToDict(attrs)
			if attrs_dict.get("class")!=None and attrs_dict["class"]=="news_left":
				self.is_news_left=True
			elif attrs_dict.get("class")!=None and attrs_dict["class"]=="news_list":
				self.is_news_list=True
				
	def end_div(self):
		if self.is_news_left==True:
			self.is_news_left=False
		if self.is_news_list==True:
			self.is_news_list=False;
		
		
	def start_dl(self,attrs):
		if self.is_news_left:
			self.is_news_left_dl=True
	def end_dl(self):
		if self.is_news_left_dl:
			self.is_news_left_dl=False
			
			
	def start_ul(self,attrs):
		if self.is_news_list:
			self.is_news_list_ul=True
			
	def end_ul(self):
		if self.is_news_list_ul:
			self.is_news_list_ul=False
			
			
	def start_a(self,attrs):
		self.is_a=True
		if self.is_news_left_dl or self.is_news_list_ul:
			target = listToDict(attrs)
			#print target['title'],target['href']
			self.headlines[target['title']]=target['href']
			#print self.headlines
		
	def end_a(self):
		self.is_a=False
		
		
	def handle_comment(self,comment):
		if 'nav'==comment :
			self.is_nav=1
		elif 'nav'!=comment and self.is_nav==1:
			self.is_nav=2
			
			
#	def handle_data(self,text):	
#		if self.is_nav==1 and (self.is_news_left_dl or self.is_news_list_ul) and self.is_a==True:
#			self.name.append(text)


def getCsdnHeadlines(main_page):
	pobj=CsdnMainPageParser()
	pobj.feed(main_page)
	return pobj.headlines

		
if __name__=='__main__':
	import urllib2
	main_page = urllib2.urlopen('http://www.csdn.net').read()
	
	headlines= getCsdnHeadlines(main_page)
	for title in headlines:
		print title,headlines[title]
		
	

