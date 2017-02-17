import os,sys,json,subprocess

def ExecuteCommand(cmd, args='', outputfile=None,envs=None):
    sys.stdout.flush()
    cmdline = "{0} {1}".format(cmd, args).strip()
    cmd = cmdline
    if envs :
        retVal = subprocess.call(cmd, env=envs,stdout=outputfile)
    else :
        retVal = subprocess.call(cmd,stdout=outputfile)
    return retVal


class CommandBase(object):
    def __init__(self, mgr, kwargs=None):
        self._mgr = mgr
        self._kwargs = dict()
        self._userEnv =None
        if kwargs is not None:
            self._kwargs = kwargs
            self.init_enviroment()

    @property
    def mgr(self):
        return self._mgr

    def init_enviroment(self) :
        envs=self._kwargs.get('env')
        self._userEnv={}
        if envs :
           for (k,v) in envs.iteritems() :
               self._userEnv[str(k)]=str(v)

    def get_arg(self, name):
        return self._kwargs.get(name)

    def do(self):
        pass

    def undo(self):
        pass

    def executeCommand(self,cmd, args='', outputfile=None):
        return ExecuteCommand(cmd,args,outputfile,self._userEnv)

    def load_json(self,jsonFile):
        if jsonFile is not None:
            assert os.path.isfile(jsonFile)
            if os.path.isfile(jsonFile):
                with open(jsonFile, 'r') as fp:
                    return json.load(fp)
        return None