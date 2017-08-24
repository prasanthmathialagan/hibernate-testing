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

'''
<votes>
	<row Id="9048" PostId="2680" VoteTypeId="8" UserId="203" CreationDate="2015-05-04T00:00:00.000" BountyAmount="150" />
</votes>
'''
def import_votes(file):
	sql="INSERT INTO Votes (`id`, `postId`, `voteTypeId`, `createdDate`, `userId`, `bountyAmount`) VALUES (%s, %s, %s, %s, %s, %s)"
	print "Importing Votes from " + file
	votes = tree.parse(file).getroot()
	total=len(votes)
	count=0;
	con=get_connection();
	cursor=con.cursor()
	for row in votes:
		userId=row.attrib.get("UserId", None)
		bountyAmount=row.attrib.get("BountyAmount", None)
		rdata=(int(row.attrib['Id']), int(row.attrib['PostId']), int(row.attrib['VoteTypeId']), row.attrib['CreationDate'], userId, bountyAmount)
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
<postlinks>
	<row Id="327" CreationDate="2015-01-24T03:20:43.000" PostId="185" RelatedPostId="199" LinkTypeId="1" />
</postlinks>
'''
def import_postlinks(file):
	sql="INSERT INTO PostLinks (`id`, `createdDate`, `postId`, `relatedPostId`, `linkTypeId`) VALUES (%s, %s, %s, %s, %s)"
	print "Importing PostLinks from " + file
	postlinks = tree.parse(file).getroot()
	total=len(postlinks)
	count=0;
	con=get_connection();
	cursor=con.cursor()
	for row in postlinks:
		rdata=(int(row.attrib['Id']), row.attrib['CreationDate'], int(row.attrib['PostId']), int(row.attrib['RelatedPostId']), int(row.attrib['LinkTypeId']))
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

'''
<users>
	<row Id="-1" Reputation="1" CreationDate="2015-01-20T16:45:52.530" DisplayName="Community" LastAccessDate="2015-01-20T16:45:52.530"
	Location="on the server farm" AboutMe="&lt;p&gt;Hi, I'm not really a person.&lt;/p&gt;&#xD;&#xA;&lt;p&gt;I'm a background process that helps keep this site clean!&lt;/p&gt;&#xD;&#xA;&lt;p&gt;I do things like&lt;/p&gt;&#xD;&#xA;&lt;ul&gt;&#xD;&#xA;&lt;li&gt;Randomly poke old unanswered questions every hour so they get some attention&lt;/li&gt;&#xD;&#xA;&lt;li&gt;Own community questions and answers so nobody gets unnecessary reputation from them&lt;/li&gt;&#xD;&#xA;&lt;li&gt;Own downvotes on spam/evil posts that get permanently deleted&lt;/li&gt;&#xD;&#xA;&lt;li&gt;Own suggested edits from anonymous users&lt;/li&gt;&#xD;&#xA;&lt;li&gt;&lt;a href=&quot;http://meta.stackoverflow.com/a/92006&quot;&gt;Remove abandoned questions&lt;/a&gt;&lt;/li&gt;&#xD;&#xA;&lt;/ul&gt;"
	Views="0" UpVotes="504" DownVotes="809" Age="2" AccountId="-1" />
</users>
'''
def import_users(file):
	sql="INSERT INTO Users (`id`, `reputation`, `createdDate`, `displayName`, `lastAccessDate`, `location`, `aboutMe`, `profileImageUrl`, `websiteUrl`, `age`, `views`, `accountId`, `upvotes`, `downvotes`) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
	print "Importing Users from " + file
	users = tree.parse(file).getroot()
	total=len(users)
	count=0;
	con=get_connection();
	cursor=con.cursor()
	for row in users:
		location=row.attrib.get("Location", None)
		profileImageUrl=row.attrib.get("ProfileImageUrl", None)
		websiteUrl=row.attrib.get("WebsiteUrl", None)
		age=row.attrib.get("Age", None)
		accountId=row.attrib.get("AccountId", None)
		aboutMe=row.attrib.get("AboutMe", None)
		rdata=(int(row.attrib['Id']), int(row.attrib['Reputation']), row.attrib['CreationDate'], row.attrib['DisplayName'], row.attrib['LastAccessDate'], location, aboutMe, profileImageUrl, websiteUrl, age, int(row.attrib['Views']), accountId, int(row.attrib['UpVotes']), int(row.attrib['DownVotes']))
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
import_votes(data_dir+"/Votes.xml")
import_postlinks(data_dir+"/PostLinks.xml")
import_users(data_dir+"/Users.xml")