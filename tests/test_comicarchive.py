from os.path import abspath, dirname, join

from comicapi.comicarchive import ComicArchive, rar_support
import pytest

thisdir = dirname(abspath(__file__))

@pytest.mark.xfail("rar_support")
def test_getPageNameList():
    ComicArchive.logo_data = b""
    c = ComicArchive(join(thisdir, "data", "fake_cbr.cbr"))
    pageNameList = c.get_page_name_list()

    assert pageNameList == [
        "page0.jpg",
        "Page1.jpeg",
        "Page2.png",
        "Page3.gif",
        "page4.webp",
        "page10.jpg",
    ]
