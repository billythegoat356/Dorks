#  REQUIREMENTS

import tkinter as tk
import requests as req
from bs4 import BeautifulSoup as bs
from pydorks import GoogleSearch, Dorks


from threading import Thread
from base64 import b64decode as bd
from webbrowser import open_new




# AUTHOR

author = "{}".format(bd("YmlsbHl0aGVnb2F0MzU2").decode('utf-8'))


    



# TKINTER GUI SETUP

class GUI:
    def __init__(self):

        self.window = window = tk.Tk()

        window.title("Dorks")
        window.geometry("1080x720")
        window.minsize(1080, 720)
        window.config(background='#000000')

        return self.run()

    def set_title(self):

        self.title_label = tk.Label(self.window, text = "Dorks", font = ("Times New Roman", 25), bg = "#000000", fg = "#ffffff")
        self.title_label.place(x=499, y=100)

    def set_author(self):

        self.author_label = tk.Label(self.window, text = f"by {author}", font = ("Times New Roman", 10), bg = "#000000", fg = "#ffffff")
        self.author_label.place(x=490, y=160)


    def set_modes(self):
        self.modes = tk.Listbox(self.window, bg = "black", fg = "white")
        self.modes.insert(1, "Google")
        self.modes.insert(2, "Github")
        self.modes.insert(3, "Stack Overflow")
        self.modes.insert(4, "Youtube")
        self.modes.insert(5, "Pornhub")
        self.modes.insert(6, "Api")

        # add Pornhub et YouTube

        self.modes.select_set(0)
        self.modes.place(x=480, y=220)

    def set_results_len(self):
        self.results_len = tk.Scale(self.window, from_=1, to=5, bg = "black", fg = "white")
        self.results_len.place(x=400, y=240)

    def set_random(self):
        self.random_bool = tk.BooleanVar()

        self.random = tk.Checkbutton(self.window, text = "Mode Aléatoire", var = self.random_bool)
        self.random.place(x=680, y=260)

    def set_advanced(self):

        self.advanced_bool = tk.BooleanVar()

        self.advanced = tk.Checkbutton(self.window, text = "Mode Recherche Avancée", var = self.advanced_bool)
        self.advanced.place(x=650, y=300)


    def set_text(self):
        self.text = tk.Entry(self.window)
        self.text.place(x=440, y=500, width=200)

    

    def set_search_button(self):
        self.search_button = tk.Button(self.window, text = "Chercher", font= ("Times New Roman", 10), bg = "black", fg = "white", command = self.search)
        self.search_button.place(x=510, y=550)

    def set_results_label(self):
            self.results_label_variable = tk.StringVar()
            self.results_label_variable.set("Chargement en cours...")
            self.results_label = tk.Label(self.window, bg = "black", fg = "white", textvariable=self.results_label_variable)
            
    def thread_search(self, choice_mode, text, random, advanced, results_len):

        if choice_mode == "Google":
            results = GoogleSearch.search(text=text, random=random, results_len=results_len)
        elif choice_mode == "Github":
            results = Dorks.github_search(text=text, random=random, advanced=advanced, results_len=results_len)
        elif choice_mode == "Stack Overflow":
            results = Dorks.stackoverflow_search(text=text, random=random, advanced=advanced, results_len=results_len)
        elif choice_mode == "Youtube":
            results = Dorks.youtube_search(text=text, random=random, advanced=advanced, results_len=results_len)
        elif choice_mode == "Pornhub":
            results = Dorks.pornhub_search(text=text, random=random, advanced=advanced, results_len=results_len)
        elif choice_mode == "Api":
            results = Dorks.api_search(text=text, random=random, advanced=advanced, results_len=results_len)

        if results == []:
            results.append("about:blank")
            
        r = 0
        for l in results:
            if len(l) > r:
                r = len(l)

        fresults = []
        for f in results:
            if len(f) < r:
                f = " " * int(((r-len(f)))) + f
            fresults.append(f)

        
        results = fresults


        self.results_label.place_forget()

    

        self.links = tk.Listbox(self.window, width=r, bg = "black", fg = "white")
        for result, number in zip(results, range(len(results))):
            self.links.insert(number, result)
        self.links.pack(side=tk.BOTTOM)

        self.open_button = tk.Button(self.window, text = "Ouvrir", font= ("Times New Roman", 10), bg = "black", fg = "white", command = self.open_link)
        self.open_button.place(x=520, y=450)
        self.skip_button = tk.Button(self.window, text = "Passer", font= ("Times New Roman", 10), bg = "black", fg = "white", command = self.skip_link)
        self.skip_button.place(x=520, y=480)


    def open_link(self, ignore=False):
        
        try:
            if not ignore:
                open_new(self.links.get(self.links.curselection()))
        except tk.TclError:
            return


    def skip_link(self):
        self.modes.pack_forget()
        self.search_button.place(x=510, y=550)
        self.open_button.place_forget()
        self.skip_button.place_forget()
        self.links.pack_forget()
        self.text.delete(0, len(self.text.get()))
        self.text.place(x=440, y=500, width=200)



    def search(self):
        global results_entry, results_entry_variable

        try:
            mode = self.modes.get(self.modes.curselection())
        except tk.TclError:
            return

        text = self.text.get()
        random = self.random_bool.get()
        advanced = self.advanced_bool.get()
        results_len = self.results_len.get()

        if not text:
            return

    


        self.text.place_forget()
        self.search_button.place_forget()
        self.results_label.place(x=480, y=550)



        Thread(target=self.thread_search, args=[mode, text, random, advanced, results_len]).start()




    def set_all(self):
        self.set_title()
        self.set_author()
        self.set_modes()
        self.set_results_len()
        self.set_random()
        self.set_advanced()
        self.set_text()
        self.set_search_button()
        self.set_results_label()


    def run(self):

        self.set_all()
        self.window.mainloop()

        
        
# START

if __name__ == '__main__':
    GUI()
