import mido
from utils import get_note_name

def open_midi_file(file_path):
    """Opens a MIDI file and returns the MIDI object."""
    try:
        midi = mido.MidiFile(file_path)
        return midi
    except Exception as e:
        print(f"Error reading MIDI file: {e}")
        return None
    
def print_midi_info(midi):
    """Prints information about the MIDI file."""
    if midi is not None:
        print(f"MIDI file: {midi.filename}")
        print(f"Number of tracks: {len(midi.tracks)}")
        print(f"Ticks per quarter note: {midi.ticks_per_beat}")
        print(f"Charset: {midi.charset}")
        print(f"debug: {midi.debug}")
        print(f"clip: {midi.clip}")

def print_midi(midi):
    """Prints the MIDI file."""
    if midi is not None:
        for i, track in enumerate(midi.tracks):
            print(f"Track {i + 1}:")
            for message in track:
                print(message)

def play_midi(midi_file, output_port, display=True):
    """Plays the MIDI file and sends it to the specified output port."""
    try:
        with mido.open_output(output_port) as outport:
            for msg in midi_file.play():
                if display:
                    print(msg)
                outport.send(msg)
    except KeyboardInterrupt:
        print("\nScript stopped by user.")
    except Exception as e:
        print(f"Error playing MIDI file: {e}")
    finally:
        outport.close()

def setup_connection(input_port, output_port):
    """Sets up a connection between the input port and the output port."""
    try:
        with mido.open_input(input_port) as inport, mido.open_output(output_port) as outport:
            print(f"Listening on {input_port} and forwarding to {output_port}...")
            for msg in inport:
                if msg.type == 'note_on':
                    print(f"Received: {msg}")
                    print(get_note_name(msg.note))
                outport.send(msg)
    except KeyboardInterrupt:
        print("\nStopped by user.")
    except Exception as e:
        print(f"An error occurred: {e}")