# DEPENDENCIES
# - pydub

# USAGE
# [$]> python3 visualize_audio_track.py [PATH_TO_AUDIO].mp3

import matplotlib.pyplot as plt
import sys

from pydub import AudioSegment

track = AudioSegment.from_mp3(sys.argv[1])

plt.title('hello sound wave')
plt.ylabel('Amplitude')
plt.xlabel('Time (seconds)')

# Add the hello sound data to the plot
plt.plot(time_gm, soundwave_gm, label='hello', alpha=0.5)
plt.legend()
plt.show()
