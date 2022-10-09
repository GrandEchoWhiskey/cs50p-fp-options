import options
import pytube
from pytube.cli import on_progress
import sys
import os
import shutil

options.opt('audio-only', 'a')
options.opt('resolution', 'r')
options.opt('target', 't')
options.opt('source', 's')
options.opt('playlist', 'p')

def rename(name):
    name = name.replace(' ', '-')
    for char in '!@#$%^&*()+=<>,.?/\'\"\\|{}[]~`':
        name = name.replace(char, '')
    return name

@options.option('source')
def sources(links, *args):
    for link in args:
        links.append(link.replace('\"', '').replace("https://", ''))

@options.option('playlist')
def playlist(links, link):
    try:
        link = link.replace('\"', '').replace("https://", '')
        start = link.index('list=')
        endl = start
        while endl < len(link):
            if link[endl] in ['&', '#']:
                break
            endl += 1
        pllst = link[start:endl]
        link = link[:link.index('?')+1]+pllst
    except Exception as e:
        raise ValueError(f"Unable to set playlist: {e}")
    try:
        p = pytube.Playlist(link)
        links.extend(list(p.video_urls))
    except Exception as e:
        raise ConnectionError(f"Unable to set playlist: {e}")

@options.option('resolution', required=False)
def resolution(ys, arg: str = 'highest'):

    try:
        if arg == 'highest':
            stream = ys.get_highest_resolution()
        elif arg == 'lowest':
            stream = ys.get_lowest_resolution() 
        else:
            stream = ys.get_by_resolution(arg)
        if stream is None:
            raise ValueError
        return stream
    except:
        raise ValueError("Resolution: " + arg + " does not exist.")

# TODO: unittests

@options.option('target', required=False)
def save_target(stream, audio, target='.'):

    # try:
        outfile = stream.download(target)
        head, tail = os.path.split(outfile)
        base, ext = os.path.splitext(tail)
        newfile = os.path.join(head, rename(base) + ('.mp3' if audio else ext))
        os.rename(outfile, newfile)
    # except:
    #     raise ValueError("Unable to save the file")

def url_to_yt(url):
    try:
        return pytube.YouTube(url, on_progress_callback=on_progress)
    except:
        raise ConnectionError("Unable to set YouTUbe stream")

def print_title(index, title):
    print(f"{index}. {title}".ljust(terminal_max_width(), ' '))

def terminal_max_width():
    return int(shutil.get_terminal_size().columns)

def main():

    audio_only = options.var('audio-only').bool
    links = []

    playlist(links)
    sources(links)

    for i, url in enumerate(links):

        # try:

            yt= url_to_yt(url)
            print_title(i+1, yt.title)

            stream = resolution(yt.streams)

            if audio_only: stream = yt.streams.get_audio_only()

            save_target(stream, audio_only)

        # except Exception as e:

        #     print(e)
        #     print("Trying to continue..")

    print("Done!".ljust(terminal_max_width(), ' '))


if __name__ == "__main__":
    main()