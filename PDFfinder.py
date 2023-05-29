'''
do zrobienia pisane 27.05.2023:

7. stworzenie 4 fukcji exportujacej do pliku z oone wyboru gdzie zapisac wyniki ostateczne z nr5:
            csv ,
            html ,
            excel ,
8.Podlinkowanie przyciskow z menu do 4 funcji
+++++++++++++++++++++++++9.Stworzenie funkicji do nowego szukania
10.Zajecie sie problemamy pozosyalych elementow menu
11.Refactoring
12. Kontorla przez K. Lemka

'''
# from pathlib import Path

import os
import pdfplumber
import pyperclip
import fnmatch

from math import floor
from tkinter import ttk, filedialog
import tkinter as tkk

from gui.menubar import Menubar


class Gui(tkk.Tk):

    def __init__(self):
        super().__init__()

        self.search = ''

        self.scaleW_value = tkk.IntVar(value=20)
        self.scaleW_value.trace_add('write', self.refresh_frame_yellow)

        self.entry_searchVar = tkk.StringVar(self)
        self.entry_searchVar.trace_add('write', self.entry_not_empty)

        self.widgets_results = []

        width_of_window = 1200
        height_of_window = 700

        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        x_coordinate = (screen_width / 2) - (width_of_window / 2)
        y_coordinate = (screen_height / 2) - (height_of_window / 2)
        self.geometry("%dx%d+%d+%d" % (width_of_window, height_of_window, x_coordinate, y_coordinate))

        self.menubar = Menubar(self)
        self._create_green_frame()
        self._create_purpure_frame()

        self.frame_black = ttk.Frame(self)
        self.frame_yellow = ttk.Frame(self)

        self._save_selected__add_file_names()
        self.no_results_found()

    def new_search(self, *args):
        self.full_list_reserch_patch_files = []
        self.widgets_results = []
        self.uppercaseVar.set("0")
        self.entry_searchVar.set("")
        self.checkbuttonFrame_purpureVar.set("0")
        self.Var_save_selected.set(0)
        self.button_folder.state((['!disabled']))
        self.button_folder.state((['!disabled']))
        self.frame__save_selected__add_file_names.forget()
        self.frame_yellow.forget()
        self.frame_black.forget()
        self.frame_no_results_found.forget()
        self.advanced.state((['disabled']))
        self.save_all_purpure_Frame.state(['disabled'])
        self.entry_search.state((['disabled']))
        self.button_search.state(['disabled'])
        self.ignore_case.state(['disabled'])

    def entry_not_empty(self, *args):
        if len(self.entry_searchVar.get()) > 2:
            self.button_search.state(['!disabled'])
        else:
            self.button_search.state(['disabled'])

    def save_file(self, listen, mark=0):
        self.full_txt = ''

        if mark == 0:
            for i in listen:
                file_name = i[-1].split("/")[-1]  # wyodrebnia nazwe pliku kazdego wyszukania
                for j in i[0:-1]:
                    j.append(file_name)
                    temp2 = ''
                    for n in j:
                        temp2 += n + ';'
                    self.full_txt += (temp2[0:-1] + "\n")
        else:
            pass
        file = filedialog.asksaveasfile(
            defaultextension='.txt',
            filetypes=[
                ("Text file", ".txt"),
                ("CSV file", ".csv"),
                ("HTML file", ".html"),
                ("All files", ".*"),
            ])

        if file is None:
            return

###############  html code generator

