import tkinter
from tkinter import LEFT,RIGHT,BOTH,ttk
import tkinter.font as tkFont

#window
root = tkinter.Tk()
root.resizable(0,0)
root.geometry('1000x600')
root.iconbitmap('notepad.ico')
root.title('Notepad')

#Functions
def full_screen_mode(event):
    print(event)
    print(root.winfo_width(),root.winfo_height())
    root.attributes("-fullscreen",not root.attributes("-fullscreen"))

def display_options_frame(event):
    options_frame.pack()
    display_option_widgets()

def hide_options_frame(event):
    options_frame.pack_forget()

def command(event):
    print("hi")

def display_option_widgets():
    new_file.grid(row = 0,column=0,padx=10)
    open_file.grid(row =0,column=1,padx=10)
    save_file.grid(row = 0,column=2,padx=10)
    save_to_cloud.grid(row = 0,column=3,padx=(5,10))
    share_file.grid(row = 0,column=4,padx=10)



#Colors and Fonts
options_frame_color = '#b6d7b9' #'#9abd97' 
root_color = '#d0f1bf'
text_box_color = '#d4f2db'#'#dbd56e'
root.config(bg = root_color)
my_font = tkFont.Font(family="Comic Sans MS", size=12)
style = ttk.Style()
style.theme_use('clam')
style.configure("Vertical.TScrollbar", gripcount=10, lightcolor="#8cffda",
                troughcolor="#cef7a0", bordercolor='#7d7c84', arrowcolor="#de8f6e",darkcolor='#2d93ad',arrowsize=18,sliderlength = 5,background='#2d93ad')

# hs = ttk.Scrollbar(root, orient="vertical")
# hs.place(x=5, y=5, width=40,height=100)
# hs.set(0.2,0.3)


#Frames
options_frame = tkinter.Frame(root,bg= options_frame_color)
options_frame.pack(pady=(0,10))

new_file_image = tkinter.PhotoImage(file='new_file.png')
new_file = tkinter.Label(options_frame,image = new_file_image,bg=options_frame_color)
new_file.bind("<Button-1>", command)

open_file_image = tkinter.PhotoImage(file='open.png')
open_file = tkinter.Label(options_frame,image =open_file_image,bg=options_frame_color)
open_file.bind("<Button-1>", command)

save_file_image = tkinter.PhotoImage(file = 'save.png')
save_file = tkinter.Label(options_frame,image = save_file_image,bg = options_frame_color)
save_file.bind("<Button-1>", command)

save_to_cloud_image = tkinter.PhotoImage(file = 'cloud.png')
save_to_cloud = tkinter.Label(options_frame,image=save_to_cloud_image,bg=options_frame_color)
save_to_cloud.bind("<Button-1>", command)

share_file_image = tkinter.PhotoImage(file= 'sendemail.png')
share_file = tkinter.Label(options_frame,image=share_file_image,bg=options_frame_color)
share_file.bind("<Button-1>", command)
display_option_widgets()

my_scroll_bar = ttk.Scrollbar(root,orient = 'vertical')
text = tkinter.Text(root,yscrollcommand = my_scroll_bar.set,font=my_font,bg=text_box_color)
my_scroll_bar.config(command=text.yview)
text.pack(expand=True,fill=BOTH,side=LEFT)
my_scroll_bar.pack(fill='y',side=RIGHT)

#bindings
#"<Control-s>"
root.bind_all("<F11>",lambda event: full_screen_mode(event))
root.bind_all("<Escape>",lambda event: root.attributes("-fullscreen",False))
# three_dots.bind('<Enter>',lambda event:  display_options_frame(event))
# options_frame.bind('<Leave>',lambda event: hide_options_frame(event))

#mainloop
root.mainloop()