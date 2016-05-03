import os
import csv

"""
format data for clustering
"""

results_dir = '../../results'

MINIMUM_POSTS = 100 #minimum to save a category


def write_rows(filename, rows):
	if len(rows) < MINIMUM_POSTS:
		return

	print 'Saving ' + str(len(rows)) + ' rows to ' + filename
	with open(filename, 'w') as out_file:
		csv_writer = csv.writer(out_file)
		for p in rows:
			csv_writer.writerow(p)

def by_city():
	for city in os.listdir(results_dir):
		d_path = os.path.join(results_dir, city)
		if os.path.isdir(d_path):
			city_posts = []
			for f in os.listdir(d_path):
				if f.endswith('.csv'): 
					with open(os.path.join(d_path, f),'r') as in_file:
						next(in_file) # skip column labels
						csv_reader = csv.reader(in_file)
						for line in csv_reader:
							city = line[1]
							title = line[7]
							text = line[8] + title + title # DOUBLE WEIGHT WORDS IN TITLE
							category = line[5]
							posttype = line[6]
							city_posts.append([text, city, category, posttype]) #text

			write_rows('data/city/' + city + '.csv', city_posts)

def by_field(dirname, column_number):
	rows_by_field = {}
	for city in os.listdir(results_dir):
		d_path = os.path.join(results_dir, city)
		if os.path.isdir(d_path):
			posts = []
			for f in os.listdir(d_path):
				if f.endswith('.csv'): 
					with open(os.path.join(d_path, f),'r') as in_file:
						next(in_file) # skip column labels
						csv_reader = csv.reader(in_file)
						for line in csv_reader:
							city = line[1]
							title = line[7]
							text = line[8] + title + title # DOUBLE WEIGHT WORDS IN TITLE
							category = line[5]
							posttype = line[6]
							# split based on value of the column we're concerned with
							value = line[column_number]
							if not value:
								value = 'none'
							if value not in rows_by_field:
								rows_by_field[value] = []
							rows_by_field[value].append([text, city, category, posttype]) #text

	for value in rows_by_field:
		write_rows('data/' + dirname + '/' + value + '.csv', rows_by_field[value])

def by_category_and_type():
	rows_by_field = {}
	for city in os.listdir(results_dir):
		d_path = os.path.join(results_dir, city)
		if os.path.isdir(d_path):
			posts = []
			for f in os.listdir(d_path):
				if f.endswith('.csv'): 
					with open(os.path.join(d_path, f),'r') as in_file:
						next(in_file) # skip column labels
						csv_reader = csv.reader(in_file)
						for line in csv_reader:
							city = line[1]
							title = line[7]
							text = line[8] + title + title # DOUBLE WEIGHT WORDS IN TITLE
							category = line[5]
							posttype = line[6]
							v1 = category
							v2 = posttype
							if not v1:
								v1 = 'none'
							if not v2:
								v2 = 'none'

							value = v1 + '_' + v2
							if value not in rows_by_field:
								rows_by_field[value] = []
							rows_by_field[value].append([text, city, category, posttype]) #text

	for value in rows_by_field:
		write_rows('data/category_type/' + value + '.csv', rows_by_field[value])

"""
split up all posts into those posted by males (for anyone) and those posted by females (for anyone)
* this excludes posts coming from two people (ie mw4m, mm4m, etc)
* this includes both platonic and romantic postss

"""
def by_gender():
	male = []
	female = []
	for city in os.listdir(results_dir):
		d_path = os.path.join(results_dir, city)
		if os.path.isdir(d_path):
			posts = []
			for f in os.listdir(d_path):
				if f.endswith('.csv'): 
					with open(os.path.join(d_path, f),'r') as in_file:
						next(in_file) # skip column labels
						csv_reader = csv.reader(in_file)
						for line in csv_reader:
							city = line[1]
							title = line[7]
							text = line[8] + title + title # DOUBLE WEIGHT WORDS IN TITLE
							category = line[5]
							posttype = line[6]
							# split on male and female posters
							if posttype.startswith('m4'):
								male.append([text, city, category, posttype])
							elif posttype.startswith('w4'):
								female.append([text, city, category, posttype])

	write_rows('data/gender/male.csv', male)
	write_rows('data/gender/female.csv', female)

def main():
	#by_city()
	#by_field('type', 6)
	#by_gender()
	by_category_and_type()

if __name__ == '__main__':
	main()
