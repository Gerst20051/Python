# DEPENDENCIES
# - pydub

# USAGE
# [$]> python3 transcribe_audio_track.py [PATH_TO_AUDIO].mp3

import io
import speech_recognition as sr
import sys

from os import path
from pydub import AudioSegment

OUTPUT_FILE = path.expanduser('~/Downloads/VideoTranscriberFiles/transcript.txt')

def save_transcript(file, text):
  f = open(file, 'w')
  f.write(text)

(prefix, sep, suffix) = sys.argv[1].rpartition('.')

wave_filename = prefix + '.wav'

sound = AudioSegment.from_mp3(sys.argv[1])
sound.export(wave_filename, format='wav')

audio_file = sr.AudioFile(wave_filename)
recognizer = sr.Recognizer()

with audio_file as source:
  audio = recognizer.record(source)

transcript = recognizer.recognize_google(audio)

save_transcript(OUTPUT_FILE, transcript)

# from pydub import AudioSegment, silence

# print(silence.detect_silence(AudioSegment.silent(2000)))
# silence.split_on_silence()
# silence.detect_nonsilent()

# track = AudioSegment.from_mp3(sys.argv[1])
# audio = AudioSegment.from_mp3(sys.argv[1])

# buffer = io.BytesIO()
# track.export(buffer, format='wav')
# buffer.seek(0)

# audio = io.BytesIO()
# track.export(audio, format='wav')
# audio.seek(0)

# audio = AudioData()

# r = sr.Recognizer()
# audio = r.record(track)
# with sr.AudioFile(AUDIO_FILE) as source:
#   audio = r.record(source)

# audio = sr.AudioData(track, 16000, 2)

# audio = sr.AudioData(buffer.read(), 16000, 2)
# 'sample_rate' and 'sample_width'

# audio = sr.AudioData(buffer.read(), track.frame_rate, track.sample_width)

# recognize speech using Sphinx
# try:
#   print("Sphinx thinks you said " + r.recognize_sphinx(audio))
# except sr.UnknownValueError:
#   print("Sphinx could not understand audio")
# except sr.RequestError as e:
#   print("Sphinx error; {0}".format(e))

# recognize speech using Google Speech Recognition
# try:
#   # for testing purposes, we're just using the default API key
#   # to use another API key, use `r.recognize_google(audio, key="GOOGLE_SPEECH_RECOGNITION_API_KEY")`
#   # instead of `r.recognize_google(audio)`
#   print("Google Speech Recognition thinks you said " + r.recognize_google(audio))
# except sr.UnknownValueError:
#   print("Google Speech Recognition could not understand audio")
# except sr.RequestError as e:
#   print("Could not request results from Google Speech Recognition service; {0}".format(e))
