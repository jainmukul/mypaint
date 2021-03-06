# This file is part of MyPaint.
# Copyright (C) 2011-2015 by Andrew Chadwick <a.t.chadwick@gmail.com>
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.

"""The application toolbar, and its specialised widgets"""


## Imports

import os

import gtk2compat
import gtk
from gtk import gdk
import gobject
from gettext import gettext as _
import pango

import widgets
from lib.helpers import escape


## Module constants


FRAMEWORK_XML = 'gui/toolbar.xml'
MERGEABLE_XML = [
    ("toolbar1_file", 'gui/toolbar-file.xml', _("File handling")),
    ("toolbar1_scrap", 'gui/toolbar-scrap.xml', _("Scraps switcher")),
    ("toolbar1_edit", 'gui/toolbar-edit.xml', _("Undo and Redo")),
    ("toolbar1_blendmodes", 'gui/toolbar-blendmodes.xml', _("Blend Modes")),
    ("toolbar1_linemodes", 'gui/toolbar-linemodes.xml', _("Line Modes")),
    ("toolbar1_view_modes", 'gui/toolbar-view-modes.xml', _("View (Main)")),
    ("toolbar1_view_manips", 'gui/toolbar-view-manips.xml', _("View (Alternative/Secondary)")),
    ("toolbar1_view_resets", 'gui/toolbar-view-resets.xml', _("View (Resetting)")),
    ]


## Class definitions

class ToolbarManager (object):
    """Manager for toolbars, currently just the main one.

    The main toolbar, /toolbar1, contains a menu button and quick
    access to the painting tools.
    """

    def __init__(self, draw_window):
        super(ToolbarManager, self).__init__()
        self.draw_window = draw_window
        self.app = draw_window.app
        self.toolbar1_ui_loaded = {}  # {name: merge_id, ...}
        self.init_actions()
        toolbarpath = os.path.join(self.app.datapath, FRAMEWORK_XML)
        self.app.ui_manager.add_ui_from_file(toolbarpath)
        self.toolbar1 = self.app.ui_manager.get_widget('/toolbar1')
        self.toolbar1.set_style(gtk.TOOLBAR_ICONS)
        self.toolbar1.set_icon_size(_get_icon_size())
        self.toolbar1.set_border_width(0)
        self.toolbar1.set_show_arrow(True)
        self.toolbar1.connect(
            "popup-context-menu",
            self.on_toolbar1_popup_context_menu
        )
        self.toolbar1_popup = self.app.ui_manager\
            .get_widget('/toolbar1-settings-menu')
        for item in self.toolbar1:
            if isinstance(item, gtk.SeparatorToolItem):
                item.set_draw(False)
        self.toolbar2 = self.app.ui_manager.get_widget('/toolbar2')
        self.toolbar2.set_style(gtk.TOOLBAR_ICONS)
        self.toolbar2.set_icon_size(_get_icon_size())
        self.toolbar2.set_border_width(0)
        self.toolbar2.set_show_arrow(False)
        for toolbar in (self.toolbar1, self.toolbar2):
            styles = toolbar.get_style_context()
            styles.add_class(gtk.STYLE_CLASS_PRIMARY_TOOLBAR)

        # Merge in UI pieces based on the user's saved preferences
        for action in self.settings_actions:
            name = action.get_property("name")
            active = self.app.preferences["ui.toolbar_items"].get(name, False)
            action.set_active(active)
            action.toggled()

    def init_actions(self):
        ag = self.draw_window.action_group
        actions = []

        self.settings_actions = []
        for name, ui_xml, label in MERGEABLE_XML:
            action = gtk.ToggleAction(name, label, None, None)
            action.connect("toggled", self.on_settings_toggle, ui_xml)
            self.settings_actions.append(action)
        actions += self.settings_actions

        for action in actions:
            ag.add_action(action)

    def on_toolbar1_popup_context_menu(self, toolbar, x, y, button):
        menu = self.toolbar1_popup

        def _posfunc(*a):
            return x, y, True
        time = gtk.get_current_event_time()
        # GTK3: arguments have a different order, and "data" is required.
        # GTK3: Use keyword arguments for max compatibility.
        menu.popup(parent_menu_shell=None, parent_menu_item=None,
                   func=_posfunc, button=button, activate_time=time,
                   data=None)

    def on_settings_toggle(self, toggleaction, ui_xml_file):
        name = toggleaction.get_property("name")
        merge_id = self.toolbar1_ui_loaded.get(name, None)
        if toggleaction.get_active():
            self.app.preferences["ui.toolbar_items"][name] = True
            if merge_id is not None:
                return
            ui_xml_path = os.path.join(self.app.datapath, ui_xml_file)
            merge_id = self.app.ui_manager.add_ui_from_file(ui_xml_path)
            self.toolbar1_ui_loaded[name] = merge_id
        else:
            self.app.preferences["ui.toolbar_items"][name] = False
            if merge_id is None:
                return
            self.app.ui_manager.remove_ui(merge_id)
            self.toolbar1_ui_loaded.pop(name)


