# IMPORT LIBRARIES
import os
import math
from PIL import Image as PIL_Image, ImageTk as PIL_ImageTk
import tkinter as TK
from .N_GUI import GUI
from .N_Frame import Frame
from .N_Custom import Event_Bind

class Tree:

    def __init__(self, Main, *args, **kwargs):
        self._GUI = GUI._Instance
        if self._GUI is not None:
            self._Type = "Tree"
            try:
                self._Config = ['Name', 'Background', 'Light_Background', 'Dark_Background', 'Foreground', 'Light_Foreground', 'Dark_Foreground', 'Border_Color', 'Light_Border_Color', 'Dark_Border_Color', 'Border_Size', 'Resize_Width', 'Resize', 'Resize_Height', 'Move', 'Move_Left', 'Move_Top', 'Popup', 'Display', 'Left', 'Top', 'Width', 'Height', 'Font_Size', 'Font_Weight', 'Background_Selected', 'Foreground_Selected', 'Hover_Background', 'Light_Hover_Background', 'Dark_Hover_Background', 'Hover_Foreground', 'Light_Hover_Foreground', 'Dark_Hover_Foreground', 'Hover_Border_Color', 'Light_Hover_Border_Color', 'Dark_Hover_Border_Color']
                self._Initialized = False
                self._Name = False
                self._Last_Name = False
                self._Tag = []
                self._Item = []
                self._Image = {}
                self._Resize_Font, self._Resize, self._Resize_Width, self._Resize_Height, self._Move, self._Move_Left, self._Move_Top = False, True, True, True, True, True, True
                self._Popup = False
                self._Display = True
                self._Main = Main
                self._Style = TK.ttk.Style()
                self._Style.theme_use('clam')
                self._Style_Name = "CustomStyle_" + str(id(self))
                self._Style.layout(self._Style_Name, [])
                self._Frame = Frame(self._Main)
                self._Widget = TK.ttk.Treeview(self._Frame._Frame, show="tree")
                self._Widget.configure(style=self._Style_Name)
                self._Scrollbar_Vertical = TK.Scrollbar(self._Frame._Frame)
                self._Scrollbar_Horizontal = TK.Scrollbar(self._Frame._Frame)
                self._Border_Color = '#000000'
                self._Border_Size = 0
                self._Background = self._Main._Background
                self._Background_Main = True
                self._Foreground = '#000000'
                self._Hover_Background = False
                self._Hover_Foreground = False
                self._Hover_Border_Color = False
                self._Last_Background = False
                self._Last_Foreground = False
                self._Last_Border_Color = False
                self._Background_Selected = "#d0e4f5"
                self._Foreground_Selected = "#000000"
                self._Font_Size = 12
                self._Font_Weight = 'normal'
                self._Resizable = self._Main._Resizable
                self._Width_Item = None
                self._Width_Text = ''
                self._On_Show = False
                self._On_Hide = False
                self._On_Hover_In = False
                self._On_Hover_Out = False
            except Exception as E:
                self._GUI.Error(f"{self._Type} -> Init -> {E}")
        else:
            print("Error: Gluonix -> GUI Instance Has Not Been Created")

    def __str__(self):
        return "Nucleon_Glunoix_Tree[]"

    def __repr__(self):
        return "Nucleon_Glunoix_Tree[]"
    
    def Copy(self, Name=False, Main=False):
        try:
            if not Main:
                Main = self._Main
            Instance = type(self)(Main)
            for Key in self._Config:
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
            self._Widget.destroy()
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
            if self._Resizable:
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
            self._Widget.place(x=0, y=0, width=self._Width_Current-(self._Border_Size*2), height=self._Height_Current-(self._Border_Size*2)-20)
            self._Display = True
        except Exception as E:
            self._GUI.Error(f"{self._Type} -> Display -> {E}")
    
    def Grab(self, Path=False):
        try:
            return self._GUI.Grab_Widget(Path=Path, Widget=self)
        except Exception as E:
            self._GUI.Error(f"{self._Type} -> Grab -> {E}")
            
    def Scroll(self, E):
        try:
            if E.delta:
                self._Widget.yview_scroll(int(-1*(E.delta/120)), "units")
        except Exception as E:
            self._GUI.Error(f"{self._Type} -> Scroll -> {E}")

    def Export(self, Path="TreeStructure.txt"):
        try:
            if os.path.exists(Path):
                os.remove(Path)
            with open(Path, "w") as File:
                self.Export_All(File)
        except Exception as E:
            self._GUI.Error(f"{self._Type} -> Export -> {E}")

    def Export_All(self, File, Parent="", Indent=0):
        try:
            Line = " " * Indent + self._Widget.item(Parent, "text") + "\n"
            File.write(Line)
            for Child in self._Widget.get_children(Parent):
                self.Export_All(File, Child, Indent + 4)
        except Exception as E:
            self._GUI.Error(f"{self._Type} -> Export_All -> {E}")
            
    def Get(self, ID=False):
        try:
            if not ID:
                ID = self._Widget.focus()
            return self._Widget.item(ID)['values']
        except Exception as E:
            self._GUI.Error(f"{self._Type} -> Get -> {E}")
            
    def Get_All(self, ID=False):
        try:
            if not ID:
                ID = self._Widget.focus()
            return self._Widget.item(ID)
        except Exception as E:
            self._GUI.Error(f"{self._Type} -> Get_All -> {E}")
            
    def Get_Selected(self):
        try:
            Return = []
            for Each in self._Widget.selection():
                Return.append(self._Widget.item(Each))
            return Return
        except Exception as E:
            self._GUI.Error(f"{self._Type} -> Get_Selected -> {E}")
            
    def Remove(self, ID):
        try:
            self._Widget.delete(ID)
            self._Item.remove(ID)
        except Exception as E:
            self._GUI.Error(f"{self._Type} -> Remove -> {E}")
            
    def Remove_All(self):
        try:
            for Each in self._Item:
                if self._Widget.exists(Each):
                    self.Remove(Each)
            self._Item = []
        except Exception as E:
            self._GUI.Error(f"{self._Type} -> Remove_All -> {E}")
            
    def Remove_Selected(self):
        try:
            for Each in self._Widget.selection():
                self.Remove(Each)
        except Exception as E:
            self._GUI.Error(f"{self._Type} -> Remove_Selected -> {E}")
            
    def Edit(self, Name=False, Value=False, Tag=False, ID=False):
        try:
            if not ID:
                ID = self._Widget.focus()
            if Name:
                self._Widget.item(ID, text=Name)
                self.Adjust_Width(Name, ID)
            if Value:
                self._Widget.item(ID, value=Value)
            if Tag:
                self._Widget.item(ID, tags=(Tag))
        except Exception as E:
            self._GUI.Error(f"{self._Type} -> Edit -> {E}")
            
    def Add(self, Name, Parent='', Index='end', Tag='Default', Value=[], ID=None, Path=None):
        try:
            if Index!='end':
                if not isinstance(Index, int):
                    Index = int(self.Index(Index))
            Insert_Args = {'parent': Parent, 'index': Index, 'text': f' {Name}', 'values': Value, 'tags': Tag}
            if ID is not None:
                Insert_Args['iid'] = ID
            if Path is not None and os.path.exists(Path):
                if Path not in self._Image:
                    Image_Pil = PIL_Image.open(Path)
                    Height = math.ceil(self._Font_Size * 1.5)
                    Aspect_Ratio = Image_Pil.width / Image_Pil.height
                    Width = int(Height * Aspect_Ratio)
                    Image_Pil = Image_Pil.resize((Width, Height), PIL_Image.NEAREST)
                    Image = PIL_ImageTk.PhotoImage(Image_Pil)
                    self._Image[Path] = Image
                else:
                    Image = self._Image[Path]
                Insert_Args['image'] = Image
            Item = self._Widget.insert(**Insert_Args)
            self._Item.append(Item)
            self.Adjust_Width(Name, Item)
            return Item
        except Exception as E:
            self._GUI.Error(f"{self._Type} -> Add -> {E}")
            
    def Index(self, Item):
        try:
            return self._Widget.index(Item)
        except Exception as E:
            self._GUI.Error(f"{self._Type} -> Index -> {E}")
            
    def Level(self, Item):
        try:
            Level = 0
            Parent = self._Widget.parent(Item)
            while Parent:
                Level += 1
                Parent = self._Widget.parent(Parent)
            return Level
        except Exception as E:
            self._GUI.Error(f"{self._Type} -> Level -> {E}")
            
    def Adjust_Width(self, Text, Item):
        try:
            if Item is not None:
                Font = TK.font.Font(family='Times New Roman', size=self._Font_Size, weight=self._Font_Weight)
                Width = Font.measure(Text) + 45 + (20 * self.Level(Item))
                Current_Width = self._Widget.column("#0", 'width')
                if Width > Current_Width:
                    self._Width_Text = Text
                    self._Width_Item = Item
                    self._Widget.column("#0", width=Width)
        except Exception as E:
            self._GUI.Error(f"{self._Type} -> Adjust_Width -> {E}")
            
    def Tag(self, Name, Foreground=False, Background=False):
        try:
            if not Foreground:
                Foreground = self._Foreground
            if not Background:
                Background = self._Background
            if Name not in self._Tag:
                self._Widget.tag_configure(Name, font=('Times New Roman', self._Font_Size, self._Font_Weight), foreground=Foreground, background=Background)
                self._Tag.append(Name)
        except Exception as E:
            self._GUI.Error(f"{self._Type} -> Tag -> {E}")
            
    def Current(self):
        try:
            return self._Widget.focus()
        except Exception as E:
            self._GUI.Error(f"{self._Type} -> Current -> {E}")
            
    def Selected(self):
        try:
            Temp_List = []
            for Each in self._Widget.selection():
                Temp_List.append(Each)
            return Temp_List
        except Exception as E:
            self._GUI.Error(f"{self._Type} -> Selected -> {E}")
            
    def Child(self, ID=False):
        try:
            if ID:
                return self._Widget.get_children(ID)
        except Exception as E:
            self._GUI.Error(f"{self._Type} -> Child -> {E}")
            
    def Parent(self, ID=False):
        try:
            if ID:
                return self._Widget.parent(ID)
        except Exception as E:
            self._GUI.Error(f"{self._Type} -> Parent -> {E}")
            
    def Expand(self, ID=False):
        try:
            if not ID:
                ID = self._Widget.focus()
            self._Widget.item(ID, open=True)
        except Exception as E:
            self._GUI.Error(f"{self._Type} -> Expand -> {E}")
            
    def Select(self, ID=False):
        try:
            if ID:
                self._Widget.selection_set(ID)
                self._Widget.focus(ID)
        except Exception as E:
            self._GUI.Error(f"{self._Type} -> Select -> {E}")
            
    def Widget(self):
        try:
            return self._Widget
        except Exception as E:
            self._GUI.Error(f"{self._Type} -> Widget -> {E}")
            
    def Bind(self, **Input):
        try:
            if 'On_Show' in Input:
                self._On_Show = Input['On_Show']
            if 'On_Hide' in Input:
                self._On_Hide = Input['On_Hide']
            self._Frame.Bind(**Input)
            if 'On_Hover_In' in Input:
                self._On_Hover_In = Input['On_Hover_In']
            Input['On_Hover_In'] = lambda E: self.On_Hover_In(E)
            if 'On_Hover_Out' in Input:
                self._On_Hover_Out = Input['On_Hover_Out']
            Input['On_Hover_Out'] = lambda E: self.On_Hover_Out(E)
            Event_Bind(self._Widget, **Input)
        except Exception as E:
            self._GUI.Error(f"{self._Type} -> Bind -> {E}")
            
    def On_Hover_In(self, E):
        try:
            Config = {}
            if self._Hover_Background:
                self._Last_Background = self._Background
                Config['Background'] = self._Hover_Background
            if self._Hover_Foreground:
                self._Last_Foreground = self._Foreground
                Config['Foreground'] = self._Hover_Foreground
            if self._Hover_Border_Color:
                self._Last_Border_Color = self._Border_Color
                Config['Border_Color'] = self._Hover_Border_Color
            if len(Config)>0:
                self.Config(**Config)
            if self._On_Hover_In:
                self._On_Hover_In(E)
        except Exception as E:
            self._GUI.Error(f"{self._Type} -> On_Hover_In -> {E}")
            
    def On_Hover_Out(self, E):
        try:
            Config = {}
            if self._Hover_Background and self._Last_Background:
                Config['Background'] = self._Last_Background
            if self._Hover_Foreground and self._Last_Foreground:
                Config['Foreground'] = self._Last_Foreground
            if self._Hover_Border_Color and self._Last_Border_Color:
                Config['Border_Color'] = self._Last_Border_Color
            if len(Config)>0:
                self.Config(**Config)
            if self._On_Hover_Out:
                self._On_Hover_Out(E)
        except Exception as E:
            self._GUI.Error(f"{self._Type} -> On_Hover_Out -> {E}")
            
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
            if self._Initialized and Run:
                self.Create()
            if "Background" in Input:
                self._Background_Main = not bool(Input["Background"])
        except Exception as E:
            self._GUI.Error(f"{self._Type} -> Config -> {E}")
            
    def Position(self, Left=None, Top=None):
        try:
            if Left is not None:
                self._Left = Left
            if Top is not None:
                self._Top = Top
            if Left is not None or Top is not None:
                self._Frame.Position(Left=Left, Top=Top)
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
                self._Frame.Size(Width=Width, Height=Height)
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
            if not self._Initialized:
                self._GUI.Initiate_Colors(self)
                self._Width_Current, self._Height_Current, self._Left_Current, self._Top_Current = self._Width, self._Height, self._Left, self._Top
                self._Frame.Config(Width=self._Width_Current, Height=self._Height_Current, Left=self._Left_Current, Top=self._Top_Current)
                self._Frame.Config(Background=self._Background, Border_Size=self._Border_Size, Border_Color=self._Border_Color)
                self._Frame.Create()
                Event_Bind(self._Widget, On_Hover_In=lambda E: self.On_Hover_In(E), On_Hover_Out=lambda E: self.On_Hover_Out(E))
                self._Widget.bind("<MouseWheel>", self.Scroll)
                self._Scrollbar_Vertical.config(orient="vertical", command=self._Widget.yview, width=20)
                self._Scrollbar_Horizontal.config(orient="horizontal", command=self._Widget.xview, width=20)
                self._Widget.configure(xscrollcommand=self._Scrollbar_Horizontal.set)
                self._Widget.configure(yscrollcommand=self._Scrollbar_Vertical.set)
                self._Scrollbar_Vertical.place(relx=1, rely=0, relheight=1, anchor="ne")
                self.Tag(Name='Default', Foreground=self._Foreground)
                if not self._Display:
                    self.Hide()
                self._Main._Widget.append(self)
                self._Initialized = True
            self._Widget.tag_configure('Default', font=('Times New Roman', self._Font_Size, self._Font_Weight), foreground=self._Foreground, background=self._Background)
            self._Style.configure(self._Style_Name, rowheight=self._Font_Size*2, background=self._Background, highlightthickness=0, bd=0, borderwidth=0)
            self._Style.map(self._Style_Name, background=[("selected", self._Background_Selected)], foreground=[("selected", self._Foreground_Selected)])
            self._Scrollbar_Horizontal.place(relx=0, rely=1, relwidth=1, anchor="sw")
            self.Adjust_Width(self._Width_Text, self._Width_Item)
            self.Relocate()
            if self._Name!=self._Last_Name:
                if self._Last_Name:
                    if self._Last_Name in self._Main.__dict__:
                        del self._Main.__dict__[self._Last_Name]
                if self._Name:
                    self._Main.__dict__[self._Name] = self
                self._Last_Name = self._Name
        except Exception as E:
            self._GUI.Error(f"{self._Type} -> Create -> {E}")
            
    def Adjustment(self):
        try:
            Width_Difference = self._Main._Width_Current - self._Main._Width
            Width_Ratio = self._Width / (self._Main._Width - self._Main._Border_Size*2)
            self._Width_Adjustment = Width_Difference * Width_Ratio
            Height_Difference = self._Main._Height_Current - self._Main._Height
            Height_Ratio = self._Height / (self._Main._Height - self._Main._Border_Size*2)
            self._Height_Adjustment = Height_Difference * Height_Ratio
            Left_Ratio = self._Left / self._Main._Width
            self._Left_Adjustment = Width_Difference * Left_Ratio
            Top_Ratio = self._Top / self._Main._Height
            self._Top_Adjustment = Height_Difference * Top_Ratio
        except Exception as E:
            self._GUI.Error(f"{self._Type} -> Adjustment -> {E}")
            
    def Relocate(self, Direct=False):
        try:
            self.Adjustment()
            if Direct or (self._Resize and self._Resize_Width):
                self._Width_Current = self._Width + self._Width_Adjustment
            else:
                self._Width_Current = self._Width
            if Direct or (self._Resize and self._Resize_Height):
                self._Height_Current = self._Height + self._Height_Adjustment
            else:
                self._Height_Current = self._Height
            if Direct or (self._Move and self._Move_Left):
                self._Left_Current = self._Left + self._Left_Adjustment
            else:
                self._Left_Current = self._Left
            if Direct or (self._Move and self._Move_Top):
                self._Top_Current = self._Top + self._Top_Adjustment
            else:
                self._Top_Current = self._Top
            if self._Display:
                self.Display()
        except Exception as E:
            self._GUI.Error(f"{self._Type} -> Relocate -> {E}")
            
    def Resize(self):
        try:
            self.Relocate()
        except Exception as E:
            self._GUI.Error(f"{self._Type} -> Resize -> {E}")