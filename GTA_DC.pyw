#17/8/2020
from pynput.keyboard import Key, Listener
import ctypes, os
#from tkinter import *
import tkinter as tk
from tkinter import filedialog
import subprocess
import ipaddress

win = tk.Tk()
hotkeyOff =Key.page_down
hotkeyOn = Key.page_up
key = []
p= 0
test_m = ''
test_bth_value = tk.IntVar()
E_IP = []
F_IP=[]
F_IP_list =[]
E_IP_list = []
file_path= ''
input=tk.StringVar()


def test_mode():
    stats_Label.config(text='Test Mode', background='blue', fg='white')
    start_btn.config(state='normal')
    test_btn.config(command=stats_Admin)

def stats_Admin():
    if isAdmin() == True:
        stats_Label.config(text= 'START ONLY after GTA Online is fully loaded and all fd are in', bg='yellow', fg='black')
    elif isAdmin() == False:
        stats_Label.config(text='必需以系統管理員身分執行此程式',
         background='red', fg='white')
        #stats_Label.config(text= 'Start ONLY after GTA Online is fully loaded and all fd are in', bg='yellow', fg='black')
        start_btn.config(state="disabled",bg='lightgray')
        firewall_btn.config(state="disabled")
        firewall_Entry.config(state="disabled")
        N_firewall_btn.config(state="disabled")
def isAdmin():
    try:
        is_admin = (os.getuid() == 0)
    except AttributeError:
        is_admin = ctypes.windll.shell32.IsUserAnAdmin() != 0
    return is_admin

def on_press(key):
    if key == hotkeyOff:
        subprocess.call("taskkill /F /IM gta5.exe", shell=True)
        subprocess.call("taskkill /F /IM SocialClubHelper.exe", shell=True)
        subprocess.run('cmd /c "netsh interface set interface' +
         ' name="乙太網路"'+ ' admin=disabled"', shell=True)
        subprocess.run('cmd /c "netsh interface set interface name='+
        "Ethernet"+' admin=disabled"', shell=True)
        KeyLog_ListB.insert(tk.END,'cmd /c "netsh interface set interface'+
        ' name="乙太網路"'+' admin=disabled" shell=True')
        KeyLog_ListB.insert(tk.END, 'NetOff 網絡已關閉'+'\n\n按下 Page Up 以開啟網絡\n\n')
        stats_Label.config(text='Recommand to RESTART this app',
        background='yellow', fg='black')
        KeyLog_ListB.itemconfigure(tk.END, background="red", fg='white')
        KeyLog_ListB.see("end")

    elif key == hotkeyOn:
        subprocess.run('cmd /c "netsh interface set interface'+
        ' name="乙太網路"'+' admin=enabled"', shell=True)
        subprocess.run('cmd /c "netsh interface set interface'+
        ' name="Ethernet"'+' admin=enabled"', shell=True)
        KeyLog_ListB.insert(tk.END,'cmd /c "netsh interface set interface'+
        ' name="乙太網路"'+' admin=enabled" shell=True')
        KeyLog_ListB.insert(tk.END, 'NetOn 網絡已開啟'+
        '\n\n按下 Page Down 以關閉網絡及GTA \n\n')
        KeyLog_ListB.itemconfigure(tk.END, background="green")
        KeyLog_ListB.see("end")
def on_release(key):
    try:
        KeyLog_ListB.insert(tk.END, 'key {0} pressed'.format(key.char))
        KeyLog_ListB.see("end")
    except AttributeError:
        KeyLog_ListB.insert(tk.END, 'special key {0} pressed'.format(key))
        KeyLog_ListB.see("end")
def KeyListen():
    listener = Listener(on_press=on_press,on_release=on_release)
    listener.start()

def stats():
    if test_bth_value.get() == 1:
        stats_Label.config(text='Test Mode', background='blue', fg='white')
    else:
        stats_Label.config(text='按下 Page Down 以關閉網絡及GTA,'
         +'按下 Page Up 以開啟網絡',bg='lightgreen')

def comb_S_R():
    stats()
    KeyListen()
    start_btn.config(state='disabled', bg='gray')

def file_select():
    global file_path
    file_path= str(filedialog.askopenfilenames())
    if 'GTA5.exe' in file_path:
        b = "''(),"
        for char in b:
            file_path = file_path.replace(char,'')
        file_path=file_path.replace('/',"\\")
        KeyLog_ListB.insert(tk.END, file_path)

        if len(F_IP_list) >= 3:
            firewall_btn.config(text='Start server', command=GTA_server, state='normal',bg='lightgreen')
            stats_Label.config(text='Press Start server', background='blue', fg='white')
        else:
            firewall_btn.config(text='Start server', command=GTA_server, state='disabled')
            stats_Label.config(text='Insert 3 IP Address', background='yellow', fg='black')
            firewall_Entry.config(state='normal')
    else:
        stats_Label.config(text='not GTA5.exe! Usually in steamapps\common\Grand Theft Auto V',font=("timesnewroman", 11,'bold'),bg='yellow',fg= 'black')
        KeyLog_ListB.insert(tk.END, file_path)
    #return file_path


