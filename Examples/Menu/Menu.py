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

    Command = {
                'File': {
                    'New': lambda: print('File -> New'),
                    'Open': lambda: print('File -> Open'),
                    'Open_Recent': {
                        'Project_A': lambda: print('File -> Open_Recent -> Project_A'),
                        'Project_B': lambda: print('File -> Open_Recent -> Project_B'),
                        'Project_C': lambda: print('File -> Open_Recent -> Project_C'),
                        'S1': '',
                        'Clear_Recent': lambda: print('File -> Open_Recent -> Clear_Recent')
                    },
                    'S1': '',
                    'Save': lambda: print('File -> Save'),
                    'Save_As': lambda: print('File -> Save_As'),
                    'Export': {
                        'Image': lambda: print('File -> Export -> Image'),
                        'PDF': lambda: print('File -> Export -> PDF'),
                        'Data': {
                            'CSV': lambda: print('File -> Export -> Data -> CSV'),
                            'JSON': lambda: print('File -> Export -> Data -> JSON'),
                            'XML': lambda: print('File -> Export -> Data -> XML')
                        }
                    },
                    'S2': '',
                    'Close': lambda: print('File -> Close'),
                    'Exit': lambda: print('File -> Exit')
                },
                'Edit': {
                    'Undo': lambda: print('Edit -> Undo'),
                    'Redo': lambda: print('Edit -> Redo'),
                    'S1': '',
                    'Cut': lambda: print('Edit -> Cut'),
                    'Copy': lambda: print('Edit -> Copy'),
                    'Paste': lambda: print('Edit -> Paste'),
                    'Duplicate': lambda: print('Edit -> Duplicate'),
                    'S2': '',
                    'Find': {
                        'Find': lambda: print('Edit -> Find -> Find'),
                        'Find_Next': lambda: print('Edit -> Find -> Find_Next'),
                        'Find_Previous': lambda: print('Edit -> Find -> Find_Previous'),
                        'Replace': lambda: print('Edit -> Find -> Replace')
                    }
                },
                'View': {
                    'Zoom_In': lambda: print('View -> Zoom_In'),
                    'Zoom_Out': lambda: print('View -> Zoom_Out'),
                    'Reset_Zoom': lambda: print('View -> Reset_Zoom'),
                    'S1': '',
                    'Panels': {
                        'Toolbar': lambda: print('View -> Panels -> Toolbar'),
                        'Sidebar': lambda: print('View -> Panels -> Sidebar'),
                        'Statusbar': lambda: print('View -> Panels -> Statusbar'),
                        'Advanced': {
                            'Inspector': lambda: print('View -> Panels -> Advanced -> Inspector'),
                            'Console': lambda: print('View -> Panels -> Advanced -> Console'),
                            'Profiler': lambda: print('View -> Panels -> Advanced -> Profiler')
                        }
                    },
                    'Theme': {
                        'Light': lambda: print('View -> Theme -> Light'),
                        'Dark': lambda: print('View -> Theme -> Dark'),
                        'System': lambda: print('View -> Theme -> System')
                    }
                },
                'Tools': {
                    'Run': lambda: print('Tools -> Run'),
                    'Stop': lambda: print('Tools -> Stop'),
                    'Reload': lambda: print('Tools -> Reload'),
                    'S1': '',
                    'Generate': {
                        'Report': lambda: print('Tools -> Generate -> Report'),
                        'Preview': lambda: print('Tools -> Generate -> Preview'),
                        'Assets': {
                            'Icons': lambda: print('Tools -> Generate -> Assets -> Icons'),
                            'Images': lambda: print('Tools -> Generate -> Assets -> Images'),
                            'Thumbnails': lambda: print('Tools -> Generate -> Assets -> Thumbnails')
                        }
                    },
                    'Batch': {
                        'Process_1': lambda: print('Tools -> Batch -> Process_1'),
                        'Process_2': lambda: print('Tools -> Batch -> Process_2'),
                        'Deep': {
                            'Level_1': {
                                'Level_2': {
                                    'Level_3_A': lambda: print('Tools -> Batch -> Deep -> Level_1 -> Level_2 -> Level_3_A'),
                                    'Level_3_B': lambda: print('Tools -> Batch -> Deep -> Level_1 -> Level_2 -> Level_3_B')
                                }
                            }
                        }
                    }
                },
                'Window': {
                    'Minimize': lambda: print('Window -> Minimize'),
                    'Maximize': lambda: print('Window -> Maximize'),
                    'Restore': lambda: print('Window -> Restore'),
                    'S1': '',
                    'Layouts': {
                        'Default': lambda: print('Window -> Layouts -> Default'),
                        'Compact': lambda: print('Window -> Layouts -> Compact'),
                        'Wide': lambda: print('Window -> Layouts -> Wide'),
                        'Debug': lambda: print('Window -> Layouts -> Debug')
                    }
                },
                'Help': {
                    'Documentation': lambda: print('Help -> Documentation'),
                    'Shortcuts': lambda: print('Help -> Shortcuts'),
                    'Examples': {
                        'Basic': lambda: print('Help -> Examples -> Basic'),
                        'Advanced': lambda: print('Help -> Examples -> Advanced'),
                        'Widgets': {
                            'Button': lambda: print('Help -> Examples -> Widgets -> Button'),
                            'Label': lambda: print('Help -> Examples -> Widgets -> Label'),
                            'Menu': lambda: print('Help -> Examples -> Widgets -> Menu')
                        }
                    },
                    'S1': '',
                    'About': lambda: print('Help -> About')
                }
            }

    Menu = Root.Menu()
    
    Menu.Set(Command)
    
    Root.L.Bind(On_Click=lambda E: Menu.Open(Widget=Root.L))

# -------------------------------------------------------------------------------------------------------------------------------
# Developer Programming End
# -------------------------------------------------------------------------------------------------------------------------------
#################################################################################################################################
#################################################################################################################################
    Root.Start() ###!REQUIRED ------- Any Script After This Will Not Execute
#################################################################################################################################