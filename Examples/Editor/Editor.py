# -------------------------------------------------------------------------------------------------------------------------------
# Gluonix Runtime
# -------------------------------------------------------------------------------------------------------------------------------
#################################################################################################################################
if __name__=='__main__':
    from Nucleon.Runner import * ###!REQUIRED ------- Any Script Before This Won't Effect GUI Elements
#################################################################################################################################
#################################################################################################################################
# -------------------------------------------------------------------------------------------------------------------------------
# Developer Programming Start
# -------------------------------------------------------------------------------------------------------------------------------

    Type = 'Viewport'  # 'Viewport' or 'Editor'

    Shapes = {
        'Rectangle': {
            'X': 0,
            'Y': 0,
            'Width': 0,
            'Height': 0,
            'Angle': 0,
            'Thickness': 0,
            'Color': ''
        },
        'Circle': {
            'X': 0,
            'Y': 0,
            'Radius': 0,
            'Thickness': 0,
            'Color': ''
        },
        'Quadrilateral': {
            'P1': [0, 0],
            'P2': [0, 0],
            'P3': [0, 0],
            'P4': [0, 0],
            'Angle': 0,
            'Thickness': 0,
            'Color': ''
        },
        'Line': {
            'Points': [[0, 0], [0, 0]],
            'Angle': 0,
            'Thickness': 0,
            'Color': ''
        },
        'Polyline': {
            'Points': [[0, 0], [0, 0]],
            'Angle': 0,
            'Thickness': 0,
            'Color': ''
        },
        'Polygon': {
            'Points': [[0, 0], [0, 0], [0, 0]],
            'Angle': 0,
            'Thickness': 0,
            'Color': ''
        }
    }

    Options = []
    Current_Shape_Type = None
    Current_Shape_ID = None

    def _Supports_Param(Func, ParamName):
        try:
            import inspect
            Sig = inspect.signature(Func)
            return ParamName in Sig.parameters
        except:
            return False

    def _Filter_Kwargs(Func, Kwargs):
        try:
            import inspect
            Sig = inspect.signature(Func)
            Params = Sig.parameters
            if any(p.kind == inspect.Parameter.VAR_KEYWORD for p in Params.values()):
                return dict(Kwargs)
            Allowed = set(Params.keys())
            return {k: v for k, v in Kwargs.items() if k in Allowed}
        except:
            return dict(Kwargs)

    def _Ensure_Fill_Keys():
        for ShapeName in list(Shapes.keys()):
            AddFunc = getattr(Editor, f"Add_{ShapeName}", None)
            HasFill = callable(AddFunc) and _Supports_Param(AddFunc, 'Fill')
            if HasFill:
                if 'Fill' not in Shapes[ShapeName]:
                    Shapes[ShapeName]['Fill'] = ''
            else:
                if 'Fill' in Shapes[ShapeName]:
                    Shapes[ShapeName].pop('Fill', None)
            HasTransparent = callable(AddFunc) and _Supports_Param(AddFunc, 'Transparent')
            if HasTransparent:
                if 'Transparent' not in Shapes[ShapeName]:
                    Shapes[ShapeName]['Transparent'] = False
            else:
                if 'Transparent' in Shapes[ShapeName]:
                    Shapes[ShapeName].pop('Transparent', None)

    def Is_Default(Value):
        if isinstance(Value, (int, float)):
            return Value == 0
        elif isinstance(Value, str):
            return Value == ''
        elif isinstance(Value, list):
            return all(v == 0 or (isinstance(v, list) and all(x == 0 for x in v)) for v in Value)
        return False

    def Format_Value(Value):
        if isinstance(Value, float):
            return round(Value, 2)
        elif isinstance(Value, str):
            return Value
        elif isinstance(Value, list):
            return [Format_Value(v) if isinstance(v, list) else (round(v, 2) if isinstance(v, float) else v) for v in Value]
        return Value

    def Expand_Shape_Data(Shape_Data):
        Expanded = []
        Items = list(Shape_Data.items())
        Items.reverse()
        QuadKeys = ['P1', 'P2', 'P3', 'P4']
        HasQuad = all(k in Shape_Data for k in QuadKeys)
        if HasQuad:
            Items = [(k, v) for (k, v) in Items if k not in QuadKeys]
            QuadItems = [(k, Shape_Data[k]) for k in QuadKeys]
            Items = Items + QuadItems
        for Key, Value in Items:
            if Key == 'Points' and isinstance(Value, list):
                for Index, Point in enumerate(Value):
                    if isinstance(Point, list) and len(Point) == 2:
                        Expanded.append((f"Point_{Index}_Y", Point[1]))
                        Expanded.append((f"Point_{Index}_X", Point[0]))
            elif Key.startswith('P') and len(Key) == 2 and isinstance(Value, list) and len(Value) == 2:
                Expanded.append((f"{Key}_Y", Value[1]))
                Expanded.append((f"{Key}_X", Value[0]))
            else:
                Expanded.append((Key, Value))
        return Expanded

    def Parse_Value(Value):
        import ast
        if Value is None:
            return None
        if isinstance(Value, (int, float, list, tuple, dict)):
            return Value
        if not isinstance(Value, str):
            return Value
        S = Value.strip()
        if S == '':
            return ''
        if S.startswith('[') or S.startswith('(') or S.startswith('{'):
            try:
                return ast.literal_eval(S)
            except:
                return Value
        try:
            if '.' in S or 'e' in S.lower():
                return float(S)
            return int(S)
        except:
            try:
                return float(S)
            except:
                return Value

    def To_Float(Value):
        try:
            return float(Value)
        except:
            return None

    def Is_Valid_Hex_Color(Text):
        if not isinstance(Text, str):
            return False
        S = Text.strip()
        if S == '':
            return True
        if not S.startswith('#'):
            return False
        HexPart = S[1:]
        if len(HexPart) not in (3, 6):
            return False
        for C in HexPart:
            if C not in '0123456789abcdefABCDEF':
                return False
        return True

    def Normalize_Color(Value):
        if Value is None:
            return ''
        S = str(Value).strip()
        if S == '':
            return ''
        if Is_Valid_Hex_Color(S):
            return S.upper()
        return None

    def Get_Key_Name(Event):
        for Name in ('keysym', 'Keysym', 'KeySym', 'Key', 'key'):
            if hasattr(Event, Name):
                Value = getattr(Event, Name)
                if isinstance(Value, str) and Value:
                    return Value
        return ''

    def Should_Ignore_Key(Key_Name):
        Ignore = {
            'Left', 'Right', 'Up', 'Down', 'Home', 'End', 'Prior', 'Next',
            'Shift_L', 'Shift_R', 'Control_L', 'Control_R', 'Alt_L', 'Alt_R',
            'Caps_Lock', 'Num_Lock', 'Scroll_Lock', 'Tab'
        }
        return Key_Name in Ignore

    def Update_Viewport():
        if Current_Shape_Type is None or Current_Shape_ID is None:
            return
        if Current_Shape_Type not in Shapes:
            return
        Update_Method = getattr(Editor, f"Update_{Current_Shape_Type}", None)
        if not callable(Update_Method):
            return
        Payload = dict(Shapes[Current_Shape_Type])
        Payload = _Filter_Kwargs(Update_Method, Payload)
        try:
            Update_Method(ID=Current_Shape_ID, **Payload)
        except TypeError:
            try:
                Update_Method(Current_Shape_ID, **Payload)
            except:
                pass

    def Apply_Expanded_Key(Shape_Data, Key, New_Value):
        if Key in ('Color', 'Fill'):
            C = Normalize_Color(New_Value)
            if C is None:
                return False
            Shape_Data[Key] = C
            return True
        if Key == 'Transparent':
            if isinstance(New_Value, bool):
                Shape_Data[Key] = New_Value
                return True
            if isinstance(New_Value, (int, float)):
                Shape_Data[Key] = bool(New_Value)
                return True
            if isinstance(New_Value, str):
                S = New_Value.strip().lower()
                if S in ('true', '1', 'yes', 'on'):
                    Shape_Data[Key] = True
                    return True
                if S in ('false', '0', 'no', 'off', ''):
                    Shape_Data[Key] = False
                    return True
            return False
        if Key.startswith('Point_') and 'Points' in Shape_Data:
            Parts = Key.split('_')
            if len(Parts) != 3:
                return False
            Index = int(Parts[1])
            Axis = Parts[2]
            Points = Shape_Data.get('Points')
            if not isinstance(Points, list) or Index < 0 or Index >= len(Points):
                return False
            if not isinstance(Points[Index], list) or len(Points[Index]) != 2:
                return False
            V = To_Float(New_Value)
            if V is None:
                return False
            if Axis == 'X':
                Points[Index][0] = V
            elif Axis == 'Y':
                Points[Index][1] = V
            else:
                return False
            Shape_Data['Points'] = Points
            return True
        if Key.startswith('P') and len(Key) == 4 and Key[1].isdigit() and Key[2] == '_' and Key[3] in ('X', 'Y'):
            Pk = Key[:2]
            Axis = Key[3]
            if Pk not in Shape_Data or not isinstance(Shape_Data[Pk], list) or len(Shape_Data[Pk]) != 2:
                return False
            V = To_Float(New_Value)
            if V is None:
                return False
            if Axis == 'X':
                Shape_Data[Pk][0] = V
            else:
                Shape_Data[Pk][1] = V
            return True
        if Key in ('X', 'Y', 'Width', 'Height', 'Radius', 'Angle', 'Thickness'):
            V = To_Float(New_Value)
            if V is None:
                return False
            if Key in ('Width', 'Height', 'Radius', 'Thickness') and V < 0:
                return False
            Shape_Data[Key] = V
            return True
        Shape_Data[Key] = New_Value
        return True

    def Commit_Option(Key, Object, Raw):
        if Current_Shape_Type is None or Current_Shape_Type not in Shapes:
            return False
        Shape_Data = Shapes[Current_Shape_Type]
        New_Value = Parse_Value(Raw)
        if not Apply_Expanded_Key(Shape_Data, Key, New_Value):
            return False
        setattr(Object, '_Last_Text', Raw)
        Shapes[Current_Shape_Type] = Shape_Data
        Update_Viewport()
        return True

    def On_Option_Key_Release(Event, Key, Object):
        Key_Name = Get_Key_Name(Event)
        if Should_Ignore_Key(Key_Name):
            return
        Raw = Object.Value.Get()
        if getattr(Object, '_Last_Text', None) == Raw:
            return
        Commit_Option(Key, Object, Raw)

    def _Event_Screen_XY(Event, Widget=None):
        for ax, ay in (('x_root', 'y_root'), ('X_root', 'Y_root'), ('XRoot', 'YRoot')):
            if hasattr(Event, ax) and hasattr(Event, ay):
                try:
                    return int(getattr(Event, ax)), int(getattr(Event, ay))
                except:
                    pass
        x = getattr(Event, 'x', None)
        y = getattr(Event, 'y', None)
        if x is None or y is None:
            return None, None
        W = None
        if Widget is not None:
            W = getattr(Widget, 'Frame', None) or Widget
        if W is not None and hasattr(W, 'winfo_rootx') and hasattr(W, 'winfo_rooty'):
            try:
                return int(W.winfo_rootx() + x), int(W.winfo_rooty() + y)
            except:
                pass
        return None, None

    def Try_Color_Picker(Event, Current_Text, Widget=None):
        try:
            import tkinter as tk
            from tkinter import colorchooser
        except:
            return None
        Initial = Normalize_Color(Current_Text)
        if Initial == '':
            Initial = None
        W = None
        if Widget is not None:
            W = getattr(Widget, 'Frame', None) or Widget
        Parent = None
        try:
            if W is not None and hasattr(W, 'winfo_toplevel'):
                Parent = W.winfo_toplevel()
        except:
            Parent = None
        X, Y = _Event_Screen_XY(Event, Widget)
        Anchor = None
        try:
            if Parent is not None and X is not None and Y is not None:
                Anchor = tk.Toplevel(Parent)
                Anchor.overrideredirect(True)
                Anchor.geometry(f"1x1+{X}+{Y}")
                Anchor.lift()
                Anchor.update_idletasks()
            Out = colorchooser.askcolor(color=Initial, parent=(Anchor if Anchor is not None else Parent))
        except:
            Out = None
        try:
            if Anchor is not None:
                Anchor.destroy()
        except:
            pass
        if not Out or len(Out) < 2:
            return None
        Hex = Out[1]
        C = Normalize_Color(Hex)
        if C is None or C == '':
            return None
        return C

    def On_Color_Click(Event, Key, Object):
        if Key not in ('Color', 'Fill'):
            return
        Raw = Object.Value.Get()
        Picked = Try_Color_Picker(Event, Raw, Object.Value)
        if Picked is None:
            return "break"
        if getattr(Object, '_Last_Text', None) == Picked:
            return "break"
        Object.Value.Set(Picked)
        Commit_Option(Key, Object, Picked)
        return "break"

    def On_Bool_Click(Event, Key, Object):
        if Key != 'Transparent':
            return
        Raw = str(Object.Value.Get()).strip().lower()
        Curr = Raw in ('1', 'true', 'yes', 'on')
        New = ('False' if Curr else 'True')
        Object.Value.Set(New)
        Commit_Option(Key, Object, New)
        return "break"

    def Rebuild_Options(Shape_Type, Shape_Data):
        for Object in list(Options):
            Object.Delete()
        Options.clear()
        Expanded = Expand_Shape_Data(Shape_Data)
        Top = -50
        for Key, Value in Expanded:
            Top += 35
            Object = Option.Copy()
            Object.Label.Set(Key)
            Text = str(Format_Value(Value))
            Object.Value.Set(Text)
            setattr(Object, '_Last_Text', Text)
            if Key in ('Color', 'Fill'):
                Object.Value.Bind(On_Click=lambda E, K=Key, O=Object: On_Color_Click(E, K, O))
                Object.Value.Bind(On_Key=lambda E: "break")
                Object.Value.Bind(On_Key_Release=lambda E: "break")
                try:
                    Object.Value.Bind(CursorHand=True)
                except:
                    pass
            elif Key == 'Transparent':
                Object.Value.Bind(On_Click=lambda E, K=Key, O=Object: On_Bool_Click(E, K, O))
                Object.Value.Bind(On_Key=lambda E: "break")
                Object.Value.Bind(On_Key_Release=lambda E: "break")
                try:
                    Object.Value.Bind(CursorHand=True)
                except:
                    pass
            else:
                Object.Value.Bind(On_Key_Release=lambda E, K=Key, O=Object: On_Option_Key_Release(E, K, O))
            Object.Move(Top=Top)
            Object.Show()
            Options.append(Object)

    def _Merge_Shape_Data(Shape_Type, NewData):
        Old = Shapes.get(Shape_Type, {})
        Out = dict(Old)
        if isinstance(NewData, dict):
            Out.update(NewData)
        return Out

    def Callback(Data):
        global Current_Shape_Type, Current_Shape_ID
        if 'Type' in Data and 'Data' in Data:
            Shape_Type = Data['Type']
            Current_Shape_Type = Shape_Type
            Current_Shape_ID = Data.get('ID', Current_Shape_ID)
            if Shape_Type in Shapes:
                Shapes[Shape_Type] = _Merge_Shape_Data(Shape_Type, Data['Data'])
            _Ensure_Fill_Keys()
            Shape_Data = Shapes[Shape_Type]
            Expanded = Expand_Shape_Data(Shape_Data)
            if len(Expanded) != len(Options):
                Rebuild_Options(Shape_Type, Shape_Data)
            else:
                for Index, (Key, Value) in enumerate(Expanded):
                    Text = str(Format_Value(Value))
                    if getattr(Options[Index], '_Last_Text', None) != Text:
                        Options[Index].Value.Set(Text)
                        setattr(Options[Index], '_Last_Text', Text)

    def Create():
        global Current_Shape_Type, Current_Shape_ID
        Shape = Choice.Get()
        if Shape not in Shapes:
            return None
        Editor.Clear()
        Shape_Data = dict(Shapes[Shape])
        Add_Method = getattr(Editor, f"Add_{Shape}", None)
        if not callable(Add_Method):
            return None
        Default = all(Is_Default(Value) for Value in Shape_Data.values())
        if Default:
            ID = Add_Method()
            Get_Method = getattr(Editor, f"Get_{Shape}", None)
            if callable(Get_Method):
                Shapes[Shape] = _Merge_Shape_Data(Shape, Get_Method(ID=ID))
        else:
            Payload = _Filter_Kwargs(Add_Method, Shape_Data)
            ID = Add_Method(**Payload)
        Current_Shape_Type = Shape
        Current_Shape_ID = ID
        _Ensure_Fill_Keys()
        Rebuild_Options(Shape, Shapes[Shape])

    if Type == 'Viewport':
        Editor = Root.Canvas.Viewport()
        Editor.Load('Image.png')
    else:
        Editor = Root.Canvas.Editor()
    Editor.Callback(Callback)

    _Ensure_Fill_Keys()

    Option = Root.Option

    Choice = Root.Choice
    Choice.Config(Font_Size=15, Popup_Font_Size=15)
    Choice.Bind(On_Change=lambda E: Create())
    for Shape_Name in Shapes:
        Choice.Add(Shape_Name)
    Choice.Set('Rectangle')

    Root.After(100, lambda: Create())

# -------------------------------------------------------------------------------------------------------------------------------
# Developer Programming End
# -------------------------------------------------------------------------------------------------------------------------------
#################################################################################################################################
#################################################################################################################################
    Root.Start() ###!REQUIRED ------- Any Script After This Will Not Execute
#################################################################################################################################