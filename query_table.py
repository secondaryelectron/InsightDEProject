from cassandra.cluster import Cluster

cluster = Cluster(config.CASSANDRA_SERVER)
session = cluster.connect()

session.execute("USE " + config.CASSANDRA_NAMESPACE)

rows = session.execute('SELECT * FROM demo1 WHERE userid=\'1000\'')

print rows
