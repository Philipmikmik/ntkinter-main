# import ssl
import json
from time import sleep
from kivy.app import App
from kivy.core.clipboard import Clipboard
from kivy.network.urlrequest import UrlRequest
from kivy.properties import StringProperty
from kivy.uix.image import AsyncImage
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.uix.textinput import TextInput
from kivy.uix.label import Label
from kivy.lang import Builder
# ssl._create_default_https_context = ssl._create_unverified_context
started = 0
slide = 0
loaded = True
#Builder.load_file('main.kv')
link_data = {}

UrlRequest("https://ntkinter-api.herokuapp.com/json/")

def formating(string):
    if string == '':
        return "None"
    else:
        string.replace(" ", "%20")
        return string

class MyLayout(Screen):
    def build(self):
        dam=Label(text="WHy", pos_hint={'center_x': .5, 'center_y': .45})
        return dam
    def press(self):
        global loaded
        if loaded:
            loaded = False
            st = Settings()
            data1 = formating(st.ids.inputEX.text)
            data2 = formating(st.ids.inputIN.text)
            UrlRequest(
                (
                    f"https://ntkinter-api.herokuapp.com/json/?exc="
                    f"{data1}&inc={data2}"
                ), self.rand)

    def rand(self, req, result):
        global page, started, yee, slide, loaded, load, backup, howmany
        print(result)
        if self.ids.my_carousel is None:
            sleep(.1)
        else:
            self.ids.my_carousel.clear_widgets()
        yee = result
        page = 0
        tags = ""
        backup = result['img']
        for i in range(len(result['tags']) - 1):
            tags = tags + str(result['tags'][i]) + ", "
        print(tags)
        tags = tags[:-2]
        autor = result['author']
        autor.append("Not defined")
        self.ids.title.text = "Title: " + result['title']
        self.ids.author.text = "Author: " + autor[0]
        self.ids.tags.text = "Tags: " + tags
        print(tags)
        self.ids.clip.text = str(result['id'])
        if len(result['img']) < 4:
            for i in range(len(result['img']) - 1):
                src = result['img'][i]
                image = AsyncImage(source=src)
                self.ids.my_carousel.add_widget(image)
        else:
            for i in range(4):
                src = result['img'][0]
                image = AsyncImage(source=src)
                self.ids.my_carousel.add_widget(image)
                backup.pop(0)
                load = 4
        self.do_layout()
        slide = 0
        howmany = str(len(result['img']) + 4)
        started = 1
        self.ids.pages.text = "1/" + howmany
        loaded = True

    def copy(self):
        if started == 1:
            Clipboard.copy(f"nhentai.net/g/{yee['id']}")

    def pages(self):
        global load, howmany
        if started == 1:
            for i in range(10):
                if slide != (self.ids.my_carousel.index + 1):
                    self.ids.pages.text = (
                        f"{self.ids.my_carousel.index + 1}"
                        f"/{howmany}")
            if (self.ids.my_carousel.index + 4) > load:
                if 0 != len(backup):
                    src = backup[0]
                    image = AsyncImage(source=src)
                    self.ids.my_carousel.add_widget(image)
                    backup.pop(0)
                    load += 1

class Settings(Screen):
    pass

class Favorites(Screen):
    def bruh(self):
        for i in range(2):
            x_damn = .2
            for j in range(2):
                ok = Label(text="BRUH", pos_hint={'x':x_damn, 'y':(i/10)})
                Favorites.add_widget(self,ok)
                x_damn += .1
    pass

class LinkEditor(TextInput):
    settings = StringProperty('settings.json')
    in_ex = StringProperty('')

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.bind(on_text=self.on_text)

    def on_kv_post(self, *largs):
        self.text = link_data.get(self.in_ex, "")

    def on_text(self, *largs):
        global link_data
        link_data[self.in_ex] = self.text
        with open(self.settings, 'w') as s:
            s.write(
                json.dumps(
                    link_data,
                    indent=4,
                    sort_keys=True))

class MainApp(App):
    def build(self):
        global link_data
        try:
            with open("settings.json", "r") as file:
                file.close()
        except FileNotFoundError:
            with open("settings.json", "w") as file:
                file.write('{}')
        with open("settings.json") as file:
            link_data = json.load(file)
        scr_mng = ScreenManager()
        scr_mng.add_widget(MyLayout(name="screen_one"))
        scr_mng.add_widget(Settings(name="screen_two"))
        scr_mng.add_widget(Favorites(name="favorites"))
        
        scr_mng.current = "screen_one"
        
        #dam=Label(text="WHy", pos_hint={'center_x': .5, 'center_y': .45})
        #return dam

        return scr_mng

if __name__ == '__main__':
    MainApp().run()
