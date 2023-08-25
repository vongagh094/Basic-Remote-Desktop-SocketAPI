import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from tkinter import filedialog
from tkinter import PhotoImage
from PIL import Image, ImageTk
import zlib
import socket
from configparser import ConfigParser
import time

FORMAT = "utf8"
PORT = 65432
HOST = "127.0.0.1"
LARGE_FONT = ("verdana", 13,"bold")

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

class info():
    def __init__(self, ID, Name, thread):
        self.ID = ID
        self.Name = Name
        self.thread = thread
class startPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.configure(bg="bisque2")

        #label
        label_title = tk.Label(self, text = "CONNECT TO SERVER", font=LARGE_FONT,fg='#20639b',bg="bisque2")
        label_serverIP = tk.Label(self, text="IP ",fg='#20639b',bg="bisque2",font='verdana 10 ')
        self.label_notice = tk.Label(self,text="",bg="bisque2")

        #entry
        self.entry_ip = tk.Entry(self,width=20,bg='light yellow')

        #button
        self.button_con = tk.Button(self,text="CONNECT", bg="#878de4",fg='floral white',command=lambda: controller.CONNECT(self)) 
        self.button_process = tk.Button(self,text="PROCESS RUNNING", bg="#ced0f1",fg="#0b0e43",command=lambda: controller.showFrame(processRunning)) 
        self.button_app = tk.Button(self,text="APP RUNNING", bg="#ced0f1",fg="#0b0e43", command=lambda: controller.showFrame(appRunning)) 
        self.button_keyStroke = tk.Button(self,text="KEY STROKE", bg="#ced0f1",fg="#0b0e43",command=lambda: controller.showFrame(keyStroke))
        self.button_shutDown = tk.Button(self,text="SHUT DOWN", bg="#ced0f1",fg="#0b0e43",command=lambda: self.doCommand("SYSTEM SHUTDOWN")) 
        self.button_disconnect = tk.Button(self,text="DISCONNECT", bg="#ced0f1",fg="#0b0e43",command =lambda: self.disconnect("")) 
        self.button_screenShot = tk.Button(self,text="SCREEN SHOT", bg="#ced0f1",fg="#0b0e43",command = self.open_screenshot) 
        self.button_exit = tk.Button(self,text="EXIT", bg="#ced0f1",fg="#0b0e43",command =lambda: self.disconnect("EXIT"))

        #configure
        self.button_con.configure(width=10)
        self.button_process.configure(width=20, height= 21)
        self.button_app.configure(width=30, height= 6)  
        self.button_keyStroke.configure(width=25, height= 6)  
        self.button_shutDown.configure(width=13, height= 6) 
        self.button_exit.configure(width=25, height= 6)  
        self.button_disconnect.configure(width=13, height= 6)         
        self.button_screenShot.configure(width=61, height= 6)

        #position
        label_title.pack()
        label_serverIP.pack()
        self.entry_ip.pack()
        self.label_notice.pack()
        self.button_con.pack()
        self.button_process.place(x = 43, y = 146)
        self.button_app.place(x= 220, y= 145)
        self.button_keyStroke.place(x = 470, y = 145)
        self.button_shutDown.place(x= 220, y = 260)
        self.button_exit.place(x = 470, y = 260)
        self.button_disconnect.place(x = 340, y = 260)
        self.button_screenShot.place(x = 220, y = 371)

        self.comm= ""

    def on_closing(self): #closing app function
        self.destroy()

    def disconnect(self, opt):
        if(opt == "EXIT"):
            client.close()
            app.destroy()
            return
        client.close()
        self.entry_ip.config(state= tk.NORMAL)
        self.button_con.config(state= tk.NORMAL)
        self.entry_ip.delete('0','end')
        messagebox.showinfo(message= "Disconnect succsessfully!", title= "Success!")
        self.lock()


    def lock(self): #lock buttons
        self.button_process.config(state= "disabled")
        self.button_app.config(state= "disabled")
        self.button_keyStroke.config(state= "disabled")
        self.button_shutDown.config(state= "disabled")
        self.button_exit.config(state= "disabled") 
        self.button_disconnect.config(state= "disabled")        
        self.button_screenShot.config(state= "disabled")
    
    def unLock(self): #unlock buttons
        self.button_process.config(state= "normal")
        self.button_app.config(state= "normal")
        self.button_keyStroke.config(state="normal")
        self.button_shutDown.config(state= "normal")
        self.button_exit.config(state= "normal")
        self.button_disconnect.config(state= "normal")      
        self.button_screenShot.config(state= "normal")

        

    def open_screenshot(self): #screenshot pops up
        self.top= tk.Toplevel()
        self.top.geometry("700x550")
        self.top.title("SCREEN SHOT")
        self.top.configure(bg = "bisque2")
        self.top.resizable(width= False, height= False)

        self.button = tk.Button(self.top,text="CAPTURE", bg="#ced0f1",fg="#0b0e43", width=12 , height=16, command=lambda : self.doCommand("SCREEN abcdef")).place(x= 600, y = 67)
        self.button = tk.Button(self.top,text="SAVE AS", bg="#ced0f1",fg="#0b0e43", width= 12, height=6, command= self.savePic).place(x= 600, y = 340)
        self.top.grab_set()


    

    def savePic(self): #save Pic pops up
        data = [("Image Files", "*.png *.jpg")] 
        #look up only PNG and JPG files
        # use another name for the output filename
        filename = filedialog.asksaveasfilename(filetypes=data, defaultextension=data)
        if filename:
            #  save the image to the output filename
            self.image.save(filename)

    
    def doCommand(self, command): #do command
        try:
            size = str(len(command))
            client.sendall(size.encode(FORMAT))
            client.sendall(command.encode(FORMAT))
            if(command == "SCREEN abcdef"):
                self.data = self.receiveScreenshot()

                self.saveScreenshot()
                self.imageShoww("screenshot.png")

            elif(command == "SYSTEM SHUTDOWN") :
                self.data = recvData()
                print(self.data)
        except :
            messagebox.showinfo(message= "Server is not responding !", title= "Error!")


    def imageShoww(self, imageName): 
        global capture
        self.image_name = imageName
        self.image = Image.open(self.image_name)
        self.image_copy = self.image.copy()
        capture = ImageTk.PhotoImage(self.image)
        self.imageShow = tk.Label(self.top, image= capture)
        self.imageShow.bind('<Configure>', self.resizeImage)
        self.imageShow.place(x = 10, y = 20, width= 578, height= 500)

    def resizeImage(self, event):
        image = self.image_copy.resize(
            (self.master.winfo_width(), self.master.winfo_height()))
        self.newimage = ImageTk.PhotoImage(image)
        self.imageShow.config(image = self.newimage)

    def receiveScreenshot(self):
        sizeData = client.recv(4)
        size = int.from_bytes(sizeData, 'big')
        
        compressedScreenshot = b''
        while len(compressedScreenshot) < size:
            data = client.recv(size - len(compressedScreenshot))
            if not data:
                break
            compressedScreenshot += data
        screenshot = zlib.decompress(compressedScreenshot)
        return screenshot
    
    def saveScreenshot(self):
        open('screenshot.png', 'wb').write(self.data)
    


