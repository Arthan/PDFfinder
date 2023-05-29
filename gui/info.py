from tkinter import Toplevel, Label, Button, PhotoImage
import webbrowser


class PDFFinderInfo(Toplevel):
    def __init__(self, master, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self.title('PDF finder info')

        window_width = self.winfo_reqwidth()
        window_height = self.winfo_reqheight()
        position_right = int(self.winfo_screenwidth() / 2 - window_width / 2)
        position_down = int(self.winfo_screenheight() / 2 - window_height / 2)
        self.geometry("+{}+{}".format(position_right, position_down))

        self.resizable(False, False)
        self.attributes('-topmost', 'true')
        self.label = Label(self, width=5)
        self.label2 = Label(self, width=5)
        self.label2 = Label(self, width=5)
        self.label3 = Label(self, width=5)
        self.label4 = Label(self, width=5)
        self.label5 = Label(self, width=5)

        Label(self, text='PdfFinder ver 1.0 (x64):').grid(row=1, column=1, padx=10, pady=5, sticky='sw')
        Label(self, text='Copyright (c) Borys Gołębiowski:').grid(row=2, column=1, padx=10, sticky='sw')

        self.logo = PhotoImage(file='logoOpnie.png')
        Label(self, image=self.logo).grid(row=2, column=2, rowspan=2)

        Label(self, text='You can find me on:').grid(row=3, column=1, padx=10, pady=5, sticky='sw')

        link1 = Label(self, text='Facebook:', cursor="hand2")
        link1.grid(row=4, column=1, padx=10, pady=10, sticky='sw')
        link1.bind("<Button-1>", lambda e: webbrowser.open_new("https://www.facebook.com/NathanCelina"))

        link2 = Label(self, text='Linkedin', cursor="hand2")
        link2.grid(row=5, column=1, padx=10, pady=10, sticky='sw')
        link2.bind("<Button-1>",
                   lambda e: webbrowser.open_new("https://www.linkedin.com/in/borys-go%C5%82%C4%99biowski-02b883158/"))

        link3 = Label(self, text='Email', cursor="hand2")
        link3.grid(row=6, column=1, pady=10, padx=10, sticky='sw')
        link3.bind("<Button-1>", lambda e: webbrowser.open_new("mailto:borysgolebiowskipl@gmail.com"))

        button_window = Button(self, text="Copy email")
        button_window.grid(row=6, column=2, sticky='sw')

        Label(self, text='PdfFinder jest programem darmowym').grid(row=7, column=1, padx=10, pady=30, sticky='sw')


if __name__ == '__main__':
    import os
    import tkinter as tk

    os.chdir("../")

    root = tk.Tk()
    feedback = PDFFinderInfo(root)
    root.mainloop()
