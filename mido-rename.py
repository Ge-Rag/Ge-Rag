#!/usr/bin/python3

from mido import Message, MidiFile, MidiTrack, MetaMessage
import os
import time
import argparse
import re
import readline
from shutil import copy, copyfile
from datetime import datetime
import pathlib

parser = argparse.ArgumentParser()
parser.add_argument('-d', '--directory',
                    action='store',         # tell to store a value
                    dest='directory',        # use `username` to access value
                    type=pathlib.Path,
                    required=True,
                    help='The directory to search for MIDI files.')
parser.add_argument('-a', '--auto',
                    action='store',         # tell to store a value
                    dest='auto',        # use `username` to access value
                    type=bool,  
                    default=False,
                    help='If auto is defined then no prompting occurs!')
args = parser.parse_args()

if args.directory:
    midi_directory = str(args.directory)
    b = os.path.basename(midi_directory)
elif args.file:
    midi_directory = os.path.dirname(args.file)
    b = '0'
    
auto=args.auto
    
date_time = datetime.now().strftime("%Y%m%d_%H%M%S")
tmp_dir = '/tmp/midi' + os.sep + date_time

def rlinput(prompt, prefill=''):
   readline.set_startup_hook(lambda: readline.insert_text(prefill))
   try:
      return input(prompt)  
   finally:
      readline.set_startup_hook()

   
def process_file_worker( midi_file ):

    if midi_file is None:
        return
    start = time.time()
    try:
        mid = MidiFile(midi_file)
    except Exception as e:
        print("exception while parsing midi")   
        print(e)
        return
           
       
    print ( "Processing: " + midi_file )
    
    fnx_src = os.path.basename(midi_file)
    fnm_src = os.path.splitext(fnx_src)[0]
    
    title = ''

    for msg in mid:
        if msg.is_meta and msg.type == 'track_name':
            title = msg.name
            title = title.strip(' ')
          
    title = get_valid_filename(title)
    fnx_tgt = title + '.mid'
    fnx_tgt = get_valid_filename(fnx_tgt)
    f_tgt = midi_directory + os.sep + fnx_tgt    
    

    i=0
    t = title
    while os.path.exists(f_tgt):
        title =  t + '-' + str(i)
        fnx_tgt = title + '.mid'
        f_tgt = midi_directory + os.sep + fnx_tgt   
        print (title)
        i+=1
 
    if not args.auto:
        t = rlinput ( "Confirm or change name: ", title )
        if t:
            title = t    
        else:
            title = fnm_src
    else:
        if not title:
            title = fnm_src
     
    title = get_valid_filename(title)
    fnx_tgt = title + '.mid'
    fnm_tgt = os.path.splitext(fnx_tgt)[0]

    f_tgt = midi_directory + os.sep + fnx_tgt
    
    if os.path.exists(f_tgt):
        print ('File exists:', f_tgt)
        return

    htm_file = midi_directory + os.sep + fnm_src + '.htm'
    if os.path.exists(htm_file):
        copy(htm_file, tmp_dir)
        os.rename(htm_file, midi_directory + os.sep + fnm_tgt + '.htm')

    print ( "Target: " + f_tgt )            
        
    copy(midi_file, tmp_dir)
    os.rename(midi_file, f_tgt )
        
def get_valid_filename(fn):
	fn = str(fn).strip().replace(' ', '_')
	fn = re.sub(r'(?u)[^-\w.]', '', fn)	
	return re.sub(r'(?u)[-_]+', '_', fn)	
        

def main():

    if not os.path.exists(tmp_dir):
        try:
            os.mkdir(tmp_dir)
        except OSError:
            print ("Creation of the directory %s failed" % tmp_dir)
        else:
            print ("Successfully created the directory %s " % tmp_dir)

    print("Going to search:", midi_directory)

    start = time.time()

    midi_files = []
    for file in os.listdir(midi_directory):
        if ".mid" in file:
            midi_files.append(midi_directory + os.sep + file)
    
    print("Found", len(midi_files), "midi files.")
    print("Search took", time.time() - start)
      
    for file in midi_files:
        process_file_worker ( file )
    print("Done.")



if __name__ == "__main__":
    if args.directory:
        main()
    else:
        exit()
        
