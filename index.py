import csv
import os
from pprint import pprint
import mysql.connector

name = raw_input("Enter CSV name > ")
dbname = raw_input("Enter database name > ")
cnx = mysql.connector.connect(user='root', password='root', database=dbname, host='localhost')

def csv_to_list(csv_file):
	f = open(csv_file)
	reader = csv.reader(f)
	data_list = list(csv.reader(f))
	return data_list

def exec_sql(statement):
	cur = cnx.cursor()
	stat = statement
	cur.execute(stat)
	cnx.commit()
	print(stat)

dataset = csv_to_list("../data/" + name + ".csv")

columns = "("
columns_2 = "("

j = 1

data_len = len(dataset[j])

for i in dataset[0]:
	columns = columns + i
	columns_2 = columns_2 + i
	if j < data_len:
		columns = columns + " varchar(1000), "
		columns_2 = columns_2 + ", "
	j = j + 1

columns = columns + " varchar(1000))"
columns_2 = columns_2 + ")"

exec_sql("CREATE TABLE IF NOT EXISTS " + name + " " + columns + " CHARACTER SET utf8;")
exec_sql("TRUNCATE TABLE " + name + ";")

dataset.pop(0)

for i in dataset:
	k = 0
	values = "('"
	while k < data_len:
		delim = "'"
		if k < data_len - 1:
			delim = "', '"
		values = values + i[k] + delim
		k = k + 1
	values = values + ")"
	exec_sql("INSERT INTO " + name + " " + columns_2 + " VALUES " + values + ";")