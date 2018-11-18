from predict import generate_midi
from midi_play import playOutputMidi

import pretty_midi
import time
import random
import keyboard

#def map_int(value, origin_min, origin_max, target_min, target_max):
#    origin_dataLen = origin_max - origin_min
#    target_dataLen = target_max - target_min
#    ret_val = target_min + target_dataLen*(value-origin_min)/origin_dataLen
#    return int(ret_val)

def predict(pitchNums):
    now = time.time()

    #initialize midi data and instrument
    midi_data = pretty_midi.PrettyMIDI()
    myInstru = pretty_midi.Instrument(program=0)

    timeTracker = 0.0 #track the entire duration of the input midi data
    #generate midi notes and append to the midi instrument
    for i in pitchNums:
        randDura = 0.1
        note = pretty_midi.Note(velocity=100, pitch=i, start=timeTracker, end=timeTracker+randDura)
        myInstru.notes.append(note)
        timeTracker += randDura

    # print("my notes:")
    # print(myInstru.notes)
    midi_data.instruments.append(myInstru)

    duration = timeTracker + 1.0
    # print("this is duration")
    # print(duration)


    ret_midi = generate_midi(midi_data, duration)

    ret_midi_data = pretty_midi.PrettyMIDI(ret_midi)
    print("returned midi")

    playOutputMidi()
    # keyboard.press_and_release('p')

    #print(ret_midi_data.instruments)

    #return ret_midi
test = [64, 64, 52, 83]
predict(test)