class keyStroke(tk.Frame): #key stroke frame
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.configure(bg="bisque2")

        #button        
        button_hook = tk.Button(self,text="HOOK", bg="#ced0f1",fg="#0b0e43", command=lambda : self.doCommand("KEYSTROKE HOOK")) 
        button_unHook = tk.Button(self,text="UNHOOK", bg="#ced0f1",fg="#0b0e43", command=lambda : self.doCommand("KEYSTROKE UNHOOK"))
        button_prInt = tk.Button(self,text="PRINT", bg="#ced0f1",fg="#0b0e43", command=lambda : self.doCommand("KEYSTROKE VIEW")) 
        button_back = tk.Button(self,text="TO START PAGE", bg="#ced0f1",fg="#0b0e43", command= lambda : controller.showFrame(startPage) or self.doCommand("KEYSTROKE QUIT"))
        button_del = tk.Button(self,text="DELETE", bg="#ced0f1",fg="#0b0e43",command=self.delete)

        #configure
        button_hook.configure(width=15, height= 4)
        button_unHook.configure(width=15, height= 4)
        button_prInt.configure(width=15, height= 4)
        button_del.configure(width=15, height= 4)
        button_back.configure(width=15, height=1 )

        #text
        self.text=tk.Text(self, font=("Georgia, 13"), width= 60, height= 10)

        #position
        button_hook.place(x = 32, y = 24)
        button_unHook.place(x = 172, y= 24)
        button_prInt.place(x = 312, y= 24)
        button_del.place(x = 452, y = 24)
        button_back.place(x = 455, y = 350)
        self.text.place(x = 24, y= 130)

    #supportive function
    def get_value(self, command):
        self.comm = command
        print(command)

    def delete(self):
        self.text.delete('1.0', 'end')

    def insertText(self):
        self.text.insert('end', self.data)
        
    def doCommand(self, command):
        try:
            size = str(len(command))
            client.sendall(size.encode(FORMAT))
            client.sendall(command.encode(FORMAT))
            self.data = recvData()
            if(command== "KEYSTROKE VIEW"):   
                self.insertText()
        except :
            messagebox.showinfo(message= "Server is not responding !", title= "Error!")


