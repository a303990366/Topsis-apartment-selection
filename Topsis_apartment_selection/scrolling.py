from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.scrollview import ScrollView
from kivy.core.window import Window
from kivy.app import runTouchApp, App
from kivy.uix.image import Image
from kivy.uix.label import Label
import webbrowser
import pandas as pd
import re
from turn_item_to_score import alter_rent_type_reverse
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.lang import Builder

Window.size = (600, 800)

class scrolling(App):
    #Builder.load_file('scrolling.kv')
    def build(self):
        Window.clearcolor = (249/255, 245/255, 235/255,1)
        layout = GridLayout(cols=2, spacing= 10, size_hint_y=None,padding = 20)
        # Make sure the height is such that there is something to scroll.
        layout.bind(minimum_height=layout.setter('height'))

        df = pd.read_csv('./data/info_scrolling.csv')

        for i in range(50):
            if i<df.shape[0]:
                layout_s = GridLayout(cols=1)
                #this place can replace with dataframe:cost,type,area,equipment
                info = Label(text = 'Cost:{0}'.format(df['price'][i]))
                info1 = Label(text = 'Type:{0}'.format(alter_rent_type_reverse(df['rent type'][i])))
                #info2 = Label(text = 'Area:{0}'.format(df['area'][i]))
                info3 = Label(text = 'Equipment supply rate:{0}%'.format(round(df['equiment'][i]*100,1)))
                info4 = Label(text = 'Location:traffic:  {0},life: {1},education: {2}'.format(df['traffic'][i],df['life'][i],df['education'][i]))
                layout_s.add_widget(info)
                layout_s.add_widget(info1)
                #layout_s.add_widget(info2)
                layout_s.add_widget(info3)
                layout_s.add_widget(info4)

                btn = Button(text='Rank:{0}\nClick me'.format(int(df['rank'][i])),
                             size_hint_y=None, height=150,font_size = 20,size_hint_x=None,width = 150
                             )
                btn.bind(on_press = self.callback)

                
                layout.add_widget(layout_s)
                layout.add_widget(btn)

        root = ScrollView(size_hint=(1, None), size=(Window.width, Window.height))
        root.add_widget(layout)
        return root
    def callback(self,instance):
        pattern = '\d+'
        number = re.search(pattern,instance.text).group()
        print(instance.text,number)
        self.open_b(number)
    def open_b(self,rank):
        df = pd.read_csv('./data/info_scrolling.csv')
        url = self.get_real_url(df['url'][int(rank)-1])
        webbrowser.open(url)
    def get_real_url(self,url):
        pattern = '\d{4,8}'
        house_id = re.search(pattern,url).group()
        
        return "https://rent.591.com.tw/home/"+ house_id
if __name__ == "__main__":
    scrolling().run()
