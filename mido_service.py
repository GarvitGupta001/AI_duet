import mido
from helpers import get_note_name

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

import mido
import time

def take_input(input_port, output_port):
    """
    Takes MIDI input from the specified input port, forwards it to the output port, 
    and records it to a MIDI file with correct timing (delta time).
    """
    # 1. Setup for the MIDI File
    mid = mido.MidiFile()
    track = mido.MidiTrack()
    mid.tracks.append(track)
    
    # Set the tempo and time resolution (required for accurate time conversion)
    # Default is 500000 microseconds per beat (120 BPM) and 480 ticks/beat
    tempo = mido.bpm2tempo(120) 
    # Must explicitly set tempo/time_signature as the first messages with time=0
    track.append(mido.MetaMessage('set_tempo', tempo=tempo, time=0)) 
    track.append(mido.MetaMessage('time_signature', numerator=4, denominator=4, time=0))
    
    # Timing variables for delta time calculation
    last_message_time = time.time()
    
    print(f"Opening Input Port: {input_port}")
    print(f"Opening Output Port: {output_port}")
    print("Recording... Press Ctrl+C to stop and save.")
    
    try:
        with mido.open_input(input_port) as inport, mido.open_output(output_port) as outport:
            for msg in inport:
                # Filter out timing messages like 'clock' or 'active_sensing'
                if msg.type in ['clock', 'sysex', 'active_sensing']:
                    outport.send(msg) # Forwarding these is fine
                    continue 

                current_time = time.time()
                delta_time_s = current_time - last_message_time
                
                # 2. Convert Real-Time Seconds to MIDI Ticks
                # Use the set tempo and the file's ticks_per_beat resolution
                ticks_per_beat = mid.ticks_per_beat
                delta_ticks = mido.second2tick(delta_time_s, ticks_per_beat, tempo)
                
                # 3. Modify the Message for Saving
                # Set the message's 'time' attribute to the calculated delta ticks
                # Ensure it's an integer and non-negative
                msg.time = max(0, int(round(delta_ticks)))
                
                # 4. Record and Forward
                track.append(msg)
                outport.send(msg)
                print(get_note_name(msg.note) if msg.type in ['note_on', 'note_off'] else None)
                
                # Update time for the next delta calculation
                last_message_time = current_time

    except KeyboardInterrupt:
        # Saving happens when the user interrupts (stops playing)
        output_filename = 'recorded_input.mid'
        mid.save(output_filename)
        print(f"\nRecording stopped by user.")
        print(f"Successfully saved MIDI file to {output_filename}")
        
    except Exception as e:
        print(f"An error occurred: {e}")

# Example usage (assuming valid port names)
# take_input('VIRTUAL MIDI OUT', 'VIRTUAL MIDI IN')