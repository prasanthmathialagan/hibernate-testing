import mysql.connector
import sys
import ConfigParser
import xml.etree.ElementTree as tree

db_user=""
db_password=""
db_host=""
db_database=""

data_dir=""

def load_properties(file):
	global db_user, db_password, db_host, db_database
	config = ConfigParser.RawConfigParser()
	config.read(file)
	db_user = config.get("DatabaseSection", "mysqldb.user")
	db_password = config.get("DatabaseSection", "mysqldb.password")
	db_host = config.get("DatabaseSection", "mysqldb.host")
	db_database = config.get("DatabaseSection", "mysqldb.database")
	print "Database=" + db_database + ", host=" + db_host + ", user=" + db_user

def get_connection():
	global db_user, db_password, db_host, db_database
	conn = mysql.connector.connect(user=db_user, password=db_password, host=db_host, database=db_database)
	return conn

'''
<badges>
  <row Id="1" UserId="21" Name="Autobiographer" Date="2015-01-20T19:04:45.823" Class="3" TagBased="False" />
  <row Id="2" UserId="2" Name="Precognitive" Date="2015-01-20T19:04:45.807" Class="3" TagBased="False" />
</badges>
'''
def import_badges(file):
	sql="INSERT INTO Badges (`id`, `userId`, `name`, `date`, `class`, `tagBased`) VALUES (%s, %s, %s, %s, %s, %s)"
	print "Importing Badges from " + file
	badges = tree.parse(file).getroot()
	total=len(badges)
	count=0;
	con=get_connection();
	cursor=con.cursor()
	for row in badges:
		rdata=(int(row.attrib['Id']), int(row.attrib['UserId']), row.attrib['Name'], row.attrib['Date'], int(row.attrib['Class']), bool(row.attrib['TagBased']))
		cursor.execute(sql, rdata)
		count=count+1
		if count % 100 == 0:
			con.commit()
			print "Processed " + str(count) + "/" + str(total)

	con.commit()
	print "Processed " + str(count) + "/" + str(total)
	cursor.close()
	con.close()

'''
<comments>
	<row Id="1" PostId="2" Score="0" Text="They can do this so simply as if it were a liquid?" CreationDate="2015-01-20T18:44:48.173" UserId="9" />
</comments>
'''
def import_comments(file):
	sql="INSERT INTO Comments (`id`, `postId`, `score`, `text`, `createdDate`, `userId`) VALUES (%s, %s, %s, %s, %s, %s)"
	print "Importing Comments from " + file
	comments = tree.parse(file).getroot()
	total=len(comments)
	count=0;
	con=get_connection();
	cursor=con.cursor()
	for row in comments:
		userId=row.attrib.get("UserId", None)
		rdata=(int(row.attrib['Id']), int(row.attrib['PostId']), int(row.attrib['Score']), row.attrib['Text'], row.attrib['CreationDate'], userId)
		cursor.execute(sql, rdata)
		count=count+1
		if count % 100 == 0:
			con.commit()
			print "Processed " + str(count) + "/" + str(total)

	con.commit()
	print "Processed " + str(count) + "/" + str(total)
	cursor.close()
	con.close()

'''
<tags>
	<row Id="1" TagName="liquid" Count="7" ExcerptPostId="130" WikiPostId="129" />
</tags>
'''
def import_tags(file):
	sql="INSERT INTO Tags (`id`, `name`, `count`, `excerptPostId`, `wikiPostId`) VALUES (%s, %s, %s, %s, %s)"
	print "Importing Tags from " + file
	tags = tree.parse(file).getroot()
	total=len(tags)
	count=0;
	con=get_connection();
	cursor=con.cursor()
	for row in tags:
		excerptPostId=row.attrib.get("ExcerptPostId", None)
		wikiPostId=row.attrib.get("WikiPostId", None)
		rdata=(int(row.attrib['Id']), row.attrib['TagName'], int(row.attrib['Count']), excerptPostId, wikiPostId)
		cursor.execute(sql, rdata)
		count=count+1
		if count % 100 == 0:
			con.commit()
			print "Processed " + str(count) + "/" + str(total)

	con.commit()
	print "Processed " + str(count) + "/" + str(total)
	cursor.close()
	con.close()

try:
	data_dir=sys.argv[1]
	print "Data directory is " + data_dir
except:
	print "Not enough arguments. Usage: import_data.py <data directory>"
	sys.exit(2)

load_properties("default.properties")

import_badges(data_dir+"/Badges.xml")
import_comments(data_dir+"/Comments.xml")
import_tags(data_dir+"/Tags.xml")