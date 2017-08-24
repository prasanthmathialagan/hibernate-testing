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
	print "Importing from " + file
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
try:
	data_dir=sys.argv[1]
	print "Data directory is " + data_dir
except:
	print "Not enough arguments. Usage: import_data.py <data directory>"
	sys.exit(2)

load_properties("default.properties")

import_badges(data_dir+"/Badges.xml")