import urllib.request
import json, os

class CommandBase(object):
    def __init__(self, mgr, kwargs=None):
        self._mgr = mgr
        self._kwargs = {}
        self._userEnv = None
        if kwargs is not None:
            self._kwargs = kwargs
            self.init_enviroment()

    @property
    def mgr(self):
        return self._mgr

    def get_arg(self, name):
        return self._kwargs.get(name)

    def init_enviroment(self):
        envs = self._kwargs.get('env')
        self._userEnv = {}
        if envs:
            for (k, v) in envs.iteritems():
                self._userEnv[str(k)] = str(v)

    def downloadURL(self, url, ctype):
        # ctype is coding type of html: utf-8 or gbk etc.
        req = urllib.request.Request(url, headers={'User-Agent': "Magic Browser"})
        page = urllib.request.urlopen(req).read()
        data = page.decode(ctype)
        return data

    # JSON file to setup filter str and envs and url site
    def loadJson(self, jsonfile):
        if self.isJson(jsonfile):
            with open(jsonfile, 'r+') as f:
                return json.load(f)
        return None

    def isJson(self, file):
        if os.path.isfile(file):
            fname, fext = os.path.splitext(file)
            if fext is not '.json':
                assert "Given file is not JSON file, please confirm"
            else:
                return True
