import socket
import os
import io #trans int and byte
import psutil #app process
import subprocess #app
import zlib #compress
from PIL import ImageGrab #screenshot
import keyboard #KEYSTROKE
import winreg #registry
import ctypes

HOST = "127.0.0.1"
PORT = 65432
key = ""
def system(command):
    if command == "SHUTDOWN":
        os.system("shutdown /s /t 1")  # Tắt máy sau 1 giây
    elif command == "RESTART":
        os.system("restart /r /t 1")  # Khởi động lại máy sau 1 giây
    elif command == "SLEEP":
        os.system("rundll32.exe powrprof.dll,SetSuspendState 0,1,0") # Sleep sau 1 giây
        
def view_process():
    processList = []
    for process in psutil.process_iter(attrs=['pid', 'name', 'num_threads']):
        name = process.info['name']
        pid = process.info['pid']
        num_thread = process.info['num_threads']
        processList.append(f"{name}|{pid}|{num_thread}")
    return '\n'.join(processList)
def kill_process(pid):
    process = psutil.Process(pid)
    process.kill()
    
def terminate_process(pid):
    process = psutil.Process(pid)
    process.terminate()
        
def isIDProcessRunning(pid):
    try:
        process = psutil.Process(pid)
        return process.is_running()
    except psutil.NoSuchProcess:
        return False
    
def process(command):
    mode = command.split()
    result = "1"
    if mode[0] == "START":
        check = os.system(f"start {mode[1]}.exe")
        if check != 0:
            result = "0"
    elif mode[0] == "VIEW":
        result = view_process()
    elif mode[0] == "KILL":
        ID = int(mode[1])
        if isIDProcessRunning(ID) == True:
            kill_process(ID)
        else: result = "0" 
    elif mode[0] == "TERMINATE":
        ID = int(mode[1])
        if isIDProcessRunning(ID) == True:
            terminate_process(ID)
        else: result = "0"
    return result


def killApp(pid):
    app = psutil.Process(pid)
    appProcessName = app.name()
    for process in psutil.process_iter(attrs=['pid', 'name']):
        if process.info['name'] == appProcessName:
            try:
                processDeleted = psutil.Process(process.info['pid'])
                processDeleted.kill()
            except psutil.NoSuchProcess:
                return "0"
    return "1"
def viewListApps():
    appList = []
    cmd = 'powershell "gps | where {$_.MainWindowTitle } | select ProcessName,Id"'
    proc = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
    for line in proc.stdout:
        parts = line.decode().split()
        if len(parts) >= 2 and parts[1].isdigit():
            processName = parts[0]
            processId = int(parts[1])
            process = psutil.Process(processId)
            numThreads = process.num_threads()
            appList.append(f"{processName}|{processId}|{numThreads}")
    return '\n'.join(appList)
def app(command):
    mode = command.split()
    result = "1"
    if mode[0] == "START":
        check = os.system(f"start {mode[1]}.exe")
        if check != 0:
            result = "0"
    if mode[0] == "VIEW":
        result = viewListApps()
    if mode[0] == "KILL":
        ID = int(mode[1])
        if isIDProcessRunning(ID) == True:
            killApp(ID)
        else: result = "0" 
    return result

def sendScreenshot(conn):
    screenshot = ImageGrab.grab()
    imageData = io.BytesIO()
    screenshot.save(imageData, format='PNG')
    screenshotBytes = imageData.getvalue()
    compressedScreenshot = zlib.compress(screenshotBytes)
    size = len(compressedScreenshot)
    sizeData = size.to_bytes(4, 'big') 
    conn.send(sizeData)
    conn.sendall(compressedScreenshot)

def callback(event):
    global key
    key += event.name

def keystroke(command):
    result = ""
    global key
    if command == "HOOK":
        key = ""
        keyboard.on_press(callback)
    elif command == "UNHOOK":
        key = ""
        keyboard.unhook_all()
    elif command == "VIEW":
        keyboard.unhook_all()
        if key == "":
            key = ""
        result = key
        key = ""
    elif command == "QUIT":
        key = ""
        keyboard.unhook_all()
    return result
def getValueRegistry(hkeyWinreg, keyPath, valueName):
    try:
        key = winreg.OpenKey(hkeyWinreg, keyPath)
        try:
            value, type = winreg.QueryValueEx(key, valueName)
            return value                
        except Exception:
            return "Not value"
        finally: winreg.CloseKey(key)
    except Exception:
        return "Key not found"
def setValueRegistry(hkeyWinreg, keyPath, valueName, value, type):
    try:
        key = winreg.OpenKey(hkeyWinreg, keyPath, 0, winreg.KEY_SET_VALUE)
        try:
            typeMapping = {
                "string": winreg.REG_SZ,
                "binary": winreg.REG_BINARY,
                "dword": winreg.REG_DWORD,
                "qword": winreg.REG_QWORD,
                "multiString": winreg.REG_MULTI_SZ,
                "expandString": winreg.REG_EXPAND_SZ
            }
            if type not in typeMapping:
                return "Type Error"
            regType = typeMapping[type]
            if type == "string":
                value = str(value)
            elif type == "binary":
                if not isinstance(value, bytes):
                    return "Binary value must be bytes"
            elif type == "dword" or type == "qword":
                if not isinstance(value, int):
                    return f"{type.upper()} value must be an integer"
            winreg.SetValueEx(key, valueName, 0, regType, value)
            return "Set value success"                
        except Exception:
            return "Not value"
        finally: winreg.CloseKey(key)
    except Exception:
        return "Key not found"
