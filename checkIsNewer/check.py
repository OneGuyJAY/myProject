import os
'''
   compare two folder, find out the file which has been changed
'''
import json

class RunCheckFileNewer(object):
    def __init__(self, jsonFile):
        self.fileList = self.load_json(jsonFile)['fileNames']
        self.oldTime = self.load_json(jsonFile)['oldTime']


    def load_json(self, jsonFile):
       if jsonFile is not None:
           assert os.path.isfile(os.path.join(os.getcwd(), jsonFile))
           if os.path.isfile(jsonFile):
               with open(jsonFile, 'r') as fp:
                   return json.load(fp)
       return None
    '''
    def getFileName(req):
       fList = []
       if os.path.isfile(req):
           with open(req, 'r+') as f:
               for item in f.readlines():
                   fList.append(item)
           return fList
       else:
           assert "The file doesn't exist."
    '''

    def judgeIsNewer(self, fn, req):
       if os.path.exists(req):
           for parent, dirnames, filenames in os.walk(req):
               for filename in filenames:
                   if filename == fn:
                       mTime = os.path.getatime(os.path.join(parent, filename))
                       if mTime > self.oldTime:
                           val = 1


if '__name__' == '__main__':
    import os
    runCheck = RunCheckFileNewer('newfiles.json')
    filePath = os.path.join(os.getcwd(), 'newfiles.json')
    newFileList = runCheck.fileList
    for fn in newFileList:

    # get info of filename in new folder
    # judge these files are newer
    # output result

