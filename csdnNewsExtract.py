#! /usr/bin/env python
# coding: UTF-8
'''
该模块主要功能：网页中提取出，作者、摘要、评论数、阅读次数、来源、发表时间等信息；
通过调用getCsdnNewsInfo，接受一个response body，返回一个dict，键值分别为：author、
summary、num_recom,view_time,from，pub_time
'''
import sgmllib
from csdnMainPageParser import listToDict

__all__=["getCsdnNewsInfo"]

def getViewTime():
	'''获取阅读次数，还不会解析js :( !!'''
	return "0"
def getNumRecomment():
	'''获取评论次数，还不会解析js :( !!'''
	return "0"
	
class csdnNewsExtracter(sgmllib.SGMLParser):
	def __init__(self):
		sgmllib.SGMLParser.__init__(self)
		self.is_tit_bar=False
		self.is_view_time=False
		self.is_num_recom=False
		self.is_tag=False
		self.is_summary=False
		self.contents={}
		self.tit_bar=""
		self.count_tit_bar=0
		
	def start_div(self,attrs):
		attrs_dict=listToDict(attrs)
		if attrs_dict.get("class")!=None and attrs_dict["class"]=="tit_bar":
			self.is_tit_bar=True
		elif attrs_dict.get("class")!=None and attrs_dict["class"]=="tag":
			self.is_tag=True
		elif attrs_dict.get("class")!=None and attrs_dict["class"]=="summary":
			self.is_summary=True
			
	def end_div(self):
		if self.is_tit_bar:
			self.is_tit_bar=False
		elif self.is_tag:
			self.is_tag=False
		elif self.is_summary:
			self.is_summary=False
	
	
	def start_input(self,attrs):
		if self.is_summary:
			attrs_dict=listToDict(attrs)
			self.contents["summary"]=attrs_dict['value']
	
	
	def start_span(self,attrs):
		if self.is_tit_bar:
			attrs_dict=listToDict(attrs)
			if attrs_dict.get("class")!=None and attrs_dict["class"]=="view_time":
				self.is_view_time=True
			elif attrs_dict.get("class")!=None and attrs_dict["class"]=="num_recom":
				self.is_num_recom=True
			
	def end_span(self):
		if self.is_view_time:
			self.is_view_time=False
		elif self.is_num_recom:
			self.is_num_recom=False
			
			
	def handle_data(self,text):
		if self.is_view_time:
			self.contents["view_time"]=getViewTime()#
		elif self.is_num_recom:
			self.contents["num_recom"]=getNumRecomment()#
		elif self.is_tit_bar:
			text=text.replace("|","").strip().replace("\n"," ").replace("\t","")
			if text:
				#print self.count_tit_bar,":",text
				self.count_tit_bar +=1
				if self.count_tit_bar%2==0:
					if self.tit_bar=="作者":
						self.contents["author"]=text
					elif self.tit_bar=="发表于":
#						print text
						self.contents["pub_time"]=text
					elif self.tit_bar=="来源":
						self.contents["from"]=text
				else:
					self.tit_bar=text
		elif self.is_tag:
			if self.contents.get('tag')!=None:
				self.contents["tag"]=self.contents["tag"]+" "+text
			else:
				self.contents["tag"]=text;

def getCsdnNewsInfo(page):
	info=csdnNewsExtracter()
	info.feed(page)
	#ret=copy.copy(info.contents)	
	return info.contents


if __name__=='__main__':
	#import urllib2
	#news = urllib2.urlopen('http://www.csdn.net/article/2015-01-08/2823483').read()
	from csdnPage import getCsdnPageObj
	news=getCsdnPageObj('http://www.csdn.net/article/2015-01-08/2823483').read()
	ret=getCsdnNewsInfo(news)
	for item in ret:
		print item+":",	ret[item]	#repr(item)