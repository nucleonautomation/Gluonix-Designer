import tkinter as TK
import tkinter.font as TK_Font
from .N_GUI import GUI

class Menu:

    def __init__(self, Main, *Args, **Kwargs):
        self._GUI = GUI._Instance
        if self._GUI is not None:
            self._Type = "Menu"
            try:
                self._Main = Main
                self._Config = ['Layout', 'Disable', 'Font_Size', 'Font_Weight', 'Font_Family', 'Foreground', 'Background', 'Active_Foreground', 'Active_Background', 'Tearoff']
                self._Layout = {}
                self._Disable = False
                self._Font_Size = 12
                self._Font_Weight = 'normal'
                self._Font_Family = 'Helvetica'
                self._Foreground = '#000000'
                self._Background = '#ffffff'
                self._Active_Foreground = '#000000'
                self._Active_Background = '#d9d9d9'
                self._Tearoff = 0
                self._Font = False
                self._Menu = False
                self._Initialized = False
                self.Create()
            except Exception as E:
                self._GUI.Error(f"{self._Type} -> Init -> {E}")
        else:
            print("Error: Gluonix -> GUI Instance Has Not Been Created")

    def __str__(self):
        return "Nucleon_Glunoix_Menu[]"

    def __repr__(self):
        return "Nucleon_Glunoix_Menu[]"

    def _Resolve_Master(self):
        try:
            if hasattr(self._Main, "_Frame"):
                return self._Main._Frame
            if hasattr(self._Main, "_Widget"):
                return self._Main._Widget
            return self._Main
        except Exception as E:
            self._GUI.Error(f"{self._Type} -> _Resolve_Master -> {E}")

    def _Empty_Command(self):
        try:
            return None
        except Exception as E:
            self._GUI.Error(f"{self._Type} -> _Empty_Command -> {E}")

    def _Wrap_Command(self, Value):
        try:
            if callable(Value):
                return lambda Value=Value: Value()
            return lambda Value=Value: Value
        except Exception as E:
            self._GUI.Error(f"{self._Type} -> _Wrap_Command -> {E}")

    def _Apply_Style(self, Menu_Widget):
        try:
            self._Font = TK_Font.Font(family=self._Font_Family, size=self._Font_Size, weight=self._Font_Weight)
            Menu_Widget.config(font=self._Font, fg=self._Foreground, bg=self._Background, activeforeground=self._Active_Foreground, activebackground=self._Active_Background, tearoff=self._Tearoff)
        except Exception as E:
            self._GUI.Error(f"{self._Type} -> _Apply_Style -> {E}")

    def _Reset_Menu(self):
        try:
            if self._Menu:
                self._Menu.destroy()
            Master = self._Resolve_Master()
            self._Menu = TK.Menu(Master, tearoff=self._Tearoff)
            self._Apply_Style(self._Menu)
        except Exception as E:
            self._GUI.Error(f"{self._Type} -> _Reset_Menu -> {E}")

    def _Build_Menu(self, Menu_Widget, Layout):
        try:
            for Key, Value in Layout.items():
                if isinstance(Key, str) and len(Key)>1 and Key[0]=='S' and Key[1:].isdigit():
                    Menu_Widget.add_separator()
                elif isinstance(Value, dict):
                    if len(Value)==0:
                        Menu_Widget.add_command(label=str(Key), command=lambda: self._Empty_Command())
                    else:
                        Sub_Menu = TK.Menu(Menu_Widget, tearoff=self._Tearoff)
                        self._Apply_Style(Sub_Menu)
                        self._Build_Menu(Sub_Menu, Value)
                        Menu_Widget.add_cascade(label=str(Key), menu=Sub_Menu)
                else:
                    if Value in ['', None, False]:
                        Menu_Widget.add_command(label=str(Key), command=lambda: self._Empty_Command())
                    else:
                        Menu_Widget.add_command(label=str(Key), command=self._Wrap_Command(Value))
        except Exception as E:
            self._GUI.Error(f"{self._Type} -> _Build_Menu -> {E}")

    def _Rebuild(self):
        try:
            self._Reset_Menu()
            if isinstance(self._Layout, dict):
                self._Build_Menu(self._Menu, self._Layout)
        except Exception as E:
            self._GUI.Error(f"{self._Type} -> _Rebuild -> {E}")

    def Create(self):
        try:
            self._Rebuild()
            self._Initialized = True
        except Exception as E:
            self._GUI.Error(f"{self._Type} -> Create -> {E}")

    def Delete(self):
        try:
            if self._Menu:
                self._Menu.destroy()
                self._Menu = False
            if self:
                del self
        except Exception as E:
            self._GUI.Error(f"{self._Type} -> Delete -> {E}")

    def Set(self, Value=False):
        try:
            if Value is not False:
                self._Layout = Value if isinstance(Value, dict) else {}
                if self._Initialized:
                    self._Rebuild()
            return self._Layout
        except Exception as E:
            self._GUI.Error(f"{self._Type} -> Set -> {E}")

    def Get(self):
        try:
            return self._Layout
        except Exception as E:
            self._GUI.Error(f"{self._Type} -> Get -> {E}")

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
            if self._Initialized and Run:
                self._Rebuild()
        except Exception as E:
            self._GUI.Error(f"{self._Type} -> Config -> {E}")

    def Open(self, Left=False, Top=False, Widget=False, Event=False):
        try:
            if self._Disable or not self._Menu:
                return False
            if self._Menu.index("end") is None:
                return False
            if Event is not False:
                Left = Event.x_root
                Top = Event.y_root
            elif Widget is not False:
                Widget._Widget.update_idletasks()
                if Left is False:
                    Left = Widget._Widget.winfo_rootx()+Widget._Widget.winfo_width()
                if Top is False:
                    Top = Widget._Widget.winfo_rooty()
            else:
                Master = self._Resolve_Master()
                Master.update_idletasks()
                if Left is False:
                    Left = Master.winfo_rootx()+Master.winfo_width()
                if Top is False:
                    Top = Master.winfo_rooty()
            try:
                self._Menu.tk_popup(int(Left), int(Top))
            finally:
                self._Menu.grab_release()
            return True
        except Exception as E:
            self._GUI.Error(f"{self._Type} -> Open -> {E}")

    def Close(self):
        try:
            if self._Menu:
                self._Menu.unpost()
            return True
        except Exception as E:
            self._GUI.Error(f"{self._Type} -> Close -> {E}")