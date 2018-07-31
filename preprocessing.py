import csv
import numpy as np

def read_csv_rows(path):
	destination=[]
	with open(path, 'rt') as f:
		reader = csv.reader(f)
		for row in reader:
			destination.append(row)
	return destination

def remove_elements(string, elements = [':','(',')','"','+','[',']',',','-','.','/','&','!','?','*', '–', '‘', '…']):
	for i in elements:
		string = string.replace(i, ' ')
	while (string.find('  ') != -1):
		string = string.replace('  ', ' ')
	return string

def oneHotOf(inp, height, width):
	arr = np.zeros((height, width))
	for i, v in enumerate(inp):
		if type(v) != list:
			arr[i][v] = 1
		else:
			for ii in v:
				arr[i][ii] = 1
	return arr

def oneHotOfBin(inp, height, width):
	arr = np.zeros((height, width))
	for i, v in enumerate(inp):
		b = [i for i in bin(v)[2:]]
		b=b.reverse()
		for ii, vv in enumerate(b):
			if vv == 1:
				arr[i][ii] = 1
			else:
				arr[i][ii] = 0
	return arr


	

items_raw = read_csv_rows('items.csv')[1:]
shops_raw = read_csv_rows('shops.csv')[1:]
item_categories_raw = read_csv_rows('item_categories.csv')[1:]

train_raw = read_csv_rows('sales_train_v2.csv')[1:]
test_raw = read_csv_rows('test.csv')[1:]



# Items
# getting rid of [':','(',')','"','+','[',']',',','-','.','/','&','!','?','*']
buff = []
for i, v in enumerate(items_raw):
	buff.append(remove_elements(v[0]).lower().strip())


dictionary = []
for i in buff:
	for ii in i.split(' '):
		if ii.lower() not in dictionary:
			dictionary.append(ii)


encoded_strings = []
for i in buff:
	row = []
	for ii in i.lower().split(' '):
		row.append(dictionary.index(ii))
	encoded_strings.append(row)


for i, v in enumerate(items_raw):
	items_raw[i] = items_raw[i][1:]
	items_raw[i][1] = int(items_raw[i][1])
	items_raw[i][0] = encoded_strings[i]


# Train
prices=[0 for i in range(len(items_raw))]
for i in train_raw:
	if float(i[4]) > prices[int(i[3])]:
		prices[int(i[3])] = float(i[4])

for i, v in enumerate(train_raw):
	train_raw[i][1] = int(train_raw[i][1])
	train_raw[i][2] = int(train_raw[i][2])
	train_raw[i][3] = int(train_raw[i][3])
	train_raw[i][4] = float(train_raw[i][4])
	train_raw[i][5] = int(float(train_raw[i][5]))


train = {}

train['date'] = [i[0] for i in train_raw]
train['block_date'] = [i[1] for i in train_raw]
train['shop_id'] = oneHotOf([i[2] for i in train_raw], len(train_raw), len(shops_raw))
items_buffer_ids = [i[3] for i in train_raw]
# train['words'] = oneHotOf([items_raw[i][0] for i in items_buffer_ids], len(train_raw), len(dictionary))
train['category'] = oneHotOf([items_raw[i][1] for i in items_buffer_ids], len(train_raw), len(item_categories_raw))

train['price'] = [(i[4]/prices[i[3]]) for i in train_raw]
train['price'] = [(i[4]/prices[i[3]]) for i in train_raw]
train['count_day'] = oneHotOfBin([i[5] for i in train_raw], len(train_raw), len(str(bin(2169))[2:]))

