from pwnagotchi.ui.components import LabeledValue
from pwnagotchi.ui.view import BLACK
from pwnagotchi.ui import fonts
from pwnagotchi import plugins
import logging
import datetime
import os
import toml
import yaml



# Changes
# make clock plugin disappear after deactivation
#
# TO DO
# Switch to one line display if GPS and memtemp are enabled.

class PwnClock(plugins.Plugin):
    __author__ = 'https://github.com/LoganMD'
    __version__ = '2.0.4.2'
    __license__ = 'GPL3'
    __description__ = 'Clock/Calendar for pwnagotchi'
    __defaults__ = {
        'enabled': False,
    }

    def on_loaded(self):
        if 'date_format' in self.options:
            self.date_format = self.options['date_format']
        else:
            self.date_format = "%y-%m-%d"

        if 'time_format' in self.options:
            self.time_format = self.options['time_format']
        else:
            self.time_format = "%I:%M %p"

        logging.info('[pwnclock] Plugin loaded.')

    def on_ui_setup(self, ui):
        gpsenable = False
        memenable = False
        config_is_toml = True if os.path.exists(
            '/etc/pwnagotchi/config.toml') else False
        config_path = '/etc/pwnagotchi/config.toml' if config_is_toml else '/etc/pwnagotchi/config.yml'
        with open(config_path) as f:
            data = toml.load(f) if config_is_toml else yaml.load(
                f, Loader=yaml.FullLoader)

            if 'memtemp' in data["main"]["plugins"]:
                if 'enabled' in data["main"]["plugins"]["memtemp"]:
                    if data["main"]["plugins"]["memtemp"]["enabled"]:
                        memenable = True
                        logging.info(
                            "[pwnclock] memtemp is enabled")
        if ui.is_waveshare_v2():
            pos = (130, 57) if memenable else (130, 57)
            ui.add_element('clock', LabeledValue(color=BLACK, label='', value='-/-/-\n-:--',
                                                 position=pos,
                                                 label_font=fonts.Small, text_font=fonts.Small))

    def on_unload(self, ui):
        with ui._lock:
            ui.remove_element('clock')

    def on_ui_update(self, ui):
        now = datetime.datetime.now()
        time_rn = now.strftime(self.date_format + " - " + self.time_format)
        ui.set('clock', time_rn)
