# -------------------------------------------------------------------------------------------------------------------------------
# Gluonix Runtime
# -------------------------------------------------------------------------------------------------------------------------------
#################################################################################################################################
from Nucleon.Runner import * ###!REQUIRED ------- Any Script Before This Won't Effect GUI Elements
#################################################################################################################################
#################################################################################################################################
# -------------------------------------------------------------------------------------------------------------------------------
# Developer Programming Start
# -------------------------------------------------------------------------------------------------------------------------------


class Button:
    def __init__(self, Canvas, Label):
        self._Config = ['Background', 'Background_Hover', 'Foreground', 'Foreground_Hover', 'Weight', 'Size', 'Value']
        self._Bind = ['On_Click', 'On_Release']
        self._Canvas = Canvas
        self._Canvas_Data = self._Label.Config_Get('Background')
        self._Label = Label
        self._Label_Data = self._Label.Config_Get('Background', 'Foreground', 'Font_Size', 'Font_Weight', 'Value')
        self._On_Click = False
        self._On_Release = False
        self._Background, self._Background_Hover = self._Canvas_Data['Background'], self._Canvas_Data['Background']
        self._Foreground, self._Foreground_Hover = self._Label_Data['Foreground'], self._Label_Data['Foreground']
        self._Weight = self._Label_Data['Font_Weight']
        self._Size = self._Label_Data['Font_Size']
        self._Value = self._Label_Data['Value']
        self._Canvas.Bind(On_Hover_In=lambda E: self.Hover_In())
        self._Canvas.Bind(On_Hover_Out=lambda E: self.Hover_Out())
        self._Canvas.Bind(On_Click=lambda E: self.Click())
        self._Canvas.Bind(On_Release=lambda E: self.Release())
        self._Label.Bind(On_Hover_In=lambda E: self.Hover_In())
        self._Label.Bind(On_Hover_Out=lambda E: self.Hover_Out())
        self._Label.Bind(On_Click=lambda E: self.Click())
        self._Label.Bind(On_Release=lambda E: self.Release())
        self.Update()
        
    def Config_Get(self, *Input):
        Return = {}
        for Each in self._Config:
            if Each in Input:
                Return[Each] = getattr(self, "_"+Each)
        return Return
                
    def Config(self, **Input):
        for Each in self._Config:
            if Each in Input:
                Value = Input[Each]
                setattr(self, "_"+Each, Value)
        self.Update()
                
    def Bind(self, **Input):
        for Each in self._Bind:
            if Each in Input:
                Value = Input[Each]
                setattr(self, "_"+Each, Value)
        
    def Set(self, Value):
        self._Value = Value
        self._Canvas.Label.Set(self._Value)
        
    def Update(self):
        self._Canvas.Config(Background=self._Background)
        self._Label.Config(Background=self._Background, Foreground=self._Foreground, Font_Weight=self._Weight, Font_Size=self._Size)
        self._Label.Set(self._Value)

    def Click(self):
        self._Canvas.Config(Background=self._Background)
        self._Label.Config(Background=self._Background, Foreground=self._Foreground)
        if self._On_Click:
            self._On_Click()

    def Release(self):
        self._Canvas.Config(Background=self._Background_Hover)
        self._Label.Config(Background=self._Background_Hover, Foreground=self._Foreground_Hover)
        if self._On_Release:
            self._On_Release()

    def Hover_In(self):
        self._Canvas.Config(Background=self._Background_Hover)
        self._Label.Config(Background=self._Background_Hover, Foreground=self._Foreground_Hover)

    def Hover_Out(self):
        self._Canvas.Config(Background=self._Background)
        self._Label.Config(Background=self._Background, Foreground=self._Foreground)
        
Button1 = Button(Root.Canvas1, Root.Canvas1.Label1)
Button1.Config(Background='#405cf4', Background_Hover='#191970')
Button1.Config(Foreground='#FFFFFF', Foreground_Hover='#FFFFFF')
Button1.Bind(On_Click = lambda : Button1_Click())

def Button1_Click():
    print('Button Pressed')

# -------------------------------------------------------------------------------------------------------------------------------
# Developer Programming End
# -------------------------------------------------------------------------------------------------------------------------------
#################################################################################################################################
#################################################################################################################################
Root.Start() ###!REQUIRED ------- Any Script After This Will Not Execute
#################################################################################################################################