def deleteValueRegistry(hkeyWinreg, keyPath, valueName):
    try:
        key = winreg.OpenKey(hkeyWinreg, keyPath, 0, winreg.KEY_SET_VALUE)
        try:
            winreg.DeleteValue(key, valueName)
            return "Delete value success"                
        except Exception:
            return "Not value"
        finally: winreg.CloseKey(key)
    except Exception:
        return "Key not found"
def deleteKeyRegistry(hkeyWinreg, keyPath):
    try:
        winreg.DeleteKey(hkeyWinreg, keyPath)
        return "Delete key success"
    except Exception:
        return "Key not found"
def createKeyRegistry(hkeyWinreg, keyPath):
    try:
        winreg.CreateKey(hkeyWinreg, keyPath)
        return "Create key success"
    except Exception:
        return "Key not found"
def isAdmin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False
def executeRegFile(regFilePath):
    try:
        subprocess.run(["regedit.exe", "/s", regFilePath], check=True)
        return "1"
    except subprocess.CalledProcessError:
        return "0"
def fileRegistry(content):
    try:
        with open("received_file.reg", "w") as regFile:
            regFile.write(content)
        regFilePath = os.path.abspath("received_file.reg")
        if isAdmin():
            return executeRegFile(regFilePath)
        else:
            ctypes.windll.shell32.ShellExecuteW(None, "runas", "python", __file__, None, 1)
    except Exception:
        return "0"
    finally:
        if os.path.exists(regFilePath):
            os.remove(regFilePath)
def registry(command):
    mode, command = command.split(maxsplit=1)
    result = "1"
    if mode == "FILEREG":
        result = fileRegistry(command)
        return result
    check = command.split("\\")
    if len(check) == 1:
        return "Error path"
    hkey, command = command.split("\\", maxsplit=1)
    hkeyMapping = {
        "HKEY_CLASSES_ROOT": winreg.HKEY_CLASSES_ROOT,
        "HKEY_CURRENT_USER": winreg.HKEY_CURRENT_USER,
        "HKEY_LOCAL_MACHINE": winreg.HKEY_LOCAL_MACHINE,
        "HKEY_USERS": winreg.HKEY_USERS,
        "HKEY_CURRENT_CONFIG": winreg.HKEY_CURRENT_CONFIG
    }
    if hkey not in hkeyMapping:
        return "NOT exist Hkey"
    hkeyWinreg = hkeyMapping[hkey]
    if mode == "GETVALUE":
        keyPath, valueName = command.split()
        result = getValueRegistry(hkeyWinreg, keyPath, valueName)
    if mode == "SETVALUE":
        keyPath, valueName, value, type = command.split()
        result = setValueRegistry(hkeyWinreg, keyPath, valueName, value, type)
    if mode == "DELETEVALUE":
        keyPath, valueName = command.split()
        result = deleteValueRegistry(hkeyWinreg, keyPath, valueName)
    if mode == "DELETEKEY":
        result = deleteKeyRegistry(hkeyWinreg, command)
    if mode == "CREATEKEY":
        result = createKeyRegistry(hkeyWinreg, command)    
    return result
def handleData(data, conn):
    mode, command = data.split(maxsplit=1)
    result = "1"
    if mode == "SYSTEM":
        system(command)
        result = "1"
    elif mode == "PROCESS":
        result = process(command)
    elif mode == "APP":
        result = app(command)
    elif mode == "SCREEN":
        sendScreenshot(conn)
        return     
    elif mode == "KEYSTROKE":
        result = keystroke(command)
    elif mode == "REGISTRY":
        result = registry(command)
    elif mode == "CONNECT" and (command == HOST or command == "127.0.0.1"):
        result = command
    elif mode == "DISCONNECT" :
        conn.close()
        return 0
    size = str(len(result))

    conn.sendall(size.encode("utf-8"))
    conn.sendall(result.encode("utf-8"))
def recvData(conn):
    sizeData = conn.recv(1024).decode("utf-8")
    size = int(sizeData)

    data = b''
    while len(data) < size:
        tmp = conn.recv(1024)
        if not tmp:
            break
        data += tmp
    return data.decode()
def main():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((HOST, PORT))
    s.listen(1)
    try:
        conn = None
        while True:
            print("Waiting connection")
            conn, addr = s.accept()
            print("Connected by ", addr)
            try:
                while True:
                    data = recvData(conn)
                    if len(data) > 0:
                        handleData(data,conn)
            except Exception:
                pass
    except KeyboardInterrupt:
        if conn:
            conn.close()
        s.close()
    finally:
        if conn:
            conn.close()
        s.close()



if __name__ == '__main__':
    main()