from pymusicxml import *
from music21 import *
from random import choice, choices

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
    # melody.show('midi')

def coordinate_test():
    score = Score(title="Coordinate Test", composer="HTMLvis")
    part = Part("Piano")
    score.append(part)

    #maps y-coords to notes, this would support c4-b5
    note_dict  = {0 : "c4", 1 : "d4", 2 : "e4", 3 : "f4", 4 : "g4", 5 : "a5", 6 : "b5"}

    test = [1, 6, 5, 4, 2, 0, 3]

    measures = []
    m = Measure(time_signature=(3, 4))

    for i in range (len(test)):
        m = Measure(time_signature=(3, 4) if i == 0 else None)
        for beat_num in range(3):
            if (i + beat_num) % 3 == 0:
                # one quarter note triad
                m.append(Note(note_dict[test[i]], 1.0))
            elif (i + beat_num) % 3 == 1:
                # two eighth note dyads
                m.append(BeamedGroup([Note(note_dict[test[i]], 0.5) for _ in range(2)]))
            else:
                # four 16th note notes
                m.append(BeamedGroup([Note(note_dict[test[i]], 0.25) for _ in range(4)]))
        measures.append(m)

    part.extend(measures)

    score.export_to_file("CoordinateTest.musicxml")

    melody = converter.parse("CoordinateTest.musicxml")
    melody.show() # YOU NEED MUSESCORE TO RUN THIS


def generate_from_input(quarter_notes, half_notes, eighth_notes, whole_notes, quarter_rests, half_rests, eighth_rests, whole_rests, sixteenth_rests):
    score = Score(title="Algorithmically Generated MusicXML", composer="HTMLvis")
    part = Part("Piano") #need to receive instrument name from data
    score.append(part)

    pitch_bank = ["f#4", "bb4", "d5", "e5", "ab5", "c6", "f6"]

    # assume treble clef?

    measures = []
    m = Measure(time_signature=(3, 4))

    for i in range (len(quarter_notes)):
        m = Measure(time_signature=(3, 4) if i == 0 else None)
        for beat_num in range(3):
            if (i + beat_num) % 3 == 0:
                # one quarter note triad
                m.append(Chord(choices(pitch_bank, k=3), 1.0))
        measures.append(m)

    # for (n, s) in quarter_notes:
    #     m = Measure(time_signature=(3, 4)) #need to receive time signature from data
    #     m.append(Note(n, 1.0))
    # measures.append(m)

    # for (n, s) in half_notes:
    #     m = Measure(time_signature=(3, 4))
    #     m.append(Note(n, 2.0))
    # measures.append(m)

    # for (n, s, f) in eighth_notes:
    #     m = Measure(time_signature=(3, 4))
    #     m.append(Note(n, 0.5))
    # measures.append(m)

    # for (n,) in whole_notes:
    #     m = Measure(time_signature=(3, 4))
    #     m.append(Note(n, 4.0))
    # measures.append(m)

    # for (n,) in quarter_rests:
    #     m = Measure(time_signature=(3, 4))
    #     m.append(Rest(n, 1.0))
    # measures.append(m)

    # for (n,) in half_rests:
    #     m = Measure(time_signature=(3, 4))
    #     m.append(Rest(n, 2.0))
    # measures.append(m)

    # for (n,) in eighth_rests:
    #     m = Measure(time_signature=(3, 4))
    #     m.append(Rest(n, 0.5))
    # measures.append(m)

    # for (n,) in whole_rests:
    #     m = Measure(time_signature=(3, 4))
    #     m.append(Rest(n, 4.0))
    # measures.append(m)

    # for (n,) in sixteenth_rests:
    #     m = Measure(time_signature=(3, 4))
    #     m.append(Rest(n, 0.25))
    # measures.append(m)

    part.extend(measures)

    score.export_to_file("InputGenerated.musicxml")

coordinate_test()