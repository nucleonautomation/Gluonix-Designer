# IMPORT LIBRARIES
import os
import sys
import time
import datetime
import _thread
from PIL import ImageGrab as PIL_ImageGrab
import tkinter as TK
from .N_Custom import Event_Bind
if os.name == 'nt':
    from ctypes import windll as DLL
else:
    from ctypes import CDLL as DLL

# GUI
class GUI():
    _Instance = None

    def __new__(Class, *args, **kwargs):
        if Class._Instance is None:
            Class._Instance = super().__new__(Class)
            return Class._Instance
        else:
            print("Gluonix -> Only One Instance Is Allowed")
            return Class._Instance

    def __init__(self, *args, **kwargs):
        if not hasattr(self, '_Initialized'):
            self._Config = ['Error_Display', 'Error_Log', 'Resize_Delay', 'Title', 'Icon', 'Background', 'Light_Background', 'Dark_Background', 'Persistent', 'Resizable', 'Full_Screen', 'Toolbar', 'Menu_Enable', 'Width', 'Height', 'Left', 'Top', 'Alignment']
            self._Config_Get = ['Error_Display', 'Error_Log', 'Resize_Delay', 'Title', 'Icon', 'Background', 'Light_Background', 'Dark_Background', 'Persistent', 'Resizable', 'Full_Screen', 'Toolbar', 'Menu_Enable', 'Width', 'Height', 'Left', 'Top', 'Alignment', 'Full_Screen', 'Screen_Width', 'Screen_Height']
            self._Initialized = False
            self._Error_Display = False
            self._Error_Log = False
            self._Log_Folder = './Log'
            self._Log_File = 'Gluonix_Error.log'
            self._Error = []
            self._Widget = []
            self._Type = "GUI"
            self._Frame = TK.Tk()
            self._Resize_Timer = False
            self._Resize_Delay = 200
            self._Title = "Nucleon Gluonix"
            self._Icon = ""
            self._Background = "#F0F0F0"
            self._Alignment = 'Pixel'
            self._Persistent = False
            self._Toolbar = True
            self._Full_Screen = False
            self._Resizable = True
            self._Border_Size = 0
            self._Menu_Enable = False
            self._On_Close = False
            self._On_Resize = False
            self._Restore_Width = False
            self._Restore_Height = False
            self._On_Show = False
            self._On_Hide = False
            self._Window = False
            if os.name == 'nt':
                self._Window = True
                    
    def __str__(self):
        return "Nucleon_Glunoix["+self._Title+"]"

    def __repr__(self):
        return "Nucleon_Glunoix["+self._Title+"]"

    def Error(self, E):
        Error_Time = int(time.time())
        self._Error.append([E, Error_Time])
        if self._Error_Display:
            print(E)
        if self._Error_Log:
            if not os.path.exists(self._Log_Folder):
                os.makedirs(self._Log_Folder)
            Log_Path = os.path.join(self._Log_Folder, self._Log_File)
            Date = datetime.datetime.fromtimestamp(Error_Time)
            Date = Date.strftime('%Y-%m-%d %H:%M:%S')
            Line = f"{Date} - {E}"
            File_Content = []
            if os.path.exists(Log_Path):
                with open(Log_Path, 'r') as File:
                    File_Content = File.readlines()
                if len(File_Content) >= 10000:
                    File_Content.pop()
            with open(Log_Path, 'w') as File:
                File.write(Line.rstrip('\r\n') + '\n')
                File.writelines(File_Content)
                
    def Nothing(self):
        return False
        
    def Maximize(self):
        try:
            self._Restore_Width = self._Width_Current
            self._Restore_Height = self._Height_Current
            if not self._Toolbar:
                if self._Window:
                    hwnd = DLL.user32.GetParent(self._Frame.winfo_id())
                    SWP_SHOWWINDOW = 0x40
                    DLL.user32.SetWindowPos(hwnd, 0, 0, 0, int(self._Frame.winfo_screenwidth()), int(self._Frame.winfo_screenheight()-48), SWP_SHOWWINDOW)
            else:
                self._Frame.state('zoomed')
        except Exception as E:
            self.Error(f"{self._Type} -> Maximize -> {E}")
        
    def Restore(self):
        try:
            if self._Restore_Width and self._Restore_Height:
                self._Width_Current = self._Restore_Width
                self._Height_Current = self._Restore_Height
            if not self._Toolbar:
                if self._Window:
                    hwnd = DLL.user32.GetParent(self._Frame.winfo_id())
                    SWP_SHOWWINDOW = 0x40
                    DLL.user32.SetWindowPos(hwnd, 0, int(self._Left_Current), int(self._Top_Current), int(self._Width_Current), int(self._Height_Current), SWP_SHOWWINDOW)
            else:
                self._Frame.geometry(f"{int(self._Width_Current)}x{int(self._Height_Current)}+{int(self._Left_Current)}+{int(self._Top_Current)}")
            self._Frame.event_generate("<Configure>")
        except Exception as E:
            self.Error(f"{self._Type} -> Restore -> {E}")
        
    def Minimize(self, Hide=False):
        try:
            if not self._Toolbar:
                if self._Window:
                    hwnd = DLL.user32.GetParent(self._Frame.winfo_id())
                    DLL.user32.ShowWindow(hwnd, 0 if Hide else 6)
            else:
                self._Frame.iconify()
        except Exception as E:
            self.Error(f"{self._Type} -> Minimize -> {E}")
            
    def Restart(self):
        try:
            self.Close()
            os.execl(sys.executable, sys.executable, *sys.argv)
        except Exception as E:
            self.Error(f"{self._Type} -> Restart -> {E}")

    def Close(self):
        try:
            self._Frame.destroy()
        except Exception as E:
            self.Error(f"{self._Type} -> Close -> {E}")
            
    def On_Close(self):
        try:
            if self._On_Close:
                self._On_Close()
            self.Close()
        except Exception as E:
            self.Error(f"{self._Type} -> On_Close -> {E}")
            
    def Hide(self):
        try:
            self._Frame.withdraw()
            if self._On_Hide:
                self._On_Hide()
        except Exception as E:
            self.Error(f"{self._Type} -> Hide -> {E}")
            
    def Show(self):
        try:
            self._Frame.deiconify()
            if self._On_Show:
                self._On_Show()
        except Exception as E:
            self.Error(f"{self._Type} -> Show -> {E}")
    
    def Grab(self, Path=False):
        try:
            return self.Grab_Widget(Path=Path)
        except Exception as E:
            self.Error(f"{self._Type} -> Grab -> {E}")

    def Start(self):
        try:
            if not self._Toolbar:
                if self._Window:
                    GWL_EXSTYLE=-20
                    WS_EX_APPWINDOW=0x00040000
                    WS_EX_TOOLWINDOW=0x00000080
                    hwnd = DLL.user32.GetParent(self._Frame.winfo_id())
                    style = DLL.user32.GetWindowLongW(hwnd, GWL_EXSTYLE)
                    style = style & ~WS_EX_TOOLWINDOW
                    style = style | WS_EX_APPWINDOW
                    res = DLL.user32.SetWindowLongW(hwnd, GWL_EXSTYLE, style)
                    self._Frame.withdraw()
                    self._Frame.wm_deiconify()
            self._Frame.mainloop()
        except Exception as E:
            self.Error(f"{self._Type} -> Start -> {E}")
            
    def Event(self, E=None):
        try:
            Widget = str(E.widget)
            Frame = str(self._Frame)
            if Widget==Frame:
                Width = E.width
                Height = E.height
                Left = E.x
                Top = E.y
                self._Left = Left
                self._Top = Top
                if (Width!=self._Width_Current) or (Height!=self._Height_Current):
                    self._Width_Current = Width
                    self._Height_Current = Height
                    if self._Resize_Timer:
                        self._Frame.after_cancel(self._Resize_Timer)
                    self._Resize_Timer = self._Frame.after(self._Resize_Delay, self.Event_Runner)
        except Exception as E:
            self.Error(f"{self._Type} -> Event -> {E}")
            
    def Event_Runner(self):
        try:
            for Each in self._Widget:
                try:
                    if Each._Display:
                        Each.Resize()
                except Exception:
                    self.Nothing = False
            if self._On_Resize:
                self._On_Resize()
        except Exception as E:
            self.Error(f"{self._Type} -> Event_Runner -> {E}")
            
    def After(self, Delay, Function):
        try:
            self._Frame.after(Delay, Function)
        except Exception as E:
            self.Error(f"{self._Type} -> After -> {E}")
            
    def Screen(self):
        try:
            return {'Width': self._Screen_Width, 'Height': self._Screen_Height}
        except Exception as E:
            self.Error(f"{self._Type} -> Screen -> {E}")
            
    def Full_Screen(self, Toggle):
        try:
            if not self._Full_Screen:
                self._Frame.overrideredirect(False)
                self._Frame.attributes('-fullscreen', Toggle)
                if self._Toolbar:
                    self._Frame.overrideredirect(False)
                else:
                    self._Frame.overrideredirect(True)
        except Exception as E:
            self.Error(f"{self._Type} -> Full_Screen -> {E}")
            
    def Widget(self):
        try:
            return self._Frame
        except Exception as E:
            self.Error(f"{self._Type} -> Widget -> {E}")
            
    def Bind(self, **Input):
        try:
            if 'On_Show' in Input:
                self._On_Show = Input['On_Show']
            if 'On_Hide' in Input:
                self._On_Hide = Input['On_Hide']
            if "On_Resize" in Input:
                self._On_Resize = Input["On_Resize"]
            if 'On_Close' in Input:
                self._On_Close = Input['On_Close']
            Event_Bind(self._Frame, **Input)
        except Exception as E:
            self.Error(f"{self._Type} -> Bind -> {E}")

    def Config_Get(self, *Input):
        try:
            Return = {}
            for Each in self._Config_Get:
                if Each in Input:
                    Return[Each] = getattr(self, "_"+Each)
            return Return
        except Exception as E:
            self.Error(f"{self._Type} -> Config_Get -> {E}")

    def Config(self, **Input):
        try:
            Run = False
            for Each in self._Config:
                if Each in Input:
                    Value = Input[Each]
                    setattr(self, "_"+Each, Value)
                    Run = True
            if self._Initialized and Run:
                self.Create()
        except Exception as E:
            self.Error(f"{self._Type} -> Config -> {E}")
            
    def Add_Menu(self, Main=False, Name=False, Command=False):
        try:
            if not self._Menu_Enable:
                self._Menu_Enable = True
                self._Menu = TK.Menu(self._Frame)
                self._Frame.config(menu=self._Menu)
            if Command:
                self._Menu.add_command(label=Name, command=Command)
            else:
                if not Main:
                    Main = self._Menu
                Menu = TK.Menu(Main, tearoff=False)
                Main.add_cascade(label=Name, menu=Menu)
                return Menu
        except Exception as E:
            self.Error(f"{self._Type} -> Add_Menu -> {E}")
            
    def Add_Sub_Menu(self, Main, Name, Command=False):
        try:
            if not Command:
                Command = self.Nothing
            Main.add_command(label=Name, command=Command)
        except Exception as E:
            self.Error(f"{self._Type} -> Add_Sub_Menu -> {E}")
            
    def Add_Separator(self, Main):
        try:
            Main.add_separator()
        except Exception as E:
            self.Error(f"{self._Type} -> Add_Separator -> {E}")
            
    def Folder(self, Initial='', Title='', Persistent=True):
        try:
            return TK.filedialog.askdirectory(initialdir=Initial, title=Title, mustexist=Persistent, parent=self._Frame)
        except Exception as E:
            self.Error(f"{self._Type} -> Folder -> {E}")
            
    def File(self, Initial='', Title='', Multiple=False, Default='.txt', Type=[["Text files", "*.txt"], ["All files", "*.*"]]):
        try:
            return TK.filedialog.askopenfilename(initialdir=Initial, title=Title, multiple=Multiple, parent=self._Frame, defaultextension=Default, filetypes=Type)
        except Exception as E:
            self.Error(f"{self._Type} -> File -> {E}")
    
    def Grab_Widget(self, Path=False, Widget=False, Custom=False):
        try:
            if Widget:
                X = self._Frame.winfo_rootx() + Widget._Frame.winfo_x()
                Y = self._Frame.winfo_rooty() + Widget._Frame.winfo_y()
                Width = X + Widget._Frame.winfo_width()
                Height = Y + Widget._Frame.winfo_height()
            elif Custom:
                X = Custom[0]
                Y = Custom[1]
                Width = Custom[2]
                Height = Custom[3]
            else:
                X = self._Frame.winfo_rootx()
                Y = self._Frame.winfo_rooty()
                Width = X + self._Frame.winfo_width()
                Height = Y + self._Frame.winfo_height()
            Temp_Image = PIL_ImageGrab.grab(bbox=(X, Y, Width, Height))
            if Path:
                Temp_Image.save(Path)
            return Temp_Image
        except Exception as E:
            self.Error(f"{self._Type} -> Grab_Widget -> {E}")
            
    def Position(self):
        try:
            Left = self._Frame.winfo_x()
            Top = self._Frame.winfo_y()
            return [Left, Top]
        except Exception as E:
            self.Error(f"{self._Type} -> Position -> {E}")
            
    def Size(self):
        try:
            return [self._Frame.winfo_width(), self._Frame.winfo_height()]
        except Exception as E:
            self.Error(f"{self._Type} -> Size -> {E}")
        
    def Locate(self, Width, Height, Left, Top):
        try:
            Width = self._Width*(Width/100)
            Height = self._Height*(Height/100)
            Left = self._Width*(Left/100)
            Top = self._Height*(Top/100)
            return [Width, Height, Left, Top]
        except Exception as E:
            self.Error(f"{self._Type} -> Locate -> {E}")
        
    def Locate_Reverse(self, Width, Height, Left, Top):
        try:
            Width = round((Width/self._Width)*100, 3)
            Height = round((Height/self._Height)*100, 3)
            Left =  round((Left/self._Width)*100, 3)
            Top =  round((Top/self._Height)*100, 3)
            return [Width, Height, Left, Top]
        except Exception as E:
            self.Error(f"{self._Type} -> Locate_Reverse -> {E}")
        
    def Locate_Fullscreen(self, Width, Height, Left, Top):
        try:
            Width = self._Screen_Width*(Width/100)
            Height = self._Screen_Height*(Height/100)
            Left = self._Screen_Width*(Left/100)
            Top = self._Screen_Height*(Top/100)
            return [Width, Height, Left, Top]
        except Exception as E:
            self.Error(f"{self._Type} -> Locate_Fullscreen -> {E}")

    def Create(self):
        try:
            if not self._Initialized:
                self.Initiate_Colors(self)
                self._Screen_Width = self._Frame.winfo_screenwidth()
                self._Screen_Height = self._Frame.winfo_screenheight()
                if self._Full_Screen:
                    self._Height = self._Frame.winfo_screenheight()
                    self._Width = self._Frame.winfo_screenwidth()
                    self._Left = 0
                    self._Top = 0
                    self._Frame.attributes('-fullscreen',True)
                    self._Frame.overrideredirect(True)
                else:
                    self._Frame.bind("<Configure>", self.Event)
                    if self._Alignment == 'Percentage':
                        self._Width = int(self._Frame.winfo_screenwidth() * (self._Width/100))
                        self._Height = int(self._Frame.winfo_screenheight() * (self._Height/100))
                        self._Left = int(self._Frame.winfo_screenwidth() * (self._Left/100))
                        self._Top = int(self._Frame.winfo_screenheight() * (self._Top/100))
                    self._Frame.geometry(f"{int(self._Width)}x{int(self._Height)}+{int(self._Left)}+{int(self._Top)}")
                    self._Frame.resizable(self._Resizable, self._Resizable)
                    self._Frame.attributes('-fullscreen', False)
                    if self._Toolbar:
                        self._Frame.overrideredirect(False)
                    else:
                        self._Frame.overrideredirect(True)
                self._Width_Current, self._Height_Current, self._Left_Current, self._Top_Current = self._Width, self._Height, self._Left, self._Top
                if self._Menu_Enable:
                    self._Menu = TK.Menu(self._Frame)
                    self._Frame.config(menu=self._Menu)
                self._Initialized = True
            if not self._Full_Screen and not self._Toolbar:
                self._Frame.geometry(f"{int(self._Width)}x{int(self._Height)}+{int(self._Left)}+{int(self._Top)}")
            self._Frame.config(bg=self._Background)
            if not hasattr(self, "_Light_Background"):
                setattr(self, "_Light_Background", self._Background)
            if not hasattr(self, "_Dark_Background"):
                setattr(self, "_Dark_Background", self.Invert(self._Background))
            if self._Title:
                self._Frame.title(self._Title)
            else:
                self._Frame.title('Nucleon Glunoix')
            if os.path.exists(self._Icon) and self._Window:
                self._Frame.iconbitmap(self._Icon)
            if self._Persistent:
                self._Frame.protocol("WM_DELETE_WINDOW", self.Nothing)
            else:
                self._Frame.protocol("WM_DELETE_WINDOW", self.On_Close)
        except Exception as E:
            self.Error(f"{self._Type} -> Create -> {E}")
            
    def Invert(self, Hex):
        try:
            if Hex:
                Html_To_Hex = {
                    "black": "#000000",
                    "white": "#FFFFFF",
                    "red": "#FF0000",
                    "green": "#008000",
                    "blue": "#0000FF",
                    "yellow": "#FFFF00",
                    "cyan": "#00FFFF",
                    "magenta": "#FF00FF",
                    "gray": "#808080",
                    "grey": "#808080",
                    "orange": "#FFA500",
                    "purple": "#800080",
                    "pink": "#FFC0CB",
                    "brown": "#A52A2A",
                    "lime": "#00FF00",
                    "navy": "#000080",
                    "teal": "#008080",
                    "maroon": "#800000",
                    "olive": "#808000",
                    "silver": "#C0C0C0"
                }
                if isinstance(Hex, str) and not Hex.startswith("#"):
                    Hex = Html_To_Hex.get(Hex.lower(), Hex)
                Hex = Hex.lstrip("#")
                R = 255 - int(Hex[0:2], 16)
                G = 255 - int(Hex[2:4], 16)
                B = 255 - int(Hex[4:6], 16)
                return f"#{R:02X}{G:02X}{B:02X}"
            else:
                return Hex
        except Exception as E:
            self.Error(f"{self._Type} -> Invert -> {E}")
            
    def Initiate_Colors(self, Widget):
        try:
            Variable_Names = ["_Background", "_Foreground", "_Border_Color", "_Shadow_Color", "_Hover_Background", "_Hover_Foreground", "_Hover_Border_Color", "_Hover_Shadow_Color"]
            for Name in Variable_Names:
                if hasattr(Widget, Name):
                    Value = getattr(Widget, Name)
                    if Value:
                        Light_Name = "_Light" + Name
                        Dark_Name = "_Dark" + Name
                        if not hasattr(Widget, Light_Name):
                            setattr(Widget, Light_Name, Value)
                        if not hasattr(Widget, Dark_Name):
                            setattr(Widget, Dark_Name, self.Invert(Value))
        except Exception as E:
            self.Error(f"{self._Type} -> Initiate_Colors -> {E}")
            
    def Apply_Mode(self, Widget, Mode='Light'):
        try:
            Variable_Names = ["Background", "Foreground", "Border_Color", "Shadow_Color", "Hover_Background", "Hover_Foreground", "Hover_Border_Color", "Hover_Shadow_Color"]
            Last_Variable_Names = ["Background", "Foreground", "Border_Color", "Shadow_Color"]
            Config_Dict = {}
            for Name in Variable_Names:
                    Mode_Name = f"_{Mode}_{Name}" 
                    if hasattr(Widget, Mode_Name):
                        Value = getattr(Widget, Mode_Name)
                        if Value:
                            Config_Dict[Name] = Value
                            if Name in Last_Variable_Names:
                                Last_Name = f"_Last_{Name}"
                                setattr(Widget, Last_Name, Value)
            if Config_Dict:
                Widget.Config(**Config_Dict)
            if hasattr(Widget, "_Widget"):
                if isinstance(Widget._Widget, (list, tuple)):
                    for Child in Widget._Widget:
                        self.Apply_Mode(Child, Mode)
        except Exception as E:
            self.Error(f"{self._Type} -> Apply_Mode -> {E}")
            
    def Light_Mode(self):
        try:
            self.Apply_Mode(self, 'Light')
        except Exception as E:
            self.Error(f"{self._Type} -> Light_Mode -> {E}")

    def Dark_Mode(self):
        try:
            self.Apply_Mode(self, 'Dark')
        except Exception as E:
            self.Error(f"{self._Type} -> Dark_Mode -> {E}")
            
    def Update_Colors(self, Widget):
        try:
            Variable_Names = ["_Background", "_Foreground", "_Border_Color", "_Shadow_Color", "_Hover_Background", "_Hover_Foreground", "_Hover_Border_Color", "_Hover_Shadow_Color"]
            for Name in Variable_Names:
                if hasattr(Widget, Name):
                    Value = getattr(Widget, Name)
                    Light_Name = "_Light" + Name
                    Dark_Name = "_Dark" + Name
                    setattr(Widget, Light_Name, Value)
                    setattr(Widget, Dark_Name, self.Invert(Value))
            if hasattr(Widget, "_Widget"):
                if isinstance(Widget._Widget, (list, tuple)):
                    for Child in Widget._Widget:
                        self.Update_Colors(Child)
        except Exception as E:
            self.Error(f"{self._Type} -> Update_Colors -> {E}")
            
    def Update_Color(self):
        try:
            self.Update_Colors(self)
        except Exception as E:
            self.Error(f"{self._Type} -> Update_Color -> {E}")