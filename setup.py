from cx_Freeze import *
import sys
includefiles=['new.png','open.png','save.png','save_as.png','exit.png','print.png','pdf.png','bold.png'
             ,'italic.png','underline.png','font_color.png',
              'left.png','right.png','center.png','speak.png',
               'cut.png','copy.png','paste.png','clear_all.png','selectall.png',
              'undo.png','light_default.png','dark.png','night_blue.png','red.png','orange.png',
              'help.png','find.png','checked.png','dateandtime.png','icon_3.ico']
base=None
if sys.platform=="win32":
    base="Win32GUI"

shortcut_table=[
    ("DesktopShortcut",
     "DesktopFolder",
     "Text Editor",
     "TARGETDIR",
     "[TARGETDIR]\texteditor.exe",
     None,
     None,
     None,
     None,
     None,
     None,
     "TARGETDIR",
     )
]
msi_data={"Shortcut":shortcut_table}

bdist_msi_options={'data':msi_data}
setup(
    version="0.1",
    description="Text editor",
    author="Prathmesh",
    name="Text editor",
    options={'build_exe':{'include_files':includefiles},'bdist_msi':bdist_msi_options,},
    executables=[
        Executable(
            script="main.py",
            base=base,
            icon='icon_3.ico',
        )
    ]
)
