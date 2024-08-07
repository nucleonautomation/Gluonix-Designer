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
    def __init__(self, Canvas):
        self._Config = ['Background', 'Background_Hover', 'Foreground', 'Foreground_Hover', 'Weight', 'Size', 'Value']
        self._Bind = ['On_Click', 'On_Release']
        self._Canvas = Canvas
        self._On_Click = False
        self._On_Release = False
        self._Background, self._Background_Hover = '#FFFFFF', '#FFFFFF'
        self._Foreground, self._Foreground_Hover = '#000000', '#000000'
        self._Weight = 'normal'
        self._Size = 20
        self._Value = 'CLICK'
        self._Canvas.Bind(On_Hover_In=lambda E: self.Hover_In())
        self._Canvas.Bind(On_Hover_Out=lambda E: self.Hover_Out())
        self._Canvas.Bind(On_Click=lambda E: self.Click())
        self._Canvas.Bind(On_Release=lambda E: self.Release())
        Canvas_Data = self._Canvas.Config_Get('Width', 'Height')
        self._Canvas.Label = self._Canvas.Text()
        self._Canvas.Label.Config(X=Canvas_Data['Width']/2, Y=Canvas_Data['Height']/2, Anchor='center', Color='white', Weight=self._Weight, Size=self._Size)
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
        self._Canvas.Label.Show()
        
    def Update(self):
        self._Canvas.Config(Background=self._Background)
        self._Canvas.Label.Config(Anchor='center', Color=self._Foreground, Weight=self._Weight, Size=self._Size)
        self._Canvas.Label.Set(self._Value)
        self._Canvas.Label.Show()

    def Click(self):
        self._Canvas.Config(Background=self._Background)
        self._Canvas.Label.Config(Color=self._Foreground)
        self._Canvas.Label.Show()
        if self._On_Click:
            self._On_Click()

    def Release(self):
        self._Canvas.Config(Background=self._Background_Hover)
        self._Canvas.Label.Config(Color=self._Foreground_Hover)
        self._Canvas.Label.Show()
        if self._On_Release:
            self._On_Release()

    def Hover_In(self):
        self._Canvas.Config(Background=self._Background_Hover)
        self._Canvas.Label.Config(Color=self._Foreground_Hover)
        self._Canvas.Label.Show()

    def Hover_Out(self):
        self._Canvas.Config(Background=self._Background)
        self._Canvas.Label.Config(Color=self._Foreground)
        self._Canvas.Label.Show()
        
Button1 = Button(Root.Canvas)
Button1.Config(Background='#405cf4', Background_Hover='#191970')
Button1.Config(Foreground='#FFFFFF', Foreground_Hover='#FFFFFF')
Button1.Config(Weight='bold', Size=15, Value='CLICK ME')
Button1.Config(On_Click = lambda : Button1_Click())

def Button1_Click():
    print('Button Pressed')

# -------------------------------------------------------------------------------------------------------------------------------
# Developer Programming End
# -------------------------------------------------------------------------------------------------------------------------------
#################################################################################################################################
#################################################################################################################################
Root.Start() ###!REQUIRED ------- Any Script After This Will Not Execute
#################################################################################################################################