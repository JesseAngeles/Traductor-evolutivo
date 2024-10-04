from tkinter import *
from tkinter import ttk
from PIL import Image, ImageTk 

from evolutiveTranslate import evolutiveTranslate

class GUI:
    def __init__(self, root):
        self.root = root
        self.root.title("App")
        self.root.geometry("620x600")

        self.root.protocol("WM_DELETE_WINDOW", self.on_close)

        # Inicialización
        self.et = evolutiveTranslate()
        [self.fromLanguage, self.toLanguage] = self.et.getHeaders()
        
        # Contenedor
        notebook = ttk.Notebook(root)
        notebook.pack(expand=True, fill="both")

        # Pestañas
        self.tab1 = ttk.Frame(notebook)
        self.tab2 = ttk.Frame(notebook)

        notebook.add(self.tab1, text="Translate")
        notebook.add(self.tab2, text="tmp")

        # labels
        self.labelTitle = ttk.Label(self.tab1, text="Traductor evolutivo", font=("Arial", 22))
        self.labelTitle.place(x=180, y = 10)

        self.labelOptions = ttk.Label(self.tab1, text="Quisite decir..", font=("Arial", 16))
        self.labelOptions.place_forget()

        self.labelfromLanguage = ttk.Label(self.tab1, font=("Arial", 16), text=self.fromLanguage)
        self.labelfromLanguage.place(x= 100, y = 55)

        self.labelToLan = ttk.Label(self.tab1, font=("Arial", 16), text=self.toLanguage)
        self.labelToLan.place(x=460, y = 55)

        #textboxes
        self.entryfromLanguage = Text(self.tab1, width=30, height=5)
        self.entryfromLanguage.place(x=10, y = 95)

        self.entryEnglish = Text(self.tab1, width=30, height=5)
        self.entryEnglish.place(x=360, y=95)
        self.entryEnglish.config(state="disabled")

        # imagenes
        image = Image.open("resources/icons/swap.png")
        resized_image = image.resize((20, 20))
        self.imageSwitch = ImageTk.PhotoImage(resized_image)

        # buttons
        self.buttonSwitch = ttk.Button(self.tab1, image=self.imageSwitch, command=self.switchLan)
        self.buttonSwitch.place(x = 295, y = 60)
        
        self.buttonTranslate = ttk.Button(self.tab1, text="Translate", command=self.translate)
        self.buttonTranslate.place(x = 267, y = 110)

        self.buttonCreate = ttk.Button(self.tab1, text="Add word", command=self.addWord)
        self.buttonCreate.place_forget()

    def on_close(self):
        self.et.saveCSV()
        self.root.destroy()

    def switchLan(self):
        tmp = self.fromLanguage
        self.fromLanguage = self.toLanguage
        self.toLanguage = tmp

        self.labelfromLanguage.config(text=self.fromLanguage)
        self.labelToLan.config(text=self.toLanguage)

    def translate(self):
        self.entryEnglish.config(state="normal")
        self.entryEnglish.delete("1.0", END)
        self.entryEnglish.config(state="disabled")
            

        word = self.entryfromLanguage.get("1.0", END).strip()     
        translate_word = self.et.findTranslate(word)
        if(translate_word):
            
            self.entryEnglish.config(state="normal")
            self.entryEnglish.insert(END, translate_word)
            self.entryEnglish.config(state="disabled")
            self.buttonCreate.place_forget()
        else:
            df = self.et.getDistances(word)
            self.printOptions(df)

            self.entryEnglish.config(state="normal")
            self.buttonCreate.place(x=267, y = 110)

    def addWord(self):
        word = self.entryfromLanguage.get("1.0", END).strip()
        translate = self.entryEnglish.get("1.0", END).strip()
        self.et.insertWord(word, translate)

        self.entryEnglish.config(state="disabled")
        
        self.buttonCreate.place_forget()
        self.labelOptions.place_forget()

        for button in self.optionButtons:
            button.destroy()

    def printOptions(self, df):
        self.labelOptions.place(x=10, y=200)
    
        self.optionButtons = []

        y = 240
        for index, row in df.head().iterrows():
            optionButton = ttk.Button(self.tab1, text=row['español'], command=lambda idx=index: self.onOptionSelect(idx))
            optionButton.place(x=30, y=y)
            
            self.optionButtons.append(optionButton)
            
            y += 40  

    def onOptionSelect(self, index):
        register = self.et.getRegister(index)
   
        self.entryfromLanguage.delete("1.0", END)
        self.entryfromLanguage.insert(END, register['español'])

        self.entryEnglish.config(state="normal")
        self.entryEnglish.delete("1.0", END)
        self.entryEnglish.insert(END, register['english'])
        self.entryEnglish.config(state="disabled")

        self.labelOptions.place_forget()
        self.buttonCreate.place_forget()

        for button in self.optionButtons:
            button.destroy()
        