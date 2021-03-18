command = 'sysctl machdep.xcpm.cpu_thermal_level'

def parseOutput(output):
    output = output.decode('utf-8')
    output = output.replace('machdep.xcpm.cpu_thermal_level: ', '')
    return float(output)