def IP_list(event):
    KeyLog_ListB.insert(tk.END, input.get())
    F=(ipaddress.IPv4Address(int(ipaddress.IPv4Address(input.get()))-1))
    global F_IP_list
    F_IP.append(str(F))
    F_IP_list = list(set(F_IP))
    F_IP_list.sort()

    E=(ipaddress.IPv4Address(int(ipaddress.IPv4Address(input.get()))+1))
    global E_IP_list
    E_IP.append(str(E))
    E_IP_list = list(set(E_IP))
    E_IP_list.sort()
    firewall_Entry.delete(0, 'end')


    if len(F_IP_list) >= 3:
        firewall_Entry.config(state='disabled')
        firewall_btn.config(state='normal')
        #stats_Label.config(text='Select GTA.exe Program Path', bg='blue', fg= 'white')


def GTA_server():
    #stats_Label.config(text='Firewall rule is running',bg='green', fg='black')
    try:
        allowIP = '0.0.0.0-'+F_IP_list[0]+','+E_IP_list[0]+'-'+F_IP_list[1]+','+E_IP_list[1]+'-'+F_IP_list[2]+','+E_IP_list[2]+'-255.255.255.255'
        b = "()"
        for char in b:
            allowIP = allowIP.replace(char,'')
    except BaseException:
        KeyLog_ListB.insert(tk.END, 'Need 3 ip address')
        KeyLog_ListB.itemconfigure(tk.END, bg="red", fg="white")
    os.system('cmd /c "netsh advfirewall firewall delete rule name="GTAPserver""')
    os.system('cmd /c "netsh advfirewall firewall add rule name= "GTAPserver" dir=in action=block program= "'+file_path+'" enable=yes profile=any localport=6672 protocol=udp remoteip= "'+allowIP+'""')
    os.system('cmd /c "netsh advfirewall firewall add rule name= "GTAPserver" dir=out action=block program= "'+file_path+'" enable=yes profile=any localport=6672 protocol=udp remoteip= "'+allowIP+'""')
    stats_Label.config(text='Firewall rule is running', bg='lightgreen', fg='black')
def Normal_server():
    os.system('cmd /c "netsh advfirewall firewall delete rule name="GTAPserver""')
    stats_Label.config(text='Firewall rule deleted', bg='yellow', fg='black')






#windows
win.resizable(0,0)
win.title('GTA DC')
stats_Label = tk.Label(win, height=2, fg='black')
stats_Label.config(font=("timesnewroman", 12,'bold'))
stats_Label.pack(fill='x')
readMe_Label = tk.Label(win,height=1,
text='***RESTART this app after each mission***',bg='lightyellow' )
readMe_Label.pack(side='top', fill='x')
firewall_frm = tk.Frame(win, width=200, height=20)
firewall_Label=tk.Label(firewall_frm, text='2. friends IP:')
firewall_Entry = tk.Entry(firewall_frm,width=20,textvariable=input)
firewall_Entry.bind('<Return>', IP_list)
firewall_Entry.config(state='disabled')
firewall_btn = tk.Button(firewall_frm, text='1. Select Program path',command=file_select)
N_firewall_btn = tk.Button(firewall_frm, text='Normal server', command=Normal_server)
firewall_frm.pack(padx=10)
N_firewall_btn.pack(padx=1, pady=1,side='right')
firewall_btn.pack(padx=1, pady=1,side='right')
firewall_Label.pack(side='left',padx=1)
firewall_Entry.pack(padx=3, pady=1,side='left')

#keylog_listbox
KeyLog_ListB = tk.Listbox(win, width=65, height=10)
KeyLog_ListB.pack()
#button
start_btn = tk.Button(win, text='START GTA DC', command=comb_S_R,
 bg='lightgreen', fg='black')
start_btn.pack(padx=4, pady=5, side='left')
test_btn = tk.Checkbutton(win, text='Test mode', onvalue=1, offvalue=0,
variable=test_bth_value, command=test_mode, state='disabled')
test_btn.pack(padx=1, pady=5, side="right")
#credits
CR = tk.Label(win, text= 'Developed by Terry Ver 0.5')
CR.config(font=("timesnewroman", 8))
CR.pack(padx=80, pady=0, side='right')
#windows


isAdmin()
stats_Admin()
win.mainloop()
