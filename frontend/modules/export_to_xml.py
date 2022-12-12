from pymusicxml import *
# from music21 import *
# from music21 import converter
from random import choice, choices
from modules import nb_train

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

    # melody = converter.parse("AlgorithmicExample.musicxml")
    # melody.show() # YOU NEED MUSESCORE TO RUN THIS

def generate_from_input(notes, keys):
    score = Score(title="Algorithmically Generated MusicXML", composer="HTMLvis")
    part = Part("Piano") #need to receive instrument name from data
    score.append(part)

    # 1 top of staff, 8 bottom of staff
    pitch_bank = {0 : "f5", 1: "e5", 2: "d5", 3: "c5", 4: "b4", 5: "a4", 6: "g4", 7: "f4", 8:"e4"}

    # assume treble clef?

    measures = []
    m = Measure(time_signature=(4, 4))

    for i in range(len(notes)):
        m = Measure(time_signature=(4, 4) if i == 0 else None)
        #0 if quarter note, 1 if half note, 2 is quarter rest, 3 is whole note
        print(i)
        for beat_num in range(4):
            if (i + beat_num) % 4 == 0:
                if notes[i] == 0:
                    m.append(Note(pitch_bank[keys[i]], 1.0))
                elif notes[i] == 1:
                    m.append(Note(pitch_bank[keys[i]], 2.0))
                elif notes[i] == 2:
                    m.append(Rest(1.0))
                elif notes[i] == 3:
                    m.append(Note(pitch_bank[keys[i]], 4.0))
        measures.append(m)


    # for i in range (len(quarter_notes)):
    #     m = Measure(time_signature=(4, 4) if i == 0 else None)
    #     for beat_num in range(4):
    #         if (i + beat_num) % 4 == 0:
    #             m.append(Note(pitch_bank[get_key(i)], 1.0))
    #     measures.append(m)

    # for i in range (len(half_notes)):
    #     m = Measure(time_signature=(4, 4) if i == 0 else None)
    #     for beat_num in range(4):
    #         if (i + beat_num) % 4 == 0:
    #             m.append(Note(pitch_bank[get_key(i)], 2.0))
    #     measures.append(m)

    # for i in range (len(eighth_notes)):
    #     m = Measure(time_signature=(4, 4) if i == 0 else None)
    #     for beat_num in range(4):
    #         if (i + beat_num) % 4 == 0:
    #             m.append(Note(pitch_bank[get_key(i)], 0.5))
    #     measures.append(m)

    # for i in range (len(whole_notes)):
    #     m = Measure(time_signature=(4, 4) if i == 0 else None)
    #     for beat_num in range(4):
    #         if (i + beat_num) % 4 == 0:
    #             m.append(Note(pitch_bank[get_key(i)], 4.0))
    #     measures.append(m)

    # for i in range (len(quarter_rests)):
    #     m = Measure(time_signature=(4, 4) if i == 0 else None)
    #     for beat_num in range(4):
    #         if (i + beat_num) % 4 == 0:
    #             m.append(Rest(1.0))
    #     measures.append(m)

    # for i in range (len(half_rests)):
    #     m = Measure(time_signature=(4, 4) if i == 0 else None)
    #     for beat_num in range(4):
    #         if (i + beat_num) % 4 == 0:
    #             m.append(Rest(2.0))
    #     measures.append(m)

    # for i in range (len(eighth_rests)):
    #     m = Measure(time_signature=(4, 4) if i == 0 else None)
    #     for beat_num in range(4):
    #         if (i + beat_num) % 4 == 0:
    #             m.append(Rest(0.5))
    #     measures.append(m)

    # for i in range (len(whole_rests)):
    #     m = Measure(time_signature=(4, 4) if i == 0 else None)
    #     for beat_num in range(4):
    #         if (i + beat_num) % 4 == 0:
    #             m.append(Rest(4.0))
    #     measures.append(m)

    # for i in range (len(sixteenth_rests)):
    #     m = Measure(time_signature=(4, 4) if i == 0 else None)
    #     for beat_num in range(4):
    #         if (i + beat_num) % 4 == 0:
    #             m.append(Rest(0.25))
    #     measures.append(m)

    part.extend(measures)

    score.export_to_file("static/result_files/InputGenerated.musicxml")

    # melody = converter.parse("frontend\static\result_files\InputGenerated.musicxml")
    # melody.show() # YOU NEED MUSESCORE TO RUN THIS