def _get_icon_size():
    from application import get_app
    app = get_app()
    size = str(app.preferences.get("ui.toolbar_icon_size", "large")).lower()
    if size == 'small':
        return widgets.ICON_SIZE_SMALL
    else:
        return widgets.ICON_SIZE_LARGE


class MainMenuButton (gtk.ToggleButton):
    """Launches the popup menu when clicked.

    This sits inside the main toolbar when the main menu bar is hidden. In
    addition to providing access to the app's menu associated with the main
    view, this is a little more compliant with Fitts's Law than a normal
    `gtk.MenuBar`: our local style modifications mean that for most styles,
    when the window is fullscreened with only the "toolbar" present the
    ``(0,0)`` screen pixel hits this button.

    Support note: Compiz edge bindings sometimes get in the way of this, so
    turn those off if you want Fitts's compliance.
    """

    def __init__(self, text, menu):
        gtk.Button.__init__(self)
        self.menu = menu
        hbox1 = gtk.HBox()
        hbox2 = gtk.HBox()
        label = gtk.Label()
        hbox1.pack_start(label, True, True)
        arrow = gtk.Arrow(gtk.ARROW_DOWN, gtk.SHADOW_IN)
        hbox1.pack_start(arrow, False, False)
        hbox2.pack_start(hbox1, True, True, widgets.SPACING_TIGHT)

        # Text settings
        text = unicode(text)
        markup = "<b>%s</b>" % escape(text)
        label.set_markup(markup)

        self.add(hbox2)
        self.set_relief(gtk.RELIEF_NONE)
        self.connect("button-press-event", self.on_button_press)

        # No keynav.
        #DISABLED: self.connect("toggled", self.on_toggled)
        self.set_can_focus(False)
        self.set_can_default(False)

        for sig in "selection-done", "deactivate", "cancel":
            menu.connect(sig, self.on_menu_dismiss)

    def on_enter(self, widget, event):
        # Not this set_state(). That one.
        #self.set_state(gtk.STATE_PRELIGHT)
        gtk.Widget.set_state(self, gtk.STATE_PRELIGHT)

    def on_leave(self, widget, event):
        #self.set_state(gtk.STATE_NORMAL)
        gtk.Widget.set_state(self, gtk.STATE_NORMAL)

    def on_button_press(self, widget, event):
        # Post the menu. Menu operation is much more convincing if we call
        # popup() with event details here rather than leaving it to the toggled
        # handler.
        self._show_menu(event)
        self.set_active(True)
        return True

    ## Key nav only. We don't support it right now, so don't compile.
    #def on_toggled(self, togglebutton):
    #    # Post the menu from a keypress. Dismiss handler untoggles it.
    #    if togglebutton.get_active():
    #        if not self.menu.get_property("visible"):
    #            self._show_menu()

    def _show_menu(self, event=None):
        button = 1
        time = 0
        if event is not None:
            button = event.button
            time = event.time
        pos_func = self._get_popup_menu_position
        # GTK3: arguments have a different order, and "data" is required.
        # GTK3: Use keyword arguments for max compatibility.
        self.menu.popup(parent_menu_shell=None, parent_menu_item=None,
                        func=pos_func, button=button,
                        activate_time=time, data=None)

    def on_menu_dismiss(self, *a, **kw):
        # Reset the button state when the user's finished, and
        # park focus back on the menu button.
        self.set_state(gtk.STATE_NORMAL)
        self.set_active(False)
        self.grab_focus()

    def _get_popup_menu_position(self, menu, *junk):
        # Underneath the button, at the same x position.
        x, y = self.get_window().get_origin()
        y += self.get_allocation().height
        return x, y, True
