# import pywinauto

# from pywinauto.application import Application
# from pywinauto.keyboard import send_keys, KeySequenceError
import time
import serial
# import pyautogui
# import pyperclip

class PuttyObj:
    def __init__(self, int_name, data={}):
        print('__init_'+int_name)
        self.name = int_name
        self.app = None
        self.bol = None
        self.wait = 0
        self.data = data
        self.data.update({self.name: []})
        self.data['prompt_request'] = []
        self.data['sending'] = []
        self.current_line = 0

    def k_func(self, str_config, v_val):
        if str_config == 'True':
            bol_config = True
        elif str_config == 'wait':
            print('wait: ', v_val)
            self.wait = v_val
            print('self.wait: ', self.wait)
            bol_config = False

        elif str_config == 'open':
            # self.app = Application().start("putty.exe -load "+ v_val, timeout=20)
            # self.app.Putty.maximize()
            # self.app = Application().start('notepad.exe', timeout=10)
            # time.sleep(20)
            self.app = serial.Serial(v_val, 9600, timeout=0)
            self.app.write(bytes('<newline>'.replace('<newline>', '\r\n') +'\r\n', 'utf-8'))
            bol_config = False
        elif str_config == 'close':
            print('close: ', v_val)
            self.app.close()
            bol_config = False

        elif str_config == 'prompt':

            # print('prompt: ', v_val, self.data)
            # self.data['prompt_request'].append(v_val)
            # prompt_out = ''
            # if v_val in self.data:
            #     print('prompt: ', v_val)
            #     waiting_count = 0
            #     while True:
            #         if self.data[v_val]:
            #             if self.data[v_val][0] == '':
            #                 del self.data[v_val][0]
            #             elif self.data[v_val][0] != '':
            #                 prompt_out = self.data[v_val][0]
            #                 del self.data[v_val][0]
            #                 waiting_count = 0
            #                 break

            #         time.sleep(1)
            #         print('waiting for input: ' + v_val + ' count: ' + str(waiting_count))
            #         if waiting_count > 60:
            #             # sys.exit(-1)                        
            #             self.data['prompt_request'].remove(v_val)
            #             break
            #         waiting_count += 1
            
            # self.data['prompt_request'].remove(v_val)
            # self.app.PuTTY.type_keys(prompt_out+'\r\n', with_spaces=True)

            try:
                prompt_out = input(v_val)
            except:
                prompt_out = input('v_val')

            if 'yes'== prompt_out:
                manual_mode = True
                while manual_mode:
                    prompt_out = input('>:')
                    if prompt_out == 'exit':
                        manual_mode = False
                        break
                    # self.app.PuTTY.type_keys(prompt_out + '\r\n', with_spaces=True)
                    self.app.write(bytes(prompt_out.replace('<newline>', '\r\n') +'\r\n', 'utf-8'))

            else:
                # self.app.PuTTY.type_keys(prompt_out+'\r\n', with_spaces=True)
                self.app.write(bytes(prompt_out.replace('<newline>', '\r\n') +'\r\n', 'utf-8'))
                #return False
            bol_config = False
        else:
            bol_config = False
            
            if "checknot'" in str_config:
                str_config = str_config.replace("checknot'","")
                if str_config in ''.join(self.data[self.name][self.current_line:]) :
                    bol_config = False
                else:
                    bol_config = True

            elif "not'" in str_config:
                str_config = str_config.replace("not'","")
                if str_config in ''.join(self.data[self.name][self.current_line:]) :
                    bol_config = False
                else:
                    bol_config = True                
                self.current_line = len(self.data[self.name])

            elif "check'" in str_config:
                str_config = str_config.replace("check'","")
                if str_config in ''.join(self.data[self.name][self.current_line:]) :
                    bol_config = True 

            else:
                if str_config in ''.join(self.data[self.name][self.current_line:]) :
                    bol_config = True
                    self.current_line = len(self.data[self.name])

        return bol_config

    def v_func(self,str_config):
        if str_config == 'break':
            bol_config = False
        elif str_config == '{ESC}':
            self.app.PuTTY.send_keystrokes('{ESC}')
            bol_config = False
        else:
            # self.app.PuTTY.type_keys(str_config+'\r\n', with_spaces=True)
            # pyperclip.copy(str_config.replace('<newline>', '\r\n') +'\r\n')
            # self.app.PuTTY.type_keys('', with_spaces=False)
            # pywinauto.mouse.click(button='right', coords=(100,100))
            # self.app.PuTTY.type_keys(''+'\r\n', with_spaces=True)
            
            # self.app.PuTTY.type_keys(str_config.replace('<newline>', '\r\n') +'\r\n', with_spaces=True)

            self.app.write(bytes(str_config.replace('<newline>', '\n') +'\n', 'utf-8'))
        
        send_rec = {"send": str_config}
        time.sleep(self.wait)
        f_readlines = []
        while 1:
            # try:                
            time.sleep(0)
            str_readline = self.app.readline()
            f_readline = str_readline.decode("utf-8")
            f_readlines.append(f_readline)
            if f_readline == '':
                break
        self.data[self.name] += f_readlines
        print(''.join(f_readlines))

        # self.data[self.name] = f_readlines
        send_rec["recv"] = ''.join(self.data[self.name][self.current_line:])
        # self.current_line = len(self.data[self.name])
        self.data['sending'].append(send_rec)
        # with open('C:\\Users\\paglipay\\Desktop\\putty-out.log') as f:
        #     f_readlines = f.readlines()
        #     print(''.join(f_readlines))
        #     self.data[self.name] = f_readlines
        #     send_rec["recv"] = ''.join(self.data[self.name][self.current_line:])
        #     # self.current_line = len(f_readlines)
        #     self.data['sending'].append(send_rec)
        bol_config = True

        # self.data = {"stuff": "juststuff"}
        return bol_config

if __name__ == "__main__":
    putty = PuttyObj('i')
    putty.k_func('open', '192.168.2.82')