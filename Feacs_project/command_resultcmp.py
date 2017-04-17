import os
import json
import time
from command_base import CommandBase
from command_compare import RunExtructUniqueCasesCmd

def  Float2Int(it):
    if it>0:
        return -1
    elif it<0:
        return 1
    return 0

def  ResultCmp(item0,item1):
    item2cmp=[item0['maxJacob2']['diff']-item1['maxJacob2']['diff'],
              item0['maxJacob']['diff'] - item1['maxJacob']['diff'],
              item0['elem2DNum']['diff'] - item1['elem2DNum']['diff']
              ]

    for it in item2cmp:
        if abs(it)>0.1:
            return Float2Int(it)

    return Float2Int(item2cmp[0])


class RunAutomationCompareCmd(CommandBase):
    def __init__(self, mgr, kwargs=None):
        super(RunAutomationCompareCmd, self).__init__(mgr, kwargs=kwargs)
        self._baseLine  ={}
        self._newResult ={}
        self._cmpResult ={}
        self._config    ={}
        self._case2cmp  =[]

    def convert2DictBy(self,input,key):
        output = {}
        for item in input:
            if key not in item:
                continue
            output[item[key]] = item
        return output

    def convertCases2Dict(self,jsonFile):
        input=self.load_json(jsonFile)
        if input :
            return self.convert2DictBy(input['meshCases'],'name')
        return None

    def setup(self):
        self._baseLine  = self.convertCases2Dict(self.get_arg('baseJson'))
        self._newResult = self.convertCases2Dict(self.get_arg('testJson'))
        self._config    = self.get_arg('globalSettings')
        for (k, v) in self._baseLine.items():
            self._case2cmp.append(k)


    def compare(self):
        missCases   =[]
        failureCases =[]
        correctCases =[]
        for it in self._case2cmp:
            if it not in self._newResult.keys():
                missCases.append(it)
            else:
                isCorrect=1
                cmpResult={'name':it}
                for (k,v0) in self._baseLine[it].items():
                    if not k in self._newResult[it]:
                         missCases.append(k)
                    v1= self._newResult[it][k]
                    if isinstance(v0,unicode) or isinstance(v0,str) :
                        pass
                    elif isinstance(v1,list):
                        dict0=self.convert2DictBy(v0,'name')
                        dict1=self.convert2DictBy(v1,'name')
                        cmpItem={}
                        for (ki0,vi0) in dict0.items():
                            if ki0 not in self._config.keys():
                                continue
                            vi1= dict1[ki0]
                            v0=vi0['value']
                            v1=vi1['value']
                            d = self.diff(v0, v1)
                            cmpItem['base']=v0
                            cmpItem['test']=v1
                            cmpItem['diff']=d
                            cmpResult[ki0]=cmpItem
                            cfg = self._config[ki0]
                            if float(cfg) <= 1e-16:
                                continue
                            if (vi0['isBiggerBetter'] and v1<v0) or (v0<v1):
                                if d >= float(cfg):
                                    if v1 > self.get_arg("maxJacob") or v0 > self.get_arg("maxJacob"):
                                        isCorrect=0
                    else:
                        cmpItem={}
                        cmpItem['base']=v0
                        cmpItem['test']=v1
                        d = self.diff(v0, v1)
                        cmpItem['diff']=d
                        if k not in self._config.keys():
                            continue
                        cfg=self._config[k]
                        if float(cfg) <= 1e-16:
                            continue
                        if d >= float(cfg):
                            if k == 'time':
                                if v1 > self.get_arg("longTime") or v1 > self.get_arg("longTime"):
                                    isCorrect = 0
                            else:
                                if v0 > self._config['elem2DNumMin'] or v1 > self._config['elem2DNumMin']:
                                    isCorrect =0
                        cmpResult[k]=cmpItem

                if isCorrect:
                    correctCases.append(cmpResult)
                else:
                    failureCases.append(cmpResult)

        failureCases.sort(cmp=ResultCmp)
        self._cmpResult['FailureCases']=failureCases
        self._cmpResult['CorrectCases']=correctCases
        self._cmpResult['Missing']     =missCases
        self._cmpResult['Summary']={
            'Correct':len(correctCases),
            'Failure':len(failureCases),
            'Missing':len(missCases),
            'Total':len(correctCases)+len(failureCases)+len(missCases)
        }


    def diff(self, baseValue, testValue):
        if abs(float(baseValue)) < 1.e-10:
            return abs((float(testValue) - float(baseValue)))
        else:
            return abs((float(testValue) - float(baseValue))) / float(baseValue)


    def outputReport(self):
        import datetime
        reportJson=self.get_arg('reportDir')
        outputDict = {"FailureCases": [], "CorrectCases": [], "Missing": [], "Summary": []}
        if reportJson:
            for i in ["FailureCases", "CorrectCases"]:
                for itemDict in self._cmpResult[i]:
                    tempDict = self.formatDict(itemDict)
                    outputDict[i].append(tempDict)
            outputDict["Missing"] = self._cmpResult["Missing"]
            outputDict["Summary"] = self._cmpResult["Summary"]
            currentTime = datetime.datetime.now()
            Time = '%d-%2d-%2d.json' % (currentTime.year, currentTime.month, currentTime.day)
            with open(os.path.join(reportJson, Time), 'w+') as f:
                json.dump(outputDict, f, indent=1)

    def outputFailures(self):
        import datetime
        currentTime = datetime.datetime.now()
        timeNamed = '%d-%2d-%2d' % (currentTime.year, currentTime.month, currentTime.day)
        failureCasesName = {}
        reportJson=self.get_arg('reportDir')
        failureCases=self.get_arg('failureCases')
        failureCasesNameList = self.get_arg('failure')
        if failureCases:
            filename=failureCases['name']
            if reportJson:
                filename=os.path.join(reportJson,filename)
            casesNameList = []
            for item in self._cmpResult['FailureCases']:
                casesNameList.append(item['name'])
            failureCasesName[timeNamed] = casesNameList
            if failureCasesNameList:
                with open(failureCasesNameList, 'w+') as f1:
                    json.dump(failureCasesName, f1, indent=1)

            source=failureCases['source']
            if source:
                args={
                    'inputDir':source,
                    'filter':failureCases['filter'],
                    'caseList':casesNameList,
                    'outputJson':filename,
                    # 'triageJson':filename
                }
                cmd=RunExtructUniqueCasesCmd(self._mgr,args)
                cmd.do()

    def output(self):
        self.outputReport()
        self.outputFailures()

    def formatDict(self, dict):
        dictItem = {}
        for k, v in dict.items():
            if k == "name":
                dictItem["%12s" % 'name'] = v
                continue
            if v["base"] > v["test"]:
                dictItem["%12s" % k] = "base:%5s, test:%5s, diff:%5s" % (v["base"], v["test"], -round(v["diff"], 2))
            else:
                dictItem["%12s" % k] = "base:%5s, test:%5s, diff:%5s" % (v["base"], v["test"], round(v["diff"], 2))
        return dictItem


    def do(self):
        self.setup()
        self.compare()
        self.output()

