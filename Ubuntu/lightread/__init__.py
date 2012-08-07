# -*- Mode: Python; coding: utf-8; indent-tabs-mode: nil; tab-width: 4 -*-
### BEGIN LICENSE
# Copyright (C) 2012 Caffeinated Code <caffeinatedco.de>
# Copyright (C) 2012 George Czabania
# Copyright (C) 2012 Jono Cooper
# Copyright (c) The Regents of the University of California.
# All rights reserved.
# 
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions
# are met:
# 1. Redistributions of source code must retain the above copyright
#    notice, this list of conditions and the following disclaimer.
# 2. Redistributions in binary form must reproduce the above copyright
#    notice, this list of conditions and the following disclaimer in the
#    documentation and/or other materials provided with the distribution.
# 3. Neither the name of the University nor the names of its contributors
#    may be used to endorse or promote products derived from this software
#    without specific prior written permission.
# 
# THIS SOFTWARE IS PROVIDED BY THE REGENTS AND CONTRIBUTORS ``AS IS'' AND
# ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED.  IN NO EVENT SHALL THE REGENTS OR CONTRIBUTORS BE LIABLE
# OR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
# DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS
# OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION)
# HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT
# LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY
# OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF
# SUCH DAMAGE.
### END LICENSE

import optparse

import gettext
from gettext import gettext as _
gettext.textdomain('lightread')

from gi.repository import Gtk, Gio # pylint: disable=E0611

from lightread import LightreadWindow

from lightread_lib import set_up_logging, get_version

def parse_options():
    """Support for command line options"""
    parser = optparse.OptionParser(version="%%prog %s" % get_version())
    parser.add_option(
        "-v", "--verbose", action="count", dest="verbose",
        help=_("Show debug messages (-vv debugs lightread_lib also)"))
    (options, args) = parser.parse_args()

    set_up_logging(options)

class LightreadApp(Gtk.Application):
    def __init__(self):
        Gtk.Application.__init__(self, application_id="net.launchpad.lightread",
                                 flags=Gio.ApplicationFlags.FLAGS_NONE)
        self.connect("activate", self.on_activate)

    def on_activate(self, data=None):
        self.window = LightreadWindow.LightreadWindow(self)
        self.window.show_all()
    
    def do_startup (self):
        Gtk.Application.do_startup(self)
        
        menu = Gio.Menu()
        menu.append("Preferences", "app.prefs")
        menu.append("Help", "app.help")
        menu.append("About Lightread", "app.about")
        menu.append("Quit", "app.quit")
        self.set_app_menu(menu)

        prefs_action = Gio.SimpleAction.new("prefs", None)
        prefs_action.connect("activate", self.prefs_cb)
        self.add_action(prefs_action)

        help_action = Gio.SimpleAction.new("help", None)
        help_action.connect("activate", self.help_cb)
        self.add_action(help_action)

        about_action = Gio.SimpleAction.new("about", None)
        about_action.connect("activate", self.about_cb)
        self.add_action(about_action)

        quit_action = Gio.SimpleAction.new("quit", None)
        quit_action.connect("activate", self.quit_cb)
        self.add_action(quit_action)

    def prefs_cb(self, action, parameter):
        self.window.logout.activate()

    def help_cb(self, action, parameter):
        self.window.on_mnu_contents_activate(None)

    def about_cb(self, action, parameter):
        self.window.on_mnu_about_activate(None)

    def quit_cb(self, action, parameter):
        self.window.on_mnu_close_activate(None)

def main():
    'constructor for your class instances'
    parse_options()

    # Run the application.    
    app = LightreadApp()
    app.run(None)
