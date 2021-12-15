# import ssl
import json
import sys
import os
from time import sleep
from kivy.app import App
from kivy.core.clipboard import Clipboard
from kivy.network.urlrequest import UrlRequest
from kivy.properties import StringProperty
from kivy.uix.image import AsyncImage
from kivy.core.window import Window
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.uix.textinput import TextInput
from kivy.uix.label import Label
from kivy.lang import Builder

#ssl._create_default_https_context = ssl._create_unverified_context
started = 0
slide = 0
loaded = True
link_data = {}

#Builder.load_file('main.kv')
root_folder = os.path.join(os.path.dirname(sys.argv[0]), 'main.kv')
print(root_folder)


# I wanna kill myself
#Builder.load_string('''
#<MyLayout>
#    FloatLayout:
#        size: (root.width, root.height)
#        orientation: 'vertical'
#        Carousel:
#            id: my_carousel
#            on_touch_up: root.pages()
#            direction: 'right'
#            pos_hint: {'center_x': .5, 'center_y': .46}
#            size_hint: .9, .9
#        Label:
#            id: title
#            pos_hint: {'center_x': .5, 'center_y': .95}
#            size_hint_y: None
#            text_size: self.width, None
#            halign: 'center'
#            height: self.texture_size[1]
#        Label:
#            id: author
#            pos_hint: {'center_x': .5, 'center_y': .92}
#        Label:
#            id: tags
#            halign: 'center'
#            size_hint_y: None
#            text_size: self.width, None
#            height: self.texture_size[1]
#            pos_hint: {'center_x': .5, 'center_y': .87}
#        Label:
#            id: pages
#            pos_hint: {'center_x': .5, 'center_y': .11}
#        Button:
#            pos_hint: {'center_x': .89, 'center_y': .04}
#            on_press: root.press()
#            size_hint: (.06, .06)
#            background_color: .19, .19, .19, 0
#            Image:
#                source: 'icons/random.png'
#                center_x: self.parent.center_x
#                center_y: self.parent.center_y
#        Button:
#            id: clip
#            pos_hint: {'center_x': .1, 'center_y': .04}
#            on_press: root.copy()
#            size_hint: (.06, .06)
#            background_color: .19, .19, .19, 0
#            Image:
#                source: 'icons/clipboard.png'
#                center_x: self.parent.center_x
#                center_y: self.parent.center_y
#        Button:
#            pos_hint: {'center_x': .68, 'center_y': .04}
#            on_press:
#                root.manager.transition.direction = 'left'
#                root.manager.current = 'screen_two'
#            size_hint: (.06, .06)
#            background_color: .19, .19, .19, 0
#            Image:
#                source: 'icons/settings.png'
#                center_x: self.parent.center_x
#                center_y: self.parent.center_y
#        Button:
#            pos_hint: {'center_x': .89, 'center_y': .11}
#            on_press:
#                root.prnt_fvs()
#                root.manager.transition.direction = 'left'
#                root.manager.current = 'favorites'
#            size_hint: (.06, .06)
#            background_color: .19, .19, .19, 0
#            Image:
#                source: 'icons/favourites.png'
#                center_x: self.parent.center_x
#                center_y: self.parent.center_y
#        Button:
#            id: fave
#            on_press: root.faves()
#            pos_hint: {'center_x': .1, 'center_y': .11}
#            size_hint: (.06, .06)
#            background_color: .19, .19, .19, 0
#            Image:
#                source: 'icons/like.png'
#                center_x: self.parent.center_x
#                center_y: self.parent.center_y
#<Settings>:
#    FloatLayout:
#        Button:
#            pos_hint: {'center_x': .14, 'center_y': .92}
#            on_press:
#                root.manager.transition.direction = 'right'
#                root.manager.current = 'screen_one'
#            size_hint: (.06, .06)
#            background_color: .19, .19, .19, 0
#            Image:
#                source: 'icons/back.png'
#                center_x: self.parent.center_x
#                center_y: self.parent.center_y
#        LinkEditor:
#            id: inputEX
#            keyboard_suggestions: False
#            in_ex: 'exclusions'
#            size_hint: (.7, .2)
#            pos_hint: {'center_x': .5, 'center_y': .65}
#        Label:
#            text: "Exclusions"
#            pos_hint: {'center_x': .5, 'center_y': .77}
#        LinkEditor:
#            id: inputIN
#            keyboard_suggestions: False
#            in_ex: 'inclusions'
#            size_hint: (.7, .2)
#            pos_hint: {'center_x': .5, 'center_y': .35}
#        Label:
#            text: "Inclusions"
#            pos_hint: {'center_x': .5, 'center_y': .47}
#<Favorites>
#    FloatLayout:
#        size: (root.width, root.height)
#        orientation: 'vertical'
#        Button:
#            text: "Random"
#            size_hint: (.18, .06)
#            pos_hint: {'center_x': .87, 'center_y': .05}
#            on_press: root.funcse()
#        Button:
#            pos_hint: {'center_x': .14, 'center_y': .92}
#            on_press:
#                root.manager.transition.direction = 'right'
#                root.manager.current = 'screen_one'
#            size_hint: (.06, .06)
#            background_color: .19, .19, .19, 0
#            Image:
#                source: 'icons/back.png'
#                center_x: self.parent.center_x
#                center_y: self.parent.center_y
#        Label:
#            id: title1
#            pos_hint: {'center_x': .3, 'center_y': .81}
#            size_hint_y: None
#            text_size: self.width, None
#            halign: 'center'
#            height: self.texture_size[1]
#        Label:
#            id: title2
#            pos_hint: {'center_x': .7, 'center_y': .81}
#            size_hint_y: None
#            text_size: self.width, None
#            halign: 'center'
#            height: self.texture_size[1]
#        Label:
#            id: title3
#            pos_hint: {'center_x': .3, 'center_y': .41}
#            size_hint_y: None
#            text_size: self.width, None
#            halign: 'center'
#            height: self.texture_size[1]
#
#''')

