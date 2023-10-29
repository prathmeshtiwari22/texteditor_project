
from tkinter import *
from tkinter.ttk import *
from tkinter import font,colorchooser
from tkinter.messagebox import *
from tkinter import filedialog,messagebox
from PIL import ImageTk, Image
import os
import tempfile
from datetime import datetime
from textblob import TextBlob
import subprocess
import pytesseract
import pygame
import speech_recognition as sr
import pyttsx3
from fpdf import FPDF
includefiles=['']

#Funtionality Part



def corrector():

    def ClearAll():
        findentryField1.delete(0, END)
        replaceentryField1.delete(0, END)

    def replace_text():
        input_word = findentryField1.get()
        blob_obj = TextBlob(input_word)
        corrected_word = str(blob_obj.correct())
        replaceentryField1.insert(10, corrected_word)


    root2 = Toplevel()
    root2.title('Corrector')
    root2.geometry('450x250+500+200')
    root2.resizable(0, 0)
    labelFrame =LabelFrame(root2, text='You can Corrector Word here:')
    labelFrame.pack()

    findlabel1 =Label(labelFrame, text='Input Word')
    findlabel1.grid(row=0, column=0, padx=5, pady=5)
    findentryField1 = Entry(labelFrame)
    findentryField1.grid(row=0, column=1, padx=5, pady=5)

    replacelabel1 = Label(labelFrame, text='Corrected Word')
    replacelabel1.grid(row=1, column=0, padx=5, pady=5)
    replaceentryField1 = Entry(labelFrame)
    replaceentryField1.grid(row=1, column=1, padx=5, pady=5)

    findButton = Button(labelFrame, text='Correct', command=replace_text)
    findButton.grid(row=2, column=0, padx=5, pady=5 )
    replaceButton = Button(labelFrame, text='Replace',  command=ClearAll)
    replaceButton.grid(row=2, column=1, padx=5, pady=5)



    root2.protocol('WM_DELETE_WINDOW', quit)
    root2.mainloop()



def printout(event=None):
    file=tempfile.mktemp('.txt')
    open(file,'w').write(textarea.get(1.0,END))
    os.startfile(file,'Print')


def date_time(event=None):
    current=datetime.now()
    format=current.strftime('%d/%m/%Y %H:%M:%S')
    textarea.insert(1.0,format)





def change_theme(bg_color,fg_color):
    textarea.config(bg=bg_color,fg=fg_color)

def toolbarfunc():
    if show_toolbar.get()==False:
        tool_bar.pack_forget()
    if show_toolbar.get()==True:
        textarea.pack_forget()
        tool_bar.pack(fill=X)
        textarea.pack(fill=BOTH,expand=1)


def Statusbarfunc():
    if show_statusbar.get()==False:
        status_bar.pack_forget()
    if show_statusbar.get()==True:
        status_bar.pack()



def find1():

    #function
    def find_words():
        textarea.tag_remove('match',1.0,END)
        start_pos='1.0'
        word=findentryField.get()
        if word:
            while True:
                start_pos=textarea.search(word,start_pos,stopindex=END)
                if not start_pos:
                    break
                end_pos=f"{start_pos}+{len(word)}c"
                textarea.tag_add('match',start_pos,end_pos)

                textarea.tag_config('match',foreground='white',background='red')
                start_pos=end_pos
        else:
            pass

    def replace_text():
        word =findentryField.get()
        replaceword=replaceentryField.get()
        content=textarea.get(1.0,END)
        newcontent=content.replace(word,replaceword)
        textarea.delete(1.0,END)
        textarea.insert(1.0,newcontent)


    root1=Toplevel()
    root1.title('Find')
    root1.geometry('450x250+500+200')
    root1.resizable(0,0)
    labelFrame =LabelFrame(root1,text='You can FIND/REPLACE:')
    labelFrame.pack()

    findlabel=Label(labelFrame,text='Find')
    findlabel.grid(row=0,column=0,padx=5,pady=5)
    findentryField=Entry(labelFrame)
    findentryField.grid(row=0,column=1,padx=5,pady=5)

    replacelabel = Label(labelFrame, text='Replace')
    replacelabel.grid(row=1, column=0, padx=5, pady=5)
    replaceentryField = Entry(labelFrame)
    replaceentryField.grid(row=1, column=1, padx=5, pady=5)

    findButton=Button(labelFrame,text='FIND',command=find_words)
    findButton.grid(row=2,column=0,padx=5,pady=5)

    replaceButton = Button(labelFrame, text='REPLACE',command=replace_text)
    replaceButton.grid(row=2, column=1, padx=5, pady=5)

    def dosomething():
        textarea.tag_remove('match',1.0,END)
        root1.destroy()

    root1.protocol('WM_DELETE_WINDOW',dosomething)
    root1.mainloop()

