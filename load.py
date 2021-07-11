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

    input_file = input('Enter the name of the input file (include extension): ')

    lang = ''

    print('\n[INFO] If you leave the following fields blank it will use the default value, displayed at the left side.')

    print('\nSUPPORTED LENGUAGES: English, Spanish, French, German, Italian, Japanese, Russian, Polish, Arabic')
    lang_input = input('[English] What lenguage is spoken in your input audio?: ') or 'English'

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
    elif lang_input.strip().lower() == 'polish':
        lang = 'pl-PL'
    else:
        print('Invalid language!')
        import sys
        import time
        time.sleep(2)
        sys.exit(0)

    min_silence_len_var = int(input('[750] Enter min silence len (1000 cuts at 1 second of silence, 500 is 0.5 sec): ') or 750)
    silence_thresh_var = int(input('[-40] Enter silence thresh: ') or -40)

    skip_large_duration_files_input = input('[Yes] Do you want to skip large duration files? (type "yes" or "no"): ')
    if skip_large_duration_files_input.strip().lower() == 'yes':
        skip_large_duration_files = True
    elif skip_large_duration_files_input.strip().lower() == 'no':
        skip_large_duration_files = False
    else:
        skip_large_duration_files = True
    
    if skip_large_duration_files:
        max_dur_audio = int(input('[12] Enter max audio duration: ') or 12)
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

        if skip_large_duration_files:
            if duration < max_dur_audio:
                transcription = transcribe.get_large_audio_transcription(out_file, lang)

                if transcription != '':
                    if os.path.isfile('output/list.txt'):
                        if os.stat("output/list.txt").st_size != 0:
                            with open('output/list.txt', 'a+', encoding=_encoding) as f:
                                f.write(f'\nwavs/{file_number}.wav|' + transcription)
                                f.flush()
                        else:
                            with open('output/list.txt', 'a+', encoding=_encoding) as f:
                                f.write(f'wavs/{file_number}.wav|' + transcription)
                                f.flush()
                    else:
                        with open('output/list.txt', 'x', encoding=_encoding) as f:
                            f.write(f'wavs/{file_number}.wav|' + transcription)

                    file_number = file_number + 1
                else:
                    os.remove(out_file)
            else:
                os.remove(out_file)

        else:
            transcription = transcribe.get_large_audio_transcription(out_file, lang)

            if transcription != '':
                if os.path.isfile('output/list.txt'):
                    if os.stat("output/list.txt", encoding=_encoding).st_size != 0:
                        with open('output/list.txt', 'a+') as f:
                            f.write(f'\nwavs/{file_number}.wav|' + transcription)
                            f.flush()
                    else:
                        with open('output/list.txt', 'a+', encoding=_encoding) as f:
                            f.write(f'wavs/{file_number}.wav|' + transcription)
                            f.flush()
                else:
                    with open('output/list.txt', 'x', encoding=_encoding) as f:
                        f.write(f'wavs/{file_number}.wav|' + transcription)

                file_number = file_number + 1
            else:
                os.remove(out_file)
