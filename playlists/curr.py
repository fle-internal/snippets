import fysom
import json
import os
import sys
from pprint import pprint


def initialize_fsm():
    return fysom.Fysom({
        'initial': 'startup',
        'final': 'end',
        'events': [
            {
                'name': 'saw_divider',
                'src': ['quiz_entry', 'video_entry', 'exercise_entry', 'new_playlist'],
                'dst': 'divider_entry'
            },
            {
                'name': 'saw_video',
                'src': ['divider_entry', 'video_entry', 'exercise_entry', 'quiz_entry', 'new_playlist'],
                'dst': 'video_entry'
            },
            {
                'name': 'saw_exercise',
                'src': ['new_playlist', 'quiz_entry', 'video_entry', 'exercise_entry'],
                'dst': 'exercise_entry'
            },
            {
                'name': 'saw_quiz',
                'src': ['exercise_entry', 'video_entry'],
                'dst': 'quiz_entry',
            },
            {
                'name': 'saw_new_playlist',
                'src': ['startup', 'video_entry', 'exercise_entry'],
                'dst': 'new_playlist',
            },
            {
                'name': 'eof',
                'src': ['video_entry', 'quiz_entry', 'exercise_entry'],
                'dst': 'end',
            }
        ],
        'callbacks': {
            'onnew_playlist': new_playlist,
            'oneof': eof,
            'onsaw_divider': saw_divider,
            'onsaw_video': saw_misc_entry,
            'onsaw_exercise': saw_misc_entry,
            'onsaw_quiz': saw_misc_entry,
        }})


# FSM callbacks
def new_playlist(e):

    if e.playlist:         # if our current playlist is empty, dont create a new one since it's just a waste
        e.playlists.append(e.playlist.copy())

    line = e.line.replace('Playlist: ', '')
    e.playlist['title'] = line


def eof(e):
    e.playlists.append(e.playlist)
    # pprint(e.playlists)
    pprint(json.dumps(e.playlists))


def saw_misc_entry(e):
    playlist = e.playlist

    if not playlist.get('entries'):
        playlist['entries'] = []

    kind = e.event.replace('saw_', '')
    entry = {'entity_kind': kind.capitalize(),
             'entity_id': e.line,
             'sort_order': len(playlist['entries']) - 1 if playlist['entries'] else 0,
    }
    playlist['entries'].append(entry)


def saw_divider(e):
    if not e.playlist.get('entries'):
        e.playlist['entries'] = []

    line = e.line.replace('subtitle: ', '')
    entry = {'entity_kind': 'Divider',
             'sort_order': len(e.playlist['entries']) - 1 if e.playlist['entries'] else 0,
             'description': line,
    }
    e.playlist['entries'].append(entry)

# main function
def main():
    testdata_path = os.path.join(os.path.dirname(__file__), 'testdata.txt')

    fsm = initialize_fsm()
    lineno = 0

    event_args = {'playlists': [], 'playlist': {}}
    with open(testdata_path) as f:
        for line in iter(f.readline, ''):
            line = line.rstrip('\n')
            lineno += 1
            if 'Playlist:' in line:
                fsm.saw_new_playlist(line=line, **event_args)
            elif 'subtitle:' in line:
                fsm.saw_divider(line=line, **event_args)
            elif '/v/' in line:
                fsm.saw_video(line=line, **event_args)
            elif '/e/' in line:
                fsm.saw_exercise(line=line, **event_args)
            elif 'quiz' in line:
                fsm.saw_quiz(line=line, **event_args)
            elif line == '\n':
                continue
            else:
                raise Exception('Error at line number %s: Unknown field "%s"' % (lineno, line))
        else:
            fsm.eof(**event_args)


if __name__ == '__main__':
    main()