UrlRequest("https://ntkinter-api.herokuapp.com/json/")
Window.clearcolor = (.19, .19, .19, 1)
Window.size = (500, 890)

def formating(string):
    if string == '':
        return "None"
    else:
        string.replace(" ", "%20")
        return string


class MyLayout(Screen):
    # def build(self):
    #    dam=Label(text="WHy", pos_hint={'center_x': .5, 'center_y': .45})
    #    return dam
    def press(self):
        global loaded
        if loaded:
            loaded = False
            st = Settings()
            data1 = formating(st.ids.inputEX.text)
            data2 = formating(st.ids.inputIN.text)
            UrlRequest(("https://ntkinter-api.herokuapp.com/json/?exc="+data1+"&inc="+data2), self.rand)

    def rand(self, req, result):
        global page, started, yee, slide, loaded, load, backup, howmany, img_0, autor
        img_0 = (result['img'])[0]
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
        tags = tags[:-2]
        autor = result['author']
        autor.append("Not defined")
        self.ids.title.text = result['title']
        self.ids.author.text = "Author: " + autor[0]
        self.ids.tags.text = "Tags: " + tags
        #self.ids.clip.text = str(result['id'])
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
            Clipboard.copy("nhentai.net/g/"+yee['id'])

    def pages(self):
        global load, howmany
        if started == 1:
            for i in range(10):
                if slide != (self.ids.my_carousel.index + 1):
                    self.ids.pages.text = (str(self.ids.my_carousel.index+1)+"/"+str(howmany))
            if (self.ids.my_carousel.index + 4) > load:
                if 0 != len(backup):
                    src = backup[0]
                    image = AsyncImage(source=src)
                    self.ids.my_carousel.add_widget(image)
                    backup.pop(0)
                    load += 1
    def faves(self):
        global file_data,yee,img_0,howmany
        with open("favorite.json") as file:
            file_data = json.load(file)
            file.close()
        if self.ids.my_carousel is None:
            sleep(.1)
        else:
            data = {
                    "title": yee['title'],
                    "img": img_0,
                    "pages": int(howmany)
            }
            file_data[self.ids.clip.text] = data
            with open("favorite.json","w") as f:
                f.write(
                    json.dumps(
                        file_data,
                        indent = 4
                    )
                )
    def prnt_fvs(self):
        with open("favorite.json") as f:
            file = json.load(f)
            for item in file:
                print (file[item])

class Settings(Screen):
    pass


class Favorites(Screen):
    def bruh(self):
        for h in range(2):
            if h == 1:
                dub = -0.1
            else:
                dub = .1
            for i in range(10):
                for j in range(10):
                    b = str(round(j*dub,1))+","+str(round(i*dub,1))
                    ok = Label(text=b, pos_hint={'x': round(j*dub,1), 'y': round(i*dub,1)})
                    Favorites.add_widget(self, ok)
    def funcse(self):
        with open("favorite.json") as file:
            file_data = json.load(file)
            file.close()
        keys = list(file_data)
        titles = [self.ids.title1, self.ids.title2, self.ids.title3]
        for i in range(3):
            titles[i].text= "Title: "+file_data[keys[i]]['title']
        #self.ids.title2.text = "Title: " + file_data[keys[1]]['title']
        #self.ids.title3.text = "Title: " + file_data[keys[2]]['title']


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
        try:
            with open("favorite.json") as file:
                file.close()
        except FileNotFoundError:
            with open("favorite.json", "w") as file:
                file.write('{}')
        scr_mng = ScreenManager()
        scr_mng.add_widget(MyLayout(name="screen_one"))
        scr_mng.add_widget(Settings(name="screen_two"))
        scr_mng.add_widget(Favorites(name="favorites"))

        scr_mng.current = "screen_one"

        # dam=Label(text="WHy", pos_hint={'center_x': .5, 'center_y': .45})
        # return dam

        return scr_mng


if __name__ == '__main__':
    MainApp().run()