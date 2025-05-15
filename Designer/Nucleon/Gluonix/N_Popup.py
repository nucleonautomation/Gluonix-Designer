# IMPORT LIBRARIES
import os
from PIL import ImageGrab as PIL_ImageGrab
import tkinter as TK
from .N_GUI import GUI
from .N_Custom import Event_Bind
if os.name == 'nt':
    from ctypes import windll as DLL
else:
    from ctypes import CDLL as DLL

# GUI
class Popup():

    def __init__(self, Main=False, **kwargs):
        self._GUI = GUI._Instance
        if self._GUI is not None:
            self._Type = "Popup"
            try:
                self._Config = ['Error_Display', 'Resize_Delay', 'Title', 'Icon', 'Background', 'Light_Background', 'Dark_Background', 'Topmost', 'Persistent', 'Resizable', 'Full_Screen', 'Toolbar', 'Menu_Enable', 'Width', 'Height', 'Left', 'Top', 'Alignment', 'Minimize']
                self._Config_Get = ['Error_Display', 'Resize_Delay', 'Title', 'Icon', 'Background', 'Light_Background', 'Dark_Background', 'Topmost','Persistent', 'Resizable', 'Full_Screen', 'Toolbar', 'Menu_Enable', 'Width', 'Height', 'Left', 'Top', 'Alignment', 'Full_Screen', 'Screen_Width', 'Screen_Height', 'Minimize']
                self._Initialized = False
                self._Error_Display = True
                self._Error = []
                self._Widget = []
                self._Name = False
                self._Main = Main
                if self._Main:
                    self._Frame = TK.Toplevel(self._Main._Frame)
                else:
                    self._Frame = TK.Toplevel(None)
                self._Resize_Timer = False
                self._Resize_Delay = 200
                self._Title = "Nucleon Gluonix"
                self._Icon = ""
                self._Background = "#F0F0F0"
                self._Alignment = 'Pixel'
                self._Topmost = False
                self._Persistent = False
                self._Toolbar = True
                self._Full_Screen = False
                self._Resizable = True
                self._Border_Size = 0
                self._Minimize = False
                self._Restricted = False
                self._Menu_Enable = False
                self._On_Resize = False
                self._Restore_Width = False
                self._Restore_Height = False
                self._Window = self._GUI._Window
                self._On_Show = False
                self._On_Hide = False
            except Exception as E:
                self._GUI.Error(f"{self._Type} -> Init -> {E}")
        else:
            print("Error: Gluonix -> GUI Instance Has Not Been Created")

    def __str__(self):
        return "Nucleon_Glunoix_Popup["+self._Title+"]"

    def __repr__(self):
        return "Nucleon_Glunoix_Popup["+self._Title+"]"

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
            self._GUI.Error(f"{self._Type} -> Maximize -> {E}")
        
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
            self._GUI.Error(f"{self._Type} -> Restore -> {E}")
        
    def Minimize(self, Hide=False):
        try:
            if not self._Toolbar:
                if self._Window:
                    hwnd = DLL.user32.GetParent(self._Frame.winfo_id())
                    DLL.user32.ShowWindow(hwnd, 0 if Hide else 6)
            else:
                self._Frame.iconify()
        except Exception as E:
            self._GUI.Error(f"{self._Type} -> Minimize -> {E}")

    def Close(self):
        try:
            if not self._Restricted:
                self._Frame.destroy()
        except Exception as E:
            self._GUI.Error(f"{self._Type} -> Close -> {E}")
            
    def On_Close(self):
        try:
            if self._On_Close:
                self._On_Close()
            self._Frame.destroy()
        except Exception as E:
            self._GUI.Error(f"{self._Type} -> On_Close -> {E}")
            
    def Hide(self):
        try:
            self._Frame.withdraw()
            if self._On_Hide:
                self._On_Hide()
        except Exception as E:
            self._GUI.Error(f"{self._Type} -> Hide -> {E}")
            
    def Show(self):
        try:
            self._Frame.deiconify()
            if self._On_Show:
                self._On_Show()
        except Exception as E:
            self._GUI.Error(f"{self._Type} -> Show -> {E}")
    
    def Grab(self, Path=False):
        try:
            return self.Grab_Widget(Path=Path)
        except Exception as E:
            self._GUI.Error(f"{self._Type} -> Grab -> {E}")
            
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
            self._GUI.Error(f"{self._Type} -> Event -> {E}")
            
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
            self._GUI.Error(f"{self._Type} -> Event_Runner -> {E}")
            
    def After(self, Delay, Function):
        try:
            self._Frame.after(Delay, Function)
        except Exception as E:
            self._GUI.Error(f"{self._Type} -> After -> {E}")
            
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
            self._GUI.Error(f"{self._Type} -> Full_Screen -> {E}")

    def Config_Get(self, *Input):
        try:
            Return = {}
            for Each in self._Config_Get:
                if Each in Input:
                    Return[Each] = getattr(self, "_"+Each)
            return Return
        except Exception as E:
            self._GUI.Error(f"{self._Type} -> Config_Get -> {E}")
            
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
            self._GUI.Error(f"{self._Type} -> Add_Menu -> {E}")
            
    def Add_Sub_Menu(self, Main, Name, Command=False):
        try:
            if not Command:
                Command = self.Nothing
            Main.add_command(label=Name, command=Command)
        except Exception as E:
            self._GUI.Error(f"{self._Type} -> Add_Sub_Menu -> {E}")
            
    def Add_Separator(self, Main):
        try:
            Main.add_separator()
        except Exception as E:
            self._GUI.Error(f"{self._Type} -> Add_Separator -> {E}")
            
    def Widget(self):
        try:
            return self._Frame
        except Exception as E:
            self._GUI.Error(f"{self._Type} -> Widget -> {E}")
            
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
            self._GUI.Error(f"{self._Type} -> Bind -> {E}")

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
            self._GUI.Error(f"{self._Type} -> Config -> {E}")
            
    def Folder(self, Initial='', Title='', Persistent=True):
        try:
            return TK.filedialog.askdirectory(initialdir=Initial, title=Title, mustexist=Persistent, parent=self._Frame)
        except Exception as E:
            self._GUI.Error(f"{self._Type} -> Folder -> {E}")
            
    def File(self, Initial='', Title='', Multiple=False, Default='.txt', Type=[["Text files", "*.txt"], ["All files", "*.*"]]):
        try:
            return TK.filedialog.askopenfilename(initialdir=Initial, title=Title, multiple=Multiple, parent=self._Frame, defaultextension=Default, filetypes=Type)
        except Exception as E:
            self._GUI.Error(f"{self._Type} -> File -> {E}")
    
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
            self._GUI.Error(f"{self._Type} -> Grab_Widget -> {E}")
            
    def Position(self):
        try:
            Left = self._Frame.winfo_x()
            Top = self._Frame.winfo_y()
            return [Left, Top]
        except Exception as E:
            self._GUI.Error(f"{self._Type} -> Position -> {E}")
            
    def Size(self):
        try:
            return [self._Frame.winfo_width(), self._Frame.winfo_height()]
        except Exception as E:
            self._GUI.Error(f"{self._Type} -> Size -> {E}")
        
    def Locate(self, Width, Height, Left, Top):
        try:
            Width = self._Width*(Width/100)
            Height = self._Height*(Height/100)
            Left = self._Width*(Left/100)
            Top = self._Height*(Top/100)
            return [Width, Height, Left, Top]
        except Exception as E:
            self._GUI.Error(f"{self._Type} -> Locate -> {E}")
        
    def Locate_Reverse(self, Width, Height, Left, Top):
        try:
            Width = round((Width/self._Width)*100, 3)
            Height = round((Height/self._Height)*100, 3)
            Left =  round((Left/self._Width)*100, 3)
            Top =  round((Top/self._Height)*100, 3)
            return [Width, Height, Left, Top]
        except Exception as E:
            self._GUI.Error(f"{self._Type} -> Locate_Reverse -> {E}")

    def Create(self):
        try:
            if not self._Initialized:
                self._GUI.Initiate_Colors(self)
                if self._Minimize:
                    self._Frame.iconify()
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
            if self._Topmost:
                self._Frame.focus_set()
                self._Frame.grab_set()
                self._Frame.attributes("-topmost", self._Topmost)
                if self._Main:
                    self._Frame.transient(self._Main._Frame)
            self._Frame.config(bg=self._Background)
            if not self._Title:
                if self._GUI._Title:
                    self._Title = self._GUI._Title
                else:
                    self._Title = 'Nucleon Glunoix'
            self._Frame.title(self._Title)
            if os.path.exists(self._Icon) and self._Window:
                self._Frame.iconbitmap(self._Icon)
            if self._Persistent:
                self._Frame.protocol("WM_DELETE_WINDOW", self.Nothing)
            else:
                self._Frame.protocol("WM_DELETE_WINDOW", self.On_Close)
                
        except Exception as E:
            self._GUI.Error(f"{self._Type} -> Create -> {E}")
            
    def Initiate_Colors(self, Widget):
        try:
            Variable_Names = ["_Background", "_Foreground", "_Border_Color", "_Shadow_Color", "_Hover_Background", "_Hover_Foreground", "_Hover_Border_Color", "_Hover_Shadow_Color"]
            for Name in Variable_Names:
                if hasattr(Widget, Name):
                    Value = getattr(Widget, Name)
                    Light_Name = "_Light" + Name
                    Dark_Name = "_Dark" + Name
                    if not hasattr(Widget, Light_Name):
                        setattr(Widget, Light_Name, Value)
                    if not hasattr(Widget, Dark_Name):
                        setattr(Widget, Dark_Name, self._GUI.Invert(Value))
        except Exception as E:
            self._GUI.Error(f"{self._Type} -> Initiate_Colors -> {E}")
            
    def Light_Mode(self):
        try:
            self._GUI.Apply_Mode(self, 'Light')
        except Exception as E:
            self._GUI.Error(f"{self._Type} -> Light_Mode -> {E}")

    def Dark_Mode(self):
        try:
            self._GUI.Apply_Mode(self, 'Dark')
        except Exception as E:
            self._GUI.Error(f"{self._Type} -> Dark_Mode -> {E}")
            
    def Update_Color(self):
        try:
            self._GUI.Update_Colors(self)
        except Exception as E:
            self._GUI.Error(f"{self._Type} -> Update_Color -> {E}")
