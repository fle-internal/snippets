import fysom
import os
import sys


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
        }})

# FSM callbacks
def new_playlist(e):

    if e.playlist:         # if our current playlist is empty, dont create a new one since it's just a waste
        e.playlists.append(e.playlist.copy())

    line = e.line.replace('Playlist: ', '')
    e.playlist['title'] = line


def eof(e):
    e.playlists.append(e.playlist)
    print e.playlists


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
                fsm.saw_divider()
            elif '/v/' in line:
                fsm.saw_video()
            elif '/e/' in line:
                fsm.saw_exercise()
            elif 'quiz' in line:
                fsm.saw_quiz()
            else:
                raise Exception('Error at line number %s: Unknown field "%s"' % (lineno, line))
        else:
            fsm.eof(**event_args)


if __name__ == '__main__':
    main()
