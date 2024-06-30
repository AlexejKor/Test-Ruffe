from kivy.app import App
from kivy.uix.screenmanager import Screen
from kivy.uix.screenmanager import ScreenManager
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.boxlayout import BoxLayout
from kivy.core.window import Window
from instructions import *
from ruffier import *
from seconds import *
from runner import *
from sits import *

pink = (0, .8, 6, 1)
Window.clearcolor = pink
name = ''
age = 0
result1 = 0
result2 = 0
result3 = 0
def check_int(str_num):
    try:
        return int(str_num)
    except:
        return False

class ScreenFirst(Screen):
    def __init__(self,**kwargs):
        super().__init__(**kwargs)
#        self.clearcolor = (1, .5, .6, 1)
        VBL = BoxLayout(orientation = 'vertical', padding=8, spacing=8)
        GBL1 = BoxLayout(size_hint=(0.8, 0.2))
        GBL2 = BoxLayout(size_hint=(0.8, 0.2))
        self.INLg = Label(text = txt_instruction, pos_hint={'center_y': 0.9})
        INLi = Label(text = '[color=#FDFFE6]'+'Введите имя:'+'[/color]',markup = True,size_hint=(0.4, 0.2), pos_hint={'left': 0.1})
        INLv = Label(text = 'Введите возраст:',size_hint=(0.4, 0.2), pos_hint={'left': 0.1,'y': 0.5})
        self.TIi = TextInput(multiline=False, size_hint=(0.8, 0.4), pos_hint={'left': 0.8})
        self.TIv = TextInput(multiline=False, size_hint=(0.8, 0.4), pos_hint={'left': 0.8, 'y': 0.5})
        self.BD = Button(text = 'Начать', size_hint=(0.3, 0.1), pos_hint={'center_x': 0.5})
        #self.BD.background_color = (.8, .6, 0, 1)
        GBL1.add_widget(INLi)
        GBL1.add_widget(self.TIi)
        GBL2.add_widget(INLv)
        GBL2.add_widget(self.TIv)
        VBL.add_widget(self.INLg)
        VBL.add_widget(GBL1)
        VBL.add_widget(GBL2)
        VBL.add_widget(self.BD)
        self.add_widget(VBL)
        self.BD.on_press = self.next
    def next(self):
        global name
        global age
        name = self.TIi.text
        age = check_int(self.TIv.text)
        if age == False or age < 7:
            self.INLg.text = 'ВНИМАНИЕ!'+'\n'+'Возраст был не правильно введён.'+'\n'+'Проверьте, он должен быть целым числом, большим либо равным 7.'
        else:
            self.manager.current = 'second'
        
class ScreenSecond(Screen):
    def __init__(self,**kwargs):
        super().__init__(**kwargs)
        self.next_screen = False
        VBL = BoxLayout(orientation = 'vertical', padding=8, spacing=8)
        GBL1 = BoxLayout()
        GBL2 = BoxLayout(size_hint=(0.8, 0.2))
        self.INLi = Label(text = txt_test1, pos_hint={'center_y': 0.5})
        INLr = Label(text = 'Введите результат:', size_hint=(0.3, 0.2), pos_hint={'left': 0.1, 'y': 0.65} )
        self.TIr = TextInput(multiline=False, size_hint=(0.5, 0.6), pos_hint={'left': 0.8, 'y': 0.55})
        self.BD = Button(text = 'Начать', size_hint=(0.3, 0.1), pos_hint={'center_x': 0.5})
        self.L_sec = Seconds(2)
        self.L_sec.bind(done = self.sec_finished)
        GBL1.add_widget(self.INLi)
        GBL2.add_widget(INLr)
        GBL2.add_widget(self.TIr)
        VBL.add_widget(GBL1)
        VBL.add_widget(self.L_sec)
        VBL.add_widget(GBL2)
        VBL.add_widget(self.BD)
        self.add_widget(VBL)
        self.BD.on_press = self.next
    def sec_finished(self, *args):
        self.TIr.set_disabled(False)
        self.BD.set_disabled(False)
        self.BD.text = 'Продолжить'
        self.next_screen = True
    def next(self):
        if not self.next_screen:
            self.BD.set_disabled(True)
            self.TIr.set_disabled(True)
            self.L_sec.start()
        else:
            global result1
            result1 = check_int(self.TIr.text)
            if result1 == False or result1 <= 0:
                self.INLi.text = 'Замерьте пульс за 15 секунд.\n \n Возникла ошибка ввода. Проверьте, верно ли был введён результат.'
            else:
                self.manager.current = 'third'

