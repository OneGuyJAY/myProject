from run_automation import RunAutomationCmd,RunAutomationWithoutDuplicatedCmd,OneClickAutomation,MakeChooseCmd
from run_automation import RunRebaseCmd
from command_resultcmp import RunAutomationCompareCmd
from command_compare import RunExtructUniqueCasesCmd,RunExtructResultCmd


_dict_name_cmdClass = {
    'runAutomation': RunAutomationCmd
    ,'runAutomationUnique':RunAutomationWithoutDuplicatedCmd
    ,'extractUniqueCases':RunExtructUniqueCasesCmd
    ,'extractMeshingResult':RunExtructResultCmd
    ,'runResultCmp':RunAutomationCompareCmd
    ,'rebaseFile':RunRebaseCmd
    ,'oneClickAuto':OneClickAutomation
    ,'makeChoose':MakeChooseCmd
}

def factory(mgr, name, kwargs=None):
    cmdClass = _dict_name_cmdClass.get(name)
    if cmdClass:
        return cmdClass(mgr, kwargs=kwargs)
    return None