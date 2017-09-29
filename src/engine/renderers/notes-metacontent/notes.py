import datetime
import json
import os


class Note:
    def __init__(self, notes_dir, name):
        self.name = name;

        fd = open(os.path.join(notes_dir, name, 'page.json'));
        self.metadata = json.load(fd);
        fd.close();

        # TODO: this is cheating because it assumes the type is `string`
        self.title = self.metadata['content']['title']['value']

        self.date = datetime.datetime.strptime(self.name.split('-')[0], '%y%m%d');

    def get_title(self):
        return self.title;

    def get_date(self):
        return self.date;

    def get_link(self):
        # TODO: don't hardcode the URL base
        return "/notes/%s" % self.name;

    def get_name(self):
        return self.name;


class NotesList:
    def __init__(self, notes_dir):
        self.notes_dir = notes_dir;

        self.note_dirs = os.listdir(self.notes_dir);
        # TODO: use less cheap chronological sorting that only works because it
        # takes advantage of the date format
        self.note_dirs.sort();

        self.notes = {};
        for nd in self.note_dirs:
            self.notes[nd] = Note(self.notes_dir, nd);

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
        pass;