def StatusBarFunction(event):
    if textarea.edit_modified():
        word=len(textarea.get(0.0,END).split())
        char=len(textarea.get(0.0,'end-1c').replace(' ',''))
        status_bar.config(text=f'Characters: {char} Words: {word}')



    textarea.edit_modified(False)


url=''
def new_file(event):
    a=0
    if a==0:
        textarea.delete(0.0,END)
        a=1
    if a==1:
        global url
        url=''
        root.title("Untited")

def open_file():
    global url
    url=filedialog.askopenfilename(initialdir=os.getcwd,title="Select File",filetypes=(('Text File','txt'),('All Files','*.*')))

    if url !='':
        data=open(url,'r')
        textarea.insert(0.0,data.read())
    root.title(os.path.basename(url))

def save_file():
    if url =='':
        save_url=filedialog.asksaveasfile(mode='w',defaultextension='.txt',filetypes=(('Text File','txt'),('All Files','*.*')))
        content=textarea.get(0.0,END)
        save_url.write(content)
        save_url.close()

    else:
        content=textarea.get(0.0,END)
        file=open(url,'w')
        file.write(content)
        #os.remove(url)

def saveas_file():
    save_url = filedialog.asksaveasfile(mode='w', defaultextension='.txt',
                                        filetypes=(('Text File', 'txt'), ('All Files', '*.*')))
    content = textarea.get(0.0, END)
    save_url.write(content)
    save_url.close()
    if url !='':
        os.remove(url)

def iexit():
    if textarea.edit_modified():
        Result=messagebox.askyesnocancel('Warning','Do you want to Save File ?')
        if Result is True:
            if url!='':
                content=textarea.get(0.0,END)
                file=open(url,'w')
                file.write(content)
                root.destroy()

            else:
                content = textarea.get(0.0, END)
                save_url = filedialog.asksaveasfile(mode='w', defaultextension='.txt',
                                                filetypes=(('Text File', 'txt'), ('All Files', '*.*')))
                save_url.write(content)
                save_url.close()
                root.destroy()

        elif Result is False:
            root.destroy()

        else:
            pass

    else:
        root.destroy()


fontSize=12
fontStyle='arial'
def font_style(event):
    global fontStyle
    fontStyle=font_families_variable.get()
    textarea.config(font=(fontStyle,fontSize))

def font_size(event):
    global fontSize
    fontSize=size_variables.get()
    textarea.config(font=(fontStyle,fontSize))

def bold_text():
   text_property=font.Font(font=textarea['font']) .actual()
   if text_property['weight']=='normal':
       textarea.config(font=(fontStyle,fontSize,'bold'))
   if text_property['weight']=='bold':
       textarea.config(font=(fontStyle,fontSize,'normal'))

def italic_text():
   text_property=font.Font(font=textarea['font']) .actual()
   if text_property['slant']=='roman':
       textarea.config(font=(fontStyle,fontSize,'italic'))
   if text_property['slant']=='italic':
       textarea.config(font=(fontStyle,fontSize,'roman'))

def underline_text():
   text_property=font.Font(font=textarea['font']) .actual()
   if text_property['underline']==0:
       textarea.config(font=(fontStyle,fontSize,'underline'))
   if text_property['underline']==1:
       textarea.config(font=(fontStyle,fontSize))

