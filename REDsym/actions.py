import os
import os.path
import shutil
import tempfile

import regex
from ftfy import fix_text

import REDsym.bigtable
import REDsym.util
import REDsym.settings


rootdir_wcd = REDsym.settings.rootdir_wcd
rootdir_red = REDsym.settings.rootdir_red
redsym_dir = REDsym.settings.redsym_dir


def update_wm2(inplace=False):

    def symlink_album(source, target):
        print("symlink '{}' -> '{}'".format(fix_text(source), target))
        try:
            os.symlink(source, target)
            db.insert_symlink_RED(new_dir, target)
        except FileExistsError:
            print("symlink exists '{}' -> '{}'".format(fix_text(source), target))

    def move_album(source, target):
        print("move '{}' -> '{}'".format(fix_text(source), target))
        shutil.move(source, target)

    db = REDsym.bigtable.DBase()
    new_dirs_only_music, deleted_dirs = REDsym.bigtable.update_bigtable()

    if inplace:
        tempdir = tempfile.mkdtemp(prefix='redsym', dir=redsym_dir)

    print("##### START symlinking #####")
    print("There are:", len(new_dirs_only_music), "new folders to symlink")
    print("There are:", len(deleted_dirs), "symlinks to delete")

    for deleted_dir in deleted_dirs:
        if rootdir_wcd and rootdir_wcd in deleted_dir:
            symlink = db.get_symlink_WCD_from_dir(deleted_dir)
            if symlink:
                db.delete_symlink_WCD(symlink)
                os.remove(symlink)
        if rootdir_red and rootdir_red in deleted_dir:
            symlink = db.get_symlink_RED_from_dir(deleted_dir)
            if symlink:
                db.delete_symlink_RED(symlink)
                os.remove(symlink)

    for new_dir in new_dirs_only_music:
#        if rootdir_wcd and rootdir_wcd in new_dir:
#            audio_info_wm2 = db.get_meta_from_dir_WCD(new_dir)
#            artist_name, album_name = REDsym.util.audio_dir_filename_wcd_wm2(new_dir)
#            artist_name_valid = REDsym.util.filenamefy(artist_name)
#            album_name_valid = REDsym.util.filenamefy(album_name)
#            if not os.path.exists(redsym_dir + artist_name_valid):
#                os.makedirs(redsym_dir + artist_name_valid)
#            new_album_path_folder = REDsym.util.get_music_dir(new_dir)
#            source = os.path.join(new_dir, new_album_path_folder)
#            target = os.path.join(redsym_dir, artist_name_valid, album_name_valid)
#            print("symlink '%s' -> '%s'" % (fix_text(source), target))
#            if os.path.exists(target):
#                target = target + ' ID: ' + str(audio_info_wm2['TorrentId'])
#            try:
#                os.symlink(source, target)
#                db.insert_symlink_WCD(new_dir, target)
#            except FileExistsError:
#                print("symlink exists '%s' -> '%s'" % (fix_text(source), target))
        if rootdir_red and rootdir_red in new_dir:
            artist_name, album_name = REDsym.util.audio_dir_filename_red_wm2(new_dir)
            artist_name_valid = REDsym.util.filenamefy(artist_name)
            album_name_valid = REDsym.util.filenamefy(album_name)

            new_album_path_folder = REDsym.util.get_music_dir(new_dir)
            source = os.path.join(new_dir, new_album_path_folder)
            if inplace:
                target = tempdir
                target_dir = os.path.join(redsym_dir, tempdir, artist_name_valid)
            else:
                target = redsym_dir
                target_dir = os.path.join(redsym_dir, artist_name_valid)
            if not os.path.exists(target_dir):
                os.makedirs(target_dir)
            target = os.path.join(target, artist_name_valid, album_name_valid)
            if os.path.exists(target):
                torrent_id = str(db.get_meta_from_dir_RED(new_dir)['TorrentId'])
                target += ' ID: ' + torrent_id

            if inplace:
                move_album(source, target)
            else:
                symlink_album(source, target)

    if inplace:
        # Remove everything except tempdir.
        with os.scandir(redsym_dir) as it:
            for entry in it:
                if entry.is_dir() and os.path.join(redsym_dir, entry.name) != tempdir:
                    shutil.rmtree(os.path.join(redsym_dir, entry.name))

        # Move tempdir's contents to redsym_dir.
        with os.scandir(tempdir) as it:
            for entry in it:
                shutil.move(os.path.join(tempdir, entry.name), redsym_dir)

        os.rmdir(os.path.join(redsym_dir, tempdir))
