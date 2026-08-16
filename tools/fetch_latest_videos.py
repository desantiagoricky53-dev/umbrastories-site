#!/usr/bin/env python3
"""Fetch each YouTube channel's newest upload (public RSS, no API key)
and write latest-videos.json at the repo root.

A channel whose feed fails or has no uploads yet is simply omitted —
partial success still writes the file. The site's JS treats a missing
entry (or a missing file) as "render the card exactly as before".
"""
import json
import sys
import urllib.request
import xml.etree.ElementTree as ET
from datetime import datetime, timezone
from pathlib import Path

CHANNELS = {
    "@UmbraColdCase":   "UCBjQIt1muTvDO4VsoIDK2ww",
    "@UmbraCasos":      "UC17wU8QrpqJFaJDHziz3t2Q",
    "@UmbraAfterDark":  "UCFJ_F8m-6hFXJQlgoa7djFA",
    "@UmbraNocturno":   "UCG8r7fqhH3tG-sh0hLnc3CA",
    "@UmbraFirsthand":  "UCNW3ZG_MbL5_funzweyXS-A",
    "@UmbraTestimonios": "UCcGiaDP_c5f4nNgbq_1NbWA",
}

NS = {
    "atom": "http://www.w3.org/2005/Atom",
    "yt": "http://www.youtube.com/xml/schemas/2015",
}

OUT = Path(__file__).resolve().parent.parent / "latest-videos.json"


def newest_entry(channel_id):
    url = "https://www.youtube.com/feeds/videos.xml?channel_id=" + channel_id
    with urllib.request.urlopen(url, timeout=10) as resp:
        root = ET.fromstring(resp.read())
    entry = root.find("atom:entry", NS)  # feed entries are newest-first
    if entry is None:
        return None
    video_id = entry.findtext("yt:videoId", default="", namespaces=NS)
    title = entry.findtext("atom:title", default="", namespaces=NS)
    published = entry.findtext("atom:published", default="", namespaces=NS)
    if not video_id or not title:
        return None
    return {
        "title": title,
        "url": "https://www.youtube.com/watch?v=" + video_id,
        "videoId": video_id,
        "published": published,
    }


def main():
    channels = {}
    for handle, channel_id in CHANNELS.items():
        try:
            entry = newest_entry(channel_id)
        except Exception as exc:
            print("skip %s: %s" % (handle, exc), file=sys.stderr)
            continue
        if entry is None:
            print("skip %s: no uploads in feed" % handle, file=sys.stderr)
            continue
        channels[handle] = entry

    data = {
        "generated": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "channels": channels,
    }
    OUT.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n",
                   encoding="utf-8")
    print("wrote %s — %d/%d channels" % (OUT.name, len(channels), len(CHANNELS)))


if __name__ == "__main__":
    main()
