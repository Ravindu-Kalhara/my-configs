import os
import subprocess
from libqtile import qtile
from libqtile import bar, layout, widget
from libqtile.config import Click, Drag, Group, Key, Match, Screen, ScratchPad, DropDown
from libqtile.lazy import lazy
from libqtile.utils import guess_terminal
from libqtile import hook

mod = "mod4"
# terminal = guess_terminal()
terminal = "st"

keys = [
    Key([mod], "h", lazy.layout.left(), desc="Move focus to left"),
    Key([mod], "l", lazy.layout.right(), desc="Move focus to right"),
    Key([mod], "j", lazy.layout.down(), desc="Move focus down"),
    Key([mod], "k", lazy.layout.up(), desc="Move focus up"),
    Key([mod], "space", lazy.layout.next(), desc="Move window focus to other window"),
    Key([mod, "shift"], "h", lazy.layout.shuffle_left(), desc="Move window to the left"),
    Key([mod, "shift"], "l", lazy.layout.shuffle_right(), desc="Move window to the right"),
    Key([mod, "shift"], "j", lazy.layout.shuffle_down(), desc="Move window down"),
    Key([mod, "shift"], "k", lazy.layout.shuffle_up(), desc="Move window up"),
    Key([mod, "control"], "h", lazy.layout.grow_left(), desc="Grow window to the left"),
    Key([mod, "control"], "l", lazy.layout.grow_right(), desc="Grow window to the right"),
    Key(
        [mod, "control"],
        "j",
        lazy.layout.grow_down(),
        lazy.layout.shrink(),
        desc="Grow window down (Columns and Monadtall)",
    ),
    Key(
        [mod, "control"], "k", lazy.layout.grow_up(), lazy.layout.grow(), desc="Grow window up (Columns and Monadtall)"
    ),
    Key([mod], "n", lazy.layout.normalize(), desc="Reset all window sizes"),
    Key(
        [mod, "control"],
        "Return",
        lazy.layout.toggle_split(),
        desc="Toggle between split and unsplit sides of stack",
    ),
    Key([mod, "shift"], "space", lazy.window.toggle_floating(), desc="Put the focused window to/from floating mode"),
    Key([mod], "F11", lazy.window.toggle_fullscreen(), desc="Put the focused window to/from fullscreen mode"),
    Key([mod], "Tab", lazy.next_layout(), desc="Toggle between layouts"),
    Key([mod, "shift"], "q", lazy.window.kill(), desc="Kill focused window"),
    Key([mod, "shift"], "r", lazy.reload_config(), desc="Reload the config"),
    Key([mod, "shift"], "e", lazy.shutdown(), desc="Shutdown Qtile"),
    # Multimedia controls
    Key([], "XF86AudioRaiseVolume", lazy.spawn("pactl set-sink-volume @DEFAULT_SINK@ +5%")),
    Key([], "XF86AudioLowerVolume", lazy.spawn("pactl set-sink-volume @DEFAULT_SINK@ -5%")),
    Key([], "XF86AudioMute", lazy.spawn("pactl set-sink-mute @DEFAULT_SINK@ toggle")),
    Key([], "XF86AudioPlay", lazy.spawn("playerctl play-pause")),
    Key([], "XF86AudioNext", lazy.spawn("playerctl next")),
    Key([], "XF86AudioPrev", lazy.spawn("playerctl previous")),
    Key([], "XF86AudioStop", lazy.spawn("playerctl stop")),
    # Launch aplications and scripts
    Key([mod], "Return", lazy.spawn(terminal), desc="Launch terminal"),
    Key([mod], "m", lazy.spawn("rofi-mount"), desc="Launch block devices mounter"),
    Key([mod, "shift"], "Return", lazy.spawn("rofi -show drun"), desc="Launch rofi"),
    Key(
        [mod],
        "y",
        lazy.spawn(
            "python /home/ravindu/Documents/Programming/Python/YouTube\ Video\ Downloader/YouTube\ Video\ Downloader\ V_01.1.py"
        ),
        desc="Launch Youtube Video Downloader",
    ),
]

# Dracula color palette
colors = [
    "#282a36",
    "#44475a",
    "#f8f8f2",
    "#6272a4",
    "#8be9fd",
    "#50fa7b",
    "#ffb86c",
    "#ff79c6",
    "#bd93f9",
    "#ff5555",
    "#f1fa8c",
]

group_names = "123456789"
group_label = [" ", " ", " ", " ", "GIMP", " ", " ", "8", "OBS"]
groups = []

for i in range(0, 9):
    groups.append(
        Group(
            name=group_names[i],
            label=group_label[i],
        )
    )

groups[1].matches = [Match(role="browser")]
groups[4].matches = [Match(wm_class="audacity")]
groups[5].matches = [Match(net_wm_pid=1050)]
groups[6].matches = [Match(net_wm_pid=3)]

for i in groups:
    keys.extend(
        [
            Key(
                [mod],
                i.name,
                lazy.group[i.name].toscreen(),
                desc="Switch to group {}".format(i.name),
            ),
            Key(
                [mod, "shift"],
                i.name,
                lazy.window.togroup(i.name, switch_group=False),
                desc="Switch to & move focused window to group {}".format(i.name),
            ),
        ]
    )

groups.extend(
    [
        ScratchPad(
            "scratchpad",
            [
                DropDown("file manager", f"{terminal} -e ranger", opacity=1, width=0.9, height=0.9, x=0.05, y=0.05),
                DropDown("resource monitor", f"{terminal} -e btop", opacity=1, width=0.9, height=0.9, x=0.05, y=0.05),
            ],
        )
    ]
)

