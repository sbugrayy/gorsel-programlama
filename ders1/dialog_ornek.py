import tkinter as tk
from tkinter import messagebox

class DialogOrnek:
    def __init__(self):
        self.pencere = tk.Tk()
        self.pencere.title("Dialog Örneği")
        self.pencere.geometry("600x400")
        
        # Frame'leri oluşturma
        self.kirmizi_frame = tk.Frame(self.pencere, bg="red")
        self.mavi_frame = tk.Frame(self.pencere, bg="blue")
        self.yesil_frame = tk.Frame(self.pencere, bg="green")
        
        # Grid layout ile yerleştirme
        self.kirmizi_frame.grid(row=0, column=0, sticky="nsew")
        self.mavi_frame.grid(row=0, column=1, sticky="nsew")
        self.yesil_frame.grid(row=0, column=2, sticky="nsew")
        
        # Grid ağırlıklarını ayarlama
        self.pencere.grid_columnconfigure(0, weight=1)
        self.pencere.grid_columnconfigure(1, weight=1)
        self.pencere.grid_columnconfigure(2, weight=1)
        self.pencere.grid_rowconfigure(0, weight=1)
        
        # Buton oluşturma
        self.buton = tk.Button(self.mavi_frame,  # Butonu mavi frame'e yerleştirdim
                              text="Show Dialog", 
                              command=self.dialog_goster,
                              width=15,
                              height=2)
        self.buton.pack(expand=True)
        
    def dialog_goster(self):
        sonuc = messagebox.askokcancel("Uyarı", "Bu bir uyarı mesajıdır!\nDevam etmek istiyor musunuz?")
        if sonuc:
            messagebox.showinfo("Bilgi", "OK butonuna tıkladınız!")
        else:
            messagebox.showinfo("Bilgi", "Cancel butonuna tıkladınız!")
    
    def baslat(self):
        self.pencere.mainloop()

if __name__ == "__main__":
    uygulama = DialogOrnek()
    uygulama.baslat() 