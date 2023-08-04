import mariadb

try:
	conn = mariadb.connect(
		user='cite',
		password='elegant_baker',
		host='127.0.0.1',
		port=3306,
		database='cite'
	)
except mariadb.Error as e:
	print(f'Error connecting to mariadb: {e}')

cur = conn.cursor()

cur.execute('select * from ctrl')

for (key, value) in cur:
	print(f'Key: {key}, Value: {value}')


cur.close()
conn.close()
