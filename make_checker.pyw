import Tkinter as tk
from tkMessageBox import showinfo
import os, sys
from time import time
# init tkinter
root=tk.Tk()
root.title('Kijiji Feed-Checking Script Generator')
w,h = root.winfo_screenwidth(), root.winfo_screenheight()
root.geometry('350x26+{}+{}'.format(w/2,h/2))
# add ui widgets
label = tk.Label(root,text='Enter Kijiji RSS Feed URL :',anchor=tk.E)
label.grid(row=1,column=1,sticky=tk.E)
entry = tk.Entry(root)
entry.grid(row=1,column=2,sticky=tk.E+tk.W)

def make_checker(callback=None):
    global entry
    rss_url = entry.get()
    # make copy of check_updates
    os.chdir(os.path.join(os.getcwd(),'_generic'))
    with open('check_updates.pyw','r') as genfile:
        genlines = genfile.readlines()
    os.chdir(os.path.join(os.getcwd(),'..'))
    # Make directories
    kw=filter(lambda x: x.lower().startswith('keyword'),rss_url.split('&'))[0].split('=')[-1]
    if not os.path.exists(os.path.join(os.getcwd(),kw)):
        os.makedirs(os.path.join(os.getcwd(),kw))
    os.chdir(os.path.join(os.getcwd(),kw))
    # Update the copied generic file with specific info
    with open('check_updates.pyw','w') as out:
        for line in genlines:
            if line.find("rss_url=''") != -1:
                out.write("rss_url='%s'\n"%rss_url)
            else: out.write(line)
    #
    showinfo(title='Success',message='All operations completed successfully')
    sys.exit()
    
button = tk.Button(root,text="Go",command=make_checker)
button.grid(row=1,column=3,sticky=tk.W)

root.columnconfigure(2,weight=1)

if __name__=='__main__':
    tk.mainloop()
