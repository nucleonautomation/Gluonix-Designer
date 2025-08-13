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

    import random
    import time
    import _thread

    # -----------------------------
    # Setup: Difficulty + Run button
    # -----------------------------
    Difficulty = Gluonix.Variable()

    Setup = Root.Setup
    Setup.Easy.Config(Variable=Difficulty, Value=30)
    Setup.Medium.Config(Variable=Difficulty, Value=20)
    Setup.Hard.Config(Variable=Difficulty, Value=10)
    Setup.Easy.Set()

    Setup.Run.Config(
        Background='#82e0aa',
        Shadow_Color='#82e0aa',
        Hover_Background='#2ecc71',
        Hover_Shadow_Color='#2ecc71',
        Foreground='#FFFFFF'
    )
    Setup.Run.Bind(On_Click=lambda E: Run_Game())

    def Run_Game():
        global New_Left, New_Top, Mid_Left, Mid_Top, Running, Stopped, Changing, Clicked, Missed, Time
        Setup.Hide()
        Apply_Style('Default', 'CLICK ME')
        R.Bind(On_Hover_In=On_Hover_In, On_Click=On_Click)
        New_Left, New_Top = 0, 0
        Mid_Left, Mid_Top = 0, 0
        Missed, Time = 0, 0
        Running  = False   # Animation In Progress
        Stopped  = False   # Game Ended
        Changing = False   # Between "MISSED" and Reset
        Clicked  = False   # Click Lock
        Root.Stats.Time.Set(Format_Time(Time))
        Root.Stats.Missed.Set(0)
        Root.Stats.Show()
        Root.Game.Show()

    # -----------------------------
    # Theme and Hlpers
    # -----------------------------
    THEME = {
        'Default': {'bg': '#af7ac5', 'fg': '#FFFFFF'},
        'Missed':  {'bg': '#ec7063', 'fg': '#FFFFFF'},
        'Won':     {'bg': '#48c9b0', 'fg': '#FFFFFF'},
    }

    def Apply_Style(State, Text=None):
        if Text is not None:
            R.Set(Text)
        Colors = THEME.get(State, THEME['Default'])
        R.Config(Background=Colors['bg'], Shadow_Color=Colors['bg'], Foreground=Colors['fg'])

    # -----------------------------
    # Game Window
    # -----------------------------
    Root_Width, Root_Height = Root.Game.Size()

    R = Root.Game.R
    R.Config(Animate_Time=0.2)

    Width, Height = R.Size()
    Max_Left = Root_Width - Width
    Max_Top  = Root_Height - Height
    Half_W = Width // 2
    Half_H = Height // 2

    # State flags
    New_Left, New_Top = 0, 0
    Mid_Left, Mid_Top = 0, 0
    Missed, Time = 0, 0
    Running  = False   # Animation In Progress
    Stopped  = False   # Game Ended
    Changing = False   # Between "MISSED" and Reset
    Clicked  = False   # Click Lock

    # -----------------------------
    # Animation Lifecycle
    # -----------------------------
    def Post_Animate():
        global Changing, Stopped
        if not Changing and not Stopped:
            Apply_Style('Missed', 'MISSED')
            Root.After(1000, lambda: Initial())
            Changing = True

    def Initial():
        global Changing, Stopped
        if Changing and not Stopped:
            Apply_Style('Default', 'CLICK ME')
            Changing = False

    def On_Click(E):
        global Stopped, Clicked, Changing
        if not Clicked:
            Changing = False
            Stopped = True
            Apply_Style('Won', 'YOU WON')
            R.Bind(On_Click=Restart)
            Root.After(2000, lambda: Apply_Style('Won', 'PLAY AGAIN'))
            
    def Restart(E):
        Root.Game.Hide()
        Setup.Show()

    def Prevent_Click():
        global Clicked
        Clicked = True

    def Find_New_Position(Avoid_Left, Avoid_Top, Avoid_Radius):
        Dis_W_Min = Avoid_Left  - Avoid_Radius - Width
        Dis_W_Max = Avoid_Left  + Avoid_Radius + Width
        Dis_H_Min = Avoid_Top   - Avoid_Radius - Height
        Dis_H_Max = Avoid_Top   + Avoid_Radius + Height
        Left = random.randint(10, max(10, Max_Left - 10))
        Top  = random.randint(10, max(10, Max_Top  - 10))
        while (Dis_W_Min < Left + Half_W < Dis_W_Max) and (Dis_H_Min < Top + Half_H < Dis_H_Max):
            Left = random.randint(10, max(10, Max_Left - 10))
            Top  = random.randint(10, max(10, Max_Top  - 10))
        return Left, Top

    def On_Hover_In(E):
        global New_Left, New_Top, Mid_Left, Mid_Top, Running, Stopped, Changing, Missed
        if Running or Stopped:
            return
        Missed += 1
        Root.After(Difficulty.Get(), lambda: Prevent_Click())
        Changing = False
        Running = True
        Left, Top = R.Position()
        Avoid_Left  = Left + E.x
        Avoid_Top   = Top + E.y
        Avoid_Range = 100
        New_Left, New_Top = Find_New_Position(Avoid_Left, Avoid_Top, Avoid_Range)
        Mid_Left = int((New_Left + Left + Half_W) / 2)
        Mid_Top  = int((New_Top  + Top + Half_H) / 2)
        R.Size(Half_W, Half_H)
        R.Position(Mid_Left, Mid_Top)
        R.Config(Animate_Left=Left, Animate_Top=Top, Animate_Width=Width, Animate_Height=Height)
        R.Bind(On_Animate=lambda: On_Animate())
        R.Animate(Hide=True)
        Root.Stats.Missed.Set(Missed)

    def On_Animate():
        global New_Left, New_Top, Mid_Left, Mid_Top, Running, Clicked
        R.Size(Width, Height)
        R.Position(New_Left, New_Top)
        R.Config(Animate_Left=Mid_Left, Animate_Top=Mid_Top, Animate_Width=Half_W, Animate_Height=Half_H)
        R.Bind(On_Animate=lambda: Post_Animate())
        R.Animate()
        Running = False
        Clicked = False
        
    def Format_Time(Seconds):
        Hours, rem = divmod(Seconds, 3600)
        Minutes, Seconds_Remaining = divmod(rem, 60)
        return f"{Hours}h {Minutes}m {Seconds_Remaining}s"
        
    def Game_Time():
        global Time, Stopped
        while True:
            time.sleep(1)
            if not Stopped:
                Time += 1
                Root.Stats.Time.Set(Format_Time(Time))
            
    _thread.start_new_thread(Game_Time, ())

# -------------------------------------------------------------------------------------------------------------------------------
# Developer Programming End
# -------------------------------------------------------------------------------------------------------------------------------
#################################################################################################################################
#################################################################################################################################
    Root.Start() ###!REQUIRED ------- Any Script After This Will Not Execute
#################################################################################################################################
