import os

with open('log.txt','rb') as f:
    f.seek(-2,os.SEEK_END)
    while f.read(1) != b'\n':
        f.seek(-2,os.SEEK_CUR)
    line = f.readline().decode()
    print(line)
       
file = open("log.txt",'a')
file.write("\r\n Append test 7")
file.close()
