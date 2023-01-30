import subprocess
import shlex
import time
import pprint as pp
class SubprocessObj:
    def __init__(self, name, data={}):
        print('SubprocessObj!')
        self.name = name
        self.data = data
        self.data.update({self.name: []})
        self.start_line = 0
        self.process = None

    def k_func(self, str_config, v_val):
        bol_config = False
        if str_config == 'True':
            bol_config = True
        elif str_config == 'False':
            bol_config = False
        elif str_config == 'open':
            bol_config = False
            self.subprocess = subprocess
            self.process = self.subprocess.Popen(shlex.split(v_val),
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE)
            while True:
                output = self.process.stdout.readline().decode("utf-8")
                if len(output) < 1:
                    break
                if output == '' and self.process.poll() is not None:
                    break
                if output:
                    # print(output.strip())                    
                    self.data[self.name].append(output.strip())
            rc = self.process.poll()
            return rc

        else:
            print('str_config: ' + str_config)
            print('self.start_line: ' + str(self.start_line))
            print('current_output: ')
            print('\n'.join(self.data[self.name][:-1]))
            if str_config in '\n'.join(self.data[self.name][:-1]) :
                bol_config = True
            
            self.start_line = len(self.data[self.name])            
            print('self.start_line2: ' + str(self.start_line))

        return bol_config

    def v_func(self, v_val):
        print('v_func: ' + v_val)
        self.my_send_wait_recieve(v_val)
        # self.data[self.name].append({v_val:output})
        return True
    
    def my_send_wait_recieve(self, send_var=''):
        send_str = send_var+'\n'
        print('self.io.write:'+send_str)
        # self.io.send(send_str)   
        self.process = self.subprocess.Popen(shlex.split(send_str), stdout=subprocess.PIPE)  
        # self.process.stdin.write(bytes(send_str, 'utf-8'))
        # time.sleep(5)
        print('#' * 44 + "Sending:" + send_var)
        # while True:
        #     print('while')
        #     if self.io.recv_ready():
        #         self.data[self.name].append(self.io.recv(65535).decode())                
        #         break
        while True:
            output = self.process.stdout.readline().decode("utf-8")
            if len(output) < 1:
                break
            if output == '' and self.process.poll() is not None:
                break
            if output:
                # print(output.strip())                    
                self.data[self.name].append(output.strip())
        rc = self.process.poll()
        return rc
            
if __name__ == "__main__":
    data = {}
    s = SubprocessObj('test', data)
    s.k_func("open","git -C C:/Users/paglipay/Documents/Projects/rancid/node-feedback-loop pull origin main")
    pp.pprint('data: ')
    pp.pprint(data)
    # s.k_func("open","dir")
    # pp.pprint('data: ')
    # pp.pprint(data)
