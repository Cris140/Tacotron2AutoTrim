import speech_recognition as sr
from os import path
import os
filecount = len([name for name in os.listdir('/content/Tacotron2AutoTrim/output/wavs') if os.path.isfile(name)])

for x in range(1,filecount):
      AUDIO_FILE = path.join(path.dirname(path.realpath(__file__)), str(x)+".wav")
      # AUDIO_FILE = path.join(path.dirname(path.realpath(__file__)), "french.aiff")
      # AUDIO_FILE = path.join(path.dirname(path.realpath(__file__)), "chinese.flac")
      # use the audio file as the audio source
      r = sr.Recognizer()
      with sr.AudioFile(AUDIO_FILE) as source:
          audio = r.record(source)  # read the entire audio file
      try:
          # for testing purposes, we're just using the default API key
          # to use another API key, use `r.recognize_google(audio, key="GOOGLE_SPEECH_RECOGNITION_API_KEY")`
          # instead of `r.recognize_google(audio)`
          print("wavs/"+str(x)+".wav"+"|"+ r.recognize_google(audio, language="pt-BR"), file=open("/content/Tacotron2AutoTrim/output/list1.txt", "a"))
      except sr.UnknownValueError:
          print("Google Speech Recognition could not understand audio")
      except sr.RequestError as e:
          print("Could not request results from Google Speech Recognition service; {0}".format(e))