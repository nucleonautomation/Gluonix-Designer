Event_Map = {
    'On_Click': '<Button-1>',
    'On_Release': '<ButtonRelease-1>',
    'On_Double_Click': '<Double-Button-1>',
    'On_Triple_Click': '<Triple-Button-1>',
    'On_Right_Click': '<Button-3>',
    'On_Right_Release': '<ButtonRelease-3>',
    'On_Right_Double_Click': '<Double-Button-3>',
    'On_Right_Triple_Click': '<Triple-Button-3>',
    'On_Middle_Click': '<Button-2>',
    'On_Middle_Release': '<ButtonRelease-2>',
    'On_Middle_Double_Click': '<Double-Button-2>',
    'On_Middle_Triple_Click': '<Triple-Button-2>',
    'On_Drag': '<B1-Motion>',
    'On_Right_Drag': '<B3-Motion>',
    'On_Middle_Drag': '<B2-Motion>',
    'On_Hover_In': '<Enter>',
    'On_Hover_Out': '<Leave>',
    'On_Motion': '<Motion>',
    'On_Focus_In': '<FocusIn>',
    'On_Focus_Out': '<FocusOut>',
    'On_Key': '<KeyPress>',
    'On_Key_Release': '<KeyRelease>',
    'On_Configure': '<Configure>',
    'On_Map': '<Map>',
    'On_Unmap': '<Unmap>',
    'On_Destroy': '<Destroy>',
    'On_Expose': '<Expose>',
    'On_Visibility': '<Visibility>',
    'On_Mouse_Wheel': ['<MouseWheel>', '<Button-4>', '<Button-5>'],
    'On_Copy': '<<Copy>>',
    'On_Paste': '<<Paste>>',
    'On_Cut': '<<Cut>>',
    'On_Undo': '<<Undo>>',
    'On_Redo': '<<Redo>>',
    'On_Control_Click': '<Control-Button-1>',
    'On_Control_Release': '<Control-ButtonRelease-1>',
    'On_Control_Double_Click': '<Control-Double-Button-1>',
    'On_Control_Triple_Click': '<Control-Triple-Button-1>',
    'On_Control_Right_Click': '<Control-Button-3>',
    'On_Control_Right_Release': '<Control-ButtonRelease-3>',
    'On_Control_Right_Double_Click': '<Control-Double-Button-3>',
    'On_Control_Right_Triple_Click': '<Control-Triple-Button-3>',
    'On_Control_Middle_Click': '<Control-Button-2>',
    'On_Control_Middle_Release': '<Control-ButtonRelease-2>',
    'On_Control_Middle_Double_Click': '<Control-Double-Button-2>',
    'On_Control_Middle_Triple_Click': '<Control-Triple-Button-2>',
    'On_Control_Drag': '<Control-B1-Motion>',
    'On_Control_Right_Drag': '<Control-B3-Motion>',
    'On_Control_Middle_Drag': '<Control-B2-Motion>',
    'On_Control_Hover_In': '<Control-Enter>',
    'On_Control_Hover_Out': '<Control-Leave>',
    'On_Control_Mouse_Wheel': ['<Control-MouseWheel>', '<Control-Button-4>', '<Control-Button-5>'],
    'On_Shift_Click': '<Shift-Button-1>',
    'On_Shift_Release': '<Shift-ButtonRelease-1>',
    'On_Shift_Double_Click': '<Shift-Double-Button-1>',
    'On_Shift_Triple_Click': '<Shift-Triple-Button-1>',
    'On_Shift_Right_Click': '<Shift-Button-3>',
    'On_Shift_Right_Release': '<Shift-ButtonRelease-3>',
    'On_Shift_Right_Double_Click': '<Shift-Double-Button-3>',
    'On_Shift_Right_Triple_Click': '<Shift-Triple-Button-3>',
    'On_Shift_Middle_Click': '<Shift-Button-2>',
    'On_Shift_Middle_Release': '<Shift-ButtonRelease-2>',
    'On_Shift_Middle_Double_Click': '<Shift-Double-Button-2>',
    'On_Shift_Middle_Triple_Click': '<Shift-Triple-Button-2>',
    'On_Shift_Drag': '<Shift-B1-Motion>',
    'On_Shift_Right_Drag': '<Shift-B3-Motion>',
    'On_Shift_Middle_Drag': '<Shift-B2-Motion>',
    'On_Shift_Hover_In': '<Shift-Enter>',
    'On_Shift_Hover_Out': '<Shift-Leave>',
    'On_Shift_Mouse_Wheel': ['<Shift-MouseWheel>', '<Shift-Button-4>', '<Shift-Button-5>'],
    'On_Alt_Click': '<Alt-Button-1>',
    'On_Alt_Release': '<Alt-ButtonRelease-1>',
    'On_Alt_Double_Click': '<Alt-Double-Button-1>',
    'On_Alt_Triple_Click': '<Alt-Triple-Button-1>',
    'On_Alt_Right_Click': '<Alt-Button-3>',
    'On_Alt_Right_Release': '<Alt-ButtonRelease-3>',
    'On_Alt_Right_Double_Click': '<Alt-Double-Button-3>',
    'On_Alt_Right_Triple_Click': '<Alt-Triple-Button-3>',
    'On_Alt_Middle_Click': '<Alt-Button-2>',
    'On_Alt_Middle_Release': '<Alt-ButtonRelease-2>',
    'On_Alt_Middle_Double_Click': '<Alt-Double-Button-2>',
    'On_Alt_Middle_Triple_Click': '<Alt-Triple-Button-2>',
    'On_Alt_Drag': '<Alt-B1-Motion>',
    'On_Alt_Right_Drag': '<Alt-B3-Motion>',
    'On_Alt_Middle_Drag': '<Alt-B2-Motion>',
    'On_Alt_Hover_In': '<Alt-Enter>',
    'On_Alt_Hover_Out': '<Alt-Leave>',
    'On_Alt_Mouse_Wheel': ['<Alt-MouseWheel>', '<Alt-Button-4>', '<Alt-Button-5>'],
}

