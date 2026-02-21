import json
import math
import time
import tkinter as Tk
from .N_GUI import GUI

class Flowchart:
    
    def __init__(self, Canvas, *Args, **Kwargs):
        self._GUI = GUI._Instance
        if self._GUI is None:
            print("Error Gluonix - GUI Instance Has Not Been Created")
            return
        self._Type = "Flowchart"
        try:
            self._Canvas = Canvas
            self._Display = True
            self._Nodes = {}
            self._Edges = {}
            self._Item_To_Node = {}
            self._Item_To_Edge = {}
            self._Node_Id_Next = 1
            self._Edge_Id_Next = 1
            self._Selected_Node_Id = None
            self._Selected_Edge_Id = None
            self._Smooth_Edges = False
            self._Thickness = 2
            self._Selected_Thickness_Multiplier = 2.0
            self._Selected_Outline_Color = None
            self._Disabled_Nodes = {}
            self._Disabled_Edges = {}
            self._Locked_Nodes = {}
            self._Locked_Edges = {}
            self._Drag_Mode = "none"
            self._Drag_Node_Id = None
            self._Drag_Start_Pos = None
            self._Drag_Offset_X = 0.0
            self._Drag_Offset_Y = 0.0
            self._Pending_Connect = None
            self._Connect_Armed_Pos = None
            self._Connect_Start_Point = None
            self._Preview_Line_Item = None
            self._Preview_Port_Item = None
            self._Connect_Drag_Threshold = 6.0
            self._Last_Click_Time = 0.0
            self._Last_Click_Pos = None
            self._Double_Click_Threshold = 0.35
            self._Context_Menu_Items = []
            self._Context_Menu = None
            self._Callback = None
            self._Callback_Mode = "Continuous"
            self._Undo_Stack = []
            self._Redo_Stack = []
            self._Undo_Lock = False
            self._Undo_Limit = 200
            self._Copy_Buffer = None
            self._Scroll_Container = None
            self._H_Scrollbar = None
            self._V_Scrollbar = None
            self._Port_Radius = 6.0
            self._Port_Offset = 10.0
            self._Port_Clearance = 20.0
            self._Route_Grid = 10.0
            self._Route_Clearance = 20.0
            self._Auto_Scroll_Margin = 30.0
            self._Auto_Scroll_Step = 1
            self._Auto_Scroll_Interval = 0.08
            self._Last_Auto_Scroll_Time = 0.0
            self._Zoom_Value = 1.0
            self._Zoom_Min = 0.3
            self._Zoom_Max = 10.0
            self._Zoom_Step = 1.10
            self._Font_Title_Base = 10
            self._Font_Desc_Base  = 9
            self._Font_Field_Base = 9
            self._Input_Single_Edge = True
            self._Output_Single_Edge = True
            self._Reconnect_Edge_Id = None
            self._Reconnect_End = None
            self._Reconnect_Fixed = None
            self._Reconnect_Armed_Pos = None
            self._Reconnect_Start_Point = None
            self._Drag_Ghost_Item = None
            self._Drag_Ghost_Node_Id = None
            self._Drag_Ghost_Hidden_Items = []
            self._Drag_Ghost_Hidden_Edge_Items = []
            self.Bind()
            self.Attach_Scrollbars()
        except Exception as E:
            self._GUI.Error(f"{self._Type} - Init - {E}")

    def __str__(self):
        return "NucleonGluonixFlowchart"

    def __repr__(self):
        return "NucleonGluonixFlowchart"

    def __del__(self):
        try:
            self.Close()
        except:
            pass

    def Close(self):
        try:
            self.Clear()
        except Exception as E:
            self._GUI.Error(f"{self._Type} - Close - {E}")

    def Callback(self, Function, Mode = "Continuous"):
        try:
            self._Callback = Function
            if Mode in ["Release", "Continuous"]:
                self._Callback_Mode = Mode
            else:
                self._Callback_Mode = "Continuous"
        except Exception as E:
            self._GUI.Error(f"{self._Type} - Callback - {E}")

    def _Callback_Invoke(self, Type, ID = None, Event = "Update", Data = None):
        try:
            CB = getattr(self, "_Callback", None)
            if CB is None or not callable(CB):
                return
            Info = {"Type": str(Type), "Event": str(Event)}
            if ID is not None:
                Info["ID"] = ID
            if Data is None and ID is not None:
                if Type == "Node" or Type == "Object":
                    Data = self.Get_Node(ID)
                if Type == "Edge":
                    Data = self.Get_Edge(ID)
            if Data is not None:
                Info["Data"] = Data
            CB(Info)
        except Exception as E:
            self._GUI.Error(f"{self._Type} - _Callback_Invoke - {E}")

    def Bind(self):
        try:
            self._Canvas.Bind(On_Click = self.On_Click, On_Drag = self.On_Drag, On_Mouse_Wheel=self.Zoom, On_Release = self.On_Release, On_Resize = self.On_Resize, On_Motion = self.On_Motion, On_Right_Click = self.On_Right_Click)
        except Exception as E:
            self._GUI.Error(f"{self._Type} - Bind - {E}")

    def Canvas_Width(self):
        try:
            return float(self._Canvas._Frame.winfo_width())
        except:
            return 800.0

    def Canvas_Height(self):
        try:
            return float(self._Canvas._Frame.winfo_height())
        except:
            return 600.0

    def Smooth(self, Value = None):
        try:
            if Value is not None:
                self._Smooth_Edges = bool(Value)
            self.Render()
        except Exception as E:
            self._GUI.Error(f"{self._Type} - Thickness - {E}")

    def Thickness(self, Value = None, Selected_Multiplier = None, Selected_Outline_Color = None):
        try:
            if Value is not None:
                self._Thickness = float(Value)
            if Selected_Multiplier is not None:
                self._Selected_Thickness_Multiplier = float(Selected_Multiplier)
            if Selected_Outline_Color is not None:
                self._Selected_Outline_Color = str(Selected_Outline_Color)
            self.Render()
        except Exception as E:
            self._GUI.Error(f"{self._Type} - Thickness - {E}")

    def Attach_Scrollbars(self):
        try:
            if Tk is None:
                return
            Parent = getattr(self._Canvas, "_Frame", None)
            if Parent is None:
                return
            if self._H_Scrollbar is not None:
                try:
                    self._H_Scrollbar.destroy()
                except:
                    pass
            if self._V_Scrollbar is not None:
                try:
                    self._V_Scrollbar.destroy()
                except:
                    pass
            self._Scroll_Container = Parent
            self._H_Scrollbar = Tk.Scrollbar(Parent, orient = "horizontal")
            self._V_Scrollbar = Tk.Scrollbar(Parent, orient = "vertical")
            try:
                Parent.configure(xscrollcommand = self._H_Scrollbar.set, yscrollcommand = self._V_Scrollbar.set)
            except:
                pass
            try:
                self._H_Scrollbar.configure(command = Parent.xview)
                self._V_Scrollbar.configure(command = Parent.yview)
            except:
                pass
            try:
                Parent.bind("<Configure>", self._On_Canvas_Configure)
            except:
                pass
            self._Scrollbars_Reposition()
            self.Update_Scrollregion()
        except Exception as E:
            self._GUI.Error(f"{self._Type} - Attach_Scrollbars - {E}")

    def _On_Canvas_Configure(self, Event = None):
        try:
            self._Scrollbars_Reposition()
            self._Scrollbars_Update_Visibility()
        except Exception as E:
            self._GUI.Error(f"{self._Type} - _On_Canvas_Configure - {E}")

    def _Scrollbars_Reposition(self):
        try:
            if self._H_Scrollbar is None or self._V_Scrollbar is None:
                return
            T = float(getattr(self, "_Scrollbar_Thickness", 18.0))
            try:
                self._V_Scrollbar.place(relx = 1.0, x = 0, rely = 0.0, y = 0, relheight = 1.0, width = T, anchor = "ne")
            except:
                pass
            try:
                self._H_Scrollbar.place(relx = 0.0, x = 0, rely = 1.0, y = 0, relwidth = 1.0, height = T, anchor = "sw")
            except:
                pass
        except Exception as E:
            self._GUI.Error(f"{self._Type} - _Scrollbars_Reposition - {E}")

    def _Scrollbars_Update_Visibility(self):
        try:
            if self._H_Scrollbar is None or self._V_Scrollbar is None:
                return
            C = getattr(self._Canvas, "_Frame", None)
            if C is None:
                return
            ShowH = True
            ShowV = True
            try:
                X0, X1 = C.xview()
                if float(X0) <= 0.0 and float(X1) >= 1.0:
                    ShowH = False
            except:
                pass
            try:
                Y0, Y1 = C.yview()
                if float(Y0) <= 0.0 and float(Y1) >= 1.0:
                    ShowV = False
            except:
                pass
            if ShowH:
                try:
                    self._H_Scrollbar.place_configure()
                except:
                    pass
            else:
                try:
                    self._H_Scrollbar.place_forget()
                except:
                    pass
            if ShowV:
                try:
                    self._V_Scrollbar.place_configure()
                except:
                    pass
            else:
                try:
                    self._V_Scrollbar.place_forget()
                except:
                    pass
            if ShowH or ShowV:
                self._Scrollbars_Reposition()
        except Exception as E:
            self._GUI.Error(f"{self._Type} - _Scrollbars_Update_Visibility - {E}")

    def _Auto_Scroll_On_Drag(self, Event):
        try:
            Now = float(time.time())
            Interval = float(getattr(self, "_Auto_Scroll_Interval", 0.03))
            Last = float(getattr(self, "_Last_Auto_Scroll_Time", 0.0))
            if Now - Last < Interval:
                return
            self._Last_Auto_Scroll_Time = Now
            C = getattr(self._Canvas, "_Frame", None)
            if C is None:
                return
            Ex = float(getattr(Event, "x", 0.0))
            Ey = float(getattr(Event, "y", 0.0))
            W = float(max(1.0, C.winfo_width()))
            H = float(max(1.0, C.winfo_height()))
            Margin = float(getattr(self, "_Auto_Scroll_Margin", 40.0))
            Step = int(getattr(self, "_Auto_Scroll_Step", 1))
            Dx = 0
            Dy = 0
            if Ex < Margin:
                Dx = -Step
            if Ex > W - Margin:
                Dx = Step
            if Ey < Margin:
                Dy = -Step
            if Ey > H - Margin:
                Dy = Step
            if Dx != 0:
                try:
                    C.xview_scroll(int(Dx), "units")
                except:
                    pass
            if Dy != 0:
                try:
                    C.yview_scroll(int(Dy), "units")
                except:
                    pass
            if Dx != 0 or Dy != 0:
                self.Update_Scrollregion()
        except Exception as E:
            self._GUI.Error(f"{self._Type} - _Auto_Scroll_On_Drag - {E}")

    def Update_Scrollregion(self):
        try:
            try:
                B = self._Canvas._Frame.bbox("all")
            except:
                B = None
            CW = float(self.Canvas_Width())
            CH = float(self.Canvas_Height())
            if not B:
                try:
                    self._Canvas._Frame.configure(scrollregion = (0.0, 0.0, CW, CH))
                except:
                    pass
                self._Scrollbars_Update_Visibility()
                return
            X1, Y1, X2, Y2 = B
            Pad = float(max(60.0, float(getattr(self, "_Route_Clearance", 20.0)) * 2.0))
            X1 = float(X1) - Pad
            Y1 = float(Y1) - Pad
            X2 = float(X2) + Pad
            Y2 = float(Y2) + Pad
            X2 = max(X2, CW)
            Y2 = max(Y2, CH)
            try:
                self._Canvas._Frame.configure(scrollregion = (X1, Y1, X2, Y2))
            except:
                pass
            self._Scrollbars_Update_Visibility()
        except Exception as E:
            self._GUI.Error(f"{self._Type} - Update_Scrollregion - {E}")

    def _Context_Menu_Invoke(self, Function, Info):
        try:
            if Function is None or not callable(Function):
                return
            try:
                Function(Info)
            except TypeError:
                Function()
        except Exception as E:
            self._GUI.Error(f"{self._Type} - _Context_Menu_Invoke - {E}")

    def Context_Menu_Add(self, Label, Function, Type = ""):
        try:
            self._Context_Menu_Items.append({"Label": str(Label), "Function": Function, "Type": Type})
        except Exception as E:
            self._GUI.Error(f"{self._Type} - Context_Menu_Add - {E}")

    def _Drag_Ghost_Begin(self, ID):
        try:
            if ID not in self._Nodes:
                return
            self._Drag_Ghost_End()
            self._Drag_Ghost_Node_Id = int(ID)
            self._Drag_Ghost_Hidden_Items = []
            self._Drag_Ghost_Hidden_Edge_Items = []
            Rect = self._Node_Rect(int(ID))
            if Rect is None:
                return
            X1, Y1, X2, Y2 = Rect
            SX1 = float(self._Scale(X1))
            SY1 = float(self._Scale(Y1))
            SX2 = float(self._Scale(X2))
            SY2 = float(self._Scale(Y2))
            SWidth = max(1.0, float(self._Scale(float(self._Thickness))))
            outline = "#505050"
            fill = "#D0D0D0"
            try:
                self._Drag_Ghost_Item = self._Canvas._Frame.create_rectangle(
                    SX1, SY1, SX2, SY2,
                    outline=outline,
                    fill=fill,
                    width=SWidth
                )
            except:
                self._Drag_Ghost_Item = None
            if self._Drag_Ghost_Item is not None:
                try:
                    self._Canvas._Frame.tag_raise(self._Drag_Ghost_Item)
                except:
                    pass
        except Exception as E:
            self._GUI.Error(f"{self._Type} - _Drag_Ghost_Begin - {E}")

    def _Drag_Ghost_End(self):
        try:
            if self._Drag_Ghost_Item is not None:
                try:
                    self._Canvas._Frame.delete(self._Drag_Ghost_Item)
                except:
                    pass
            self._Drag_Ghost_Item = None
            self._Drag_Ghost_Node_Id = None
            self._Drag_Ghost_Hidden_Items = []
            self._Drag_Ghost_Hidden_Edge_Items = []
        except Exception as E:
            self._GUI.Error(f"{self._Type} - _Drag_Ghost_End - {E}")


    def _Drag_Ghost_Update(self, ID, NX, NY):
        try:
            if self._Drag_Ghost_Item is None or self._Drag_Ghost_Node_Id is None:
                return
            if int(self._Drag_Ghost_Node_Id) != int(ID):
                return
            N = self._Nodes.get(int(ID), None)
            if N is None:
                return
            W = float(N.get("Width", 160.0))
            H = float(N.get("Height", 100.0))
            X1 = float(NX) - 0.5 * W
            Y1 = float(NY) - 0.5 * H
            X2 = float(NX) + 0.5 * W
            Y2 = float(NY) + 0.5 * H
            SX1 = float(self._Scale(X1))
            SY1 = float(self._Scale(Y1))
            SX2 = float(self._Scale(X2))
            SY2 = float(self._Scale(Y2))
            try:
                self._Canvas._Frame.coords(
                    self._Drag_Ghost_Item,
                    SX1, SY1, SX2, SY2
                )
            except:
                pass
            try:
                self._Canvas._Frame.tag_raise(self._Drag_Ghost_Item)
            except:
                pass
        except Exception as E:
            self._GUI.Error(f"{self._Type} - _Drag_Ghost_Update - {E}")

    def Clear(self):
        try:
            self.Remove_Node("all")
            self.Remove_Edge("all")
            self._Selected_Node_Id = None
            self._Selected_Edge_Id = None
            self._Pending_Connect = None
            self._Undo_Stack = []
            self._Redo_Stack = []
            self._Copy_Buffer = None
            self.Update_Scrollregion()
        except Exception as E:
            self._GUI.Error(f"{self._Type} - Clear - {E}")

    def Zoom_Get(self):
        try:
            return float(getattr(self, "_Zoom_Value", 1.0))
        except:
            return 1.0

    def Zoom_Set(self, Value = None):
        try:
            if Value is None:
                return float(self.Zoom_Get())
            _Z0 = float(self.Zoom_Get())
            _Z  = float(Value)
            _Z_Min = float(getattr(self, "_Zoom_Min", 0.7))
            _Z_Max = float(getattr(self, "_Zoom_Max", 5.0))
            _Z = max(_Z_Min, min(_Z_Max, _Z))
            if abs(_Z - _Z0) < 1e-9:
                return float(_Z)
            _C = getattr(self._Canvas, "_Frame", None)
            _XV = None
            _YV = None
            try:
                if _C is not None:
                    _XV = _C.xview()
                    _YV = _C.yview()
            except:
                _XV = None
                _YV = None
            self._Zoom_Value = float(_Z)
            try:
                self.Render()
            except:
                pass
            try:
                if _C is not None and _XV is not None:
                    _C.xview_moveto(float(_XV[0]))
                if _C is not None and _YV is not None:
                    _C.yview_moveto(float(_YV[0]))
            except:
                pass
            return float(_Z)
        except Exception as E:
            self._GUI.Error(f"{self._Type} - Zoom_Set - {E}")
            return float(self.Zoom_Get())

    def Zoom_In(self):
        try:
            _Step = float(getattr(self, "_Zoom_Step", 1.10))
            return float(self.Zoom_Set(float(self.Zoom_Get()) * _Step))
        except Exception as E:
            self._GUI.Error(f"{self._Type} - Zoom_In - {E}")
            return float(self.Zoom_Get())

    def Zoom_Out(self):
        try:
            _Step = float(getattr(self, "_Zoom_Step", 1.10))
            return float(self.Zoom_Set(float(self.Zoom_Get()) / _Step))
        except Exception as E:
            self._GUI.Error(f"{self._Type} - Zoom_Out - {E}")
            return float(self.Zoom_Get())

    def Zoom(self, Event):
        try:
            _Delta = int(getattr(Event, "delta", 0))
            if _Delta > 0:
                self.Zoom_In()
            elif _Delta < 0:
                self.Zoom_Out()
        except Exception as E:
            self._GUI.Error(f"{self._Type} - _On_Zoom - {E}")
            return None

    def Zoom_Reset(self):
        try:
            return float(self.Zoom_Set(1.0))
        except Exception as E:
            self._GUI.Error(f"{self._Type} - Zoom_Reset - {E}")
            return float(self.Zoom_Get())

    def _Scale(self, V):
        try:
            return float(V) * float(self.Zoom_Get())
        except:
            return float(V)

    def _Unscale(self, V):
        try:
            _Z = float(self.Zoom_Get())
            if _Z <= 1e-9:
                return float(V)
            return float(V) / _Z
        except:
            return float(V)

    def _Font_Size(self, Base):
        try:
            _Z = float(self.Zoom_Get())
            _S = int(round(float(Base) * _Z))
            return int(max(6, _S))
        except:
            try:
                return int(Base)
            except:
                return 10

    def _Event_Canvas_XY(self, Event):
        try:
            if hasattr(self._Canvas._Frame, "canvasx") and hasattr(self._Canvas._Frame, "canvasy"):
                _X = float(self._Canvas._Frame.canvasx(Event.x))
                _Y = float(self._Canvas._Frame.canvasy(Event.y))
            else:
                _X = float(getattr(Event, "x", 0.0))
                _Y = float(getattr(Event, "y", 0.0))
            return float(self._Unscale(_X)), float(self._Unscale(_Y))

        except Exception as E:
            self._GUI.Error(f"{self._Type} - _Event_Canvas_XY - {E}")
            return 0.0, 0.0

    def _Clamp_Pos(self, X, Y):
        try:
            return max(0.0, float(X)), max(0.0, float(Y))
        except Exception as E:
            self._GUI.Error(f"{self._Type} - _Clamp_Pos - {E}")
            return 0.0, 0.0

    def _Node_Ports_Default(self):
        try:
            return {"Top": True, "Left": True, "Right": True, "Bottom": True}
        except Exception as E:
            self._GUI.Error(f"{self._Type} - _Node_Ports_Default - {E}")
            return {"Top": True, "Left": True, "Right": True, "Bottom": True}

    def _Node_Port_Counts_Default(self):
        try:
            return {"Top": 3, "Bottom": 3, "Left": 2, "Right": 2}
        except Exception as E:
            self._GUI.Error(f"{self._Type} - _Node_Port_Counts_Default - {E}")
            return {"Top": 3, "Bottom": 3, "Left": 2, "Right": 2}

    def _Node_Port_Counts_Normalize(self, Port_Counts):
        try:
            Default = self._Node_Port_Counts_Default()
            Out = {}
            Inp = dict(Port_Counts or {})
            for Side in ["Top", "Bottom", "Left", "Right"]:
                V = Inp.get(Side, Default.get(Side, 0))
                try:
                    V = int(V)
                except:
                    V = int(Default.get(Side, 0))
                Out[Side] = max(0, V)
            return Out
        except Exception as E:
            self._GUI.Error(f"{self._Type} - _Node_Port_Counts_Normalize - {E}")
            return self._Node_Port_Counts_Default()
            
    def _Node_Port_Names_Default(self):
        try:
            return {}
        except Exception as E:
            self._GUI.Error(f"{self._Type} - _Node_Port_Names_Default - {E}")
            return {}

    def _Node_Port_Names_Normalize(self, Port_Names, Port_Counts = None):
        try:
            Allowed = None
            if Port_Counts is not None:
                C = self._Node_Port_Counts_Normalize(Port_Counts)
                Allowed = set()
                for Side in ["Top", "Bottom", "Left", "Right"]:
                    for Index in range(max(0, int(C.get(Side, 0)))):
                        Allowed.add(f"{str(Side)}:{int(Index)}")
            Inp = dict(Port_Names or {})
            Out = {}
            Sides = ["Top", "Bottom", "Left", "Right"]
            for K, V in Inp.items():
                try:
                    K2 = str(K).strip()
                except:
                    continue
                KeyOut = None
                if ":" in K2:
                    KeyOut = K2
                else:
                    SideHit = None
                    Rest = None
                    for S in Sides:
                        if K2.startswith(S):
                            SideHit = S
                            Rest = K2[len(S):]
                            break
                    if SideHit is not None:
                        try:
                            I = int(Rest)
                            KeyOut = f"{str(SideHit)}:{int(I)}"
                        except:
                            KeyOut = None
                if KeyOut is None:
                    continue
                if Allowed is not None and KeyOut not in Allowed:
                    continue
                if V is None:
                    continue
                try:
                    V2 = str(V)
                except:
                    V2 = ""
                V2 = V2.strip()
                if len(V2) == 0:
                    continue
                Out[KeyOut] = V2
            return Out
        except Exception as E:
            self._GUI.Error(f"{self._Type} - _Node_Port_Names_Normalize - {E}")
            return self._Node_Port_Names_Default()

    def _Node_Port_Colors_Default(self):
        try:
            return {"Top": [], "Bottom": [], "Left": [], "Right": []}
        except Exception as E:
            self._GUI.Error(f"{self._Type} - _Node_Port_Colors_Default - {E}")
            return {"Top": [], "Bottom": [], "Left": [], "Right": []}

    def _Node_Port_Colors_Normalize(self, Port_Colors, Port_Counts = None, Default_Color = None):
        try:
            Inp = dict(Port_Colors or {})
            Out = {}
            Counts = None
            if Port_Counts is not None:
                Counts = self._Node_Port_Counts_Normalize(Port_Counts)
            def _Color_Normalize(C):
                try:
                    if C is None:
                        return None
                    S = str(C).strip()
                    if len(S) <= 0:
                        return None
                    if not S.startswith("#"):
                        S = "#" + S
                    if len(S) not in [4, 7]:
                        return None
                    Hex = S[1:]
                    for Ch in Hex:
                        if Ch.lower() not in "0123456789abcdef":
                            return None
                    return S
                except:
                    return None
            Default = self._Node_Port_Colors_Default()
            for Side in ["Top", "Bottom", "Left", "Right"]:
                V = Inp.get(Side, Default.get(Side, []))
                if not isinstance(V, (list, tuple)):
                    V = []
                Colors = []
                for C in V:
                    C2 = _Color_Normalize(C)
                    if C2 is None:
                        continue
                    Colors.append(C2)
                if Counts is not None:
                    N = max(0, int(Counts.get(Side, 0)))
                    Colors = Colors[:N]
                    if Default_Color is not None:
                        DC = _Color_Normalize(Default_Color)
                        if DC is not None:
                            while len(Colors) < N:
                                Colors.append(DC)
                Out[Side] = Colors
            return Out
        except Exception as E:
            self._GUI.Error(f"{self._Type} - _Node_Port_Colors_Normalize - {E}")
            return self._Node_Port_Colors_Default()

    def _Node_Rect(self, ID):
        try:
            N = self._Nodes.get(ID, None)
            if N is None:
                return None
            X = float(N["X"])
            Y = float(N["Y"])
            W = float(N["Width"])
            H = float(N["Height"])
            return X - 0.5 * W, Y - 0.5 * H, X + 0.5 * W, Y + 0.5 * H
        except Exception as E:
            self._GUI.Error(f"{self._Type} - _Node_Rect - {E}")
            return None

    def _Port_Is_Input(self, Side):
        try:
            return str(Side) in ["Left", "Top"]
        except:
            return False

    def _Port_Is_Output(self, Side):
        try:
            return str(Side) in ["Right", "Bottom"]
        except:
            return False

    def _Port_Fill(self, Node_Id, Side, Index = 0):
        try:
            N = self._Nodes.get(int(Node_Id), None)
            if N is None:
                return "#000000"
            D = N.get("PortFill", None)
            if not isinstance(D, dict):
                D = {"Input": "#000000", "Output": "#000000"}
                N["PortFill"] = D
            Role = "Input" if self._Port_Is_Input(Side) else "Output"
            PerPort = N.get("PortFillPerPort", None)
            if isinstance(PerPort, dict):
                Key = f"{str(Side)}:{int(Index)}"
                if Key in PerPort:
                    return str(PerPort.get(Key))
            return str(D.get(Role, "#000000"))
        except Exception as E:
            self._GUI.Error(f"{self._Type} - _Port_Fill - {E}")
            return "#000000"

    def _Node_Port_Point(self, ID, Side, Index = 0):
        try:
            N = self._Nodes.get(ID, None)
            if N is None:
                return None
            Ports = dict(N.get("Ports", self._Node_Ports_Default()))
            if not Ports.get(str(Side), False):
                return None
            Port_Counts = self._Node_Port_Counts_Normalize(N.get("PortCounts", self._Node_Port_Counts_Default()))
            Count = int(Port_Counts.get(str(Side), 0))
            if Count <= 0:
                return None
            try:
                Index = int(Index)
            except:
                Index = 0
            Index = max(0, min(Count - 1, Index))
            Rect = self._Node_Rect(ID)
            if Rect is None:
                return None
            X1, Y1, X2, Y2 = Rect
            W = float(X2 - X1)
            H = float(Y2 - Y1)
            Pad = float(max(12.0, min(28.0, 0.15 * min(W, H))))
            Offset = float(getattr(self, "_Port_Offset", 12.0))
            if str(Side) in ["Top", "Bottom"]:
                Yp = float(Y1) - Offset if str(Side) == "Top" else float(Y2) + Offset
                Ratio = float(Index + 1) / float(Count + 1)
                Xp = float(X1) + Pad + Ratio * float(max(1.0, (W - 2.0 * Pad)))
                return float(Xp), float(Yp)
            if str(Side) in ["Left", "Right"]:
                Xp = float(X1) - Offset if str(Side) == "Left" else float(X2) + Offset
                Ratio = float(Index + 1) / float(Count + 1)
                Yp = float(Y1) + Pad + Ratio * float(max(1.0, (H - 2.0 * Pad)))
                return float(Xp), float(Yp)
            return None
        except Exception as E:
            self._GUI.Error(f"{self._Type} - _Node_Port_Point - {E}")
            return None

    def _Node_Port_All_Points(self, ID):
        try:
            N = self._Nodes.get(ID, None)
            if N is None:
                return []
            Ports = dict(N.get("Ports", self._Node_Ports_Default()))
            Port_Counts = self._Node_Port_Counts_Normalize(N.get("PortCounts", self._Node_Port_Counts_Default()))
            if "PortDisabled" not in N or not isinstance(N.get("PortDisabled"), set):
                N["PortDisabled"] = set()
            Out = []
            for Side in ["Top", "Left", "Right", "Bottom"]:
                if not Ports.get(Side, False):
                    continue
                Count = int(Port_Counts.get(Side, 0))
                for Index in range(max(0, Count)):
                    Key = f"{str(Side)}:{int(Index)}"
                    if Key in N["PortDisabled"]:
                        continue
                    P = self._Node_Port_Point(ID, Side, Index)
                    if P is None:
                        continue
                    X, Y = P
                    Out.append((Side, int(Index), float(X), float(Y)))
            return Out
        except Exception as E:
            self._GUI.Error(f"{self._Type} - _Node_Port_All_Points - {E}")
            return []

    def _Node_Port_Hit(self, ID, X, Y, Tol = 10.0):
        try:
            Best = None
            BestD = None
            for Side, Index, Px, Py in self._Node_Port_All_Points(ID):
                D = math.hypot(float(X) - float(Px), float(Y) - float(Py))
                if D <= float(Tol) and (BestD is None or D < BestD):
                    BestD = D
                    Best = (str(Side), int(Index))
            return Best
        except Exception as E:
            self._GUI.Error(f"{self._Type} - _Node_Port_Hit - {E}")
            return None

    def _Node_Port_Items_Init(self, Node):
        try:
            if "PortItems" not in Node or not isinstance(Node.get("PortItems"), dict):
                Node["PortItems"] = {}
            return Node["PortItems"]
        except Exception as E:
            self._GUI.Error(f"{self._Type} - _Node_Port_Items_Init - {E}")
            Node["PortItems"] = {}
            return Node["PortItems"]

    def _Node_Port_Color_Get(self, ID, Side, Index, Default = None):
        try:
            if ID not in self._Nodes:
                return Default
            N = self._Nodes[ID]
            PortColors = N.get("PortColors", None)
            if not isinstance(PortColors, dict):
                return Default
            SideKey = str(Side)
            L = PortColors.get(SideKey, [])
            if not isinstance(L, (list, tuple)):
                return Default
            I = int(Index)
            if I < 0 or I >= len(L):
                return Default
            C = L[I]
            if C is None:
                return Default
            S = str(C).strip()
            if len(S) <= 0:
                return Default
            return S
        except Exception as E:
            self._GUI.Error(f"{self._Type} - _Node_Port_Color_Get - {E}")
            return Default

    def _Node_Draw_Ports(self, ID):
        try:
            if ID not in self._Nodes:
                return
            N = self._Nodes[ID]
            Disabled = bool(self._Disabled_Nodes.get(ID, False))
            PortItems = self._Node_Port_Items_Init(N)
            if "PortStubItems" not in N or not isinstance(N.get("PortStubItems"), dict):
                N["PortStubItems"] = {}
            if "PortDisabled" not in N or not isinstance(N.get("PortDisabled"), set):
                N["PortDisabled"] = set()
            if "PortNameItems" not in N or not isinstance(N.get("PortNameItems"), dict):
                N["PortNameItems"] = {}
            StubItems = N["PortStubItems"]
            NameItems = N["PortNameItems"]
            PortNames = N.get("PortNames", {})
            if not isinstance(PortNames, dict):
                PortNames = {}
            Keep = set()
            Pending = getattr(self, "_Pending_Connect", None)
            PendingKey = None
            if Pending is not None and isinstance(Pending, tuple) and len(Pending) >= 3 and int(Pending[0]) == int(ID):
                PendingKey = f"{str(Pending[1])}:{int(Pending[2])}"
            Rect = self._Node_Rect(ID)
            if Rect is None:
                return
            X1, Y1, X2, Y2 = Rect
            R = float(self._Port_Radius)
            SR = float(self._Scale(R))
            for Side, Index, Px, Py in self._Node_Port_All_Points(ID):
                Key = f"{str(Side)}:{int(Index)}"
                Keep.add(Key)
                IsInput = self._Port_Is_Input(Side)
                Outline = "#1F618D" if IsInput else "#117A65"
                DefaultFill = str(self._Port_Fill(ID, Side, Index))
                Fill = str(self._Node_Port_Color_Get(ID, Side, Index, Default = DefaultFill))
                Width = 1.5
                if self._Selected_Node_Id == ID:
                    Width = 2.0
                if Disabled:
                    Outline = "#808080"
                    Fill = "#C0C0C0"
                if PendingKey is not None and Key == PendingKey:
                    Outline = "#000000"
                BorderX = float(Px)
                BorderY = float(Py)
                if str(Side) == "Left":
                    BorderX = float(X1)
                if str(Side) == "Right":
                    BorderX = float(X2)
                if str(Side) == "Top":
                    BorderY = float(Y1)
                if str(Side) == "Bottom":
                    BorderY = float(Y2)
                SPx = float(self._Scale(Px))
                SPy = float(self._Scale(Py))
                SBorderX = float(self._Scale(BorderX))
                SBorderY = float(self._Scale(BorderY))
                Stub = StubItems.get(Key, None)
                if Stub is None:
                    try:
                        Stub = self._Canvas._Frame.create_line(
                            float(SBorderX), float(SBorderY), float(SPx), float(SPy),
                            fill = Outline,
                            width = max(1.0, float(self._Scale(float(self._Thickness) * 0.8)))
                        )
                    except:
                        Stub = None
                    StubItems[Key] = Stub
                    if Stub is not None:
                        self._Item_To_Node[Stub] = ID
                else:
                    try:
                        self._Canvas._Frame.coords(Stub, float(SBorderX), float(SBorderY), float(SPx), float(SPy))
                        self._Canvas._Frame.itemconfigure(
                            Stub,
                            fill = Outline,
                            width = max(1.0, float(self._Scale(float(self._Thickness) * 0.8))),
                            state = "normal"
                        )
                    except:
                        pass
                Item = PortItems.get(Key, None)
                SWidth = float(self._Scale(Width))
                if IsInput:
                    Ax1 = float(SPx) - SR
                    Ay1 = float(SPy) - SR
                    Ax2 = float(SPx) + SR
                    Ay2 = float(SPy) + SR
                    if Item is None:
                        try:
                            Item = self._Canvas._Frame.create_rectangle(Ax1, Ay1, Ax2, Ay2, outline = Outline, fill = Fill, width = SWidth)
                        except Exception as E:
                            self._GUI.Error(f"{self._Type} - create_rectangle failed: {E} (Frame={type(self._Canvas._Frame)})")
                            continue
                        PortItems[Key] = Item
                        self._Item_To_Node[Item] = ID
                    else:
                        try:
                            self._Canvas._Frame.coords(Item, Ax1, Ay1, Ax2, Ay2)
                            self._Canvas._Frame.itemconfigure(Item, outline = Outline, fill = Fill, width = SWidth, state = "normal")
                        except:
                            pass
                else:
                    Pts = []
                    for A in [0.0, 60.0, 120.0, 180.0, 240.0, 300.0]:
                        Rad = math.radians(A)
                        Pts.append(float(SPx) + SR * math.cos(Rad))
                        Pts.append(float(SPy) + SR * math.sin(Rad))
                    if Item is None:
                        try:
                            Item = self._Canvas._Frame.create_polygon(*Pts, outline = Outline, fill = Fill, width = SWidth)
                        except Exception as E:
                            self._GUI.Error(f"{self._Type} - create_polygon failed: {E} (Frame={type(self._Canvas._Frame)})")
                            continue
                        PortItems[Key] = Item
                        self._Item_To_Node[Item] = ID
                    else:
                        try:
                            self._Canvas._Frame.coords(Item, *Pts)
                            self._Canvas._Frame.itemconfigure(Item, outline = Outline, fill = Fill, width = SWidth, state = "normal")
                        except:
                            pass
                Label = PortNames.get(Key, None)
                if not isinstance(Label, str):
                    Label = ""
                Label = Label.strip()
                Name = NameItems.get(Key, None)
                if Label == "":
                    if Name is not None:
                        try:
                            self._Canvas._Frame.delete(Name)
                        except:
                            pass
                        if Name in self._Item_To_Node:
                            del self._Item_To_Node[Name]
                        del NameItems[Key]
                else:
                    Pad = float(max(10.0, float(R) + 6.0))
                    Tx = float(Px)
                    Ty = float(Py)
                    Anchor = "center"
                    if str(Side) == "Left":
                        Tx = float(X1) + Pad
                        Ty = float(Py)
                        Anchor = "w"
                    if str(Side) == "Right":
                        Tx = float(X2) - Pad
                        Ty = float(Py)
                        Anchor = "e"
                    if str(Side) == "Top":
                        Tx = float(Px)
                        Ty = float(Y1) + Pad
                        Anchor = "n"
                    if str(Side) == "Bottom":
                        Tx = float(Px)
                        Ty = float(Y2) - Pad
                        Anchor = "s"
                    STx = float(self._Scale(Tx))
                    STy = float(self._Scale(Ty))
                    Font = ("Arial", int(self._Font_Size(int(getattr(self, "_Font_Field_Base", 9)))), "normal")
                    TextColor = "#808080" if Disabled else str(N.get("Color", "#000000"))
                    if Name is None:
                        try:
                            Name = self._Canvas._Frame.create_text(
                                STx, STy,
                                text = Label,
                                anchor = Anchor,
                                font = Font,
                                fill = TextColor
                            )
                        except:
                            Name = None
                        NameItems[Key] = Name
                        if Name is not None:
                            self._Item_To_Node[Name] = ID
                    else:
                        try:
                            self._Canvas._Frame.coords(Name, STx, STy)
                            self._Canvas._Frame.itemconfigure(Name, text = Label, anchor = Anchor, font = Font, fill = TextColor, state = "normal")
                        except:
                            pass
            for Key in list(PortItems.keys()):
                if Key in Keep:
                    continue
                Old = PortItems.get(Key, None)
                if Old is not None:
                    try:
                        self._Canvas._Frame.delete(Old)
                    except:
                        pass
                if Old in self._Item_To_Node:
                    del self._Item_To_Node[Old]
                del PortItems[Key]
            for Key in list(StubItems.keys()):
                if Key in Keep:
                    continue
                Old = StubItems.get(Key, None)
                if Old is not None:
                    try:
                        self._Canvas._Frame.delete(Old)
                    except:
                        pass
                if Old in self._Item_To_Node:
                    del self._Item_To_Node[Old]
                del StubItems[Key]
            for Key in list(NameItems.keys()):
                if Key in Keep:
                    continue
                Old = NameItems.get(Key, None)
                if Old is not None:
                    try:
                        self._Canvas._Frame.delete(Old)
                    except:
                        pass
                if Old in self._Item_To_Node:
                    del self._Item_To_Node[Old]
                del NameItems[Key]
            for Key in Keep:
                It = StubItems.get(Key, None)
                if It is not None:
                    try:
                        self._Canvas._Frame.tag_raise(It)
                    except:
                        pass
                It2 = PortItems.get(Key, None)
                if It2 is not None:
                    try:
                        self._Canvas._Frame.tag_raise(It2)
                    except:
                        pass
                It3 = NameItems.get(Key, None)
                if It3 is not None:
                    try:
                        self._Canvas._Frame.tag_raise(It3)
                    except:
                        pass
        except Exception as E:
            self._GUI.Error(f"{self._Type} - _Node_Draw_Ports - {E}")

    def _Node_Draw(self, ID):
        try:
            if ID not in self._Nodes:
                return
            N = self._Nodes[ID]
            Rect = self._Node_Rect(ID)
            if Rect is None:
                return
            X1, Y1, X2, Y2 = Rect
            Disabled = bool(self._Disabled_Nodes.get(ID, False))
            Outline = str(N.get("Color", "#4F8EF7"))
            Fill = str(N.get("Fill", "#DC7633"))
            if Disabled:
                Outline = "#808080"
                Fill = "#C0C0C0"
            Width = float(self._Thickness)
            if self._Selected_Node_Id == ID:
                Width = float(self._Thickness) * float(self._Selected_Thickness_Multiplier)
            if self._Selected_Node_Id == ID and self._Selected_Outline_Color is not None:
                Outline = str(self._Selected_Outline_Color)
            SX1 = float(self._Scale(X1))
            SY1 = float(self._Scale(Y1))
            SX2 = float(self._Scale(X2))
            SY2 = float(self._Scale(Y2))
            SWidth = max(1.0, float(self._Scale(Width)))
            Item = N.get("Item", None)
            if Item is None:
                try:
                    Item = self._Canvas._Frame.create_rectangle(SX1, SY1, SX2, SY2, outline = Outline, fill = Fill, width = SWidth)
                except Exception as E:
                    self._GUI.Error(f"{self._Type} - create_rectangle failed: {E} (Frame={type(self._Canvas._Frame)})")
                    return
                N["Item"] = Item
                self._Item_To_Node[Item] = ID
            else:
                try:
                    self._Canvas._Frame.coords(Item, SX1, SY1, SX2, SY2)
                    self._Canvas._Frame.itemconfigure(Item, outline = Outline, fill = Fill, width = SWidth, state = "normal")
                except:
                    pass
            TitleItem = N.get("TitleItem", None)
            DescItem = N.get("DescItem", None)
            Title = str(N.get("Title", ""))
            Description = str(N.get("Description", ""))
            Xc = 0.5 * (float(X1) + float(X2))
            Yc = 0.5 * (float(Y1) + float(Y2))
            SXc = float(self._Scale(Xc))
            TextWidth = max(20, int(max(0.0, float(SX2 - SX1) - 12.0)))
            TitleFont = ("Arial", int(self._Font_Size(int(getattr(self, "_Font_Title_Base", 10)))), "bold")
            DescFont  = ("Arial", int(self._Font_Size(int(getattr(self, "_Font_Desc_Base", 9)))), "normal")
            Gap = 14.0
            Yt = float(Yc) - 0.5 * float(Gap)
            Yd = float(Yc) + 0.5 * float(Gap)
            SYt = float(self._Scale(Yt))
            SYd = float(self._Scale(Yd))
            if TitleItem is None:
                try:
                    TitleItem = self._Canvas._Frame.create_text(
                        SXc, SYt,
                        text = Title,
                        anchor = "center",
                        justify = "center",
                        font = TitleFont,
                        fill = "#000000",
                        width = TextWidth
                    )
                except:
                    TitleItem = None
                N["TitleItem"] = TitleItem
                if TitleItem is not None:
                    self._Item_To_Node[TitleItem] = ID
            else:
                try:
                    self._Canvas._Frame.coords(TitleItem, SXc, SYt)
                    self._Canvas._Frame.itemconfigure(TitleItem, text = Title, state = "normal", width = TextWidth, justify = "center", font = TitleFont, anchor = "center")
                except:
                    pass
            if DescItem is None:
                try:
                    DescItem = self._Canvas._Frame.create_text(
                        SXc, SYd,
                        text = Description,
                        anchor = "center",
                        justify = "center",
                        font = DescFont,
                        fill = "#000000",
                        width = TextWidth
                    )
                except:
                    DescItem = None
                N["DescItem"] = DescItem
                if DescItem is not None:
                    self._Item_To_Node[DescItem] = ID
            else:
                try:
                    self._Canvas._Frame.coords(DescItem, SXc, SYd)
                    self._Canvas._Frame.itemconfigure(DescItem, text = Description, state = "normal", width = TextWidth, justify = "center", font = DescFont, anchor = "center")
                except:
                    pass
                    
            Locked = bool(self._Locked_Nodes.get(ID, False))
            LockItem = N.get("LockItem", None)
            if Locked:
                R = 6.0
                Pad = 6.0
                SR = float(self._Scale(R))
                SPad = float(self._Scale(Pad))
                LX1 = float(SX1 + SPad)
                LY1 = float(SY1 + SPad)
                LX2 = float(LX1 + 2.0 * SR)
                LY2 = float(LY1 + 2.0 * SR)
                if LockItem is None:
                    try:
                        LockItem = self._Canvas._Frame.create_oval(LX1, LY1, LX2, LY2, outline = "#000000", fill = "#FF0000", width = max(1.0, float(self._Scale(1.0))))
                    except:
                        LockItem = None
                    N["LockItem"] = LockItem
                    if LockItem is not None:
                        self._Item_To_Node[LockItem] = ID
                else:
                    try:
                        self._Canvas._Frame.coords(LockItem, LX1, LY1, LX2, LY2)
                        self._Canvas._Frame.itemconfigure(LockItem, outline = "#000000", fill = "#FF0000", state = "normal", width = max(1.0, float(self._Scale(1.0))))
                    except:
                        pass
            else:
                if LockItem is not None:
                    try:
                        self._Canvas._Frame.delete(LockItem)
                    except:
                        pass
                    if LockItem in self._Item_To_Node:
                        del self._Item_To_Node[LockItem]
                    N["LockItem"] = None
            try:
                self._Canvas._Frame.tag_raise(Item)
                if TitleItem is not None:
                    self._Canvas._Frame.tag_raise(TitleItem)
                if DescItem is not None:
                    self._Canvas._Frame.tag_raise(DescItem)
                if LockItem is not None:
                    self._Canvas._Frame.tag_raise(LockItem)
            except:
                pass
            self._Node_Draw_Ports(ID)
        except Exception as E:
            self._GUI.Error(f"{self._Type} - _Node_Draw - {E}")

    def _Route_Snap(self, X, Y):
        try:
            G = float(getattr(self, "_Route_Grid", 10.0))
            if G <= 1.0:
                return float(X), float(Y)
            return float(round(float(X) / G) * G), float(round(float(Y) / G) * G)
        except:
            return float(X), float(Y)

    def _Rect_Expanded(self, Rect, Pad):
        try:
            X1, Y1, X2, Y2 = Rect
            P = float(Pad)
            return float(X1) - P, float(Y1) - P, float(X2) + P, float(Y2) + P
        except:
            return Rect

    def _Point_In_Rect(self, X, Y, Rect):
        try:
            X1, Y1, X2, Y2 = Rect
            return float(X) >= float(X1) and float(X) <= float(X2) and float(Y) >= float(Y1) and float(Y) <= float(Y2)
        except:
            return False
            
    def _Port_Obstacle_Rect(self, Node_Id, Side, Index = 0):
        try:
            P = self._Node_Port_Point(int(Node_Id), str(Side), int(Index))
            if P is None:
                return None
            X, Y = float(P[0]), float(P[1])
            C = float(max(getattr(self, "_Port_Clearance", 14.0), float(self._Port_Radius) + 6.0))
            return (X - C, Y - C, X + C, Y + C)
        except Exception as E:
            self._GUI.Error(f"{self._Type} - _Port_Obstacle_Rect - {E}")
            return None

    def _Segment_Intersects_Rect(self, A_X, A_Y, B_X, B_Y, Rect):
        try:
            A_X = float(A_X); A_Y = float(A_Y); B_X = float(B_X); B_Y = float(B_Y)
            X1, Y1, X2, Y2 = Rect
            X_Min = float(min(X1, X2)); X_Max = float(max(X1, X2)); Y_Min = float(min(Y1, Y2)); Y_Max = float(max(Y1, Y2))
            Seg_X_Min = float(min(A_X, B_X)); Seg_X_Max = float(max(A_X, B_X)); Seg_Y_Min = float(min(A_Y, B_Y)); Seg_Y_Max = float(max(A_Y, B_Y))
            if Seg_X_Max < X_Min or Seg_X_Min > X_Max or Seg_Y_Max < Y_Min or Seg_Y_Min > Y_Max:
                return False
            if abs(A_X - B_X) < 1e-6:
                if A_X < X_Min or A_X > X_Max:
                    return False
                return not (Seg_Y_Max < Y_Min or Seg_Y_Min > Y_Max)
            if abs(A_Y - B_Y) < 1e-6:
                if A_Y < Y_Min or A_Y > Y_Max:
                    return False
                return not (Seg_X_Max < X_Min or Seg_X_Min > X_Max)
            return True
        except:
            return True

    def _Segment_Intersects_Any_Rect(self, A_Point, B_Point, Obstacles):
        try:
            A_X = float(A_Point[0]); A_Y = float(A_Point[1]); B_X = float(B_Point[0]); B_Y = float(B_Point[1])
            for Rect in list(Obstacles or []):
                if self._Segment_Intersects_Rect(A_X, A_Y, B_X, B_Y, Rect):
                    return True
            return False
        except:
            return True

    def _Port_Escape_Point(self, Node_Id, Side, Index):
        try:
            Port_Point = self._Node_Port_Point(int(Node_Id), str(Side), int(Index))
            if Port_Point is None:
                return None
            Port_X = float(Port_Point[0]); Port_Y = float(Port_Point[1])
            Grid = float(getattr(self, "_Route_Grid", 10.0))
            Clearance = float(getattr(self, "_Route_Clearance", 20.0))
            Offset = float(getattr(self, "_Port_Offset", 12.0))
            Step = float(max(Grid, (Clearance - Offset) + Grid))
            Dx = 0.0; Dy = 0.0
            if str(Side) == "Left":
                Dx = -Step
            if str(Side) == "Right":
                Dx = Step
            if str(Side) == "Top":
                Dy = -Step
            if str(Side) == "Bottom":
                Dy = Step
            Escape_X, Escape_Y = self._Route_Snap(Port_X + Dx, Port_Y + Dy)
            return (float(Escape_X), float(Escape_Y))
        except Exception as E:
            self._GUI.Error(f"{self._Type} - _Port_Escape_Point - {E}")
            return None

    def _Build_Route_Obstacles(self, Ignore_Edge_Id = None, Allow_Ports = None):
        try:
            Pad = float(getattr(self, "_Route_Clearance", 20.0))
            Allow_Set = set(Allow_Ports or [])
            Obstacles = []
            for Node_Id in list(self._Nodes.keys()):
                Node_Rect = self._Node_Rect(Node_Id)
                if Node_Rect is None:
                    continue
                Obstacles.append(self._Rect_Expanded(Node_Rect, Pad))
            for Node_Id in list(self._Nodes.keys()):
                for Side, Index, Px, Py in self._Node_Port_All_Points(Node_Id):
                    Port_Key = (int(Node_Id), str(Side), int(Index))
                    if Port_Key in Allow_Set:
                        continue
                    Port_Rect = self._Port_Obstacle_Rect(Node_Id, Side, Index)
                    if Port_Rect is not None:
                        Obstacles.append(Port_Rect)
            return Obstacles
        except Exception as E:
            self._GUI.Error(f"{self._Type} - _Build_Route_Obstacles - {E}")
            return []

    def _Edge_To_Grid_Segments(self, Points):
        try:
            Segs = set()
            if not Points or len(Points) < 2:
                return Segs
            Prev = None
            for P in Points:
                GX, GY = self._Route_Snap(float(P[0]), float(P[1]))
                Cur = (float(GX), float(GY))
                if Prev is None:
                    Prev = Cur
                    continue
                Ax, Ay = Prev
                Bx, By = Cur
                if abs(Ax - Bx) < 1e-6 and abs(Ay - By) < 1e-6:
                    Prev = Cur
                    continue
                if abs(Ax - Bx) >= abs(Ay - By):
                    Step = 1.0 if Bx >= Ax else -1.0
                    X = Ax
                    while (X - Bx) * Step < -1e-6:
                        Nxt = (float(X + Step * float(getattr(self, "_Route_Grid", 10.0))), float(Ay))
                        Segs.add((Prev, Nxt) if Prev <= Nxt else (Nxt, Prev))
                        Prev = Nxt
                        X = Prev[0]
                    Prev = Cur
                else:
                    Step = 1.0 if By >= Ay else -1.0
                    Y = Ay
                    while (Y - By) * Step < -1e-6:
                        Nxt = (float(Ax), float(Y + Step * float(getattr(self, "_Route_Grid", 10.0))))
                        Segs.add((Prev, Nxt) if Prev <= Nxt else (Nxt, Prev))
                        Prev = Nxt
                        Y = Prev[1]
                    Prev = Cur
            return Segs
        except:
            return set()

    def _Occupied_Segments(self, Ignore_Edge_Id = None):
        try:
            Occ = set()
            for Eid, E in list(self._Edges.items()):
                if Ignore_Edge_Id is not None and int(Eid) == int(Ignore_Edge_Id):
                    continue
                Pts = list(E.get("Points", []))
                Occ |= self._Edge_To_Grid_Segments(Pts)
            return Occ
        except Exception as E:
            self._GUI.Error(f"{self._Type} - _Occupied_Segments - {E}")
            return set()

    def _Neighbors_4(self, P):
        try:
            G = float(getattr(self, "_Route_Grid", 10.0))
            X, Y = P
            return [(float(X + G), float(Y)), (float(X - G), float(Y)), (float(X), float(Y + G)), (float(X), float(Y - G))]
        except:
            return []

    def _AStar_Path(self, Start, Goal, Obstacles, Occupied):
        try:
            import heapq
            Grid = float(getattr(self, "_Route_Grid", 10.0))
            Pad = float(getattr(self, "_Route_Clearance", 20.0))
            Xs = [float(Start[0]), float(Goal[0])]; Ys = [float(Start[1]), float(Goal[1])]
            for Node_Id in list(self._Nodes.keys()):
                Node_Rect = self._Node_Rect(Node_Id)
                if Node_Rect is None:
                    continue
                X1, Y1, X2, Y2 = self._Rect_Expanded(Node_Rect, Pad)
                Xs.extend([float(X1), float(X2)]); Ys.extend([float(Y1), float(Y2)])
            Bounds_Pad = float(max(6.0 * Grid, 6.0 * Pad))
            Min_X = float(min(Xs) - Bounds_Pad); Max_X = float(max(Xs) + Bounds_Pad); Min_Y = float(min(Ys) - Bounds_Pad); Max_Y = float(max(Ys) + Bounds_Pad)
            def In_Bounds(Point):
                X = float(Point[0]); Y = float(Point[1])
                return X >= Min_X and X <= Max_X and Y >= Min_Y and Y <= Max_Y
            def Is_Point_Blocked(Point):
                X = float(Point[0]); Y = float(Point[1])
                for Rect in Obstacles:
                    if self._Point_In_Rect(X, Y, Rect):
                        return True
                return False
            def Is_Move_Blocked(A_Point, B_Point):
                if not In_Bounds(B_Point):
                    return True
                if Is_Point_Blocked(B_Point):
                    return True
                if self._Segment_Intersects_Any_Rect(A_Point, B_Point, Obstacles):
                    return True
                Seg = (A_Point, B_Point) if A_Point <= B_Point else (B_Point, A_Point)
                if Seg in Occupied:
                    return True
                return False
            Start = (float(Start[0]), float(Start[1])); Goal = (float(Goal[0]), float(Goal[1]))
            if not In_Bounds(Start) or not In_Bounds(Goal):
                return None
            if Is_Point_Blocked(Start) or Is_Point_Blocked(Goal):
                return None
            Open_Heap = []
            heapq.heappush(Open_Heap, (0.0, Start))
            Came_From = {}
            G_Score = {Start: 0.0}
            Dir_From = {Start: None}
            Best_Goal = None
            Limit = 120000
            Iter = 0
            while Open_Heap and Iter < Limit:
                Iter += 1
                Cur = heapq.heappop(Open_Heap)[1]
                if abs(Cur[0] - Goal[0]) < 1e-6 and abs(Cur[1] - Goal[1]) < 1e-6:
                    Best_Goal = Cur
                    break
                Cur_Dir = Dir_From.get(Cur, None)
                for Nxt in self._Neighbors_4(Cur):
                    Nxt = (float(Nxt[0]), float(Nxt[1]))
                    if Is_Move_Blocked(Cur, Nxt):
                        continue
                    Step_Cost = 1.0
                    This_Dir = (float(Nxt[0] - Cur[0]), float(Nxt[1] - Cur[1]))
                    if Cur_Dir is not None and (abs(Cur_Dir[0] - This_Dir[0]) > 1e-6 or abs(Cur_Dir[1] - This_Dir[1]) > 1e-6):
                        Step_Cost += 0.65
                    Tent = float(G_Score.get(Cur, 1e30) + Step_Cost)
                    if Tent < float(G_Score.get(Nxt, 1e30)):
                        Came_From[Nxt] = Cur
                        Dir_From[Nxt] = This_Dir
                        G_Score[Nxt] = Tent
                        H = (abs(Nxt[0] - Goal[0]) + abs(Nxt[1] - Goal[1])) / float(max(1.0, Grid))
                        heapq.heappush(Open_Heap, (Tent + H, Nxt))
            if Best_Goal is None:
                return None
            Path = [Best_Goal]
            Cur = Best_Goal
            while Cur in Came_From:
                Cur = Came_From[Cur]
                Path.append(Cur)
            Path.reverse()
            return Path
        except Exception as E:
            self._GUI.Error(f"{self._Type} - _AStar_Path - {E}")
            return None

    def _Simplify_Polyline(self, Points):
        try:
            if not Points:
                return []
            Out = [Points[0]]
            PrevDir = None
            for I in range(1, len(Points)):
                A = Out[-1]
                B = Points[I]
                Dx = float(B[0]) - float(A[0])
                Dy = float(B[1]) - float(A[1])
                ThisDir = (0.0, 0.0)
                if abs(Dx) >= abs(Dy):
                    ThisDir = (1.0 if Dx > 0 else (-1.0 if Dx < 0 else 0.0), 0.0)
                else:
                    ThisDir = (0.0, 1.0 if Dy > 0 else (-1.0 if Dy < 0 else 0.0))
                if PrevDir is None:
                    Out.append(B)
                    PrevDir = ThisDir
                    continue
                if abs(PrevDir[0] - ThisDir[0]) < 1e-6 and abs(PrevDir[1] - ThisDir[1]) < 1e-6:
                    Out[-1] = B
                else:
                    Out.append(B)
                    PrevDir = ThisDir
            return Out
        except:
            return Points

    def _Edge_Route(self, From_Id, From_Side, To_Id, To_Side, From_Index = 0, To_Index = 0, Ignore_Edge_Id = None):
        try:
            Start_Port = self._Node_Port_Point(From_Id, From_Side, From_Index)
            End_Port = self._Node_Port_Point(To_Id, To_Side, To_Index)
            if Start_Port is None or End_Port is None:
                return []
            Start_X = float(Start_Port[0]); Start_Y = float(Start_Port[1])
            End_X = float(End_Port[0]); End_Y = float(End_Port[1])
            Start_Escape = self._Port_Escape_Point(From_Id, From_Side, From_Index)
            End_Escape = self._Port_Escape_Point(To_Id, To_Side, To_Index)
            if Start_Escape is None or End_Escape is None:
                return [(Start_X, Start_Y), (End_X, End_Y)]
            Start = self._Route_Snap(float(Start_Escape[0]), float(Start_Escape[1]))
            Goal = self._Route_Snap(float(End_Escape[0]), float(End_Escape[1]))
            Allow = {(int(From_Id), str(From_Side), int(From_Index)), (int(To_Id), str(To_Side), int(To_Index))}
            Obstacles = self._Build_Route_Obstacles(Ignore_Edge_Id = Ignore_Edge_Id, Allow_Ports = Allow)
            Occupied = self._Occupied_Segments(Ignore_Edge_Id = Ignore_Edge_Id)
            Path = self._AStar_Path(Start, Goal, Obstacles, Occupied)
            if Path is None:
                Grid = float(getattr(self, "_Route_Grid", 10.0))
                A_X = float(Start[0]); A_Y = float(Start[1]); B_X = float(Goal[0]); B_Y = float(Goal[1])
                Candidates = []
                Candidates.append([Start, (B_X, A_Y), Goal])
                Candidates.append([Start, (A_X, B_Y), Goal])
                for K in range(1, 17):
                    Off = float(K) * Grid
                    Candidates.append([Start, (B_X, A_Y + Off), Goal])
                    Candidates.append([Start, (B_X, A_Y - Off), Goal])
                    Candidates.append([Start, (A_X + Off, B_Y), Goal])
                    Candidates.append([Start, (A_X - Off, B_Y), Goal])
                Best = None
                for Cand in Candidates:
                    Cand2 = [self._Route_Snap(float(P[0]), float(P[1])) for P in Cand]
                    Ok = True
                    for I in range(len(Cand2) - 1):
                        if self._Segment_Intersects_Any_Rect(Cand2[I], Cand2[I + 1], Obstacles):
                            Ok = False
                            break
                    if Ok:
                        Best = Cand2
                        break
                if Best is None:
                    Best = [Start, Goal]
                Poly = self._Simplify_Polyline(Best)
            else:
                Poly = self._Simplify_Polyline(Path)
            Out = [(Start_X, Start_Y), (float(Start[0]), float(Start[1]))]
            for P in Poly[1:-1]:
                Out.append((float(P[0]), float(P[1])))
            Out.append((float(Goal[0]), float(Goal[1])))
            Out.append((End_X, End_Y))
            return Out
        except Exception as E:
            self._GUI.Error(f"{self._Type} - _Edge_Route - {E}")
            return [(0.0, 0.0), (0.0, 0.0)]

    def _Edge_Draw(self, ID):
        try:
            if ID not in self._Edges:
                return
            E = self._Edges[ID]
            Disabled = bool(self._Disabled_Edges.get(ID, False))
            Color = str(E.get("Color", "#000000"))
            if Disabled:
                Color = "#808080"
            Width = float(self._Thickness)
            if self._Selected_Edge_Id == ID:
                Width = float(self._Thickness) * float(self._Selected_Thickness_Multiplier)
            SWidth = max(1.0, float(self._Scale(Width)))
            Points = list(E.get("Points", []))
            Ortho = []
            for I, P in enumerate(Points):
                Px, Py = float(P[0]), float(P[1])
                if not Ortho:
                    Ortho.append((Px, Py))
                    continue
                Ax, Ay = Ortho[-1]
                if abs(Ax - Px) < 1e-6 or abs(Ay - Py) < 1e-6:
                    Ortho.append((Px, Py))
                else:
                    Ortho.append((Px, Ay))
                    Ortho.append((Px, Py))
            Clean = []
            for P in Ortho:
                if not Clean:
                    Clean.append(P)
                else:
                    if abs(Clean[-1][0] - P[0]) > 1e-6 or abs(Clean[-1][1] - P[1]) > 1e-6:
                        Clean.append(P)
            Flat = []
            for Px, Py in Clean:
                Flat.append(float(self._Scale(Px)))
                Flat.append(float(self._Scale(Py)))
            Item = E.get("Item", None)
            if Item is None:
                try:
                    Item = self._Canvas._Frame.create_line(*Flat, fill = Color, width = SWidth, smooth = self._Smooth_Edges)
                except Exception as e:
                    self._GUI.Error(f"{self._Type} - create_line failed: {e} (Frame={type(self._Canvas._Frame)})")
                    return
                E["Item"] = Item
                self._Item_To_Edge[Item] = ID
            else:
                try:
                    self._Canvas._Frame.coords(Item, *Flat)
                    self._Canvas._Frame.itemconfigure(Item, fill = Color, width = SWidth, state = "normal", smooth = self._Smooth_Edges)
                except:
                    pass
            try:
                self._Canvas._Frame.tag_raise(Item)
            except:
                pass
        except Exception as E:
            self._GUI.Error(f"{self._Type} - _Edge_Draw - {E}")

    def _Edge_End_Hit(self, Edge_Id, X, Y, Tol = 12.0):
        try:
            E = self._Edges.get(int(Edge_Id), None)
            if E is None:
                return None
            FX, FY = None, None
            TX, TY = None, None
            FP = self._Node_Port_Point(int(E.get("FromID", 0)), str(E.get("FromSide", "")), int(E.get("FromIndex", 0)))
            TP = self._Node_Port_Point(int(E.get("ToID", 0)),   str(E.get("ToSide", "")),   int(E.get("ToIndex", 0)))
            if FP is not None:
                FX, FY = float(FP[0]), float(FP[1])
            if TP is not None:
                TX, TY = float(TP[0]), float(TP[1])
            Best = None
            BestD = None
            if FX is not None:
                D = math.hypot(float(X) - FX, float(Y) - FY)
                if D <= float(Tol):
                    Best = "From"
                    BestD = float(D)
            if TX is not None:
                D = math.hypot(float(X) - TX, float(Y) - TY)
                if D <= float(Tol) and (BestD is None or D < BestD):
                    Best = "To"
                    BestD = float(D)
            return Best
        except:
            return None

    def Render(self):
        try:
            for ID in list(self._Edges.keys()):
                self._Edge_Draw(ID)
            for ID in list(self._Nodes.keys()):
                self._Node_Draw(ID)
            self.Update_Scrollregion()
        except Exception as E:
            self._GUI.Error(f"{self._Type} - Render - {E}")

    def On_Resize(self, Event = None):
        try:
            self.Render()
        except Exception as E:
            self._GUI.Error(f"{self._Type} - On_Resize - {E}")

    def _Pick_Item(self, X, Y):
        try:
            try:
                SX = float(self._Scale(float(X)))
                SY = float(self._Scale(float(Y)))
                Items = self._Canvas._Frame.find_overlapping(SX - 2.0, SY - 2.0, SX + 2.0, SY + 2.0)
            except:
                Items = []
            for It in reversed(list(Items)):
                if It in self._Item_To_Node:
                    return "Node", self._Item_To_Node[It]
                if It in self._Item_To_Edge:
                    return "Edge", self._Item_To_Edge[It]
            return None, None
        except Exception as E:
            self._GUI.Error(f"{self._Type} - _Pick_Item - {E}")
            return None, None

    def _Port_Connected_Edges(self, Node_Id, Side, Index):
        try:
            Node_Id = int(Node_Id)
            Side = str(Side)
            Index = int(Index)
            Out = []
            for Eid, E in list(self._Edges.items()):
                if int(E.get("FromID", -1)) == Node_Id and str(E.get("FromSide", "")) == Side and int(E.get("FromIndex", -1)) == Index:
                    Out.append((int(Eid), "From"))
                if int(E.get("ToID", -1)) == Node_Id and str(E.get("ToSide", "")) == Side and int(E.get("ToIndex", -1)) == Index:
                    Out.append((int(Eid), "To"))
            return Out
        except:
            self._GUI.Error(f"{self._Type} - _Port_Connected_Edges - {E}")
            return []

    def _Reconnect_Pick_Edge(self, Node_Id, Side, Index):
        try:
            Hits = list(self._Port_Connected_Edges(Node_Id, Side, Index))
            if not Hits:
                return None
            Sel = getattr(self, "_Selected_Edge_Id", None)
            if Sel is not None:
                for Eid, End in Hits:
                    if int(Eid) == int(Sel):
                        return (int(Eid), str(End))
            Hits.sort(key = lambda P: int(P[0]))
            return (int(Hits[-1][0]), str(Hits[-1][1]))
        except:
            self._GUI.Error(f"{self._Type} - _Reconnect_Pick_Edge - {E}")
            return None

    def _Edge_Half_Hit(self, Edge_Id, X, Y, Tol = 12.0):
        try:
            E = self._Edges.get(int(Edge_Id), None)
            if E is None:
                return None
            Pts = list(E.get("Points", []))
            if len(Pts) < 2:
                return None
            X = float(X)
            Y = float(Y)
            Tol = float(Tol)
            Total = 0.0
            SegLen = []
            for I in range(len(Pts) - 1):
                Ax, Ay = float(Pts[I][0]), float(Pts[I][1])
                Bx, By = float(Pts[I + 1][0]), float(Pts[I + 1][1])
                L = math.hypot(Bx - Ax, By - Ay)
                SegLen.append(L)
                Total += L
            if Total <= 1e-9:
                return None
            BestD = None
            BestS = 0.0
            Acc = 0.0
            for I in range(len(Pts) - 1):
                Ax, Ay = float(Pts[I][0]), float(Pts[I][1])
                Bx, By = float(Pts[I + 1][0]), float(Pts[I + 1][1])
                Dx = Bx - Ax
                Dy = By - Ay
                Den = Dx * Dx + Dy * Dy
                if Den <= 1e-12:
                    T = 0.0
                else:
                    T = ((X - Ax) * Dx + (Y - Ay) * Dy) / Den
                    T = max(0.0, min(1.0, float(T)))
                Qx = Ax + T * Dx
                Qy = Ay + T * Dy
                D = math.hypot(X - Qx, Y - Qy)
                if BestD is None or D < BestD:
                    BestD = D
                    BestS = Acc + T * float(SegLen[I])
                Acc += float(SegLen[I])
            if BestD is None or float(BestD) > float(Tol):
                return None
            if float(BestS) <= 0.5 * float(Total):
                return "From"
            return "To"
        except:
            return None

    def _Undo_Push(self):
        try:
            if bool(getattr(self, "_Undo_Lock", False)):
                return
            Snap = self.To_Dict()
            self._Undo_Stack.append(Snap)
            if len(self._Undo_Stack) > int(self._Undo_Limit):
                self._Undo_Stack = self._Undo_Stack[-int(self._Undo_Limit):]
            self._Redo_Stack = []
        except Exception as E:
            self._GUI.Error(f"{self._Type} - _Undo_Push - {E}")

    def Undo(self):
        try:
            if not self._Undo_Stack:
                return
            Current = self.To_Dict()
            State = self._Undo_Stack.pop(-1)
            self._Redo_Stack.append(Current)
            KeepUndo = list(self._Undo_Stack)
            KeepRedo = list(self._Redo_Stack)
            self._Undo_Lock = True
            try:
                self.From_Dict(State)
            finally:
                self._Undo_Lock = False
            self._Undo_Stack = KeepUndo
            self._Redo_Stack = KeepRedo
            self._Callback_Invoke("Flowchart", Event = "Undo", Data = {"Ok": True})
        except Exception as E:
            self._GUI.Error(f"{self._Type} - Undo - {E}")

    def Redo(self):
        try:
            if not self._Redo_Stack:
                return
            Current = self.To_Dict()
            State = self._Redo_Stack.pop(-1)
            self._Undo_Stack.append(Current)
            KeepUndo = list(self._Undo_Stack)
            KeepRedo = list(self._Redo_Stack)
            self._Undo_Lock = True
            try:
                self.From_Dict(State)
            finally:
                self._Undo_Lock = False
            self._Undo_Stack = KeepUndo
            self._Redo_Stack = KeepRedo
            self._Callback_Invoke("Flowchart", Event = "Redo", Data = {"Ok": True})
        except Exception as E:
            self._GUI.Error(f"{self._Type} - Redo - {E}")

    def Copy(self):
        try:
            if self._Selected_Node_Id is None:
                return
            D = self.Get_Node(self._Selected_Node_Id)
            if D is None:
                return
            self._Copy_Buffer = {"Node": D}
            self._Callback_Invoke("Flowchart", Event = "Copy", Data = {"ID": self._Selected_Node_Id})
        except Exception as E:
            self._GUI.Error(f"{self._Type} - Copy - {E}")

    def Paste(self):
        try:
            if not self._Copy_Buffer or "Node" not in self._Copy_Buffer:
                return
            N = self._Copy_Buffer["Node"]
            X = float(N.get("X", 40.0)) + 20.0
            Y = float(N.get("Y", 40.0)) + 20.0
            ID = self.Add_Node(
                X = X,
                Y = Y,
                Width  = float(N.get("Width", 120.0)),
                Height = float(N.get("Height", 80.0)),
                Color = str(N.get("Color", "#4F8EF7")),
                Fill  = str(N.get("Fill", "#DC7633")),
                Title = str(N.get("Title", "")),
                Description = str(N.get("Description", "")),
                Type = str(N.get("Type", "")),
                Ports = dict(N.get("Ports", self._Node_Ports_Default())),
                Port_Counts = dict(N.get("PortCounts", self._Node_Port_Counts_Default())),
                Port_Names  = dict(N.get("PortNames", self._Node_Port_Names_Default())),
                Port_Colors = dict(N.get("PortColors", self._Node_Port_Colors_Default())),
            )
            self.Select_Node(ID)
            self._Callback_Invoke("Flowchart", Event = "Paste", Data = {"ID": ID})
        except Exception as E:
            self._GUI.Error(f"{self._Type} - Paste - {E}")

    def On_Key_Undo(self, Event = None):
        try:
            self.Undo()
        except Exception as E:
            self._GUI.Error(f"{self._Type} - On_Key_Undo - {E}")

    def On_Key_Redo(self, Event = None):
        try:
            self.Redo()
        except Exception as E:
            self._GUI.Error(f"{self._Type} - On_Key_Redo - {E}")

    def On_Key_Copy(self, Event = None):
        try:
            self.Copy()
        except Exception as E:
            self._GUI.Error(f"{self._Type} - On_Key_Copy - {E}")

    def On_Key_Paste(self, Event = None):
        try:
            self.Paste()
        except Exception as E:
            self._GUI.Error(f"{self._Type} - On_Key_Paste - {E}")

    def On_Key_Delete(self, Event = None):
        try:
            if self._Selected_Edge_Id is not None:
                self.Remove_Edge(self._Selected_Edge_Id)
                return
            if self._Selected_Node_Id is not None:
                self.Remove_Node(self._Selected_Node_Id)
        except Exception as E:
            self._GUI.Error(f"{self._Type} - On_Key_Delete - {E}")

    def On_Click(self, Event):
        try:
            CX, CY = self._Event_Canvas_XY(Event)
            _Double_Click_Tol = float(self._Unscale(6.0))
            _Port_Hit_Tol = float(self._Unscale(max(12.0, float(self._Scale(float(self._Port_Radius))) + 10.0)))
            Now = time.time()
            Double = False
            if self._Last_Click_Time is not None and Now - float(self._Last_Click_Time) <= float(self._Double_Click_Threshold):
                if self._Last_Click_Pos is not None:
                    PX, PY = self._Last_Click_Pos
                    if math.hypot(float(CX) - float(PX), float(CY) - float(PY)) <= float(_Double_Click_Tol):
                        Double = True
            self._Last_Click_Time = Now
            self._Last_Click_Pos = (float(CX), float(CY))
            Kind, ID = self._Pick_Item(CX, CY)
            if Kind == "Node":
                if bool(self._Disabled_Nodes.get(ID, False)) or bool(self._Locked_Nodes.get(ID, False)):
                    self.Select_Node(ID)
                    return
                Hit = self._Node_Port_Hit(ID, CX, CY, Tol = float(_Port_Hit_Tol))
                if Hit is not None:
                    Side, Index = Hit
                    self.Select_Node(ID)
                    P = self._Node_Port_Point(int(ID), str(Side), int(Index))
                    D = 1e30
                    if P is not None:
                        PX, PY = P
                        D = math.hypot(float(CX) - float(PX), float(CY) - float(PY))
                    _Port_Click_Tol = float(self._Port_Radius) * 1.25
                    if D > float(_Port_Click_Tol):
                        Pick = self._Reconnect_Pick_Edge(int(ID), str(Side), int(Index))
                        if Pick is not None:
                            Eid, End = Pick
                            E = self._Edges.get(int(Eid), None)
                            if E is None:
                                return
                            self._Reconnect_Edge_Id = int(Eid)
                            self._Reconnect_End = str(End)
                            self._Reconnect_Armed_Pos = (float(CX), float(CY))
                            if str(End) == "From":
                                self._Reconnect_Fixed = (int(E.get("ToID", 0)), str(E.get("ToSide", "Left")), int(E.get("ToIndex", 0)))
                            else:
                                self._Reconnect_Fixed = (int(E.get("FromID", 0)), str(E.get("FromSide", "Right")), int(E.get("FromIndex", 0)))
                            FN, FS, FI = self._Reconnect_Fixed
                            self._Reconnect_Start_Point = self._Node_Port_Point(int(FN), str(FS), int(FI))
                            self._Pending_Connect = None
                            self._Connect_Armed_Pos = None
                            self._Connect_Start_Point = None
                            self._Drag_Mode = "reconnectarmed"
                            self._Drag_Node_Id = None
                            self.Render()
                            return
                    if self._Pending_Connect is None:
                        self._Pending_Connect = (int(ID), str(Side), int(Index))
                        self._Connect_Armed_Pos = (float(CX), float(CY))
                        self._Connect_Start_Point = self._Node_Port_Point(int(ID), str(Side), int(Index))
                        self._Drag_Mode = "connect_armed"
                        self._Drag_Node_Id = None
                        self._Callback_Invoke("Flowchart", Event = "BeginConnect", Data = {"NodeID": int(ID), "Side": str(Side), "Index": int(Index)})
                        self.Render()
                        return
                    return
                self.Select_Node(ID)
                self._Drag_Mode = "move"
                self._Drag_Node_Id = ID
                self._Drag_Start_Pos = (float(CX), float(CY))
                NX = float(self._Nodes[ID]["X"])
                NY = float(self._Nodes[ID]["Y"])
                self._Drag_Offset_X = float(CX) - NX
                self._Drag_Offset_Y = float(CY) - NY
                if Double:
                    self._Callback_Invoke("Node", ID = ID, Event = "DoubleClick")
                return
            if Kind == "Edge" and ID is not None:
                self.Select_Edge(ID)
                End = self._Edge_End_Hit(int(ID), float(CX), float(CY), Tol = float(_Port_Hit_Tol))
                if End is None:
                    _Edge_Click_Tol = float(self._Unscale(10.0))
                    End = self._Edge_Half_Hit(int(ID), float(CX), float(CY), Tol = float(_Edge_Click_Tol))
                if End is not None:
                    E = self._Edges.get(int(ID), None)
                    if E is None:
                        return
                    if bool(self._Disabled_Edges.get(int(ID), False)) or bool(self._Locked_Edges.get(int(ID), False)):
                        return
                    self._Reconnect_Edge_Id = int(ID)
                    self._Reconnect_End = str(End)
                    self._Reconnect_Armed_Pos = (float(CX), float(CY))
                    if str(End) == "From":
                        self._Reconnect_Fixed = (int(E.get("ToID", 0)), str(E.get("ToSide", "Left")), int(E.get("ToIndex", 0)))
                    else:
                        self._Reconnect_Fixed = (int(E.get("FromID", 0)), str(E.get("FromSide", "Right")), int(E.get("FromIndex", 0)))
                    FN, FS, FI = self._Reconnect_Fixed
                    self._Reconnect_Start_Point = self._Node_Port_Point(int(FN), str(FS), int(FI))
                    self._Drag_Mode = "reconnectarmed"
                    self._Drag_Node_Id = None
                    return
                return
            self._Selected_Node_Id = None
            self._Selected_Edge_Id = None
            self._Pending_Connect = None
            self._Connect_Armed_Pos = None
            self._Connect_Start_Point = None
            self._Drag_Mode = "pan"
            self._Drag_Node_Id = None
            try:
                self._Drag_Start_Pos = (float(getattr(Event, "x", 0.0)), float(getattr(Event, "y", 0.0)))
            except:
                self._Drag_Start_Pos = None
            try:
                self._Canvas._Frame.scan_mark(int(getattr(Event, "x", 0)), int(getattr(Event, "y", 0)))
            except:
                pass
            self.Render()
        except Exception as E:
            self._GUI.Error(f"{self._Type} - On_Click - {E}")

    def On_Drag(self, Event):
        try:
            if self._Drag_Mode == "pan":
                try:
                    self._Canvas._Frame.scan_dragto(int(getattr(Event, "x", 0)), int(getattr(Event, "y", 0)), gain = 1)
                except:
                    pass
                try:
                    self._Scrollbars_Update_Visibility()
                except:
                    pass
                return
            self._Auto_Scroll_On_Drag(Event)
            CX, CY = self._Event_Canvas_XY(Event)
            if self._Drag_Mode == "connect_armed":
                if self._Connect_Armed_Pos is None or self._Connect_Start_Point is None or self._Pending_Connect is None:
                    self._Drag_Mode = "none"
                    return
                AX, AY = self._Connect_Armed_Pos
                SCX = float(self._Scale(CX))
                SCY = float(self._Scale(CY))
                SAX = float(self._Scale(AX))
                SAY = float(self._Scale(AY))
                if math.hypot(float(SCX) - float(SAX), float(SCY) - float(SAY)) < float(self._Connect_Drag_Threshold):
                    return
                self._Drag_Mode = "connect"
                SX, SY = self._Connect_Start_Point
                AId, ASide, AIdx = self._Pending_Connect
                Color = str(self._Port_Color_Effective(AId, ASide, AIdx))
                SSX = float(self._Scale(SX))
                SSY = float(self._Scale(SY))
                if self._Preview_Line_Item is None:
                    try:
                        self._Preview_Line_Item = self._Canvas._Frame.create_line(
                            float(SSX), float(SSY), float(SCX), float(SCY),
                            fill = Color,
                            width = max(1.0, float(self._Scale(float(self._Thickness))))
                        )
                        try:
                            self._Canvas._Frame.tag_raise(self._Preview_Line_Item)
                        except:
                            pass
                    except:
                        self._Preview_Line_Item = None
                if self._Preview_Port_Item is None:
                    try:
                        R = float(self._Port_Radius)
                        SR = float(self._Scale(R))
                        if self._Port_Is_Input(ASide):
                            self._Preview_Port_Item = self._Canvas._Frame.create_rectangle(
                                float(SCX) - SR, float(SCY) - SR, float(SCX) + SR, float(SCY) + SR,
                                outline = "#000000",
                                fill = Color,
                                width = max(1.0, float(self._Scale(2.0)))
                            )
                        else:
                            Pts = []
                            for A in [0.0, 60.0, 120.0, 180.0, 240.0, 300.0]:
                                Rad = math.radians(A)
                                Pts.append(float(SCX) + SR * math.cos(Rad))
                                Pts.append(float(SCY) + SR * math.sin(Rad))
                            self._Preview_Port_Item = self._Canvas._Frame.create_polygon(
                                *Pts,
                                outline = "#000000",
                                fill = Color,
                                width = max(1.0, float(self._Scale(2.0)))
                            )
                        try:
                            self._Canvas._Frame.tag_raise(self._Preview_Port_Item)
                        except:
                            pass
                    except:
                        self._Preview_Port_Item = None
                return
            if self._Drag_Mode == "connect":
                if self._Connect_Start_Point is None or self._Pending_Connect is None:
                    return
                SX, SY = self._Connect_Start_Point
                SCX = float(self._Scale(CX))
                SCY = float(self._Scale(CY))
                SSX = float(self._Scale(SX))
                SSY = float(self._Scale(SY))
                if self._Preview_Line_Item is not None:
                    try:
                        self._Canvas._Frame.coords(self._Preview_Line_Item, float(SSX), float(SSY), float(SCX), float(SCY))
                    except:
                        pass
                if self._Preview_Port_Item is not None:
                    try:
                        R = float(self._Port_Radius)
                        SR = float(self._Scale(R))
                        AId, ASide, AIdx = self._Pending_Connect
                        if self._Port_Is_Input(ASide):
                            self._Canvas._Frame.coords(self._Preview_Port_Item, float(SCX) - SR, float(SCY) - SR, float(SCX) + SR, float(SCY) + SR)
                        else:
                            Pts = []
                            for A in [0.0, 60.0, 120.0, 180.0, 240.0, 300.0]:
                                Rad = math.radians(A)
                                Pts.append(float(SCX) + SR * math.cos(Rad))
                                Pts.append(float(SCY) + SR * math.sin(Rad))
                            self._Canvas._Frame.coords(self._Preview_Port_Item, *Pts)
                    except:
                        pass
                return
            if self._Drag_Mode == "reconnectarmed":
                if self._Reconnect_Armed_Pos is None or self._Reconnect_Start_Point is None or self._Reconnect_Edge_Id is None:
                    self._Drag_Mode = "none"
                    return
                AX, AY = self._Reconnect_Armed_Pos
                if math.hypot(float(CX) - float(AX), float(CY) - float(AY)) <= float(self._Connect_Drag_Threshold):
                    return
                self._Drag_Mode = "reconnect"
            if self._Drag_Mode == "reconnect":
                if self._Reconnect_Start_Point is None or self._Reconnect_End is None:
                    return
                SX, SY = self._Reconnect_Start_Point
                SCX = float(self._Scale(CX))
                SCY = float(self._Scale(CY))
                SSX = float(self._Scale(SX))
                SSY = float(self._Scale(SY))
                if self._Preview_Line_Item is None:
                    try:
                        self._Preview_Line_Item = self._Canvas._Frame.create_line(
                            float(SSX), float(SSY), float(SCX), float(SCY),
                            fill = "#000000",
                            width = max(1.0, float(self._Scale(float(self._Thickness))))
                        )
                        try:
                            self._Canvas._Frame.tag_raise(self._Preview_Line_Item)
                        except:
                            pass
                    except:
                        self._Preview_Line_Item = None
                else:
                    try:
                        self._Canvas._Frame.coords(self._Preview_Line_Item, float(SSX), float(SSY), float(SCX), float(SCY))
                    except:
                        pass
                if self._Preview_Port_Item is None:
                    try:
                        R = float(self._Port_Radius)
                        SR = float(self._Scale(R))
                        Moving_Is_Input = (str(self._Reconnect_End) == "To")
                        if Moving_Is_Input:
                            self._Preview_Port_Item = self._Canvas._Frame.create_rectangle(
                                float(SCX) - SR, float(SCY) - SR, float(SCX) + SR, float(SCY) + SR,
                                outline = "#000000",
                                fill = "#FFFFFF",
                                width = max(1.0, float(self._Scale(2.0)))
                            )
                        else:
                            Pts = []
                            for A in [0.0, 60.0, 120.0, 180.0, 240.0, 300.0]:
                                Rad = math.radians(A)
                                Pts.append(float(SCX) + SR * math.cos(Rad))
                                Pts.append(float(SCY) + SR * math.sin(Rad))
                            self._Preview_Port_Item = self._Canvas._Frame.create_polygon(
                                *Pts,
                                outline = "#000000",
                                fill = "#FFFFFF",
                                width = max(1.0, float(self._Scale(2.0)))
                            )
                        try:
                            self._Canvas._Frame.tag_raise(self._Preview_Port_Item)
                        except:
                            pass
                    except:
                        self._Preview_Port_Item = None
                else:
                    try:
                        R = float(self._Port_Radius)
                        SR = float(self._Scale(R))
                        Moving_Is_Input = (str(self._Reconnect_End) == "To")

                        if Moving_Is_Input:
                            self._Canvas._Frame.coords(self._Preview_Port_Item, float(SCX) - SR, float(SCY) - SR, float(SCX) + SR, float(SCY) + SR)
                        else:
                            Pts = []
                            for A in [0.0, 60.0, 120.0, 180.0, 240.0, 300.0]:
                                Rad = math.radians(A)
                                Pts.append(float(SCX) + SR * math.cos(Rad))
                                Pts.append(float(SCY) + SR * math.sin(Rad))
                            self._Canvas._Frame.coords(self._Preview_Port_Item, *Pts)
                    except:
                        pass
                return
            if self._Drag_Mode != "move" or self._Drag_Node_Id is None:
                return
            ID = self._Drag_Node_Id
            if bool(self._Disabled_Nodes.get(ID, False)):
                return
            NX = float(CX) - float(self._Drag_Offset_X)
            NY = float(CY) - float(self._Drag_Offset_Y)
            G = getattr(self, "_Route_Grid", 10.0)
            try:
                G = float(G)
            except:
                G = 0.0
            if G > 0.0:
                NX = float(round(float(NX) / float(G)) * float(G))
                NY = float(round(float(NY) / float(G)) * float(G))
            NX, NY = self._Clamp_Pos(NX, NY)
            if (
                self._Drag_Ghost_Item is None
                or self._Drag_Ghost_Node_Id is None
                or int(self._Drag_Ghost_Node_Id) != int(ID)
            ):
                self._Drag_Ghost_Begin(ID)
            self._Drag_Ghost_Update(ID, float(NX), float(NY))
            self.Update_Scrollregion()
            if self._Callback_Mode == "Continuous":
                self._Callback_Invoke("Node", ID = ID, Event = "Update")
        except Exception as E:
            self._GUI.Error(f"{self._Type} - On_Drag - {E}")

    def On_Release(self, Event):
        try:
            if self._Drag_Mode == "pan":
                self._Drag_Mode = "none"
                self._Drag_Node_Id = None
                self._Drag_Start_Pos = None
                return
            CX, CY = self._Event_Canvas_XY(Event)
            _Port_Hit_Tol = float(self._Unscale(max(12.0, float(self._Scale(float(self._Port_Radius))) + 10.0)))
            if self._Drag_Mode == "reconnect":
                Kind, ID = self._Pick_Item(CX, CY)
                Hit = None
                if Kind == "Node" and ID is not None:
                    Hit = self._Node_Port_Hit(ID, CX, CY, Tol = float(_Port_Hit_Tol))
                if self._Preview_Line_Item is not None:
                    try: self._Canvas._Frame.delete(self._Preview_Line_Item)
                    except: pass
                if self._Preview_Port_Item is not None:
                    try: self._Canvas._Frame.delete(self._Preview_Port_Item)
                    except: pass
                self._Preview_Line_Item = None
                self._Preview_Port_Item = None
                Eid = self._Reconnect_Edge_Id
                End = self._Reconnect_End
                Fixed = self._Reconnect_Fixed
                self._Drag_Mode = "none"
                self._Reconnect_Edge_Id = None
                self._Reconnect_End = None
                self._Reconnect_Fixed = None
                self._Reconnect_Armed_Pos = None
                self._Reconnect_Start_Point = None
                if Eid is None or Fixed is None or Hit is None or Kind != "Node" or ID is None:
                    self.Render()
                    return
                TNode = int(ID)
                TSide = str(Hit[0])
                TIdx  = int(Hit[1])
                if str(End) == "From":
                    if not self._Port_Is_Output(TSide):
                        self.Render()
                        return
                    From_Id, From_Side, From_Index = TNode, TSide, TIdx
                    To_Id, To_Side, To_Index = int(Fixed[0]), str(Fixed[1]), int(Fixed[2])
                else:
                    if not self._Port_Is_Input(TSide):
                        self.Render()
                        return
                    From_Id, From_Side, From_Index = int(Fixed[0]), str(Fixed[1]), int(Fixed[2])
                    To_Id, To_Side, To_Index = TNode, TSide, TIdx
                if self._Input_Single_Edge:
                    Hits = list(self._Port_Connected_Edges(int(To_Id), str(To_Side), int(To_Index)) or [])
                    Hits = [(Other_Id, Other_End) for (Other_Id, Other_End) in Hits if int(Other_Id) != int(Eid)]
                    if Hits:
                        self.Render()
                        return
                if self._Output_Single_Edge:
                    Hits = list(self._Port_Connected_Edges(int(From_Id), str(From_Side), int(From_Index)) or [])
                    Hits = [(Other_Id, Other_End) for (Other_Id, Other_End) in Hits if int(Other_Id) != int(Eid)]
                    if Hits:
                        self.Render()
                        return
                E = self._Edges.get(int(Eid), None)
                if E is None:
                    self.Render()
                    return
                self._Undo_Push()
                E["FromID"] = int(From_Id)
                E["FromSide"] = str(From_Side)
                E["FromIndex"] = int(From_Index)
                E["ToID"] = int(To_Id)
                E["ToSide"] = str(To_Side)
                E["ToIndex"] = int(To_Index)
                E["Points"] = list(self._Edge_Route(
                    int(E["FromID"]), str(E["FromSide"]),
                    int(E["ToID"]),   str(E["ToSide"]),
                    int(E["FromIndex"]), int(E["ToIndex"]),
                    Ignore_Edge_Id = int(Eid)
                ))
                if str(End) == "From":
                    E["Color"] = str(self._Port_Color_Effective(int(E["FromID"]), str(E["FromSide"]), int(E["FromIndex"])))
                self.Render()
                return
            if self._Drag_Mode == "connect":
                Kind, ID = self._Pick_Item(CX, CY)
                Hit = None
                if Kind == "Node" and ID is not None:
                    Hit = self._Node_Port_Hit(ID, CX, CY, Tol = float(_Port_Hit_Tol))

                if self._Preview_Line_Item is not None:
                    try:
                        self._Canvas._Frame.delete(self._Preview_Line_Item)
                    except:
                        pass
                if self._Preview_Port_Item is not None:
                    try:
                        self._Canvas._Frame.delete(self._Preview_Port_Item)
                    except:
                        pass
                self._Preview_Line_Item = None
                self._Preview_Port_Item = None
                if self._Pending_Connect is not None and Hit is not None and Kind == "Node" and ID is not None:
                    AId, ASide, AIdx = self._Pending_Connect
                    BId, BSide, BIdx = int(ID), str(Hit[0]), int(Hit[1])
                    AOut = self._Port_Is_Output(ASide)
                    BOut = self._Port_Is_Output(BSide)
                    AIn  = self._Port_Is_Input(ASide)
                    BIn  = self._Port_Is_Input(BSide)
                    if AOut and BIn or BOut and AIn:
                        if AOut and BIn:
                            self.Add_Edge(From_Id = AId, From_Side = ASide, To_Id = BId, To_Side = BSide, From_Index = AIdx, To_Index = BIdx, Color = None)
                        else:
                            self.Add_Edge(From_Id = BId, From_Side = BSide, To_Id = AId, To_Side = ASide, From_Index = BIdx, To_Index = AIdx, Color = None)
                self._Pending_Connect = None
                self._Connect_Armed_Pos = None
                self._Connect_Start_Point = None
                self._Drag_Mode = "none"
                self.Render()
                return
            if self._Drag_Mode == "connect_armed":
                self._Drag_Mode = "none"
                return
            if self._Drag_Mode == "move" and self._Drag_Node_Id is not None:
                ID = self._Drag_Node_Id
                if bool(self._Disabled_Nodes.get(ID, False)):
                    self._Drag_Ghost_End()
                    self._Drag_Mode = "none"
                    self._Drag_Node_Id = None
                    self._Drag_Start_Pos = None
                    return
                NX = float(CX) - float(self._Drag_Offset_X)
                NY = float(CY) - float(self._Drag_Offset_Y)
                G = getattr(self, "_Route_Grid", 10.0)
                try:
                    G = float(G)
                except:
                    G = 0.0
                if G > 0.0:
                    NX = float(round(float(NX) / float(G)) * float(G))
                    NY = float(round(float(NY) / float(G)) * float(G))
                NX, NY = self._Clamp_Pos(NX, NY)
                self._Undo_Push()
                self._Nodes[ID]["X"] = float(NX)
                self._Nodes[ID]["Y"] = float(NY)
                self._Update_Edges_For_Node(ID)
                self._Drag_Ghost_End()
                self.Render()
                self._Callback_Invoke("Node", ID=ID, Event="Update")
                self._Drag_Mode = "none"
                self._Drag_Node_Id = None
                self._Drag_Start_Pos = None
                return
        except Exception as E:
            self._GUI.Error(f"{self._Type} - On_Release - {E}")

    def On_Motion(self, Event):
        try:
            CX, CY = self._Event_Canvas_XY(Event)
            _Port_Hit_Tol = float(self._Unscale(max(12.0, float(self._Scale(float(self._Port_Radius))) + 6.0)))
            Kind, ID = self._Pick_Item(CX, CY)
            if Kind == "Node" and ID is not None:
                Hit = self._Node_Port_Hit(ID, CX, CY, Tol = float(_Port_Hit_Tol))
                if Hit is not None:
                    try:
                        self._Canvas._Frame.configure(cursor = "crosshair")
                    except:
                        pass
                    return
                try:
                    self._Canvas._Frame.configure(cursor = "fleur")
                except:
                    pass
                return
            if Kind == "Edge":
                try:
                    self._Canvas._Frame.configure(cursor = "hand2")
                except:
                    pass
                return
            try:
                self._Canvas._Frame.configure(cursor = "arrow")
            except:
                pass
        except Exception as E:
            self._GUI.Error(f"{self._Type} - On_Motion - {E}")

    def _Build_Context_Menu(self, Context_Kind = "Canvas", Node_Id = None, Port = None, Edge_Id = None):
        try:
            if Tk is None:
                return None
            M = Tk.Menu(self._Canvas._Frame, tearoff = 0)
            CanUndo = bool(self._Undo_Stack)
            CanRedo = bool(self._Redo_Stack)
            CanPaste = bool(self._Copy_Buffer)
            if Context_Kind in ["Canvas", "Object"]:
                if CanUndo:
                    M.add_command(label = "Undo", command = self.Undo)
                if CanRedo:
                    M.add_command(label = "Redo", command = self.Redo)
                if Context_Kind == "Object" and Node_Id is not None:
                    M.add_command(label = "Copy", command = self.Copy)
                if CanPaste:
                    M.add_command(label = "Paste", command = self.Paste)
                if Context_Kind == "Object" and Node_Id is not None:
                    M.add_command(label = "Delete", command = self._Context_Delete_Selected)
                    NDis = bool(self._Disabled_Nodes.get(Node_Id, False))
                    if NDis:
                        M.add_command(label = "Enable", command = self._Context_Enable_Selected)
                    else:
                        M.add_command(label = "Disable", command = self._Context_Disable_Selected)
                    NLck = bool(self._Locked_Nodes.get(Node_Id, False))
                    if NLck:
                        M.add_command(label = "Unlock", command = self._Context_Unlock_Selected)
                    else:
                        M.add_command(label = "Lock", command = self._Context_Lock_Selected)
            if Context_Kind == "Port" and Port is not None:
                PNode, PSide, PIndex = Port
                if PNode in self._Nodes:
                    N = self._Nodes[PNode]
                    if "PortDisabled" not in N or not isinstance(N.get("PortDisabled"), set):
                        N["PortDisabled"] = set()
                    Key = f"{str(PSide)}:{int(PIndex)}"

                    def Disconnect_Port():
                        self._Undo_Push()
                        Remove = []
                        for Eid, E in list(self._Edges.items()):
                            A = int(E.get("FromID", -1)) == int(PNode) and str(E.get("FromSide", "")) == str(PSide) and int(E.get("FromIndex", -1)) == int(PIndex)
                            B = int(E.get("ToID", -1)) == int(PNode) and str(E.get("ToSide", "")) == str(PSide) and int(E.get("ToIndex", -1)) == int(PIndex)
                            if A or B:
                                Remove.append(Eid)
                        for Eid in Remove:
                            self.Remove_Edge(Eid)

                    def Disable_Port():
                        Disconnect_Port()
                        N["PortDisabled"].add(Key)
                        self._Pending_Connect = None
                        self.Render()

                    def Enable_Port():
                        if Key in N["PortDisabled"]:
                            N["PortDisabled"].remove(Key)
                        self.Render()
                    M.add_command(label = "Disconnect Port", command = Disconnect_Port)
                    if Key in N["PortDisabled"]:
                        M.add_command(label = "Enable Port", command = Enable_Port)
                    else:
                        M.add_command(label = "Disable Port", command = Disable_Port)
            if Context_Kind == "Edge" and Edge_Id is not None:
                if CanUndo or CanRedo:
                    if CanUndo:
                        M.add_command(label = "Undo", command = self.Undo)
                    if CanRedo:
                        M.add_command(label = "Redo", command = self.Redo)
                M.add_command(label = "Delete", command = self._Context_Delete_Selected)
                EDis = bool(self._Disabled_Edges.get(Edge_Id, False))
                if EDis:
                    M.add_command(label = "Enable", command = self._Context_Enable_Selected)
                else:
                    M.add_command(label = "Disable", command = self._Context_Disable_Selected)
                ELck = bool(self._Locked_Edges.get(Edge_Id, False))
                if ELck:
                    M.add_command(label = "Unlock", command = self._Context_Unlock_Selected)
                else:
                    M.add_command(label = "Lock", command = self._Context_Lock_Selected)
            Info_Node_Id = None
            if Context_Kind == "Object" and Node_Id is not None:
                Info_Node_Id = int(Node_Id)
            elif Context_Kind == "Port" and Port is not None:
                try:
                    Info_Node_Id = int(Port[0])
                except:
                    Info_Node_Id = None
            Node_Info = None
            if Info_Node_Id is not None:
                try:
                    Node_Info = self.Get_Node(Info_Node_Id)
                except:
                    try:
                        Node_Info = dict(self._Nodes.get(Info_Node_Id, None) or None)
                    except:
                        Node_Info = None
            Node_Type = ""
            try:
                if isinstance(Node_Info, dict):
                    Node_Type = str(Node_Info.get("Type", ""))
            except:
                Node_Type = ""
            Custom_Added = 0
            for Item in list(self._Context_Menu_Items or []):
                try:
                    Label = str(Item.get("Label", ""))
                    Function = Item.get("Function", None)
                    Allowed = Item.get("Type", "")
                    Show = False
                    if Allowed is None:
                        Show = True
                    elif isinstance(Allowed, (list, tuple, set)):
                        Show = Node_Type in [str(A) for A in list(Allowed)]
                    else:
                        Allowed = str(Allowed)
                        if Allowed == "":
                            Show = True
                        elif Allowed == Node_Type:
                            Show = True
                    if not Show:
                        continue
                    if Custom_Added == 0:
                        try:
                            if M.index("end") is not None:
                                M.add_separator()
                        except:
                            pass
                    M.add_command(
                        label = Label,
                        command = (lambda F = Function, Info = Node_Info: self._Context_Menu_Invoke(F, Info))
                    )
                    Custom_Added += 1
                except Exception as E:
                    self._GUI.Error(f"{self._Type} - _Build_Context_Menu Custom - {E}")
            return M
        except Exception as E:
            self._GUI.Error(f"{self._Type} - _Build_Context_Menu - {E}")
            return None

    def On_Right_Click(self, Event):
        try:
            CX, CY = self._Event_Canvas_XY(Event)
            _Port_Hit_Tol = float(self._Unscale(max(12.0, float(self._Scale(float(self._Port_Radius))) + 10.0)))
            Kind, ID = self._Pick_Item(CX, CY)
            Ctx = "Canvas"
            Node_Id = None
            Port = None
            Edge_Id = None
            if Kind == "Node" and ID is not None:
                Hit = self._Node_Port_Hit(ID, CX, CY, Tol = float(_Port_Hit_Tol))
                Node_Id = int(ID)
                if Hit is not None:
                    Side, Index = Hit
                    Port = (int(ID), str(Side), int(Index))
                    Ctx = "Port"
                    self.Select_Node(ID)
                else:
                    Ctx = "Object"
                    self.Select_Node(ID)
            elif Kind == "Edge" and ID is not None:
                Ctx = "Edge"
                Edge_Id = int(ID)
                self.Select_Edge(ID)
            else:
                Ctx = "Canvas"
            self._Context_Menu = self._Build_Context_Menu(Context_Kind = Ctx, Node_Id = Node_Id, Port = Port, Edge_Id = Edge_Id)
            if self._Context_Menu is None:
                return
            try:
                self._Context_Menu.tk_popup(Event.x_root, Event.y_root)
            except:
                pass
            self._Callback_Invoke("Flowchart", Event = "ContextMenu", Data = {"X": float(CX), "Y": float(CY), "Context": str(Ctx)})
        except Exception as E:
            self._GUI.Error(f"{self._Type} - On_Right_Click - {E}")

    def _Context_Add_Node(self):
        try:
            self._Undo_Push()
            CW = self.Canvas_Width()
            CH = self.Canvas_Height()
            self.Add_Node(X = 0.5 * CW, Y = 0.5 * CH, Width = 180.0, Height = 120.0, Color = "#4F8EF7", Fill = "#DC7633", Title = "Object", Description = "", Port_Counts = self._Node_Port_Counts_Default())
        except Exception as E:
            self._GUI.Error(f"{self._Type} - _Context_Add_Node - {E}")

    def _Context_Delete_Selected(self):
        try:
            if self._Selected_Edge_Id is not None:
                self.Remove_Edge(self._Selected_Edge_Id)
                return
            if self._Selected_Node_Id is not None:
                self.Remove_Node(self._Selected_Node_Id)
        except Exception as E:
            self._GUI.Error(f"{self._Type} - _Context_Delete_Selected - {E}")

    def _Context_Lock_Selected(self):
        try:
            if self._Selected_Node_Id is not None:
                self.Lock_Node(self._Selected_Node_Id)
                return
            if self._Selected_Edge_Id is not None:
                self.Lock_Edge(self._Selected_Edge_Id)
        except Exception as E:
            self._GUI.Error(f"{self._Type} - _Context_Lock_Selected - {E}")

    def _Context_Unlock_Selected(self):
        try:
            if self._Selected_Node_Id is not None:
                self.Unlock_Node(self._Selected_Node_Id)
                return
            if self._Selected_Edge_Id is not None:
                self.Unlock_Edge(self._Selected_Edge_Id)
        except Exception as E:
            self._GUI.Error(f"{self._Type} - _Context_Unlock_Selected - {E}")

    def _Context_Enable_Selected(self):
        try:
            if self._Selected_Node_Id is not None:
                self.Enable_Node(self._Selected_Node_Id)
                return
            if self._Selected_Edge_Id is not None:
                self.Enable_Edge(self._Selected_Edge_Id)
        except Exception as E:
            self._GUI.Error(f"{self._Type} - _Context_Enable_Selected - {E}")

    def _Context_Disable_Selected(self):
        try:
            if self._Selected_Node_Id is not None:
                self.Disable_Node(self._Selected_Node_Id)
                return
            if self._Selected_Edge_Id is not None:
                self.Disable_Edge(self._Selected_Edge_Id)
        except Exception as E:
            self._GUI.Error(f"{self._Type} - _Context_Disable_Selected - {E}")

    def Add_Node(self, X = None, Y = None, Width = None, Height = None, Color = "#4F8EF7", Fill = "#DC7633", Title = "", Description = "", Type = "", Ports = None, Port_Counts = None, Port_Names = None, Port_Colors = None):
        try:
            self._Undo_Push()
            CW = self.Canvas_Width()
            CH = self.Canvas_Height()
            if X is None:
                X = 0.5 * CW
            if Y is None:
                Y = 0.5 * CH
            if Width is None:
                Width = 160.0
            if Height is None:
                Height = 100.0
            X, Y = self._Clamp_Pos(X, Y)
            ID = int(self._Node_Id_Next)
            self._Node_Id_Next += 1
            if Ports is None:
                Ports = self._Node_Ports_Default()
            if Port_Counts is None:
                Port_Counts = self._Node_Port_Counts_Default()
            if Port_Names is None:
                Port_Names = self._Node_Port_Names_Default()
            if Port_Colors is None:
                Port_Colors = self._Node_Port_Colors_Default()
            NormCounts = self._Node_Port_Counts_Normalize(Port_Counts)
            self._Nodes[ID] = {
                "X": float(X),
                "Y": float(Y),
                "Width":  float(max(40.0, Width)),
                "Height": float(max(40.0, Height)),
                "Color": str(Color),
                "Fill":  str(Fill),
                "Title": str(Title),
                "Description": str(Description),
                "Type": str(Type),
                "Ports": dict(Ports),
                "PortCounts": NormCounts,
                "PortNames":  self._Node_Port_Names_Normalize(Port_Names, Port_Counts = NormCounts),
                "PortColors": self._Node_Port_Colors_Normalize(Port_Colors, Port_Counts = NormCounts),
                "Item": None,
                "TitleItem": None,
                "DescItem": None,
                "FieldItems": [],
                "PortItems": {},
            }
            self._Disabled_Nodes[ID] = False
            self._Locked_Nodes[ID] = False
            self._Node_Draw(ID)
            self.Render()
            self.Select_Node(ID)
            self._Callback_Invoke("Node", ID = ID, Event = "Add")
            return ID
        except Exception as E:
            self._GUI.Error(f"{self._Type} - Add_Node - {E}")
            return None

    def Add_Object(self, *Args, **Kwargs):
        return self.Add_Node(*Args, **Kwargs)

    def Update_Node(self, ID = None, X = None, Y = None, Width = None, Height = None, Color = None, Fill = None, Title = None, Description = None, Type = None, Ports = None, Port_Counts = None, Port_Names = None, Port_Colors = None, Disabled = None, Locked = None):
        try:
            if ID is None:
                if not self._Nodes:
                    return ID
                ID = sorted(self._Nodes.keys())[0]
            if ID not in self._Nodes:
                return
            self._Undo_Push()
            N = self._Nodes[ID]
            if X is not None:
                N["X"] = float(self._Clamp_Pos(X, N["Y"])[0])
            if Y is not None:
                N["Y"] = float(self._Clamp_Pos(N["X"], Y)[1])
            if Width is not None:
                N["Width"] = float(max(40.0, Width))
            if Height is not None:
                N["Height"] = float(max(40.0, Height))
            if Color is not None:
                N["Color"] = str(Color)
            if Fill is not None:
                N["Fill"] = str(Fill)
            if Title is not None:
                N["Title"] = str(Title)
            if Description is not None:
                N["Description"] = str(Description)
            if Type is not None:
                N["Type"] = str(Type)
            if Ports is not None:
                N["Ports"] = dict(Ports)
            CountsChanged = False
            if Port_Counts is not None:
                N["PortCounts"] = self._Node_Port_Counts_Normalize(Port_Counts)
                CountsChanged = True
            CurCounts = N.get("PortCounts", self._Node_Port_Counts_Default())
            if Port_Names is not None:
                N["PortNames"] = self._Node_Port_Names_Normalize(Port_Names, Port_Counts = CurCounts)
            elif CountsChanged:
                N["PortNames"] = self._Node_Port_Names_Normalize(N.get("PortNames", {}), Port_Counts = CurCounts)
            if Port_Colors is not None:
                N["PortColors"] = self._Node_Port_Colors_Normalize(Port_Colors, Port_Counts = CurCounts)
            elif CountsChanged:
                N["PortColors"] = self._Node_Port_Colors_Normalize(N.get("PortColors", {}), Port_Counts = CurCounts)
            if Disabled is not None:
                self._Disabled_Nodes[ID] = bool(Disabled)
            if Locked is not None:
                self._Locked_Nodes[ID] = bool(Locked)
            self._Update_Edges_For_Node(ID)
            self.Render()
            self._Callback_Invoke("Node", ID = ID, Event = "Update")
        except Exception as E:
            self._GUI.Error(f"{self._Type} - Update_Node - {E}")

    def Update_Object(self, *Args, **Kwargs):
        return self.Update_Node(*Args, **Kwargs)

    def Remove_Node(self, ID = None):
        try:
            if isinstance(ID, str) and ID.lower() == "all":
                self._Undo_Push()
                for EachId in list(self._Nodes.keys()):
                    self.Remove_Node(EachId)
                return
            if ID is None:
                if not self._Nodes:
                    return
                ID = sorted(self._Nodes.keys())[0]
            if ID not in self._Nodes:
                return
            self._Undo_Push()
            Edges_To_Remove = []
            for Eid, E in list(self._Edges.items()):
                if int(E.get("FromID", -1)) == int(ID) or int(E.get("ToID", -1)) == int(ID):
                    Edges_To_Remove.append(Eid)
            for Eid in Edges_To_Remove:
                self.Remove_Edge(Eid)
            N = self._Nodes[ID]
            Items = []
            Items.append(N.get("Item", None))
            Items.append(N.get("TitleItem", None))
            Items.append(N.get("DescItem", None))
            Port_Items = dict(N.get("PortItems", {}) or {})
            for It in list(Port_Items.values()):
                Items.append(It)
            Port_Stub_Items = dict(N.get("PortStubItems", {}) or {})
            for It in list(Port_Stub_Items.values()):
                Items.append(It)
            Port_Name_Items = dict(N.get("PortNameItems", {}) or {})
            for It in list(Port_Name_Items.values()):
                Items.append(It)
            for It in Items:
                if It is None:
                    continue
                try:
                    self._Canvas._Frame.delete(It)
                except:
                    pass
                if It in self._Item_To_Node:
                    del self._Item_To_Node[It]
            if "PortItems" in N:
                N["PortItems"] = {}
            if "PortStubItems" in N:
                N["PortStubItems"] = {}
            if "PortNameItems" in N:
                N["PortNameItems"] = {}
            if "PortDisabled" in N:
                N["PortDisabled"] = set()
            if ID in self._Nodes:
                del self._Nodes[ID]
            if ID in self._Disabled_Nodes:
                del self._Disabled_Nodes[ID]
            if ID in self._Locked_Nodes:
                del self._Locked_Nodes[ID]
            if self._Selected_Node_Id == ID:
                self._Selected_Node_Id = None
            if self._Pending_Connect is not None and int(self._Pending_Connect[0]) == int(ID):
                self._Pending_Connect = None
            self.Render()
            self._Callback_Invoke("Node", ID = ID, Event = "Remove")
        except Exception as E:
            self._GUI.Error(f"{self._Type} - Remove_Node - {E}")

    def Remove_Object(self, *Args, **Kwargs):
        return self.Remove_Node(*Args, **Kwargs)

    def Lock_Node(self, ID = None):
        try:
            if ID is None:
                if self._Selected_Node_Id is None:
                    return
                ID = self._Selected_Node_Id
            if ID not in self._Nodes:
                return
            self._Undo_Push()
            self._Locked_Nodes[ID] = True
            self.Render()
            self._Callback_Invoke("Node", ID = ID, Event = "Lock")
        except Exception as E:
            self._GUI.Error(f"{self._Type} - Lock_Node - {E}")

    def Unlock_Node(self, ID = None):
        try:
            if ID is None:
                if self._Selected_Node_Id is None:
                    return
                ID = self._Selected_Node_Id
            if ID not in self._Nodes:
                return
            self._Undo_Push()
            self._Locked_Nodes[ID] = False
            self.Render()
            self._Callback_Invoke("Node", ID = ID, Event = "Unlock")
        except Exception as E:
            self._GUI.Error(f"{self._Type} - Unlock_Node - {E}")

    def Enable_Node(self, ID = None):
        try:
            if ID is None:
                if self._Selected_Node_Id is None:
                    return
                ID = self._Selected_Node_Id
            if ID not in self._Nodes:
                return
            self._Undo_Push()
            self._Disabled_Nodes[ID] = False
            self.Render()
            self._Callback_Invoke("Node", ID = ID, Event = "Enable")
        except Exception as E:
            self._GUI.Error(f"{self._Type} - Enable_Node - {E}")

    def Disable_Node(self, ID = None):
        try:
            if ID is None:
                if self._Selected_Node_Id is None:
                    return
                ID = self._Selected_Node_Id
            if ID not in self._Nodes:
                return
            self._Undo_Push()
            self._Disabled_Nodes[ID] = True
            self.Render()
            self._Callback_Invoke("Node", ID = ID, Event = "Disable")
        except Exception as E:
            self._GUI.Error(f"{self._Type} - Disable_Node - {E}")

    def Select_Node(self, ID):
        try:
            self._Selected_Edge_Id = None
            self._Selected_Node_Id = ID
            self.Render()
            self._Callback_Invoke("Node", ID = ID, Event = "Select")
        except Exception as E:
            self._GUI.Error(f"{self._Type} - Select_Node - {E}")

    def Select_Object(self, *Args, **Kwargs):
        return self.Select_Node(*Args, **Kwargs)

    def Get_Node(self, ID = None):
        try:
            if isinstance(ID, str) and ID.lower() == "all":
                Out = []
                for EachId in sorted(self._Nodes.keys()):
                    Out.append(self.Get_Node(EachId))
                return Out
            if ID is None:
                ID = self._Selected_Node_Id
            if ID is None or ID not in self._Nodes:
                return None
            N = self._Nodes[ID]
            return {"ID": int(ID), "X": float(N.get("X", 0.0)), "Y": float(N.get("Y", 0.0)), "Width": float(N.get("Width", 0.0)), "Height": float(N.get("Height", 0.0)), "Color": str(N.get("Color", "")), "Fill": str(N.get("Fill", "")), "Title": str(N.get("Title", "")), "Description": str(N.get("Description", "")), "Type": str(N.get("Type", "")), "Ports": dict(N.get("Ports", self._Node_Ports_Default())), "PortCounts": dict(N.get("PortCounts", self._Node_Port_Counts_Default())), "PortNames": dict(N.get("PortNames", self._Node_Port_Names_Default())), "PortColors": dict(N.get("PortColors", self._Node_Port_Colors_Default())), "Disabled": bool(self._Disabled_Nodes.get(ID, False)), "Locked": bool(self._Locked_Nodes.get(ID, False))}
        except Exception as E:
            self._GUI.Error(f"{self._Type} - Get_Node - {E}")
            return None

    def Get_Object(self, *Args, **Kwargs):
        return self.Get_Node(*Args, **Kwargs)

    def _Update_Edges_For_Node(self, Node_Id):
        try:
            try:
                Node_Id = int(Node_Id)
            except:
                return
            for Eid, E in list(self._Edges.items()):
                if int(E.get("FromID", -1)) != int(Node_Id) and int(E.get("ToID", -1)) != int(Node_Id):
                    continue
                From_Id = int(E.get("FromID", 0))
                To_Id   = int(E.get("ToID", 0))
                if From_Id not in self._Nodes or To_Id not in self._Nodes:
                    continue
                From_Side = str(E.get("FromSide", "Right"))
                To_Side   = str(E.get("ToSide", "Left"))
                From_Index = int(E.get("FromIndex", 0))
                To_Index   = int(E.get("ToIndex", 0))
                Points = self._Edge_Route(
                    int(From_Id), str(From_Side),
                    int(To_Id),   str(To_Side),
                    int(From_Index), int(To_Index),
                    Ignore_Edge_Id = int(Eid)
                )
                E["Points"] = list(Points)
                self._Edge_Draw(Eid)
        except Exception as E:
            self._GUI.Error(f"{self._Type} - _Update_Edges_For_Node - {E}")

    def _Port_Color_Effective(self, NodeId, Side, Index):
        try:
            C = self._Node_Port_Color_Get(NodeId, Side, Index, Default=None)
            if C is not None:
                return str(C)
            return str(self._Port_Fill(NodeId, Side, Index))
        except Exception as E:
            self._GUI.Error(f"{self._Type} - _Port_Color_Effective - {E}")
            return "#000000"

    def Add_Edge(self, From_Id, From_Side, To_Id, To_Side, Color = None, From_Index = 0, To_Index = 0):
        try:
            if From_Id not in self._Nodes or To_Id not in self._Nodes:
                return None
            if bool(self._Disabled_Nodes.get(From_Id, False)) or bool(self._Disabled_Nodes.get(To_Id, False)):
                return None
            PortsA = self._Nodes[From_Id].get("Ports", self._Node_Ports_Default())
            PortsB = self._Nodes[To_Id].get("Ports", self._Node_Ports_Default())
            if not PortsA.get(str(From_Side), False):
                return None
            if not PortsB.get(str(To_Side), False):
                return None
            AOut = self._Port_Is_Output(From_Side)
            BIn  = self._Port_Is_Input(To_Side)
            if not (AOut and BIn):
                return None
            if self._Input_Single_Edge:
                Hits = list(self._Port_Connected_Edges(int(To_Id), str(To_Side), int(To_Index)) or [])
                if Hits:
                    return None
            if self._Output_Single_Edge:
                Hits = list(self._Port_Connected_Edges(int(From_Id), str(From_Side), int(From_Index)) or [])
                if Hits:
                    return None
            NA = self._Nodes.get(From_Id, {})
            NB = self._Nodes.get(To_Id, {})
            if "PortDisabled" not in NA or not isinstance(NA.get("PortDisabled"), set):
                NA["PortDisabled"] = set()
            if "PortDisabled" not in NB or not isinstance(NB.get("PortDisabled"), set):
                NB["PortDisabled"] = set()
            if f"{str(From_Side)}:{int(From_Index)}" in NA["PortDisabled"]:
                return None
            if f"{str(To_Side)}:{int(To_Index)}" in NB["PortDisabled"]:
                return None
            for Eid, E in list(self._Edges.items()):
                Same_From = int(E.get("FromID", -1)) == int(From_Id) and str(E.get("FromSide", "")) == str(From_Side) and int(E.get("FromIndex", -1)) == int(From_Index)
                Same_To   = int(E.get("ToID", -1))   == int(To_Id)   and str(E.get("ToSide", ""))   == str(To_Side)   and int(E.get("ToIndex", -1))   == int(To_Index)
                if Same_From and Same_To:
                    return None
            if Color is None:
                Color = str(self._Port_Color_Effective(From_Id, From_Side, From_Index))
            self._Undo_Push()
            ID = int(self._Edge_Id_Next)
            self._Edge_Id_Next += 1
            Points = self._Edge_Route(
                From_Id, str(From_Side), To_Id, str(To_Side),
                int(From_Index), int(To_Index),
                Ignore_Edge_Id = None
            )
            self._Edges[ID] = {
                "FromID": int(From_Id),
                "FromSide": str(From_Side),
                "FromIndex": int(From_Index),
                "ToID": int(To_Id),
                "ToSide": str(To_Side),
                "ToIndex": int(To_Index),
                "Points": list(Points),
                "Color": str(Color),
                "Item": None
            }
            self._Disabled_Edges[ID] = False
            self._Locked_Edges[ID] = False
            self._Edge_Draw(ID)
            self.Render()
            self.Select_Edge(ID)
            self._Callback_Invoke("Edge", ID = ID, Event = "Add")
            return ID
        except Exception as E:
            self._GUI.Error(f"{self._Type} - Add_Edge - {E}")
            return None

    def Update_Edge(self, ID = None, Color = None, Disabled = None, Locked = None):
        try:
            if ID is None:
                if self._Selected_Edge_Id is None:
                    return ID
                ID = self._Selected_Edge_Id
            if ID not in self._Edges:
                return
            self._Undo_Push()
            E = self._Edges[ID]
            if Color is not None:
                E["Color"] = str(Color)
            if Disabled is not None:
                self._Disabled_Edges[ID] = bool(Disabled)
            if Locked is not None:
                self._Locked_Edges[ID] = bool(Disabled)
            Points = self._Edge_Route(
                int(E.get("FromID", 0)), str(E.get("FromSide", "")),
                int(E.get("ToID", 0)),   str(E.get("ToSide", "")),
                int(E.get("FromIndex", 0)),
                int(E.get("ToIndex", 0)),
                Ignore_Edge_Id = int(ID)
            )
            E["Points"] = Points
            self.Render()
            self._Callback_Invoke("Edge", ID = ID, Event = "Update")
        except Exception as E:
            self._GUI.Error(f"{self._Type} - Update_Edge - {E}")

    def Remove_Edge(self, ID = None):
        try:
            if isinstance(ID, str) and ID.lower() == "all":
                self._Undo_Push()
                for EachId in list(self._Edges.keys()):
                    self.Remove_Edge(EachId)
                return
            if ID is None:
                if not self._Edges:
                    return
                ID = sorted(self._Edges.keys())[0]
            if ID not in self._Edges:
                return
            self._Undo_Push()
            E = self._Edges[ID]
            It = E.get("Item", None)
            if It is not None:
                try:
                    self._Canvas._Frame.delete(It)
                except:
                    pass
                if It in self._Item_To_Edge:
                    del self._Item_To_Edge[It]
            if ID in self._Edges:
                del self._Edges[ID]
            if ID in self._Disabled_Edges:
                del self._Disabled_Edges[ID]
            if ID in self._Locked_Edges:
                del self._Locked_Edges[ID]
            if self._Selected_Edge_Id == ID:
                self._Selected_Edge_Id = None
            self.Render()
            self._Callback_Invoke("Edge", ID = ID, Event = "Remove")
        except Exception as E:
            self._GUI.Error(f"{self._Type} - Remove_Edge - {E}")

    def Lock_Edge(self, ID = None):
        try:
            if ID is None:
                if self._Selected_Edge_Id is None:
                    return
                ID = self._Selected_Edge_Id
            if ID not in self._Edges:
                return
            self._Undo_Push()
            self._Locked_Edges[ID] = True
            self.Render()
            self._Callback_Invoke("Edge", ID = ID, Event = "Lock")
        except Exception as E:
            self._GUI.Error(f"{self._Type} - Lock_Edge - {E}")

    def Unlock_Edge(self, ID = None):
        try:
            if ID is None:
                if self._Selected_Edge_Id is None:
                    return
                ID = self._Selected_Edge_Id
            if ID not in self._Edges:
                return
            self._Undo_Push()
            self._Locked_Edges[ID] = False
            self.Render()
            self._Callback_Invoke("Edge", ID = ID, Event = "Unlock")
        except Exception as E:
            self._GUI.Error(f"{self._Type} - Unlock_Edge - {E}")

    def Enable_Edge(self, ID = None):
        try:
            if ID is None:
                if self._Selected_Edge_Id is None:
                    return
                ID = self._Selected_Edge_Id
            if ID not in self._Edges:
                return
            self._Undo_Push()
            self._Disabled_Edges[ID] = False
            self.Render()
            self._Callback_Invoke("Edge", ID = ID, Event = "Enable")
        except Exception as E:
            self._GUI.Error(f"{self._Type} - Enable_Edge - {E}")

    def Disable_Edge(self, ID = None):
        try:
            if ID is None:
                if self._Selected_Edge_Id is None:
                    return
                ID = self._Selected_Edge_Id
            if ID not in self._Edges:
                return
            self._Undo_Push()
            self._Disabled_Edges[ID] = True
            self.Render()
            self._Callback_Invoke("Edge", ID = ID, Event = "Disable")
        except Exception as E:
            self._GUI.Error(f"{self._Type} - Disable_Edge - {E}")

    def Select_Edge(self, ID):
        try:
            self._Selected_Node_Id = None
            self._Selected_Edge_Id = ID
            self.Render()
            self._Callback_Invoke("Edge", ID = ID, Event = "Select")
        except Exception as E:
            self._GUI.Error(f"{self._Type} - Select_Edge - {E}")

    def Get_Edge(self, ID = None):
        try:
            if isinstance(ID, str) and ID.lower() == "all":
                Out = []
                for EachId in sorted(self._Edges.keys()):
                    Out.append(self.Get_Edge(EachId))
                return Out
            if ID is None:
                ID = self._Selected_Edge_Id
            if ID is None or ID not in self._Edges:
                return None
            E = self._Edges[ID]
            return {"ID": int(ID), "FromID": int(E.get("FromID", 0)), "FromSide": str(E.get("FromSide", "")), "FromIndex": int(E.get("FromIndex", 0)), "ToID": int(E.get("ToID", 0)), "ToSide": str(E.get("ToSide", "")), "ToIndex": int(E.get("ToIndex", 0)), "Points": [(float(Px), float(Py)) for Px, Py in list(E.get("Points", []))], "Color": str(E.get("Color", "")), "Disabled": bool(self._Disabled_Edges.get(ID, False)), "Locked": bool(self._Locked_Edges.get(ID, False))}
        except Exception as E:
            self._GUI.Error(f"{self._Type} - Get_Edge - {E}")
            return None
            
    def Get_Edges(self, Node_Id, Side, Index):
        try:
            return self._Port_Connected_Edges(Node_Id, Side, Index)
        except:
            self._GUI.Error(f"{self._Type} - Get_Edges - {E}")
            return []

    def Get(self, ID = None):
        try:
            if ID is not None:
                if ID in self._Nodes:
                    return self.Get_Node(ID)
                if ID in self._Edges:
                    return self.Get_Edge(ID)
                return None
            if self._Selected_Node_Id is not None:
                return self.Get_Node(self._Selected_Node_Id)
            if self._Selected_Edge_Id is not None:
                return self.Get_Edge(self._Selected_Edge_Id)
            return None
        except Exception as E:
            self._GUI.Error(f"{self._Type} - Get - {E}")
            return None

    def Get_All(self):
        try:
            return {"Nodes": self.Get_Node("all"), "Edges": self.Get_Edge("all")}
        except Exception as E:
            self._GUI.Error(f"{self._Type} - Get_All - {E}")
            return {"Nodes": [], "Edges": []}

    def To_Dict(self):
        try:
            OutNodes = {}
            for ID in sorted(self._Nodes.keys()):
                OutNodes[str(ID)] = self.Get_Node(ID)
            OutEdges = {}
            for ID in sorted(self._Edges.keys()):
                OutEdges[str(ID)] = self.Get_Edge(ID)
            return {"Meta": {"Thickness": float(self._Thickness)}, "Nodes": OutNodes, "Edges": OutEdges}
        except Exception as E:
            self._GUI.Error(f"{self._Type} - To_Dict - {E}")
            return {"Meta": {"Thickness": float(self._Thickness)}, "Nodes": {}, "Edges": {}}

    def From_Dict(self, Data):
        try:
            self.Clear()
            Meta = dict(Data.get("Meta", {}))
            if "Thickness" in Meta:
                self._Thickness = float(Meta.get("Thickness"))
            Nodes = dict(Data.get("Nodes", {}))
            Edges = dict(Data.get("Edges", {}))
            IdMap = {}
            for Sid in Nodes:
                N = Nodes[Sid]
                NormCounts = self._Node_Port_Counts_Normalize(dict(N.get("PortCounts", self._Node_Port_Counts_Default())))
                NewId = self.Add_Node(X = float(N.get("X", 40.0)), Y = float(N.get("Y", 40.0)), Width = float(N.get("Width", 160.0)), Height = float(N.get("Height", 100.0)), Color = str(N.get("Color", "#4F8EF7")), Fill = str(N.get("Fill", "#DC7633")), Title = str(N.get("Title", "")), Description = str(N.get("Description", "")), Type = str(N.get("Type", "")), Ports = dict(N.get("Ports", self._Node_Ports_Default())), Port_Counts = self._Node_Port_Counts_Normalize(dict(N.get("PortCounts", self._Node_Port_Counts_Default()))), Port_Names = self._Node_Port_Names_Normalize(dict(N.get("PortNames", self._Node_Port_Names_Default())), Port_Counts = NormCounts), Port_Colors = self._Node_Port_Colors_Normalize(dict(N.get("PortColors", self._Node_Port_Colors_Default())), Port_Counts = NormCounts))
                if bool(N.get("Disabled", False)):
                    self._Disabled_Nodes[NewId] = True
                if bool(N.get("Locked", False)):
                    self._Locked_Nodes[NewId] = True
                IdMap[int(N.get("ID", int(Sid)))] = int(NewId)
            for Sid in Edges:
                E = Edges[Sid]
                A = int(E.get("FromID", 0))
                B = int(E.get("ToID", 0))
                FromId = int(IdMap.get(A, A))
                ToId = int(IdMap.get(B, B))
                Eid = self.Add_Edge(From_Id = FromId, From_Side = str(E.get("FromSide", "Right")), To_Id = ToId, To_Side = str(E.get("ToSide", "Left")), Color = str(E.get("Color", "#000000")), From_Index = int(E.get("FromIndex", 0)), To_Index = int(E.get("ToIndex", 0)))
                if Eid is not None and bool(E.get("Disabled", False)):
                    self._Disabled_Edges[Eid] = True
                if Eid is not None and bool(E.get("Locked", False)):
                    self._Locked_Edges[Eid] = True
            self._Selected_Node_Id = None
            self._Selected_Edge_Id = None
            self._Pending_Connect = None
            self.Render()
        except Exception as E:
            self._GUI.Error(f"{self._Type} - From_Dict - {E}")

    def Save_To_File(self, Path):
        try:
            D = self.To_Dict()
            with open(Path, "w", encoding = "utf-8") as F:
                json.dump(D, F, indent = 2)
            self._Callback_Invoke("Flowchart", Event = "Save", Data = {"Path": str(Path)})
        except Exception as E:
            self._GUI.Error(f"{self._Type} - Save_To_File - {E}")

    def Load_From_File(self, Path):
        try:
            with open(Path, "r", encoding = "utf-8") as F:
                D = json.load(F)
            self.From_Dict(D)
            self._Callback_Invoke("Flowchart", Event = "Load", Data = {"Path": str(Path)})
        except Exception as E:
            self._GUI.Error(f"{self._Type} - Load_From_File - {E}")

    def Flow_Order(self, Include_Disabled=True, Allow_Cycles=True):
        try:
            Data=self.To_Dict()
            Nodes_Raw=dict(Data.get("Nodes",{}) or {})
            Edges_Raw=dict(Data.get("Edges",{}) or {})
            Nodes={}
            for K,V in list(Nodes_Raw.items()):
                try:
                    Node_Id=int(K) if not isinstance(K,int) else int(K)
                    if isinstance(V,dict):
                        Nodes[Node_Id]=V
                except:
                    pass
            Edges={}
            for K,V in list(Edges_Raw.items()):
                try:
                    Edge_Id=int(K) if not isinstance(K,int) else int(K)
                    if isinstance(V,dict):
                        Edges[Edge_Id]=V
                except:
                    pass
            if not Nodes:
                return {"Paths":[],"Unreached":[],"Cycles":[]}
            Disabled_Nodes=getattr(self,"Disabled_Nodes",{}) or {}
            Disabled_Edges=getattr(self,"Disabled_Edges",{}) or {}
            def Node_Is_Disabled(Node_Id):
                try:
                    Node_Data=Nodes.get(int(Node_Id),{}) or {}
                    if "Disabled" in Node_Data:
                        return bool(Node_Data.get("Disabled",False))
                    return bool(Disabled_Nodes.get(int(Node_Id),False))
                except:
                    return False
            def Edge_Is_Disabled(Edge_Id):
                try:
                    Edge_Data=Edges.get(int(Edge_Id),{}) or {}
                    if "Disabled" in Edge_Data:
                        return bool(Edge_Data.get("Disabled",False))
                    return bool(Disabled_Edges.get(int(Edge_Id),False))
                except:
                    return False
            def Node_Pos(Node_Id):
                try:
                    Node_Data=Nodes.get(int(Node_Id),{}) or {}
                    return (float(Node_Data.get("Y",0.0)),float(Node_Data.get("X",0.0)))
                except:
                    return (0.0,0.0)
            Out={}
            for Node_Id in list(Nodes.keys()):
                Out[int(Node_Id)]=[]
            for Edge_Id,Edge_Data in list(Edges.items()):
                try:
                    if (not Include_Disabled) and Edge_Is_Disabled(Edge_Id):
                        continue
                    From_Id=int(Edge_Data.get("FromID",-1))
                    To_Id=int(Edge_Data.get("ToID",-1))
                    if From_Id not in Nodes or To_Id not in Nodes:
                        continue
                    if not Include_Disabled:
                        if Node_Is_Disabled(From_Id) or Node_Is_Disabled(To_Id):
                            continue
                    Rec={"From":[From_Id,str(Edge_Data.get("FromSide","")),int(Edge_Data.get("FromIndex",0))],"To":[To_Id,str(Edge_Data.get("ToSide","")),int(Edge_Data.get("ToIndex",0))]}
                    Out[From_Id].append(Rec)
                except:
                    continue
            for Node_Id in list(Out.keys()):
                try:
                    Out[Node_Id].sort(key=lambda R:(Node_Pos(int(R["To"][0]))[0],Node_Pos(int(R["To"][0]))[1],int(R["To"][0])))
                except:
                    pass
            Runnable_Paths=[]
            Non_Runnable_Paths=[]
            Cycles=[]
            def Dfs(Current,Path_Nodes,Path_Edges,Stack_Set,Visited,Path_Sink):
                try:
                    Current=int(Current)
                except:
                    return
                if (not Include_Disabled) and Node_Is_Disabled(Current):
                    return
                Visited.add(Current)
                Stack_Set.add(Current)
                Path_Nodes.append(Current)
                Outs=list(Out.get(Current,[]) or [])
                if not Outs:
                    Path_Sink.append({"Nodes":list(Path_Nodes),"Edges":list(Path_Edges),"Cyclic":False})
                else:
                    for R in Outs:
                        try:
                            To_Id=int(R["To"][0])
                        except:
                            continue
                        if (not Include_Disabled) and Node_Is_Disabled(To_Id):
                            continue
                        if To_Id in Stack_Set:
                            Cy={"From":list(R.get("From",[])),"To":list(R.get("To",[]))}
                            Cycles.append(Cy)
                            if Allow_Cycles:
                                Path_Sink.append({"Nodes":list(Path_Nodes)+[To_Id],"Edges":list(Path_Edges)+[R],"Cyclic":True,"Cycle":Cy})
                            continue
                        Path_Edges.append(R)
                        Dfs(To_Id,Path_Nodes,Path_Edges,Stack_Set,Visited,Path_Sink)
                        Path_Edges.pop()
                Path_Nodes.pop()
                Stack_Set.remove(Current)
            Start_Id=1
            Reached_From_Start=set()
            if Start_Id in Nodes:
                Dfs(Start_Id,[],[],set(),Reached_From_Start,Runnable_Paths)
            All_Node_Ids=set(int(Node_Id) for Node_Id in list(Nodes.keys()))
            Reached_All=set(Reached_From_Start)
            Remaining=set(All_Node_Ids-Reached_All)
            In_Deg={int(Node_Id):0 for Node_Id in list(Nodes.keys())}
            for From_Id,Outs in list(Out.items()):
                for R in list(Outs or []):
                    try:
                        To_Id=int(R["To"][0])
                        if To_Id in In_Deg:
                            In_Deg[To_Id]+=1
                    except:
                        pass
            while Remaining:
                Extra_Starts=[Node_Id for Node_Id in list(Remaining) if int(In_Deg.get(int(Node_Id),0))==0]
                if Extra_Starts:
                    Extra_Starts.sort(key=lambda Node_Id:(Node_Pos(Node_Id)[0],Node_Pos(Node_Id)[1],int(Node_Id)))
                    Next_Start=int(Extra_Starts[0])
                else:
                    Next_Start=int(min(list(Remaining),key=lambda Node_Id:(Node_Pos(Node_Id)[0],Node_Pos(Node_Id)[1],int(Node_Id))))
                Dfs(Next_Start,[],[],set(),Reached_All,Non_Runnable_Paths)
                Remaining=set(All_Node_Ids-Reached_All)
            Unreached=list(All_Node_Ids-Reached_All)
            Unreached.sort(key=lambda Node_Id:(Node_Pos(Node_Id)[0],Node_Pos(Node_Id)[1],int(Node_Id)))
            return {"Paths":Runnable_Paths,"Unreached":Non_Runnable_Paths,"Cycles":Cycles}
        except Exception as E:
            self._GUI.Errorf(self._Type+" - Flow_Order - "+str(E))
            return None