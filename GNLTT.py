from tkinter import Tk, Text, TOP, BOTH, X, N, LEFT, RIGHT, StringVar, END, CENTER,BOTTOM
from tkinter.ttk import Frame, Label, Entry, Button
import ctypes

user32 = ctypes.windll.user32
screensize = user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)
height = 500
width = 400


def sipbit(ipbit):
    result = ""
    for i in range(0, 32):
        result += str(ipbit[i])
        if (i == 7 or i == 15 or i == 23):
            result += "."
    return result

def sip(ip):
    return ("{0}.{1}.{2}.{3}".format(ip[0],ip[1],ip[2],ip[3]))


def bit2dec(ip):
    result = []
    temp1="{0}{1}{2}{3}{4}{5}{6}{7}".format(ip[24],ip[25],ip[26],ip[27],ip[28],ip[29],ip[30],ip[31])
    result.append(int(temp1,2))
    temp2="{0}{1}{2}{3}{4}{5}{6}{7}".format(ip[16],ip[17],ip[18],ip[19],ip[20],ip[21],ip[22],ip[23])
    result.append(int(temp2,2))
    temp3="{0}{1}{2}{3}{4}{5}{6}{7}".format(ip[8],ip[9],ip[10],ip[11],ip[12],ip[13],ip[14],ip[15])
    result.append(int(temp3,2))
    temp4="{0}{1}{2}{3}{4}{5}{6}{7}".format(ip[0],ip[1],ip[2],ip[3],ip[4],ip[5],ip[6],ip[7])
    result.append(int(temp4,2))
    result.reverse()
    return result

def dec2bit(ip):
    ipbit = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
    temp = ip[0]
    for i in range(7,-1,-1):
        ipbit[i] = temp % 2
        temp//=2

    temp = ip[1]
    for i in range(15,7,-1):
        ipbit[i] = temp % 2
        temp//=2

    temp = ip[2]
    for i in range(23,15,-1):
        ipbit[i] = temp % 2
        temp//=2

    temp = ip[3]
    for i in range(31,23,-1):
        ipbit[i] = temp % 2
        temp//=2
    return ipbit

def utobit(u):
    subnetmask = [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]
    for i in range(u,32):
        subnetmask[i] = 0
    return subnetmask
    
def plusipdec(ipdec,value):
    temp = ipdec
    temp[3] = temp[3] + value
    count = 0
    for i in range(3,0,-1):
        if (temp[i] > 255):
            temp[i] = temp[i] % 255
            temp[i-1] = temp[i] + temp[i] // 255
        if (temp[i] < 0):
            count = abs(temp[i])//255 + 1
            temp[i] += count*255
            temp[i-1] -= count
    return temp

def nadec(ipdec,smdec):
    nadec = [0,0,0,0]
    for i in range(0,4):
        nadec[i] = ipdec[i] & smdec[i]
    return nadec

def badec(nadec,smdec):
    badec = [0,0,0,0]
    for i in range(0,4):
        badec[i] = nadec[i] ^ (255-smdec[i])
    return badec

def wcdec(smdec):
    wcdec=[0,0,0,0]
    for i in range(0,4):
        wcdec[i] = 255-smdec[i]
    return wcdec

def hostmindec(nadec):
    hostmindec=nadec
    plusipdec(hostmindec,1)
    return hostmindec

def hostmaxdec(badec):
    hostmaxdec=badec
    plusipdec(hostmaxdec,-1)
    return hostmaxdec



