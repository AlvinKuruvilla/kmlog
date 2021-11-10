import pyautogui
if __name__ == '__main__':
    buf = []
    while True:
        print(pyautogui.position())
        buf.append(pyautogui.position())
        mouse_data_file = open("mouse_data_file.log", "w")
        for elem in buf:
            mouse_data_file.write(str(elem) + "\n")
        mouse_data_file.close()
