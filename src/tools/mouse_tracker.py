import pyautogui
if __name__ == '__main__':
    buf = []
    while True:
        print(pyautogui.position())
        buf.append(pyautogui.position())
        with open("mouse_data_file.log", "w") as file:
            for elem in buf:
                file.write(str(elem) + "\n")
