import os
import subprocess
import hashlib
import keyword
import re
import builtins

    #Get System UUID
def UUID():
    if os.name == 'nt':
        return subprocess.check_output('wmic csproduct get uuid').decode().split('\n')[1].strip()
    else:
        Output = subprocess.check_output(['sudo', 'dmidecode', '-s', 'system-uuid'], stderr=subprocess.STDOUT)
        return Output.decode().strip()
    
    #Check Empty Folder
def Is_Empty(Path):
    return len(os.listdir(Path)) == 0
    
    #MD5 Hash Generator
def MD5(String):
    return hashlib.md5(String.encode('utf-8')).hexdigest()
    
    #String Is Float
def Is_Float(String):
    try:
        float(String)
        return True
    except:
        return False
    
    #String Is Int
def Is_Int(String):
    try:
        int(String)
        return True
    except:
        return False
        
    #Get Attribute
def Get_Attr_Class(Object, Attr):
    Attributes = Attr.split('.')
    for Attribute in Attributes:
        Object = getattr(Object, Attribute)
    return Object
    
    #Valid Variable
def Valid_Variable(Name):
    Custom = ['Error', 'Nothing', 'Maximize', 'Restart',  'Close',  'Hide', 'Show', 'Display', 'Save', 'Start', 'Event', 'Event_Runner', 'After', 'Screen', 'Full_Screen', 'Widget', 'Bind', 'Config_Get', 'Config', 'Add_Menu', 'Add_Sub_Manu', 'Add_Separator', 'Folder', 'File', 'Grab', 'Position', 'Locate', 'Locate_Reverse', 'Locate_Fullscreen', 'Create', 'Copy', 'Delete', 'Clear', 'Adjustment', 'Relocate', 'Resize', 'Top', 'Reset', 'Scroll', 'Bind_Item', 'Update', 'Update_All', 'Hide_Item', 'Show_Item', 'Delete_Item', 'Delete_All', 'Find_Near', 'Find_Overlap', 'Line', 'Polyline', 'Circle', 'Rectangle', 'Oval', 'Polygon', 'Text', 'Image', 'Border', 'Compound', 'Label', 'Open', 'Frame', 'Canvas', 'Scroll']
    if not Name:
        return False
    if Name in Custom:
        return False
    if keyword.iskeyword(Name):
        return False
    if Name in dir(builtins):
        return False
    if Name.startswith('_') or Name.endswith('_'):
        return False
    if Name[0].isdigit():
        return False
    valid_pattern = re.compile(r'^[A-Za-z0-9_]+$')
    if not valid_pattern.match(Name):
        return False
    if '__' in Name:
        return False
    return True