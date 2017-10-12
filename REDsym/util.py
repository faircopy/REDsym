import os
import os.path
import sys

import REDsym.bigtable


def filenamefy(value):
    value_fix_char = value.replace('/', '-')
    value_fix_dot = value_fix_char.lstrip('.')
    value_valid = value_fix_dot[0:254]
    return value_valid


def audio_dir_filename_wcd_wm2(dir):
    db = REDsym.bigtable.DBase()
    audio_info_wm2 = db.get_meta_from_dir_WCD(dir)
    if audio_info_wm2['year'] !='':
        album_name = '(' +  str(audio_info_wm2['year']) + ') '  + audio_info_wm2['name']
    else:
        album_name = audio_info_wm2['name']
    if audio_info_wm2['remasterTitle'] !='':
        album_name = album_name + ' (' +  audio_info_wm2['remasterTitle'] + ') '
    if audio_info_wm2['remasterCatalogueNumber'] !='':
        album_name = album_name + ' (' +  audio_info_wm2['remasterCatalogueNumber'] + ') '
    album_name = album_name + ' [' + audio_info_wm2['format'] + ']'

    #detect classical or jazz
    if any("classical" in s for s in audio_info_wm2['tags']):
        classical = True
    else:
        classical = False
    if any("jazz" in s for s in audio_info_wm2['tags']):
        jazz = True
    else:
        jazz = False

    if len(audio_info_wm2['musicInfo'].values()) == 1:
        for key, value in audio_info_wm2['musicInfo'].items():
                if len(value) <= 3:
                    artist_name = ', '.join(value)
                elif classical:
                    artist_name = 'Various Classical Artists'
                elif jazz:
                    artist_name = 'Various Jazz Artists'
                else:
                    artist_name = 'Various Artists'

    elif classical:
        if 'composers' in audio_info_wm2['musicInfo']:
                if len(audio_info_wm2['musicInfo']['composers']) <= 3:
                    artist_name = ', '.join(audio_info_wm2['musicInfo']['composers'])
                else:
                    artist_name = 'Various Classical Artists'
        elif 'artists' in audio_info_wm2['musicInfo']:
            if len(audio_info_wm2['musicInfo']['artists']) <= 3:
                artist_name = ', '.join(audio_info_wm2['musicInfo']['artists'])
            else:
                artist_name = 'Various Classical Artists'
        elif 'conductor' in audio_info_wm2['musicInfo']:
            if len(audio_info_wm2['musicInfo']['conductor']) <= 3:
                artist_name = ', '.join(audio_info_wm2['musicInfo']['conductor'])
            else:
                artist_name = 'Various Classical Artists'

    elif 'artists' not in audio_info_wm2['musicInfo']:
        for key, value in audio_info_wm2['musicInfo'].items():
            if value:
                artist_name = ', '.join(value)

    elif jazz:
        if 'artists' in audio_info_wm2['musicInfo']:
            if len(audio_info_wm2['musicInfo']['artists']) <= 3:
                artist_name = ', '.join(audio_info_wm2['musicInfo']['artists'])
            else:
                artist_name = 'Various Jazz Artists'
        elif 'with' in audio_info_wm2['musicInfo']:
            if len(audio_info_wm2['musicInfo']['with']) <= 3:
                artist_name = ', '.join(audio_info_wm2['musicInfo']['with'])
            else:
                artist_name = 'Various Jazz Artists'

    elif 'artists' in audio_info_wm2['musicInfo']:
        if len(audio_info_wm2['musicInfo']['artists']) <= 3:
            artist_name = ', '.join(audio_info_wm2['musicInfo']['artists'])
        else:
            artist_name = 'Various Artists'

    elif 'composers' in audio_info_wm2['musicInfo']:
        if len(audio_info_wm2['musicInfo']['composers']) <= 3:
            artist_name = ', '.join(audio_info_wm2['musicInfo']['composers'])
        else:
            artist_name = 'Various Artists'

    return artist_name, album_name


