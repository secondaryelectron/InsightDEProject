from cassandra.cluster import Cluster
import config

cluster = Cluster(config.CASSANDRA_SERVER)
session = cluster.connect()

session.execute('USE ' + config.CASSANDRA_NAMESPACE)

session.execute('DROP TABLE IF EXISTS news;')
session.execute('CREATE TABLE news (newsid text, date int, category text, mentions int, PRIMARY KEY ((newsid,category),date)) WITH CLUSTERING ORDER BY (date DESC);')