###HTML
        if file.name.split('.')[-1] == 'html':
            print('TEST: is html')
            ##### insert the code to generate the tables in html here

        file.write(self.full_txt)
        file.close()

    def function_save_selected(self, listen):
        self.list_selection = []
        for results in self.widgets_results:
            for _dict in results:
                try:
                    if _dict['checkbox_str'].get() == "on":
                        selection_index = _dict['checkbox_field_no'].get()
                        self.list_selection.append(selection_index)
                except ValueError:
                    selection_index = -1
                    self.list_selection.append(selection_index)
        self.select_reserch_patch_files = []

        self.full_txt = ''

        for plik in self.full_list_reserch_patch_files:

            file_name = plik[-1].split("/")[-1]

            for results in plik[0:-1]:
                temp_list = []

                for inx in self.list_selection:
                    temp_list.append(results[inx])

                if self.Var_save_selected.get() == 1:
                    temp_list.append(file_name)

                temp2 = ''

                for n in temp_list:
                    temp2 += n + ';'

                self.full_txt += (temp2[0:-1] + "\n")

        file = filedialog.asksaveasfile(
            defaultextension='.txt',
            filetypes=[
                ("Text file", ".txt"),
                ("CSV file", ".csv"),
                ("HTML file", ".html"),
                ("All files", ".*"),
            ])
        if file is None:
            return

        ###############  html code generator

        ###HTML
        if file.name.split('.')[-1] == 'html':
            print('is html')
            ##### insert the code to generate the tables in html here

        file.write(self.full_txt)
        file.close()

    def _scrollbar(self):
        self.main_frame = tkk.Frame(self)
        self.main_frame.pack(fill=tkk.BOTH, expand=1)

        self.main_canvas = tkk.Canvas(self.main_frame)
        self.main_canvas.pack(side=tkk.LEFT, fill=tkk.BOTH, expand=1)

        self.main_scrollbar = ttk.Scrollbar(self.main_frame, orient=tkk.VERTICAL, command=self.main_canvas.yview)
        self.main_scrollbar.pack(side=tkk.RIGHT, fill=tkk.Y)

        self.main_canvas.configure(yscrollcommand=self.main_scrollbar.set)

        self.main_canvas.bind('<Configure>',
                              lambda e: self.main_canvas.configure(scrollregion=self.main_canvas.bbox("all")))

        self.top_frame = tkk.Frame(self.main_canvas)

        self.main_canvas.create_window((0, 0), window=self.top_frame, anchor="nw")

    def pyperclip_function(self):
        return pyperclip.copy('borysgolebiowskipl@gmail.com')

    def open_folder(self):
        self.open_action = filedialog.askdirectory()
        if self.open_action:

            self.entry_search.state((['!disabled']))
            self.ignore_case.state(['!disabled'])

    def open_file(self):
        self.open_action = filedialog.askopenfilenames(
            title="Open PDF File",
            filetypes=(
                ("PDF Files", "*.pdf"),
                ("All Files", "*.*")))

        if self.open_action:
            self.entry_search.state((['!disabled']))
            self.ignore_case.state(['!disabled'])

    def create_text_in_entries(self, full_list_reserch_patch_files):

        if len(self.full_list_reserch_patch_files[0][0]) > 1 and isinstance(self.full_list_reserch_patch_files[0][0], list):
            self.frame_no_results_found.forget()
            self._create__yellow_frame(full_list_reserch_patch_files)
            self.advanced.state((['!disabled']))
            self.save_all_purpure_Frame.state(['!disabled'])
            self.entry_search.state((['disabled']))
            self.button_search.state(['disabled'])
            self.ignore_case.state(['disabled'])
            self.button_folder.state(['disabled'])
            self.button_files.state(['disabled'])

        else:
            self.frame_no_results_found.pack()

        return full_list_reserch_patch_files

    def combo(self, files):
        self.full_list_reserch_patch_files = []

        if not type(files) is tuple:
            self.open_action = tuple()
            for path, dirs, filess in os.walk(files):

                for file in filess:
                    if fnmatch.fnmatch(file, '*.pdf'):
                        full_path = path + '/' + file
                        self.open_action += (full_path,)
            return self.combo(self.open_action)

        else:
            for file in files:
                list_search_result_file = self.engine_search(self.pdf2txt(file))
                list_search_result_file.append(file)
                self.full_list_reserch_patch_files.append(list_search_result_file)
        print('------>return self.full_list_reserch_patch_files', self.full_list_reserch_patch_files)
        return self.full_list_reserch_patch_files

    def pdf2txt(self, fill_patch_pdf_file):
        with pdfplumber.open(fill_patch_pdf_file) as pdf:
            full_txt_from_pdf_file = ''
            total_pages = len(pdf.pages)
            for i in range(0, total_pages):
                page_obj = pdf.pages[i]
                full_txt_from_pdf_file += page_obj.extract_text() + '\n'
        return full_txt_from_pdf_file

    def engine_search(self, full_txt_from_pdf):
        search_phrase = self.entry_search.get()
        len_search_phrase = len(search_phrase.split())
        # temp_list3 -a list of lists of occurrences of the word followed by occurrences of one file
        temp_list3 = []

        full_txt_from_pdf__split = full_txt_from_pdf.split()

        print('search phrase find as: ', search_phrase)

        for idx, elem in enumerate(full_txt_from_pdf__split):
            lista_temp = []
            text_join = " ".join(full_txt_from_pdf__split[
                                idx:idx + len_search_phrase])

            if self.uppercaseVar.get() == "1":
                has_phrase_found = search_phrase.lower() == text_join.lower()
            else:
                has_phrase_found = search_phrase == text_join

            if has_phrase_found:
                lista_temp.append(text_join)
                for i in range(idx + len_search_phrase,
                               # hard 19 words after we found it
                               idx + len_search_phrase + 19):
                    try:

                        lista_temp.append(full_txt_from_pdf__split[i])
                    except:
                        pass
                temp_list3.append(lista_temp)

        return temp_list3

    def _create_green_frame(self):

        self.frame_green = ttk.Frame(self)
        self.frame_green.config(height=100, width=400, )  # relief=tkk.SUNKEN,

        ttk.Label(self.frame_green, text='Wybierz pliki/pliki lub folder do przeszukania', font=('Arial', 12)).grid(
            row=0,
            column=0,
            pady=20,
            padx=100,
            sticky='sw')

        self.button_folder = ttk.Button(self.frame_green, text="Folder", command=self.open_folder)
        self.button_folder.grid(row=1, column=0, padx=10, pady=0, sticky='sw')

        self.button_files = ttk.Button(self.frame_green, text="Plik", command=self.open_file)
        self.button_files.grid(row=1, column=0, padx=10, pady=0, sticky='se')

        self.entry_search = ttk.Entry(self.frame_green, textvariable=self.entry_searchVar, width=45,
                                      font=('Arial', 10))
        self.entry_search.grid(row=4, column=0, padx=10, pady=0, columnspan=2, sticky='swe')
        self.entry_search.state((['disabled']))

        self.uppercaseVar = tkk.StringVar(value='0')
        self.ignore_case = ttk.Checkbutton(self.frame_green, text='ingoruj wielkosc liter?')  # kwadrat do zaznaczenia
        self.ignore_case.grid(row=3, column=0, padx=10, pady=0, columnspan=2, sticky='swe')
        self.ignore_case.config(variable=self.uppercaseVar, onvalue="1",
                                offvalue="0")
        self.ignore_case.state(['disabled'])

        link5 = ttk.Label(self.frame_green, text='Wpisz fraze szukana', font=('Arial', 8))
        link5.grid(row=5, column=0, pady=0, padx=100, columnspan=2)
        self.wyniki = lambda: self.create_text_in_entries(self.combo(self.open_action))
        self.button_search = ttk.Button(self.frame_green, text="Szukaj",
                                        command=self.wyniki)
        self.button_search.grid(row=6, column=0, padx=10, pady=20, sticky='sw')
        self.button_search.state(['disabled'])
        self.frame_green.pack()

    def _create_purpure_frame(self):
        self.frame_purpure = ttk.Frame(self)
