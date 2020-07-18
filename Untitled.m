
[x,fs] = audioread('E:\birdsound_datasets\ºìÊ÷ÁÖÄñÀàÉùÒô\myData\Pycnonotus_jocosus\XC19826-Pycnonotus_jocosus.mp3');
start_time = 0;
end_time = 5;
Y_new=x((fs*start_time+1):fs*end_time,1);
audiowrite('..\XC19826-Pycnonotus_jocosus.wav',Y_new,fs);