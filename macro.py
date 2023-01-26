import pynput
import logging
import pickle
import time

# File to store the inputs in a human-readable format
human_readable_logs_name = "key-logs.txt"
# Store inputs in a python list
pickle_file_name = "pickle"

# store input logs
inputs = []

logging.basicConfig(filename=human_readable_logs_name, level=logging.DEBUG,
                    format="%(levelname)s: %(asctime)s: %(message)s", encoding="utf-8")


def save_dictionary(file_name, dictionary):
    with open(f'{file_name}.pkl', 'wb') as f:
        pickle.dump(dictionary, f)
    # print(f'Saved to {file_name}')


def load_dictionary(file_name):
    with open(f'{file_name}.pkl', 'rb') as f:
        return pickle.load(f)
    # print(f'{file_name} loaded')


def on_press(key):
    if key == pynput.keyboard.Key.esc:
        listener.stop()  # return False
    logging.info(str(key) + " ( \u2193 Key pressed)")
    inputs.append({"time_stamp": (time.time() - start_time), "type": "keyboard", "key": key, "action": "press"})
    # print(f'{key} pressed')


def on_release(key):
    logging.info(str(key) + " ( \u2191 Key released)")
    inputs.append({"time_stamp": (time.time() - start_time), "type": "keyboard", "key": key, "action": "release"})
    # print(f'{key} released')


def on_move(x, y):
    logging.info(f"Mouse moved to ({x}, {y})")
    inputs.append({"time_stamp": (time.time() - start_time), "type": "mouse", "x": x, "y": y, "action": "move"})
    # print(f"Mouse moved to ({x}, {y})")


def on_click(x, y, button, pressed):
    if pressed:
        logging.info(f"Mouse clicked at ({x}, {y}) with {button}")
        inputs.append(
            {"time_stamp": (time.time() - start_time), "type": "mouse", "x": x, "y": y,
             "action": ("press" if pressed else "release"),
             "button": button})
        # print(f"Mouse clicked at ({x}, {y}) with {button}")


def on_scroll(x, y, dx, dy):
    logging.info(f"Mouse scrolled at ({x}, {y})({dx}, {dy})")
    inputs.append(
        {"time_stamp": (time.time() - start_time), "type": "mouse", "x": x, "y": y, "action": "scroll", "dx": dx,
         "dy": dy})
    # print(f"Mouse scrolled at ({x}, {y})({dx}, {dy})".format(x, y, dx, dy))


# Read the recorded inputs file and execute them
def execute_inputs(pickle_input):
    print(f"Executing inputs...")
    mouse_controller = pynput.mouse.Controller()
    keyboard_controller = pynput.keyboard.Controller()
    last_execution_time = 0
    for input_ in pickle_input:
        # Execute in order with correct timing
        execution_time = float(input_['time_stamp'])
        sleep_time = execution_time - last_execution_time
        time.sleep(sleep_time)
        # print(f"  Sleeping for {sleep_time} sec")

        if input_['type'] == 'mouse':
            x, y = input_['x'], input_['y']
            if input_['action'] == 'move':
                # print(f"Moving mouse: ({x}, {y})")
                mouse_controller.position = (x, y)
            elif input_['action'] == 'press':
                # print(f"Clicking mouse: {input_['button']}")
                mouse_controller.press(input_['button'])
            elif input_['action'] == 'release':
                # print(f"Releasing mouse: {input_['button']}")
                mouse_controller.release(input_['button'])
            elif input_['action'] == 'scroll':
                # print(f"Scrolling mouse: ({input_['dx']}, {input_['dy']})")
                mouse_controller.scroll(input_['dx'], input_['dy'])
        elif input_['type'] == 'keyboard':
            key = input_['key']
            if input_['action'] == 'press':
                # print(f"Pressing Key: {key}")
                keyboard_controller.press(key)
            elif input_['action'] == 'release':
                # print(f"Releasing Key: {key}")
                keyboard_controller.release(key)

        # Update timing
        last_execution_time = execution_time


# Simulate typing on keyboard
def write_with_keyboard(text, delay=True, delay_value=0.1):
    keyboard_controller = pynput.keyboard.Controller()
    for char in text:
        keyboard_controller.press(char)
        keyboard_controller.release(char)
        if delay:
            time.sleep(delay_value)


# Double click
# pynput.mouse.Controller().press(pynput.mouse.Button.left, 2)

# Write text with keyboard
# write_with_keyboard("texttexttexttexttexttexttexttet", delay_value=0.1)

start_time = 0

with pynput.mouse.Listener(on_click=on_click, on_scroll=on_scroll, on_move=on_move) as listener:
    with pynput.keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
        print(f"Started listening (Press ESC to stop listening)")
        start_time = time.time()
        listener.join()
        print(f"Stopped listening")

save_dictionary(pickle_file_name, inputs)
a = input("Press any key to execute the recorded inputs.")

# Execute stored pickle file
inputs = load_dictionary(pickle_file_name)
execute_inputs(inputs)