keys.extend(
    [
        Key([mod], "f", lazy.group["scratchpad"].dropdown_toggle("file manager")),
        Key([mod], "r", lazy.group["scratchpad"].dropdown_toggle("resource monitor")),
    ]
)

layout_theme = {"border_width": 2, "margin": 3, "border_focus": colors[8], "border_normal": colors[0]}

layouts = [
    layout.MonadTall(**layout_theme),
    layout.Columns(**layout_theme),
    layout.Max(border_focus=colors[8], border_noarmal=colors[0], border_width=0),
    layout.TreeTab(
        active_bg=colors[3],
        bg_color=colors[1],
        font="Hasklug Nerd Font",
        fontsize=14,
        place_right=True,
        urgent_bg=colors[9],
        sections=["TreeTab"],
        section_fontsize=14,
    ),
    layout.Floating(border_focus=colors[8], border_normal=colors[0], border_width=2),
    # layout.Tile(shift_windows=True, **layout_theme),
    # layout.Stack(num_stacks=2),
    # layout.Bsp(),
    # layout.Matrix(),
    # layout.MonadWide(),
    # layout.RatioTile(),
    # layout.VerticalTile(),
    # layout.Zoomy(),
]

widget_defaults = dict(font="Hasklug Nerd Font", fontsize=14, padding=3)
extension_defaults = widget_defaults.copy()

screens = [
    Screen(
        top=bar.Bar(
            [
                widget.CurrentLayoutIcon(
                    background=colors[0], custom_icon_paths=[os.path.expanduser("~/.config/qtile/icons")]
                ),
                widget.GroupBox(
                    background=colors[0],
                    highlight_color=colors[8],
                    foreground=colors[2],
                    inactive="#515469",
                    highlight_method="line",
                    font="Hasklug Nerd Font",
                    padding=2
                    # hide_unused=True
                ),
                widget.Sep(
                    background=colors[0],
                    foreground=colors[8],
                ),
                widget.Spacer(background=colors[0]),
                widget.Sep(
                    background=colors[0],
                    foreground=colors[8],
                ),
                widget.Volume(
                    background=colors[0],
                    foreground=colors[4],
                    mute_command="pactl set-sink-mute @DEFAULT_SINK@ toggle",
                    volume_up_command="pactl set-sink-volume @DEFAULT_SINK@ +1%",
                    volume_down_command="pactl set-sink-volume @DEFAULT_SINK@ -1%",
                    font="Hasklug Nerd Font",
                    padding=6,
                    fmt="🔊 {}",
                    interval=0.1,
                ),
                widget.Sep(
                    background=colors[0],
                    foreground=colors[8],
                ),
                widget.Backlight(
                    backlight_name="intel_backlight",
                    background=colors[0],
                    foreground=colors[9],
                    padding=6,
                    font="Hasklug Nerd Font",
                    step=5,
                    fmt="  {}",
                    format="{percent:2.0%}",
                ),
                widget.Sep(
                    background=colors[0],
                    foreground=colors[8],
                ),
                widget.Battery(
                    background=colors[0],
                    foreground=colors[4],
                    charge_char=" ",
                    discharge_char=" ",
                    empty_char=" ",
                    full_char=" ",
                    unknown_char=" ",
                    format="{char} {percent:2.0%}",
                    show_short_text=False,
                    padding=8,
                    update_interval=1,
                ),
                widget.Sep(
                    background=colors[0],
                    foreground=colors[8],
                ),
                widget.CPUGraph(
                    background=colors[0],
                    border_color="#854d6f",
                    graph_color=colors[7],
                    fill_color="#ebb9d8",
                    line_width=3,
                    border_width=1,
                ),
                widget.MemoryGraph(
                    background=colors[0],
                    border_color="#8f673c",
                    graph_color=colors[6],
                    fill_color="#f1fa8c",
                    line_width=3,
                    border_width=1,
                ),
                widget.Sep(
                    background=colors[0],
                    foreground=colors[8],
                ),
                widget.Clock(format="%Y-%m-%d %a %I:%M %p", background=colors[0], foreground="#50fa7b", padding=4),
                widget.Sep(
                    background=colors[0],
                    foreground=colors[8],
                ),
                widget.Systray(background=colors[0]),
            ],
            24,
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
        *layout.Floating.default_float_rules,
        Match(title="Qalculate!"),
        Match(wm_class="confirmreset"),  # gitk
        Match(title="pinentry"),  # GPG key password entry
        Match(title="Chat"),
        Match(wm_class="cairo-dock"),
        Match(wm_class="Cairo-clock"),
    ],
    border_focus=colors[8],
    border_normal=colors[0],
    border_width=2,
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
def start_once():
    # autostarts
    home = os.path.expanduser("~")
    subprocess.call([home + "/.config/qtile/autostart.sh"])


# XXX: Gasp! We're lying here. In fact, nobody really uses or cares about this
# string besides java UI toolkits; you can see several discussions on the
# mailing lists, GitHub issues, and other WM documentation that suggest setting
# this string if your java app doesn't work correctly. We may as well just lie
# and say that we're a working one by default.
#
# We choose LG3D to maximize irony: it is a 3D non-reparenting WM written in
# java that happens to be on java's whitelist.
wmname = "LG3D"
