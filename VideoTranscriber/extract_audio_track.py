# DEPENDENCIES
# - pydub

# USAGE
# [$]> python3 extract_audio_track.py [PATH_TO_VIDEO].mp4 [NUM_SECONDS (optional)]

import sys

from os import path
from pydub import AudioSegment

NUM_SECONDS = int(sys.argv[2]) if len(sys.argv) == 3 else 0 # use 0 seconds to export the whole track
OUTPUT_FILE = path.expanduser('~/Downloads/VideoTranscriberFiles/test.mp3')

track = AudioSegment.from_file(sys.argv[1], 'mp4')

if NUM_SECONDS > 0:
  first_30_seconds = track[:NUM_SECONDS*1000]
  first_30_seconds.export(OUTPUT_FILE, format='mp3')
else:
  track.export(OUTPUT_FILE, format='mp3')
