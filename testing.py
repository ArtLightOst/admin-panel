from threading import Thread
from subprocess import Popen, PIPE, STDOUT

class MyThread(Thread):
    
    def __init__(self, name, command):
        super().__init__()
        self.last_output = None
        self.name = name
        self.command = command
        self.all_output = []

    def run(self):

        proc =  Popen(self.command, stdout = PIPE, stderr = STDOUT, text = True)

        for line in iter(proc.stdout.readline, ''):
            if line:
                self.last_output = line
                self.all_output.append(line)


example = MyThread(name="Длительная операция", command=["ls", "-la"])

example.start()

while example.is_alive():
    if example.last_output is not None:
        print(example.name + ": " + str(example.last_output))

print(example.all_output)
