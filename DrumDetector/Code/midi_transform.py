import mido
import numpy as np
from mido.midifiles.tracks import merge_tracks
'''
midi_matric_col_num mora se poklapati sa brojem kolona spektrograma
time_interval predstavlja vremenski interval jedne kolone spektrograma. koristimo ga da bi sihronizovali udarce bubnjeva u spektrogramu sa udardima u midi matrici
'''
def midi_transform(midi_file, midi_matrix_col_num, time_interval, midi_notes):
    ret_mat = np.zeros((len(midi_notes), midi_matrix_col_num))
    
    for msg in merge_tracks(midi_file.tracks):
        if msg.type == 'set_tempo':
            tempo = msg.tempo    
    time_of_tick = mido.tick2second(1, midi_file.ticks_per_beat, tempo)
    
    #print 'jedan tick traje ' + str(time_of_tick) + ' sekundi'
    #print 'vremenski interval jedne kolone je ' + str(time_interval)
    #print 'u jedanu kolonu stane ' + str(time_interval/time_of_tick) + 'tickova'
    ticks_per_col = time_interval/time_of_tick
    
    num_of_ticks = 0 #broj tickova 
    for msg in merge_tracks(midi_file.tracks):
        num_of_ticks += msg.time
        if msg.type == 'note_on':
            if msg.note in midi_notes:
                ret_mat[midi_notes[msg.note], int(num_of_ticks/ticks_per_col):] = msg.velocity
        if msg.type == 'note_off':
            if msg.note in midi_notes:
                ret_mat[midi_notes[msg.note], int(num_of_ticks/ticks_per_col):] = 0 
        #print msg

    return ret_mat
