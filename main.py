from mido import get_input_names, get_output_names
import midi_file_service as MidiService

# List Input Ports
input_ports = get_input_names()
for i, port in enumerate(input_ports):
    print(f"Input Port {i + 1}: {port}")
input_port_number = input("Enter the number of your MIDI input port: ")
input_port = input_ports[int(input_port_number) - 1]

# List Output Ports
output_ports = get_output_names()
for i, port in enumerate(output_ports):
    print(f"Output Port {i + 1}: {port}")
output_port_number = input("Enter the number of your MIDI output port: ")
output_port = output_ports[int(output_port_number) - 1]
print("-" * 30)

MidiService.setup_connection(input_port, output_port)