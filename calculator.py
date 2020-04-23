def showipbit(ipbit):
    result = ""
    for i in range(0, 32):
        result += str(ipbit[i])
        if (i == 7 or i == 15 or i == 23):
            result += "."
    return result

def showip(ip):
        print("{0}.{1}.{2}.{3}".format(ip[0],ip[1],ip[2],ip[3]))


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
    temp[3]+=value
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



# ipmask = input("Nhap IP/n : ")
ipmask = "172.168.0.1/21"

try:

    ip = ipmask.split("/")[0]
    u = ipmask.split("/")[1]
    x = ip.split(".")[0]
    y = ip.split(".")[1]
    z = ip.split(".")[2]
    t = ip.split(".")[3]
    u = int(u)

    ipdec = [int(x),int(y),int(z),int(t)]
    (showip(ipdec))

    ipbit=dec2bit(ipdec)
    print(showipbit(ipbit))
    
    #subnet mask
    smbit = utobit(u)
    showipbit(smbit)

    smdec = bit2dec(smbit)
    showip(smdec)

    #wildcard address
    wcdec = wcdec(smdec)
    showip(wcdec)

    wcbit = dec2bit(wcdec)
    showipbit(wcbit)
    
    #network address
    nadec =nadec(ipdec,smdec)
    showip(nadec)

    nabit = dec2bit(nadec)
    showipbit(nabit)

    #broadcast address
    badec =badec(nadec,smdec)
    showip(badec)

    babit =dec2bit(badec)
    showipbit(babit)


    test = hostmaxdec(badec)
    showip(test)
except Exception as e:
    print(e)
    print("Nhập đàng hoàng bạn eww")