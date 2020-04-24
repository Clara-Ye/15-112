# hw8_spicy.py
# Your name: Clara Ye
# Your andrew id: zixuany
import copy
def rF(p):
    with open(p,"rt")as f:return f.read()
def movieAwards(o):
    r={}
    for a in o:
        m=a[1]
        r[m]=1+r.get(m,0) 
    return r
def friendsOfFriends(fs):
    r={}
    for p in fs:
        fSet,fof=fs[p],set()
        for f in fSet:
            for pfof in fs[f]:
                if(pfof not in fSet)and(pfof!=p):fof.add(pfof)
        r[p] = fof
    return r
def invertDictionary(d):
    r={}
    for k in d:
        v=d[k]
        if(v in r):r[v].add(k)
        else:r[v]=set([k])
    return r
def readDogDataCsvFileInto2dList(y):
    f,L=rF(f"dog-licenses-{y}.csv"),[]
    for l in f.splitlines():L+=[l.split(",")]
    return L
def convert2dListToTable(d):
    l=d[0]
    t=[l]
    for i in range(1,len(d)):
        dr,tr=d[i],{}
        for j in range(len(l)):
            e=dr[j]
            tr[l[j]] = e
        t+=[tr]
    return t
def cLT(l):
    if"Female"in l:return"Female"
    elif"Male"in l:return"Male"
    else:return"Unknown"
def rSC(r):
    for l in r:
        e=r[l]
        if type(e)==str:
            ce=""
            for c in e:
                if(c.isalnum())or(c.isspace()):ce+=c
            r[l]=ce
def cleanData(t):
    for r in t[1:]:
        r["Color"]=r["Color"].lower().split("/")
        r["Breed"]=r["Breed"].title()
        r["LicenseType"]=cLT(r["LicenseType"])
        r["DogName"]=r["DogName"].title()
        r["ExpYear"]=int(r["ExpYear"])
        r["ValidDate"]=int(r["ValidDate"][:4])
        rSC(r)
def getCleanedTable(y):
    d=readDogDataCsvFileInto2dList(y)
    t=convert2dListToTable(d)
    cleanData(t)
    return t
def gLV(t,l):
    vs=set()
    for r in t[1:]:
        v=r[l]
        if l=="Color":
            for c in v:vs.add(c)
        else:vs.add(v)
    return vs
def getValueSets(y):
    t,vSet=getCleanedTable(y),{}
    for l in t[0]:
        vs=gLV(t,l)
        vSet[l]=vs
    return vSet
def gLC(t,l):
    lc={}
    for r in t[1:]:
        v=r[l]
        if l=="Color":
            for c in v:lc[c]=lc.get(c,0)+1
        else:lc[v]=lc.get(v,0)+1
    return lc
def getValueCounts(y):
    vSet,t,vc=getValueSets(y),getCleanedTable(y),{}
    for l in vSet:
        lc=gLC(t,l)
        vc[l]=lc
    return vc
def gMV(vc):
    mv,mc=None,-1
    for v in vc:
        if vc[v]>mc:mv,mc=v,vc[v]
        elif vc[v]==mc:
            if type(mv)==set:mv.add(v)
            else:mv=set([mv,v])
    return mv
def getMostPopularValues(y):
    vc,pv=getValueCounts(y),{}
    for l in vc:
        mv=gMV(vc[l])
        pv[l]=mv
    return pv