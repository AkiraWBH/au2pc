import subprocess
import pyautogui
import time
import os
from tkinter import Tk, Label, Button, Text, Scrollbar, END, filedialog, PhotoImage
import threading
import pygetwindow as gw
import pyperclip
import sys

if sys.stdout is not None:
    sys.stdout.reconfigure(encoding='utf-8')

class App:
    def __init__(self, master):
        self.master = master
        self.master.title("Auto")
        self.master.geometry("400x400+0+0")
        self.master.config(bg="#f0f0f0")
        self.master.iconbitmap(r'C:\Users\letha\OneDrive\Documents\python\test au2pc\image\logo.ico')

        self.title_label = Label(master, text="Quay vòng quay", font=("Arial", 14, "bold"), bg="#f0f0f0")
        self.title_label.pack(pady=5)

        self.label = Label(master, text="Chưa bắt đầu...", wraplength=300, bg="#f0f0f0")
        self.label.pack(pady=5)

        self.start_button = Button(master, text="Bắt đầu", command=self.start_process, bg="#4CAF50", fg="white", font=("Arial", 10))
        self.start_button.pack(pady=5)

        self.text_area = Text(master, height=15, width=50, wrap='word', bg="#fff", font=("Arial", 10))
        self.text_area.pack(pady=10)

        self.scrollbar = Scrollbar(master, command=self.text_area.yview)
        self.scrollbar.pack(side='right', fill='y')
        self.text_area['yscrollcommand'] = self.scrollbar.set

        self.process_thread = None

    def start_process(self):
        self.label.config(text="Đang xử lý...")
        self.start_button.config(state='disabled')

        self.process_thread = threading.Thread(target=self.process_task)
        self.process_thread.start()

    def append_to_text_area(self, text):
        self.text_area.insert(END, text + "\n")
        self.text_area.see(END)

    def process_task(self):
        launcher_path = self.select_game_launcher()
        if launcher_path:
            account_file = r'C:\Users\letha\OneDrive\Documents\python\test au2pc\acc.txt'
            accounts = self.read_accounts_from_file(account_file)

            process_names = ["au2pc.exe", "VTCPlus.exe"]

            for username, password in accounts:
                while True:
                    self.label.config(text=f"Đang xử lý tài khoản: {username}")
                    self.append_to_text_area(f"Đang xử lý tài khoản: {username}")

                    if self.open_launcher(launcher_path):
                        self.auto_login(username, password)

                        time.sleep(20)

                        if not self.is_game_loaded():
                            self.label.config(text="Game chưa vào, đang thử lại...")
                            self.append_to_text_area("Game chưa vào, đang thử lại...")
                            self.close_launcher(process_names)
                            continue

                        if not self.click_nut_1():
                            self.label.config(text="Đang thử lại với tài khoản...")
                            self.append_to_text_area("Đang thử lại với tài khoản...")
                            continue

                        time.sleep(4)
                        self.click_nut_2()
                        self.take_screenshot(username)

                        self.close_launcher(process_names)
                        self.label.config(text="Đợi một chút trước khi mở lại launcher cho tài khoản tiếp theo")
                        self.append_to_text_area("Đợi một chút trước khi mở lại launcher cho tài khoản tiếp theo")
                        time.sleep(5)
                        break

        self.label.config(text="Đã xong hết acc, không còn acc để tiếp tục!")
        self.append_to_text_area("Đã xong hết acc, không còn acc để tiếp tục!")

    def select_game_launcher(self):
        launcher_path = filedialog.askopenfilename(
            title="Chọn đường dẫn đến launcher của game",
            filetypes=[("Executable files", "*.exe")]
        )
        if not launcher_path:
            self.append_to_text_area("Bạn chưa chọn launcher!")
            return None
        self.append_to_text_area(f"Đường dẫn launcher được chọn: {launcher_path}")
        return launcher_path

    def open_launcher(self, launcher_path):
        if not os.path.exists(launcher_path):
            self.append_to_text_area(f"Launcher path not found: {launcher_path}")
            return False
        try:
            subprocess.Popen([launcher_path])
            self.append_to_text_area("Launcher đã mở thành công!")
            return True
        except Exception as e:
            self.append_to_text_area(f"Không thể mở launcher: {e}")
            return False

    def auto_login(self, username, password):
        time.sleep(5)
        self.append_to_text_area("Bắt đầu quá trình đăng nhập...")
        try:
            username_field = pyautogui.locateOnScreen(r'C:\Users\letha\OneDrive\Documents\python\test au2pc\image\login.png', confidence=0.8)
            if username_field:
                pyperclip.copy(username)
                pyautogui.click(username_field)
                pyautogui.hotkey('ctrl', 'v')
                self.append_to_text_area("Đã nhập tài khoản.")
            else:
                self.append_to_text_area("Không tìm thấy tài khoản.")

            password_field = pyautogui.locateOnScreen(r'C:\Users\letha\OneDrive\Documents\python\test au2pc\image\pass.png', confidence=0.8)
            if password_field:
                pyperclip.copy(password)
                pyautogui.click(password_field)
                pyautogui.hotkey('ctrl', 'v')
                self.append_to_text_area("Đã nhập mật khẩu.")
            else:
                self.append_to_text_area("Không tìm thấy mật khẩu.")
            
            pyautogui.press('enter')
            time.sleep(3)

            login_button = pyautogui.locateOnScreen(r'C:\Users\letha\OneDrive\Documents\python\test au2pc\image\dangnhap.png', confidence=0.8)
            if login_button:
                pyautogui.click(login_button)
                self.append_to_text_area("Đã nhấp vào nút đăng nhập.")
            else:
                self.append_to_text_area("Không tìm thấy nút đăng nhập.")

            self.append_to_text_area("Đang đăng nhập vào game!")
        except Exception as e:
            self.append_to_text_area(f"Có lỗi! Tắt chạy lại{e}")

    def read_accounts_from_file(self, file_path):
        self.append_to_text_area(f"Đọc tài khoản từ file: {file_path}")
        with open(file_path, 'r') as file:
            accounts = [line.strip().split(':') for line in file.readlines() if line.strip()]
        self.append_to_text_area(f"Tổng số acc: {len(accounts)}")
        return accounts

    def close_launcher(self, process_names):
        for process_name in process_names:
            try:
                subprocess.call(['taskkill', '/F', '/IM', process_name])
                self.append_to_text_area(f"{process_name} đã được tắt.")
            except Exception as e:
                self.append_to_text_area(f"Lỗi khi tắt launcher: {e}")

    def click_nut_1(self):
        image_path_1 = r'C:\Users\letha\OneDrive\Documents\python\test au2pc\image\nut1_1.png'
        image_path_2 = r'C:\Users\letha\OneDrive\Documents\python\test au2pc\image\nut1_2.png'

        self.append_to_text_area("Đang tìm Vòng Quay...")
        for attempt in range(3):
            click_position_1 = pyautogui.locateOnScreen(image_path_1, confidence=0.5)
            if click_position_1:
                for _ in range(3):
                    pyautogui.click(click_position_1)
                self.append_to_text_area("Đã nhấp vào Vòng Quay.")
                return True

            click_position_2 = pyautogui.locateOnScreen(image_path_2, confidence=0.5)
            if click_position_2:
                for _ in range(3):
                    pyautogui.click(click_position_2)
                self.append_to_text_area("Đã nhấp vào vòng quay quay.")
                return True

        self.append_to_text_area("Không tìm thấy nút 1 trong cả hai hình ảnh. Đang tắt tất cả và chạy lại...")
        self.close_launcher(["au2pc.exe", "VTCPlus.exe"])
        return False

    def click_nut_2(self):
        image_path_2 = r'C:\Users\letha\OneDrive\Documents\python\test au2pc\image\nut2.png'
        self.append_to_text_area("Đang tìm nút quay...")
        click_position_2 = pyautogui.locateOnScreen(image_path_2, confidence=0.5)
        if click_position_2:
            for _ in range(3):
                pyautogui.click(click_position_2)
            self.append_to_text_area("Đã nhấp vào nút quay.")
            self.append_to_text_area("Chờ 10s để quay!")
        else:
            self.append_to_text_area("Không tìm thấy nút 2.")

    def create_screenshots_directory(self):
        screenshots_directory = "kiểm tra"
        if not os.path.exists(screenshots_directory):
            os.makedirs(screenshots_directory)
            self.append_to_text_area(f"Thư mục '{screenshots_directory}' đã được tạo.")

    def take_screenshot(self, username):
        screenshots_directory = "kiểm tra"
        game_window = gw.getWindowsWithTitle('Au2PCGame')[0]
        if game_window:
            x, y, width, height = game_window.left, game_window.top, game_window.width, game_window.height
            screenshot_path = os.path.join(screenshots_directory, f"{username}.png")
            time.sleep(10)
            screenshot = pyautogui.screenshot(region=(x, y, width, height))
            screenshot.save(screenshot_path)
            self.append_to_text_area(f"Đã chụp màn hình game và lưu tại: {screenshot_path}")
        else:
            self.append_to_text_area("Không tìm thấy cửa sổ game.")

    def is_game_loaded(self):
        game_interface_image = r'C:\Users\letha\OneDrive\Documents\python\test au2pc\image\giaodien.png'
        return pyautogui.locateOnScreen(game_interface_image, confidence=0.5) is not None

if __name__ == "__main__":
    root = Tk()
    app = App(root)
    root.mainloop()