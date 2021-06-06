from __future__ import print_function
import tkinter
from tkinter import LEFT,RIGHT,BOTH,END,ttk,messagebox,filedialog
import tkinter.font as tkFont
from tkinter import simpledialog
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from apiclient import errors
from googleapiclient.http import MediaFileUpload
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.audio import MIMEAudio
from email.mime.base import MIMEBase
import base64
import re
import mimetypes


#window
root = tkinter.Tk()
root.resizable(1,1)
root.geometry('1000x600')
root.wm_minsize(1000,600)
root.iconbitmap('notepad.ico')
root.title('Notepad')
file_name = ''
path = ''
prev_length = 0
drive_service = None
gmail_service = None
SCOPES = ['https://www.googleapis.com/auth/drive','https://www.googleapis.com/auth/gmail.send']
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

def create_service():
    global gmail_service,drive_service,SCOPES
    creds = None
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
        drive_service = build('drive','v3', credentials=creds)
        gmail_service = build('gmail', 'v1',credentials=creds)
    except Exception as error:
        messagebox.showerror('Service', 'Error occurred while creating service')
        print(error)
    

def insert_file(event):
  create_service()
  service = drive_service
  if(service != None):  
    global file_name
    print(file_name)
    mime_type = get_mime_type(file_name)
    print(path)
    media_body = MediaFileUpload(path, mimetype=mime_type, resumable=True)
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

def send_to_email(event):
    create_service()
    service = gmail_service
    if(service !=None):
        to = simpledialog.askstring('Email','Enter To Email Address')
        validate_email(to)
        print('path',path)
        message = create_message_with_attachment(to,'File from Notepad App','This is file is attached from Notepad app',path)
        send_message(service,"me",message)

def create_message_with_attachment(to, subject, message_text, file):
  file = r'{}'.format(file)
  print(file)
  message = MIMEMultipart()
  message['to'] = to
  message['subject'] = subject
  msg = MIMEText(message_text)
  message.attach(msg)
  content_type, encoding = mimetypes.guess_type(file)
  if content_type is None or encoding is not None:
    content_type = 'application/octet-stream'  
  main_type, sub_type = content_type.split('/', 1)
  print(main_type,content_type,sub_type)
  try:
    if main_type == 'text': 
        fp = open(file, 'rb')
        msg = MIMEText(main_type, sub_type)
        msg.set_payload(fp.read())
        fp.close()
    elif main_type == 'image':
        fp = open(file, 'rb')
        msg = MIMEImage(fp.read(), _subtype=sub_type)
        fp.close()
    elif main_type == 'audio':
        fp = open(file, 'rb')
        msg = MIMEAudio(fp.read(), _subtype=sub_type)
        fp.close()
    else:
        fp = open(file, 'rb')
        msg = MIMEBase(main_type, sub_type)
        msg.set_payload(fp.read())
        fp.close()
    filename = os.path.basename(file)
    msg.add_header('Content-Disposition', 'attachment', filename=filename)
    message.attach(msg)
    return {'raw': base64.urlsafe_b64encode(message.as_bytes()).decode()}
  except Exception as error:
      messagebox.showerror('Message','Error occurred while creating email message')  

def send_message(service, user_id, message):
  try:
    message = (service.users().messages().send(userId=user_id, body=message)
               .execute())
    print('Message Id: %s' % message['id'])
    messagebox.showinfo('Email', 'Sent to email successfully')
    return message
  except errors.HttpError as error:
    print('An error occurred: %s' % error)

def validate_email(email):
    regex = '^(\w|\.|\_|\-)+[@](\w|\_|\-|\.)+[.]\w{2,3}$'
    if(re.search(regex, email)):
        return email; 
    else:
        email = simpledialog.askstring('Email','Enter a valid To Email Address')
        validate_email(email)

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
    global file_name,prev_length,path
    if file_name == '':
        file_name = filedialog.asksaveasfilename(initialdir="./", title="Save Note", filetypes=(("Text Files", "*.txt"), ("All Files", "*.*")))
    if(file_name !=''):
        path = file_name
        file_name = file_name.split("/")[-1]
        root.title(file_name+"-Notepad")
        with open(file_name, 'w') as f:
            f.write(text.get("1.0", END))
        prev_length = len(text.get("1.0",END))


def open_note(event):
    global file_name,prev_length,path
    open_name = filedialog.askopenfilename(initialdir="./", title='Open Note', filetypes=(("Text Files", "*.txt"), ("All Files", "*.*")))
    if(open_name!= ''):
        path = open_name
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
share_file.bind("<Button-1>", send_to_email)

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