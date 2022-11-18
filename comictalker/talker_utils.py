"""Generic sources utils to format API data and the like.
"""
# Copyright 2012-2014 Anthony Beville
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
from __future__ import annotations

import logging
import re
from datetime import datetime

from bs4 import BeautifulSoup

from comicapi import utils
from comicapi.genericmetadata import GenericMetadata
from comicapi.issuestring import IssueString
from comictaggerlib import ctversion
from comictalker.talkerbase import ComicIssue

logger = logging.getLogger(__name__)


def map_comic_issue_to_metadata(
    issue_results: ComicIssue, source: str, remove_html_tables: bool = False, use_year_volume: bool = False
) -> GenericMetadata:
    # Now, map the ComicIssue data to generic metadata
    metadata = GenericMetadata()
    metadata.is_empty = False

    # Is this best way to go about checking?
    if issue_results["volume"].get("name"):
        metadata.series = utils.xlate(issue_results["volume"]["name"])
    if issue_results.get("issue_number"):
        metadata.issue = IssueString(issue_results["issue_number"]).as_string()
    if issue_results.get("name"):
        metadata.title = utils.xlate(issue_results["name"])
    if issue_results.get("image_url"):
        metadata.cover_image = issue_results["image_url"]

    if issue_results["volume"].get("publisher"):
        metadata.publisher = utils.xlate(issue_results["volume"]["publisher"])

    if issue_results.get("cover_date"):
        metadata.day, metadata.month, metadata.year = utils.parse_date_str(issue_results["cover_date"])
    elif issue_results["volume"].get("start_year"):
        metadata.year = utils.xlate(issue_results["volume"]["start_year"], True)

    metadata.comments = cleanup_html(issue_results["description"], remove_html_tables)
    if use_year_volume:
        metadata.volume = issue_results["volume"]["start_year"]

    metadata.tag_origin = source
    metadata.issue_id = issue_results["id"]

    metadata.notes = (
        f"Tagged with ComicTagger {ctversion.version} using info from {source} on"
        f" {datetime.now():%Y-%m-%d %H:%M:%S}.  [Issue ID {issue_results['id']}]"
    )
    metadata.web_link = issue_results["site_detail_url"]

    for person in issue_results["credits"]:
        if "role" in person:
            roles = person["role"].split(",")
            for role in roles:
                # can we determine 'primary' from CV??
                metadata.add_credit(person["name"], role.title().strip(), False)

    if issue_results.get("characters"):
        metadata.characters = ", ".join(issue_results["characters"])
    if issue_results.get("teams"):
        metadata.teams = ", ".join(issue_results["teams"])
    if issue_results.get("locations"):
        metadata.locations = ", ".join(issue_results["locations"])
    if issue_results.get("story_arcs"):
        metadata.story_arc = ", ".join(issue_results["story_arcs"])

    return metadata


def parse_date_str(date_str: str) -> tuple[int | None, int | None, int | None]:
    day = None
    month = None
    year = None
    if date_str:
        parts = date_str.split("-")
        year = utils.xlate(parts[0], True)
        if len(parts) > 1:
            month = utils.xlate(parts[1], True)
            if len(parts) > 2:
                day = utils.xlate(parts[2], True)
    return day, month, year


def cleanup_html(string: str, remove_html_tables: bool) -> str:
    if string is None:
        return ""
    # find any tables
    soup = BeautifulSoup(string, "html.parser")
    tables = soup.findAll("table")

    # remove all newlines first
    string = string.replace("\n", "")

    # put in our own
    string = string.replace("<br>", "\n")
    string = string.replace("</li>", "\n")
    string = string.replace("</p>", "\n\n")
    string = string.replace("<h1>", "*")
    string = string.replace("</h1>", "*\n")
    string = string.replace("<h2>", "*")
    string = string.replace("</h2>", "*\n")
    string = string.replace("<h3>", "*")
    string = string.replace("</h3>", "*\n")
    string = string.replace("<h4>", "*")
    string = string.replace("</h4>", "*\n")
    string = string.replace("<h5>", "*")
    string = string.replace("</h5>", "*\n")
    string = string.replace("<h6>", "*")
    string = string.replace("</h6>", "*\n")

    # remove the tables
    p = re.compile(r"<table[^<]*?>.*?</table>")
    if remove_html_tables:
        string = p.sub("", string)
        string = string.replace("*List of covers and their creators:*", "")
    else:
        string = p.sub("{}", string)

    # now strip all other tags
    p = re.compile(r"<[^<]*?>")
    newstring = p.sub("", string)

    newstring = newstring.replace("&nbsp;", " ")
    newstring = newstring.replace("&amp;", "&")

    newstring = newstring.strip()

    if not remove_html_tables:
        # now rebuild the tables into text from BSoup
        try:
            table_strings = []
            for table in tables:
                rows = []
                hdrs = []
                col_widths = []
                for hdr in table.findAll("th"):
                    item = hdr.string.strip()
                    hdrs.append(item)
                    col_widths.append(len(item))
                rows.append(hdrs)

                for row in table.findAll("tr"):
                    cols = []
                    col = row.findAll("td")
                    i = 0
                    for c in col:
                        item = c.string.strip()
                        cols.append(item)
                        if len(item) > col_widths[i]:
                            col_widths[i] = len(item)
                        i += 1
                    if len(cols) != 0:
                        rows.append(cols)
                # now we have the data, make it into text
                fmtstr = "|"
                for w in col_widths:
                    fmtstr += f" {{:{w + 1}}}|"
                table_text = ""
                counter = 0
                for row in rows:
                    table_text += fmtstr.format(*row) + "\n"
                    if counter == 0 and len(hdrs) != 0:
                        table_text += "|"
                        for w in col_widths:
                            table_text += "-" * (w + 2) + "|"
                        table_text += "\n"
                    counter += 1

                table_strings.append(table_text + "\n")

            newstring = newstring.format(*table_strings)
        except Exception:
            # we caught an error rebuilding the table.
            # just bail and remove the formatting
            logger.exception("table parse error")
            newstring.replace("{}", "")

    return newstring
