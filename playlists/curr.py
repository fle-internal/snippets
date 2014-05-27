import csv
import functools
import fysom
import json
import pathlib
import random
from pprint import pprint


def initialize_fsm():
    return fysom.Fysom({
        'initial': 'startup',
        'final': 'end',
        'events': [
            {
                'name': 'saw_divider',
                'src': ['quiz_entry',
                        'video_entry',
                        'exercise_entry',
                        'new_playlist'],
                'dst': 'divider_entry'
            },
            {
                'name': 'saw_video',
                'src': ['divider_entry',
                        'video_entry',
                        'exercise_entry',
                        'quiz_entry',
                        'new_playlist'],
                'dst': 'video_entry'
            },
            {
                'name': 'saw_exercise',
                'src': ['new_playlist',
                        'quiz_entry',
                        'divider_entry',
                        'video_entry',
                        'exercise_entry'],
                'dst': 'exercise_entry'
            },
            {
                'name': 'saw_quiz',
                'src': ['exercise_entry',
                        'video_entry'],
                'dst': 'quiz_entry',
            },
            {
                'name': 'saw_new_playlist',
                'src': ['startup',
                        'video_entry',
                        'quiz_entry',
                        'exercise_entry'],
                'dst': 'new_playlist',
            },
            {
                'name': 'eof',
                'src': ['video_entry',
                        'quiz_entry',
                        'exercise_entry'],
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

    # if our current playlist is empty, dont create a new one since
    # it's just a waste
    if e.playlist:
        e.playlists.append(e.playlist.copy())

    e.playlist['title'] = e.playlist_title
    e.playlist['id'] = e.playlist_id


def eof(e):
    e.playlists.append(e.playlist)

    pprint(e.playlists)


def saw_misc_entry(e):
    playlist = e.playlist

    if not playlist.get('entries'):
        playlist['entries'] = []

    kind = e.event.replace('saw_', '')
    entries = playlist['entries']
    entry = {
        'entity_kind': kind.capitalize(),
        'entity_id': e.entity_id,
        'sort_order': len(entries) if entries else 0,
    }
    playlist['entries'].append(entry)


def saw_divider(e):
    if not e.playlist.get('entries'):
        e.playlist['entries'] = []

    entries = e.playlist['entries']
    entry = {
        'entity_kind': 'Divider',
        'sort_order': len(entries) - 1 if entries else 0,
        'description': e.description,
    }
    e.playlist['entries'].append(entry)


def generate_playlist_from_tsv(tsv_path, fsm):
    with open(tsv_path.as_posix()) as f:
        tsv = csv.DictReader(f, delimiter='\t')

        current_playlist = {}
        playlists = []
        unit_test_writing_funcs = []
        event_default_args = {
            'playlists': playlists,
            'playlist': current_playlist
        }
        for row in tsv:

            # Maybe we got a new playlist
            playlist_title = row['Index'] or row['Link']
            if 'Playlist' in playlist_title:

                # invalid format for new playlist row, skip
                if not row['Playlist ID']:
                    continue
                else:  # valid playlist title
                    fsm.saw_new_playlist(
                        playlist_id=row['Playlist ID'],
                        playlist_title=playlist_title,
                        **event_default_args
                    )

            elif 'subtitle' in row['Link'].lower():  # we got a subtitle row
                fsm.saw_divider(
                    description=row['Link'],
                    **event_default_args
                )

            elif 'video' in row['Index'].lower():  # we got a video row
                fsm.saw_video(
                    entity_id=row['Link'],
                    **event_default_args
                )

            elif 'exercise' in row['Index'].lower():  # we got an exercise row
                fsm.saw_exercise(
                    entity_id=row['Link'],
                    **event_default_args
                )

            elif 'quiz' in row['Link'].lower():  # we got a video row
                fsm.saw_quiz(
                    entity_id=row['Link'],
                    **event_default_args
                )

            elif 'baseline exam' in row['Link'].lower():
                # Skip for now
                # TODO: handle this
                continue

            elif 'unit test' in row['Link'].lower():
                unit_test_func = functools.partial(
                    write_unit_test_to_file,
                    test_name=row['Link'],
                    playlist_ids_string=row['Playlist ID']
                )

                unit_test_writing_funcs.append(unit_test_func)

            # Whatever is that we get here, we don't understand it.
            # Print it out if it's not empty.
            else:
                # Empty row, don't bother printing
                if row['Index'] == row['Link'] == '':
                    continue
                else:
                    err_msg_template = "Don't understand row from file %s: %s"
                    raise Exception(err_msg_template % (tsv_path, row))

        else:
            playlists.append(current_playlist)
            return (playlists, unit_test_writing_funcs)


def write_unit_test_to_file(test_name, playlist_ids_string, all_playlists):
    test_id = random.randint(1, 5000)
    unit_test_filepath = pathlib.Path('.') / "{}.json".format(test_id)

    playlist_ids = [s.strip() for s in playlist_ids_string.split(',')]

    for playlist_id in playlist_ids:
        # get the playlist, and collect the entity id of all exercises
        # in that playlist
        playlist = all_playlists[playlist_id]
        exercise_ids = [
            entity['entity_id'] for entity
            in playlist['entries']
            if entity['entity_kind'] == 'Exercise'
        ]

    unit_test_data = {
        'title': test_name,
        'ids': exercise_ids,
        'seed': random.randint(1, 5000),
        'repeats': 1,
    }

    with open(unit_test_filepath.as_posix(), 'w') as f:
        json.dump(unit_test_data, f)


def main_tsv_playlists():
    cwd = pathlib.Path('.')
    tsv_files = cwd.glob("*Playlists.tsv")
    playlist_json_filepath = cwd / 'playlists.json'

    playlists = []
    test_writing_partials = []
    fsm = initialize_fsm()
    for tsv_file in tsv_files:
        playlists_this_file, test_fns = generate_playlist_from_tsv(
            tsv_file,
            fsm
        )
        playlists.extend(playlists_this_file)
        test_writing_partials.extend(test_fns)

    # execute the unit test writes
    for test_writing_fn in test_writing_partials:
        # transform the playlists list into a dict first with the
        # playlist id as key, so searching for playlists will be more
        # efficient
        playlists_dict = {pl["id"]: pl for pl in playlists}
        test_writing_fn(all_playlists=playlists_dict)

    # write the playlists to the playlist json
    with open(playlist_json_filepath.as_posix(), 'w') as f:
        json.dump(playlists, f)


if __name__ == '__main__':
    random.seed(1026)
    main_tsv_playlists()
