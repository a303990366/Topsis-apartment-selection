from kivy.core.window import Window
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.widget import Widget
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import ObjectProperty
import numpy as np 
from topsis import run_topsis_and_get_result
from kivy.uix.scrollview import ScrollView
from kivy.app import runTouchApp, App
import webbrowser
import pandas as pd
import re
from turn_item_to_score import alter_rent_type_reverse
from kivy.lang import Builder
from scrolling import scrolling
from kivy.uix.dropdown import DropDown
from kivy.uix.spinner import Spinner
from kivy.lang import Builder
from crawler import house_591
import threading

Window.clearcolor = (249/255, 245/255, 235/255,1)#(1,1,1,1)
Window.size = (600, 800)




class MenuScreen(BoxLayout,Screen):
    def __init__(self,**kwargs):
        self.df = pd.read_csv("./data/town_english.csv")
        super(MenuScreen, self).__init__(**kwargs)
        self.orientation = "vertical"
        grid = GridLayout(cols= 1)
        
        spinner_county = Spinner(
            text='Please choose the county that you want...',
            values=tuple(self.df['county_label_ch'].unique()),
            pos_hint={'center_x': .5, 'center_y': .5}
            )
        spinner_county.bind(text=self.show_selected_value)
        grid.add_widget(spinner_county)

        
        self.spinner_town1 = Spinner(
            # default value shown
            text='Please choose the town that you want',
            pos_hint={'center_x': .5, 'center_y': .5}
        )
        self.spinner_town1.bind(text=self.show_selected_value_town,on_release=self.change_town)
        grid.add_widget(self.spinner_town1)

        self.spinner_town2 = Spinner(
            # default value shown
            text='Please choose the town that you want',
            pos_hint={'center_x': .5, 'center_y': .5}
        )
        self.spinner_town2.bind(text=self.show_selected_value_town,on_release=self.change_town)
        grid.add_widget(self.spinner_town2)

        self.spinner_town3 = Spinner(
            # default value shown
            text='Please choose the town that you want',
            pos_hint={'center_x': .5, 'center_y': .5}
        )
        self.spinner_town3.bind(text=self.show_selected_value_town,on_release=self.change_town)
        grid.add_widget(self.spinner_town3)
        self.add_widget(Label(text = 'Please enter your county and towns'))
        self.add_widget(grid)
        
    def callback_value(self, value):
        print(value.text)
    def show_selected_value(self,spinner, text):
        self.chinese_county = self.df[self.df['county_label_ch']==text]['county_label'].values[0]
        #col: label
        print('The county:', text,self.chinese_county)
    def show_selected_value_town(self,spinner, text):
        self.chinese_town = self.df[(self.df['county_label']==self.chinese_county)&(self.df['label_ch']==text)]['label'].values[0]
        print('The town:', text,self.chinese_town)
    def change_town(self,spinner):
        town_list = tuple(self.df[self.df['county_label']==self.chinese_county]['label_ch'].values)
        spinner.values = town_list
    def collect_town_values(self):

        town1=self.df[self.df['label_ch']==self.spinner_town1.text]['label'].values[0]
        town2=self.df[self.df['label_ch']==self.spinner_town2.text]['label'].values[0]
        town3=self.df[self.df['label_ch']==self.spinner_town3.text]['label'].values[0]
        self.town_list = [town1,town2,town3]
        print(self.town_list,self.chinese_county)
        test = house_591(self.chinese_county,self.town_list)
        test.main()
class Manager(ScreenManager):
     #class SliderWidget(BoxLayout):
     val = ObjectProperty(None)
     val1 = ObjectProperty(None)
     val21 = ObjectProperty(None)
     val22 = ObjectProperty(None)
     val23 = ObjectProperty(None)
     val3 = ObjectProperty(None)
     val4 = ObjectProperty(None)
     val5 = ObjectProperty(None)
     val6 = ObjectProperty(None)
     val7 = ObjectProperty(None)
     county = ObjectProperty(None)
    ##     def get_value(self):
    ##         print("Values:{0}".format(self.val.value))
     def get_button_value(self):
         print("Weight:")
         print("(0) Cost:{0}".format(self.val.value))
         print("(1) Type:{0}".format(self.val1.value))
         print("(2-1) Location-traffic:{0}".format(self.val21.value))
         print("(2-2) Location-life:{0}".format(self.val22.value))
         print("(2-3) Location-education:{0}".format(self.val23.value))
         print("(3) Area:{0}".format(self.val3.value))
         print("(4) Building:{0}".format(self.val4.value))
         print("(5) Equipment:{0}".format(self.val5.value))
         print("(6) Poster:{0}".format(self.val6.value))
         print("(7) Reach/Save:{0}".format(self.val7.value))
         self.val_list = np.array([self.val.value,self.val1.value,self.val21.value,
                              self.val22.value,self.val23.value,self.val3.value,
                              self.val4.value,self.val5.value,self.val6.value,
                              self.val7.value])
         self.produce_rank()
     def produce_rank(self):
         weight = self.val_list/sum(self.val_list)
         print('weight:{0}'.format(weight))
         path = './data/final_591data.csv'
         info = run_topsis_and_get_result(path,weight)
         info.sort_values('rank',inplace =True)
         info.to_csv('./data/info_scrolling.csv',index = False)
         print('Create rank info for each item....')

     def press_c(self):
        print(self.county.text)
##class MyLayout(Widget):
##    def clickNext(self):
##        print('test ok...' )

class MyApp(App):
    def build(self):
        test = Manager()
        return test

if __name__ == '__main__':
    MyApp().run()
    #Builder.unload_file("my.kv")
    #Builder.load_file('scrolling.kv')
    scrolling().run()
