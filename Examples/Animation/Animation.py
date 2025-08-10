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

    import _thread
    import time

    Root.Label1.Hide()
    Root.Label2.Hide()
    Root.Label3.Hide()
    Root.Label4.Hide()

    def Run():
        time.sleep(0.3)
        Left, Top = Root.Label1.Position()
        Width, Height  = Root.Label1.Size()
        Root.Label1.Config(Animate_Left=int(Left+Width/2), Animate_Top=int(Top+Height/2), Animate_Width=1, Animate_Height=1, Animate_Time=1)
        Root.Label1.Animate()
        time.sleep(1)
        Left, Top = Root.Label2.Position()
        Width, Height  = Root.Label2.Size()
        Root.Label2.Config(Animate_Left=int(Left), Animate_Top=int(Top+Height/2), Animate_Width=1, Animate_Height=1, Animate_Time=1)
        Root.Label2.Animate()
        time.sleep(1)
        Left, Top = Root.Label3.Position()
        Width, Height  = Root.Label3.Size()
        Root.Label3.Config(Animate_Left=Left, Animate_Top=Height*-1, Animate_Time=1)
        Root.Label3.Animate()
        time.sleep(1)
        Left, Top = Root.Label4.Position()
        Width, Height  = Root.Label4.Size()
        Root.Label4.Config(Animate_Left=Width*-1, Animate_Top=Height*-1, Animate_Time=1)
        Root.Label4.Animate()
        
    _thread.start_new_thread(Run, ())

# -------------------------------------------------------------------------------------------------------------------------------
# Developer Programming End
# -------------------------------------------------------------------------------------------------------------------------------
#################################################################################################################################
#################################################################################################################################
    Root.Start() ###!REQUIRED ------- Any Script After This Will Not Execute
#################################################################################################################################