from libqtile.config import Key, Screen, Group, Click, Drag
from libqtile.command import lazy, Client
from libqtile import layout, bar, widget, hook
import Xlib.display

mod = "mod4"
alt = "mod1"

keys = [
    # Switch between windows in current stack pane
    Key(
        [mod], "k",
        lazy.layout.down()
    ),
    Key(
        [mod], "j",
        lazy.layout.up()
    ),
    Key(
        ["mod1"], "Tab",
        lazy.layout.down()
    ),

    # Move windows up or down in current stack
    Key(
        [mod, "control"], "k",
        lazy.layout.shuffle_down()
    ),
    Key(
        [mod, "control"], "j",
        lazy.layout.shuffle_up()
    ),

    # Switch window focus to other pane(s) of stack
    Key(
        [mod], "space",
        lazy.layout.next()
    ),

    # Swap panes of split stack
    Key(
        [mod, "shift"], "space",
        lazy.layout.rotate()
    ),

    # Toggle between split and unsplit sides of stack.
    # Split = all windows displayed
    # Unsplit = 1 window displayed, like Max layout, but still with multiple stack panes
    Key(
        [mod, "shift"], "Return",
        lazy.layout.toggle_split()
    ),
    Key([mod], "h",      lazy.to_screen(1)),
    Key([mod], "l",      lazy.to_screen(0)),
    Key(["mod1"], "Return", lazy.spawn("xterm")),
    Key(["mod4"],"Return", lazy.spawn("gnome-terminal")),

    # Toggle between different layouts as defined below
    Key([mod], "Tab",    lazy.nextlayout()),
    Key([mod], "w",      lazy.window.kill()),

    Key([mod, "control"], "r", lazy.restart()),
    Key([mod], "r", lazy.spawncmd()),
]

mouse = [
    Drag([alt], "Button1", lazy.window.set_position_floating(),
        start=lazy.window.get_position()),
    Drag([alt], "Button3", lazy.window.set_size_floating(),
        start=lazy.window.get_size()),
    Click([alt], "Button2", lazy.window.bring_to_front())
]

# groups = [
#     Group("INET"),
#     Group("console"),
#     Group("IDE"),
#     Group("FileBrowse"),
#     Group("messangers"),
#     Group("6"),
#     Group("7"),
#     #Group("a"),
#     #Group("s"),
#     #Group("d"),
#     #Group("f"),
#     #Group("u"),
#     #Group("i"),
#     #Group("o"),
#     #Group("p"),
# ]
# for index, item in enumerate(groups):
#     # mod1 + letter of group = switch to group
#     keys.append(
#         Key([mod], str(index+1), lazy.group[item.name].toscreen())
#     )

#     # mod1 + shift + letter of group = switch to & move focused window to group
#     keys.append(
#         Key([mod, "shift"], str(index+1), lazy.window.togroup(item.name))
#     )

group_names = [
    ("INET", {'layout': 'max'}),
    ("console", {'layout':'RatioTile'}),
    ("IDE", {'layout': 'max'}),
    ("FileBrowse", {'layout': 'max'}),
    ("messangers", {'layout': 'RatioTile'}),
    ("docs", {'layout': 'TreeTab'}),
    ("emule", {'layout': 'max'}),
    ("etc1", {'layout':'RatioTile'}),
]

groups = [Group(name, **kwargs) for name, kwargs in group_names]

for i, (name, kwargs) in enumerate(group_names, 1):
    keys.append(Key([mod], str(i), lazy.group[name].toscreen()))
    keys.append(Key([mod, "shift"], str(i), lazy.window.togroup(name)))


dgroups_key_binder = None
dgroups_app_rules = []

layouts = [
    layout.RatioTile(),
    layout.Max(),
    #layout.Stack(stacks=2),
    #layout.Tile(),
    #layout.Matrix(),
    #layout.Floating(),
    layout.MonadTall(),
    layout.Zoomy(),
    layout.TreeTab(),
]

