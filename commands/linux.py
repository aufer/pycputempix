command = "cat /sys/class/thermal/thermal_zone0/temp"

def parseOutput(output):
    return float(output.decode('utf-8')) / 1000