#@title Now use this cell to transcribe the file
from google.colab import files

skip_large_duration_files ="No" #@param ["Yes", "No"]
max_duration_of_audio ="20"#@param {type: "string"}
minimum_silence_length ="200" #@param {type: "string"}
silence_threshold ="-40" #@param {type: "string"}
Language ="Brazilian Portuguese"#@param ["English", "Spanish", "French", "German", "Italian", "Japanese", "Russian", "Brazilian Portuguese", "Polish", "Arabic"]
max_duration_of_audio = int(max_duration_of_audio)
silence_threshold = int(silence_threshold)
minimum_silence_length = int(minimum_silence_length)

import re

from pydub import AudioSegment
from pydub.silence import split_on_silence

import glob
import os

import wave
import contextlib

import transcribe

if __name__ == '__main__':
    
    import imageio
    imageio.plugins.ffmpeg.download()

    file_number = 1

    input_file = "audio.mp3"

    lang = ''
    
    lang_input = Language

    _encoding = 'utf-8'

    if lang_input.strip().lower() == 'english':
        lang = 'en-US'
    elif lang_input.strip().lower() == 'spanish':
        lang = 'es-ES'
    elif lang_input.strip().lower() == 'french':
        lang = 'fr-FR'
    elif lang_input.strip().lower() == 'german':
        lang = 'de-DE'
    elif lang_input.strip().lower() == 'italian':
        lang = 'it-IT'
    elif lang_input.strip().lower() == 'japanese':
        lang = 'ja'
        _encoding = 'utf-16'
    elif lang_input.strip().lower() == 'russian':
        lang = 'ru'
    elif lang_input.strip().lower() == 'arabic':
        lang = 'ar-EG'
    elif lang_input.strip().lower() == 'brazilian portuguese':
        lang = 'pt-BR'
    elif lang_input.strip().lower() == 'polish':
        lang = 'pl-PL'
    else:
        print('Invalid language!')
        import sys
        import time
        time.sleep(2)
        sys.exit(0)

    min_silence_len_var = minimum_silence_length
    silence_thresh_var = silence_threshold

    skip_large_duration_files_input = skip_large_duration_files
    if skip_large_duration_files_input.strip().lower() == 'yes':
        skip_large_duration_files = True
    elif skip_large_duration_files_input.strip().lower() == 'no':
        skip_large_duration_files = False
    else:
        skip_large_duration_files = True
    
    if skip_large_duration_files:
        max_dur_audio = max_duration_of_audio
    else:
        max_dur_audio = 12

    # assign files
    input_file = 'input/' + input_file

    # create dir if doesn't exist
    os.makedirs(os.path.dirname('input/'), exist_ok=True)
    os.makedirs(os.path.dirname('output/'), exist_ok=True)
    os.makedirs(os.path.dirname('output/wavs/'), exist_ok=True)

    sound_file = AudioSegment.from_file(input_file)
    sound_file = sound_file.set_frame_rate(22050)  # don't change this
    sound_file = sound_file.set_channels(1)  # don't change this
    audio_chunks = split_on_silence(sound_file, min_silence_len=min_silence_len_var,  # 1000 cuts at 1 second of silence. 500 is 0.5 sec
                                    silence_thresh=silence_thresh_var)

    for i, chunk in enumerate(audio_chunks):

        if not len(os.listdir('output/wavs')) == 0:
            list_of_files = glob.glob('output/wavs/*')  # * means all
            latest_file = max(list_of_files, key=os.path.getctime)

            # Extract numbers and cast them to int
            list_of_nums = re.findall('\\d+', latest_file)

            if int(list_of_nums[0]) >= file_number:
                file_number = int(list_of_nums[0]) + 1

        out_file = "output/wavs/{0}.wav".format(file_number)
        print("exporting", out_file + '\n')

        chunk.export(out_file, format="wav")

        fname = out_file
        with contextlib.closing(wave.open(fname, 'r')) as f:
            frames = f.getnframes()
            rate = f.getframerate()
            duration = frames / float(rate)
            #print('Duration:', duration)
from distutils.dir_util import copy_tree
copy_tree("/content/Tacotron2AutoTrim/output/wavs", "/content/Tacotron2AutoTrim/output/adittional")
from pydub import AudioSegment
from pydub.playback import play
import os

path, dirs, files = next(os.walk("/content/Tacotron2AutoTrim/output/wavs/"))
file_count = len(files)
for x in range(1,file_count+1):

  input_wav_file   = "/content/Tacotron2AutoTrim/output/wavs/"+str(x)+".wav"
  output_wav_file  = (input_wav_file)
  target_wav_time  = 5 * 1000 # 5 seconds (or 5000 milliseconds)

  original_segment = AudioSegment.from_wav(input_wav_file)
  silence_duration = target_wav_time - len(original_segment)
  silenced_segment = AudioSegment.silent(duration=silence_duration)
  combined_segment = original_segment + silenced_segment
  combined_segment.export(output_wav_file, format="wav") 
import speech_recognition as sr
from os import path
import os
__file__ = 'trans.py'
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
          print("wavs/"+str(x)+".wav"+"|"+r.recognize_google(audio, language="pt-BR"), file=open("/content/Tacotron2AutoTrim/output/list1.txt", "a"))
      except sr.UnknownValueError:
          print("Google Speech Recognition could not understand audio")
      except sr.RequestError as e:
          print("Could not request results from Google Speech Recognition service; {0}".format(e))
import os

if not os.path.exists('/content/Tacotron2AutoTrim/output/list1.txt'):
    os.mknod('/content/Tacotron2AutoTrim/output/list1.txt')
with open('/content/Tacotron2AutoTrim/output/list1.txt', 'r') as istr:
    with open('/content/Tacotron2AutoTrim/output/list2.txt', 'w') as ostr:
        for line in istr:
            line = line.rstrip('\n') + '.'
            print(line, file=ostr)

copy_tree("/content/Tacotron2AutoTrim/output/adittional", "/content/Tacotron2AutoTrim/output/wavs")

dir_path = '/content/Tacotron2AutoTrim/output/adittional'

try:
    os.rmdir(dir_path)
except OSError as e:
    print("Error: %s : %s" % (dir_path, e.strerror))
!rm /content/Tacotron2AutoTrim/output/list1.txt
!mv /content/Tacotron2AutoTrim/output/list2.txt /content/Tacotron2AutoTrim/output/list.txt
#@markdown ###Deixe essa opção desativada se quiser transcrever usando wav2vec2
baixar_arquivo_ao_finalizar = True #@param{type:"boolean"}
%cd /content/Tacotron2AutoTrim/
if baixar_arquivo_ao_finalizar==True:
    !zip -r /content/dataset.zip /content/Tacotron2AutoTrim/output
    files.download("/content/dataset.zip")
else:
    !rm /content/Tacotron2AutoTrim/input/audio.mp3