class ScreenThird(Screen):
    def __init__(self,**kwargs):
        super().__init__(**kwargs)
        self.next_screen = False
        self.L_sits = Sits(3)
        self.run = Runner(total = 3, steptime = 1.5, size_hint = (0.4, 1))
        self.run.bind(finished = self.finished)
        VBL = BoxLayout(orientation = 'vertical', padding=8, spacing=8)
        INL = Label(text = txt_sits ,pos_hint={'center_y': 0.5})
        self.BD = Button(text = 'Продолжить', size_hint=(0.3, 0.1), pos_hint={'center_x': 0.5})
        VBL.add_widget(INL)
        VBL.add_widget(self.L_sits)
        VBL.add_widget(self.run)
        VBL.add_widget(self.BD)
        self.add_widget(VBL)
        self.BD.on_press = self.next
    def finished(self, instance, valeu):
        self.BD.set_disabled(False)
        self.BD.text = 'Продолжить'
        self.next_screen = True
    def next(self):
        if not self.next_screen:
            self.BD.set_disabled(True)
            self.run.start()
            self.run.bind(value = self.L_sits.next)
        else:
            self.manager.current = 'fourth'

class ScreenFourth(Screen):
    def __init__(self,**kwargs):
        super().__init__(**kwargs)
        self.stage = 0
        self.next_screen = False
        self.L_sec = Seconds(2)
        self.L_sec.bind(done = self.seс_finished)
        VBLg = BoxLayout(orientation = 'vertical', padding=8, spacing=8)
        GBL1 = BoxLayout(size_hint=(0.8, 0.2))
        GBL2 = BoxLayout(size_hint=(0.8, 0.2))
        self.INLo = Label(text = 'Считайте пульс',pos_hint={'center_y': 0.5})
        self.INLg = Label(text = txt_test3 ,pos_hint={'center_y': 0.5})
        INL1 = Label(text = 'Результат:', size_hint=(0.3, 0.3), pos_hint={'left': 0.1, 'y': 0.58} )
        INL2 = Label(text = 'Результат после отдыха:',size_hint=(0.4, 0.3), pos_hint={'left': 0.1,'y': 0.5})
        self.TI1 = TextInput(multiline=False, size_hint=(0.5, 0.9), pos_hint={'left': 0.8, 'y': 0.55})
        self.TI2 = TextInput(multiline=False, size_hint=(0.5, 0.9), pos_hint={'left': 0.8, 'y': 0.55})
        self.BD = Button(text = 'Начать', size_hint=(0.3, 0.1), pos_hint={'center_x': 0.5})
        VBLg.add_widget(self.INLg)
        GBL1.add_widget(INL1)
        GBL1.add_widget(self.TI1)
        GBL2.add_widget(INL2)
        GBL2.add_widget(self.TI2)
        VBLg.add_widget(self.INLo)
        VBLg.add_widget(self.L_sec)
        VBLg.add_widget(GBL1)
        VBLg.add_widget(GBL2)
        VBLg.add_widget(self.BD)
        self.add_widget(VBLg)
        self.BD.on_press = self.next
        self.TI1.set_disabled(True)
        self.TI2.set_disabled(True)
    def seс_finished(self, *args):
        if self.L_sec.done:
            if self.stage == 0:
                self.stage = 1
                self.L_sec.restart(3)
                self.TI1.set_disabled(False)
                self.INLo.text = 'Отдыхайте'
            elif self.stage == 1:
                self.stage = 2
                self.L_sec.restart(2)
                self.INLo.text = 'Считайте пульс'
            elif self.stage == 2:
                self.TI2.set_disabled(False)
                self.BD.set_disabled(False)
                self.BD.text = 'Завершить'
                self.next_screen = True
    def next(self):
        if not self.next_screen:
            self.BD.set_disabled(True)
            self.L_sec.start()
        else:
            global result2
            global result3
            result2 = check_int(self.TI1.text)
            result3 = check_int(self.TI2.text)
            if result2 == False or result2 <= 0 or result3 == False or result3 <= 0:
                self.INLg.text = 'В течение минуты замерьте пульс два раза:\n за первые 15 секунд минуты, затем за последние 15 секунд.\nВозникла ошибка ввода.\nПроверьте, верно ли введён результат.'
            else:
                self.manager.current = 'fifth'

class ScreenFifth(Screen):
    def __init__(self,**kwargs):
        super().__init__(**kwargs)
        VBL = BoxLayout()
        self.INL = Label(text = '')
        VBL.add_widget(self.INL)
        self.add_widget(VBL)
        self.on_enter = self.before
    def before(self):
        global name
        self.INL.text = name + '\n'+ test(result1,result2,result3,age)

class TestRuff(App):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(ScreenFirst(name = 'first'))
        sm.add_widget(ScreenSecond(name = 'second'))
        sm.add_widget(ScreenThird(name = 'third'))
        sm.add_widget(ScreenFourth(name = 'fourth'))
        sm.add_widget(ScreenFifth(name = 'fifth'))
        return sm
app = TestRuff()
app.run()