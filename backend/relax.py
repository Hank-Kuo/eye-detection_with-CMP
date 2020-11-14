import tkinter as tk, threading
import imageio
from PIL import Image, ImageTk
import os
import redis
import playsound

r = redis.Redis(host='localhost', port=6379, decode_responses=True)
r.set("flag_relax",1)

local=os.path.abspath('.').replace("\\","/")+"/code/" #os.path.abspath('.').replace("\\","/")+"/code/"
video_name = local+"E/relax.mp4" #This is your video file path
video = imageio.get_reader(video_name)
def stream(label):
    playsound.playsound(local+"sound/111.mp3",False)
    for image in video.iter_data():
        frame_image = ImageTk.PhotoImage(Image.fromarray(image))
        label.config(image=frame_image)
        label.image = frame_image
        #playsound.playsound(local+"sound/relax_s.mp3",True)


def exit():
    #r.set("flag_relax",2)
    B.destroy()
    root.destroy()
if __name__ == "__main__":
    root = tk.Tk()
    my_label = tk.Label(root,bg='black')
    root.attributes("-fullscreen",True)
    root.configure(background='black')

    photo1 = Image.open(local+'E/exit_btn.png')
    phot=photo1.resize((200, 100),Image.ANTIALIAS)
    phot=ImageTk.PhotoImage(phot)
    B = tk.Button(root,image = phot ,command=exit,bg='black')
    B.place(relx=0.86, rely=0.07)
    my_label.pack()
    thread = threading.Thread(target=stream, args=(my_label,))
    thread.daemon = 1
    thread.start()
    #
    root.mainloop()