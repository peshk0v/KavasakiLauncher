import shutil

def ad_rp(minedir, rppath, rpFileName):
    rpdir = minedir + "/resourcepacks"
    rppathnew = rppath + "\\" + rpFileName
    shutil.move(rppathnew, rpdir)

def adNewOptions(newoptionsFileName, datadir, minedir):
    nOptionsPath = datadir + "\\" + newoptionsFileName
    oOptionsPath = minedir + "\\options.txt"
    with open(nOptionsPath, "r") as nOptions:
        nOptionsText = nOptions.read()
    with open(oOptionsPath, "w") as oOptions:
        oOptions.write(nOptionsText)