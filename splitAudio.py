# -*- coding: utf-8 -*-
from __future__ import division, print_function

import os
import math
import numpy as np
import librosa, soundfile
from pydub import AudioSegment
import sys

def view_bar(message, num, total):
    rate = num / total
    rate_num = int(rate * 40)
    rate_nums = math.ceil(rate * 100)
    r = '\r%s:[%s%s]%d%%\t%d/%d' % (message, ">" * rate_num, " " * (40 - rate_num), rate_nums, num, total,)
    sys.stdout.write(r)
    sys.stdout.flush()

def mkdir(fd):
    if not os.path.exists(fd):
        os.makedirs(fd)

def list_audio_files(folder):
    files = []
    for dirpath,d,f in os.walk(folder):
        for file in f:
            if file[-4:].lower()=='.wav':
                files.append(os.path.join(dirpath,file))
    return files

def read_audio(path, target_fs=None):
    (audio, fs) = soundfile.read(path)
    print(os.path.basename(path), fs, audio.shape, audio.shape[0]/fs)
    if audio.ndim > 1:
        audio = np.mean(audio, axis=1)
    if target_fs is not None and fs != target_fs:
        audio = librosa.resample(audio, orig_sr=fs, target_sr=target_fs)
        fs = target_fs
    return audio, fs

def write_audio(path, audio, sample_rate):
    soundfile.write(file=path, data=audio, samplerate=sample_rate)

def second_to_sample(t, sample_rate):
    return int(t*sample_rate)

def second_to_frame(t, sample_rate, n_window, n_overlap):
    return int(t*sample_rate/(n_window-n_overlap))

def sample_to_second(s, sample_rate):
    return float(1.0*s/sample_rate)

def sample_to_frame(s, n_window, n_overlap):
    return int(s/(n_window-n_overlap))

def mp3_to_wav(audio_dir, out_dir):
    files = []
    for dirpath,d,f in os.walk(audio_dir):
        for file in f:
            if file[-4:].lower() == '.mp3':
                files.append(os.path.join(dirpath, file))

    for file in files:
        AudioSegment.converter = "D:\\ffmpeg\\bin\\ffmpeg.exe"
        sound = AudioSegment.from_mp3(file)
        sound.export(file.replace('mp3', 'wav'), format="wav")

def split_audio(audio_dir, out_dir, target_fs=16000, clips_time=5):
    mkdir(out_dir)

    clips_len = second_to_sample(clips_time, target_fs)

    files = list_audio_files(audio_dir)
    for i, filename in enumerate(files):
        audio, fs = read_audio(filename, target_fs=target_fs)
        temp = 0
        for j in range(len(audio) // clips_len):
            clips = audio[j*clips_len : (j+1)*clips_len]
            clips_name = os.path.join(out_dir, os.path.basename(filename)[:-4]+'_'+str(j+1)+'.wav')
            write_audio(clips_name, clips, target_fs)
            temp = j+1
        if len(audio[temp*clips_len:])*1.0 / clips_len > 0.7 and temp > 0:
            clips = audio[-1*clips_len:]
            clips_name = os.path.join(out_dir, os.path.basename(filename)[:-4]+'_'+str(temp+1)+'.wav')
            write_audio(clips_name, clips, target_fs)

if __name__ == '__main__':          
    #pdb.set_trace() 
    audio_dir = '.\mp3\大白鹭'
    out_dir = '.\wav\Ardea_alba1'
    time = 5
    fs = 16000
    mp3_to_wav(audio_dir, out_dir)
    split_audio(audio_dir, out_dir, fs, time)
