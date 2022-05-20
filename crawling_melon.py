#!/usr/bin/python3
# -*- coding: utf-8 -*-

import re
import sys

import requests
from bs4 import BeautifulSoup

URL_MELON_PREFIX = "https://www.melon.com/chart"

URL_SONG_PREFIX = ""
URL_ARTIST_PREFIX = "https://www.melon.com/artist/timeline.htm?artistId="
URL_ALBUM_PREFIX = "https://www.melon.com/album/detail.htm?albumId="


class Melon:
    def __init__(self, song, song_id, artist, artist_id, album, album_id):
        self.song = song
        self.song_id = song_id
        self.artist = artist
        self.artist_id = artist_id
        self.album = album
        self.album_id = album_id

    def __str__(self):
        return (f"\nSONG[{self.song}%{self.song_id}], ARTIST[{self.artist}%{self.artist_id}], ALBUM[{self.album}%{self.album_id}]"
                f"\nARTIST URL[{self.get_url_artist()}], ALBUM URL[{self.get_url_album()}]\n")

    def __repr__(self):
        return str(self)

    def get_url_song(self):
        print(f"Not supported [{self.get_url_song.__name__}]")
        return ""

    def get_url_artist(self):
        return f"{URL_ARTIST_PREFIX}{self.artist_id}"

    def get_url_album(self):
        return f"{URL_ALBUM_PREFIX}{self.album_id}"


def get_items(url):

    print(f"URL : {url}")

    results = []

    session = requests.Session()
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,image/svg+xml,image/*,*/*;q=0.8",
        "Connection": "close"
    }
    bs_obj = BeautifulSoup(session.get(
        url, headers=headers).content, "html.parser")
    tbody = bs_obj.find("tbody")
    tr_all = tbody.find_all("tr")

    for tr_each in tr_all:
        a_song = tr_each.find("div", {"class": "ellipsis rank01"}).find("a")
        song_name = a_song.get_text().strip().replace("\n", "")
        song_id = re.findall("\\(([^)]+)", a_song["href"])[0]
        a_artist = tr_each.find("div", {"class": "ellipsis rank02"}).find("a")
        artist_name = a_artist.get_text().strip().replace("\n", "")
        artist_id = re.findall("\\(\'([^')]+)", a_artist["href"])[0]
        a_album = tr_each.find("div", {"class": "ellipsis rank03"}).find("a")
        album_name = a_album.get_text().strip().replace("\n", "")
        album_id = re.findall("\\(\'([^')]+)", a_album["href"])[0]
        results.append(Melon(song_name, song_id, artist_name,
                       artist_id, album_name, album_id))

    return results


def get_items_for_weekly(start_yyyymmdd, finish_yyyymmdd):
    url = f"{URL_MELON_PREFIX}/week/index.htm?classCd=DM0000&moved=Y&startDay={start_yyyymmdd}&endDay={finish_yyyymmdd}"
    return get_items(url)


def get_items_for_monthly(yyyymm):
    url = f"{URL_MELON_PREFIX}/month/index.htm?classCd=DM0000&moved=Y&rankMonth={yyyymm}"
    return get_items(url)


if __name__ == "__main__":
    if len(sys.argv) == 3:
        melon_items = get_items_for_weekly(sys.argv[1], sys.argv[2])
    elif len(sys.argv) == 2:
        melon_items = get_items_for_monthly(sys.argv[1])
    else:
        sys.exit(1)

    print(melon_items)