class appRunning(tk.Frame): #app running frame
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.configure(bg="bisque2")

        #button
        button_kill = tk.Button(self,text="KILL", bg="#ced0f1",fg="#0b0e43",command=self.open_kill) 
        button_check = tk.Button(self,text="CHECK", bg="#ced0f1",fg="#0b0e43",command= lambda : self.doCommand("", "APP VIEW")) 
        button_del = tk.Button(self,text="DELETE", bg="#ced0f1",fg="#0b0e43",command= self.delete) 
        button_start = tk.Button(self,text="START", bg="#ced0f1",fg="#0b0e43",command=self.open_start) 
        button_back = tk.Button(self,text="TO START PAGE", bg="#ced0f1",fg="#0b0e43",command=lambda: controller.showFrame(startPage)) 

        #configure
        button_kill.configure(width=15, height= 4)
        button_check.configure(width=15, height= 4)
        button_del.configure(width=15, height= 4)
        button_start.configure(width=15, height= 4)
        button_back.configure(width=15, height=1 )


        #tree view
        cols = ("Name Application", "ID Application", "Court Thread")
        self.my_tree = ttk.Treeview(self, column = cols, height= 10, selectmode = "browse", show = 'headings')
        self.my_tree.column("#1", anchor= tk.CENTER, stretch= 'no', width= 175)
        self.my_tree.heading("#1", text="Name Application")
        self.my_tree.column("#2", anchor= tk.CENTER, stretch= 'no', width = 175)
        self.my_tree.heading("#2", text="ID Application")
        self.my_tree.column("#3", anchor= tk.CENTER, stretch= 'no', width = 175)
        self.my_tree.heading("#3", text="Court Thread")

        tree_scroll = ttk.Scrollbar(self, orient= "vertical")
        tree_scroll.configure(command= self.my_tree.yview)
        self.my_tree.configure(yscrollcommand= tree_scroll.set)
        
        #position
        self.my_tree.place(x = 24, y = 130)
        tree_scroll.place(x = 552, y= 130, height= 226)
        button_kill.place(x = 32, y = 24)
        button_check.place(x = 172, y= 24)
        button_del.place(x = 312, y= 24)
        button_start.place(x = 452, y = 24)
        button_back.place(x = 455, y = 365)

        self.arrayInfo = []

    #supportive function - pops up
    def get_value(self, variable, command):
        value = variable.get()
        self.variable = value
        self.comm = command
        print(value)
        print(command)

    def open_kill(self):
        top= tk.Toplevel()
        top.geometry("250x70")
        top.title("KILL")
        top.configure(bg = "bisque2")
        tk.Label(top, text="ID ",fg='#20639b',bg="bisque2",font='verdana 10 ').place(x = 27, y = 27)
        self.entry_id = tk.Entry(top,width=20,bg='light yellow')
        top.button = tk.Button(top,text="KILL", bg="#ced0f1",fg="#0b0e43", width= 6, height=1, command=lambda: self.doCommand(self.entry_id, "APP KILL")).place(x= 185, y = 27)
        self.entry_id.place(x = 57, y = 30)
        top.grab_set()


    def open_start(self):
        top= tk.Toplevel()
        top.geometry("250x70")
        top.title("START")
        top.configure(bg = "bisque2")
        tk.Label(top, text="NAME ",fg='#20639b',bg="bisque2",font='verdana 10 ').place(x = 12, y = 27)
        self.entry_id = tk.Entry(top,width=20,bg='light yellow')
        top.button = tk.Button(top,text="START", bg="#ced0f1",fg="#0b0e43", width= 6, height=1, command=lambda: self.doCommand(self.entry_id, "APP START")).place(x= 185, y = 27)
        self.entry_id.place(x = 57, y = 30)
        top.grab_set()


    def delete(self):
        for i in self.my_tree.get_children():
            self.my_tree.delete(i)

    def insertText(self):
        self.delete()
        for i in range (0, len(self.arrayInfo)) :
            self.my_tree.insert("", 'end', values= (self.arrayInfo[i].ID, self.arrayInfo[i].Name, self.arrayInfo[i].thread))

    def doCommand(self, entry, command):
        id = ""
        if(entry != ""):
            id = entry.get()
        
        try:
            if(command != "APP VIEW") :
                command = command +" " + id
            size = str(len(command))
            client.sendall(size.encode(FORMAT))
            client.sendall(command.encode(FORMAT))
            if(command== "APP VIEW"):
                self.data = recvData()
                rows = self.data.split('\n')
                self.arrayInfo.clear()
                for row in rows:
                    cols = row.split('|')
                    self.arrayInfo.append(info(cols[0], cols[1], int(cols[2])))
                self.insertText()
            else : 
                print(1)
                self.data = recvData()
                print(self.data)
        except :
            messagebox.showinfo(message= "Server is not responding !", title= "Error!")

    
