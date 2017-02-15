import os, time


def readFile(fp):
    fileList = []
    if os.path.exists(fp):
        with open(fp, "r+") as f:
            for readline in f.readlines():
                fileList.append(readline.strip('\n'))
        return fileList


def output(fn, req):
    if os.path.exists(req):
        for parent, dirnames, filenames in os.walk(req):
            if fn in filenames:
                atime = os.path.getatime(os.path.join(parent, fn))
                timeArray = time.localtime(atime)
                formatTime = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)
                print os.path.join(parent, fn), formatTime
            else:
                print "%s doesn't exist." % fn


if __name__ == "__main__":
    filePath = "D:/test.txt"
    folderPath = "D:/testfolder"
    fileList = readFile(filePath)
    for fn in fileList:
        output(fn, folderPath)



