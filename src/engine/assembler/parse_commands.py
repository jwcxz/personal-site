import sys

from assembler import Assembler


class Command:
    command_name = None;
    metadata = None;

    def __init__(self, metadata=None, search_dirs=None):
        if not self.command_name:
            self.command_name = self.__class__.__name__[len('Command'):].lower();

        if metadata:
            self.metadata = metadata;

        if search_dirs:
            self.search_dirs = search_dirs;

    def execute(self, arglist):
        return "";

    def get_name(self):
        return self.command_name;

    def set_metadata(self, metadata):
        self.metadata = metadata;

    def set_search_dirs(self, search_dirs):
        self.search_dirs = search_dirs;


class CommandDefault(Command):
    command_name = 'default';

    def execute(self, arglist):
        sys.stderr.write("Error: %s is not a valid command (args: %r)\n" %(arglist[-1], arglist[:-1]));
        # TODO: exit?
        return "";


class CommandContent(Command):
    def __init__(self, metadata=None, search_dirs=None):
        Command.__init__(self, metadata=metadata, search_dirs=search_dirs);

    def execute(self, arglist):
        key = arglist[0];

        if key not in self.metadata['content']:
            # TODO: warning?
            return "";

        c = self.metadata['content'][key];

        # TODO: build more elegant content replacement backend
        if c['type'] == 'string':
            return c['value'];
        elif c['type'] == 'file':
            filename = "%s.frag.html" % c['value'];
            a = Assembler(metadata=self.metadata, search_dirs=self.search_dirs);
            return a.populate_template(filename);


class CommandRequire(Command):
    def execute(self, arglist):
        a = Assembler(metadata=self.metadata, search_dirs=self.search_dirs);
        return a.populate_template(arglist[0]);

command_list = [ CommandDefault, CommandContent, CommandRequire ];

