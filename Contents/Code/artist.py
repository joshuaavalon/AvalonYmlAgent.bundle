import hashlib
from os.path import dirname, exists, join
from urllib import unquote

import yaml
from utils import set_metadata_list


def get_artist(media):
    path = get_artist_file(media)
    album_dir = dirname(path)
    artist_dir = dirname(album_dir)
    file_path = join(artist_dir, "artist.yml")
    string = Core.storage.load(file_path)
    return yaml.safe_load(string)


def set_artist(metadata, media, artist):
    metadata.summary = artist.get("summary")
    metadata.rating = artist.get("rating")
    set_metadata_list(metadata, "genres", artist.get("genres"))
    set_metadata_list(metadata, "collections", artist.get("collections"))
    set_metadata_list(metadata, "similar", artist.get("similar"))

    set_artist_cover(metadata, media)


def set_artist_cover(metadata, media):
    path = get_artist_file(media)
    artist_dir = dirname(path)
    file_path = join(artist_dir, "cover.jpg")
    if not exists(file_path):
        file_path = join(artist_dir, "cover.png")
    if not exists(file_path):
        return
    cover = Core.storage.load(file_path)
    key = hashlib.md5(cover).hexdigest()
    metadata.posters[key] = Proxy.Media(cover)


def get_artist_file(media):
    if hasattr(media, "filename") and media.filename is not None:
        return unquote(media.filename).decode("utf8")
    for album in media.children:
        for track in album.children:
            return track.items[0].parts[0].file
