#python packages
import pickle
import os
import time
import kivy
import datetime
from database import authenicator, DataFrame, note, user, get_date

#kivy packages
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.widget import Widget
from kivy.uix.image import Image
from kivy.uix.popup import Popup
from kivy.uix.screenmanager import ScreenManager, Screen, ShaderTransition
from kivy.uix.recycleview import RecycleView
from kivy.uix.scrollview import ScrollView
from kivy.uix.recycleview.views import RecycleDataViewBehavior
from kivy.uix.label import Label
from kivy.properties import BooleanProperty, NumericProperty, StringProperty, ObjectProperty
from kivy.animation import Animation
from kivy.uix.recycleboxlayout import RecycleBoxLayout
from kivy.uix.recyclegridlayout import RecycleGridLayout
from kivy.uix.behaviors import FocusBehavior
from kivy.uix.recycleview.layout import LayoutSelectionBehavior
from kivy.uix.behaviors.button import ButtonBehavior
from kivy.vector import Vector
from kivy.uix.floatlayout import FloatLayout
from kivy.clock import Clock
from kivy.core.window import Window


new_note_instance_name = None


# Error Popup page
# global methods
def error1():
	pop_up = Popup(title = "Error 1", content=Label(text="Invalid Username or Password"), size_hint=(None, None), size=(400,400))
	pop_up.open()

def error2():
	pop_up = Popup(title = "Error 2", content=Label(text="Please input valid information for all inputs."), size_hint=(None, None), size=(400,400))
	pop_up.open()

def NoteName():
	pop_up = Popup(title = "Give your note a name.", content=TextInput(), id=(NoteName), size_hint=(None, None), size=(400,400))
	pop_up.open()


# Buttons
class Notes_Buttons(Button):
	pass
# Screens
#>>>>>>> ADD FADE TRANSITION IF POSSIBLE<<<<<<
class FirstScreen(Screen):
	def thing(self, dt):
		self.manager.current = "SuSi"

class SignuporSignin(Screen):
    pass

class SignUpScreen(Screen):
	email = ObjectProperty(None)
	username = ObjectProperty(None)
	passw = ObjectProperty(None)
	#wnat to send email
	def newusersubmit(self):
		if self.ids["username"].text != "" and self.ids["email"].text != "" and self.ids["email"].text.count("@") == 1 and self.email.text.count(".") > 0:
			if self.ids["passw"].text != "":
				db.add_user(self.ids["email"].text, self.ids["username"].text, self.ids["passw"].text)

				self.reset()
				sm.current = "signin"
			else:
				self.reset()
				error2()
		else:
			self.reset()
			error2()

	def back(self):
		self.reset()
		sm.current = "signin"

	def reset(self):
		self.email.text = ""
		self.username.text = ""
		self.password.text = ""

class SignInScreen(Screen):
	username = ObjectProperty(None)
	passw = ObjectProperty(None)

	def verify_credentials(self):
		if db.validate(self.ids["username"].text, self.ids["passw"].text):
			MainPage.current = self.ids["username"].text
			NewNote.current = self.ids["username"].text
			self.reset()
			sm.current = "main"
		else:
			self.reset()
			error1()

	def reset(self):
		self.ids["username"].text = ""
		self.ids["passw"].text = ""

class MainPage(Screen):
	view = ObjectProperty(None)
	# View = ObjectProperty(None)

	email = ObjectProperty(None)
	created = ObjectProperty(None)
	username = ObjectProperty(None)
	current = ""
	# def __init__(self, **kw):
	scrollview = ObjectProperty(None)
	gridlayout = ObjectProperty(None)


	def logOut(self):
		sm.current = "SuSi"

	def on_enter(self, *args):
		username, password, created = db.get_user(self.current)
		self.username.text = "Username: " + self.current
		x = self.load_df_notes()
		# view = ObjectProperty(None)
		self.gridlayout = self.buttonlist(x)
		self.scrollview = ScrollView(size_hint=(1, None), size=(Window.width, Window.height))
		self.addscrollview(self.gridlayout, self.scrollview)

	def on_leave(self, *args):
		pass

	def rem_widgets(self, parent, child):
		print("Removing Widgets...")
		parent.remove_widget(child)


	def buttonlist(self, base):
		layout = GridLayout(cols=1, spacing=5, size_hint_y=None)
		layout.bind(minimum_height=layout.setter("height"))
		for element in base:
			layout.add_widget(Notes_Buttons(text=element))
		return layout

	def addscrollview(self, child, parent):
		view = ObjectProperty(None)
		parent.add_widget(child)
		self.view.add_widget(parent)


	def load_df_notes(self):
		df = DataFrame(self.current)
		if len(df.load_notes()) != 0:
			base = []
			for i in df.load_notes():
				base.append("{}".format(i))
		else:
			base = ["You dont have any notes. Create one using the 'Plus' Button."]
		return base


	def select(self, title):

		sm.current = "Exist"

	def new(self):
		self.rem_widgets(self.view, self.scrollview)
		sm.current = "new"

class NewNote(Screen):
	df = ObjectProperty(None)
	current = ""
	# user = self.current

	def on_enter(self, *args):
		df = self.loadDF(self.current)

	def save(self):
		# df = DataFrame(self.current)
		created_date = get_date()
		color = "None"
		print(self.ids["title"].text, self.ids["txt"].text)
		x = note(self.ids["title"].text, self.ids["txt"].text, created_date, created_date, color)
		self.df.add_new_note(x)
		view = ObjectProperty(None)
		self.reset()
		sm.current = "main"

	def loadDF(self, file):
		self.df = DataFrame(file)

	def reset(self):
		self.ids["title"].text = ""
		self.ids["txt"].text = ""

	def back(self):
		self.reset()
		sm.current = "main"

class ExistingNote(Screen):
	def on_enter(self, *args):
		df = DataFrame(self.current)
		df.open_note(self.current)

class WindowManager(ScreenManager):
	pass

Builder.load_file("Much_2-Do.kv")
db = authenicator("users.txt")


sm = WindowManager()
screens = [FirstScreen(name='first'), SignuporSignin(name="SuSi"), SignInScreen(name='signin'), SignUpScreen(name="signup"), MainPage(name="main"), NewNote(name="new"), ExistingNote(name="exist")]#, Circle(name="circle")]#, ErrorPage(name='error')]

for each in screens:
	sm.add_widget(each)
sm.current = 'first'

class MyApp(App):
	title = 'Much 2-Do'
	def build(self):
		return sm
if __name__ == "__main__":
    MyApp().run()
