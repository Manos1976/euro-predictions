from kivy.app import App
from kivy.uix.label import Label

class EuroPredictionsApp(App):
    def build(self):
        return Label(text="Euro Football Predictions\n(App Ready!)", font_size='20sp')

if __name__ == '__main__':
    EuroPredictionsApp().run()
  