class GNLTT(Frame):
    
    def __init__(self, parent):
        Frame.__init__(self, parent)
        
        self.parent = parent
        self.initUI()

    

    def initUI(self):
        def callback():
            ipmask = etip.get()
            try:
                ip = ipmask.split("/")[0]
                u = ipmask.split("/")[1]
                x = ip.split(".")[0]
                y = ip.split(".")[1]
                z = ip.split(".")[2]
                t = ip.split(".")[3]
                if ( int(x) > 255 or int(y) > 255 or int(z) > 255 or int(t) > 255 ):
                    raise Exception()
                if ( int(x) < 0 or int(y) < 0 or int(z) < 0 or int(t) < 0 ):
                    raise Exception()
                u = int(u)
                if(u < 0 or u > 32):
                    raise Exception()
                #IP
                ipdec = [int(x),int(y),int(z),int(t)]
                ipbit = dec2bit(ipdec)
                
                etipbit.delete(0, END)
                etipbit.insert(0, sipbit(ipbit)+ "\t\t" +sip(ipdec))
                
                #SM
                smbit = utobit(u)
                smdec = bit2dec(smbit)

                etsm.delete(0, END)
                etsm.insert(0,sipbit(smbit) + "\t\t" + sip(smdec) )
                
                #WC
                wcdec1 = wcdec(smdec)
                wcbit = dec2bit(wcdec1)

                etwc.delete(0, END)
                etwc.insert(0, sipbit(wcbit) + "\t\t" + sip(wcdec1))
                
                #NA
                nadec1 =nadec(ipdec,smdec)
                nabit = dec2bit(nadec1)

                etna.delete(0, END)
                etna.insert(0, sipbit(nabit) + "\t\t" + sip(nadec1))

                #BA
                badec1 =badec(nadec1,smdec)
                babit =dec2bit(badec1)

                etba.delete(0, END)
                etba.insert(0, sipbit(babit) + "\t\t" + sip(badec1))             

                #Hmin
                hmindec = hostmindec(nadec1)
                hminbit = dec2bit(hmindec)

                etmin.delete(0, END)
                etmin.insert(0, sipbit(hminbit) + "\t\t" + sip(hmindec)  )

                #Hmax
                hmaxdec1 = hostmaxdec(badec1)
                hmaxbit = dec2bit(hmaxdec1)

                etmax.delete(0, END)
                etmax.insert(0, sipbit(hmaxbit) + "\t\t" + sip(hmaxdec1)  )

                errortext.set("")
            except Exception as e:
                errortext.set("\n\nNhập ngu rồi bạn ơi\nMà cũng có thể là do code mình ngu ^^\nThông cảm nhập input khác nha")
        self.parent.title("GNLTT")
        self.pack(fill=BOTH, expand=True)

        frame1 = Frame(self)
        frame1.pack(fill=X)
        
        
        lbip = Label(frame1, text="IP/u", width=16)
        lbip.pack(side=LEFT, padx=5, pady=5)

        btnsubmit = Button(frame1, text="Submit", command=callback)
        btnsubmit.pack(side=RIGHT, padx=5, pady=5)
        
        etip = Entry(frame1)
        etip.pack(fill=X, padx=5, expand=True)

        frame2 = Frame(self)
        frame2.pack(fill=X)

        lbipbit = Label(frame2, text=">> IP", width=16)
        lbipbit.pack(side=LEFT, padx=5, pady=5)

        etipbit = Entry(frame2)
        etipbit.pack(fill=X, padx=5, expand=True)

        frame3 = Frame(self)
        frame3.pack(fill=X)

        lbsm = Label(frame3, text=">> Netmask", width=16)
        lbsm.pack(side=LEFT, padx=5, pady=5)

        etsm = Entry(frame3)
        etsm.pack(fill=X, padx=5, expand=True)

        frame4 = Frame(self)
        frame4.pack(fill=X)

        lbwc = Label(frame4, text=">> Wildcard", width=16)
        lbwc.pack(side=LEFT, padx=5, pady=5)

        etwc= Entry(frame4)
        etwc.pack(fill=X, padx=5, expand=True)

        frame5 = Frame(self)
        frame5.pack(fill=X)

        lbna = Label(frame5, text=">> Network", width=16)
        lbna.pack(side=LEFT, padx=5, pady=5)

        etna = Entry(frame5)
        etna.pack(fill=X, padx=5, expand=True)

        frame6 = Frame(self)
        frame6.pack(fill=X)

        lbba = Label(frame6, text=">> Broadcast", width=16)
        lbba.pack(side=LEFT, padx=5, pady=5)

        etba = Entry(frame6)
        etba.pack(fill=X, padx=5, expand=True)

        frame7 = Frame(self)
        frame7.pack(fill=X)

        lbhmin = Label(frame7, text=">> HostMin", width=16)
        lbhmin.pack(side=LEFT, padx=5, pady=5)

        etmin = Entry(frame7)
        etmin.pack(fill=X, padx=5, expand=True)

        frame8 = Frame(self)
        frame8.pack(fill=X)

        lbhmax = Label(frame8, text=">> HostMax", width=16)
        lbhmax.pack(side=LEFT, padx=5, pady=5)

        etmax = Entry(frame8)
        etmax.pack(fill=X, padx=5, expand=True)

        frame9 = Frame(self)
        frame9.pack(fill=X)

        errortext = StringVar()
        error = Label(frame9, font=100, textvariable=errortext, width=0,justify=CENTER)
        error.pack(side=TOP, expand=True) 

        frame10 = Frame(self)
        frame10.pack(side=BOTTOM, fill=X)

        infortext = StringVar()
        infor = Label(frame10, font=1, text="code by GioQuy",justify=CENTER)
        infor.pack(side=BOTTOM, padx = 5, pady = 5) 

root = Tk()
root.geometry( "{0}x{1}+{2}+{3}".format(height, width, (screensize[0]//2 - height//2), (screensize[1]//2 - width//2) ))
app = GNLTT(root)
root.mainloop() 