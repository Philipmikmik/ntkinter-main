#import ssl
from kivy.app import App
from kivy.core.clipboard import Clipboard
from kivy.network.urlrequest import UrlRequest
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.image import AsyncImage
from kivy.uix.textinput import TextInput
from kivy.properties import StringProperty
import json
from time import sleep
#ssl._create_default_https_context = ssl._create_unverified_context
started = 0
slide = 0
loaded = True
UrlRequest("https://ntkinter-api.herokuapp.com/json/")
def formating(string):
    if string == '':
        return "None"
    else:
        string.replace(" ","%20")
        return string
class MyLayout(Screen):
    def press(self):
        global loaded
        if loaded:
            loaded = False
            st = Settings()
            data1 = formating(st.ids.inputEX.text)
            data2 = formating(st.ids.inputIN.text)
            UrlRequest("https://ntkinter-api.herokuapp.com/json/?exc="+data1+"&inc="+data2, self.rand)
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
        tt = 0
        backup = result['img']
        for i in range(len(result['tags']) - 1):
            tags = tags + str(result['tags'][i]) + ", "
        tags = tags[:-2]
        autor = result['author']
        autor.append("Not defined")
        self.ids.title.text = "Title: " + result['title']
        self.ids.author.text = "Author: " + autor[0]
        self.ids.tags.text = "Tags: " + tags
        self.ids.clip.text = str(result['id'])
        if len(result['img']) < 4:
            for i in range(len(result['img']) - 1):
                src = result['img'][i]
                image = AsyncImage(source=src)
                self.ids.my_carousel.add_widget(image)
        else:
            for i in range (4):
                src = result['img'][0]
                image = AsyncImage(source=src)
                self.ids.my_carousel.add_widget(image)
                backup.pop(0)
                load = 4
        self.do_layout()
        slide = 0
        howmany = str(len(result['img'])+4)
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
                if slide != (self.ids.my_carousel.index+1):
                    self.ids.pages.text = str(self.ids.my_carousel.index+1)+"/"+howmany
            if (self.ids.my_carousel.index+4)>load:
                if 0 != len(backup):
                    src = backup[0]
                    image = AsyncImage(source=src)
                    self.ids.my_carousel.add_widget(image)
                    backup.pop(0)
                    load += 1
class Settings(Screen):
    def prit(self):
        with open("settings.json", "w") as file:
            exclusions = self.ids.inputEX.text
            inclusions = self.ids.inputIN.text
            inpdict = {"exclusions": exclusions, "inclusions": inclusions}
            json.dump(inpdict, file)
    pass

class LinkEditor(TextInput):
    in_ex = StringProperty('')

    def on_kv_post(self, *largs):
        with open("settings.json") as file:
            data = json.load(file)
            self.text = data.get(self.in_ex, "")

class MainApp(App):
    def build(self):
        try:
            with open("settings.json", "r") as file:
                file.close()
        except FileNotFoundError:
            with open("settings.json", "w") as file:
                file.write('{}')
        scr_mng = ScreenManager()
        scr_mng.add_widget(MyLayout(name="screen_one"))
        scr_mng.add_widget(Settings(name="screen_two"))
        return scr_mng
if __name__ == '__main__':
    MainApp().run()