def color_select():
    color=colorchooser.askcolor()
    textarea.config(fg=color[1])

def align_right():
    data=textarea.get(0.0,END)
    textarea.tag_config('right',justify=RIGHT)
    textarea.delete(0.0,END)
    textarea.insert(INSERT,data,'right')


def align_left():
    data = textarea.get(0.0, END)
    textarea.tag_config('left', justify=LEFT)
    textarea.delete(0.0, END)
    textarea.insert(INSERT, data, 'left')


def align_center():
    data = textarea.get(0.0, END)
    textarea.tag_config('center', justify=CENTER)
    textarea.delete(0.0, END)
    textarea.insert(INSERT, data, 'center')



def save_as_pdf():
    filename = filedialog.asksaveasfilename(defaultextension=".pdf", filetypes=[("PDF Files", "*.pdf")])
    if filename:
        temp_file = os.path.splitext(filename)[0] + '.ps'
        with open(temp_file, 'w') as file:
            file.write(textarea.get("1.0", "end"))
        try:
            process = subprocess.Popen(['ps2pdf', temp_file, filename])
            process.communicate()
        except FileNotFoundError:
            messagebox.showerror("Save As PDF", "Unable to find ps2pdf command. Please install Ghostscript.")
            os.remove(temp_file)
            return
        os.remove(temp_file)
        messagebox.showinfo("Save As PDF", "File saved successfully.")


def open_image():
    root2 = Toplevel()
    root2.title(' TEXT TO SPEECH')
    root2.geometry('850x550+500+200')
    root2.resizable(0, 0)

    def stot():
        text = speech_to_text()
        my_entry.delete(0, END)
        my_entry.insert(0, text)

    def talk():
        engine = pyttsx3.init()
        voices = engine.getProperty('voices')
        engine.setProperty('voice', voices[1].id)
        engine.say(my_entry.get())
        engine.runAndWait()
        my_entry.delete(0, END)

    def speech_to_text():
        # Initialize the speech recognizer
        r = sr.Recognizer()

        # Use the default microphone as the audio source
        with sr.Microphone() as source:
            print("Speak now...")
            audio = r.listen(source)

        # Attempt to recognize speech in the audio
        try:
            text = r.recognize_google(audio)
            return text
        except sr.UnknownValueError:
            return "Could not understand audio"
        except sr.RequestError as e:
            return "Error: {0}".format(e)

    labelFrame = LabelFrame(root2, text='You can GENERATE WORDS HERE:')
    labelFrame.pack()

    findlabel = Label(labelFrame, text='WORDS')
    findlabel.grid(row=0, column=0, padx=5, pady=5)

    my_entry = Entry(labelFrame, font=("Helvetica", 28))
    my_entry.grid(row=2, column=2, pady=20)

    my_button = Button(labelFrame, text='Speak', command=talk)
    my_button.grid(row=4, column=4, pady=20)

    button = Button(labelFrame, text='Say', command=stot)
    button.grid(row=4, column=2, pady=20)

    def dosomething():
        root2.destroy()

    root2.protocol('WM_DELETE_WINDOW', dosomething)
    root2.mainloop()


def help7():
    showinfo("Text Editor","YOU CAN ACCESS THIS SIR....")

root = Tk()
root.title("TEXT EDITOR")
root.geometry("1200x620+10+10")
root.resizable(False,False)
menubar=Menu()
root.config(menu=menubar)

#filemenu

filemenu=Menu(menubar,tearoff=False)
menubar.add_cascade(label='File',menu=filemenu)
newImage=PhotoImage(file="new.png")
opemImage=PhotoImage(file="open.png")
saveImage=PhotoImage(file="save.png")
saveasImage=PhotoImage(file="save_as.png")
exitImage=PhotoImage(file="exit.png")
printImage=PhotoImage(file='print.png')
pdfimage=PhotoImage(file='pdf.png')
filemenu.add_command(label='New',accelerator='Ctrl+N',image=newImage,compound=LEFT,command=new_file)
filemenu.add_command(label='Open',accelerator='Ctrl+O',image=opemImage,compound=LEFT,command=open_file)
filemenu.add_command(label='Save',accelerator='Ctrl+S',image=saveImage,compound=LEFT,command=save_file)
filemenu.add_command(label='Save As',accelerator='Ctrl+Alt+S',image=saveasImage,compound=LEFT,command=saveas_file)
filemenu.add_command(label='Save As PDF',accelerator='Ctrl+Alt+P',image=pdfimage,compound=LEFT,command=save_as_pdf)
filemenu.add_command(label='Print',accelerator='Ctrl+Alt+P',image=printImage,compound=LEFT,command=printout)
filemenu.add_separator()
filemenu.add_command(label='Exit',accelerator='Ctrl+N',image=exitImage  ,compound=LEFT,command=iexit)



