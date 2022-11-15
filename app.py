
#By importing specific classes from moudles, we isolating our project from whole library. It is Facade pattern
from fileinput import filename
import tkinter as tk
from tkinter.constants import DISABLED, NORMAL, W, E
from tkinter import filedialog as fd
from adapter import ClientAdapter

class App(tk.Tk):
    #class level variables
    filename = ""
    #creating window with __init__ method
    def __init__(self):
        super().__init__()

        #creating variable for checkbuttons
        self.is_csv = tk.IntVar()
        self.is_xml = tk.IntVar()
        #configuring the root window
        self.title("Formatter v1.0.0")
        #self.geometry("320x200")

        #adding frames
        self.frame1 = tk.LabelFrame(self, text = "File path")
        self.frame1.pack(fill="both")

        self.frame2 = tk.LabelFrame(self, text = "File format")
        self.frame2.pack(fill="both")

        self.frame3 = tk.LabelFrame(self, text = "Output file")
        self.frame3.pack(fill="both")

        #first frame widgets
        self.label1 = tk.Label(self.frame1, text = "Please, choose a file:", font = "Helvetica 15")
        self.label1.grid(sticky= W,row = 0, column = 0)

        self.choose_button = tk.Button(self.frame1, text = "Browse files", command = self.select_file)
        self.choose_button.grid(sticky = W, row = 0, column = 1)

        self.format_info = tk.Label(self.frame1, text = "Supported formats: .txt, .csv", font='Helvetica 13 italic', fg = "#ccc612")
        self.format_info.grid(sticky = W, row = 1, column = 0)
        
        self.selected_file = tk.Label(self.frame1, text = "", font='Helvetica 13')
        self.selected_file.grid(sticky = W, row = 1, column = 1)


        #second frame widgets
        self.format_label = tk.Label(self.frame2, text = "Please choose the format:", font = "Helvetica 15")
        self.format_label.grid(sticky = W, row = 0, column = 0)

        self.csv_check = tk.Checkbutton(self.frame2, text = "CSV", variable = self.is_csv, command = self.is_checked, state = DISABLED)
        self.csv_check.grid(sticky = W, row = 0, column = 1)

        self.xml_check = tk.Checkbutton(self.frame2, text = "XML", variable = self.is_xml, command = self.is_checked, state = DISABLED)
        self.xml_check.grid(sticky = W, row = 0, column = 2)

        #third frame widgets
        self.file_generator = tk.Button(self.frame3, text = "Generate file", command = self.generate, state = DISABLED)
        self.file_generator.grid(sticky = W, row = 0, column = 0)

        self.file_generator_error = tk.Label(self.frame3, text = "Format or file not chosen!", fg = "red")
        self.file_generator_error.grid(sticky = E, row = 0, column = 1)

    #creating new window for choosing the file. File formats are restricted: TXT and CSV ONLY. Idea of Facade pattern.
    def select_file(self):
        self.filetypes = (('text files', '*.txt'),('csv files', '*.csv'))

        self.filename = fd.askopenfilename(title = 'Choose a file', initialdir = '/', filetypes = self.filetypes)

        self.selected_file['text'] = self.filename

        if self.filename != "":
            self.csv_check.config(state = NORMAL)
            self.xml_check.config(state = NORMAL)
            self.file_generator_error['text'] = "Format not chosen!"
    #checking the state of the checkbuttons. Checkbuttons saves the state of choice. Mimics the Memento pattern.
    def is_checked(self):
        if self.is_xml.get() == 1 or self.is_csv.get() == 1:
            self.file_generator['state'] = NORMAL
            self.file_generator_error['text'] = ""
        else:
            self.file_generator['state'] = DISABLED
            self.file_generator_error['text'] = "Format not chosen!"

    #generating new XML/CSV file with adapter
    def generate(self):
        client_adapter = ClientAdapter(self.filename, self.is_csv.get(), self.is_xml.get())
        client_adapter.adapter()



#During the launch only one window can be launched, so is is a implementation of Singleton pattern
if __name__ == "__main__":
    app = App()
    app.mainloop()