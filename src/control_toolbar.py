#! /usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright (C) 2011~2013 Deepin, Inc.
#               2011~2013 Kaisheng Ye
#
# Author:     Kaisheng Ye <kaisheng.ye@gmail.com>
# Maintainer: Kaisheng Ye <kaisheng.ye@gmail.com>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import gtk
from dtk.ui.statusbar import Statusbar
from dtk.ui.threads import post_gui
from dtk.ui.box import Markbox
from star_view import StarView
from dtk.ui.utils import get_event_coords

from theme import app_theme
from button import Button, ToggleButton
from events import global_event
from cookie_parser import get_cookie_star, set_cookie_star
from download_manager import SetStarScore
from nls import _
import utils

STAR_SIZE = utils.get_common_image_pixbuf('star/star_on.png').get_width()

class ControlToolbar(Statusbar):
    def __init__(self, appid, has_star_view=True):
        Statusbar.__init__(self, 39, )

        self.appid = appid
        status_box = gtk.HBox()

        self.mute_button = ToggleButton(
                app_theme.get_pixbuf('mute/sound_normal.png'),
                app_theme.get_pixbuf('mute/mute_normal.png'),
                app_theme.get_pixbuf('mute/sound_hover.png'),
                app_theme.get_pixbuf('mute/mute_hover.png'),
                app_theme.get_pixbuf('mute/sound_press.png'),
                app_theme.get_pixbuf('mute/mute_press.png'),
                active_button_label = _('Volume'),
                inactive_button_label = _('Mute'),
                draw_background=True,
                padding_edge=10,
                padding_middle=6)
        #self.mute_button.connect('clicked', self.mute_handler)
        mute_button_align = gtk.Alignment()
        mute_button_align.set(0, 0.5, 0, 0)
        mute_button_align.set_padding(3, 6, 3, 3)
        mute_button_align.add(self.mute_button)

        self.favorite_button = ToggleButton(
                app_theme.get_pixbuf('favorite/unfavorite_normal.png'),
                app_theme.get_pixbuf('favorite/favorite_normal.png'),
                app_theme.get_pixbuf('favorite/unfavorite_hover.png'),
                app_theme.get_pixbuf('favorite/favorite_hover.png'),
                app_theme.get_pixbuf('favorite/unfavorite_press.png'),
                app_theme.get_pixbuf('favorite/favorite_press.png'),
                active_button_label = _('Favorite'),
                draw_background=True,
                padding_edge=10,
                padding_middle=6)
        #self.favorite_button.connect('clicked', self.toggle_favorite)
        favorite_button_align = gtk.Alignment()
        favorite_button_align.set(0, 0.5, 0, 0)
        favorite_button_align.set_padding(3, 6, 3, 3)
        favorite_button_align.add(self.favorite_button)

        self.replay_button = Button(
                app_theme.get_pixbuf('replay/replay_normal.png'),
                app_theme.get_pixbuf('replay/replay_hover.png'),
                app_theme.get_pixbuf('replay/replay_press.png'),
                button_label = _('Replay'),
                draw_background=True,
                padding_edge=10,
                padding_middle=6)
        #self.replay_button.connect('clicked', self.replay_action)
        replay_button_align = gtk.Alignment()
        replay_button_align.set(0, 0.5, 0, 0)
        replay_button_align.set_padding(3, 6, 3, 3)
        replay_button_align.add(self.replay_button)

        self.hand_pause = False
        self.game_pause = False
        self.pause_button = ToggleButton(
                app_theme.get_pixbuf('pause/pause_normal.png'),
                app_theme.get_pixbuf('pause/play_normal.png'),
                app_theme.get_pixbuf('pause/pause_hover.png'),
                app_theme.get_pixbuf('pause/play_hover.png'),
                app_theme.get_pixbuf('pause/pause_press.png'),
                app_theme.get_pixbuf('pause/play_press.png'),
                active_button_label = _('Pause'),
                inactive_button_label = _('Continue'),
                draw_background=True,
                padding_edge=10,
                padding_middle=6)
        #self.pause_button.connect('button-press-event', self.pause_handler)
        pause_button_align = gtk.Alignment()
        pause_button_align.set(0, 0.5, 0, 0)
        pause_button_align.set_padding(3, 6, 10, 3)
        pause_button_align.add(self.pause_button)

        self.fullscreen_button = Button(
                app_theme.get_pixbuf('fullscreen/fullscreen_normal.png'),
                app_theme.get_pixbuf('fullscreen/fullscreen_hover.png'),
                app_theme.get_pixbuf('fullscreen/fullscreen_press.png'),
                button_label = _('Fullscreen'),
                draw_background=True,
                padding_edge=10,
                padding_middle=6)
        #self.fullscreen_button.connect('clicked', self.fullscreen_action)
        fullscreen_button_align = gtk.Alignment()
        fullscreen_button_align.set(0, 0.5, 0, 0)
        fullscreen_button_align.set_padding(3, 6, 3, 3)
        fullscreen_button_align.add(self.fullscreen_button)

        self.share_button = Button(
                app_theme.get_pixbuf('share/share_normal.png'),
                app_theme.get_pixbuf('share/share_hover.png'),
                app_theme.get_pixbuf('share/share_press.png'),
                button_label = _('Share'),
                draw_background=True,
                padding_edge=10,
                padding_middle=6)
        #self.share_button.connect('clicked', self.share_action)
        share_button_align = gtk.Alignment()
        share_button_align.set(0, 0.5, 0, 0)
        share_button_align.set_padding(3, 6, 3, 3)
        share_button_align.add(self.share_button)

        star_box = gtk.HBox()
        self.star = StarView()
        self.star.set_star_level(9)
        star_align = gtk.Alignment(0.5, 0.5, 0, 0)
        star_align.set_padding(2, 2, 3, 0)
        star_align.add(self.star)

        self.star_mark = Markbox(5.0, '#ffffff')
        star_mark_align = gtk.Alignment(0.5, 0, 0, 0)
        star_mark_align.set_padding(2, 4, 3, 20)
        star_mark_align.add(self.star_mark)
        
        star_box.pack_start(star_align)
        star_box.pack_start(star_mark_align)
        star_box_align = gtk.Alignment(1, 0.5, 0, 0)
        star_box_align.set_padding(0, 0, 3, 0)
        star_box_align.add(star_box)

        status_box.pack_start(pause_button_align, False, False)
        #status_box.pack_start(mute_button_align, False, False)
        status_box.pack_start(replay_button_align, False, False)
        status_box.pack_start(favorite_button_align, False, False)
        status_box.pack_start(fullscreen_button_align, False, False)
        status_box.pack_start(share_button_align, False, False)
        if has_star_view:
            status_box.pack_start(star_box_align)

        self.status_box.pack_start(status_box, True, True)

        self.leave_callback = None
        #self.connect('motion-notify-event', self.leave_event_handler)

        global_event.register_event('download-app-info-finish', self.update_star)
        global_event.register_event('set-star-score-success', self.score_success_handler)
        self.star.connect("button-press-event", self.star_press)

        self.cookie = get_cookie_star(self.appid)
        if self.cookie:
            self.star.set_read_only(True)

    def star_press(self, widget, event):
        (event_x, event_y) = get_event_coords(event)
        star = int(min(event_x / (STAR_SIZE / 2) + 1, 10))

        if self.star.read_only:
            self.star.progressbar_tip.show_image_text(_('You score today already'), 'star/star_finish.png')
            self.star.show_progressbar_tip(event)
        else:
            self.star.progressbar_tip.show_image_text(_('Ratings success'), 'star/star_success.png')
            self.star.show_progressbar_tip(event)
            if getattr(self, 'appid'):
                SetStarScore(self.appid, star).start()
                set_cookie_star(self.appid, int(star/2))

    def score_success_handler(self, js):
        score = float(js['score'])
        self.star.set_star_level(score)
        self.star_mark.set_value(score)
        self.star.set_read_only(True)

    @post_gui
    def update_star(self, js):
        star = js['star']
        self.star.set_star_level(float(star))
        self.star_mark.set_value(float(star))
