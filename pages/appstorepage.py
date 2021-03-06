import os, sys
import tkinter.filedialog
import tkinter as tk
import style as style
from appstore import Parser, Store_handler
from widgets import ThemedFrame, ThemedListbox, ThemedLabel, searchBox, activeFrame, scrolledText, button, categorylistFrame, installedcategorylistFrame
from github_updater import updater
from asyncthreader import threader
from .yesnopage import yesnoPage
from .settingspage import settingsPage
from .exitpage import exitPage
import config

sort_option_default = "Sort: Default"
sort_option_package_name_ascending = "Name A -> Z"
sort_option_package_name_descending = "Name Z -> A"
sort_option_package_title_ascending = "Title A -> Z"
sort_option_package_title_descending = "Title Z -> A"
sort_option_package_author_ascending = "Author (A->Z)"
sort_option_package_author_descending = "Author (Z->A)"
# sort_option_package_updated_ascending = "Updated (Recent first)"
# sort_option_package_updated_descending = "Updated (Recent last)"

SORT_OPTIONS = [
	sort_option_default,
	sort_option_package_name_ascending,
	sort_option_package_name_descending,
	sort_option_package_title_ascending,
	sort_option_package_title_descending,
	sort_option_package_author_ascending,
	sort_option_package_author_descending,
	# sort_option_package_updated_ascending,
	# sort_option_package_updated_descending
]

SORT_MAP = {
	sort_option_default : None,
	sort_option_package_name_ascending : "name",
	sort_option_package_name_descending : "name-",
	sort_option_package_title_ascending : "title",
	sort_option_package_title_descending : "title-",
	sort_option_package_author_ascending : "author",
	sort_option_package_author_descending : "author-",
	# sort_option_package_updated_ascending : "updated",
	# sort_option_package_updated_descending : "updated-"
}

