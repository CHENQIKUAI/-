import requests
import time
from playsound import playsound
import tkinter as tk
import threading


# 配置
URL = "http://dl.scs.gov.cn/api/result/checkWritten/8a81f6d09024e05b01914fc92ed90023?_=" + str(int(time.time() * 1000)) 
SOUND_FILE = "ji.mp3"  # 替换为你的声音文件路径
INTERVAL = 60  # 查询间隔，单位为秒


def check_results():
    try:
        response = requests.get(URL)
        response.raise_for_status()  # 检查请求是否成功
        # 打印返回的数据，并且打印时间
        print(response.text, time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
        return response.text!= '{"scoreTime":"0"}'
    except requests.exceptions.RequestException as e:
        print(f"请求出现异常：{e}，请检查网络或服务器状态！")
        return False


def notify_user(data=None):
    def play_music(stop_event):
        while not stop_event.is_set():
            try:
                playsound(SOUND_FILE, block=True)
            except FileNotFoundError:
                print(f"声音文件 {SOUND_FILE} 不存在，请检查文件路径是否 correct！")
                break
            except playsound.PlaysoundException as e:
                print(f"声音播放出现其他问题：{e}，可能是文件格式或播放设备故障，请检查相关设置。")
                break

    def stop_music(stop_event):
        stop_event.set()
        root.destroy()

    # 仅当 check_results() 为 True 时创建窗口
    if data:
        root = tk.Tk()
        root.title("成绩通知")
        label = tk.Label(root, text="成绩已出！详细信息：" + str(data))
        label.pack(pady=20)
        button = tk.Button(root, text="确定", command=lambda: stop_music(stop_event))
        button.pack(pady=20)

        # 初始化 stop_event 变量
        stop_event = threading.Event()


        music_thread = threading.Thread(target=play_music, args=(stop_event,))
        music_thread.start()
        root.mainloop()


def main():
    result = None  # 存储 check_results 的结果
    while True:
        result = check_results()
        if result:
            notify_user(result)
        time.sleep(INTERVAL)


if __name__ == "__main__":
    main()