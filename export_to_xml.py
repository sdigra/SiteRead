from pymusicxml import *
from music21 import *
from random import choice, choices
from nb_train import get_key

def generate_example():
    score = Score(title="Algorithmically Generated MusicXML", composer="HTMLvis")
    part = Part("Piano")
    score.append(part)

    pitch_bank = ["f#4", "bb4", "d5", "e5", "ab5", "c6", "f6"]

    measures = []

    for i in range(20):
        m = Measure(time_signature=(3, 4) if i == 0 else None)
        for beat_num in range(3):
            if (i + beat_num) % 3 == 0:
                # one quarter note triad
                m.append(Chord(choices(pitch_bank, k=3), 1.0))
            elif (i + beat_num) % 3 == 1:
                # two eighth note dyads
                m.append(BeamedGroup([Chord(choices(pitch_bank, k=2), 0.5) for _ in range(2)]))
            else:
                # four 16th note notes
                m.append(BeamedGroup([Note(choice(pitch_bank), 0.25) for _ in range(4)]))
        measures.append(m)
        
    part.extend(measures)
    score.export_to_file("AlgorithmicExample.musicxml")

    melody = converter.parse("AlgorithmicExample.musicxml")
    melody.show() # YOU NEED MUSESCORE TO RUN THIS

def generate_from_input(quarter_notes, half_notes, eighth_notes, whole_notes, quarter_rests, half_rests, eighth_rests, whole_rests, sixteenth_rests):
    score = Score(title="Algorithmically Generated MusicXML", composer="HTMLvis")
    part = Part("Piano") #need to receive instrument name from data
    score.append(part)

    # 1 top of staff, 8 bottom of staff
    pitch_bank = {1 : "f5", 2: "e5", 3: "d5", 4: "c5", 5: "b4", 6: "a4", 7: "g4", 8: "f4"}

    # assume treble clef?

    measures = []
    m = Measure(time_signature=(4, 4))

    for i in range (len(quarter_notes)):
        m = Measure(time_signature=(4, 4) if i == 0 else None)
        for beat_num in range(4):
            if (i + beat_num) % 4 == 0:
                m.append(Note(pitch_bank[get_key(i)], 1.0))
        measures.append(m)

    for i in range (len(half_notes)):
        m = Measure(time_signature=(4, 4) if i == 0 else None)
        for beat_num in range(4):
            if (i + beat_num) % 4 == 0:
                m.append(Note(pitch_bank[get_key(i)], 2.0))
        measures.append(m)

    for i in range (len(eighth_notes)):
        m = Measure(time_signature=(4, 4) if i == 0 else None)
        for beat_num in range(4):
            if (i + beat_num) % 4 == 0:
                m.append(Note(pitch_bank[get_key(i)], 0.5))
        measures.append(m)

    for i in range (len(whole_notes)):
        m = Measure(time_signature=(4, 4) if i == 0 else None)
        for beat_num in range(4):
            if (i + beat_num) % 4 == 0:
                m.append(Note(pitch_bank[get_key(i)], 4.0))
        measures.append(m)

    for i in range (len(quarter_rests)):
        m = Measure(time_signature=(4, 4) if i == 0 else None)
        for beat_num in range(4):
            if (i + beat_num) % 4 == 0:
                m.append(Rest(1.0))
        measures.append(m)

    for i in range (len(half_rests)):
        m = Measure(time_signature=(4, 4) if i == 0 else None)
        for beat_num in range(4):
            if (i + beat_num) % 4 == 0:
                m.append(Rest(2.0))
        measures.append(m)

    for i in range (len(eighth_rests)):
        m = Measure(time_signature=(4, 4) if i == 0 else None)
        for beat_num in range(4):
            if (i + beat_num) % 4 == 0:
                m.append(Rest(0.5))
        measures.append(m)

    for i in range (len(whole_rests)):
        m = Measure(time_signature=(4, 4) if i == 0 else None)
        for beat_num in range(4):
            if (i + beat_num) % 4 == 0:
                m.append(Rest(4.0))
        measures.append(m)

    for i in range (len(sixteenth_rests)):
        m = Measure(time_signature=(4, 4) if i == 0 else None)
        for beat_num in range(4):
            if (i + beat_num) % 4 == 0:
                m.append(Rest(0.25))
        measures.append(m)

    part.extend(measures)

    score.export_to_file("InputGenerated.musicxml")

    melody = converter.parse("InputGenerated.musicxml")
    melody.show() # YOU NEED MUSESCORE TO RUN THIS