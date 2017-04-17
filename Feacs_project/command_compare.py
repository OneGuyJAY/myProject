import os,json,hashlib,shutil,errno, stat
from command_base import CommandBase

def ChangeAccess(seq):
    for parent, dirnames, filenames in os.walk(seq):
        for fname in filenames:
            if not os.access(os.path.join(parent, fname), os.W_OK):
                os.chmod(os.path.join(parent, fname), stat.S_IWUSR)

def CopyAnything(src, dst):
    try:
        if os.path.exists(dst):
            ChangeAccess(dst)
            shutil.rmtree(dst)
        shutil.copytree(src, dst)
    except OSError as exc:
        if exc.errno == errno.ENOTDIR:
            shutil.copy(src, dst)
        else: raise

def LoadJson(jsonFile):
    if jsonFile is not None:
        if os.path.isfile(jsonFile):
            with open(jsonFile, 'r') as fp:
                return json.load(fp)
    return None

def GetStrMD5(str):
    m = hashlib.md5()
    m.update(str)
    return m.hexdigest()


def GetFileMD5(f):
    m = hashlib.md5()
    while True:
        data = f.read(10240)
        if not data:
            break
        m.update(data)
    return m.hexdigest()


def GetFileMD5ByName(fn):
    if fn is not None:
        if os.path.isfile(fn):
            with open(fn, 'rb') as fp:
                return GetFileMD5(fp)
    return None


def GetFileMD5ByName2(fn, SHAhash):
    if fn is not None:
        if os.path.isfile(fn):
            with open(fn, 'rb') as fp:
                while True:
                    data = fp.read(10240)
                    if not data:
                        break
                    SHAhash.update(hashlib.md5(data).hexdigest())


def GetDirMD5(directory, flst=None):
    SHAhash = hashlib.md5()
    if not os.path.exists(directory):
        return -1
    try:
        for root, dirs, files in os.walk(directory):
            if flst:
                for names in files:
                    if not names in flst:
                        continue
                    filepath = os.path.join(root, names)
                    GetFileMD5ByName2(filepath,SHAhash)
            else:
                for names in files:
                    filepath = os.path.join(root, names)
                    GetFileMD5ByName2(filepath,SHAhash)
    except:
        import traceback
        # Print the stack traceback
        traceback.print_exc()
        return -2
    return SHAhash.hexdigest()


def IsSameFile(f1, f2):
    md1 = GetFileMD5ByName(f1)
    md2 = GetFileMD5ByName(f1)
    if (md1 and md2 and md1 == md2):
        return True
    return False


def GetFileInDir(dir):
    fst = []
    for fn in os.listdir(dir):
        fst.append(fn)


def IsSameCase(dir1, dir2, flst):
    for fn in flst:
        fn1 = os.path.join(dir1, fn)
        fn2 = os.path.join(dir2, fn)
        if not IsSameFile(fn1, fn2):
            return False
    return True

def Unique(seq,idfun=None): 
   # order preserving
   if idfun is None:
       def idfun(x): return x
   seen = {}
   result = []
   for item in seq:
       marker = idfun(item)
       # in old Python versions:
       # if seen.has_key(marker)
       # but in new ones:
       if marker in seen: 
           continue
       seen[marker] = 1
       result.append(item)
   return result

def getKeyBy1st(item):
    return item[0]


class RunExtructUniqueCasesCmd(CommandBase):

    def __init__(self, mgr, kwargs=None):
        super(RunExtructUniqueCasesCmd, self).__init__(mgr, kwargs=kwargs)
        self._fileList2Cmp=self.get_arg('filter')

    def output(self,cases,seen):
        fileName=self.get_arg('outputJson')
        if fileName is not None:
            caseGroup={}
            for (k,v) in seen.items():
                num=len(v)
                if num>1:
                    caseGroup[v[0]]=v[1:]
                else:
                    caseGroup[v[0]]=[]
            dictCases={}
            dictCases['uniqueCases']=cases
            dictCases['caseGroup']=caseGroup
            with open(fileName, 'w') as fp:
                cmd=json.dump(dictCases,fp,sort_keys=True, indent=1)


        outputdir=self.get_arg('outputDir')
        if outputdir:
            if not os.path.exists(outputdir):
                os.makedirs(outputdir)
            inputDir = self.get_arg('inputDir')
            for it in cases:
                fullFn = os.path.join(inputDir, it)
                CopyAnything(fullFn,os.path.join(outputdir, it))

    def append(self,fn,dir,caseLists,seen):
        fullFn = os.path.join(dir, fn)
        if os.path.isdir(fullFn):
            md5 = GetDirMD5(fullFn, self._fileList2Cmp)
            if md5 in seen:
                seen[md5].append(fn)
            else:
                lst=[]
                lst.append(fn)
                seen[md5] = lst
                caseLists.append(fn)

    def do(self):
        inputDir = self.get_arg('inputDir')
        inputCases=self.get_arg('caseList')
        caseLists=[]
        seen = {}

        if inputCases :
            for fn in inputCases:
                self.append(fn,inputDir,caseLists,seen)
        else :
            for fn in os.listdir(inputDir):
                self.append(fn,inputDir,caseLists,seen)

        self.output(caseLists,seen)
        return caseLists
        #sorted(caseLists,key=getKeyBy1st)
        #caseLists= Unique(caseLists,lambda x : x[0])

class RunExtructResultCmd(CommandBase):
    def __init__(self, mgr, kwargs=None):
        super(RunExtructResultCmd, self).__init__(mgr, kwargs=kwargs)
        self._result={}
        self._result['version']=1.0
        self._result['name'] = 'meshing test cases'

    def do(self):
        inputDir = self.get_arg('path')
        if not inputDir:
            return None
        self._caseLists=[]
        for fn in os.listdir(inputDir):
            fullFn = os.path.join(inputDir, fn)
            if os.path.isdir(fullFn):
                resultJson = LoadJson(os.path.join(fullFn, 'res.json'))
                if resultJson:
                    self._caseLists.append(resultJson)

        self._caseLists.sort(key=lambda item:1.0/item['time'])
        self._result['meshCases']=self._caseLists

        fileName = self.get_arg('outPath')
        if fileName :
            with open(fileName, 'w') as fp:
                cmd=json.dump(self._result,fp,indent=2,sort_keys=True)
