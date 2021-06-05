from __future__ import print_function
import tkinter
from tkinter import LEFT,RIGHT,BOTH,END,ttk,messagebox,filedialog
import tkinter.font as tkFont
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from apiclient import errors
from googleapiclient.http import MediaFileUpload
import mimetypes


#window
root = tkinter.Tk()
root.resizable(1,1)
root.geometry('1000x600')
root.wm_minsize(1000,600)
root.iconbitmap('notepad.ico')
root.title('Notepad')
file_name = ''
prev_length = 0
# mime_type =  "*/*"#'text/plain'

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

def create_google_drive_service():
    creds = None
    service = None
    SCOPES = ['https://www.googleapis.com/auth/drive']
    try:
        if os.path.exists('token.json'):
            creds = Credentials.from_authorized_user_file('token.json', SCOPES)
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    'credentials.json', SCOPES)
                creds = flow.run_local_server(port=0)
            with open('token.json', 'w') as token:
                token.write(creds.to_json())
        service = build('drive', 'v3', credentials=creds)
    except Exception:
        messagebox.showerror('Google Drive', 'Error occurred while connecting to google drive api')
    return service

def insert_file(event):
  service  = create_google_drive_service()
  if(service != None):  
    global file_name
    print(file_name)
    mime_type = get_mime_type(file_name)
    print(mime_type)
    media_body = MediaFileUpload(file_name, mimetype=mime_type, resumable=True)
    body = {
        'name': file_name,
    }
    try:
        file = service.files().create(
            body=body,
            media_body=media_body).execute()
        messagebox.showinfo('Upload File', 'File has been successfully uploaded')
        print(file)
        return file
    except errors.HttpError as error:
        messagebox.showerror('Upload File','An error occurred: %s' % error)
        return None
  return; 

def get_mime_type(file_name):
    try:
        return mimetypes.MimeTypes().guess_type('my_file.txt')[0]
    except Exception:
        return '*/*'

def display_option_widgets():
    new_file.grid(row = 0,column=0,padx=10)
    open_file.grid(row =0,column=1,padx=10)
    save_file.grid(row = 0,column=2,padx=10)
    save_to_cloud.grid(row = 0,column=3,padx=(5,10))
    share_file.grid(row = 0,column=4,padx=10)
    text.pack(expand=True,fill=BOTH,side=LEFT)
    my_scroll_bar.pack(fill='y',side=RIGHT)

def new_note(event):
    global file_name,prev_length
    question = messagebox.askyesno("New Note", "Are you sure you want to start a new note?")
    if question == 1:
        file_name = ''
        root.title('Untitled.txt-Notepad')
        text.delete("1.0", END)
        prev_length = 0

def save_note(event):
    global file_name,prev_length
    if file_name == '':
        file_name = filedialog.asksaveasfilename(initialdir="./", title="Save Note", filetypes=(("Text Files", "*.txt"), ("All Files", "*.*")))
    if(file_name !=''):
        file_name = file_name.split("/")[-1]
        root.title(file_name+"-Notepad")
        with open(file_name, 'w') as f:
            f.write(text.get("1.0", END))
        prev_length = len(text.get("1.0",END))


def open_note(event):
    global file_name,prev_length
    open_name = filedialog.askopenfilename(initialdir="./", title='Open Note', filetypes=(("Text Files", "*.txt"), ("All Files", "*.*")))
    if(open_name!= ''):
        file_name = open_name.split("/")[-1]
        root.title(file_name+"-Notepad")
        with open(open_name, 'r') as f:
            text.delete("1.0", END)
            t = f.read()
            text.insert("1.0", t)
        prev_length = len(text.get("1.0",END))

def note_changed(event):
    global prev_length
    if(prev_length!=len(text.get("1.0",END))):
        prev_length = len(text.get("1.0",END))
        if(file_name ==''):
            root.title('*Untitled.txt-Notepad')
        else:
            root.title('*'+file_name+'-Notepad')    


#Colors and Fonts
options_frame_color = '#b6d7b9'
root_color = '#d0f1bf'
text_box_color = '#d4f2db'
root.config(bg = root_color)
my_font = tkFont.Font(family="Comic Sans MS", size=12)
style = ttk.Style()
style.theme_use('clam')
style.configure("Vertical.TScrollbar", gripcount=10, lightcolor="#8cffda",
                troughcolor="#cef7a0", bordercolor='#7d7c84', arrowcolor="#de8f6e",darkcolor='#2d93ad',arrowsize=18,sliderlength = 5,background='#2d93ad')

#Frames
options_frame = tkinter.Frame(root,bg= options_frame_color)
options_frame.pack(pady=(0,10))

new_file_image = tkinter.PhotoImage(file='new_file.png')
new_file = tkinter.Label(options_frame,image = new_file_image,bg=options_frame_color)
new_file.bind("<Button-1>", new_note)

open_file_image = tkinter.PhotoImage(file='open.png')
open_file = tkinter.Label(options_frame,image =open_file_image,bg=options_frame_color)
open_file.bind("<Button-1>", open_note)

save_file_image = tkinter.PhotoImage(file = 'save.png')
save_file = tkinter.Label(options_frame,image = save_file_image,bg = options_frame_color)
save_file.bind("<Button-1>", save_note)

save_to_cloud_image = tkinter.PhotoImage(file = 'cloud.png')
save_to_cloud = tkinter.Label(options_frame,image=save_to_cloud_image,bg=options_frame_color)
save_to_cloud.bind("<Button-1>", insert_file)

share_file_image = tkinter.PhotoImage(file= 'sendemail.png')
share_file = tkinter.Label(options_frame,image=share_file_image,bg=options_frame_color)
share_file.bind("<Button-1>", command)

my_scroll_bar = ttk.Scrollbar(root,orient = 'vertical')
text = tkinter.Text(root,yscrollcommand = my_scroll_bar.set,font=my_font,bg=text_box_color,undo=True)
my_scroll_bar.config(command=text.yview)

display_option_widgets()

#bindings
root.bind_all("<F11>",lambda event: full_screen_mode(event))
root.bind_all("<Escape>",lambda event: root.attributes("-fullscreen",False))
root.bind_all("<Control-s>",save_note)
root.bind_all("<Control-n>",new_note)
root.bind_all("<Control-o>",open_note)
root.bind_all("<Control-u>",insert_file)
text.bind("<Key>",note_changed)

#mainloop
root.mainloop()