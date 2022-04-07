#@title Now use this cell to transcribe the file
from google.colab import files
import shutil
import os
import sys
from natsort import natsorted
erase_audios_that_google_couldnt_transcribe = False #@param{type:"boolean"}
file_exists1 = os.path.exists('/content/dataset/wavs')
if file_exists1==True:
    dir1= "/content/dataset/wavs/"
    txt_file = "/content/dataset/list.txt"
    # checking whether file exists or not
    if os.path.exists(txt_file):
        # removing the file using the os.remove() method
        os.remove(txt_file)
    else:
        # file not found message
        print("File not found in the directory")
    mp3_file = "/content/input/audio.mp3"
    # checking whether file exists or not
    if os.path.exists(mp3_file):
        # removing the file using the os.remove() method
        os.remove(mp3_file)
    try:
        shutil.rmtree(dir1)
    except OSError as e:
        print("Error: %s - %s." % (e.filename, e.strerror))
    dir2= "/content/wavs1/"
    try:
        shutil.rmtree(dir2)
    except OSError as e:
        print("Error: %s - %s." % (e.filename, e.strerror))
    # removing the file using the os.remove() method
    os.remove(file_path)
skip_large_duration_files ="No" #@param ["Yes", "No"]
max_duration_of_audio ="20"#@param {type: "string"}
minimum_silence_length ="200" #@param {type: "string"}
silence_threshold ="-40" #@param {type: "string"}
Language ="Brazilian Portuguese"#@param ["English", "Spanish", "French", "German", "Italian", "Japanese", "Russian", "Brazilian Portuguese", "Polish", "Arabic", "Turkish", "Zulu", "Slovak", "Mandarin Chinese", "Czech", "Korean"]
max_duration_of_audio = int(max_duration_of_audio)
silence_threshold = int(silence_threshold)
minimum_silence_length = int(minimum_silence_length)
lang = ''
  
lang_input = Language
if Language == 'English':
    Language = 'en-US'
elif Language == 'Spanish':
    Language = 'es-ES'
elif Language == 'French':
    Language = 'fr-FR'
elif Language == 'German':
    Language = 'de-DE'
elif Language == 'Italian':
    Language = 'it-IT'
elif Language == 'Japanese':
    Language = 'ja'
    _encoding = 'utf-16'
elif Language == 'Russian':
    Language = 'ru'
elif Language =='Arabic':
    Language = 'ar-EG'
elif Language == 'Brazilian Portuguese':
    Language = 'pt-BR'
elif Language == 'Polish':
    Language = 'pl-PL'
elif Language == 'Turkish':
    Language = 'tr'
elif Language == 'Zulu':
    Language = 'zu'
elif Language == 'Slovak':
    Language = 'sk'
elif Language == 'Mandarin Chinese':
    Language = 'zh-CN'
elif Language == 'Czech':
    Language = 'cs'
elif Language == 'Korean':
    Language = 'ko-KR'
else:
    print('Invalid Language!')
import re
import shutil
import sys
from pydub import AudioSegment
from pydub.silence import split_on_silence
import speech_recognition as sr
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


    _encoding = 'utf-8'
file_exists = os.path.exists('/content/input/audio.mp3')
if file_exists==True:
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
    input_file = '/content/input/' + input_file

    # create dir if doesn't exist
    os.makedirs(os.path.dirname('/content/wavs/'), exist_ok=True)

    sound_file = AudioSegment.from_file(input_file)
    sound_file = sound_file.set_frame_rate(22050)  # don't change this
    sound_file = sound_file.set_channels(1)  # don't change this
    audio_chunks = split_on_silence(sound_file, min_silence_len=min_silence_len_var,  # 1000 cuts at 1 second of silence. 500 is 0.5 sec
                                    silence_thresh=silence_thresh_var)

    for i, chunk in enumerate(audio_chunks):

        if not len(os.listdir('/content/wavs')) == 0:
            list_of_files = glob.glob('/content/wavs/*')  # * means all
            latest_file = max(list_of_files, key=os.path.getctime)

            # Extract numbers and cast them to int
            list_of_nums = re.findall('\\d+', latest_file)

            if int(list_of_nums[0]) >= file_number:
                file_number = int(list_of_nums[0]) + 1

        out_file = "/content/wavs/{0}.wav".format(file_number)
        print("exporting", out_file + '\n')

        chunk.export(out_file, format="wav")

        fname = out_file
        with contextlib.closing(wave.open(fname, 'r')) as f:
            frames = f.getnframes()
            rate = f.getframerate()
            duration = frames / float(rate)
            #print('Duration:', duration)

path, dirs, files1 = next(os.walk("/content/wavs/"))
file_count = len(files1)
if os.path.isdir('/content/wavs1')==False:
    shutil.copytree('/content/wavs', '/content/wavs1')
arquivos = os.listdir("/content/wavs1/")
for file in natsorted(arquivos):

  input_wav_file   = '/content/wavs1/'+file
  output_wav_file  = input_wav_file
  target_wav_time  = 5 * 1000 # 5 seconds (or 5000 milliseconds)

  original_segment = AudioSegment.from_wav(input_wav_file)
  silence_duration = target_wav_time - len(original_segment)
  silenced_segment = AudioSegment.silent(duration=silence_duration)
  combined_segment = original_segment + silenced_segment
  combined_segment.export(output_wav_file, format="wav") 

# obtain path to "english.wav" in the same folder as this script
from os import path
__file__ = 'trans.py'
# use the audio file as the audio source
file_exists = os.path.exists('/content/input/audio.mp3')
if file_exists==True:
      pasta1="/content/wavs1/"
else:
      pasta1="/content/wavs/"
os.chdir(pasta1)
arquivos1 = os.listdir("/content/wavs1/")
for file in natsorted(arquivos1):
      pastaaudio = "/content/wavs1/"
      AUDIO_FILE = pastaaudio + file
      r = sr.Recognizer()
      with sr.AudioFile(AUDIO_FILE) as source:
          audio = r.record(source)  # read the entire audio file    
      try:
          # for testing purposes, we're just using the default API key
          # to use another API key, use `r.recognize_google(audio, key="GOOGLE_SPEECH_RECOGNITION_API_KEY", show_all=True)`
          # instead of `r.recognize_google(audio, show_all=True)`
          print("wavs/"+file+"|"+ r.recognize_google(audio, language=Language), file=open("/content/dataset/list1.txt", "a"))
      except sr.UnknownValueError:
           if erase_audios_that_google_couldnt_transcribe:
                os.remove("/content/wavs/"+file)
           else:
                print("Google wasn't able to transcribe the audio "+file+", Skipping it...")
      except sr.RequestError as e:
          print("Could not request results from Googleeech Recognition service; {0}".format(e))
%cd /content/
with open('/content/dataset/list1.txt', 'r') as istr:
    with open('/content/dataset/list2.txt', 'w') as ostr:
        for line in istr:
            line = line.rstrip('\n') + '.'
            print(line, file=ostr)

#@markdown ###Let this option turned off if you want to use wav2vec2 to transcribe
download_dataset_when_finished = True #@param{type:"boolean"}
!rm /content/dataset/list1.txt
!mv /content/dataset/list2.txt /content/dataset/list.txt
shutil.move("/content/wavs","/content/dataset")
pasta="/content/wavs1"
try:
    shutil.rmtree(pasta)
except OSError as e:
    print("Error: %s - %s." % (e.filename, e.strerror))
if download_dataset_when_finished==True:
      !zip -r /content/dataset.zip /content/dataset/      
      files.download("/content/dataset.zip")
else:
    !rm /content/input/audio.mp3
