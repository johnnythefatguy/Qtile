#  $$$$$$\    $$\     $$\ $$\
# $$  __$$\   $$ |    \__|$$ |
# $$ /  $$ |$$$$$$\   $$\ $$ | $$$$$$\
# $$ |  $$ |\_$$  _|  $$ |$$ |$$  __$$\
# $$ |  $$ |  $$ |    $$ |$$ |$$$$$$$$ |
# $$ $$\$$ |  $$ |$$\ $$ |$$ |$$   ____|
# \$$$$$$ /   \$$$$  |$$ |$$ |\$$$$$$$\
#  \___$$$\    \____/ \__|\__| \_______|
#      \___|

###############
## JS Config ##
###############

from libqtile import bar, layout, widget, hook
from libqtile.config import Click, Drag, Group, Key, Match, Screen
from libqtile.lazy import lazy
import subprocess, os

mod = "mod4"
terminal = "terminator"
filemanager = "pcmanfm"
browser = "librewolf"
texteditor = "atom"
mediaplayer = "vlc"

keys = [
    Key([mod, "shift"], "left", lazy.layout.left(), desc="Move focus to left"),
    Key([mod, "shift"], "right", lazy.layout.right(), desc="Move focus to right"),
    Key([mod], "space", lazy.layout.next(), desc="Move window focus to other window"),
    Key([mod], "n", lazy.layout.normalize(), desc="Reset all window sizes"),
    # Personal Keybindings
    Key([mod, "shift"], "d", lazy.spawn("dmenu_run"), desc="Launch dmenu"),
    Key([mod, "shift"], "Return", lazy.spawn(filemanager), desc="Launch File Manager"),
    Key([mod], "b", lazy.spawn(browser), desc="Launch Browser"),
    Key([mod], "e", lazy.spawn(texteditor), desc="Launch Text Editor"),
    Key([mod], "m", lazy.spawn(mediaplayer), desc="Launch mediaplayer"),
    Key([mod, "shift"], "n", lazy.spawn("nitrogen"), desc="Launch Nitrogen"),
    Key([], "XF86MonBrightnessUp", lazy.spawn("xbacklight -inc 10")),
    Key([], "XF86MonBrightnessDown", lazy.spawn("xbacklight -dec 10")),
    # Toggle between split and unsplit sides of stack.
    # Split = all windows displayed
    # Unsplit = 1 window displayed, like Max layout, but still with
    # multiple stack panes
    Key([mod], "Return", lazy.spawn(terminal), desc="Launch terminal"),
    Key([mod], "Tab", lazy.next_layout(), desc="Toggle between layouts"),
    Key([mod, "shift"], "c", lazy.window.kill(), desc="Kill focused window"),
    Key([mod, "shift"], "r", lazy.reload_config(), desc="Reload the config"),
    Key([mod, "shift"], "q", lazy.shutdown(), desc="Shutdown Qtile"),
]

groups = [Group(i) for i in "123456789"]

for i in groups:
    keys.extend(
        [
            # mod1 + letter of group = switch to group
            Key(
                [mod],
                i.name,
                lazy.group[i.name].toscreen(),
                desc="Switch to group {}".format(i.name),
            ),
            # mod1 + shift + letter of group = switch to & move focused window to group
            Key(
                [mod, "shift"],
                i.name,
                lazy.window.togroup(i.name, switch_group=True),
                desc="Switch to & move focused window to group {}".format(i.name),
            ),
            # Or, use below if you prefer not to switch to that group.
            # # mod1 + shift + letter of group = move focused window to group
            # Key([mod, "shift"], i.name, lazy.window.togroup(i.name),
            #     desc="move focused window to group {}".format(i.name)),
        ]
    )

layouts = [
    layout.Columns(border_focus_stack=["#d75f5f", "#8f3d3d"], border_width=1, margin=15),
    layout.Max(border_width=1, margin=15),
    # Try more layouts by unleashing below layouts.
    # layout.Stack(num_stacks=2),
    # layout.Bsp(),
    # layout.Matrix(),
    # layout.MonadTall(),
    # layout.MonadWide(),
    # layout.RatioTile(),
    layout.Tile(border_width=1, margin=15),
    # layout.TreeTab(),
    # layout.VerticalTile(),
    # layout.Zoomy(),
]

widget_defaults = dict(
    font="monospace regular",
    fontsize=12,
    padding=3,
)
extension_defaults = widget_defaults.copy()

screens = [
    Screen(
        top=bar.Bar(
            [
                widget.GroupBox(),
                widget.Chord(
                    chords_colors={
                        "launch": ("#ff0000", "#ffffff"),
                    },
                    name_transform=lambda name: name.upper(),
                ),
                widget.TextBox("johnnytfg", name="Shitbox"),
                widget.Systray(),
                widget.Clock(format="%Y-%m-%d %a %I:%M %p"),
            ],
            25,
        ),
        bottom=bar.Bar(
            [
                widget.CurrentLayout(),
                widget.WindowName(),
                widget.QuickExit(),
            ],
            25,
        ),
    ),
]

# Drag floating layouts.
mouse = [
    Drag([mod], "Button1", lazy.window.set_position_floating(), start=lazy.window.get_position()),
    Drag([mod], "Button3", lazy.window.set_size_floating(), start=lazy.window.get_size()),
    Click([mod], "Button2", lazy.window.bring_to_front()),
]

dgroups_key_binder = None
dgroups_app_rules = []  # type: list
follow_mouse_focus = True
bring_front_click = False
cursor_warp = False
floating_layout = layout.Floating(
    float_rules=[
        # Run the utility of `xprop` to see the wm class and name of an X client.
        *layout.Floating.default_float_rules,
        Match(wm_class="confirmreset"),  # gitk
        Match(wm_class="makebranch"),  # gitk
        Match(wm_class="maketag"),  # gitk
        Match(wm_class="ssh-askpass"),  # ssh-askpass
        Match(title="branchdialog"),  # gitk
        Match(title="pinentry"),  # GPG key password entry
    ]
)
auto_fullscreen = True
focus_on_window_activation = "smart"
reconfigure_screens = True

# If things like steam games want to auto-minimize themselves when losing
# focus, should we respect this or not?
auto_minimize = True

# When using the Wayland backend, this can be used to configure input devices.
wl_input_rules = None

@hook.subscribe.startup_once
def autostart():
    start = os.path.expanduser("/home/johnnytfg/.config/autostart.sh")
    os.run(start)

wmname = "Shitbox"
