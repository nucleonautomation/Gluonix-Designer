################################################################################################################################
# Programming Start
################################################################################################################################

# -------------------------------------------------------------------------------------------------------------------------------
# Import Libraries
# -------------------------------------------------------------------------------------------------------------------------------
# Custom Libraries
from Nucleon import Gluonix

# Default Libraries
import os
import time
import atexit
import datetime
import warnings

# -------------------------------------------------------------------------------------------------------------------------------
# Customization
# -------------------------------------------------------------------------------------------------------------------------------
warnings.filterwarnings("ignore", category=DeprecationWarning)

# -------------------------------------------------------------------------------------------------------------------------------
# Global Variables
# -------------------------------------------------------------------------------------------------------------------------------
Error_List = []
Log_Folder = "./Log"
Log_File = "Gluonix_Error.log"
Error_Log = True
Root = False

# -------------------------------------------------------------------------------------------------------------------------------
# Error Log
# -------------------------------------------------------------------------------------------------------------------------------
def Error(E):
    global Error_List, Error_Display
    Error_Time = int(time.time())
    Error_List.append([E, Error_Time])
    if Error_Log:
        if not os.path.exists(Log_Folder):
            os.makedirs(Log_Folder)
        Log_Path = os.path.join(Log_Folder, Log_File)
        Date = datetime.datetime.fromtimestamp(Error_Time)
        Date = Date.strftime("%Y-%m-%d %H:%M:%S")
        Line = f"{Date} - {E}"
        File_Content = []
        if os.path.exists(Log_Path):
            with open(Log_Path, "r") as File:
                File_Content = File.readlines()
            if len(File_Content) >= 10000:
                File_Content.pop()
        with open(Log_Path, "w") as File:
            File.write(Line.rstrip("\r\n") + "\n")
            File.writelines(File_Content)
            
# -------------------------------------------------------------------------------------------------------------------------------
# Relative Path
# -------------------------------------------------------------------------------------------------------------------------------

def File(Name):
    try:
        Base_Dir = os.path.dirname(os.path.abspath(__file__))
        Path = os.path.join(Base_Dir, "Data", "File", f"{Name}")
        if os.path.exists(Path):
            return Path
        else:
            return ""
    except Exception as E:
        Error("Image -> " + str(E))

def Data(Name):
    try:
        Base_Dir = os.path.dirname(os.path.abspath(__file__))
        Path = os.path.join(Base_Dir, "Data", f"{Name}")
        if os.path.exists(Path):
            return Path
        else:
            return ""
    except Exception as E:
        Error("Data -> " + str(E))
        
# -------------------------------------------------------------------------------------------------------------------------------
# Database
# -------------------------------------------------------------------------------------------------------------------------------
Database = Gluonix.SQL(Data('NGD.dll'))

# -------------------------------------------------------------------------------------------------------------------------------
# Database Variables
# -------------------------------------------------------------------------------------------------------------------------------
Variable_Data = {}
Variable_Data_Temp = Database.Get("SELECT * FROM `Variable`", Keys=True)
for Each in Variable_Data_Temp:
        Variable_Data[Each['ID']] = Each['Data']

try:
    Error_Log = bool(int(Variable_Data['Error_Log']))
except:
    Error_Log = True

# -------------------------------------------------------------------------------------------------------------------------------
# Global Functions
# -------------------------------------------------------------------------------------------------------------------------------

def Error_Clear():
    try:
        global Error_List
        Error_List = []
    except Exception as E:
        Error("Error_Clear -> " + str(E))
        
def Load(Global):
    try:
        Display = Database.Get(f"SELECT * FROM `Display` WHERE `ID`='Root'", Keys=True)
        if len(Display)==1:
            Display = Display[0]
            Global[Display['ID']] = Gluonix.GUI()
            Temp_Root = Global[Display['ID']]
            Temp_Root.Config(Error_Log=Error_Log)
            Temp_Root.Config(Width=int(Display['Width']), Height=int(Display['Height']), Left=int(Display['Left']), Top=int(Display['Top']))
            Temp_Root.Config(Title=Display['Title'], Background=Display['Background'], Icon=File(Variable_Data['Icon']), Resizable=bool(int(Display['Resizable'])))
            Temp_Root.Config(Persistent=bool(int(Display['Persistent'])), Full_Screen=bool(int(Display['Full_Screen'])), Toolbar=bool(int(Display['Toolbar'])), Alignment=Display['Alignment'], Menu_Enable=bool(int(Display['Menu'])))
            Temp_Root.Create()
            Temp_Root.Hide()
            Load_Child(Display['ID'], Temp_Root, Global)
    except Exception as E:
        Error("Load -> "+str(E))
        
