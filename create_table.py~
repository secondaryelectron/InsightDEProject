from cassandra.cluster import Cluster
import config

cluster = Cluster(config.CASSANDRA_SERVER)
session = cluster.connect()

session.execute('DROP KEYSPACE IF EXISTS '+config.CASSANDRA_NAMESPACE+ ';')

session.execute('CREATE KEYSPACE ' + config.CASSANDRA_NAMESPACE  + ' WITH replication = {\'class\': \'SimpleStrategy\', \'replication_factor\' : 3};')
session.execute('USE ' + config.CASSANDRA_NAMESPACE)

session.execute('DROP TABLE IF EXISTS summary;')
session.execute('CREATE TABLE summary (userid text, category text, count bigint, PRIMARY KEY (userid,count)) WITH CLUSTERING ORDER BY (count DESC);')

session.execute('DROP TABLE IF EXISTS news;')
session.execute('CREATE TABLE news (newsid text, date int, category text, mentions int, sourceurl text, PRIMARY KEY ((category),date,mentions)) WITH CLUSTERING ORDER BY (date DESC,mentions DESC);')
