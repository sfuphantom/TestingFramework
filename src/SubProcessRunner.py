import os
import subprocess
import platform
import threading

class SubProcessExecution:

    def __init__(self, filepath):
        self.path = filepath
        

    def run_batch_file(self):
        batch_file_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'execPOC.bat'))
        subprocess.Popen(batch_file_path, shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, stdin=subprocess.DEVNULL)

    def run_shell_script(self):
        #shell_script_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'execPOC.sh'))
        subprocess.Popen(['sh', self.path], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, stdin=subprocess.DEVNULL)

    def invoke_runscript(self):
        if platform.system() == 'Windows':
            batch_thread = threading.Thread(target=self.run_batch_file)
            batch_thread.start()
        else:
            shell_thread = threading.Thread(target=self.run_shell_script)
            shell_thread.start()