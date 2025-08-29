# IMPORT LIBRARIES
import io
import base64
from PIL import Image as PIL_Image
from .N_GUI import GUI
from .N_Image_Lite import Image_Lite
from .N_Custom import Event_Bind

def Create_Image(Image_Data):
    try:
        Image_Data = base64.b64decode(Image_Data)
        return PIL_Image.open(io.BytesIO(Image_Data))
    except:
        pass

Image_True = Create_Image("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")
Image_False = Create_Image("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")
           
class Switch:

    def __init__(self, Main, *args, **kwargs):
        self._GUI = GUI._Instance
        if self._GUI is not None:
            self._Type = "Switch"
            try:
                self._Config = ['Name', 'Auto_Dark', 'Background', 'Light_Background', 'Dark_Background', 'Resize_Width', 'Resize', 'Resize_Height', 'Move', 'Move_Left', 'Move_Top', 'Popup', 'Display', 'Left', 'Top', 'Width', 'Height']
                self._Initialized = False
                self._Widget = []
                self._Name = False
                self._Last_Name = False
                self._Resize_Font, self._Resize, self._Resize_Width, self._Resize_Height, self._Move, self._Move_Left, self._Move_Top = False, True, True, True, True, True, True
                self._Image = {True: Image_True, False: Image_False}
                self._Popup = False
                self._Display = True
                self._Size_Update = False
                self._Resize_Index = 0
                self._Main = Main
                self._Frame = Image_Lite(self._Main)
                self._Frame.Config(Convert_Type='RGBA')
                self._Border_Color = '#000000'
                self._Border_Size = 0
                self._Background = self._Main._Background
                self._Background_Main = True
                self._Auto_Dark = True
                self._Check = False
                self._Resizable = self._Main._Resizable
                self._On_Change = False
                self._On_Show = False
                self._On_Hide = False
            except Exception as E:
                self._GUI.Error(f"{self._Type} -> Init -> {E}")
        else:
            print("Error: Gluonix -> GUI Instance Has Not Been Created")

    def __str__(self):
        return "Nucleon_Glunoix_Switch[]"

    def __repr__(self):
        return "Nucleon_Glunoix_Switch[]"
    
    def Copy(self, Name=False, Main=False):
        try:
            if not Main:
                Main = self._Main
            Instance = type(self)(Main)
            for Key in self._Config:
                if hasattr(self, "_"+Key):
                    setattr(Instance, "_"+Key, getattr(self, "_"+Key))
            if Name:
                setattr(Instance, "_Name", Name)
            Instance.Create()
            return Instance
        except Exception as E:
            self._GUI.Error(f"{self._Type} -> Copy -> {E}")
        
    def Delete(self):
        try:
            self._Main._Widget.remove(self)
            self._Frame.Delete()
            if self:
                del self
        except Exception as E:
            self._GUI.Error(f"{self._Type} -> Delete -> {E}")
            
    def Hide(self):
        try:
            self._Frame.Hide()
            self._Display = False
            if self._On_Hide:
                self._On_Hide()
        except Exception as E:
            self._GUI.Error(f"{self._Type} -> Hide -> {E}")
            
    def Show(self):
        try:
            self._Display = True
            if self._Resizable and self._Resize_Index<self._GUI._Resize_Index:
                self.Resize()
            else:
                self.Display()
            if self._On_Show:
                self._On_Show()
        except Exception as E:
            self._GUI.Error(f"{self._Type} -> Show -> {E}")
            
    def Display(self):
        try:
            self._Frame.Show()
            self._Display = True
        except Exception as E:
            self._GUI.Error(f"{self._Type} -> Display -> {E}")
    
    def Grab(self, Path=False):
        try:
            return self._GUI.Grab_Widget(Path=Path, Widget=self)
        except Exception as E:
            self._GUI.Error(f"{self._Type} -> Grab -> {E}")
            
    def Animate(self):
        try:
            self._Frame.Animate()
            self.Show()
        except Exception as E:
            self._GUI.Error(f"{self._Type} -> Animate -> {E}")
            self.Animate_Cancel()
            
    def Animate_Cancel(self):
        try:
            self._Frame.Animate_Cancel()
        except Exception as E:
            self._GUI.Error(f"{self._Type} -> Animate_Cancel -> {E}")
            
    def Get(self):
        try:
            return self._Check
        except Exception as E:
            self._GUI.Error(f"{self._Type} -> Get -> {E}")
            
    def Set(self, Check):
        try:
            if Check!=self._Check:
                self._Check = Check
                self._Frame.Set(Path=self._Image[self._Check])
        except Exception as E:
            self._GUI.Error(f"{self._Type} -> Set -> {E}")
            
    def Set_On_Click(self):
        try:
            self._Check = not self._Check
            self._Frame.Set(Path=self._Image[self._Check])
            if self._On_Change:
                self._On_Change()
        except Exception as E:
            self._GUI.Error(f"{self._Type} -> Set_On_Click -> {E}")
            
    def Widget(self):
        try:
            return self._Frame._Widget
        except Exception as E:
            self._GUI.Error(f"{self._Type} -> Widget -> {E}")
            
    def Bind(self, **Input):
        try:
            if 'On_Show' in Input:
                self._On_Show = Input['On_Show']
            if 'On_Hide' in Input:
                self._On_Hide = Input['On_Hide']
            if 'On_Change' in Input:
                self._On_Change = Input['On_Change']
            self._Frame.Bind(**Input)
        except Exception as E:
            self._GUI.Error(f"{self._Type} -> Bind -> {E}")
            
    def Config_Get(self, *Input):
        try:
            Return = {}
            for Each in self._Config:
                if Each in Input:
                    Return[Each] = getattr(self, "_"+Each)
            return Return
        except Exception as E:
            self._GUI.Error(f"{self._Type} -> Config_Get -> {E}")
                
    def Config(self, **Input):
        try:
            Run = False
            for Each in self._Config:
                if Each in Input:
                    Value = Input[Each]
                    setattr(self, "_"+Each, Value)
                    Run = True
            self._Frame.Config(**Input)
            if "Width" in Input or "Height" in Input:
                self._Size_Update = True
            if self._Initialized and Run:
                self.Create()
            if "Background" in Input:
                self._Background_Main = not bool(Input["Background"])
        except Exception as E:
            self._GUI.Error(f"{self._Type} -> Config -> {E}")
            
    def Move(self, Left=None, Top=None):
        try:
            if Left is not None:
                self._Left += Left
            if Top is not None:
                self._Top += Top
            if Left is not None or Top is not None:
                self.Position(Left=self._Left, Top=self._Top)
            return True
        except Exception as E:
            self._GUI.Error(f"{self._Type} -> Move -> {E}")
            
    def Center(self, Left=None, Top=None):
        try:
            if Left is not None:
                self._Left = Left-self._Width/2
            if Top is not None:
                self._Top = Top-self._Height/2
            if Left is not None or Top is not None:
                self.Position(Left=self._Left, Top=self._Top)
            return [self._Left+self._Width/2, self._Top+self._Height/2]
        except Exception as E:
            self._GUI.Error(f"{self._Type} -> Center -> {E}")
            
    def Position(self, Left=None, Top=None):
        try:
            if Left is not None:
                self._Left = Left
            if Top is not None:
                self._Top = Top
            if Left is not None or Top is not None:
                self._Frame.Position(Left=self._Left, Top=self._Top)
                self.Relocate()
            return self._Frame.Position()
        except Exception as E:
            self._GUI.Error(f"{self._Type} -> Position -> {E}")
            
    def Size(self, Width=False, Height=False):
        try:
            if Width:
                self._Width = Width
            if Height:
                self._Height = Height
            if Width or Height:
                self._Frame.Size(Width=self._Width, Height=self._Height)
                self.Relocate()
            return self._Frame.Size()
        except Exception as E:
            self._GUI.Error(f"{self._Type} -> Size -> {E}")
        
    def Locate(self, Width, Height, Left, Top):
        try:
            Width = self._Width*(Width/100)
            Height = self._Height*(Height/100)
            Left = self._Width*(Left/100)-self._Border_Size
            Top = self._Height*(Top/100)-self._Border_Size
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
            if not self._Background:
                self._Background = self._Main._Background
                if not hasattr(self, "_Light_Background"):
                    setattr(self, "_Light_Background", self._Background)
                if not hasattr(self, "_Dark_Background"):
                    setattr(self, "_Dark_Background", self._GUI.Invert(self._Background))
            if self._Auto_Dark and not self._GUI._Dark_Mode:
                self.Update_Color()
            if not self._Initialized:
                self.Update_Color()
                self._Width_Current, self._Height_Current, self._Left_Current, self._Top_Current, = self._Width, self._Height, self._Left, self._Top
                self._Frame.Config(Width=self._Width_Current, Height=self._Height_Current, Left=self._Left_Current, Top=self._Top_Current)
                self._Frame.Config(Background=self._Background, Aspect_Ratio=False)
                self._Frame.Config(Transparent=True, Use_Foreground=True)
                self._Frame.Bind(On_Click=lambda E: self.Set_On_Click())
                self._Frame.Create()
                self._Frame.Config(Convert_Type='RGBA', Pil=True)
                if not self._Display:
                    self.Hide()
                self._Main._Widget.append(self)
                self._Initialized = True
            self._Frame.Set(Path=self._Image[self._Check])
            self.Resize()
            if self._Display:
                self.Display()
            if self._Name!=self._Last_Name:
                if self._Last_Name:
                    if self._Last_Name in self._Main.__dict__:
                        del self._Main.__dict__[self._Last_Name]
                if self._Name:
                    self._Main.__dict__[self._Name] = self
                self._Last_Name = self._Name
        except Exception as E:
            self._GUI.Error(f"{self._Type} -> Create -> {E}")
            
    def Update_Color(self):
        try:
            self._GUI.Initiate_Colors(self)
        except Exception as E:
            self._GUI.Error(f"{self._Type} -> Update_Color -> {E}")
            
    def Relocate(self, Direct=False):
        try:
            self.Display()
        except Exception as E:
            self._GUI.Error(f"{self._Type} -> Relocate -> {E}")
            
    def Resize(self):
        try:
            self._Resize_Index = self._GUI._Resize_Index
            self.Relocate()
        except Exception as E:
            self._GUI.Error(f"{self._Type} -> Resize -> {E}")
            