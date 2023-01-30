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
        self.data['prompt_request'] = []
        self.data['sending'] = []

    def k_func(self, str_config, v_val):
        bol_config = False
        if str_config == 'True':
            bol_config = True
        elif str_config == 'False':
            bol_config = False
        elif str_config == 'open':
            bol_config = False
            self.subprocess = subprocess
            self.process = self.start(v_val)

        else:            
            bol_config = False
            print('str_config: ' + str_config)
            
            if "checknot'" in str_config:
                str_config = str_config.replace("checknot'","")
                if str_config in ''.join(self.data[self.name][self.start_line:]) :
                    bol_config = False
                else:
                    bol_config = True
            elif "not'" in str_config:
                str_config = str_config.replace("not'","")
                if str_config in ''.join(self.data[self.name][self.start_line:]) :
                    bol_config = False
                else:
                    bol_config = True
                self.start_line = len(self.data[self.name]) 
            elif "check'" in str_config:
                str_config = str_config.replace("check'","")
                if str_config in ''.join(self.data[self.name][self.start_line:]) :
                    bol_config = True  
            else:
                if str_config in ''.join(self.data[self.name][self.start_line:]) :
                    bol_config = True            
                self.start_line = len(self.data[self.name]) 

        return bol_config

    def v_func(self, v_val, line_count=100):
        print('v_func: ' + v_val)
        if v_val == 'end':
            self.terminate(self.process)
            print('ENDED')
        else:
            self.my_send_wait_recieve(v_val, line_count)
        return True
    
    def my_send_wait_recieve(self, send_var='', line_count=100):
        send_str = send_var+'\n'
        print('self.io.write:'+send_str)
        self.write(self.process, send_str)    
        # print('time.sleep(self.wait): ', self.wait) 
        # self_wait = self.wait  

        # time.sleep(self_wait)
        print('#' * 44 + "Sending:" + send_var)
        send_rec = {"send": send_var}

        self.read(self.process, line_count)
        # while_count = 0
        # while True:       
        #     if while_count >= 100:
        #         break
        #     time.sleep(.5)
        #     while_count += 1
        #     print('while: ', while_count, flush=True)
        #     self.read(self.process)


        #     if 'logout' in self.data[self.name][-1]:                
        #         print('while break')              
        #         break
        
        # send_rec["recv"] = self.data[self.name][-1].split('\n')[-1]
        # send_rec["recv"] = self.data[self.name][-1]
        send_rec["recv"] = self.data[self.name][self.start_line:]
        self.data['sending'].append(send_rec)
        return send_rec["recv"]
    
    
    def start(self,executable_file):
        return subprocess.Popen(
            executable_file,
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE)


    def read(self, process, line_count=100):
        # return process.stdout.readline().decode("utf-8").strip()
        # while True:
        for i in range(line_count):
            output = process.stdout.readline().decode("utf-8")
            if len(output) < 1:
                break
            # if '' == output.strip() :
            #     break
            if '' == output and process.poll() is not None:
                break
            if output:
                print(output.strip())                    
                self.data[self.name].append(output.strip())
        rc = process.poll()
        return rc


    def write(self,process, message):
        process.stdin.write(f"{message.strip()}\n".encode("utf-8"))
        process.stdin.flush()


    def terminate(self,process):
        print('terminate')
        process.stdin.close()
        process.terminate()
        process.wait(timeout=0.2)
                
if __name__ == "__main__":
    data = {}
    s = SubprocessObj('test', data)
    # s.k_func("open","python -V")
    # s.v_func("")
    # s.k_func("open","ping 8.8.8.8")
    # s.v_func("")
    # s.k_func("open","ping 9.9.9.9")
    # s.v_func("")
    
    # s.k_func("open","cmd")
    # # s.v_func("")
    
    # s.v_func("python -V", 1)
    # pp.pprint(data)
    
    # s.v_func("ping 8.8.8.8", 13)
    # time.sleep(11)
    # pp.pprint(data)
    
    # s.v_func("ping 9.9.9.9", 12)
    # time.sleep(11)
    # pp.pprint(data)
    
    # s.v_func("exit", 2)
    # # time.sleep(6)
    # pp.pprint(data)
    
    s.k_func("open","python ./dummy.py")
    s.v_func("python", 1)
    time.sleep(3)
    pp.pprint(data)
    s.v_func("print('HELLO')", 1)
    time.sleep(3)
    pp.pprint(data)
    s.v_func("exit()", 1)
    time.sleep(3)
    pp.pprint(data)
    s.v_func("exit", 1)
    time.sleep(3)
    pp.pprint(data)
    
    # s.v_func("python", 1)
    # pp.pprint(data)
    
    # s.v_func("print(\"HI\")", 1)
    # time.sleep(3)
    # pp.pprint(data)
    
    # s.v_func("exit", 1)
    # # time.sleep(6)
    # pp.pprint(data)
    
    # s.k_func("open","cmd")

    # s.v_func("cd \"C:\\Program Files\\ (x86)\\Cisco\\Cisco AnyConnect\\ Secure Mobility Client\\\" && dir", 5)
    # time.sleep(6)
    # pp.pprint(data)
    
    # s.v_func("dir", 14)
    # time.sleep(3)
    # pp.pprint(data)
    
    # # s.v_func("vpncli connect ssl.vpn.ucla.edu", 1)
    # # time.sleep(3)
    # # pp.pprint(data)
    
    # # s.v_func("paglipay", 1)
    # # time.sleep(3)
    # # pp.pprint(data)
    
    # # s.v_func("26559@pa", 1)
    # # time.sleep(3)
    # # pp.pprint(data)
    
    # # s.v_func("y", 1)
    # # time.sleep(3)
    # # pp.pprint(data)
    
    # s.v_func("exit", 1)
    # time.sleep(3)
    # pp.pprint(data)




    
    # s.k_func("open","python ./dummy.py")
    # s.v_func("dir")
    # pp.pprint('data: ')
    # pp.pprint(data)
    # s.v_func("")
    # pp.pprint('data: ')
    # pp.pprint(data)
