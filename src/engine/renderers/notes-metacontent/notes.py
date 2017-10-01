import datetime
import json
import os


class Note:
    def __init__(self, notes_dir, name, content_fn=None):
        self.name = name;

        fd = open(os.path.join(notes_dir, name, 'page.json'));
        self.metadata = json.load(fd);
        fd.close();

        # TODO: this is cheating because it assumes the type is `string`
        self.title = self.metadata['content']['title']['value']

        self.date = datetime.datetime.strptime(self.name.split('-')[0], '%y%m%d');

        if content_fn:
            fd = open(content_fn);
            self.content = fd.read();
            fd.close();
        else:
            self.content = "";

    def get_title(self):
        return self.title;

    def get_date(self):
        return self.date;

    def get_link(self):
        # TODO: don't hardcode the URL base
        return "/notes/%s" % self.name;

    def get_name(self):
        return self.name;

    def get_content_preview(self):
        lines = [];
        for line in self.content.split("\n"):
            if line.strip() == "<!--break-->":
                break;
            lines.append(line);

        return "\n".join(lines);


class NotesList:
    def __init__(self, notes_dir, content_dir=None):
        self.notes_dir = notes_dir;

        nds = os.listdir(self.notes_dir);
        self.note_dirs = [];
        for nd in nds:
            try:
                # TODO: don't rely on date being interpreted as an integer
                _ = int(nd.split('-')[0]);
                self.note_dirs.append(nd);
            except:
                continue;

        # TODO: use less cheap chronological sorting that only works because it
        # takes advantage of the date format
        self.note_dirs.sort();

        self.notes = {};
        for nd in self.note_dirs:
            if content_dir:
                # TODO: don't rely on hardcoded content file name
                content_fn = os.path.join(content_dir, nd, 'body.frag.html');
            else:
                content_fn = None;
            self.notes[nd] = Note(self.notes_dir, nd, content_fn=content_fn);

    def get_prev_note(self, cur_note):
        i = self.note_dirs.index(cur_note.get_name());
        if i == 0:
            return None;
        else:
            return self.notes[self.note_dirs[i-1]];

    def get_next_note(self, cur_note):
        i = self.note_dirs.index(cur_note.get_name());
        if i == len(self.note_dirs)-1:
            return None;
        else:
            return self.notes[self.note_dirs[i+1]];

    def get_chronological_list(self):
        note_list = [];
        for n in self.note_dirs:
            note_list.append(self.notes[n]);

        return note_list;