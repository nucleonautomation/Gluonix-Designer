def Event_Bind(Widget, **Input):
    if 'Cursor_Hand' in Input:
        if Input['Cursor_Hand']:
            Widget.config(cursor="hand2")
    if 'Cursor_Loading' in Input:
        if Input['Cursor_Loading']:
            Widget.config(cursor="watch")
    if 'Cursor_Resize_Vertical' in Input:
        if Input['Cursor_Resize_Vertical']:
            Widget.config(cursor='sb_h_double_arrow')
    if 'Cursor_Resize_Horizontal' in Input:
        if Input['Cursor_Resize_Horizontal']:
            Widget.config(cursor='sb_v_double_arrow')
    if 'Cursor_Arrow' in Input:
        if Input['Cursor_Arrow']:
            Widget.config(cursor="")
    if 'Cursor' in Input:
        if Input['Cursor']:
            Widget.config(cursor=Input['Cursor'])
    if "On_Configure" in Input:
        Widget.bind("<Configure>", Input["On_Configure"], add="+")
    if "On_Destroy" in Input:
        Widget.bind("<Destroy>", Input["On_Destroy"], add="+")
    if "On_Expose" in Input:
        Widget.bind("<Expose>", Input["On_Expose"], add="+")
    if "On_Visibility" in Input:
        Widget.bind("<Visibility>", Input["On_Visibility"], add="+")
    if "On_Motion" in Input:
        Widget.bind("<Motion>", Input["On_Motion"], add="+")
    if "On_Click" in Input:
        Widget.bind("<ButtonPress-1>", Input["On_Click"], add="+")
    if "On_Release" in Input:
        Widget.bind("<ButtonRelease-1>", Input["On_Release"], add="+")
    if "On_Double_Click" in Input:
        Widget.bind("<Double-1>", Input["On_Double_Click"], add="+")
    if "On_Triple_Click" in Input:
        Widget.bind("<Triple-1>", Input["On_Triple_Click"], add="+")
    if "On_Middle_Click" in Input:
        Widget.bind("<ButtonPress-2>", Input["On_Middle_Click"], add="+")
    if "On_Middle_Release" in Input:
        Widget.bind("<ButtonRelease-2>", Input["On_Middle_Release"], add="+")
    if "On_Middle_Double_Click" in Input:
        Widget.bind("<Double-2>", Input["On_Middle_Double_Click"], add="+")
    if "On_Middle_Triple_Click" in Input:
        Widget.bind("<Triple-2>", Input["On_Middle_Triple_Click"], add="+")
    if "On_Right_Click" in Input:
        Widget.bind("<ButtonPress-3>", Input["On_Right_Click"], add="+")
    if "On_Right_Release" in Input:
        Widget.bind("<ButtonRelease-3>", Input["On_Right_Release"], add="+")
    if "On_Right_Double_Click" in Input:
        Widget.bind("<Double-3>", Input["On_Right_Double_Click"], add="+")
    if "On_Right_Triple_Click" in Input:
        Widget.bind("<Triple-3>", Input["On_Right_Triple_Click"], add="+")
    if "On_Drag" in Input:
        Widget.bind("<B1-Motion>", Input["On_Drag"], add="+")
    if "On_Middle_Drag" in Input:
        Widget.bind("<B2-Motion>", Input["On_Middle_Drag"], add="+")
    if "On_Right_Drag" in Input:
        Widget.bind("<B3-Motion>", Input["On_Right_Drag"], add="+")
    if "On_Mouse_Wheel" in Input:
        Func = Input["On_Mouse_Wheel"]
        def Mouse_Wheel_Handler(Event, Func=Func):
            if not hasattr(Event, "delta"):
                Num = getattr(Event, "num", 0)
                if Num == 4:
                    Event.delta = 120
                elif Num == 5:
                    Event.delta = -120
                else:
                    Event.delta = 0
            Func(Event)
        Widget.bind("<MouseWheel>", Mouse_Wheel_Handler, add="+")
        Widget.bind("<Button-4>", Mouse_Wheel_Handler, add="+")
        Widget.bind("<Button-5>", Mouse_Wheel_Handler, add="+")
    if "On_Hover_In" in Input:
        Widget.bind("<Enter>", Input["On_Hover_In"], add="+")
    if "On_Hover_Out" in Input:
        Widget.bind("<Leave>", Input["On_Hover_Out"], add="+")
    if "On_Key" in Input:
        Widget.bind("<KeyPress>", Input["On_Key"], add="+")
    if "On_Key_Release" in Input:
        Widget.bind("<KeyRelease>", Input["On_Key_Release"], add="+")
    if "On_Focus_In" in Input:
        Widget.bind("<FocusIn>", Input["On_Focus_In"], add="+")
    if "On_Focus_Out" in Input:
        Widget.bind("<FocusOut>", Input["On_Focus_Out"], add="+")
    if "On_Map" in Input:
        Widget.bind("<Map>", Input["On_Map"], add="+")
    if "On_Unmap" in Input:
        Widget.bind("<Unmap>", Input["On_Unmap"], add="+")
    if "On_Copy" in Input:
        Widget.bind("<<Copy>>", Input["On_Copy"], add="+")
    if "On_Cut" in Input:
        Widget.bind("<<Cut>>", Input["On_Cut"], add="+")
    if "On_Paste" in Input:
        Widget.bind("<<Paste>>", Input["On_Paste"], add="+")
    if "On_Undo" in Input:
        Widget.bind("<<Undo>>", Input["On_Undo"], add="+")
    if "On_Redo" in Input:
        Widget.bind("<<Redo>>", Input["On_Redo"], add="+")
    if "On_Control_Click" in Input:
        Widget.bind("<Control-Button-1>", Input["On_Control_Click"], add="+")
    if "On_Control_Release" in Input:
        Widget.bind("<Control-ButtonRelease-1>", Input["On_Control_Release"], add="+")
    if "On_Control_Double_Click" in Input:
        Widget.bind("<Control-Double-1>", Input["On_Control_Double_Click"], add="+")
    if "On_Control_Triple_Click" in Input:
        Widget.bind("<Control-Triple-1>", Input["On_Control_Triple_Click"], add="+")
    if "On_Control_Middle_Click" in Input:
        Widget.bind("<Control-Button-2>", Input["On_Control_Middle_Click"], add="+")
    if "On_Control_Middle_Release" in Input:
        Widget.bind("<Control-ButtonRelease-2>", Input["On_Control_Middle_Release"], add="+")
    if "On_Control_Middle_Double_Click" in Input:
        Widget.bind("<Control-Double-2>", Input["On_Control_Middle_Double_Click"], add="+")
    if "On_Control_Middle_Triple_Click" in Input:
        Widget.bind("<Control-Triple-2>", Input["On_Control_Middle_Triple_Click"], add="+")
    if "On_Control_Right_Click" in Input:
        Widget.bind("<Control-Button-3>", Input["On_Control_Right_Click"], add="+")
    if "On_Control_Right_Release" in Input:
        Widget.bind("<Control-ButtonRelease-3>", Input["On_Control_Right_Release"], add="+")
    if "On_Control_Right_Double_Click" in Input:
        Widget.bind("<Control-Double-3>", Input["On_Control_Right_Double_Click"], add="+")
    if "On_Control_Right_Triple_Click" in Input:
        Widget.bind("<Control-Triple-3>", Input["On_Control_Right_Triple_Click"], add="+")
    if "On_Control_Drag" in Input:
        Widget.bind("<Control-B1-Motion>", Input["On_Control_Drag"], add="+")
    if "On_Control_Middle_Drag" in Input:
        Widget.bind("<Control-B2-Motion>", Input["On_Control_Middle_Drag"], add="+")
    if "On_Control_Right_Drag" in Input:
        Widget.bind("<Control-B3-Motion>", Input["On_Control_Right_Drag"], add="+")
    if "On_Control_Mouse_Wheel" in Input:
        Func = Input["On_Control_Mouse_Wheel"]
        def Control_Mouse_Wheel_Handler(Event, Func=Func):
            if not hasattr(Event, "delta"):
                Num = getattr(Event, "num", 0)
                if Num == 4:
                    Event.delta = 120
                elif Num == 5:
                    Event.delta = -120
                else:
                    Event.delta = 0
            Func(Event)
        Widget.bind("<Control-MouseWheel>", Control_Mouse_Wheel_Handler, add="+")
        Widget.bind("<Control-Button-4>", Control_Mouse_Wheel_Handler, add="+")
        Widget.bind("<Control-Button-5>", Control_Mouse_Wheel_Handler, add="+")
    if "On_Control_Hover_In" in Input:
        Widget.bind("<Control-Enter>", Input["On_Control_Hover_In"], add="+")
    if "On_Control_Hover_Out" in Input:
        Widget.bind("<Control-Leave>", Input["On_Control_Hover_Out"], add="+")
    if "On_Alt_Click" in Input:
        Widget.bind("<Alt-Button-1>", Input["On_Alt_Click"], add="+")
    if "On_Alt_Release" in Input:
        Widget.bind("<Alt-ButtonRelease-1>", Input["On_Alt_Release"], add="+")
    if "On_Alt_Double_Click" in Input:
        Widget.bind("<Alt-Double-1>", Input["On_Alt_Double_Click"], add="+")
    if "On_Alt_Triple_Click" in Input:
        Widget.bind("<Alt-Triple-1>", Input["On_Alt_Triple_Click"], add="+")
    if "On_Alt_Middle_Click" in Input:
        Widget.bind("<Alt-Button-2>", Input["On_Alt_Middle_Click"], add="+")
    if "On_Alt_Middle_Release" in Input:
        Widget.bind("<Alt-ButtonRelease-2>", Input["On_Alt_Middle_Release"], add="+")
    if "On_Alt_Middle_Double_Click" in Input:
        Widget.bind("<Alt-Double-2>", Input["On_Alt_Middle_Double_Click"], add="+")
    if "On_Alt_Middle_Triple_Click" in Input:
        Widget.bind("<Alt-Triple-2>", Input["On_Alt_Middle_Triple_Click"], add="+")
    if "On_Alt_Right_Click" in Input:
        Widget.bind("<Alt-Button-3>", Input["On_Alt_Right_Click"], add="+")
    if "On_Alt_Right_Release" in Input:
        Widget.bind("<Alt-ButtonRelease-3>", Input["On_Alt_Right_Release"], add="+")
    if "On_Alt_Right_Double_Click" in Input:
        Widget.bind("<Alt-Double-3>", Input["On_Alt_Right_Double_Click"], add="+")
    if "On_Alt_Right_Triple_Click" in Input:
        Widget.bind("<Alt-Triple-3>", Input["On_Alt_Right_Triple_Click"], add="+")
    if "On_Alt_Drag" in Input:
        Widget.bind("<Alt-B1-Motion>", Input["On_Alt_Drag"], add="+")
    if "On_Alt_Middle_Drag" in Input:
        Widget.bind("<Alt-B2-Motion>", Input["On_Alt_Middle_Drag"], add="+")
    if "On_Alt_Right_Drag" in Input:
        Widget.bind("<Alt-B3-Motion>", Input["On_Alt_Right_Drag"], add="+")
    if "On_Alt_Mouse_Wheel" in Input:
        Func = Input["On_Alt_Mouse_Wheel"]
        def Alt_Mouse_Wheel_Handler(Event, Func=Func):
            if not hasattr(Event, "delta"):
                Num = getattr(Event, "num", 0)
                if Num == 4:
                    Event.delta = 120
                elif Num == 5:
                    Event.delta = -120
                else:
                    Event.delta = 0
            Func(Event)
        Widget.bind("<Alt-MouseWheel>", Alt_Mouse_Wheel_Handler, add="+")
        Widget.bind("<Alt-Button-4>", Alt_Mouse_Wheel_Handler, add="+")
        Widget.bind("<Alt-Button-5>", Alt_Mouse_Wheel_Handler, add="+")
    if "On_Alt_Hover_In" in Input:
        Widget.bind("<Alt-Enter>", Input["On_Alt_Hover_In"], add="+")
    if "On_Alt_Hover_Out" in Input:
        Widget.bind("<Alt-Leave>", Input["On_Alt_Hover_Out"], add="+")
    if "On_Shift_Click" in Input:
        Widget.bind("<Shift-Button-1>", Input["On_Shift_Click"], add="+")
    if "On_Shift_Release" in Input:
        Widget.bind("<Shift-ButtonRelease-1>", Input["On_Shift_Release"], add="+")
    if "On_Shift_Double_Click" in Input:
        Widget.bind("<Shift-Double-1>", Input["On_Shift_Double_Click"], add="+")
    if "On_Shift_Triple_Click" in Input:
        Widget.bind("<Shift-Triple-1>", Input["On_Shift_Triple_Click"], add="+")
    if "On_Shift_Middle_Click" in Input:
        Widget.bind("<Shift-Button-2>", Input["On_Shift_Middle_Click"], add="+")
    if "On_Shift_Middle_Release" in Input:
        Widget.bind("<Shift-ButtonRelease-2>", Input["On_Shift_Middle_Release"], add="+")
    if "On_Shift_Middle_Double_Click" in Input:
        Widget.bind("<Shift-Double-2>", Input["On_Shift_Middle_Double_Click"], add="+")
    if "On_Shift_Middle_Triple_Click" in Input:
        Widget.bind("<Shift-Triple-2>", Input["On_Shift_Middle_Triple_Click"], add="+")
    if "On_Shift_Right_Click" in Input:
        Widget.bind("<Shift-Button-3>", Input["On_Shift_Right_Click"], add="+")
    if "On_Shift_Right_Release" in Input:
        Widget.bind("<Shift-ButtonRelease-3>", Input["On_Shift_Right_Release"], add="+")
    if "On_Shift_Right_Double_Click" in Input:
        Widget.bind("<Shift-Double-3>", Input["On_Shift_Right_Double_Click"], add="+")
    if "On_Shift_Right_Triple_Click" in Input:
        Widget.bind("<Shift-Triple-3>", Input["On_Shift_Right_Triple_Click"], add="+")
    if "On_Shift_Drag" in Input:
        Widget.bind("<Shift-B1-Motion>", Input["On_Shift_Drag"], add="+")
    if "On_Shift_Middle_Drag" in Input:
        Widget.bind("<Shift-B2-Motion>", Input["On_Shift_Middle_Drag"], add="+")
    if "On_Shift_Right_Drag" in Input:
        Widget.bind("<Shift-B3-Motion>", Input["On_Shift_Right_Drag"], add="+")
    if "On_Shift_Mouse_Wheel" in Input:
        Func = Input["On_Shift_Mouse_Wheel"]
        def Shift_Mouse_Wheel_Handler(Event, Func=Func):
            if not hasattr(Event, "delta"):
                Num = getattr(Event, "num", 0)
                if Num == 4:
                    Event.delta = 120
                elif Num == 5:
                    Event.delta = -120
                else:
                    Event.delta = 0
            Func(Event)
        Widget.bind("<Shift-MouseWheel>", Shift_Mouse_Wheel_Handler, add="+")
        Widget.bind("<Shift-Button-4>", Shift_Mouse_Wheel_Handler, add="+")
        Widget.bind("<Shift-Button-5>", Shift_Mouse_Wheel_Handler, add="+")
    if "On_Shift_Hover_In" in Input:
        Widget.bind("<Shift-Enter>", Input["On_Shift_Hover_In"], add="+")
    if "On_Shift_Hover_Out" in Input:
        Widget.bind("<Shift-Leave>", Input["On_Shift_Hover_Out"], add="+")

