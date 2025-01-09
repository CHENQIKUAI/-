from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from playsound import playsound
import tkinter as tk
from tkinter import ttk
import threading
import webbrowser


def check_keyword_with_selenium(url, keywords, music_file):
    def play_music(stop_event):
        while not stop_event.is_set():
            try:
                playsound(music_file, block=True)
            except FileNotFoundError:
                print(f"声音文件 {music_file} 不存在，请检查文件路径是否正确！")
                break
            except Exception as e:
                print(f"声音播放出现其他问题：{e}，可能是文件格式或播放设备故障，请检查相关设置。")
                break

    def stop_music(stop_event):
        stop_event.set()
        try:
            root.destroy()
        except tk.TclError:
            pass

    # 配置 Chrome 浏览器驱动，指定 ChromeDriver 的路径
    service = Service(executable_path='D:\\store\\chromedriver-win64\\chromedriver.exe')
    options = webdriver.ChromeOptions()
    # 设置为无头模式，即后台运行
    options.add_argument('--headless')
    driver = webdriver.Chrome(service=service, options=options)
    try:
        while True:
            # 打开网页
            driver.get(url)
            # 等待页面完全加载，这里等待 20 秒钟，直到 body 元素可访问
            WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.TAG_NAME, 'body')))
            # 执行 JavaScript 代码，将页面滚动到底部，以确保所有内容加载
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            # 再次等待一段时间，确保动态加载的内容完全呈现，可根据实际情况调整等待时间
            time.sleep(5)
            # 获取网页的全部文本内容
            page_text = driver.find_element(By.TAG_NAME, 'body').text
            # 检查是否包含任何一个关键字
            if any(keyword in page_text for keyword in keywords):
                print(f"页面中包含关键字 '{keywords}' 中的一个。")
                # 先打开网页
                webbrowser.open(url)
                root = tk.Tk()
                root.title("成绩通知")
                root.geometry("300x200")  # 设置窗口大小
                root.resizable(False, False)  # 禁止调整窗口大小
                style = ttk.Style()
                style.configure('TButton', font=('Helvetica', 14))
                style.configure('TLabel', font=('Helvetica', 16))
                label = ttk.Label(root, text="页面中出现成绩或分数或笔试信息！\n请查看详情。", padding=(20, 20))
                label.pack()
                button = ttk.Button(root, text="确定", command=lambda: stop_music(stop_event))
                button.pack(pady=20)
                stop_event = threading.Event()
                music_thread = threading.Thread(target=play_music, args=(stop_event,))
                music_thread.start()
                root.mainloop()
                break  # 找到关键字后退出循环
            else:
                print(f"页面中不包含关键字 '{keywords}' 中的任何一个。")
            # 等待 3 秒
            time.sleep(3)
    except Exception as e:
        print(f"出现异常: {e}")
    finally:
        # 关闭浏览器
        driver.quit()


# 要检查的网址
url = "http://bm.scs.gov.cn/pp/gkweb/core/web/ui/business/home/gkhome.html"
# 要查找的关键字列表
keywords = ["分数", "成绩"]
# 音乐文件的路径，替换为你自己的音乐文件路径
music_file = "goodluck.mp3"
check_keyword_with_selenium(url, keywords, music_file)