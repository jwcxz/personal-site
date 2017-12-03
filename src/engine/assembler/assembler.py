import re
import os

import sys
reload(sys)
sys.setdefaultencoding('utf-8');

class Assembler:
    command_finder = re.compile(r"\<!--__(?P<command>[^:>]+):(?P<arglist>[^>]*)--\>");

    def __init__(self, metadata, search_dirs=[]):
        import parse_commands

        self.metadata = metadata;
        self.search_dirs = search_dirs;

        self.commands = {};
        for c in parse_commands.command_list:
            ci = c(metadata=self.metadata, search_dirs=self.search_dirs);
            self.commands[ci.get_name()] = ci;

    def populate_template(self, filename):
        def replace_command_invocation(m):
            parsed = m.groupdict();
            command = parsed['command'];
            arglist = parsed['arglist'].split(',');

            if command in self.commands:
                ci = self.commands[command];
            else:
                ci = self.commands['default'];
                arglist.append(command);

            return ci.execute(arglist);

        template_path = self._find_file(filename);

        if not template_path:
            sys.stderr.write("Error: %s not found in search directories\n" % filename);
            # TODO: exit?
            return "";

        fd = open(template_path, 'r');
        file_content = fd.read();
        fd.close();

        return self.command_finder.sub(replace_command_invocation, file_content);

    def populate_master_template(self):
        master_template = "%s.template.html" % self.metadata['template'];
        return self.populate_template(master_template);

    def _find_file(self, filename):
        for sd in self.search_dirs:
            test_path = os.path.join(sd, filename);
            if os.path.exists(test_path):
                return test_path;

        return None;
