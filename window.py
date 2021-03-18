import PySimpleGUIQt as sg
import cputemp as ct

class Win:
    oStr = "CPU temp {}°C (60s avg: {}°C)"

    window = None

    def __init__(self):
        c = ct.CpuTemper()
        c.addListener(self)
        c.run()        
        self.window = sg.Window(title='cpu temp', layout=[[sg.Text('N/A', key='txtTemp')]], size=(200,30))

        while True:
            evt, values = self.window.read()
            print(evt, values)

            if evt in (None, 'Exit'):
                break

        self.window.close()

    def notify(self, value, avg):
        self.window.FindElement('txtTemp').update(self.oStr.format(value, avg))
        self.window.refresh()
        
if __name__ == '__main__':
    Win()