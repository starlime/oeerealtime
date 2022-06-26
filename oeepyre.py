from numpy import double
import pyrebase
import requests, json
import threading

interval = 5

config = {
  "apiKey": "AIzaSyCRBdKqw53VdK0y-9KZy1qcLUJHNywLP0k",
  "authDomain": "nodemcu-01-818e1.firebaseapp.com",
  "databaseURL": "https://nodemcu-01-818e1-default-rtdb.firebaseio.com",
  "projectId": "nodemcu-01-818e1",  
  "storageBucket": "nodemcu-01-818e1.appspot.com"
}

firebase = pyrebase.initialize_app(config)

db=firebase.database()

def dataIoT(): 
#dari arduino
    count=db.child('RealtimeOEE').child('countOUT').get()
    cval=count.val()
    db.child("RtOEEComponent").child("TPc").set(cval)

    url = requests.get('https://nodemcu-01-818e1-default-rtdb.firebaseio.com/Hisrrr.json')
    text = url.text
    data = json.loads(text)
    sum = 0
# iterating key value pair
    for key ,value in data.items():
    
        if value and '0' in value.keys():
            # Adding value of sharpness to sum
            sum += value['0']
    #set ke rtoeecomponent
    db.child("RtOEEComponent").child("OTc").set(sum)

def dataOEE(): 
    #ambil data
    ict=db.child('RtOEEComponent').child('ICTc').get()
    ot=db.child('RtOEEComponent').child('OTc').get()
    pot=db.child('RtOEEComponent').child('POTc').get()
    defect=db.child('RtOEEComponent').child('defc').get()
    tp=db.child('RtOEEComponent').child('TPc').get()

    ictval = ict.val()
    otval = ot.val()
    potval = pot.val()
    defval = defect.val()
    tpval = tp.val()

    #hitungannya
    gp = tpval - defval
    Pe = ((ictval*tpval) / otval)*100
    Av = (otval / (potval*3600))*100
    Ql = (gp/tpval)*100
    Oee = (Pe * Av * Ql)/10000

    db.child("RtOEEComponent").child("GPc").set(gp)
    db.child("RtOEECalculation").child("AVc").set(Av)
    db.child("RtOEECalculation").child("PEc").set(Pe)
    db.child("RtOEECalculation").child("QLc").set(Ql)
    db.child("RtOEECalculation").child("OEEc").set(Oee)

def historicaldata1():
    pathy4=db.child('RealtimeOEE').child('waktuOUT').get()
    oee=db.child('RtOEECalculation').child('OEEc').get()
    pr=db.child('RtOEECalculation').child('PEc').get()
    ql=db.child('RtOEECalculation').child('QLc').get()
    av=db.child('RtOEECalculation').child('AVc').get()
    pot=db.child('RtOEEComponent').child('POTc').get()
    ot=db.child('RtOEEComponent').child('OTc').get()
    ict=db.child('RtOEEComponent').child('ICTc').get()
    gp=db.child('RtOEEComponent').child('gp').get()
    tp=db.child('RtOEEComponent').child('tp').get()
    defc= db.child('RtOEEComponent').child('tp').get()
    waktuu=pathy4.val()
    Oee=oee.val()
    Pr=pr.val()
    Ql=ql.val()
    Av=av.val()
    Pot=pot.val()
    Ot=ot.val()
    Ict=ict.val()
    Gp=gp.val()
    Tp=tp.val()
    df=defc.val()
    waktuus= str(''.join(waktuu))
    oees= str (''.join(Oee))
    prs= str (''.join(Pr))
    qls= str (''.join(Ql))
    avs= str (''.join(Av))
    pots= str (''.join(Pot))
    ots= str (''.join(Ot))
    icts= str (''.join(Ict))
    gps= str (''.join(Gp))
    tps= str (''.join(Tp))
    dfs= str(''.join(df) )
    db.child("HistOEEall").push({"waktu2":waktuus, "pot1":pots, "ot1":ots, "ict1":icts, "gp1":gps, "tp1":tps , "oee1":oees, "pr1":prs, "ql":qls, "av":avs, "defect":dfs})

def historicaldata2():
    waktur=db.child('RealtimeOEE').child('waktuOUT').get()
    sk = db.child('RealtimeARM').child('SK').get()
    a = db.child('ARMcomp').child('defA').get()
    b = db.child('ARMcomp').child('defB').get()
    c = db.child('ARMcomp').child('defC').get()
    bd = db.child('ARMcomp').child('breakdown').get()
    oeer=db.child('RtOEECalculation').child('OEEc').get()
    prr=db.child('RtOEECalculation').child('PEc').get()
    qlr=db.child('RtOEECalculation').child('QLc').get()
    avr=db.child('RtOEECalculation').child('AVc').get()
    wkt=waktur.val()
    skk=sk.val()
    aa=a.val()
    bb=b.val()
    cc=c.val()
    bdv=bd.val()
    oe=oeer.val()
    prt=prr.val()
    qlt=qlr.val()
    avt=avr.val()
    wkts= str (''.join(wkt))
    sks= str (''.join(skk))
    ast= str (''.join(aa))
    bst= str (''.join(bb))
    cst= str (''.join(cc))
    bdst = str (''.join(bdv))
    oest= str (''.join(oe))
    prst= str (''.join(prt))
    qlst= str (''.join(qlt))
    avst= str (''.join(avt))
    db.child("HistARMall").push({"waktuARM":wkts, "sarankp":sks, "defcA":ast, "defcB":bst, "defcC":cst,"breakdown1":bdst ,"OEEarm":oest , "PRarm":prst, "QLarm":qlst, "AVarm":avst})


def startTimer():
    threading.Timer(interval, startTimer).start()
    dataIoT() 
    dataOEE()
    historicaldata1()
    historicaldata2()

startTimer()    