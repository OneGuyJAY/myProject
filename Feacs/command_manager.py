import sys,json,os
import command_factory

class CommandManager(object):

    def __init__(self):
        self._undo_stack = list()
        self._redo_stack = list()
        self._status = {}
        self._status['bValid'] = 0

    def call_rawcmd(self, rawcmd):
        assert isinstance(rawcmd, dict)
        inst_cmd = command_factory.factory(
            self,
            rawcmd.get('name'),
            kwargs=rawcmd.get('args')
        )
        if inst_cmd:
            self.call_cmd(inst_cmd)
        else:
            raise ValueError('Unknown cmd %s' % str(rawcmd))

    def call_cmd(self, cmd):
        cmd.do()

        self._undo_stack.append(cmd)
        self._redo_stack = list()

    def undo(self):
        if self._undo_stack:
            cmd = self._undo_stack.pop()
            self._redo_stack.append(cmd)
            cmd.undo()

    def redo(self):
        if self._redo_stack:
            cmd = self._redo_stack.pop()
            self._undo_stack.append(cmd)
            cmd.do()


if __name__ == '__main__':
    nargv = len(sys.argv)
    if nargv == 2:
        jsonFile = sys.argv[1]
        if jsonFile is not None:
            assert os.path.isfile(jsonFile)
            if os.path.isfile(jsonFile):
                with open(jsonFile, 'r') as fp:
                    cmd=json.load(fp)
                    m = CommandManager()
                    m.call_rawcmd(cmd)
                    sys.exit(0)

    raise ValueError('Usage:  python [path]/command_manager.py [path]/json file')
