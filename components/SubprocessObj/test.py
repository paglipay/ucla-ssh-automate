import subprocess
import shlex
import time
 
def start(executable_file):
    return subprocess.Popen(
        executable_file,
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE)


def read(process, line_count):
    # return process.stdout.readline().decode("utf-8").strip()
    count = 0
    output = ""
    # while True:
    for i in range(line_count):
        count += 1
        # print('reading')
        if process.poll() is not None:
            break
        # output = process.stdout.readline().decode("utf-8")
        output = process.stdout.readline().decode("utf-8")
        # print('output:', output)
        # print('len output:', len(output))
        if len(output) < 1:
            break
        if output == '' and process.poll() is not None:
            break
        if output:
            print(output.strip())                    
            # data[name].append(output.strip())
    rc = process.poll()
    
    # terminate(process)
    return [rc, count, len(output)]


def write(process, message):
    print('write: ', message)
    process.stdin.write(f"{message.strip()}\n".encode("utf-8"))
    process.stdin.flush()


def terminate(process):
    print('terminate')
    process.stdin.close()
    process.terminate()
    process.wait(timeout=0.2)


process = start(shlex.split("cmd"))
# process = start("python ./dummy.py")
# time.sleep(6)
print('read(process, 4): ', read(process, 3))
write(process, "python -V")
time.sleep(6)
print('read(process, 4): ', read(process, 3))
write(process, "ping 8.8.8.8")
time.sleep(6)
print('read(process, 4): ', read(process, 12))
write(process, "ping 9.9.9.9")
time.sleep(6)
print('read(process, 4): ', read(process, 12))
write(process, "exit")
time.sleep(6)
print('read(process, 4): ', read(process, 3))

# time.sleep(6)
# # write(process, "dir")
# # # write(process, "")
# # print('read(process, 4): ',read(process, 15))

# # time.sleep(6)

# write(process, "ping 8.8.8.8")
# # write(process, "")
# print('read(process, 4): ',read(process, 14))


print('WILL Terminate')
# terminate(process)
print('TERMINATED')