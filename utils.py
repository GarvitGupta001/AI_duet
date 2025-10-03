def get_note_name(note_number):
    note_names = ["C", "C#", "D", "D#", "E", "F", 
                  "F#", "G", "G#", "A", "A#", "B"]
    octave = (note_number // 12) - 1   # MIDI standard: C4 = 60
    name = note_names[note_number % 12]
    return f"{name}{octave}"