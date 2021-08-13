"""
Basic tests for vimeo-downloader package
"""
from typing import List

import pytest
import requests

from vimeo_downloader import Vimeo, _Stream

TEST_DATA = [
    {'url': 'https://vimeo.com/503166067', 'title': "We Don't Have To Know - Keli Holiday"},
    {'url': 'https://player.vimeo.com/video/498617513', 'title': 'NEET ekalavya all',
     'embedded_on': 'https://atpstar.com/plans-162.html'},
    {'url': 'https://player.vimeo.com/video/528717721', 'title': 'ENGLISH LECTURE-11'},
]

VIDEO_ID_DATA = [
    {'url': 'https://player.vimeo.com/video/528717721', 'title': 'ENGLISH LECTURE-11',
     'video_id': '528717721'}
]


def test_metadata():
    v = Vimeo('https://vimeo.com/503166067')
    meta = v.metadata
    assert meta.title == "We Don't Have To Know - Keli Holiday"
    assert meta.views


def _check_all_streams_work(streams: List[_Stream], video_title: str):
    for stream in streams:
        r = requests.get(stream.direct_url, stream=True)
        assert r.ok
        assert stream.title == video_title


@pytest.mark.parametrize('video_information', TEST_DATA)
def test_download_video(video_information):
    kwargs_for_vimeo_obj = {'url': video_information['url']}
    if video_information.get('embedded_on'):
        kwargs_for_vimeo_obj['embedded_on'] = video_information['embedded_on']
    v = Vimeo(**kwargs_for_vimeo_obj)
    streams = v.streams
    assert streams
    _check_all_streams_work(streams, video_information['title'])


@pytest.mark.parametrize('video_information', VIDEO_ID_DATA)
def test_from_video_id(video_information):
    """
    Test that it selects the right video from video ID
    """
    video_id = video_information['video_id']
    v = Vimeo.from_video_id(video_id)
    assert v.streams[0].title == video_information['title']


def test_best_stream():
    v = Vimeo('https://vimeo.com/503166067')
    assert v.streams[-1].quality == v.best_stream.quality
