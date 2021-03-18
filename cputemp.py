import time
import subprocess
import threading
import platform
from statistics import mean
from bcolors import bcolors as c

os = platform.system()
if os == 'Linux':
    from commands.linux import parseOutput, command
elif os == 'Darwin':
    from commands.darwin import parseOutput, command
else:
    print('Operating system not supported (yet)')
    exit(-1)

printValue = False

def runner(listeners, event = None):
    histSize = 2 * 60 # 120 times 0.5s
    history = [None] * histSize
    rundicator = '|'

    rundicatorSymbols = ['|', '/', '\u2013', '\\']

    def getCCode(val):
        return c.WARNING if val > 55 and val <= 69 else c.FAIL if val > 69 else c.OKGREEN

    oStr = "{} CPU temp {}{}{}°C (60s avg: {}{}{}°C)"

    idx = 0
    while True:
        process = subprocess.Popen(command.split(), stdout=subprocess.PIPE)
        output, error = process.communicate()

        if error:
            print("{}{}{}".format(c.FAIL, error, c.ENDC))
            exit(-1)

        output = parseOutput(output)
        history[idx] = output

        idx = 0 if idx == (histSize - 1) else (idx + 1)

        avg = round(mean(list(filter(lambda x: x != None, history))), 1)

        [listener.notify(*[output, avg]) for listener in listeners]
        if len(listeners) == 0 or printValue:
            print(oStr.format(rundicator, getCCode(output), output, c.ENDC, getCCode(avg), round(avg, 2), c.ENDC), end="\r", flush=True)
            rundicator = rundicatorSymbols[idx % 4]
        time.sleep(0.5)

class CpuTemper:
    listeners = []

    def addListener(self, listener):
        self.listeners.append(listener)
        return self

    def run(self):
        threading.Thread(target=runner, args=[self.listeners], daemon=True).start()

    def runStandalone(self):
        printValue = True
        event = threading.Event()
        threading.Thread(target=runner, args=[self.listeners, event], daemon=True).start()

        event.wait()

if __name__ == '__main__':
    CpuTemper().runStandalone()