#        self.frame_purpure.config(relief=tkk.SUNKEN)  # relief=tkk.SUNKEN,
        self.frame_purpure.pack()

        self.canvas = tkk.Canvas(self.frame_purpure)  # tworze płótno
        self.canvas.config(height=30)
        self.canvas.create_line(0, 30, 10000, 30, fill='black', width=2)
        self.canvas.pack()

        self.checkbuttonFrame_purpureVar = tkk.StringVar(value='0')

        self.advanced = ttk.Checkbutton(self.frame_purpure, text='zaawansowane?')  # kwadrat do zaznaczenia
        self.advanced.state((['disabled']))
        self.advanced.pack(side=tkk.TOP, anchor='nw')
        self.advanced.config(variable=self.checkbuttonFrame_purpureVar, onvalue=1,
                             offvalue=0, command=self.display_input)  # display_input pack okna

        ttk.Label(self.frame_purpure, text='', font=('Arial', 8)).pack(pady=20)

        self.save_all_purpure_Frame = ttk.Button(self.frame_purpure, text="Zapisz wszyskie",
                                                 command=lambda: self.save_file(self.full_list_reserch_patch_files))
        self.save_all_purpure_Frame.pack(side=tkk.TOP, )
        self.save_all_purpure_Frame.state(['disabled'])

    def _create__yellow_frame(self, list_full_search_results_from_path):
        self.button_search.state((['disabled']))
        self.frame_yellow.config(relief=tkk.SUNKEN, padding=(30, 15))

        for result in self.widgets_results:
            for widgets in result:
                widgets['entry'].destroy()
                widgets['checkbox'].destroy()

        result_no = 0
        self.widgets_results = []
        list_full_search_results_from_1st_path = []

        if (len(self.full_list_reserch_patch_files[0][0]) > 1
                and isinstance(self.full_list_reserch_patch_files[0][0], list)):
            list_full_search_results_from_1st_path = [list_full_search_results_from_path[0]]  # concept change

        for file in list_full_search_results_from_1st_path:
            first_result_widgets = []
            file = [file[0]] + [file[-1]]  # concept change

            for result in file[:-1]:
                result_no += 1
                for field_no in range(int(self.scaleW_value.get())):
                    widgets = {'entry_str': tkk.StringVar(self)}
                    if field_no < len(result):
                        widgets['entry_str'].set(result[field_no])

                    widgets['entry'] = ttk.Entry(self.frame_yellow, textvariable=widgets['entry_str'], width=15,
                                                 font=('Arial', 10))

                    if not floor(field_no / 10):
                        row = (result_no - 1) * 4 + 1
                    else:
                        row = (result_no - 1) * 4 + 3
                    widgets['entry'].grid(row=row, column=field_no % 10, padx=0, pady=0)
                    widgets['entry'].state(['readonly'])
                    widgets['checkbox_str'] = tkk.StringVar(value='off')
                    widgets['checkbox_field_no'] = tkk.IntVar(value=field_no)

                    if not floor(field_no / 10):
                        row = (result_no - 1) * 4 + 2
                    else:
                        row = (result_no - 1) * 4 + 4
                    widgets['checkbox'] = ttk.Checkbutton(self.frame_yellow, text='dodać?')
                    widgets['checkbox'].config(variable=widgets['checkbox_str'], onvalue='on', offvalue='off')
                    widgets['checkbox'].grid(row=row, column=field_no % 10, padx=0, pady=(0, 20), sticky='n')

                    first_result_widgets.append(widgets)

                self.widgets_results.append(first_result_widgets)

        self.scaleW = tkk.Scale(
            self.frame_black, from_=10, label='ilość wyszukanych słów po', variable=self.scaleW_value,
            length=300, to=20, resolution=10, orient=tkk.HORIZONTAL)

        self.scaleW.grid(row=0, column=2, padx=0, pady=20)

        self.iw = len(list_full_search_results_from_path[0]) - 1
        self.ik = self.scaleW.get()

        print('iw:', self.iw)
        print('ik:', self.ik)

        self.button_search.state((['!disabled']))

    def no_results_found(self):
        self.frame_no_results_found = ttk.Frame(self)
        self.frame_no_results_found.config(height=50, width=400)
        nothing = ttk.Label(self.frame_no_results_found, text='Nie znaleziono żadnych wyników!', font=('Arial', 20))
        nothing.grid(row=5, column=0, pady=50, padx=100, columnspan=2)

    def _save_selected__add_file_names(self):
        self.frame__save_selected__add_file_names = ttk.Frame(self)
        self.frame__save_selected__add_file_names.config(height=50, width=400)

        self.save_selected = ttk.Button(
            self.frame__save_selected__add_file_names,
            text="Zapisz zaznaczone",
            command=lambda: self.function_save_selected(self.full_list_reserch_patch_files))

        self.save_selected .grid(row=0, column=0, padx=0, pady=10)
        self.save_selected .state(['!disabled'])

        self.Var_save_selected = tkk.IntVar(value=0)
        self.button_save_selected = ttk.Checkbutton(
            self.frame__save_selected__add_file_names,
            text='dodać nazwę plików??')
        self.button_save_selected.state((['!disabled']))

        self.button_save_selected.grid(row=0, column=2, padx=30, pady=10)
        self.button_save_selected.config(variable=self.Var_save_selected, onvalue=1, offvalue=0)

    def display_input(self):
        if self.checkbuttonFrame_purpureVar.get() == '1':
            self.save_all_purpure_Frame.state(['disabled'])
            self.frame_black.pack()
            self.frame_yellow.pack()
            self.frame__save_selected__add_file_names.pack()

        else:
            self.frame_black.forget()
            self.frame_yellow.forget()
            self.frame__save_selected__add_file_names.forget()
            self.save_all_purpure_Frame.state(['!disabled'])

    def refresh_frame_yellow(self, *args):
        self.create_text_in_entries(self.full_list_reserch_patch_files)
        self.save_all_purpure_Frame.state(['disabled'])


def main():
    gui_object = Gui()
    gui_object.mainloop()


if __name__ == "__main__":
    main()