def Event_Bind(Widget, **Input):
    Bind_Add = "+"
    if 'Add' in Input and Input['Add'] is False:
        Bind_Add = ""
    if 'Cursor' in Input:
        Widget.config(cursor=Input['Cursor'])
    elif 'Cursor_Hand' in Input and Input['Cursor_Hand']:
        Widget.config(cursor="hand2")
    elif 'Cursor_Loading' in Input and Input['Cursor_Loading']:
        Widget.config(cursor="watch")
    elif 'Cursor_Resize_Vertical' in Input and Input['Cursor_Resize_Vertical']:
        Widget.config(cursor='sb_v_double_arrow')
    elif 'Cursor_Resize_Horizontal' in Input and Input['Cursor_Resize_Horizontal']:
        Widget.config(cursor='sb_h_double_arrow')
    elif 'Cursor_Arrow' in Input and Input['Cursor_Arrow']:
        Widget.config(cursor='arrow')
    for Key, Value in Input.items():
        if Key in Event_Map:
            Sequences = Event_Map[Key]
            if isinstance(Sequences, list):
                for Seq in Sequences:
                    Widget.bind(Seq, Value, add=Bind_Add)
            else:
                Widget.bind(Sequences, Value, add=Bind_Add)

def Event_Bind_Canvas(Widget, Item, **Input):
    Bind_Add = "+"
    if 'Add' in Input and Input['Add'] is False:
        Bind_Add = ""
    for Key, Value in Input.items():
        if Key in Event_Map:
            Sequences = Event_Map[Key]
            if isinstance(Sequences, list):
                for Seq in Sequences:
                    Widget.tag_bind(Item, Seq, Value, add=Bind_Add)
            else:
                Widget.tag_bind(Item, Sequences, Value, add=Bind_Add)