class appstorePage(activeFrame):
	def __init__(self, parent, controller):
		self.controller = controller
		self.appstore_handler = Store_handler
		self.repo_parser = Parser
		self.current_frame = None
		self.current_frame_name = None
		self.last_selection = None
		self.last_sort_option = None
		self.updater = updater
		activeFrame.__init__(self,parent,controller)

		self.column = ThemedFrame(self, background = style.color_1)
		self.column.place(relx = 0, rely = 0, width = style.sidecolumnwidth, relheight = 1)

		self.column_header = ThemedFrame(self.column, background = style.color_1)
		self.column_header.place(relx = 0, rely = 0, relwidth = 1, height = style.column_headerheight)

		self.column_header_title = ThemedLabel(self.column_header,"Appstore\nWorkbench\nGPLv3",anchor="center",font=style.largeboldtext, background = style.color_1)
		self.column_header_title.place(relx = 0,rely = 0, relwidth = 1, relheight = 1, height = - (style.offset + 1), y = + style.offset)

		self.column_header_separator = ThemedLabel(self.column_header, "", background=style.w)
		self.column_header_separator.place(x = style.offset, rely = 1, y = - 1, relwidth = 1, width = -2 * style.offset)

		self.column_body = ThemedFrame(self.column, background = style.color_1)
		self.column_body.place(relx = 0, relwidth = 1, y = style.column_headerheight, relheight = 1, height = - (style.column_headerheight + style.footerheight))

		self.category_listbox = ThemedListbox(self.column_body, foreground = style.w)
		self.category_listbox.configure(activestyle = "none")
		self.category_listbox.place(relwidth=1,relheight=1)
		self.category_listbox.bind('<<ListboxSelect>>',self.select_frame)

		self.column_footer = ThemedFrame(self.column, background = style.color_1)
		self.column_footer.place(relx = 0, rely = 1, relwidth = 1, height = 2 * style.listbox_footer_height, y = - 2 * style.listbox_footer_height)

		self.column_set_sd = button(self.column_footer, 
			callback = self.set_sd, 
			text_string = "Select SD Root", 
			font=style.mediumtext, 
			background=style.color_2
			).place(relwidth = 1, y = 0, x = style.offset, width = - 2 * style.offset, height = style.listbox_footer_height)

		self.column_sd_status_label = ThemedLabel(self.column_footer,"SD - Not Set",anchor="center",font=style.smalltext, background = style.color_1, foreground= style.pathdisplaytextcolor)
		self.column_sd_status_label.place(x = style.offset, relwidth = 1, width = - 2 * style.offset, y = -style.listbox_footer_height, height = style.listbox_footer_height, rely=1,  )

		self.content_frame = ThemedFrame(self)
		self.content_frame.place(x = style.sidecolumnwidth, width = -style.sidecolumnwidth, rely = 0, relheight = 1, relwidth = 1)

		self.content_frame_header = ThemedFrame(self.content_frame)
		self.content_frame_header.place(relx = 0, rely = 0, relwidth = 1, height = style.searchboxheight)

		self.category_label = ThemedLabel(self.content_frame_header,"",anchor="nw",font=style.giantboldtext, background = style.color_1, foreground=style.lg)
		self.category_label.place(x = + style.offset, relx = 0,rely = 0, relheight = 1, height = - (style.offset + 1), y = + style.offset)

		self.content_frame_header_search_bar = searchBox(self.content_frame_header, command = self.search, entry_background=style.color_2, borderwidth = 0, entry_foreground = style.w)

		self.selected_sort_method = tk.StringVar()
		self.selected_sort_method.set(SORT_OPTIONS[0])
		self.content_frame_header_sort_method_dropdown = tk.OptionMenu(self.content_frame_header,self.selected_sort_method,*SORT_OPTIONS)
		self.content_frame_header_sort_method_dropdown.configure(foreground = style.w)
		self.content_frame_header_sort_method_dropdown.configure(background = style.color_2)
		self.content_frame_header_sort_method_dropdown.configure(highlightthickness = 0)
		self.content_frame_header_sort_method_dropdown.configure(borderwidth = 0)
		
		#The various content gets stacked on top of each other here.
		self.content_stacking_frame = ThemedFrame(self.content_frame)
		self.content_stacking_frame.place(relx = 0, y=(style.searchboxheight + style.offset), relwidth = 1, relheight = 1, height=-(style.searchboxheight + style.offset))

		all_frame = categorylistFrame(self.content_stacking_frame, self.controller, self, self.repo_parser.all)
		tools_frame = categorylistFrame(self.content_stacking_frame, self.controller, self, self.repo_parser.tools)
		
		emus_frame = categorylistFrame(self.content_stacking_frame, self.controller, self, self.repo_parser.emus)
		games_frame = categorylistFrame(self.content_stacking_frame, self.controller, self, self.repo_parser.games)
		installed_frame = installedcategorylistFrame(self.content_stacking_frame, self.controller, self, self.repo_parser.all)
		# help_frame = helpFrame(self.content_stacking_frame)
		# about_frame = aboutFrame(self.content_stacking_frame)
		# readme_frame = readmeFrame(self.content_stacking_frame)
		settings_frame = settingsPage(self.content_stacking_frame, self.controller)
		exit_frame = exitPage(self.content_stacking_frame, self.controller)

		self.category_frames = [all_frame,tools_frame,emus_frame,games_frame,installed_frame]

		self.frames = [
			{
			"frame" : all_frame,
			"text" : "All Apps"
			},
			{
			"frame" : tools_frame,
			"text" : "Tools"
			},
			
			{
			"frame" : emus_frame,
			"text" : "Emulators"
			},
			{
			"frame" : games_frame,
			"text" : "Games"
			},
		]

		if config.CONSOLE in [config.WII, config.WII_OSC]:
			misc_frame = categorylistFrame(self.content_stacking_frame, self.controller, self, self.repo_parser.misc)
			self.category_frames.append(misc_frame)
			self.frames.extend(
				[
					{
					"frame" : misc_frame,
					"text" : "Misc"
					},
				]
			)
		elif config.CONSOLE == config.SWITCH:
			legacy_frame = categorylistFrame(self.content_stacking_frame, self.controller, self, self.repo_parser.legacy)
			themes_frame = categorylistFrame(self.content_stacking_frame, self.controller, self, self.repo_parser.themes)
			advanced_frame = categorylistFrame(self.content_stacking_frame, self.controller, self, self.repo_parser.advanced)
			self.category_frames.append(legacy_frame)
			self.category_frames.append(themes_frame)
			self.category_frames.append(advanced_frame)
			self.frames.extend(
				[
					{
					"frame" : advanced_frame,
					"text" : "Advanced Homebrew"
					},
					{
					"frame" : themes_frame,
					"text" : "Themes"
					},
					{
					"frame" : legacy_frame,
					"text" : "Legacy"
					},
					
				]
			)
		elif config.CONSOLE == config.WIIU:
			misc_frame = categorylistFrame(self.content_stacking_frame, self.controller, self, self.repo_parser.misc)
			advanced_frame = categorylistFrame(self.content_stacking_frame, self.controller, self, self.repo_parser.advanced)
			self.category_frames.append(misc_frame)
			self.category_frames.append(advanced_frame)
			self.frames.extend(
				[
					{
					"frame" : advanced_frame,
					"text" : "Advanced Homebrew"
					},
					{
					"frame" : misc_frame,
					"text" : "Misc"
					},
					
				]
			)
		else:
			raise "Invalid Console"

		self.frames.extend(
			[
				{
				"frame" : installed_frame,
				"text" : "Installed"
				},
				# {
				# "frame" : help_frame,
				# "text" : "HELP"
				# },
				# {
				# "frame" : about_frame,
				# "text" : "ABOUT"
				# },
				# {
				# "frame" : readme_frame,
				# "text" : "README",
				# },
				{
				"frame" : settings_frame,
				"text" : "SETTINGS"
				},
				{
				"frame" : exit_frame,
				"text" : "EXIT"
				}
			]
		)

		self.all_frames = []
		self.content_frames = {}

		def make_frames_and_add_to_list(frame_list, listbox):
			for f in frame_list:
				page_name = f["text"]
				frame = f["frame"]
				self.content_frames[page_name] = frame
				frame.place(relx = 0, rely = 0, relwidth = 1, relheight = 1)
				listbox.insert("end", " {}".format(page_name))
				self.all_frames.append(f)

		threader.do_async(lambda: make_frames_and_add_to_list(self.frames, self.category_listbox))

		self.category_listbox.select_set(0) #sets focus on the first item in listbox
		self.category_listbox.event_generate("<<ListboxSelect>>")

		self.show_frame("All Apps")

		if self.updater.status:
			print(self.updater.status)
			self.yesnoPage = yesnoPage(self)
			self.yesnoPage.getanswer("An update is available, would you like to download it?\nPatch notes:\n{}".format(self.updater.status), self.updater.update)

		self.loaded()
		self.add_on_refresh_callback(self.update_sd_path)
		self.add_on_tick_callback(self.update_sd_path)
		self.sort_check_loop()

	def show_frame(self, page_name):
		#Show a frame for the given page name
		frame = self.content_frames[page_name]
		frame.event_generate("<<ShowFrame>>")
		frame.tkraise()
		self.category_label.set(page_name)
		self.controller.after(100, self.update_search_bar_position)

		for frm in self.category_frames:
			frm.deselect()
		if frame in self.category_frames:
			frame.select()
		self.current_frame = frame
		self.current_frame_name = page_name

	def update_search_bar_position(self):
		if not self.current_frame in self.category_frames:
			self.content_frame_header_search_bar.place_forget()
			self.content_frame_header_sort_method_dropdown.place_forget()
		else:
			category_label_offset = self.category_label.winfo_width()
			#If the category label has been populated, otherwise the offset is usually just a few pixels (prevents an ugly draw on launch)
			if category_label_offset > style.offset:
				self.content_frame_header_sort_method_dropdown.place(relx = 1, x = -(style.offset + style.sortdropdownwidth), width = style.sortdropdownwidth, y=+ 1.5 * style.offset, relheight =1, height = - 2 *style.offset)
				self.content_frame_header_search_bar.place(x = + 1.5 * style.offset + category_label_offset, y=+ 1.5 * style.offset, relheight =1, relwidth = 1, width = - (category_label_offset + 3.5 * style.offset + style.sortdropdownwidth), height = - 2 *style.offset)
			else:
				self.content_frame_header_search_bar.place_forget()
				self.controller.after(100, self.update_search_bar_position)

	def select_frame(self, event):
		try:
			widget = event.widget
			selection = widget.curselection()
			picked = widget.get(selection[0])
			if not picked == self.last_selection:
				frame = None
				for f in self.all_frames:
					t = f["text"]
					if t.strip() == picked.strip():
						self.show_frame(t)
						break
				self.last_selection = picked
		except Exception as e:
			# print(e)
			pass

	def search(self, searchterm):
		self.current_frame.search(searchterm)

	def reload_category_frames(self):
		print("Reloading frames")
		for frame in self.category_frames:
			frame.configure(None)

	def set_sd(self):
		chosensdpath = tkinter.filedialog.askdirectory(initialdir="/",  title='Please select your SD card')
		self.appstore_handler.set_path(chosensdpath)
		self.reload_category_frames()
		self.update_sd_path()

	def update_sd_path(self):
		chosensdpath = self.appstore_handler.check_path()
		if chosensdpath:
			#Get the basename
			basepath = os.path.basename(os.path.normpath(chosensdpath))
			#If we didn't find it, assume it's a root dir and just return the whole path
			if not basepath:
				basepath = chosensdpath
		else:
			basepath = "Not Set"
		self.column_sd_status_label.set("SD - {}".format(basepath))

	def update_sort(self):
		for frame in self.category_frames:
			frame.set_sort_type(SORT_MAP[self.selected_sort_method.get()])
			frame.rebuild()

	#loop to check if the sorting methog has been applied yet
	def sort_check_loop(self):
		if not self.last_sort_option == self.selected_sort_method.get():
			self.last_sort_option = self.selected_sort_method.get()
			self.update_sort()

		#schedule self
		self.schedule_callback(self.sort_check_loop, 100)

class textFrame(ThemedFrame):
	def __init__(self,frame):
		ThemedFrame.__init__(self, frame, background = style.color_2)
		self.text = scrolledText(self, wrap = 'word', font = style.mediumtext, background = style.color_2, foreground = style.w, borderwidth = 0, highlightthickness = 0)
		self.text.place(relwidth=1, relheight =1)

	def set(self, text):
		self.text.insert("1.0", text)
		self.text.configure(state="disabled")

#Super basic about frame, pulls from about.txt
class aboutFrame(textFrame):
	def __init__(self,frame):
		textFrame.__init__(self, frame)
		with open("about.txt") as aboutfile:
			self.set(aboutfile.read())

#Super basic readme frame, pulls from readme.md
class readmeFrame(textFrame):
	def __init__(self,frame):
		textFrame.__init__(self, frame)
		with open('readme.md') as readme:
			self.set(readme.read())

#Super basic readme frame, pulls from help.txt
class helpFrame(textFrame):
	def __init__(self,frame):
		textFrame.__init__(self, frame)
		with open("help.txt") as text:
			self.set(text.read())