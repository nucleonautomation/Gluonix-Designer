################################################################################################################################
#Stock_Circle
################################################################################################################################
import inspect
import time
import random
import string

class Stock_Canvas_Circle:
    def __init__(self, Global, Stock, Left, Top):
        try:
            self.Global = Global
            self.Stock = Stock
            self.Widget= []
            self.Type = 'Canvas_Circle'
            
            #Label
            Fixture = self.Stock.Scroll.Locate(30, 5, Left, Top)
            self.Label = self.Global['Gluonix'].Compound(self.Stock.Scroll)
            self.Label.Config(Width=Fixture[0], Height=Fixture[1], Left=Fixture[2], Top=Fixture[3])
            self.Label.Config(Background='#FFFFFF', Border_Size=1, Border_Color='#adadad', Display=True)
            self.Label.Config(Foreground='#000000', Font_Size=11, Font_Weight='normal', Align='center', Compound='left')
            self.Label.Config(Resize=True, Move=True)
            self.Label.Bind(On_Hover_In=lambda E: self.Label.Config(Border_Color='#0078d7', Background='#d5dcf0'))
            self.Label.Bind(On_Hover_Out=lambda E: self.Label.Config(Border_Color='#adadad', Background='#FFFFFF'))
            self.Label.Bind(On_Click=lambda E: self.On_Click())
            self.Label.Create()
            self.Label.Set(Path=self.Global['Image'](self.Type), Value=' Circle')
            self.Stock.Widget.append(self.Label)
            
        except Exception as E:
            self.Global['Error'](__class__.__name__+" -> "+inspect.currentframe().f_code.co_name+" -> "+str(E))
            
    def On_Click(self):
        try:
            ID_List = self.Stock.Design.Element.Tree.Get()
            if not ID_List:
                Root_ID = self.Stock.Design.Element.Parent
                Root_Type = 'Frame'
                Root_Level = 0
            else:
                Root_ID = ID_List[0]
                Root_Type = ID_List[1]
                Root_Level = ID_List[2]
            Level = Root_Level+1
            if (Root_Type!='Canvas' and Root_Type!='Scroll'):
                Widget = self.Stock.Design.Database.Get(f"SELECT * FROM `Widget` WHERE `ID`='{Root_ID}'", Keys=True)
                if len(Widget)==0:
                    Widget = self.Stock.Design.Database.Get(f"SELECT * FROM `Item` WHERE `ID`='{Root_ID}'", Keys=True)
                if len(Widget)==0:
                    Widget = self.Stock.Design.Database.Get(f"SELECT * FROM `Frame` WHERE `ID`='{Root_ID}'", Keys=True)
                Root_ID = Widget[0]['Root']
                Level = Root_Level
                Root_Container = self.Stock.Design.Database.Get(f"SELECT * FROM `Frame` WHERE `ID`='{Root_ID}'", Keys=True)
                if len(Root_Container)>0:
                    Root_Type = Root_Container[0]['Type']
                else:
                    Root_Type = 'Frame'
            if  Root_Type=='Canvas' or Root_Type=='Scroll':
                Number = 1
                Exist = self.Stock.Design.Database.Get(f"SELECT * FROM `Item` WHERE (`Name`='{self.Type}{Number}' AND `Root`='{Root_ID}')")
                while len(Exist)>0:
                    Number += 1
                    Exist = self.Stock.Design.Database.Get(f"SELECT * FROM `Item` WHERE (`Name`='{self.Type}{Number}' AND `Root`='{Root_ID}')")
                Name = f"{self.Type.replace('Canvas_', '')}{Number}"
                Random_Letter = ''.join(random.choices(string.ascii_letters, k=10))
                ID = Random_Letter+self.Global['Custom'].MD5(Root_ID+Name+str(time.time()*1000000))
                Root = getattr(self.Stock.Design.Element, Root_ID)
                Image = self.Global['Image'](self.Type)
                setattr(self.Stock.Design.Element, ID, self.Stock.Design.Element.Tree.Add(Name=f' {Name}', Parent=Root, Value=[ID, self.Type, Level], Path=Image))
                self.Stock.Design.Element.Tree.Expand(Root)
                ID_Tree = getattr(self.Stock.Design.Element, ID)
                self.Stock.Design.Element.Tree.Select(ID_Tree)
                self.Stock.Design.Database.Post(f"INSERT INTO `Item` (`ID`, `Name`, `Type`, `Root`, `Left`, `Top`) VALUES ('{ID}', '{Name}', '{self.Type}', '{Root_ID}', '40', '40')")
                self.Create(ID)
                self.Stock.Design.Configure.Hide_All()
                Configure = getattr(self.Stock.Design.Configure, f'Configure_{self.Type}')
                Configure.Load(ID)
            else:
                self.Global['Message'].Show('Error', 'Select A Canvas / Scroll')
                self.Global['Message'].Hide(Delay=2)
        except Exception as E:
            self.Global['Error'](__class__.__name__+" -> "+inspect.currentframe().f_code.co_name+" -> "+str(E))
            
    def Create(self, ID=False):
        try:
            if ID:
                Widget_Data = self.Stock.Design.Database.Get(f"SELECT * FROM `Item` WHERE `ID`='{ID}'", Keys=True)
                if len(Widget_Data)==1:
                    Widget_Data = Widget_Data[0]
                    Temp_Root = Widget_Data['Root']
                    Root = Temp_Root
                    while Temp_Root!=self.Stock.Design.Element.Parent:
                        Widget_Data = self.Stock.Design.Database.Get(f"SELECT * FROM `Frame` WHERE `ID`='{Temp_Root}'", Keys=True)
                        if len(Widget_Data)==1:
                            Widget_Data = Widget_Data[0]
                            Temp_Root = Widget_Data['Root']
                            Root = Temp_Root+'.'+Root
                        else:
                            break
                    Root = self.Global['Custom'].Get_Attr_Class(self.Stock.Design, Root)
                    setattr(Root, ID, self.Global['Gluonix'].Canvas_Circle(Root))
                    Widget_Data = self.Stock.Design.Database.Get(f"SELECT * FROM `Item` WHERE `ID`='{ID}'", Keys=True)
                    Widget_Data = Widget_Data[0]
                    Fixture = [Widget_Data['Width'], Widget_Data['Height'], Widget_Data['Left'], Widget_Data['Top']]
                    Widget = getattr(Root, ID)
                    Widget._ID = ID
                    Widget.Config(Width=Fixture[0], Height=Fixture[1], Left=Fixture[2], Top=Fixture[3], Radius=Widget_Data['Radius'])
                    Widget.Config(Size=Widget_Data['Size'], Weight=Widget_Data['Weight'], Font=Widget_Data['Font'], Value=Widget_Data['Value'])
                    Widget.Config(Thickness=Widget_Data['Thickness'], Fill=Widget_Data['Fill'], Outline=Widget_Data['Outline'])
                    Widget.Config(Justify=bool(Widget_Data['Justify']), Anchor=bool(Widget_Data['Anchor']))
                    Widget.Config(Resize=bool(Widget_Data['Resize']), Move=bool(Widget_Data['Move']))
                    Widget.Config(Path=f"{self.Stock.Design.Project_Path}/Data/File/{ID}")
                    Widget.Config(Url=bool(Widget_Data['Url']), Transparent=bool(Widget_Data['Transparent']), Rotate=Widget_Data['Rotate'], Aspect_Ratio=bool(Widget_Data['Aspect_Ratio']))
                    Widget.Lock = bool(Widget_Data['Lock'])
                    Widget.Create()
                    self.Stock.Design.Element.Intractive(Widget)
        except Exception as E:
            self.Global['Error'](__class__.__name__+" -> "+inspect.currentframe().f_code.co_name+" -> "+str(E))