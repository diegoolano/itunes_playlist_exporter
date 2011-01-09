#!/usr/bin/env python

import os
import sys
import codecs
import xml.etree.ElementTree as ET

from appscript import *
import tarfile

iTunes = app('iTunes')

playlists = iTunes.user_playlists()
def get_playlist_by_name(name):
	for pl in playlists:
		if pl.name() == name:	
			return pl
	return ''

def get_tracks_in_playlist(playlist):
	return playlist.file_tracks()

def get_songs_to_put_in_tar(name):
	pl = get_playlist_by_name(name)
	if pl != '':
		tr = get_tracks_in_playlist(pl)
		##can use id(), name(), artist(), album(), location(), year(), composer(),
		print "Putting the following in the tar file: "
		for t in tr:
			print t.location().path
		return tr
	else:
		print "Error: Did not find playlist with name: %s" % name
		return []


def make_tar_of_playlist(plname, tarname):
	trks = get_songs_to_put_in_tar(plname)
	if trks != []:
		tarname_with_ext = "%s.tar" % tarname
		tFile = tarfile.open(tarname_with_ext, 'w')
		for tr in trks:
			tmp = (tr.location().path).split('/')
			name = tmp[len(tmp) - 1]
			add_to = "%s/%s" % (plname,name)
			tFile.add(tr.location().path,add_to,False) #last False emits recursive directory structure (ie. original path to file) 

			

		for f in tFile.getnames():
		    print "Successfully Added %s" % f

		tFile.close()	
		print "Created: %s" % tarname_with_ext	
	

##usage python get_playlist_and_make_tar.py playlistname tarfilename 
if len(sys.argv) < 2:
	print "Usage python get_playlist_and_make_tar.py playlistname tarfilename"
	print "if no tarfilename, playlistname is used instead"
	sys.exit(1)

plname = sys.argv[1]
if len(sys.argv) < 3:
	tarname = plname
else:
	tarname = sys.argv[2]

make_tar_of_playlist(plname,tarname)
