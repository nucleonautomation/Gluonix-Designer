# -------------------------------------------------------------------------------------------------------------------------------
# Gluonix Runtime
# -------------------------------------------------------------------------------------------------------------------------------
#################################################################################################################################
if __name__ == '__main__':
    from Nucleon.Runner import *
#################################################################################################################################
#################################################################################################################################
# -------------------------------------------------------------------------------------------------------------------------------
# Developer Programming Start
# -------------------------------------------------------------------------------------------------------------------------------

    import random
    import time

    AddBtn = Root.Add
    Output = Root.Output

    def Output_Set(Text):
        S = str(Text)
        try:
            Output.Set(S)
            return
        except:
            pass
        try:
            W = getattr(Output, "Widget", None)
            if W is not None:
                W.config(state="normal")
                W.delete("1.0", "end")
                W.insert("end", S)
                W.config(state="disabled")
                return
        except:
            pass

    Flowchart = Root.Canvas.Flowchart()
    Flowchart.Thickness(2)

    NAME_WORDS = [
        "Filter", "Map", "Join", "GroupBy", "Aggregate", "Normalize", "Enrich",
        "Validate", "Dedup", "Route", "Split", "Merge", "Format", "Encode",
        "Decode", "Rank", "Score", "Classify", "Index", "Export"
    ]
    _name_counter = 0

    PORT_WORDS = [
        "in", "out", "left", "right", "top", "bottom",
        "data", "rows", "cols", "cfg", "params", "keys",
        "main", "aux", "ctrl", "err"
    ]

    PORT_PALETTE = [
        "#1F77B4", "#FF7F0E", "#2CA02C", "#D62728", "#9467BD", "#17BECF",
        "#E67E22", "#16A085", "#2980B9", "#8E44AD", "#C0392B", "#2C3E50"
    ]

    def Next_Nice_Name():
        global _name_counter
        _name_counter += 1
        return f"{random.choice(NAME_WORDS)}"

    def Rand_Color():
        return random.choice(["#1F77B4", "#FF7F0E", "#2CA02C", "#D62728", "#9467BD", "#17BECF", "#2C3E50"])

    def Rand_Fill():
        return random.choice(["#FADBD8", "#D5F5E3", "#EBDEF0", "#FDEBD0", "#EAF2F8", "#FCF3CF"])

    def Canvas_Size():
        W = 800.0
        H = 600.0
        try:
            W = float(Flowchart.Canvas_Width())
        except:
            pass
        try:
            H = float(Flowchart.Canvas_Height())
        except:
            pass
        return W, H

    def Make_Port_Names(Title, Port_Counts):
        Out = {}
        for Side in ["Top", "Left", "Right", "Bottom"]:
            C = int((Port_Counts or {}).get(Side, 0) or 0)
            Names = []
            for I in range(max(0, C)):
                Names.append(f"{random.choice(PORT_WORDS)}_{Side.lower()}_{I}")
            Out[Side] = Names
        return Out

    def Make_Port_Colors(Port_Counts):
        Out = {}
        for Side in ["Top", "Left", "Right", "Bottom"]:
            C = int((Port_Counts or {}).get(Side, 0) or 0)
            Colors = []
            for I in range(max(0, C)):
                Colors.append(random.choice(PORT_PALETTE))
            Out[Side] = Colors
        return Out

    def Add_Random_Node():
        W, H = Canvas_Size()
        X = random.randint(140, max(141, int(W) - 140))
        Y = random.randint(140, max(141, int(H) - 140))
        Title = Next_Nice_Name()
        Top = random.choice([True, False])
        Left = random.choice([True, False])
        if not (Top or Left):
            random.choice(["Top", "Left"])
            if random.choice([True, False]):
                Top = True
            else:
                Left = True
        Right = random.choice([True, False])
        Bottom = random.choice([True, False])
        if not (Right or Bottom):
            if random.choice([True, False]):
                Right = True
            else:
                Bottom = True
        Ports = {
            "Top": Top,
            "Left": Left,
            "Right": Right,
            "Bottom": Bottom,
        }
        Port_Counts = {
            "Top": random.randint(1, 3) if Top else 0,
            "Left": random.randint(1, 3) if Left else 0,
            "Right": random.randint(1, 3) if Right else 0,
            "Bottom": random.randint(1, 3) if Bottom else 0,
        }
        Port_Names = Make_Port_Names(Title, Port_Counts)
        Port_Colors = Make_Port_Colors(Port_Counts)
        Flowchart.Add_Node(
            X=X, Y=Y, Width=180, Height=100,
            Color=Rand_Color(), Fill=Rand_Fill(),
            Title=Title, Description="Random node",
            Ports=Ports, Port_Counts=Port_Counts,
            Port_Names=Port_Names, Port_Colors=Port_Colors
        )

    def Format_Status(Info):
        D = Flowchart.To_Dict()
        Nodes = (D.get("Nodes") or {})
        Edges = (D.get("Edges") or {})

        TitleById = {}
        for Sid, N in (Nodes.items() if isinstance(Nodes, dict) else []):
            try:
                Nid = int((N or {}).get("ID", Sid))
            except:
                Nid = Sid
            TitleById[Nid] = str((N or {}).get("Title", "") or f"Node {Nid}")

        T = str((Info or {}).get("Type", ""))
        E = str((Info or {}).get("Event", ""))
        ID = (Info or {}).get("ID", None)

        Lines = []
        Lines.append(f"Last event: {T} {E} (ID={ID})")
        Lines.append(f"Nodes: {len(Nodes) if isinstance(Nodes, dict) else 0}    Edges: {len(Edges) if isinstance(Edges, dict) else 0}")
        Lines.append("")
        Lines.append("Nodes:")
        if isinstance(Nodes, dict) and Nodes:
            for Sid in sorted(Nodes.keys(), key=lambda x: int(x) if str(x).isdigit() else 10**9):
                N = Nodes.get(Sid, {}) or {}
                Nid = N.get("ID", Sid)
                Lines.append(f"  [{Nid}] {str(N.get('Title','') or '')} - {str(N.get('Description','') or '')}".rstrip(" -"))
        else:
            Lines.append("  (none)")

        Lines.append("")
        Lines.append("Edges:")
        if isinstance(Edges, dict) and Edges:
            for Sid in sorted(Edges.keys(), key=lambda x: int(x) if str(x).isdigit() else 10**9):
                Ed = Edges.get(Sid, {}) or {}
                Eid = Ed.get("ID", Sid)
                A = Ed.get("FromID", None)
                B = Ed.get("ToID", None)
                AS = str(Ed.get("FromSide", ""))
                BS = str(Ed.get("ToSide", ""))
                AI = int(Ed.get("FromIndex", 0) or 0)
                BI = int(Ed.get("ToIndex", 0) or 0)
                AT = TitleById.get(A, f"Node {A}")
                BT = TitleById.get(B, f"Node {B}")
                Lines.append(f"  [{Eid}] {A}({AT}) {AS}:{AI}  ->  {B}({BT}) {BS}:{BI}")
        else:
            Lines.append("  (none)")

        return "\n".join(Lines) + "\n"

    def Callback(Info):
        Output_Set(Format_Status(Info))

    Flowchart.Callback(Callback)

    def Callback_Custom(Info):
        print(Info)

    Flowchart.Context_Menu_Add("Show node info", Callback_Custom, Type="")
    Flowchart.Context_Menu_Add("Append '*' to title", Callback_Custom, Type="")
    Flowchart.Context_Menu_Add("Source only", Callback_Custom, Type="Source")
    Flowchart.Context_Menu_Add("Filter/Sink only", Callback_Custom, Type=["Filter", "Sink"])

    def Create_Initial():
        try:
            Flowchart.Clear()
        except:
            pass

        try:
            Flowchart.Thickness(Value=2.0, SelectedMultiplier=2.0, SelectedOutlineColor="#FF0000")
        except:
            pass

        A_Ports = {"Top": False, "Left": False, "Right": True, "Bottom": True}
        A_Port_Counts = {"Top": 0, "Left": 0, "Right": 1, "Bottom": 1}
        A_Port_Names = {"Top": [], "Left": [], "Right": ["out_main"], "Bottom": ["out_aux"]}
        A_Port_Colors = {"Top": [], "Left": [], "Right": ["#1F77B4"], "Bottom": ["#FF7F0E"]}

        B_Ports = {"Top": False, "Left": True, "Right": True, "Bottom": False}
        B_Port_Counts = {"Top": 0, "Left": 1, "Right": 1, "Bottom": 0}
        B_Port_Names = {"Top": [], "Left": ["in_main"], "Right": ["out_main"], "Bottom": []}
        B_Port_Colors = {"Top": [], "Left": ["#2CA02C"], "Right": ["#D62728"], "Bottom": []}

        C_Ports = {"Top": True, "Left": True, "Right": False, "Bottom": False}
        C_Port_Counts = {"Top": 1, "Left": 1, "Right": 0, "Bottom": 0}
        C_Port_Names = {"Top": ["in_aux"], "Left": ["in_main"], "Right": [], "Bottom": []}
        C_Port_Colors = {"Top": ["#9467BD"], "Left": ["#17BECF"], "Right": [], "Bottom": []}

        A = Flowchart.Add_Node(
            X=170, Y=160, Width=180, Height=100,
            Color="#1F77B4", Fill="#EAF2F8", Type='Source',
            Title="Source", Description="Produces data",
            Ports=A_Ports, Port_Counts=A_Port_Counts,
            Port_Names=A_Port_Names, Port_Colors=A_Port_Colors
        )

        B = Flowchart.Add_Node(
            X=500, Y=160, Width=180, Height=100,
            Color="#2CA02C", Fill="#D5F5E3", Type='Filter',
            Title="Filter", Description="Drops invalid rows",
            Ports=B_Ports, Port_Counts=B_Port_Counts,
            Port_Names=B_Port_Names, Port_Colors=B_Port_Colors
        )

        C = Flowchart.Add_Node(
            X=830, Y=310, Width=180, Height=100,
            Color="#9467BD", Fill="#EBDEF0", Type='Sink',
            Title="Sink", Description="Consumes data",
            Ports=C_Ports, Port_Counts=C_Port_Counts,
            Port_Names=C_Port_Names, Port_Colors=C_Port_Colors
        )

        if A is not None and B is not None:
            Flowchart.Add_Edge(A, "Right", B, "Left", Color=None, From_Index=0, To_Index=0)
        if B is not None and C is not None:
            Flowchart.Add_Edge(B, "Right", C, "Top", Color=None, From_Index=0, To_Index=0)
        if A is not None and C is not None:
            Flowchart.Add_Edge(A, "Bottom", C, "Left", Color=None, From_Index=0, To_Index=0)

    AddBtn.Bind(On_Click=lambda E: Add_Random_Node())
    Root.After(50, Create_Initial)

# -------------------------------------------------------------------------------------------------------------------------------
# Developer Programming End
# -------------------------------------------------------------------------------------------------------------------------------
#################################################################################################################################
#################################################################################################################################
    Root.Start()
#################################################################################################################################