def recvData():
    sizeData = client.recv(1024).decode(FORMAT)
    size = int(sizeData)

    data = b''
    while len(data) < size:
        tmp = client.recv(1024)
        if not tmp:
            break
        data += tmp
    return data.decode(FORMAT)


class processRunning(tk.Frame): #process running frame
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.configure(bg="bisque2")

        #buttons
        button_kill = tk.Button(self,text="KILL", bg="#ced0f1",fg="#0b0e43",command=self.open_kill) 
        button_check = tk.Button(self,text="CHECK", bg="#ced0f1",fg="#0b0e43",command= lambda : self.doCommand("", "PROCESS VIEW"))
        button_del = tk.Button(self,text="DELETE", bg="#ced0f1",fg="#0b0e43",command=self.delete) 
        button_start = tk.Button(self,text="START", bg="#ced0f1",fg="#0b0e43",command=self.open_start)
        button_back = tk.Button(self,text="TO START PAGE", bg="#ced0f1",fg="#0b0e43",command=lambda: controller.showFrame(startPage)) 

        #configure
        button_kill.configure(width=15, height= 4)
        button_check.configure(width=15, height= 4)
        button_del.configure(width=15, height= 4)
        button_start.configure(width=15, height= 4)
        button_back.configure(width=15, height=1 )


        #tree view
        cols = ("Name Proces", "ID Process", "Court Thread")
        self.my_tree = ttk.Treeview(self, column = cols, height= 10, selectmode = "browse", show = 'headings')
        self.my_tree.column("#1", anchor= tk.CENTER, stretch= 'no', width= 175)
        self.my_tree.heading("#1", text="Name Process")
        self.my_tree.column("#2", anchor= tk.CENTER, stretch= 'no', width = 175)
        self.my_tree.heading("#2", text="ID Process")
        self.my_tree.column("#3", anchor= tk.CENTER, stretch= 'no', width = 175)
        self.my_tree.heading("#3", text="Court Thread")

        tree_scroll = ttk.Scrollbar(self, orient= "vertical")
        tree_scroll.configure(command= self.my_tree.yview)
        self.my_tree.configure(yscrollcommand= tree_scroll.set)
        

        #position
        self.my_tree.place(x = 24, y = 130)
        tree_scroll.place(x = 552, y= 130, height= 226)
        button_kill.place(x = 32, y = 24)
        button_check.place(x = 172, y= 24)
        button_del.place(x = 312, y= 24)
        button_start.place(x = 452, y = 24)
        button_back.place(x = 455, y = 365)

        self.arrayInfo = []

    

    #supportive funtions - pops up
    def get_value(self, variable, command):
        value = variable.get()
        self.variable = value
        self.comm = command


    def open_kill(self):
        top= tk.Toplevel()
        top.geometry("250x70")
        top.title("KILL")
        top.configure(bg = "bisque2")
        tk.Label(top, text="ID ",fg='#20639b',bg="bisque2",font='verdana 10 ').place(x = 27, y = 27)
        self.entry_id = tk.Entry(top,width=20,bg='light yellow')
        top.button = tk.Button(top,text="KILL", bg="#ced0f1",fg="#0b0e43", width= 6, height=1, command=lambda:  self.doCommand(self.entry_id, "PROCESS KILL")).place(x= 185, y = 27)
        self.entry_id.place(x = 57, y = 30)
        top.grab_set()



    def open_start(self):
        top= tk.Toplevel()
        top.geometry("250x70")
        top.title("START")
        top.configure(bg = "bisque2")
        tk.Label(top, text="NAME ",fg='#20639b',bg="bisque2",font='verdana 10 ').place(x = 12, y = 27)
        self.entry_id = tk.Entry(top,width=20,bg='light yellow')
        top.button = tk.Button(top,text="START", bg="#ced0f1",fg="#0b0e43", width= 6, height=1, command=lambda: self.doCommand(self.entry_id, "PROCESS START")).place(x= 185, y = 27)
        self.entry_id.place(x = 57, y = 30)
        top.grab_set()


    def delete(self):
        for i in self.my_tree.get_children():
            self.my_tree.delete(i)


    def insertText(self):
        self.delete()
        for i in range (0, len(self.arrayInfo)) :
            self.my_tree.insert("", 'end', values= (self.arrayInfo[i].ID, self.arrayInfo[i].Name, self.arrayInfo[i].thread))

    def doCommand(self, entry, command):
        id = ""
        if(entry != ""):
            id = entry.get()
        try:
            if(command != "PROCESS VIEW") :
                command = command + " " + id
            size = str(len(command))
            client.sendall(size.encode(FORMAT))
            client.sendall(command.encode(FORMAT))
            if(command == "PROCESS VIEW"):
                data = recvData()
                rows = data.split('\n')
                for row in rows:
                    cols = row.split('|')
                    self.arrayInfo.append(info(cols[0], cols[1], int(cols[2])))
                self.insertText()
            else : 
                data = recvData()
        except :
            messagebox.showinfo(message= "Server is not responding !", title= "Error!")



