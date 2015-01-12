#! /usr/bin/env python
# coding: UTF-8

import httplib
import urllib
import time
import socket
import re
import sys

_all__=["getCsdnPageObj"]




def iniRequest(host,method,url,body=None,headers={}):
	con=httplib.HTTPConnection(host)
	try:
		con.request(method,url,body,headers)
		req_object=con.getresponse()
	except httplib.HTTPException as ex:
		print 'error in iniRequest:',ex,req_object.status,req_object.reason
		raise
	except socket.gaierror as e:
		print 'error in iniRequest:',e
		raise
	return req_object
	
def printHeaders(req_object):
	print 'status:', req_object.status
	print 'version:',req_object.version
	print 'reason:',req_object.reason
	print "req_object heads:",req_object.getheaders()
	print 'msg:',req_object.msg
	print 'gethead set-cookies:',req_object.getheader('set-Cookie')
	#print '\n\nread:',req_object.read()
	
	
def splitHostUrl(url):
	pattern=re.compile(r'\s*(http://)?(.*?)(/.*)')
	m=pattern.match(url)
	#print m.group(2,3)
	return m.group(2,3)
	
def getCsdnPageObj(where):
	count=0
	while(count<5):
		count+=1
		host,url=splitHostUrl(where)		
		csdn_headers={ 'Host':host,
			'User-Agent':'Mozilla/5.0 (Windows NT 6.1; rv:34.0) Gecko/20100101 Firefox/34.0',
			'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
			'Accept-Language':'zh-cn,zh;q=0.8,en-us;q=0.5,en;q=0.3',
#			'Accept-Encoding':'gzip, deflate',
#			'Connection':'keep-alive'
		}
		req_obj=iniRequest(host,'GET',url,headers=csdn_headers)
		if host=="huiyi.csdn.net":
			is_news_page=False
		else:
			is_news_page=True
			
		if(httplib.OK==req_obj.status):
			break
		elif(httplib.FOUND==req_obj.status):
			where=req_obj.getheader('Location')
#			print '*****need redirction***************'
			warn_msg='Warning!!!Redirction to: '+where+"\n"
			sys.stderr.write(warn_msg)
			req_obj.close()
		else:
			print 'error:',req_obj.status
			printHeaders(req_obj)
			raise
			
		req_obj.close()
	return is_news_page,req_obj
	
if __name__=='__main__':
	#url=raw_input(u'Please input url:')
	url='www.csdn.net/'
	is_news_page,obj=getCsdnPageObj(url)
	printHeaders(obj)
#	file_name=_url+'['+time.strftime('%Y-%m-%d--%H-%M-%S',time.localtime(time.time()))+']'+'.html'
	file_name='['+time.strftime('%Y-%m-%d--%H-%M-%S',time.localtime(time.time()))+']'+'.html'
	print file_name
	file=open(file_name,'w')
	file.write(obj.read());
	file.close()
	