def Load_Child(Parent, Root, Global):
    try:
        Widgets = Database.Get(f"SELECT * FROM `Widget` WHERE `Root`='{Parent}'", Keys=True)
        for Widget in Widgets:
            if Widget['Type']=='Image':
                if bool(Widget['Interactive']):
                    Temp_Class = getattr(Gluonix, "Image_Zoom")
                else:
                    Temp_Class = getattr(Gluonix, f"{Widget['Type']}")
            else:
                Temp_Class = getattr(Gluonix, f"{Widget['Type']}")
            Temp_Widget = Temp_Class(Root)
            if Widget['Alignment']=='Percentage':
                Fixture = Root.Locate(Widget['Width'], Widget['Height'], Widget['Left'], Widget['Top'])
            else:
                Fixture = [Widget['Width'], Widget['Height'], Widget['Left'], Widget['Top']]
            Temp_Widget.Config(Name=Widget['Name'])
            Temp_Widget.Config(Width=Fixture[0], Height=Fixture[1], Left=Fixture[2], Top=Fixture[3])
            if Widget['Background']=='False':
                Temp_Widget.Config(Background=False)
            else:
                Temp_Widget.Config(Background=Widget['Background'])
            Temp_Widget.Config(Foreground=Widget['Foreground'], Border_Size=Widget['Border_Size'], Border_Color=Widget['Border_Color'], Radius=Widget['Radius'], Display=bool(Widget['Display']), Disable=bool(Widget['Disabled']))
            Temp_Widget.Config(Font_Size=Widget['Font_Size'], Font_Weight=Widget['Font_Weight'], Font_Family=Widget['Font_Family'], Align=Widget['Align'], Value=Widget['Value'])
            Temp_Widget.Config(Shadow_Size=Widget['Shadow_Size'], Shadow_Color=Widget['Shadow_Color'], Shadow_Full=Widget['Shadow_Full'])
            Temp_Widget.Config(Resize=True, Move=True)
            Temp_Widget.Config(Resize_Width=bool(Widget['Resize_Width']), Resize_Height=bool(Widget['Resize_Height']))
            Temp_Widget.Config(Move_Left=bool(Widget['Move_Left']), Move_Top=bool(Widget['Move_Top']))
            Temp_Widget.Config(Progress=Widget['Progress'], Zero=Widget['Zero'], Increment=Widget['Increment'], Mimimum=Widget['Minimum'], Maximum=Widget['Maximum'])
            Temp_Widget.Config(Path=File(Widget['ID']))
            Temp_Widget.Config(Url=bool(Widget['Url']), Transparent=bool(Widget['Transparent']), Rotate=Widget['Rotate'], Compound=Widget['Compound'], Aspect_Ratio=bool(Widget['Aspect_Ratio']))
            Temp_Widget.Config(Secure=Widget['Secure'])
            Temp_Widget.Config(Orient=Widget['Orient'], Ridge=Widget['Ridge'], Height_List=Widget['Height_List'])
            Temp_Widget.Create()
        Items = Database.Get(f"SELECT * FROM `Item` WHERE `Root`='{Parent}'", Keys=True)
        for Item in Items:
            Temp_Class = getattr(Gluonix, f"{Item['Type']}")
            Temp_Item = Temp_Class(Root)
            Fixture = [Item['Width'], Item['Height'], Item['Left'], Item['Top']]
            Temp_Item.Config(Name=Item['Name'])
            Temp_Item.Config(Width=Fixture[0], Height=Fixture[1], Left=Fixture[2], Top=Fixture[3], Radius=Item['Radius'])
            Temp_Item.Config(Start=Item['Start'], Extent=Item['Extent'])
            Temp_Item.Config(Size=Item['Size'], Weight=Item['Weight'], Font=Item['Font'], Value=Item['Value'])
            Temp_Item.Config(Thickness=Item['Thickness'], Fill=Item['Fill'], Outline=Item['Outline'])
            Temp_Item.Config(Justify=Item['Justify'], Anchor=Item['Anchor'])
            Temp_Item.Config(Resize=bool(Item['Resize']), Move=bool(Item['Move']))
            Temp_Item.Config(Url=bool(Item['Url']), Array=bool(Item['Array']), Pil=bool(Item['Pil']), Transparent=bool(Item['Transparent']), Rotate=Item['Rotate'], Aspect_Ratio=bool(Item['Aspect_Ratio']))
            Temp_Item.Config(Path=File(Item['ID']))
            Temp_Item.Create()
        Frames = Database.Get(f"SELECT * FROM `Frame` WHERE `Root`='{Parent}'", Keys=True)
        for Frame in Frames:
            Temp_Class = getattr(Gluonix, f"{Frame['Type']}")
            Temp_Frame = Temp_Class(Root)
            if Frame['Alignment']=='Percentage':
                Fixture = Root.Locate(Frame['Width'], Frame['Height'], Frame['Left'], Frame['Top'])
            else:
                Fixture = [Frame['Width'], Frame['Height'], Frame['Left'], Frame['Top']]
            Temp_Frame.Config(Name=Frame['Name'])
            Temp_Frame.Config(Width=Fixture[0], Height=Fixture[1], Left=Fixture[2], Top=Fixture[3])
            if Frame['Background']=='False':
                Temp_Frame.Config(Background=False)
            else:
                Temp_Frame.Config(Background=Frame['Background'])
            Temp_Frame.Config(Border_Size=Frame['Border_Size'], Border_Color=Frame['Border_Color'], Radius=Frame['Radius'], Display=bool(Frame['Display']))
            Temp_Frame.Config(Shadow_Size=Frame['Shadow_Size'], Shadow_Color=Frame['Shadow_Color'], Shadow_Full=Frame['Shadow_Full'])
            Temp_Frame.Config(Resize=True, Move=True)
            Temp_Frame.Config(Resize_Width=bool(Frame['Resize_Width']), Resize_Height=bool(Frame['Resize_Height']))
            Temp_Frame.Config(Move_Left=bool(Frame['Move_Left']), Move_Top=bool(Frame['Move_Top']))
            Temp_Frame.Create()
            Load_Child(Frame['ID'], Temp_Frame, Global)
    except Exception as E:
        Error("Load_Child -> "+str(E))
        
