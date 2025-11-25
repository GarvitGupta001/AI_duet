from mido import get_input_names, get_output_names
import mido_service as MidiService
from miditok import REMI
from pathlib import Path
from keras.models import load_model
import helpers
from tqdm import tqdm
import numpy as np

CONTEXT_LEN = 512

# Select Input Port
input_ports = get_input_names()
for i, port in enumerate(input_ports):
    print(f"Input Port {i + 1}: {port}")
input_port_number = input("Enter the number of your MIDI input port: ")
input_port = input_ports[int(input_port_number) - 1]

# Select Output Port
output_ports = get_output_names()
for i, port in enumerate(output_ports):
    print(f"Output Port {i + 1}: {port}")
output_port_number = input("Enter the number of your MIDI output port: ")
output_port = output_ports[int(output_port_number) - 1]
print("-" * 30)

try:
    print("initializing tokenizer...")
    token_config_path = "tokenizer_trained.json"
    tokenizer = REMI(params='./tokenizer_trained.json')
    print("Tokenizer initialized successfully.")
except Exception as e:
    print(f"Error initializing tokenizer: {e}")
    exit(1)

try:
    print("Loading model...")
    model_path = "./music_lstm_model.keras"
    model = load_model(model_path)
    print("Model loaded successfully.")
except Exception as e:
    print(f"Error loading model: {e}")
    exit(1)

def generate_sequence(input_tokens, Note_Count=500):
    tokens_ids= [t for t in input_tokens]
    for i in tqdm(range(Note_Count), desc="Generating Music"):
        input_arr = np.array(tokens_ids[-CONTEXT_LEN:])[None, :]
        prediction = model.predict(input_arr, verbose=0)[0]
        token_id = int(np.argmax(prediction))
        tokens_ids.append(token_id)
    return tokens_ids[-Note_Count:]

MidiService.take_input(input_port, output_port)

#tokenise recorded_input.mid
input_tokens = tokenizer(Path("./recorded_input.mid"))[0].ids
print(f"Number of tokens: {len(input_tokens)}")
print(f"First 20 tokens: {input_tokens[:20]}")

#trim/pad to 512 tokens if needed
input_tokens = helpers.prepare_seed_sequence(input_tokens, context_len=CONTEXT_LEN, bos_id=1)
print(f"Final seed length: {len(input_tokens)}")
print(f"First 20 tokens: {input_tokens[:20]}")

#Generate with model
generated_tokens = generate_sequence(input_tokens, Note_Count=50)
print(f"Generated {len(generated_tokens)} tokens.")
print(f"First 20 generated tokens: {generated_tokens[:20]}")

# detokenise and play generated output
output_midi = tokenizer.decode([generated_tokens])
output_path = "./generated_output.mid"
output_midi.dump_midi(output_path)
print(f"Generated MIDI saved to {output_path}. Playing now...")
midi_file = MidiService.open_midi_file(output_path)
MidiService.play_midi(midi_file, output_port, display=False)