import os,multiprocessing, json, time
from command_base import CommandBase,ExecuteCommand
from command_compare import RunExtructUniqueCasesCmd,RunExtructResultCmd
from command_resultcmp import RunAutomationCompareCmd

def TestCase(FeacsExec,inputDir,item,envs):
    fullFn = os.path.join(inputDir, item)
    print "\ntesting: %s" % (item)
    args = "/meshes /folder " + fullFn
    return ExecuteCommand(FeacsExec,args,envs=envs)
        

class RunAutomationCmd(CommandBase):
    def __init__(self, mgr, kwargs=None):
        super(RunAutomationCmd, self).__init__(mgr, kwargs=kwargs)
        self._inputDir = self.get_arg('inputDir')
        self._exec = self.get_arg('exec')
        self._excludedCases = self.get_arg('excluded')
        if self._excludedCases is not None:
            self._excludedCases=map(lambda item:item.upper(),self._excludedCases)

        self._inputList = []
        caselist = self.get_arg('inputList')
        if self._exec and self._inputDir:
            if caselist:
                inputDict = self.load_json(caselist)
                if inputDict:
                    self._inputList = inputDict['meshCases']
            else:
                for fn in os.listdir(self._inputDir):
                    if self._excludedCases and  fn.upper() in self._excludedCases:
                        continue
                    fullFn = os.path.join(self._inputDir, fn)
                    if os.path.isdir(fullFn):
                        self._inputList.append(fn)


    def _test(self,FeacsExec,inputDir,item):
        fullFn = os.path.join(inputDir, item)
        print "testing: %s" % (item)
        args = "/meshes /folder " + fullFn
        return self.executeCommand(FeacsExec,args)

    def do(self):
        if len(self._inputList) < 1:
            return
        nprocesses=self.get_arg('nprocesses')
        if not nprocesses or nprocesses < 1:
            nprocesses=int(multiprocessing.cpu_count()*0.8)
        pool = multiprocessing.Pool(processes=nprocesses)
        result = []
        for fn in self._inputList:
            fullFn = os.path.join(self._inputDir, fn)
            if os.path.isdir(fullFn):
                result.append(pool.apply_async(TestCase, args=(self._exec,self._inputDir,fn,self._userEnv,)))
        pool.close()
        pool.join()

        outJson = self.get_arg('outputJson')
        if outJson :
            kwargs={
                    'path':self._userEnv['FEACS_NewAutomationCaseFolder'],
                    'outPath':outJson
            }
            wt=RunExtructResultCmd(self._mgr,kwargs)
            wt.do()



class RunAutomationWithoutDuplicatedCmd(RunAutomationCmd):
    def __init__(self, mgr, kwargs=None):
        super(RunAutomationWithoutDuplicatedCmd, self).__init__(mgr, kwargs=kwargs)
        extract=RunExtructUniqueCasesCmd(mgr, kwargs=kwargs)
        print "please wait,removing duplicated cases..."
        self._inputList=extract.do()


class RunRebaseCmd(RunAutomationCompareCmd):
    def __init__(self, mgr, kwargs=None):
        super(RunRebaseCmd, self).__init__(mgr, kwargs=kwargs)
        self._meseCases = []

    def setup(self):
        self._baseLine = self.convertCases2Dict(self.get_arg('baseJson'))
        self._newResult = self.convertCases2Dict(self.get_arg('testJson'))

    def do(self):
        self.setup()
        rebasePath = self.get_arg("rebaseJson")
        if self._baseLine and self._newResult and rebasePath:
            rebaseFN = self.load_json(rebasePath)
            fnList = rebaseFN['caseGroup']
            for fn in fnList:
                self._baseLine[fn] = self._newResult[fn]
            for (k, v) in self._baseLine.items():
                self._meseCases.append(v)
            baseLine = self.load_json(self.get_arg('baseJson'))
            baseLine["meshCases"] = self._meseCases
            with open(self.get_arg('baseJson'), 'w+') as f:
                json.dump(baseLine, f, indent=2)


class OneClickAutomation(RunAutomationCmd, RunAutomationCompareCmd):
    def __init__(self, mgr, kwargs=None):
        super(OneClickAutomation, self).__init__(mgr, kwargs=kwargs)
        runAuto = RunAutomationCmd(mgr, kwargs=kwargs)
        runAuto.do()
        print("\nTesting Completed")
        print("\nPrepare to compare two JSON files....")
        print("\nRunning....")
        time.sleep(3)
        cmpAuto = RunAutomationCompareCmd(mgr, kwargs=kwargs)
        cmpAuto.do()

    def do(self):
        print("\nDone! You can go to site %s to see the compared-results" % self.get_arg('reportDir'))


class MakeChooseCmd(RunAutomationCmd, RunAutomationCompareCmd, RunExtructUniqueCasesCmd):
    def __init__(self, mgr, kwargs=None):
        super(MakeChooseCmd, self).__init__(mgr, kwargs=kwargs)
        self._option = {
            "1": self._extract,
            "2": self._runBase,
            "3": self._runTest,
            "4": self._compare
        }

    def do(self):
        # self.choose()
        self._extract()

    def choose(self):
        usrOpt = self.get_arg("option")
        if not usrOpt:
            assert "No 'option' arg found in JSON."
        else:
            if usrOpt in self._option.keys():
                self._option[usrOpt]()

    def _extract(self):
        extract_args_json = self.get_arg("extract_args")
        if os.path.exists(extract_args_json):
            extract_args = self.load_json(extract_args_json)
            args = extract_args["args"]
        ext = RunExtructUniqueCasesCmd(self._mgr, args)
        ext.do()

    def _runBase(self):
        pass

    def _runTest(self):
        pass

    def _compare(self):
        pass
