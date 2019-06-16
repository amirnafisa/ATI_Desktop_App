import os
import time

def set_app_title(master, title):
    master.winfo_toplevel().title(title)

def get_file_name():
    dirName = './saved_sessions'
    if not os.path.exists(dirName):
        os.mkdir(dirName)
    title = os.path.join(dirName,'session')
    return title+'_'+time.strftime("%Y%m%d-%H%M%S")+'.txt'
