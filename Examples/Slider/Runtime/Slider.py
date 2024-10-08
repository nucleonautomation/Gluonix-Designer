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


class Slider():

    def __init__(self, Bar, Frame):
        self._Config = ['Minimum', 'Maximum', 'Increment']
        self._Bind = ['On_Change']
        self._Bar = Bar
        self._Frame = Frame
        self._On_Change = False
        self._Minimum = 0
        self._Maximum = 100
        self._Increment = 1
        self._Bar.Set(0)
        self._Frame.Bind(On_Click=lambda E: self.Progress_Start(E), On_Drag=lambda E: self.Progress(E), On_Release=lambda E: self.On_Change())
        Bar_Data = self._Bar.Config_Get('Left', 'Width')
        Minimum = Bar_Data['Left']
        self._Frame.Config(Left=Minimum)
        self._Frame.Show()
        
    def On_Change(self):
        if self._On_Change:
            self._On_Change()
        
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
                
    def Bind(self, **Input):
        for Each in self._Bind:
            if Each in Input:
                Value = Input[Each]
                setattr(self, "_"+Each, Value)
        
    def Get(self):
        Progress = self._Bar.Get()
        Range  = self._Maximum - self._Minimum
        Value = self._Minimum + (Progress / 100.0) * Range
        Value = round(Value / self._Increment) * self._Increment
        return Value
        
    def Set(self, Value):
        Range  = self._Maximum - self._Minimum
        Value = (Value - self._Minimum) / Range
        Value = Value * 100.0
        self._Bar.Set(Value)
        Bar_Data = self._Bar.Config_Get('Left', 'Width')
        Frame_Data = self._Frame.Config_Get('Left', 'Width')
        Minimum = Bar_Data['Left']
        Maximum = Bar_Data['Left']+Bar_Data['Width']-Frame_Data['Width']
        Frame_Left = Bar_Data['Left']+((Maximum-Minimum)*(Value/100))
        self._Frame.Config(Left=Frame_Left)

    def Progress_Start(self, E):
        self._Start = E.x

    def Progress(self, E):
        Frame_Data = self._Frame.Config_Get('Left', 'Width')
        Frame_Left = Frame_Data['Left'] + E.x - self._Start
        Bar_Data = self._Bar.Config_Get('Left', 'Width')
        Minimum = Bar_Data['Left']
        Maximum = Bar_Data['Left']+Bar_Data['Width']-Frame_Data['Width']
        Frame_Left = max(Minimum, min(Frame_Left, Maximum))
        Bar_Progress = (Frame_Left-Bar_Data['Left'])/(Maximum-Minimum)*100
        self._Bar.Set(Bar_Progress)
        self._Frame.Config(Left=Frame_Left)
        self.On_Change()
        
def Output():
    print(Slider1.Get())
    
Slider1 = Slider(Root.Bar, Root.Frame)
    
# -------------------------------------------------------------------------------------------------------------------------------
# Developer Programming End
# -------------------------------------------------------------------------------------------------------------------------------
#################################################################################################################################
#################################################################################################################################
Root.Start() ###!REQUIRED ------- Any Script After This Will Not Execute
#################################################################################################################################
