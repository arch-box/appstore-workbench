import os
import tkinter as tk
from tkinter.constants import *
from widgets import button, ThemedLabel
import style
from .yesnopage import yesnoPage
from .usermessagepage import usermessagePage
from settings_tool import settings
import config

class customOptionMenu(tk.OptionMenu):
	def __init__(self, frame, opts):
		option = tk.StringVar()
		tk.OptionMenu.__init__(self, frame, option, *opts)
		self.configure(foreground = style.w)
		self.configure(background = style.color_1)
		self.configure(highlightthickness = 0)
		self.configure(borderwidth = 0)
		self.option = option
		self.option.set(opts[0])

truefalse_options = [ "true", "false"]

dropdown_width = 400
label_width = 200

class settingsPage(tk.Frame):
	def __init__(self, parent, controller):
		tk.Frame.__init__(self,parent,background=style.color_2)
		self.settings = settings
		self.controller = controller

		self.settings_page_header = ThemedLabel(self, text = "Most settings will not take effect until next launch", background = style.color_2, font = style.mediumboldtext)
		self.settings_page_header.place(y = style.offset, x = style.offset, height = style.buttonsize - 2 * style.offset, relwidth = 1, width = - 2 * style.offset)

		consoles = [config.WII, config.WII_OSC, config.WIIU, config.SWITCH]
		self.console_dropdown = customOptionMenu(self, consoles)
		self.console_dropdown.place(y = 1 * (style.offset + style.buttonsize), x = style.offset, height = style.buttonsize - 2 * style.offset, width = dropdown_width - style.offset)
		self.console_dropdown_label = ThemedLabel(self, text = "~ Console - Repo\n(Needs restart)", background = style.color_2)
		self.console_dropdown_label.place(y = 1 * (style.offset + style.buttonsize), x = dropdown_width + style.offset, height = style.buttonsize - 2 * style.offset, width = label_width)
		
		thread_levels = [x for x in range(1,17)]
		self.gui_threads_dropdown = customOptionMenu(self, thread_levels)
		self.gui_threads_dropdown.place(y = 2 * (style.offset + style.buttonsize), x = style.offset, height = style.buttonsize - 2 * style.offset, width = dropdown_width - style.offset)
		self.gui_threads_dropdown_label = ThemedLabel(self, text = "~ Max threads\n(No restart)", background = style.color_2)
		self.gui_threads_dropdown_label.place(y = 2 * (style.offset + style.buttonsize), x = dropdown_width + style.offset, height = style.buttonsize - 2 * style.offset, width = label_width)

		maximized_options = [ "fullscreen", "maximized", "windowed"]
		self.maximized_on_launch_dropdown = customOptionMenu(self, maximized_options)
		self.maximized_on_launch_dropdown.place(y = 3 * (style.offset + style.buttonsize), x = style.offset, height = style.buttonsize - 2 * style.offset, width = dropdown_width - style.offset)
		self.maximized_dropdown_label = ThemedLabel(self, text = "~ Maximized on launch", background = style.color_2)
		self.maximized_dropdown_label.place(y = 3 * (style.offset + style.buttonsize), x = dropdown_width + style.offset, height = style.buttonsize - 2 * style.offset, width = label_width)

		self.topmost_dropdown = customOptionMenu(self, truefalse_options)
		self.topmost_dropdown.place(y = 4 * (style.offset + style.buttonsize), x = style.offset, height = style.buttonsize - 2 * style.offset, width = dropdown_width - style.offset)
		self.topmost_dropdown_label = ThemedLabel(self, text = "~ Keep window topmost", background = style.color_2)
		self.topmost_dropdown_label.place(y = 4 * (style.offset + style.buttonsize), x = dropdown_width + style.offset, height = style.buttonsize - 2 * style.offset, width = label_width)

		self.borderless_dropdown = customOptionMenu(self, truefalse_options)
		self.borderless_dropdown.place(y = 5 * (style.offset + style.buttonsize), x = style.offset, height = style.buttonsize - 2 * style.offset, width = dropdown_width - style.offset)
		self.borderless_dropdown_label = ThemedLabel(self, text = "~ Borderless window\n(broken on some systems)", background = style.color_2)
		self.borderless_dropdown_label.place(y = 5 * (style.offset + style.buttonsize), x = dropdown_width + style.offset, height = style.buttonsize - 2 * style.offset, width = label_width)

		self.savebutton = button(self, callback=self.save,text_string="Save",background=style.color_1)
		self.savebutton.place(relx=0.5, x = - 0.5 * style.sidecolumnwidth, width = style.sidecolumnwidth, height = style.buttonsize, rely = 1, y = - (style.offset + style.buttonsize))
		#Bind frame raise
		self.bind("<<ShowFrame>>", self.configure)
		self.yesno = yesnoPage(self)
		self.okpage = usermessagePage(self)

	def configure(self, event):
		self.console_dropdown.option.set(self.settings.get_setting("console"))
		self.maximized_on_launch_dropdown.option.set(self.settings.get_setting("maximized"))
		self.topmost_dropdown.option.set(self.settings.get_setting("keep_topmost"))
		self.borderless_dropdown.option.set(self.settings.get_setting("borderless"))
		self.gui_threads_dropdown.option.set(self.settings.get_setting("gui_threads"))

	def save(self):
		try:
			self.settings.set_setting("console", self.console_dropdown.option.get())
			self.settings.set_setting("maximized", self.maximized_on_launch_dropdown.option.get())
			self.settings.set_setting("keep_topmost", self.topmost_dropdown.option.get())
			self.settings.set_setting("borderless", self.borderless_dropdown.option.get())
			self.settings.set_setting("gui_threads", self.gui_threads_dropdown.option.get())
			self.settings.save()
			self.okpage.telluser("Settings saved successfully")
		except Exception as e:
			self.okpage.telluser("Failed to save settings\n{}".format(e))