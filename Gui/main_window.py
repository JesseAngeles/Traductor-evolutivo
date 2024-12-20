import tkinter as tk
from tkinter import ttk
from tkinter import Text

from Controller.evolutive_translate import EvolutiveTranslate
from Controller.grammar import Grammar

class MainWindow:
    def __init__(self, root, db):
        self.root = root
        self.root.title("Aplicación Tkinter con MongoDB")
        self.root.geometry("620x600")
        
        self.evolutive_translate = EvolutiveTranslate(db)
        self.grammar = Grammar(db)
        
        # Contenedor
        notebook = ttk.Notebook(root)
        notebook.pack(expand=True, fill="both")

        # Pestañas
        self.tab1 = ttk.Frame(notebook)
        self.tab2 = ttk.Frame(notebook)

        ### Translate frame
        notebook.add(self.tab1, text="Translate")
        
        # Labels
        self.label_title = ttk.Label(self.tab1, text="Traductor evolutivo", font=("Arial", 22))
        self.label_title.place(x=180, y = 10)        

        self.label_options = ttk.Label(self.tab1, text="Similar options", font=("Arial", 16))
        self.label_options.place_forget()

        self.label_options.bind("<Enter>", self.show_hover_message)
        self.label_options.bind("<Leave>", self.hide_hover_message)

        # Combobox
        self.combo_from_lan = ttk.Combobox(self.tab1, font=("Arial", 12))
        self.combo_from_lan.place(x= 50, y = 55)
        
        self.combo_to_lan = ttk.Combobox(self.tab1, font=("Arial", 12))
        self.combo_to_lan.place(x= 375, y = 55)

        # text 
        self.entry_from_lan = Text(self.tab1, width=30, height=5)
        self.entry_from_lan.place(x=10, y = 95)

        self.entry_to_lan = Text(self.tab1, width=30, height=5)
        self.entry_to_lan.place(x=360, y=95)
        self.entry_to_lan.config(state="disabled")
        
        # Button
        self.button_switch_lan = ttk.Button(self.tab1, text="Switch", command=self.switch_lan)
        self.button_switch_lan.place(x=267, y = 50)
        
        self.button_translate = ttk.Button(self.tab1, text="Translate", command=self.translate)
        self.button_translate.place(x = 267, y = 110)

        self.button_add_translate = ttk.Button(self.tab1, text="Add word", command=self.add_translate)
        self.button_add_translate.place_forget()
    
        self.buttons_recommendation = []
    
        self.popup = None
    
        #  Grammar Frame
        notebook.add(self.tab2, text="Categories")

        # Label
        self.label_grammar = ttk.Label(self.tab2, text= "GRAMMAR", font=("Arial", 12))
        self.label_grammar.place(x=110, y = 30)  

        self.label_word = ttk.Label(self.tab2, text= "SET GRAMMAR WORD", font=("Arial", 12))
        self.label_word.place(x=110, y = 175)  

        self.label_struct = ttk.Label(self.tab2, text= "SET GRAMMAR STRUCTURE", font=("Arial", 12))
        self.label_struct.place(x=110, y = 320)  


        # text
        self.entry_grammar = Text(self.tab2, width= 30, height=3)
        self.entry_grammar.place(x=10, y = 75)
        
        self.entry_word = Text(self.tab2, width= 30, height=3)
        self.entry_word.place(x=10, y = 220)
        
        self.entry_struct_from = Text(self.tab2, width= 30, height=3)
        self.entry_struct_from.place(x=10, y = 400)
        
        self.entry_struct_to = Text(self.tab2, width= 30, height=3)
        self.entry_struct_to.place(x=360, y = 400)
          
        # Combobox
        self.combo_grammar = ttk.Combobox(self.tab2, font = ("Arial", 12))
        self.combo_grammar.place(x = 325, y = 220)
        
        self.combo_from_lan_g = ttk.Combobox(self.tab2, font= ("Arial", 12))
        self.combo_from_lan_g.place(x = 50, y = 365)
        
        self.combo_to_lan_g = ttk.Combobox(self.tab2, font= ("Arial", 12))
        self.combo_to_lan_g.place(x = 375, y = 365)
        
        # Button
        self.button_add_grammar = ttk.Button(self.tab2, text= "Add Grammar", command=self.add_category)
        self.button_add_grammar.place(x = 325, y = 100)
    
        self.button_set_grammar = ttk.Button(self.tab2, text= "Set Grammar", command=self.set_category)
        self.button_set_grammar.place(x = 325, y = 255)
    
        self.button_set_struct = ttk.Button(self.tab2, text="Create", command=self.set_struct)
        self.button_set_struct.place(x = 267, y = 415)

        # Init functions
        self.set_combobox_options()

    # Efecto hover
    def show_hover_message(self, event):
        # Crear un Toplevel que actúa como un popup
        if not self.popup:
            self.popup = tk.Toplevel(self.root)
            self.popup.wm_overrideredirect(True)  # Quitar bordes
            self.popup.geometry(f"+{event.x_root+10}+{event.y_root+10}")  # Posición del popup

            # Crear el contenido del popup
            label = tk.Label(self.popup, text="Palabra (Distancia de Levenshtein, Frecuencia de error)")
            label.pack()

    def hide_hover_message(self, event):
        # Destruir el popup cuando el mouse salga del botón
        if self.popup:
            self.popup.destroy()
            self.popup = None
    
    # Llenar las opciones de lenguage
    def set_combobox_options(self):
        languages = self.evolutive_translate.get_languages()
        categories = self.grammar.get_categories()

        # Llenar los combobox con las categorías de los lenguajes
        self.combo_from_lan['values'] = languages
        self.combo_to_lan['values'] = languages
        self.combo_from_lan_g['values'] = languages
        self.combo_to_lan_g['values'] = languages
        self.combo_grammar['values'] = categories
    
        self.combo_from_lan.set(languages[0]) 
        self.combo_to_lan.set(languages[1]) 
        self.combo_from_lan_g.set(languages[0]) 
        self.combo_to_lan_g.set(languages[1]) 
        self.combo_grammar.set(categories[0])        
        
            
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
            button = ttk.Button(self.tab1, text=f"{word[0]} ({word[1]}, {word[2]})", command=lambda w=word[0]: self.change_option(content, w))
            button.place(x=10, y=i)
            i += 40
            self.buttons_recommendation.append(button)

    def change_option(self, word, translate):
        self.evolutive_translate.update_frecuency_errors(word, translate)
        
        language = self.evolutive_translate.find_lan_by_word(translate)
        
        if language == self.combo_to_lan.get():
            self.switch_lan()
        
        self.label_options.place_forget()
        for button in self.buttons_recommendation:
            button.destroy()
        
        self.combo_from_lan.set(language)
        self.set_entry_from_lan(translate)
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
        
        
    def add_category(self):
        category = self.entry_grammar.get("1.0", tk.END).strip()
        self.grammar.addCategory(category)
        
        categories = list(self.combo_grammar['values'])
        categories.append(category)
        self.combo_grammar['values'] = categories
        self.combo_grammar.set(category)
        
             
    def set_category(self):
        word = self.entry_word.get("1.0", tk.END).strip()
        category = self.combo_grammar.get()
        
        self.grammar.setCategory(word, category)
        self.entry_word.delete('1.0', tk.END)
        
    
    def set_struct(self):
         lan_from = self.combo_from_lan_g.get()
         lan_to = self.combo_to_lan_g.get()
         
         struct_from = self.entry_struct_from.get("1.0", tk.END).strip()
         struct_to = self.entry_struct_to.get("1.0", tk.END).strip()
         
         self.grammar.setStruct(lan_from, lan_to, struct_from, struct_to)