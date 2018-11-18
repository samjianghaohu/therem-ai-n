from mido import MidiFile, Message, MidiTrack
from pyo import *

def playOutputMidi():
    mid = MidiFile('midfile/returning.mid')
    print("midi file read")
    if len(mid.tracks) != 1:
        midTrack = mid.tracks[0]
        mid.tracks.remove(midTrack)


    messages = []

    mid.tracks[0].name = "mainTrack"

    for track in mid.tracks:
        for msg in track:
            if not msg.is_meta:
                if msg.type == "note_on":
                    messages.append(msg)


    s = Server().boot()
    s.start()
    sig2 = Sine(1, 0).out()

    tempFreq = 0.0

    for idx,msg in enumerate(mid.play()):
        if idx < len(messages):
            if messages[idx].note > 96:
                frequencyFromMidi = midiToHz(messages[idx].note - 12)
            else:
                frequencyFromMidi = midiToHz(messages[idx].note + 24)
            print(frequencyFromMidi)
            # if frequencyFromMidi != tempFreq:
            
            sig2.set("freq", frequencyFromMidi, port = 1)
            tempFreq = frequencyFromMidi