#toolbar section
tool_bar=Label(root)
tool_bar.pack(side=TOP,fill=X)
font_families=font.families()
font_families_variable=StringVar()
fontfamily_combobox=Combobox(tool_bar,width=30,values=font_families,state='readonly',textvariable=font_families_variable)
fontfamily_combobox.current(font_families.index('Arial'))
fontfamily_combobox.grid(row=0,column=0,padx=5)
size_variables=IntVar()
font_size_Combobox=Combobox(tool_bar,textvariable=size_variables,state='readonly',values=tuple(range(8,81)))
font_size_Combobox.current(4)
font_size_Combobox.grid(row=0,column=1,padx=5)

fontfamily_combobox.bind('<<ComboboxSelected>>',font_style)
font_size_Combobox.bind('<<ComboboxSelected>>',font_size)


#BUTTON SECTIONS
bold=PhotoImage(file="bold.png")
boldButton=Button(tool_bar,image=bold,command=bold_text)
boldButton.grid(row=0,column=2,padx=5)



italic=PhotoImage(file="italic.png")
italicButton=Button(tool_bar,image=italic,command=italic_text)
italicButton.grid(row=0,column=3,padx=5)

underline=PhotoImage(file="underline.png")
underlineButton=Button(tool_bar,image=underline,command=underline_text)
underlineButton.grid(row=0,column=4,padx=5)

fcolor=PhotoImage(file="font_color.png")
fcolorButton=Button(tool_bar,image=fcolor,command=color_select)
fcolorButton.grid(row=0,column=5,padx=5)



leftalign=PhotoImage(file="left.png")
leftalignButton=Button(tool_bar,image=leftalign,command=align_left)
leftalignButton.grid(row=0,column=6,padx=5)

rightalign=PhotoImage(file="right.png")
rightalignButton=Button(tool_bar,image=rightalign,command=align_right)
rightalignButton.grid(row=0,column=7,padx=5)

centeralign=PhotoImage(file="center.png")
centeralignButton=Button(tool_bar,image=centeralign,command=align_center)
centeralignButton.grid(row=0,column=8,padx=5)

insert=PhotoImage(file='speak.png')
insertimageButton=Button(tool_bar,image=insert,command=open_image)
insertimageButton.grid(row=0,column=9,padx=5)



scrollbar=Scrollbar(root)
scrollbar.pack(side=RIGHT,fill=Y)
#Text Area
textarea=Text(root,yscrollcommand=scrollbar.set,font=('arial',12),undo=True)
textarea.pack(fill=BOTH,expand=TRUE)
scrollbar.config(command=textarea.yview)

#STATUS BAR
status_bar=Label(root,text="Status Bar")
status_bar.pack(side=BOTTOM)

textarea.bind('<<Modified>>',StatusBarFunction)


