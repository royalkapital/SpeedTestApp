import speedtest
from tkinter import *
import requests
import threading
from PIL import Image, ImageTk
from itertools import count

class speed_test:
    def __init__(self):
        self.main = Tk()
        self.main.geometry('1080x600+200+100')
        self.main.title('Speedtest App')

        self.main.resizable(width=False, height=False)
        self.main.configure(bg='#2b2e2c')

        self.main.iconphoto(False, PhotoImage(file='icon_photo.png'))

        self.font_1 = ('poppins', 15)
        self.font_2 = ('poppins', 24, 'bold')
        self.font_3 = ('poppins', 35, 'bold')
        self.font_4 = ('poppins', 50, 'bold')

        self.gui_components()

        self.main.mainloop()

    def gui_components(self):
        self.title_label = Label(self.main, font=self.font_3, bg='#1b1c1b', fg='cyan', text='Speedtest app')
        self.title_label.place(relx=0, rely=0, relheight=0.12, relwidth=1)

        self.go_button = Button(self.main, font=self.font_4, text='GO', width=10, bg='black', fg='white', command=self.func_go)
        self.go_button.place(relx=0.4, rely=0.3, relheight=0.3, relwidth=0.2)

        self.ip_address, self.owner_name, self.city_name = self.get_ip_owner_city()
        self.server_name_label = Label(self.main, font=self.font_1, bg='#2b2e2c', fg='cyan', text=f'{self.owner_name}')
        self.server_name_label.place(relx=0.3, rely=0.7)

        self.ip_label = Label(self.main, font=self.font_1, bg='#2b2e2c', fg='cyan', text=f'{self.ip_address}')
        self.ip_label.place(relx=0.3, rely=0.77)

        self.city_label = Label(self.main, font=self.font_1, bg='#2b2e2c', fg='cyan', text=f'{self.city_name}')
        self.city_label.place(relx=0.6, rely=0.7)

        self.connection_name_label = Label(self.main, font=self.font_1, bg='#2b2e2c', fg='cyan') #, text='sp1.katv1.net:8080'
        self.connection_name_label.place(relx=0.6, rely=0.77)

        self.ping_label_name = Label(self.main, font=self.font_2, bg='#2b2e2c', fg='cyan')#, text=f'PING: '
        self.ping_label_name.place(relx=0.42, rely=0.17)

        self.ping_label_value = Label(self.main, font=self.font_2, bg='#2b2e2c', fg='cyan')#, text=f'59.2')
        self.ping_label_value.place(relx=0.52, rely=0.17)

        self.download_label_name = Label(self.main, font=self.font_2, bg='#2b2e2c', fg='cyan')#, text=f'Download speed: ')
        self.download_label_name.place(relx=0.1, rely=0.3)

        self.download_label_value = Label(self.main, font=self.font_2, bg='#2b2e2c', fg='cyan')#, text=f'13.8')
        self.download_label_value.place(relx=0.2, rely=0.4)

        self.upload_label_name = Label(self.main, font=self.font_2, bg='#2b2e2c', fg='cyan')#, text=f'Upload speed: ')
        self.upload_label_name.place(relx=0.7, rely=0.3)

        self.upload_label_value = Label(self.main, font=self.font_2, bg='#2b2e2c', fg='cyan')#, text=f'2.89')
        self.upload_label_value.place(relx=0.77, rely=0.4)

    def get_ip_owner_city(self):
        api = 'http://ipinfo.io/json'
        json_data = requests.get(api).json()
        ip = json_data['ip']
        owner = json_data['org'][7:]
        city = json_data['city']
        return ip, owner, city

    def func_go(self):
        self.frame = Frame(self.main)
        self.frame.place(relx=0.43, rely=0.315)
        self.loading = ImageLabel(self.frame)
        self.loading.pack()
        self.loading_case = threading.Thread(target=self.loading.load('loading.gif'))

        test = threading.Thread(target=self.speedtest)
        test.start()

        self.info_label = Label(self.main, font=self.font_2, bg='#2b2e2c', fg='cyan')
        self.info_label.place(relx=0.32, rely=0.17)
        self.info_label.config(text='Data are being prepared.\n'
                                    '       Please wait.     ')

    def speedtest(self):
        self.loading_case.start()
        self.test = speedtest.Speedtest()

        self.test.get_servers()

        self.best = self.test.get_best_server()

        self.connection_name_label.config(text=f'{self.best["host"]}')

        self.download_result = self.test.download()
        self.download_str = f'{self.download_result / 1024 ** 2:.2f}'

        self.download_label_name.config(text='Download speed: ')
        self.download_label_value.config(text=f'{self.download_str}')

        self.upload_result = self.test.upload()
        self.upload_str = f'{self.upload_result / 1024 ** 2:.2f}'

        self.upload_label_name.config(text='Upload speed: ')
        self.upload_label_value.config(text=f'{self.upload_str}')

        self.ping_result = self.test.results.ping
        self.ping_str = f'{self.ping_result:.2f}'

        self.info_label.destroy()

        self.ping_label_name.config(text='PING: ')
        self.ping_label_value.config(text=f'{self.ping_str}')

        self.loading_case.join()
        self.frame.destroy()



class ImageLabel(Label):
    def load(self, im):
        if isinstance(im, str):
            im = Image.open(im)

        self.loc = 0
        self.frames = []

        try:
            for i in count(1):
                self.frames.append(ImageTk.PhotoImage(im.copy()))
                im.seek(i)
        except EOFError:
            pass

        try:
            self.delay = im.info['duration']
        except:
            self.delay = 100

        if len(self.frames) == 1:
            self.config(image=self.frames[0])
        else:
            self.next_frame()

    def unload(self):
        self.config(image="")
        self.frames = None

    def next_frame(self):
        if self.frames:
            self.loc += 1
            self.loc %= len(self.frames)
            self.config(image=self.frames[self.loc])
            self.after(self.delay, self.next_frame)


app = speed_test()