################################################################################################################################
#Stock_Canvas
################################################################################################################################
import inspect
import time
import random
import string

class Stock_Canvas:
    def __init__(self, Global, Stock, Left, Top):
        try:
            self.Global = Global
            self.Stock = Stock
            self.Widget= []
            self.Type = 'Canvas'
            
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
            self.Label.Set(Path=self.Global['Image'](self.Type), Value=' Canvas')
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
            if (Root_Type!='Frame' and Root_Type!='Canvas' and Root_Type!='Scroll'):
                Widget = self.Stock.Design.Database.Get(f"SELECT * FROM `Widget` WHERE `ID`='{Root_ID}'", Keys=True)
                if len(Widget)==0:
                    Widget = self.Stock.Design.Database.Get(f"SELECT * FROM `Item` WHERE `ID`='{Root_ID}'", Keys=True)
                Root_ID = Widget[0]['Root']
                Level = Root_Level
            Number = 1
            Exist = self.Stock.Design.Database.Get(f"SELECT * FROM `Frame` WHERE (`Name`='{self.Type}{Number}' AND `Root`='{Root_ID}')")
            while len(Exist)>0:
                Number += 1
                Exist = self.Stock.Design.Database.Get(f"SELECT * FROM `Frame` WHERE (`Name`='{self.Type}{Number}' AND `Root`='{Root_ID}')")
            Name = f'{self.Type}{Number}'
            Random_Letter = ''.join(random.choices(string.ascii_letters, k=10))
            ID = Random_Letter+self.Global['Custom'].MD5(Root_ID+Name+str(time.time()*1000000))
            Root = getattr(self.Stock.Design.Element, Root_ID)
            Image = self.Global['Image'](self.Type)
            setattr(self.Stock.Design.Element, ID, self.Stock.Design.Element.Tree.Add(Name=f' {Name}', Parent=Root, Value=[ID, self.Type, Level], Path=Image))
            self.Stock.Design.Element.Tree.Expand(Root)
            ID_Tree = getattr(self.Stock.Design.Element, ID)
            self.Stock.Design.Element.Tree.Select(ID_Tree)
            self.Stock.Design.Database.Post(f"INSERT INTO `Frame` (`ID`, `Name`, `Type`, `Level`, `Root`, `Alignment`) VALUES ('{ID}', '{Name}', '{self.Type}', '{Level}', '{Root_ID}', '{self.Stock.Design.Alignment}')")
            self.Create(ID)
            self.Stock.Design.Configure.Hide_All()
            Configure = getattr(self.Stock.Design.Configure, f'Configure_{self.Type}')
            Configure.Load(ID)
        except Exception as E:
            self.Global['Error'](__class__.__name__+" -> "+inspect.currentframe().f_code.co_name+" -> "+str(E))
            
    def Create(self, ID=False):
        try:
            if ID:
                Frame_Data = self.Stock.Design.Database.Get(f"SELECT * FROM `Frame` WHERE `ID`='{ID}'", Keys=True)
                if len(Frame_Data)==1:
                    Frame_Data = Frame_Data[0]
                    Temp_Root = Frame_Data['Root']
                    Root = Temp_Root
                    while Temp_Root!=self.Stock.Design.Element.Parent:
                        Frame_Data = self.Stock.Design.Database.Get(f"SELECT * FROM `Frame` WHERE `ID`='{Temp_Root}'", Keys=True)
                        if len(Frame_Data)==1:
                            Frame_Data = Frame_Data[0]
                            Temp_Root = Frame_Data['Root']
                            Root = Temp_Root+'.'+Root
                        else:
                            break
                    Root = self.Global['Custom'].Get_Attr_Class(self.Stock.Design, Root)
                    setattr(Root, ID, self.Global['Gluonix'].Canvas(Root))
                    Frame_Data = self.Stock.Design.Database.Get(f"SELECT * FROM `Frame` WHERE `ID`='{ID}'", Keys=True)
                    Frame_Data = Frame_Data[0]
                    if Frame_Data['Alignment']=='Percentage':
                        Fixture = Root.Locate(Frame_Data['Width'], Frame_Data['Height'], Frame_Data['Left'], Frame_Data['Top'])
                    else:
                        Fixture = [Frame_Data['Width'], Frame_Data['Height'], Frame_Data['Left'], Frame_Data['Top']]
                    Frame = getattr(Root, ID)
                    Frame._ID = ID
                    Frame.Config(Width=Fixture[0], Height=Fixture[1], Left=Fixture[2], Top=Fixture[3])
                    if Frame_Data['Background']=='False':
                        Frame.Config(Background=False)
                    else:
                        Frame.Config(Background=Frame_Data['Background'])
                    Frame.Config(Border_Size=Frame_Data['Border_Size'], Border_Color=Frame_Data['Border_Color'], Radius=Frame_Data['Radius'], Display=True)
                    Frame.Config(Shadow_Size=Frame_Data['Shadow_Size'], Shadow_Color=Frame_Data['Shadow_Color'], Shadow_Full=Frame_Data['Shadow_Full'])
                    Frame.Config(Resize=True, Move=True)
                    Frame.Config(Resize_Width=bool(Frame_Data['Resize_Width']), Resize_Height=bool(Frame_Data['Resize_Height']))
                    Frame.Config(Move_Left=bool(Frame_Data['Move_Left']), Move_Top=bool(Frame_Data['Move_Top']))
                    Frame.Lock = bool(Frame_Data['Lock'])
                    Frame.Create()
                    self.Stock.Design.Element.Intractive(Frame)
        except Exception as E:
            self.Global['Error'](__class__.__name__+" -> "+inspect.currentframe().f_code.co_name+" -> "+str(E))