#edit menu
cut=PhotoImage(file="cut.png")
copy=PhotoImage(file="copy.png")
paste=PhotoImage(file="paste.png")
clear=PhotoImage(file="clear_all.png")
select=PhotoImage(file='selectall.png')
undo=PhotoImage(file='undo.png')
editmenu=Menu(menubar,tearoff=False)
editmenu.add_command(label='Undo',accelerator='Ctrl+Z',image=undo,compound=LEFT)
editmenu.add_command(label='Cut',accelerator='Ctrl+X',image=cut,compound=LEFT,command=lambda :textarea.event_generate('<Control x>'))
editmenu.add_command(label='Copy',accelerator='Ctrl+C',image=copy,compound=LEFT,command=lambda :textarea.event_generate("<Control c>"))
editmenu.add_command(label='Paste',accelerator='Ctrl+V',image=paste,compound=LEFT,command=lambda :textarea.event_generate("<Control v>"))
editmenu.add_command(label='Clear',accelerator='Ctrl+Alt+X',image=clear,compound=LEFT,command=lambda :textarea.delete(0.0,END))
editmenu.add_command(label='Select All',accelerator='Ctrl+A',image=select,compound=LEFT)
menubar.add_cascade(label='Edit',menu=editmenu)

#view menu section
show_toolbar=BooleanVar()
show_statusbar=BooleanVar()
tool=PhotoImage(file="tool_bar.png")
status=PhotoImage(file="status_bar.png")
viewmenu=Menu(menubar,tearoff=False)
viewmenu.add_checkbutton(label="Toolbar",variable=show_toolbar,onvalue=True,offvalue=False,image=tool,compound=LEFT,command=toolbarfunc)
show_toolbar.set(True)
viewmenu.add_checkbutton(label="Statusbar",variable=show_statusbar,onvalue=True,offvalue=False,image=status,compound=LEFT,command=Statusbarfunc)
show_statusbar.set(True)
menubar.add_cascade(label="View",menu=viewmenu)

#themes menu section
themesmenu=Menu(menubar,tearoff=False)

theme_choice=StringVar()
light=PhotoImage(file='light_default.png')
dark=PhotoImage(file='dark.png')
blue=PhotoImage(file='night_blue.png')
pink=PhotoImage(file="red.png")
orange=PhotoImage(file="orange.png")
themesmenu.add_radiobutton(label="Light Default",image=light,variable=theme_choice,compound=LEFT,command=lambda :change_theme('white','black'))
themesmenu.add_radiobutton(label="Dark",image=dark,variable=theme_choice,compound=LEFT,command=lambda :change_theme('black','white'))
themesmenu.add_radiobutton(label="Pink",image=pink,variable=theme_choice,compound=LEFT,command=lambda :change_theme('pink','red'))
themesmenu.add_radiobutton(label="Blue",image=blue,variable=theme_choice,compound=LEFT,command=lambda :change_theme('blue','black'))
themesmenu.add_radiobutton(label="Orange",image=orange,variable=theme_choice,compound=LEFT,command=lambda :change_theme('orange','dark blue'))
menubar.add_cascade(label="Themes",menu=themesmenu)





#help menu
help=PhotoImage(file='help.png')
helpmenu = Menu(menubar,tearoff=False)
menubar.add_cascade(label='Help',menu=helpmenu)
helpmenu.add_command(label='About Notepad',command=help7,image=help)

#other button

find=PhotoImage(file="find.png")
replace=PhotoImage(file='replace.png')
othermenu =Menu(menubar,tearoff=False)
menubar.add_cascade(label='Find',menu=othermenu)
othermenu.add_command(label='Find',accelerator='Ctrl+F',image=find,compound=LEFT,command=find1)

#corrector button

correct=PhotoImage(file="find.png")
pattern=PhotoImage(file='checked.png')
correctmenu=Menu(menubar,tearoff=False)
menubar.add_cascade(label="Corrector",menu=correctmenu)
#correctmenu.add_command(label="pattern",image=pattern,command=open_image,compound=LEFT)
correctmenu.add_command(label="checker",image=correct,command=corrector,compound=LEFT)


#Text to speech
#texttospeech.add_command(label='Text',accelerator='Ctrl+T',image=text,compound=LEFT,command=text_tospeech)


#DATE BUTTON
date=PhotoImage(file='dateandtime.png')
datemenu =Menu(menubar,tearoff=False)
menubar.add_cascade(label='Date&Time',menu=datemenu)
datemenu.add_command(label='DATE',accelerator='Ctrl+D',image=date,compound=LEFT,command=date_time)



root.wm_iconbitmap('icon_3.ico')
root.mainloop()