class registryEditor(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.configure(bg = "bisque2")

        #text box
        self.addr=tk.Text(self, font=("Georgia, 13"), width= 52, height= 1)
        self.cont=tk.Text(self, font=("Georgia, 13"), width= 52, height= 4)
        self.dir=tk.Text(self, font=("Georgia, 15"), width= 51, height= 1)
        self.nameValue=tk.Text(self, font=("Georgia, 13"), width= 18, height= 1)
        self.Value=tk.Text(self, font=("Georgia, 13"), width= 62, height= 6)
        self.middle=tk.Text(self, font=("Georgia, 13"), width= 18, height= 1)
        self.lable_notice = tk.Label(self, text = "",font= ("Georgia, 10"), bg = "bisque2")
        self.Value.config(state = tk.DISABLED)

        #button
        self.button_browse = tk.Button(self,text="Browse", bg="#ced0f1",fg="#0b0e43", width= 10, height=1,command= self.select_file)
        self.button_sendCont = tk.Button(self,text="Send content", bg="#ced0f1",fg="#0b0e43", width= 10, height=5, command= self.send_reg_file)
        self.button_send = tk.Button(self,text="Send ", bg="#ced0f1",fg="#0b0e43", width= 10, height=2, command= lambda : self.doCommand(self.opt))
        self.button_Del = tk.Button(self,text="Delete", bg="#ced0f1",fg="#0b0e43", width= 10, height=2, command= self.del_text)
        self.button_Back = tk.Button(self,text="Back", bg="#ced0f1",fg="#0b0e43", width= 10, height=2, command=lambda : controller.showFrame(startPage))
        self.lable_fixValue = tk.Label(self, text= "Edit value", bg="#ced0f1",fg="#0b0e43", font=("Georgia, 10"), padx= 100, pady= 0, anchor= 's')
        self.dir.insert('end', "Directory")


        #drop down
        self.menu= tk.StringVar()
        self.menu.set("Options")
        self.dataType = tk.StringVar()
        self.dataType.set("String")
        self.drop_valueEdit= tk.OptionMenu(self, self.menu,"Set Value", "Get Value","Delete Value","Create Key","Delete Key", command= self.display_selected)
        self.drop_dataEdit= tk.OptionMenu(self, self.dataType,"String", "Binary","DWORD","QWORD","Multi-string", "Expandable String", command = self.get_dropDownDataType)

        #position
        self.addr.place(x = 19, y = 25)
        self.cont.place(x= 19, y = 70)
        self.dir.place(x = 17, y= 230)
        self.nameValue.place(x = 19, y= 268)
        self.Value.place(x = 19, y = 300)
        self.middle.place(x = 215, y = 268)
        self.lable_notice.place(x = 350, y= 165)

        self.button_browse.place(x= 505, y= 23)
        self.button_sendCont.place(x= 505, y= 67)
        self.button_send.place(x = 100, y = 435)
        self.button_Del.place(x = 250, y = 435)
        self.button_Back.place(x = 400, y = 435)

        self.lable_fixValue.place(x = 19, y = 165)
        self.drop_valueEdit.place(x= 19, y= 194, width= 565)
        self.drop_dataEdit.place(x = 413, y = 263, width= 168)



        self.data = "String"
        self.filename = ""
        self.opt = ""

    def doCommand(self, command):
        directory = self.dir.get("1.0", "end-1c")
        nameValue = self.nameValue.get("1.0", "end-1c")
        value = self.middle.get("1.0", "end-1c")
        if(command == "") :
            self.lable_notice["text"] = "Choose an option first !"
            return
        elif(command == "Set Value") :
           package = f"REGISTRY SETVALUE {directory} {nameValue} {value} {self.data}"
        elif(command == "Get Value") :
            package = f"REGISTRY GETVALUE {directory} {nameValue}"
        elif(command== "Delete Value") :
            package = f"REGISTRY DELETEVALUE {directory} {nameValue}"
        elif(command == "Delete Key") :
            package = f"REGISTRY DELETEKEY {directory}"
        elif(command == "Create Key") :
            package = f"REGISTRY CREATEKEY {directory}"
        try:
            size = str(len(package))
            client.sendall(size.encode(FORMAT))
            client.sendall(package.encode(FORMAT))
            recieve = recvData()
            self.add_text(recieve + "\n")
        except :
            messagebox.showinfo(message= "Server is not responding !", title= "Error!")



    #supportive funtions - pops up
    def display_selected(self, choice):
        if(choice == "Get Value" or choice == "Delete Value"):
            self.middle.delete('1.0', 'end')
            self.middle.config(state = tk.DISABLED)
            self.drop_dataEdit.config(state = tk.DISABLED)
        elif(choice == "Create Key" or choice == "Delete Key"):
            self.middle.delete('1.0', 'end')
            self.nameValue.delete('1.0', 'end')
            self.middle.config(state = tk.DISABLED)
            self.drop_dataEdit.config(state = tk.DISABLED)
            self.nameValue.config(state = tk.DISABLED)
        else :
            self.middle.config(state = tk.NORMAL)
            self.drop_dataEdit.config(state = tk.NORMAL)
            self.nameValue.config(state = tk.NORMAL)
            self.middle.delete('1.0', 'end')
            self.nameValue.delete('1.0', 'end')
            self.nameValue.insert('end', "Name value")
            self.middle.insert('end', "Value")
        self.opt = choice
        self.lable_notice["text"] = ""
    

    def select_file(self):
        filetypes = (
            ('text files', '*.reg'),
            ('All files', '*.*')
        )

        self.filename = filedialog.askopenfilename(
            title='Open a file',
            initialdir='/',
            filetypes=filetypes)
        
        self.addr.delete('1.0', 'end')
        self.addr.insert('insert', self.filename)
        self.read_reg_file()


    def read_reg_file(self):
        with open(self.filename, "r", encoding= "utf-16") as reg_file:
            reg_content = reg_file.read()
        self.cont.delete('1.0', 'end')
        self.cont.insert('insert', reg_content)

    
    def add_text(self, text):
        self.Value.config(state = tk.NORMAL)
        self.Value.insert(tk.END, text)
        self.Value.config(state = tk.DISABLED)

    def del_text(self):
        self.Value.config(state = tk.NORMAL)
        self.Value.delete('1.0', 'end')
        self.Value.config(state = tk.DISABLED)

    def send_reg_file(self):
        content = self.cont.get("1.0", "end-1c")
        if(content== ""):
            self.lable_notice["text"] = "Content is empty !"
            return
        self.lable_notice["text"] = ""
        regFile = f"FILEREG {content}"
        filesize = str(len(regFile))
        try :
            client.sendall(filesize.encode())
            client.sendall(regFile.encode())
            data = recvData()
            print(1)
        except :
            tk.messagebox.showerror(title="Something is wrong ", message= "Server is not responding ! Transmission failed !")
    
    
    def get_dropDownDataType(self, choice):
        self.data = choice
        

class App(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        
        self.geometry("700x500")
        self.resizable(width=False, height=False)
        self.protocol("WM_DELETE_WINDOW", self.on_closing)

        container = tk.Frame(self)
        container.pack(side="top", fill = "both", expand = True)
        
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        for F in (startPage, processRunning, keyStroke, appRunning):
            frame = F(container, self)

            self.frames[F] = frame 

            frame.grid(row=0, column=0, sticky = "nsew")

        self.showFrame(startPage)
        self.frames[startPage].lock()


    def on_closing(self):
        if(messagebox.askokcancel("Quit", "Do you want to quit?")):
            self.destroy()
        try:
            option = "DISCONNECT SERVER"
            size = str(len(option))
            client.sendall(size.encode(FORMAT))
            client.sendall(option.encode(FORMAT))
            client.close()
        except:
            pass

    
    def showFrame(self, container):
        frame = self.frames[container]
        if container==startPage:
            self.geometry("700x500")
            self.title("Client")
        elif container == processRunning:
            self.geometry("600x400")
            self.title("Process")
        elif container == appRunning:
            self.geometry("600x400")
            self.title("List App")
        elif container == keyStroke:
            self.geometry("600x400")
            self.title("Key Stroke")
        else:
            self.geometry("500x200")
        frame.tkraise()


    def CONNECT(self,curFrame):
        try:
            ip = curFrame.entry_ip.get()

            if ip == "":
                curFrame.label_notice["text"] = "Fields cannot be empty"
                return 
            
            server_addres= (ip, PORT)
            client.connect(server_addres)
            time.sleep(1)


            option = f"CONNECT {ip}"
            size = str(len(option))
            client.sendall(size.encode(FORMAT))
            client.sendall(option.encode(FORMAT))

            # see if login is accepted
            accepted = recvData()
            if(accepted != ip):
                curFrame.label_notice["text"] = "Error: Server is not responding"
                return
            
            print("accepted: "+ accepted)

            curFrame.entry_ip.config(state = tk.DISABLED)
            curFrame.button_con.config(state = tk.DISABLED)
            curFrame.label_notice["text"] = ""
            curFrame.unLock()
            messagebox.showinfo(message= "Connect succsessfully!", title= "Success!")
        except:
            curFrame.label_notice["text"] = "Error: Server is not responding"



app = App()
app.mainloop()   