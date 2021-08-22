#  REQUIREMENTS

import tkinter as tk
from tkinter.constants import LEFT, YES
import requests as req
from bs4 import BeautifulSoup as bs



from threading import Thread
from base64 import b64decode as bd
from random import choice, randint
from pyperclip import copy




# AUTHOR

author = "{}".format(bd("YmlsbHl0aGVnb2F0MzU2").decode('utf-8'))



class GoogleSearch():

    headers = {'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36"}

    def search(query:str=None,
                results_len:int=1, 
                lang:str="fr", 
                encoding:str="utf-8",
                random:bool=False,
                **kwargs):
        
        """
        Google Search
        :param query | str: --> The text to be searched | ex: "billythegoat356"
        :param results_len | int: --> Number of results | ex: 4
        :param lang | str: --> The language | ex: "en"
        :param encoding | str: --> The encoding for the research | ex: "utf-8"
        :param random | bool: --> Return a random link

        :google dorks | str: --> Google Dorks keyword arguments. Query has to be None.                                      
        """
        
        return GoogleSearch._search(query=query, results_len=results_len, lang=lang, encoding=encoding, random=random, **kwargs)


    def _search(query:str=None,
                results_len:int=1, 
                lang:str="fr", 
                encoding:str="utf-8",
                random:bool=False,
                **kwargs):


        if query is None and kwargs == {} or query is not None and kwargs != {}:
            raise GoogleSearch.QueryError("Either 'query' argument either keyword arguments has to be passed.")

        query = GoogleSearch._dorks(**kwargs) if query is None else query.replace(" ", "+")

        results_len_search = randint(5, 25) + results_len if random else results_len

        url = f"https://google.com/search?q={query}&num={results_len_search}&hl={lang}&ie={encoding}"
        r = req.get(url, headers=GoogleSearch.headers)

        r.raise_for_status()
        html = r.text


        results = GoogleSearch._parse(html)


        if random:
            random_results = []
            for _ in range(results_len):
                random_result = choice(results)
                random_results.append(random_result)
                results.remove(random_result)
            return random_results


        if results_len != len(results):
            results = results[:results_len]


        return results

    
    def _dorks(**kwargs):
        return " ".join(k+":"+v for k, v in kwargs.items() if v is not None)
    
    def _parse(html:str):
        results = []

        soup = bs(html, 'html.parser')
        result_block = soup.find_all('div', attrs={'class': 'g'})
        for result in result_block:
            link = result.find('a', href=True)
            title = result.find('h3')
            if link and title:
                results.append(link['href'])
        
        return results


    class QueryError(Exception): ...




class Dorks:

    def github_search(text:str, results_len:int=1, random:bool=False, advanced:bool=False):
        return Dorks.website_search(website="github.com", text=text, results_len=results_len, random=random, advanced=advanced)

    def stackoverflow_search(text:str, results_len:int=1, random:bool=False, advanced:bool=False):
        return Dorks.website_search(website="stackoverflow.com", text=text, results_len=results_len, random=random, advanced=advanced)
    
    def youtube_search(text:str, results_len:int=1, random:bool=False, advanced:bool=False):
        return Dorks.website_search(website="youtube.com", text=text, results_len=results_len, random=random, advanced=advanced)
    
    def pornhub_search(text:str, results_len:int=1, random:bool=False, advanced:bool=False):
        return Dorks.website_search(website="pornhub.com", text=text, results_len=results_len, random=random, advanced=advanced)
    
    def api_search(text:str, results_len:int=1, random:bool=False, advanced:bool=False):
        text += " api"
        url, title = "api" if advanced else None, "api" if advanced else None
        return GoogleSearch.search(results_len=results_len, random=random, inurl=url, intitle=title, intext=text)
    


    def website_search(website:str, text:str, results_len:int=1, random:bool=False, advanced:bool=False):
        title = text if advanced else None
        return GoogleSearch.search(results_len=results_len, random=random, site=website, intitle=title, intext=text)

    # add Pornhub et YouTube
    




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

        self.copy_button = tk.Button(self.window, text = "Copier le lien", font= ("Times New Roman", 10), bg = "black", fg = "white", command = self.copy_scale)
        self.copy_button.place(x=505, y=450)
        self.pass_button = tk.Button(self.window, text = "Ignorer", font= ("Times New Roman", 10), bg = "black", fg = "white", command = self.pass_scale)
        self.pass_button.place(x=520, y=480)


    def copy_scale(self, ignore=False):
        
        try:
            if not ignore:
                copy(self.links.get(self.links.curselection()))
        except tk.TclError:
            return

        self.modes.pack_forget()
        self.search_button.place(x=510, y=550)
        self.copy_button.place_forget()
        self.pass_button.place_forget()
        self.results_label.place_forget()
        self.text.delete(0, len(self._search_text.get()))
        self.text.place(x=440, y=500, width=200)

    def pass_scale(self):
        self.copy_scale(ignore=True)



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


if __name__ == '__main__':
    GUI()