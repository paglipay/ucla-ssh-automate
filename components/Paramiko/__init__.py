import paramiko
import time
import os, sys
import io

class Paramiko:
    def __init__(self, name, data={}):
        print('ParamikoObj!')
        self.name = name
        self.data = data
        self.data.update({self.name: ['START']})
        self.start_line = 0
        self.ready_prompt = ':~$'
        self.wait = 0
        self.data['prompt_request'] = []
        self.data['sending'] = []

    def k_func(self, str_config, v_val):
        bol_config = False
        if str_config == 'True':
            bol_config = True
        elif str_config == 'False':
            bol_config = False
        elif str_config == 'kill':
            print('kill: ', v_val)
            bol_config = False
            self.io.close()
        elif str_config == 'wait':
            print('wait: ', v_val)
            self.wait = v_val
            print('self.wait: ', self.wait)
            bol_config = False
        elif str_config == 'return':
            print('return')
            print(v_val)
            if v_val == 'True':
                b_val = True
            elif v_val == 'False':
                b_val = False
            else:
                if "not'" in v_val:
                    v_val = v_val.replace("not'", "")
                    b_val = False
                    try:
                        prop = getattr(self, v_val)
                        if prop == None:
                            b_val = True
                    except:
                        print('getattr error')
                else:
                    b_val = True
                    try:
                        prop = getattr(self, v_val)
                        if prop == None:
                            b_val = False
                    except:
                        print('getattr error')
            print(b_val)
            self.bol = b_val
            bol_config = False
        elif str_config == 'prompt':            
            bol_config = False
            print('prompt: ', v_val, self.data)
            self.data['prompt_request'].append(v_val)
            prompt_out = ''
            if v_val in self.data:
                print('prompt: ', v_val)
                waiting_count = 0
                while True:
                    if self.data[v_val]:
                        if self.data[v_val][0] == '':
                            del self.data[v_val][0]
                        elif self.data[v_val][0] != '':
                            prompt_out = self.data[v_val][0]
                            del self.data[v_val][0]
                            waiting_count = 0
                            break

                    time.sleep(1)
                    print('waiting for input: ' + v_val + ' count: ' + str(waiting_count))
                    if waiting_count > 60:
                        # sys.exit(-1)                        
                        self.data['prompt_request'].remove(v_val)
                        break
                    waiting_count += 1
            
            self.data['prompt_request'].remove(v_val)
            self.v_func(prompt_out)

        elif str_config == 'open':
            bol_config = False
            port = 22
            if 'port' in v_val:
                port = v_val['port']
            
            remote_conn_pre = paramiko.SSHClient()
            remote_conn_pre.set_missing_host_key_policy(
                paramiko.AutoAddPolicy())
            remote_conn_pre.connect(v_val['ip'], username=v_val['username'], password=v_val['password'], port=port, look_for_keys=False,
                                    allow_agent=False)
            print("SSH connection established to %s" % v_val['ip'])

            self.io = remote_conn_pre.invoke_shell(width=5000, height=800)
            self.data[self.name].append('GO')
            self.io.send("\n\n") 

        else:            
            bol_config = False
            print('str_config: ' + str_config)
            print('current_output: ')
            print(self.data[self.name][-1])
            
            if "not'" in str_config:
                str_config = str_config.replace("not'","")
                if str_config in self.data[self.name][-1]:
                    bol_config = False
                else:
                    bol_config = True
            else:
                if str_config in self.data[self.name][-1] :
                    bol_config = True            
                    self.start_line = len(self.data[self.name]) 

        return bol_config

    def v_func(self, v_val):
        print('v_func: ' + v_val)
        output = self.my_send_wait_recieve(v_val)
        return True
    
    def my_send_wait_recieve(self, send_var=''):
        
        send_str = send_var+'\n'
        print('self.io.write:'+send_str)
        self.io.send(send_str)    
        print('time.sleep(self.wait): ', self.wait) 
        self_wait = self.wait  

        time.sleep(self_wait)
        print('#' * 44 + "Sending:" + send_var)
        send_rec = {"send": send_var}

        while_count = 0
        while True:       
            if while_count >= 100:
                break
            time.sleep(.5)
            while_count += 1
            print('while: ', while_count, flush=True)
            if self.io.recv_ready(): 
                self.data[self.name].append(self.io.recv(65535).decode())                

                while_count = 0
                if self.data[self.name][-1].split('\n')[-1].strip() != '':
                    break


            if 'logout' in self.data[self.name][-1]:                
                print('while break')              
                break
        
        # send_rec["recv"] = self.data[self.name][-1].split('\n')[-1]
        send_rec["recv"] = self.data[self.name][-1]
        self.data['sending'].append(send_rec)
        return send_rec["recv"]
