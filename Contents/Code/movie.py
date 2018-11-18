from os.path import dirname, join
from urllib import unquote

from utils import convert_date, first_or, set_metadata_actors, \
    set_metadata_list, set_metadata_list_name


def get_movie(media):
    path = get_movie_file(media)
    movie_dir = dirname(path)
    file_path = join(movie_dir, "movie.yml")
    string = Core.storage.load(file_path)
    return YAML.ObjectFromString(string)


def set_movie(metadata, movie):
    metadata.title = movie.get("title")
    metadata.title_sort = movie.get("sort_title")
    metadata.original_title = movie.get("original_title")
    metadata.content_rating = movie.get("content_rating")
    metadata.studio = first_or(movie.get("studio"))
    aired = convert_date(movie.get("aired"))
    metadata.originally_available_at = aired
    metadata.year = aired.year if aired is not None else None
    metadata.tagline = " / ".join(movie.get("tagline"))
    metadata.summary = movie.get("summary")
    metadata.rating = movie.get("rating")
    set_metadata_list(metadata, "genres", movie.get("genres"))
    set_metadata_list(metadata, "collections", movie.get("collections"))
    set_metadata_actors(metadata, movie.get("actors"))
    set_metadata_list_name(metadata, "writers", movie.get("writers", []))
    set_metadata_list_name(metadata, "directors", movie.get("directors", []))


def get_movie_file(media):
    if hasattr(media, "filename") and media.filename is not None:
        return unquote(media.filename).decode("utf8")
    return media.items[0].parts[0].file
