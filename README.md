# Macro Program for Recording and Replaying Keyboard and Mouse Inputs

This is a Python program that enables recording and replaying of keyboard and mouse inputs using the `pynput` library. It allows you to automate repetitive tasks by capturing input events and executing them at a later time.

## Features

- Records keyboard and mouse inputs including key presses, releases, mouse movements, clicks,, scrolling and the delays between the actions.
- Stores the recorded inputs in a human-readable log file and also as a serialized pickle file for later use.
- Provides functions to execute the recorded inputs with correct timing.
- Supports simulating keyboard typing and performing a double-click with the mouse.

## Dependencies

- Python 3.x
- `pynput` library (`pip install pynput`)

## Usage

1. Install the required dependencies mentioned above.
2. Clone or download this repository.
3. Run the `macro_program.py` script using Python.

### Recording Inputs

- The program will start listening for input events.
- Press the **ESC** key to stop listening and save the recorded inputs.

### Executing Recorded Inputs

- After stopping the recording, the inputs will be saved as a pickle file.
- To execute the recorded inputs:
  - Load the pickle file using the `load_dictionary` function.
  - Call the `execute_inputs` function, passing the loaded inputs as an argument.

### Additional Functions

- `write_with_keyboard(text, delay=True, delay_value=0.1)`: Simulates typing the provided `text` using the keyboard. You can optionally specify a delay between key presses.
