#! /usr/bin/env python
#coding=utf-8

import MySQLdb
import sys
import warnings
import time
import datetime
import re
__all__=["NewsStore"]

reload(sys)
sys.setdefaultencoding('utf-8') 
warnings.filterwarnings("ignore", "Table 'news_list' already exists")

def _AdjustPubTime(pub_time):
	pattern2=re.compile(r'(\d+)小时前')
	m=pattern2.match(pub_time)
	if m:
		h=m.group(1)
		pub_time=datetime.datetime.now()-datetime.timedelta(hours=int(h)) 
#	print pub_time
	return pub_time
	
def _formatInsertData(list):
	scratch_time=time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
	records=[]
	for item in list:
		row=[]
		row.append(item['title'])
		row.append(item['author'])
		row.append(item['num_recom'])
		row.append(item['view_time'])
		row.append(_AdjustPubTime(item['pub_time']))
		row.append(scratch_time)
		row.append(item['url'])
		row.append(item['from'])
		row.append(item['summary'])
		row.append(item['page'])
		records.append(row)
	return records

class NewsStore():
	conn=None
	cur=None
	_database_name='csdn_headlines'
	_table_name='news_list'
	_charset='utf8'
	def __init__(self,args):
		self._connect(args)
		try:
			self._createDatabaseIfNeed()
			self.conn.select_db(self._database_name)
			self.cur=self.conn.cursor()
			self._createTableIfNeed()
		except MySQLdb.Error,e:
			print "Mysql Error %d: %s" % (e.args[0], e.args[1])
	def _connect(self,args):
		self.conn= MySQLdb.connect(\
				host=args['host'],
				port = args['port'],
				user=args['user'],
				passwd=args['passwd'],
#		    	db ='csdn_headlines',
				charset=self._charset,
			)
	def _createDatabaseIfNeed(self):
		'''we create csdn_headlines database if not exists	
		'''
		query_sql='SELECT EXISTS(SELECT 1 FROM INFORMATION_SCHEMA.SCHEMATA \
			WHERE SCHEMA_NAME = %s) AS e'
		cur = self.conn.cursor()
		cur.execute(query_sql,(self._database_name,))
		is_exists=cur.fetchone()[0]
		if not is_exists:
			create_database_sql="CREATE DATABASE IF NOT EXISTS "+self._database_name+\
			" default character set "+self._charset+" COLLATE utf8_general_ci"
			cur.execute(create_database_sql)
		
	def _createTableIfNeed(self):
		create_news_list_sql="CREATE TABLE IF NOT EXISTS "+self._table_name+"(\
					title varchar(50),\
					author varchar(30),\
					num_recom int,\
					view_time int,\
					pub_time datetime,\
					scratch_time datetime,\
					url varchar(200),\
					`from` varchar(50),\
					summary text,\
					page MEDIUMTEXT,\
					PRIMARY KEY(title,author)\
					) ENGINE=InnoDB DEFAULT CHARSET="+self._charset
#		cur.execute(create_news_list_sql,[_table_name,_charset])
		self.cur.execute(create_news_list_sql)	
	def write(self,records_list):
#		args=dictToList(data_dict)
		records=_formatInsertData(records_list)
		insert_sql='REPLACE INTO news_list(title,author,num_recom,view_time,\
					pub_time,scratch_time,url,`from`,summary,page) \
					values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'
		self.cur.executemany(insert_sql,records)

		
	def finish(self):
		self.cur.close()
		self.conn.commit()
		self.conn.close()

		

	
		
		
		
if __name__=="__main__":
	connect_arg={'user':'root','passwd':"wu",'host':'localhost','port':3306}
	try:
		data_instance=NewsStore(connect_arg)
		
		example_data=[{'title':"title1",'author':"wu",'view_time':0,
						'num_recom':0,'pub_time':"2015-01-08 18:31",
						'url':"www.example1.com",'from':"wu",
						'summary':"this is example1!",'page':"aaaaaaa"},
						{'title':"title2",'author':"wu",'view_time':1,
						'num_recom':1,'pub_time':"2015-01-08 18:32",
						'url':"www.example2.com",'from':"wu",
						'summary':"this is example2!",'page':"bbbbbbb"}
				]
		data_instance.write(example_data)
		data_instance.finish()
	except MySQLdb.Error,e:
		print "Mysql Error %d: %s" % (e.args[0], e.args[1])
	 
	 