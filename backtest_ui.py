from threading import Thread

from kivy.app import App
from kivy.uix.widget import Widget
from kivy.properties import ObjectProperty, Clock, StringProperty
from kivy.lang import Builder

# Designate Our .kv design file
from backtest import TestRun
from multiprocessing import Process, Pipe

# Builder.load_file('backtest_ui_scene.kv')

kv = '''
MyLayout:
    target: target

    BoxLayout:
        orientation: 'vertical'
        size: root.width, root.height

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
    txt = StringProperty('Text will be changed')
    btn_txt = StringProperty('Start')
    tst = TestRun()

    # child_conn = Pipe()
    # process = Process(target=tst.test_run_con, args=(child_conn,))

    thread = Thread(target=tst.test_run)
    thread.daemon = True

    def click(self):
        if self.tst.is_running == 0:
            self.txt = 'Starting'
            self.btn_txt = 'Stop'
            # self.process.start()
            self.thread.start()
            Clock.schedule_interval(self.update_text, 0.2)
        else:
            self.txt = 'Stopped'
            self.btn_txt = 'Start'

    def update_text(self, dt):
        self.txt = self.tst.status


class AwesomeApp(App):
    def build(self):
        return Builder.load_string(kv)


if __name__ == '__main__':
    AwesomeApp().run()
