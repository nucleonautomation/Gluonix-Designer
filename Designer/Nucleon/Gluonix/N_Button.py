# IMPORT LIBRARIES
from .N_GUI import GUI
from .N_Label import Label
from .N_Custom import Event_Bind

class Button(Label):

    def __init__(self, Main, *Args, **Kwargs):
        self._GUI = GUI._Instance
        if self._GUI is not None:
            self._Type = "Button"
            try:
                super().__init__(Main, *Args, **Kwargs)
                self._Config = ['Name', 'Auto_Dark', 'Background', 'Light_Background', 'Dark_Background', 'Foreground', 'Light_Foreground', 'Dark_Foreground', 'Border_Color', 'Light_Border_Color', 'Dark_Border_Color', 'Border_Size', 'Resize', 'Popup', 'Display', 'Left', 'Top', 'Width', 'Height', 'Animate_Left', 'Animate_Top', 'Animate_Width', 'Animate_Height', 'Animate_Time', 'Font_Size', 'Font_Weight', 'Font_Family', 'Align', 'Value', 'Hover_Background', 'Light_Hover_Background', 'Dark_Hover_Background', 'Hover_Foreground', 'Light_Hover_Foreground', 'Dark_Hover_Foreground', 'Hover_Border_Color', 'Light_Hover_Border_Color', 'Dark_Hover_Border_Color', 'Disable']
                self._Type = "Button"
                self._Disable = False
                Event_Bind(self._Widget, On_Click=lambda E: self.On_Click(E), On_Release=lambda E: self.On_Release(E))
            except Exception as E:
                self._GUI.Error(f"{self._Type} -> Init -> {E}")
        else:
            print("Error: Gluonix -> GUI Instance Has Not Been Created")

    def __str__(self):
        return "Nucleon_Glunoix_Button[]"

    def __repr__(self):
        return "Nucleon_Glunoix_Button[]"
            
    def Bind(self, **Input):
        try:
            if 'On_Show' in Input:
                self._On_Show = Input['On_Show']
            if 'On_Hide' in Input:
                self._On_Hide = Input['On_Hide']
            if 'On_Animate' in Input:
                self._On_Animate = Input['On_Animate']
            if 'On_Change' in Input:
                self._On_Change = Input['On_Change']
            Event_Bind(self._Widget, **Input)
        except Exception as E:
            self._GUI.Error(f"{self._Type} -> Bind -> {E}")
            
    def On_Click(self, E):
        try:
            if self._Disable or not self._Widget:
                return
            self._Widget.config(background=self._GUI.Fade(self._Background, 70), foreground=self._Foreground)
        except Exception as E:
            self._GUI.Error(f"{self._Type} -> On_Press -> {E}")
            
    def On_Release(self, E):
        try:
            if self._Disable or not self._Widget:
                return
            self._Widget.config(background=self._Background, foreground=self._Foreground)
        except Exception as E:
            self._GUI.Error(f"{self._Type} -> On_Release -> {E}")