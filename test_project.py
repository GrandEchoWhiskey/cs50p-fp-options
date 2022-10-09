import unittest
import sys
import project
import options
from itertools import product
import pytube

class TestSum_project(unittest.TestCase):

    def test_rename(self):
        
        name = 'Renamed string !@#$%^&*()+=<>,.?/\'\"\\|{}[]~` should be empty and spaces are -.'
        self.assertEqual(project.rename(name), 'Renamed-string--should-be-empty-and-spaces-are--')

    def test_sources(self):
        argv = "-s https://www.yout\"ube.com/watch?v=example783 https://www.youtube.com/watch?v=example733".split(' ')
        should = ['www.youtube.com/watch?v=example783', 'www.youtube.com/watch?v=example733']

        options.default_translation.__init__(argv)
        result = []
        project.sources(result)

        for i in range(max(len(result), len(should))):
            self.assertEqual(result[i], should[i])

    def test_playlist(self):
        argv1 = '-p "https://youtube.com/playlist?list=PLln1HX5fO8p1Q50tSGY2lVq3rMm6QOKBi"'.split(' ')
        argv2 = '-p "https://youtube.com/watch?v=159cF0O70f8&list=PLln1HX5fO8p1Q50tSGY2lVq3rMm6QOKBi"'.split(' ')
        argv3 = '-p "https://youtube.com/playlist?list=rMm6QOKBi"'.split(' ')
        argv4 = '-p "https://youtube.com/watch?v=159cF0O70f8"'.split(' ')
        vid_ids = ['TJglkLYUsak', 'zM5teWLCV-A', '159cF0O70f8', 'uEY9DQZGDIE', 'EvmfmfT-T3E', 'mq3xWw2SWcY', 'Lt5-mGc-N9Q']
        vid_links = list(map(lambda x: 'https://www.youtube.com/watch?v='+x, vid_ids))

        for argv in [argv1, argv2]:
            options.default_translation.__init__(argv)
            result = []
            ctr = 0
            neg_ctr = 0
            project.playlist(result)
            for link, id in product(result, vid_links):
                if id in link: ctr += 1
                else: neg_ctr += 1
            self.assertEqual(ctr, len(result))
            self.assertEqual(neg_ctr, len(result)*(len(vid_links)-1))

        for argv, err in [(argv3, ConnectionError), (argv4, ValueError)]:
            options.default_translation.__init__(argv)
            result = []
            try:
                project.playlist(result)
            except err:
                self.assertTrue(True)  
            else:
                if len(result) != 0:
                    raise AssertionError

    def test_resolution(self):
        yt = pytube.YouTube("https://youtube.com/watch?v=159cF0O70f8")
        existing = [stream.resolution for stream in yt.streams.filter(progressive=True)]
        existing.remove('144p') # 144p not working mp4, only 3gpp
        existing.extend(['highest', 'lowest'])
        for arg in existing:
            project.resolution(yt.streams, arg)
        for arg in ['notexisting', '1080', '721p', '144p', '']:
            try:
                res = project.resolution(yt.streams, arg)
                if not res:
                    raise AssertionError
            except ValueError:
                self.assertTrue(True)

if __name__ == "__main__":
	unittest.main()