import options
import pytube
import sys

options.opt('audio-only', 'a')
options.opt('resolution', 'r')
options.opt('target', 't')
options.opt('source', 's')
options.opt('playlist', 'p')

links = []

def rename_file(name):
    name = name.replace(' ', '-')
    for char in '!@#$%^&*()+=<>,.?/\'\"\\|{}[]~`':
        name = name.replace(char, '')
    return name

@options.option('source')
def set_sources(*args):
    links.extend(args)

@options.option('playlist')
def set_playlist(link):
    link = link.replace('\"', '').replace("https://", '')
    try:
        start = link.index('list=')
        endl = start
        while endl < len(link):
            if link[endl] in ['&', '#']:
                break
            endl += 1
        pllst = link[start:endl]
        link = link[:link.index('?')+1]+pllst
        p = pytube.Playlist(link)
        links.extend(list(p.video_urls))
    except Exception as e:
        sys.exit(f"Unable to set playlist: {e}")

@options.option('resolution')
def set_resolution(arg):
    if arg in ['high', 'low']:
        return arg
    try: return int(arg)
    except: return 'high'

def main():
    pass

if __name__ == "__main__":
    main()