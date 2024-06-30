# напиши модуль для подсчета количества приседаний
from kivy.uix.label import Label

class Sits(Label):
    def __init__(self, total, **kwargs):
        self.sits = 0
        self.total_sits = total
        self.current = 0
        my_text = 'Осталось приседаний: ' + str(self.total_sits)
        super().__init__(text = my_text, **kwargs)
    def next(self, *args):
        self.current += 1
        remain = max(0, self.total_sits - self.current)
        self.text = 'Осталось приседаний: ' + str(remain)