import tkinter as tk
from tkinter import ttk
from tkinter import Text

from Controller.evolutive_translate import EvolutiveTranslate

class MainWindow:
    def __init__(self, root, db):
        self.root = root
        self.root.title("Aplicación Tkinter con MongoDB")
        self.root.geometry("620x600")
        
        self.evolutive_translate = EvolutiveTranslate(db)
        
        # Contenedor
        notebook = ttk.Notebook(root)
        notebook.pack(expand=True, fill="both")

        # Pestañas
        self.tab1 = ttk.Frame(notebook)
        self.tab2 = ttk.Frame(notebook)

        notebook.add(self.tab1, text="Translate")
        notebook.add(self.tab2, text="tmp")

        # Labels
        self.label_title = ttk.Label(self.tab1, text="Traductor evolutivo", font=("Arial", 22))
        self.label_title.place(x=180, y = 10)        

        self.label_options = ttk.Label(self.tab1, text="Similar options", font=("Arial", 16))
        self.label_options.place_forget()

        # Combobox
        self.combo_from_lan = ttk.Combobox(self.tab1, font=("Arial", 12))
        self.combo_from_lan.place(x= 50, y = 55)
        
        self.combo_to_lan = ttk.Combobox(self.tab1, font=("Arial", 12))
        self.combo_to_lan.place(x= 375, y = 55)
        
        self.set_languages()

        # text 
        self.entry_from_lan = Text(self.tab1, width=30, height=5)
        self.entry_from_lan.place(x=10, y = 95)

        self.entry_to_lan = Text(self.tab1, width=30, height=5)
        self.entry_to_lan.place(x=360, y=95)
        self.entry_to_lan.config(state="disabled")
        
        # Button
        self.button_switch_lan = ttk.Button(self.tab1, text="Swtich", command=self.switch_lan)
        self.button_switch_lan.place(x=267, y = 50)
        
        self.button_translate = ttk.Button(self.tab1, text="Translate", command=self.translate)
        self.button_translate.place(x = 267, y = 110)

        self.button_add_translate = ttk.Button(self.tab1, text="Add word", command=self.add_translate)
        self.button_add_translate.place_forget()
    
        self.buttons_recommendation = []
    
    # Llenar las opciones de lenguage
    def set_languages(self):
        languages = self.evolutive_translate.get_languages()

        # Llenar los combobox con las categorías de los lenguajes
        self.combo_from_lan['values'] = languages
        self.combo_to_lan['values'] = languages
    
        self.combo_from_lan.set(languages[0]) 
        self.combo_to_lan.set(languages[1]) 
            
    # Insertar texto en los entry
    def set_entry_from_lan(self, content):
        self.entry_from_lan.delete("1.0", tk.END)
        self.entry_from_lan.insert(tk.END, content)
        
    def set_entry_to_lan(self, content):
        self.entry_to_lan.config(state="normal")
        self.entry_to_lan.delete("1.0", tk.END)
        self.entry_to_lan.insert(tk.END, content)
        self.entry_to_lan.config(state="disabled")
        
    # Funciones de botones
    def switch_lan(self):
        from_text = self.combo_from_lan.get()      
        self.combo_from_lan.set(self.combo_to_lan.get())
        self.combo_to_lan.set(from_text)
        
        self.set_entry_from_lan(self.entry_to_lan.get("1.0", tk.END).strip())
        self.translate()
        self.button_add_translate.place_forget()
    
    def translate(self):
        from_language = self.combo_from_lan.get()
        to_language = self.combo_to_lan.get()
        
        if(from_language == to_language): return False
        
        content = self.entry_from_lan.get("1.0", tk.END).strip()  
        
        translate = self.evolutive_translate.find_translate(from_language, to_language, content)

        if translate:
            self.set_entry_to_lan(translate)
            self.button_add_translate.place_forget()
            self.label_options.place_forget()
        else:
            self.set_entry_to_lan("")
            self.entry_to_lan.config(state="normal")
            self.button_add_translate.place(x=267, y = 150)
            
            self.similar_options(content)
            
    def similar_options(self, content):
        self.label_options.place(x=10, y=200)
        words = self.evolutive_translate.get_similar_words(content)

        # Si la palabra existe unicamente en otro idioma
        if words[0][1] == 0 and words[1][1] != 0:
            language = self.evolutive_translate.find_lan_by_word(words[0][0])
            self.combo_to_lan.set(self.combo_from_lan.get())
            self.combo_from_lan.set(language)
            self.translate()
            self.label_options.place_forget()
            for button in self.buttons_recommendation:
                button.destroy()
            
            return
            
        i = 240
        for word in words:
            # Usar lambda para posponer la ejecución del comando hasta que el botón sea presionado
            button = ttk.Button(self.tab1, text=f"{word[0]}({word[1]})", command=lambda w=word[0]: self.change_option(w))
            button.place(x=10, y=i)
            i += 40
            self.buttons_recommendation.append(button)

    def change_option(self, word):
        language = self.evolutive_translate.find_lan_by_word(word)
        
        if language == self.combo_to_lan.get():
            self.switch_lan()
        
        self.label_options.place_forget()
        for button in self.buttons_recommendation:
            button.destroy()
        
        self.combo_from_lan.set(language)
        self.set_entry_from_lan(word)
        self.translate()
        
        
            
    def add_translate(self):
        from_language = self.combo_from_lan.get()
        to_language = self.combo_to_lan.get()
        content = self.entry_from_lan.get("1.0", tk.END).strip()  
        translate = self.entry_to_lan.get("1.0", tk.END).strip()  
        
        self.evolutive_translate.add_translate(from_language, to_language, content, translate)
        
        self.label_options.place_forget()
        for button in self.buttons_recommendation:
            button.destroy()
        