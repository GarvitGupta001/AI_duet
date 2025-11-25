def get_note_name(note_number):
    note_names = ["C", "C#", "D", "D#", "E", "F", 
                  "F#", "G", "G#", "A", "A#", "B"]
    octave = (note_number // 12) - 1   # MIDI standard: C4 = 60
    name = note_names[note_number % 12]
    return f"{name}{octave}"

def prepare_seed_sequence(user_input_ids, context_len=512, bos_id=1):
    """
    Normalizes a user-provided list of token IDs to the model's required length (CONTEXT_LEN).

    :param user_input_ids: A list of integer IDs representing the music.
    :param context_len: The required input size (512).
    :param bos_id: The ID used for Beginning of Sequence (BOS) padding.
    :return: A list of integer IDs of exactly context_len size.
    """
    
    input_length = len(user_input_ids)
    
    if input_length > context_len:
        # Case 1: Truncation (Input is TOO LONG)
        # Take the most recent (last) context_len tokens, as they are most relevant for prediction.
        print(f"Input is too long ({input_length} tokens). Truncating to last {context_len} tokens.")
        prepared_ids = user_input_ids[-context_len:]
        
    elif input_length < context_len:
        # Case 2: Padding (Input is TOO SHORT)
        # Pad the beginning of the sequence with BOS tokens.
        # This signals to the model that the music is starting/continuing from an unknown point.
        print(f"Input is too short ({input_length} tokens). Padding with BOS_ID ({bos_id}).")
        
        padding_needed = context_len - input_length
        # Pre-pend the padding tokens
        padding_tokens = [bos_id] * padding_needed
        prepared_ids = padding_tokens + user_input_ids
        
    else:
        # Case 3: Perfect Length
        prepared_ids = user_input_ids
    
    return prepared_ids

# --- EXAMPLE USAGE ---

# Assume the user provided 10 integer IDs
short_user_input = [10, 12, 14, 15, 17, 19, 21, 22, 24, 26] 

# The BOS_ID must be confirmed from your tokenizer file!
BOS_ID = 1 # Use 1 as a typical default

# Prepare the seed
seed_ids = prepare_seed_sequence(short_user_input, context_len=512, bos_id=BOS_ID)

print(f"Final seed length: {len(seed_ids)}")

# Now you pass this prepared seed to your generation function:
# new_music_ids = generate_sequence(seed_ids, max_new_tokens=500, temperature=0.8)