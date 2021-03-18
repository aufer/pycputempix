import PySimpleGUIQt as sg
import cputemp as ct

class Win:
    textFormat = ('Arial', '12')
    window = None

    def __init__(self):
        ct.CpuTemper().addListener(self).run()

        output = [
            sg.Text('CPU temp', font=self.textFormat),
            sg.Text('N/A', key='txtTemp', font=self.textFormat),
            sg.Text('°C (60s avg: ', font=self.textFormat),
            sg.Text('N/A', key='txtAvg', font=self.textFormat),
            sg.Text('°C) ', font=self.textFormat),
            sg.Button('EXIT', key='btnClose', button_color=('white', 'darkred'), size=(6, 0.6))
        ]
       
        self.window = sg.Window(title='cpu temp', layout=[output], keep_on_top=True, no_titlebar=True, grab_anywhere=True)

        while True:
            evt, _ = self.window.read()
            if evt in (None, 'Exit', 'btnClose'):
                break

        self.window.close()

    def notify(self, value, avg):
        self.updateField('txtTemp', value)
        self.updateField('txtAvg', avg)
        self.window.refresh()
    
    def updateField(self, key, value):
        el = self.window.FindElement(key)
        if el == None:
            return
        el.update(value)
        
if __name__ == '__main__':
    Win()