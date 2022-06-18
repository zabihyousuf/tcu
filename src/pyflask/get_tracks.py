from RaceTrack import *


def get_tracks():
    track_list = []
    tracks = []

    with open("tracks.txt", 'r') as trackFile:
        tracks = [x.strip() for x in trackFile.readlines()]

    for i in tracks:
        i = i.split(',')
        track_list.append(RaceTrack(i[0], i[1], i[2], i[3]))

    return track_list
