from Gui.main_window import MainWindow
from Database.db_connection import get_db
import tkinter as tk

def main():
    # Conexion con la base de datos
    db = get_db()
    
    
    # Iniciar ventana tkinter
    root = tk.Tk()
    app = MainWindow(root, db)
    root.mainloop()
    

if __name__ == "__main__":
    main()