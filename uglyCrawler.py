#! /usr/bin/env python
#coding:utf-8

from csdnPage import getCsdnPageObj
from csdnMainPageParser import getCsdnHeadlines
from csdnNewsExtract import getCsdnNewsInfo
from csdnActivityExtract import getCsdnActivityInfo
from writeToDatabase import *

_url='www.csdn.net/'

main_page=getCsdnPageObj(_url)[1].read()
headlines= getCsdnHeadlines(main_page)
records=[]
count=0
for title in headlines:
	count+=1;
	try:
		is_news_page,req_obj= getCsdnPageObj(headlines[title])
		page_obj= req_obj.read()
	except Exception,ex:
		print "Get ",title,"error"
		print Exception,":",ex  
		continue
	if is_news_page:
		news_info=getCsdnNewsInfo(page_obj)
		news_info['title']=title
		news_info['url']=headlines[title]
		news_info['page']=page_obj;
#		print "detail:"
#		for item in news_info:
#			if item=='title':
#				print count,item+":",	news_info[item]	#repr(item)
#		print "********************************************************************"
		records.append(news_info)
	else:
		activity_info=getCsdnActivityInfo(page_obj)
	
connect_arg={'user':'root','passwd':"wu",'host':'localhost','port':3306}
db=NewsStore(connect_arg)
db.write(records)
db.finish()


		
		