def Create_Popup(Display):
    try:
        Global = globals()
        if isinstance(Display, int):
            Display = str(Display)
        if Display.isdigit:
            Display = 'Popup'+Display
        Display = Database.Get(f"SELECT * FROM `Display` WHERE `ID`='{Display}'", Keys=True)
        if len(Display)==1:
            Display = Display[0]
            Temp_Popup = Gluonix.Popup(Global['Root'])
            Temp_Popup.Config(Width=int(Display['Width']), Height=int(Display['Height']), Left=int(Display['Left']), Top=int(Display['Top']))
            Temp_Popup.Config(Title=Display['Title'], Background=Display['Background'], Icon=File(Variable_Data['Icon']), Resizable=bool(int(Display['Resizable'])))
            Temp_Popup.Config(Persistent=bool(int(Display['Persistent'])), Full_Screen=bool(int(Display['Full_Screen'])), Toolbar=bool(int(Display['Toolbar'])), Alignment=Display['Alignment'], Topmost=bool(int(Display['Topmost'])), Menu_Enable=bool(int(Display['Menu'])))
            Temp_Popup.Create()
            Load_Child(Display['ID'], Temp_Popup, Global)
            Temp_Popup.Show()
            return Temp_Popup
    except Exception as E:
        Error("Create_Popup -> "+str(E))
        
def Cleanup():
    try:
        global Database
        Database.Close()
    except Exception as E:
        Error("Close -> "+str(E))
        
atexit.register(Cleanup)

# -------------------------------------------------------------------------------------------------------------------------------
# GUI
# -------------------------------------------------------------------------------------------------------------------------------

Load(globals())
Root.Popup = Create_Popup
Root.Show()


################################################################################################################################
# Programming End
################################################################################################################################