def audio_dir_filename_red_wm2(dir):
    db = REDsym.bigtable.DBase()
    audio_info_wm2 = db.get_meta_from_dir_RED(dir)
    if audio_info_wm2['year'] !='':
        album_name = '(' +  str(audio_info_wm2['year']) + ') '  + audio_info_wm2['name']
    else:
        album_name = audio_info_wm2['name']
    if audio_info_wm2['remasterTitle'] !='':
        album_name = album_name + ' (' +  audio_info_wm2['remasterTitle'] + ') '
    if audio_info_wm2['remasterCatalogueNumber'] !='':
        album_name = album_name + ' (' +  audio_info_wm2['remasterCatalogueNumber'] + ') '
    album_name = album_name + ' [' + audio_info_wm2['format'] + ']'

    #detect classical or jazz
    if any("classical" in s for s in audio_info_wm2['tags']):
        classical = True
    else:
        classical = False
    if any("jazz" in s for s in audio_info_wm2['tags']):
        jazz = True
    else:
        jazz = False

    if len(audio_info_wm2['musicInfo'].values()) == 1:
        for key, value in audio_info_wm2['musicInfo'].items():
                if len(value) <= 3:
                    artist_name = ', '.join(value)
                elif classical:
                    artist_name = 'Various Classical Artists'
                elif jazz:
                    artist_name = 'Various Jazz Artists'
                else:
                    artist_name = 'Various Artists'

    elif classical:
        if 'composers' in audio_info_wm2['musicInfo']:
                if len(audio_info_wm2['musicInfo']['composers']) <= 3:
                    artist_name = ', '.join(audio_info_wm2['musicInfo']['composers'])
                else:
                    artist_name = 'Various Classical Artists'
        elif 'artists' in audio_info_wm2['musicInfo']:
            if len(audio_info_wm2['musicInfo']['artists']) <= 3:
                artist_name = ', '.join(audio_info_wm2['musicInfo']['artists'])
            else:
                artist_name = 'Various Classical Artists'
        elif 'conductor' in audio_info_wm2['musicInfo']:
            if len(audio_info_wm2['musicInfo']['conductor']) <= 3:
                artist_name = ', '.join(audio_info_wm2['musicInfo']['conductor'])
            else:
                artist_name = 'Various Classical Artists'

    elif 'artists' not in audio_info_wm2['musicInfo']:
        for key, value in audio_info_wm2['musicInfo'].items():
            if value:
                artist_name = ', '.join(value)

    elif jazz:
        if 'artists' in audio_info_wm2['musicInfo']:
            if len(audio_info_wm2['musicInfo']['artists']) <= 3:
                artist_name = ', '.join(audio_info_wm2['musicInfo']['artists'])
            else:
                artist_name = 'Various Jazz Artists'
        elif 'with' in audio_info_wm2['musicInfo']:
            if len(audio_info_wm2['musicInfo']['with']) <= 3:
                artist_name = ', '.join(audio_info_wm2['musicInfo']['with'])
            else:
                artist_name = 'Various Jazz Artists'

    elif 'artists' in audio_info_wm2['musicInfo']:
        if len(audio_info_wm2['musicInfo']['artists']) <= 3:
            artist_name = ', '.join(audio_info_wm2['musicInfo']['artists'])
        else:
            artist_name = 'Various Artists'

    elif 'composers' in audio_info_wm2['musicInfo']:
        if len(audio_info_wm2['musicInfo']['composers']) <= 3:
            artist_name = ', '.join(audio_info_wm2['musicInfo']['composers'])
        else:
            artist_name = 'Various Artists'

    return artist_name, album_name


def get_music_dir(dir):

    def get_immediate_subdirectories(a_dir):
        return [name for name in os.listdir(a_dir) if os.path.isdir(os.path.join(a_dir, name))]

    def media_in_directory(directory):
        count = 0
        media_extensions = ('flac', 'mp3', 'dts', 'wav', 'm4a', 'ac3')
        for filename in os.listdir(directory):
            for ext in media_extensions:
                if filename.lower().endswith('.' + ext):
                    count += 1
                    break
        return count

    def media_in_subdirs(album_path):
        count = 0
        for root, dirs, files in os.walk(album_path):
            for name in dirs:
                count += media_in_directory(name)
        return count

    sub_directory = get_immediate_subdirectories(dir)
    if len(sub_directory) == 0:
        sub_directory = ''
    else:
        sub_directory = sub_directory[0]
    if (media_in_directory(os.path.join(dir, sub_directory)) > 1) and (media_in_directory(dir) > 1):
        return ''
    elif (media_in_directory(os.path.join(dir, sub_directory)) > 1) or media_in_subdirs(os.path.join(dir, sub_directory)):
        return sub_directory
    elif media_in_directory(dir) > 1:
        return ''
    elif media_in_directory(dir) == 0:
        return False


def remove_surrogate_escaping(s, method='ignore'):
    assert method in ('ignore', 'replace'), 'invalid removal method'
    return s.encode('utf-8', method).decode('utf-8')


def is_surrogate_escaped(s):
    try:
        s.encode('utf-8')
    except UnicodeEncodeError as e:
        if e.reason == 'surrogates not allowed':
            return True
        raise
    return False
