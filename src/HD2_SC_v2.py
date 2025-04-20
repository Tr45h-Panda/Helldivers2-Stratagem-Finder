import pyautogui
from screeninfo import get_monitors
from PIL import Image
import pytesseract
import keyboard
import os
import shutil

# Specify the path to the Tesseract-OCR executable
pytesseract.pytesseract.tesseract_cmd = r'tesseract'  # Use 'tesseract' for cross-platform compatibility

# Global variable to store the extracted text
extracted_text = []

def capture_and_read_text():
    global extracted_text
    monitors = get_monitors()
    monitor_index = 1
    monitor = monitors[monitor_index]

    monitor.x = 0
    monitor.y = 0
    monitor.width = 340
    monitor.height = 600
    region = (monitor.x, monitor.y, monitor.width, monitor.height)

    screenshot = pyautogui.screenshot(region=region)
    screenshot.save("monitor_screenshot.png")

    screenshot_image = Image.open("monitor_screenshot.png")
    text = pytesseract.image_to_string(screenshot_image)

    extracted_text = [line.lower() for line in text.split('\n') if line.isupper()]

    print("Text read from the screenshot (only capitalized lines):")
    for line in extracted_text:
        print(line)

def clear_destination_folder():
    destination_dir = os.path.join("data", "ToESP")
    for file_name in os.listdir(destination_dir):
        file_path = os.path.join(destination_dir, file_name)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            print(f"Failed to delete {file_path}. Reason: {e}")

def copy_svg_files():
    global extracted_text
    source_dir = os.path.join("data", "HD2_Stratagem_Icons")
    destination_dir = os.path.join("data", "ToESP")

    os.makedirs(destination_dir, exist_ok=True)
    clear_destination_folder()

    for root, dirs, files in os.walk(source_dir):
        for file_name in files:
            if file_name.endswith(".svg"):
                file_name_no_ext = os.path.splitext(file_name)[0].lower()
                if file_name_no_ext in extracted_text:
                    source_file = os.path.join(root, file_name)
                    destination_file = os.path.join(destination_dir, file_name)
                    shutil.copy(source_file, destination_file)
                    print(f"Copied {file_name} to {destination_dir}")

def main():
    keyboard.add_hotkey('ctrl+shift+s', capture_and_read_text)
    keyboard.add_hotkey('ctrl+shift+c', copy_svg_files)

    print("Press Ctrl+Shift+S to capture and read text from the screen.")
    print("Press Ctrl+Shift+C to copy .svg files to the destination folder.")
    keyboard.wait('esc')

if __name__ == "__main__":
    main()