# orange text on grey background
default_data = dict(fontsize=9,
                    foreground="FDFCED", #1D1D1D
                    background="2A4C4A", #FF6600
                    font="DejaVu Sans Mono")

screens = [
    Screen(
        top = bar.Bar(
            [
                widget.GroupBox(**default_data),
                widget.Prompt(**default_data),
    			widget.TextBox("Vol",**default_data),
    			widget.Volume(**default_data),
                widget.WindowName(**default_data),
                widget.TextBox("*", name="default",**default_data),
                widget.Systray(**default_data),
                widget.Clock('%y-%m-%d %a %I:%M %p',**default_data),
                ],
            20,     
            ),
    	bottom = bar.Bar(
    		[
    			widget.Battery(**default_data),
    			widget.TextBox("cpu",**default_data),
    			widget.CPUGraph(**default_data),
    			widget.TextBox("mem",**default_data),
    			widget.MemoryGraph(**default_data),
    			widget.TextBox("swap",**default_data),
    			widget.SwapGraph(**default_data),
    			widget.TextBox("Net",**default_data),
    			widget.NetGraph(**default_data),
    			widget.TextBox("hdd",**default_data),
    			widget.HDDGraph(**default_data),
    			widget.Canto(**default_data),
    			widget.CurrentLayout(**default_data),
    			#widget.WindowTabs(),
    			#widget.TaskList(),
                widget.RunScripts(**default_data),
    			#widget.Canto(feeds=["1","2",],**default_data),
    		    ],
    		40,			
    		),
        ),
        Screen(
        bottom=bar.Bar([
            widget.GroupBox(),
            widget.WindowName()
            ], 30),
        )
    ]

import subprocess, re
from os import system
from datetime import datetime

def is_running(process):
    s = subprocess.Popen(["ps", "axuw"], stdout=subprocess.PIPE)
    for x in s.stdout:
        if re.search(process, x):
            return True
    return False

def execute_once(process):
    if not is_running(process):
        return subprocess.Popen(process.split())

def qtile_history_put_event(event):
    try:
        event_time = datetime.now()
        system(
            "echo \"%s*%s\" >>~/.qtile_history" % (
                event_time.strftime(
                    "%Y-%m-%d*%H:%M:%S"
                    ),
                event)
            )
    except:
        print ("Error putting history event!")

@hook.subscribe.client_new
def dialogs(window):
    if(window.window.get_wm_type() == 'dialog'
        or window.window.get_wm_transient_for()):
        window.floating = True

@hook.subscribe.client_new
def swap_to_groups(
    window, 
    windows={
            'google-chrome':"INET",
            'gnome-terminal':"console",
            'sublime3':"IDE",
            'skype':"messangers",
            'libreoffice':"docs",
            'nemo':"FileBrowse",
        }
    ):

    windowtype = window.window.get_wm_class()[0]

    if windowtype in windows.keys():
        window.togroup(windows[windowtype])

client = Client()
def get_name_window(window):
    print window.name
    if window.name == None or window.name == '':
        display = Xlib.display.Display()
        window = display.get_input_focus().focus
        wmname = window.get_wm_name()
        wmclass = window.get_wm_class()
        if wmclass is None and wmname is None:
            window = window.query_tree().parent
            wmname = window.get_wm_name()
        return "%s" % ( wmname, )
    else:
        return window.name

@hook.subscribe.client_focus
def time_waste_manager(window):
    print (get_name_window(window))
    try:
        qtile_history_put_event("Switched to %s" % get_name_window(window))
    except:
        print "ERROR!"

main = None
follow_mouse_focus = False
cursor_warp = False
floating_layout = layout.Floating()
mouse = ()
auto_fullscreen = True
widget_defaults = {}

@hook.subscribe.startup
def startup():
    #execute_once("set_background.sh")
    #execute_once("google-chrome")
    #execute_once("skype")
    pass
