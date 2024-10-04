from tkinter import *
from tkinter import ttk

from evolutiveTranslate import evolutiveTranslate

class GUI:
    def __init__(self, root):
        self.root = root
        self.root.title("App")
        self.root.geometry("620x600")

        self.root.protocol("WM_DELETE_WINDOW", self.on_close)

        # Contenedor
        notebook = ttk.Notebook(root)
        notebook.pack(expand=True, fill="both")

        # Pestañas
        tab1 = ttk.Frame(notebook)
        tab2 = ttk.Frame(notebook)

        notebook.add(tab1, text="Translate")
        notebook.add(tab2, text="tmp")

        # labels
        self.labelTitle = ttk.Label(tab1, text="Traductor evolutivo", font=("Arial", 22))
        self.labelTitle.place(x=180, y = 10)

        #textboxes
        self.entrySpanish = Text(tab1, width=30, height=5)
        self.entrySpanish.place(x=10, y = 55)

        self.entryEnglish = Text(tab1, width=30, height=5)
        self.entryEnglish.place(x=360, y=55)
        self.entryEnglish.config(state="disabled")

        # buttons
        self.buttonTranslate = ttk.Button(tab1, text="Translate", command=self.translate)
        self.buttonTranslate.place(x = 267, y = 70)

        self.buttonCreate = ttk.Button(tab1, text="Add word", command=self.addWord)
        self.buttonCreate.place_forget()

        # Inicialización
        self.et = evolutiveTranslate()

    def on_close(self):
        self.et.saveCSV()
        self.root.destroy()

    def translate(self):
        self.entryEnglish.config(state="normal")
        self.entryEnglish.delete("1.0", END)
        self.entryEnglish.config(state="disabled")
            

        word = self.entrySpanish.get("1.0", END).strip()     
        translate_word = self.et.findTranslate(word)
        if(translate_word):
            self.entryEnglish.config(state="normal")
            self.entryEnglish.insert(END, translate_word)
            self.entryEnglish.config(state="disabled")
            self.buttonCreate.place_forget()
        else:
            self.entryEnglish.config(state="normal")
            self.buttonCreate.place(x=267, y = 110)

    def addWord(self):
        word = self.entrySpanish.get("1.0", END).strip()
        translate = self.entryEnglish.get("1.0", END).strip()
        self.et.insertWord(word, translate)

        self.entryEnglish.config(state="disabled")
        self.buttonCreate.place_forget()