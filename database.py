# https://techwithtim.net/tutorials/kivy-tutorial/example-gui/
# make user instead of name
# https://stackoverflow.com/questions/51029199/how-to-store-data-from-python-kivy-app
#https://kivy.org/doc/stable/api-kivy.storage.html
# work on drop down menus?
import datetime
import pandas as pd
import csv
import os.path
import glob
#------------------------------------------------
class note():
	def __init__(self, title, txt, created_date, updated_date, color):
		self.title = title
		self.txt = txt
		self.created_date = created_date
		self.updated_date = updated_date
		self.color = color

class user:
	def __init__(self,user):
		self.user = user
		self.notes = {}

# @staticmethod
def get_date():
	return str(datetime.datetime.now())
#------------------------------------------------
class DataFrame:
	def __init__(self, username):
		self.user = user(username)# its like a cart that we carry the user around in
		self.csvfilename = self.get_csv_file(username)
		self.file = None

	#note objects
	def load_notes(self):
		self.file = pd.read_csv(self.csvfilename)
		self.user.notes = self.file.set_index('title').to_dict()['txt']
		return self.user.notes

	# basically same as load note except no initial load
	# and save as a new note
	def add_new_note(self, note):
		title = note.title
		txt = note.txt
		created_date = note.created_date
		updated_date = note.created_date
		color = note.color

		with open(os.path.join('C:/Users/Josh/Python_Wizard/GitProj/Much_2-Do/user_notes', self.csvfilename), "a", newline="") as f:
			x = csv.writer(f, delimiter=',', quotechar = '|', quoting=csv.QUOTE_MINIMAL)
			x.writerow([title, txt, created_date, updated_date, color])

	def get_csv_file(self, username):
		path = "C:/Users/Josh/Python_Wizard/GitProj/Much_2-Do/user_notes/" + username + ".csv"
		isFile = os.path.isfile(path)
		if isFile:
			print("Path Exists and is Selected.")
			return path
		else:
			print("No Path Selected.")
	# have to organize data with created_date
	def open_note(self, updated_date):
		self.updated_date = updated_date
		df = pd.read_csv(self.csvfilename)
		x = len(load_notes())
		for i in df['updated_date']:
			if i == self.updated_date:
				for j in range(x)


			title = note.title
			txt = note.txt
			created_date = note.created_date
			updated_date = note.updated_date
			color = note.color

		with open(os.path.join('C:/Users/Josh/Python_Wizard/GitProj/Much_2-Do/user_notes', self.csvfilename), "w", newline="") as f:
			rows = csv.reader(f)
			for row in rows:
				# if row["title"] == self.title and row['txt'] == self.txt and row["created_date"] == self.created_date:
				if row["created_date"] == self.created_date:
					self.txt = row["txt"]
					created_date = row["created_date"]
					updated_date = row["created_date"]
					color = row["color"]

	def delete_note(self):
		pass

#------------------------------------------------
class authenicator:
	def __init__(self, txtfilename):
		self.txtfilename = txtfilename
		self.users = None
		self.file = None
		self.load()

	def load(self):
		self.file = open(self.txtfilename, "r")
		self.users = {}
		for line in self.file:
			try:
				username, email, passw, created = line.strip().split(";")
				self.users[username] = (email, passw, created)
			except:
				pass
		self.file.close()

	def get_user(self, username):
		if username in self.users:
			return self.users[username]
		else:
			return -1

	def add_user(self, email, username, passw):
		if username.strip() not in self.users:
			self.users[username.strip()] = (email.strip(), passw.strip(), str(get_date()))
			self.save()
			# load csv and add in user
			self.new_csv_file(username.strip())
			return 1
		else:
			print("Username exists already")
			return -1

	def new_csv_file(self, username):
		with open(os.path.join('C:/Users/Josh/Python_Wizard/GitProj/Much_2-Do/user_notes', username + ".csv"), "w", newline="") as f:
			x = csv.writer(f, delimiter=',', quotechar = '|', quoting=csv.QUOTE_MINIMAL)
			x.writerow(["title", "txt", "created_date", "updated_date", "color"])

	def validate(self, username, passw):
		if self.get_user(username) != -1:
			return self.users[username][1] == passw
		else:
			return False

	def save(self):
		with open(self.txtfilename, "w") as f:
			for i in self.users:
				f.write(i + ";" + self.users[i][0] + ";" + self.users[i][1] + ";" + self.users[i][2] + "\n")
