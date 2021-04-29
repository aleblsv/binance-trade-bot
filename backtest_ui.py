from threading import Thread
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.properties import ObjectProperty, Clock, StringProperty
from kivy.lang import Builder
from backtest import BackTestClass
from math import sin
from kivy_garden.graph import Graph, MeshLinePlot

kv = '''
MyLayout:
    target: target
    
    # 

            
            
    BoxLayout:
        orientation: 'vertical'
        size: root.width, root.height

        Label:
            id: main_title
            text: root.txt2
            font_size: 32
            size_hint: 1, .5
        
        Label:
            size_hint_x: 0.8
            source: root.draw_my_plot() #<=== initial plot placement
        
        Label:
            id: target
            text: root.txt
            font_size: 32
            size_hint: 1, .5

        Button:
            text: root.btn_txt
            font_size: 32
            on_press: root.click()

'''


class MyLayout(Widget):
    target = ObjectProperty(None)
    txt = StringProperty('Press Start Button')
    txt2 = StringProperty('Plotting using graph in Kivy')
    btn_txt = StringProperty('Start')
    tst = BackTestClass()
    first_run = True
    # child_conn = Pipe()
    # process = Process(target=tst.test_run_con, args=(child_conn,))
    thread = Thread(target=tst.test_run)

    def click(self):
        if self.tst.is_running == 0:
            self.tst.is_running = 1
            self.txt = 'Starting'
            self.btn_txt = 'Stop'
            if self.first_run:
                self.first_run = False
                Clock.schedule_interval(self.update_text, 0.2)
                self.thread.start()
            else:
                if not self.thread.is_alive():
                    self.thread = Thread(target=self.tst.test_run)
                    self.thread.start()
        else:
            self.tst.stop = 1

    def update_text(self, dt):
        self.txt = self.tst.status
        if self.tst.is_running == 0:
            self.btn_txt = 'Start'

    def draw_my_plot(self):
        graph = Graph(xlabel='X', ylabel='Y', x_ticks_minor=5,
                      x_ticks_major=25, y_ticks_major=1,
                      y_grid_label=True, x_grid_label=True, padding=5,
                      x_grid=True, y_grid=True, xmin=-0, xmax=100, ymin=-1, ymax=1)
        plot = MeshLinePlot(color=[1, 0, 0, 1])
        plot.points = [(x, sin(x / 10.)) for x in range(0, 101)]
        graph.add_plot(plot)
        self.add_widget(graph, 1)


class BacktestUI(App):
    def build(self):
        return Builder.load_string(kv)


if __name__ == '__main__':
    BacktestUI().run()