def Event_Bind_Canvas(Widget, Item, **Input):
    if "On_Motion" in Input:
        Widget.tag_bind(Item, "<Motion>", Input["On_Motion"], add="+")
    if "On_Click" in Input:
        Widget.tag_bind(Item, "<ButtonPress-1>", Input["On_Click"], add="+")
    if "On_Release" in Input:
        Widget.tag_bind(Item, "<ButtonRelease-1>", Input["On_Release"], add="+")
    if "On_Double_Click" in Input:
        Widget.tag_bind(Item, "<Double-1>", Input["On_Double_Click"], add="+")
    if "On_Triple_Click" in Input:
        Widget.tag_bind(Item, "<Triple-1>", Input["On_Triple_Click"], add="+")
    if "On_Middle_Click" in Input:
        Widget.tag_bind(Item, "<ButtonPress-2>", Input["On_Middle_Click"], add="+")
    if "On_Middle_Release" in Input:
        Widget.tag_bind(Item, "<ButtonRelease-2>", Input["On_Middle_Release"], add="+")
    if "On_Middle_Double_Click" in Input:
        Widget.tag_bind(Item, "<Double-2>", Input["On_Middle_Double_Click"], add="+")
    if "On_Middle_Triple_Click" in Input:
        Widget.tag_bind(Item, "<Triple-2>", Input["On_Middle_Triple_Click"], add="+")
    if "On_Right_Click" in Input:
        Widget.tag_bind(Item, "<ButtonPress-3>", Input["On_Right_Click"], add="+")
    if "On_Right_Release" in Input:
        Widget.tag_bind(Item, "<ButtonRelease-3>", Input["On_Right_Release"], add="+")
    if "On_Right_Double_Click" in Input:
        Widget.tag_bind(Item, "<Double-3>", Input["On_Right_Double_Click"], add="+")
    if "On_Right_Triple_Click" in Input:
        Widget.tag_bind(Item, "<Triple-3>", Input["On_Right_Triple_Click"], add="+")
    if "On_Drag" in Input:
        Widget.tag_bind(Item, "<B1-Motion>", Input["On_Drag"], add="+")
    if "On_Middle_Drag" in Input:
        Widget.tag_bind(Item, "<B2-Motion>", Input["On_Middle_Drag"], add="+")
    if "On_Right_Drag" in Input:
        Widget.tag_bind(Item, "<B3-Motion>", Input["On_Right_Drag"], add="+")
    if "On_Mouse_Wheel" in Input:
        Func = Input["On_Mouse_Wheel"]
        def Mouse_Wheel_Handler(Event, Func=Func):
            if not hasattr(Event, "delta"):
                Num = getattr(Event, "num", 0)
                if Num == 4:
                    Event.delta = 120
                elif Num == 5:
                    Event.delta = -120
                else:
                    Event.delta = 0
            Func(Event)
        Widget.tag_bind(Item, "<Button-4>", Mouse_Wheel_Handler, add="+")
        Widget.tag_bind(Item, "<Button-5>", Mouse_Wheel_Handler, add="+")
    if "On_Hover_In" in Input:
        Widget.tag_bind(Item, "<Enter>", Input["On_Hover_In"], add="+")
    if "On_Hover_Out" in Input:
        Widget.tag_bind(Item, "<Leave>", Input["On_Hover_Out"], add="+")
    if "On_Key" in Input:
        Widget.tag_bind(Item, "<KeyPress>", Input["On_Key"], add="+")
    if "On_Key_Release" in Input:
        Widget.tag_bind(Item, "<KeyRelease>", Input["On_Key_Release"], add="+")
    if "On_Copy" in Input:
        Widget.tag_bind(Item, "<<Copy>>", Input["On_Copy"], add="+")
    if "On_Cut" in Input:
        Widget.tag_bind(Item, "<<Cut>>", Input["On_Cut"], add="+")
    if "On_Paste" in Input:
        Widget.tag_bind(Item, "<<Paste>>", Input["On_Paste"], add="+")
    if "On_Undo" in Input:
        Widget.tag_bind(Item, "<<Undo>>", Input["On_Undo"], add="+")
    if "On_Redo" in Input:
        Widget.tag_bind(Item, "<<Redo>>", Input["On_Redo"], add="+")
    if "On_Control_Click" in Input:
        Widget.tag_bind(Item, "<Control-Button-1>", Input["On_Control_Click"], add="+")
    if "On_Control_Release" in Input:
        Widget.tag_bind(Item, "<Control-ButtonRelease-1>", Input["On_Control_Release"], add="+")
    if "On_Control_Double_Click" in Input:
        Widget.tag_bind(Item, "<Control-Double-1>", Input["On_Control_Double_Click"], add="+")
    if "On_Control_Triple_Click" in Input:
        Widget.tag_bind(Item, "<Control-Triple-1>", Input["On_Control_Triple_Click"], add="+")
    if "On_Control_Middle_Click" in Input:
        Widget.tag_bind(Item, "<Control-Button-2>", Input["On_Control_Middle_Click"], add="+")
    if "On_Control_Middle_Release" in Input:
        Widget.tag_bind(Item, "<Control-ButtonRelease-2>", Input["On_Control_Middle_Release"], add="+")
    if "On_Control_Middle_Double_Click" in Input:
        Widget.tag_bind(Item, "<Control-Double-2>", Input["On_Control_Middle_Double_Click"], add="+")
    if "On_Control_Middle_Triple_Click" in Input:
        Widget.tag_bind(Item, "<Control-Triple-2>", Input["On_Control_Middle_Triple_Click"], add="+")
    if "On_Control_Right_Click" in Input:
        Widget.tag_bind(Item, "<Control-Button-3>", Input["On_Control_Right_Click"], add="+")
    if "On_Control_Right_Release" in Input:
        Widget.tag_bind(Item, "<Control-ButtonRelease-3>", Input["On_Control_Right_Release"], add="+")
    if "On_Control_Right_Double_Click" in Input:
        Widget.tag_bind(Item, "<Control-Double-3>", Input["On_Control_Right_Double_Click"], add="+")
    if "On_Control_Right_Triple_Click" in Input:
        Widget.tag_bind(Item, "<Control-Triple-3>", Input["On_Control_Right_Triple_Click"], add="+")
    if "On_Control_Drag" in Input:
        Widget.tag_bind(Item, "<Control-B1-Motion>", Input["On_Control_Drag"], add="+")
    if "On_Control_Middle_Drag" in Input:
        Widget.tag_bind(Item, "<Control-B2-Motion>", Input["On_Control_Middle_Drag"], add="+")
    if "On_Control_Right_Drag" in Input:
        Widget.tag_bind(Item, "<Control-B3-Motion>", Input["On_Control_Right_Drag"], add="+")
    if "On_Control_Hover_In" in Input:
        Widget.tag_bind(Item, "<Control-Enter>", Input["On_Control_Hover_In"], add="+")
    if "On_Control_Hover_Out" in Input:
        Widget.tag_bind(Item, "<Control-Leave>", Input["On_Control_Hover_Out"], add="+")
    if "On_Alt_Click" in Input:
        Widget.tag_bind(Item, "<Alt-Button-1>", Input["On_Alt_Click"], add="+")
    if "On_Alt_Release" in Input:
        Widget.tag_bind(Item, "<Alt-ButtonRelease-1>", Input["On_Alt_Release"], add="+")
    if "On_Alt_Double_Click" in Input:
        Widget.tag_bind(Item, "<Alt-Double-1>", Input["On_Alt_Double_Click"], add="+")
    if "On_Alt_Triple_Click" in Input:
        Widget.tag_bind(Item, "<Alt-Triple-1>", Input["On_Alt_Triple_Click"], add="+")
    if "On_Alt_Middle_Click" in Input:
        Widget.tag_bind(Item, "<Alt-Button-2>", Input["On_Alt_Middle_Click"], add="+")
    if "On_Alt_Middle_Release" in Input:
        Widget.tag_bind(Item, "<Alt-ButtonRelease-2>", Input["On_Alt_Middle_Release"], add="+")
    if "On_Alt_Middle_Double_Click" in Input:
        Widget.tag_bind(Item, "<Alt-Double-2>", Input["On_Alt_Middle_Double_Click"], add="+")
    if "On_Alt_Middle_Triple_Click" in Input:
        Widget.tag_bind(Item, "<Alt-Triple-2>", Input["On_Alt_Middle_Triple_Click"], add="+")
    if "On_Alt_Right_Click" in Input:
        Widget.tag_bind(Item, "<Alt-Button-3>", Input["On_Alt_Right_Click"], add="+")
    if "On_Alt_Right_Release" in Input:
        Widget.tag_bind(Item, "<Alt-ButtonRelease-3>", Input["On_Alt_Right_Release"], add="+")
    if "On_Alt_Right_Double_Click" in Input:
        Widget.tag_bind(Item, "<Alt-Double-3>", Input["On_Alt_Right_Double_Click"], add="+")
    if "On_Alt_Right_Triple_Click" in Input:
        Widget.tag_bind(Item, "<Alt-Triple-3>", Input["On_Alt_Right_Triple_Click"], add="+")
    if "On_Alt_Drag" in Input:
        Widget.tag_bind(Item, "<Alt-B1-Motion>", Input["On_Alt_Drag"], add="+")
    if "On_Alt_Middle_Drag" in Input:
        Widget.tag_bind(Item, "<Alt-B2-Motion>", Input["On_Alt_Middle_Drag"], add="+")
    if "On_Alt_Right_Drag" in Input:
        Widget.tag_bind(Item, "<Alt-B3-Motion>", Input["On_Alt_Right_Drag"], add="+")
    if "On_Alt_Hover_In" in Input:
        Widget.tag_bind(Item, "<Alt-Enter>", Input["On_Alt_Hover_In"], add="+")
    if "On_Alt_Hover_Out" in Input:
        Widget.tag_bind(Item, "<Alt-Leave>", Input["On_Alt_Hover_Out"], add="+")
    if "On_Shift_Click" in Input:
        Widget.tag_bind(Item, "<Shift-Button-1>", Input["On_Shift_Click"], add="+")
    if "On_Shift_Release" in Input:
        Widget.tag_bind(Item, "<Shift-ButtonRelease-1>", Input["On_Shift_Release"], add="+")
    if "On_Shift_Double_Click" in Input:
        Widget.tag_bind(Item, "<Shift-Double-1>", Input["On_Shift_Double_Click"], add="+")
    if "On_Shift_Triple_Click" in Input:
        Widget.tag_bind(Item, "<Shift-Triple-1>", Input["On_Shift_Triple_Click"], add="+")
    if "On_Shift_Middle_Click" in Input:
        Widget.tag_bind(Item, "<Shift-Button-2>", Input["On_Shift_Middle_Click"], add="+")
    if "On_Shift_Middle_Release" in Input:
        Widget.tag_bind(Item, "<Shift-ButtonRelease-2>", Input["On_Shift_Middle_Release"], add="+")
    if "On_Shift_Middle_Double_Click" in Input:
        Widget.tag_bind(Item, "<Shift-Double-2>", Input["On_Shift_Middle_Double_Click"], add="+")
    if "On_Shift_Middle_Triple_Click" in Input:
        Widget.tag_bind(Item, "<Shift-Triple-2>", Input["On_Shift_Middle_Triple_Click"], add="+")
    if "On_Shift_Right_Click" in Input:
        Widget.tag_bind(Item, "<Shift-Button-3>", Input["On_Shift_Right_Click"], add="+")
    if "On_Shift_Right_Release" in Input:
        Widget.tag_bind(Item, "<Shift-ButtonRelease-3>", Input["On_Shift_Right_Release"], add="+")
    if "On_Shift_Right_Double_Click" in Input:
        Widget.tag_bind(Item, "<Shift-Double-3>", Input["On_Shift_Right_Double_Click"], add="+")
    if "On_Shift_Right_Triple_Click" in Input:
        Widget.tag_bind(Item, "<Shift-Triple-3>", Input["On_Shift_Right_Triple_Click"], add="+")
    if "On_Shift_Drag" in Input:
        Widget.tag_bind(Item, "<Shift-B1-Motion>", Input["On_Shift_Drag"], add="+")
    if "On_Shift_Middle_Drag" in Input:
        Widget.tag_bind(Item, "<Shift-B2-Motion>", Input["On_Shift_Middle_Drag"], add="+")
    if "On_Shift_Right_Drag" in Input:
        Widget.tag_bind(Item, "<Shift-B3-Motion>", Input["On_Shift_Right_Drag"], add="+")
    if "On_Shift_Hover_In" in Input:
        Widget.tag_bind(Item, "<Shift-Enter>", Input["On_Shift_Hover_In"], add="+")
    if "On_Shift_Hover_Out" in Input:
        Widget.tag_bind(Item, "<Shift-Leave>", Input["On_Shift_Hover_Out"], add="+")
