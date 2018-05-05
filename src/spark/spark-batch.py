import sys

# import pyspark

from pyspark import SparkContext

from pyspark import SparkConf

from pyspark.sql import SparkSession

from pyspark.sql.types import StringType, DoubleType, IntegerType

from pyspark.sql.functions import udf

import json

import random

# import cassandra spark connector(datastax)

from cassandra.cluster import Cluster

from cassandra.query import BatchStatement

from cassandra import ConsistencyLevel

import config



def sendCassandra(iter):

    print("send to cassandra")
    cluster = Cluster(config.CASSANDRA_SERVER)
    session = cluster.connect(config.CASSANDRA_NAMESPACE)

    insert_statement = session.prepare("INSERT INTO data (userid, newsid, count) VALUES (?, ?, ?)")

    count = 0

    # batch insert into cassandra database
    batch = BatchStatement(consistency_level=ConsistencyLevel.QUORUM)
    
    for record in iter:
        batch.add(insert_statement, (record['userid'], record['newsid'], record['count']))


        # split the batch, so that the batch will not exceed the size limit
        count += 1
        if count % 500 == 0:
            session.execute(batch)
            batch = BatchStatement(consistency_level=ConsistencyLevel.QUORUM)

    # send the batch that is less than 500            
    session.execute(batch)
    session.shutdown()




if __name__ == "__main__":

	category_dict = {'COP':'Politics', 'GOV':'Politics','INS':'WAR','JUD':'Social','MIL':'WAR','OPP':'Politics','REB':'WAR','SEP':'WAR','SPY':'Social','UAF':'WAR','AGR':'Agriculture',\
				'BUS':'Business', 'CRM': 'Social', 'CVL': 'Social', 'DEV':'Technology','EDU':'Education', 'ELI':'Social', 'ENV':'Environment', 'HLH':'Health', 'HRI':'Social','LAB':'Social',\
				'LEG':'Politics', 'MED':'Media', 'REF':'Social', 'MOD': 'Sports', 'RAD':'Politics', 'AMN':'Sports', 'IRC':'Social', 'GRP':'Sports', 'UNO': 'Social','PKO':'Sports', 'UIS':'Other',\
				'IGO':'Sports','IMG':'International', 'INT': 'International', 'MNC': 'International', 'NGM': 'International', 'NGO':'International', 'UIS':'Other', 'SET': 'Sports'}
	def normalize_category(genre):
		
		if genre:
			modified_genre = category_dict[genre]
		else:
			modified_genre = genre
		
		return modified_genre

	# Set Spark context
	sc = SparkContext(appName="Gdelt-Analytics")
	# Set Spark session
    	sqlContext = SparkSession(sc)
	
	# Read news data from S3
	gdelt_bucket = "s3a://gdelt-open-data/v2/events/20180410190000.export.csv"

	lines = sc.textFile(gdelt_bucket)

	# Split lines into columns by delimiter '\t'
	parts = lines.map(lambda l: l.split("\t"))

	# Convert Rdd into DataFrame
	from urllib import urlopen

	html = urlopen("http://gdeltproject.org/data/lookups/CSV.header.dailyupdates.txt").read().rstrip()

	columns = html.split("\t")

 
	df = sqlContext.createDataFrame(parts,columns)

	df_news = df.select('GLOBALEVENTID','SQLDATE','Actor1Type1Code', 'NumMentions')

	cateudf = udf(lambda z: normalize_category(z), StringType())

	df_temp = df_news.select('GLOBALEVENTID','SQLDATE','Actor1Type1Code', 'NumMentions',\
				cateudf('Actor1Type1Code').alias('category'))

	df_filtered = df_temp.select('GLOBALEVENTID','SQLDATE','category', 'NumMentions')

	
	
	user_bucket = "s3a://userclicklogs/click_log.txt"
	# Read user clicklogs from S3
	click_logs = sc.textFile(user_bucket)
	
	# Split lines into columns by delimiter '\t'
	record = click_logs.map(lambda x: x.split("\t"))

	# Convert Rdd into DataFram
	df_click = sqlContext.createDataFrame(record,['userid','GLOBALEVENTID'])

	df_join = df_click.join(df_filtered, on='GLOBALEVENTID')

	df_grouped = df_join.groupby(['userid', 'category']).count()

	df_grouped.write.format("org.apache.spark.sql.cassandra").options(
  	table='demo1', keyspace='playground').save()
