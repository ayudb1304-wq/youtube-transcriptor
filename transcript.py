"""Fetch a YouTube video's transcript using youtube-transcript-api.

Usage: python transcript.py <video-url-or-id> [lang ...]
"""
import re
import sys

from youtube_transcript_api import YouTubeTranscriptApi


def video_id(arg):
    m = re.search(r"(?:v=|youtu\.be/|shorts/|embed/)([\w-]{11})", arg)
    return m.group(1) if m else arg


def main():
    if len(sys.argv) < 2:
        sys.exit(__doc__)
    vid = video_id(sys.argv[1])
    langs = sys.argv[2:] or ["en"]
    transcript = YouTubeTranscriptApi().fetch(vid, languages=langs)
    out = f"{vid}.txt"
    with open(out, "w") as f:
        for s in transcript:
            f.write(f"[{int(s.start // 60):02d}:{int(s.start % 60):02d}] {s.text}\n")
    print(f"Saved {len(transcript)} lines to {out}")


if __name__ == "__main__":
    main()
