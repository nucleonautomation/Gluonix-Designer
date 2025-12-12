# IMPORT LIBRARIES
import tkinter as TK
import threading, math, time
from .N_GUI import GUI
from .N_Frame import Frame
from .N_Custom import Event_Bind
from .N_Custom import Event_Bind_Canvas
from .N_Canvas_Line import Canvas_Line
from .N_Canvas_Polyline import Canvas_Polyline
from .N_Canvas_Pie import Canvas_Pie
from .N_Canvas_Arc import Canvas_Arc
from .N_Canvas_Circle import Canvas_Circle
from .N_Canvas_Oval import Canvas_Oval
from .N_Canvas_Rectangle import Canvas_Rectangle
from .N_Canvas_RectangleR import Canvas_RectangleR
from .N_Canvas_Polygon import Canvas_Polygon
from .N_Canvas_Image import Canvas_Image
from .N_Canvas_Text import Canvas_Text
from .N_Canvas_Text_Old import Canvas_Text_Old

class Scroll:

    def __init__(self, Main, *args, **kwargs):
        self._GUI = GUI._Instance
        if self._GUI is not None:
            self._Type = "Scroll"
            try:
                self._Config = ['Name', 'Auto_Dark', 'Background', 'Light_Background', 'Dark_Background', 'Border_Color', 'Light_Border_Color', 'Dark_Border_Color', 'Border_Size', 'Resize', 'Popup', 'Left', 'Top', 'Width', 'Height', 'Scrollbar_Size', 'Vertical', 'Horizontal', 'Last']
                self._Initialized = False
                self._Name = False
                self._Last_Name = False
                self._Widget = []
                self._Item = []
                self._Resize = True
                self._Popup = False
                self._Display = True
                self._Main = Main
                self._Frame_Canvas = Frame(self._Main)
                self._Canvas_Scroll = TK.Canvas(self._Frame_Canvas._Frame)
                self._Scrollbar_Vertical = TK.Scrollbar(self._Frame_Canvas._Frame)
                self._Scrollbar_Horizontal = TK.Scrollbar(self._Frame_Canvas._Frame)
                self._Frame = TK.Canvas(self._Canvas_Scroll)
                self._Frame_Scroll = False
                self._Border_Color = '#000000'
                self._Border_Size = 0
                self._Background = self._Main._Background
                self._Background_Main = True
                self._Scrollbar_Size = 20
                self._Vertical = False
                self._Horizontal = False
                self._Width_Frame = 0
                self._Height_Frame = 0
                self._Last = False
                self._On_Resize = False
                self._Auto_Dark = True
                self._On_Show = False
                self._On_Hide = False
                self._Configure_After_Id = None
            except Exception as E:
                self._GUI.Error(f"{self._Type} -> Init -> {E}")
        else:
            print("Error: Gluonix -> GUI Instance Has Not Been Created")

    def __str__(self):
        return "Nucleon_Glunoix_Scroll[]"

    def __repr__(self):
        return "Nucleon_Glunoix_Scroll[]"
    
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
            for Each in self._Widget:
                Each.Copy(Main=Instance)
            return Instance
        except Exception as E:
            self._GUI.Error(f"{self._Type} -> Copy -> {E}")
        
    def Delete(self):
        try:
            self._Main._Widget.remove(self)
            self._Frame.destroy()
            self._Scrollbar_Vertical.destroy()
            self._Scrollbar_Horizontal.destroy()
            self._Canvas_Scroll.destroy()
            self._Frame_Canvas.Delete()
            if self:
                del self
        except Exception as E:
            self._GUI.Error(f"{self._Type} -> Delete -> {E}")

    def Clear(self):
        try:
            for Each in self._Widget:
                Each.Delete()
            for Each in self._Frame.winfo_children():
                Each.destroy()
        except Exception as E:
            self._GUI.Error(f"{self._Type} -> Clear -> {E}")

    def Refresh(self):
        try:
            self._Frame.update_idletasks()
        except Exception as E:
            self._GUI.Error(f"{self._Type} -> Refresh -> {E}")
            
    def On_Configure(self, Event):
        try:
            if self._Configure_After_Id is not None:
                self._Canvas_Scroll.after_cancel(self._Configure_After_Id)
            self._Configure_After_Id = self._Canvas_Scroll.after(50, self.On_Configure_Debounced)
        except Exception as E:
            self._GUI.Error(f"{self._Type} -> On_Configure -> {E}")
                
    def On_Configure_Debounced(self):
        try:
            self._Configure_After_Id = None
            T = threading.Thread(target=self.On_Configure_Thread, daemon=True)
            T.start()
        except Exception as E:
            self._GUI.Error(f"{self._Type} -> On_Configure_Debounced -> {E}")
    
    def On_Configure_Thread(self):
        try:
            if self._Last:
                self.Update(self._Last)
            else:
                self.Update_All()
        except Exception as E:
            self._GUI.Error(f"{self._Type} -> On_Configure_Thread -> {E}")
            
    def Hide(self):
        try:
            self._Frame_Canvas.Hide()
            self._Display = False
            if self._On_Hide:
                self._On_Hide()
        except Exception as E:
            self._GUI.Error(f"{self._Type} -> Hide -> {E}")
            
    def Show(self):
        try:
            self._Display = True
            self._Frame_Canvas.Show()
            if self._Last:
                self.Update(self._Last)
            else:
                self.Update_All()
            if self._On_Show:
                self._On_Show()
        except Exception as E:
            self._GUI.Error(f"{self._Type} -> Show -> {E}")
            
    def Animate(self, Hide=False, Thread=True):
        try:
            self._Frame_Canvas.Animate(Hide=Hide, Thread=True)
        except Exception as E:
            self._GUI.Error(f"{self._Type} -> Animate -> {E}")
            
    def Animate_Cancel(self):
        try:
            self._Frame_Canvas.Animate_Cancel()
        except Exception as E:
            self._GUI.Error(f"{self._Type} -> Animate_Cancel -> {E}")
            
    def Animate_From(self, Left, Top, Time=None, Speed=None, Ease=None):
        try:
            if Time is not None:
                self._Animate_Time = Time
            if Speed is not None:
                self._Animate_Speed = Speed
            if Ease is not None:
                self._Animate_Ease = Ease
            self._Animate_Left, self._Animate_Top = Left, Top
            if Time is not None:
                self._Frame_Canvas._Animate_Time = Time
            if Speed is not None:
                self._Frame_Canvas._Animate_Speed = Speed
            if Ease is not None:
                self._Frame_Canvas._Animate_Ease = Ease
            self._Frame_Canvas._Animate_Left, self._Frame_Canvas._Animate_Top = Left, Top
            self._Frame_Canvas.Animate()
        except Exception as E:
            self._GUI.Error(f"{self._Type} -> Animate_From -> {E}")
    
    def Grab(self, Path=False):
        try:
            return self._GUI.Grab_Widget(Path=Path, Widget=self)
        except Exception as E:
            self._GUI.Error(f"{self._Type} -> Grab -> {E}")
            
    def Top(self):
        try:
            self._Canvas_Scroll.yview_moveto(0)
            self._Canvas_Scroll.xview_moveto(0)
        except Exception as E:
            self._GUI.Error(f"{self._Type} -> Top -> {E}")
            
    def Reset(self):
        try:
            self.Top()
            self._Width_Frame = self._Width
            self._Height_Frame = self._Height
            self._Frame.config(width=self._Width_Frame, height=self._Height_Frame)
            self._Scrollbar_Horizontal.place_forget()
            self._Scrollbar_Vertical.place_forget()
        except Exception as E:
            self._GUI.Error(f"{self._Type} -> Reset -> {E}")
            
    def Scroll(self, E):
        try:
            if E.delta:
                self._Canvas_Scroll.yview_scroll(int(-1*(E.delta/120)), "units")
        except Exception as E:
            self._GUI.Error(f"{self._Type} -> Scroll -> {E}")
            
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
            Event_Bind(self._Frame, **Input)
        except Exception as E:
            self._GUI.Error(f"{self._Type} -> Bind -> {E}")
            
    def Bind_Item(self, Item, **Input):
        try:
            Event_Bind_Canvas(self._Frame, Item, **Input)
        except Exception as E:
            self._GUI.Error(f"{self._Type} -> Bind_Item -> {E}")
            
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
            self._Frame_Canvas.Config(**Input)
            if self._Initialized and Run:
                self.Create()
            if "Background" in Input:
                self._Background_Main = not bool(Input["Background"])
                for Each in self._Widget:
                    try:
                        if Each._Background_Main:
                            Each.Config(Background=False)
                        if hasattr(Each, '_Radius'):
                            if Each._Radius>0:
                                Each.Config(Radius=Each._Radius)
                    except Exception:
                        self.Nothing = False
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
                self.Config(Left=self._Left, Top=self._Top)
            return self._Frame_Canvas.Position()
        except Exception as E:
            self._GUI.Error(f("{self._Type} -> Position -> {E}"))
            
    def Size(self, Width=False, Height=False):
        try:
            if Width:
                self._Width = Width
            if Height:
                self._Height = Height
            if Width or Height:
                self.Config(Width=self._Width, Height=self._Height)
            return self._Frame_Canvas.Size()
        except Exception as E:
            self._GUI.Error(f"{self._Type} -> Size -> {E}")
            
    def Box(self):
        try:
            return self._Frame_Canvas.Box()
        except Exception as E:
            self._GUI.Error(f"{self._Type} -> Box -> {E}")
        
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
                self._Width_Frame = self._Width
                self._Height_Frame = self._Height
                self._Frame_Canvas.Config(Width=self._Width, Height=self._Height, Left=self._Left, Top=self._Top)
                self._Frame_Canvas.Config(Background=self._Background, Border_Size=self._Border_Size, Border_Color=self._Border_Color)
                self._Frame_Canvas.Create()
                self._Canvas_Scroll.bind("<Configure>", self.On_Configure, add="+")
                self._Frame.bind("<MouseWheel>", self.Scroll)
                self._Frame.bind("<Configure>", lambda e: self._Canvas_Scroll.configure(scrollregion=self._Canvas_Scroll.bbox("all")))
                if not self._Display:
                    self.Hide()
                self._Main._Widget.append(self)
                self._Canvas_Scroll.config(background=self._Background, highlightthickness=0)
                self._Canvas_Scroll.place(relx=0, rely=0, relwidth=1, relheight=1)
                self._Frame.config(background=self._Background, highlightthickness=0)
                self._Initialized = True
            self._Scrollbar_Vertical.config(orient="vertical", command=self._Canvas_Scroll.yview, width=self._Scrollbar_Size)
            self._Scrollbar_Horizontal.config(orient="horizontal", command=self._Canvas_Scroll.xview, width=self._Scrollbar_Size)
            self._Frame.place(relx=0, rely=0, relwidth=(self._Width-self._Scrollbar_Size)/self._Width, relheight=(self._Height-self._Scrollbar_Size)/self._Height)
            self._Frame['highlightthickness']=0
            if not self._Frame_Scroll:
                self._Frame_Scroll = self._Canvas_Scroll.create_window((0, 0), window=self._Frame, anchor="nw")
                self._Canvas_Scroll.configure(yscrollcommand=self._Scrollbar_Vertical.set)
                self._Canvas_Scroll.configure(xscrollcommand=self._Scrollbar_Horizontal.set)
                self._Canvas_Scroll.pack(side="left", fill="both", expand=True)
            if self._Last:
                self.Update(self._Last)
            else:
                self.Update_All()
            if self._Vertical:
                self._Scrollbar_Vertical.place(relx=(self._Width-self._Scrollbar_Size)/self._Width, rely=0, relwidth=self._Scrollbar_Size/self._Width, relheight=1)
            if self._Horizontal:
                self._Scrollbar_Horizontal.place(relx=0, rely=(self._Height-self._Scrollbar_Size)/self._Height, relwidth=1, relheight=self._Scrollbar_Size/self._Height)
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
             
    def _Update_Scrollbars(self):
        try:
            Left, Top, Width, Height = self._Frame_Canvas.Box()
            self._Frame.config(width=self._Width_Frame, height=self._Height_Frame)
            if Height >= self._Height_Frame:
                self._Scrollbar_Vertical.place_forget()
            else:
                self._Scrollbar_Vertical.place(relx=(self._Width-self._Scrollbar_Size)/self._Width, rely=0, relwidth=self._Scrollbar_Size/self._Width, relheight=1)
            if Width >= self._Width_Frame:
                self._Scrollbar_Horizontal.place_forget()
            else:
                self._Scrollbar_Horizontal.place(relx=0, rely=(self._Height-self._Scrollbar_Size)/self._Height, relwidth=1, relheight=self._Scrollbar_Size/self._Height)
            if self._Vertical:
                self._Scrollbar_Vertical.place(relx=(self._Width-self._Scrollbar_Size)/self._Width, rely=0, relwidth=self._Scrollbar_Size/self._Width, relheight=1)
            if self._Horizontal:
                self._Scrollbar_Vertical.place(relx=(self._Width-self._Scrollbar_Size)/self._Width, rely=0, relwidth=self._Scrollbar_Size/self._Width, relheight=1)
        except Exception as E:
            self._GUI.Error(f"{self._Type} -> _Update_Scrollbars -> {E}")
             
    def Update(self, Widget):
        try:
            Extra_Space = self._Scrollbar_Size
            Left, Top, Width, Height = Widget.Box()
            Right = Left + Width
            Bottom = Top + Height
            if self._Width_Frame < Right:
                self._Width_Frame = Right + Extra_Space*2
            if self._Height_Frame < Bottom:
                self._Height_Frame = Bottom + Extra_Space*3
            self._Update_Scrollbars()
            self._Last = Widget
        except Exception as E:
            self._GUI.Error(f"{self._Type} -> Update -> {E}")
             
    def Update_All(self):
        try:
            Extra_Space = self._Scrollbar_Size
            for Widget in self._Widget:
                Left, Top, Width, Height = Widget.Box()
                Right = Left + Width
                Bottom = Top + Height
                if self._Width_Frame < Right:
                    self._Width_Frame = Right + Extra_Space
                if self._Height_Frame < Bottom:
                    self._Height_Frame = Bottom + Extra_Space
            self._Update_Scrollbars()
        except Exception as E:
            self._GUI.Error(f"{self._Type} -> Update_All -> {E}")

    def Hide_Item(self, Item=False):
        try:
            if Item:
                self._Frame.itemconfigure(Item, state='hidden')
        except Exception as E:
            self._GUI.Error(f"{self._Type} -> Hide_Item -> {E}")

    def Show_Item(self, Item=False):
        try:
            if Item:
                self._Frame.itemconfigure(Item, state='normal')
                self._Frame.tag_raise(Item)
        except Exception as E:
            self._GUI.Error(f"{self._Type} -> Show_Item -> {E}")
    
    def Delete_Item(self, Item=False):
        try:
            if Item:
                self._Frame.delete(Item)
        except Exception as E:
            self._GUI.Error(f"{self._Type} -> Delete_Item -> {E}")
    
    def Delete_All(self):
        try:
            self._Frame.delete('all')
        except Exception as E:
            self._GUI.Error(f"{self._Type} -> Delete_All -> {E}")
            
    def Find_Near(self, X, Y):
        try:
            return self._Frame.find_closest(X, Y)
        except Exception as E:
            self._GUI.Error(f"{self._Type} -> Find_Near -> {E}")
            
    def Find_Overlap(self, X1, Y1, X2, Y2):
        try:
            return self._Frame.find_overlapping(X1, Y1, X2, Y2)
        except Exception as E:
            self._GUI.Error(f"{self._Type} -> Find_Overlap -> {E}")
            
    def Line(self, Name=False):
        try:
            Item = Canvas_Line(self)
            if Name:
                Item.Config(Name=Name)
            return Item
        except Exception as E:
            self._GUI.Error(f"{self._Type} -> Line -> {E}")
            
    def Polyline(self, Name=False):
        try:
            Item = Canvas_Polyline(self)
            if Name:
                Item.Config(Name=Name)
            return Item
        except Exception as E:
            self._GUI.Error(f"{self._Type} -> Polyline -> {E}")
                
    def Pie(self, Name=False):
        try:
            Item = Canvas_Pie(self)
            if Name:
                Item.Config(Name=Name)
            return Item
        except Exception as E:
            self._GUI.Error(f"{self._Type} -> Pie -> {E}")
                
    def Arc(self, Name=False):
        try:
            Item = Canvas_Arc(self)
            if Name:
                Item.Config(Name=Name)
            return Item
        except Exception as E:
            self._GUI.Error(f"{self._Type} -> Arc -> {E}")
                
    def Circle(self, Name=False):
        try:
            Item = Canvas_Circle(self)
            if Name:
                Item.Config(Name=Name)
            return Item
        except Exception as E:
            self._GUI.Error(f"{self._Type} -> Circle -> {E}")
                
    def Oval(self, Name=False):
        try:
            Item = Canvas_Oval(self)
            if Name:
                Item.Config(Name=Name)
            return Item
        except Exception as E:
            self._GUI.Error(f"{self._Type} -> Oval -> {E}")
            
    def Polygon(self, Name=False):
        try:
            Item = Canvas_Polygon(self)
            if Name:
                Item.Config(Name=Name)
            return Item
        except Exception as E:
            self._GUI.Error(f"{self._Type} -> Polygon -> {E}")
                
    def Rectangle(self, Name=False):
        try:
            Item = Canvas_Rectangle(self)
            if Name:
                Item.Config(Name=Name)
            return Item
        except Exception as E:
            self._GUI.Error(f"{self._Type} -> Rectangle -> {E}")
                
    def RectangleR(self, Name=False):
        try:
            Item = Canvas_RectangleR(self)
            if Name:
                Item.Config(Name=Name)
            return Item
        except Exception as E:
            self._GUI.Error(f"{self._Type} -> RectangleR -> {E}")
                
    def Image(self, Name=False):
        try:
            Item = Canvas_Image(self)
            if Name:
                Item.Config(Name=Name)
            return Item
        except Exception as E:
            self._GUI.Error(f"{self._Type} -> Image -> {E}")
            
    def Text(self, Name=False):
        try:
            Item = Canvas_Text(self)
            if Name:
                Item.Config(Name=Name)
            return Item
        except Exception as E:
            self._GUI.Error(f"{self._Type} -> Text -> {E}")
            
    def Text_Old(self, Name=False):
        try:
            Item = Canvas_Text_Old(self)
            if Name:
                Item.Config(Name=Name)
            return Item
        except Exception as E:
            self._GUI.Error(f"{self._Type} -> Text_Old -> {E}")
