# memtemp shows memory infos and cpu temperature
#
# mem usage, cpu load, cpu temp
#
###############################################################
#
# Changelog 
#
# 2021-02-04 by mkoterski/koteshi <koteshi@gmail.com>
# - WIP reduce the display height for 2.13 waveshare display
#
# 2019-10-20 by spees <speeskonijn@gmail.com>
# - Refactored to use the already existing functions
# - Now only shows memory usage in percentage
# - Added CPU load
# - Added horizontal and vertical orientation
#
# 2019-10-18 by spees <speeskonijn@gmail.com>
# - Changed the place where the data was displayed on screen
# - Made the data a bit more compact and easier to read
# - removed the label so we wont waste screen space
# - Updated version to 1.0.1
#
###############################################################
from pwnagotchi.ui.components import LabeledValue
from pwnagotchi.ui.view import BLACK
import pwnagotchi.ui.fonts as fonts
import pwnagotchi.plugins as plugins
import pwnagotchi
import logging


class MemTemp(plugins.Plugin):
    __author__ = 'https://github.com/xenDE'
    __version__ = '1.0.3.1'
    __license__ = 'GPL3'
    __description__ = 'A plugin that will display memory/cpu usage and temperature'

    def on_loaded(self):
        logging.info("memtemp-niu plugin loaded.")

    def mem_usage(self):
        return int(pwnagotchi.mem_usage() * 100)

    def cpu_load(self):
        return int(pwnagotchi.cpu_load() * 100)

    def on_ui_setup(self, ui):
        if ui.is_waveshare_v2():
            h_pos = (180, 80)
            v_pos = (180, 61)
            # modular element positions added below
            v_pos_mem = (185, 80)
            v_pos_cpu = (185, 89)
            v_pos_temp = (180, 99)

            # below values are not tested/adjusted for horizontal view yet
            h_pos_mem = (180, 80)
            h_pos_cpu = (180, 80)
            h_pos_temp = (180, 80)

        elif ui.is_waveshare_v1():
            h_pos = (170, 80)
            v_pos = (170, 61)
        elif ui.is_waveshare144lcd():
            h_pos = (53, 77)
            v_pos = (78, 67)
        elif ui.is_inky():
            h_pos = (140, 68)
            v_pos = (165, 54)
        elif ui.is_waveshare27inch():
            h_pos = (192, 138)
            v_pos = (216, 122)
        else:
            h_pos = (155, 76)
            v_pos = (180, 61)

        #removed label spacing   
        label_spacing = 0


        if self.options['orientation'] == "vertical":
            # ui.add_element('memtemp', LabeledValue(color=BLACK, label='', value=' mem:-\n cpu:-\ntemp:-',
            #                                        position=v_pos,
            #                                        label_font=fonts.Small, text_font=fonts.Small))

            ui.add_element(
                "mem",
                LabeledValue(
                    color=BLACK,
                    label="mem:",
                    value=" ",
                    position=v_pos_mem,
                    label_font=fonts.Small,
                    text_font=fonts.Small,
                    label_spacing=label_spacing,
                ),
            )
            ui.add_element(
                "cpu",
                LabeledValue(
                    color=BLACK,
                    label="cpu:",
                    value="",
                    position=v_pos_cpu,
                    label_font=fonts.Small,
                    text_font=fonts.Small,
                    label_spacing=label_spacing,
                ),
            )
            ui.add_element(
                "temp",
                LabeledValue(
                    color=BLACK,
                    label="temp:",
                    value="",
                    position=v_pos_temp,
                    label_font=fonts.Small,
                    text_font=fonts.Small,
                    label_spacing=label_spacing,
                ),
            )

        else:
            # default to horizontal
            ui.add_element('memtemp', LabeledValue(color=BLACK, label='', value='mem cpu temp\n - -  -',
                                                   position=h_pos,
                                                   label_font=fonts.Small, text_font=fonts.Small))

# Add modular ui elements for horizontal orientation.


# Updated unload function for modular element positioning
    def on_unload(self, ui):
        with ui._lock:
            ui.remove_element('mem')
            ui.remove_element('cpu')
            ui.remove_element('temp')

    def on_ui_update(self, ui):
        if self.options['scale'] == "fahrenheit":
            temp = (pwnagotchi.temperature() * 9 / 5) + 32
            symbol = "f"
        elif self.options['scale'] == "kelvin":
            temp = pwnagotchi.temperature() + 273.15
            symbol = "k"
        else:
            # default to celsius
            temp = pwnagotchi.temperature()
            symbol = "c"

        if self.options['orientation'] == "vertical":
            # ui.set('memtemp',
            #        " mem:%s%%\n cpu:%s%%\ntemp:%s%s" % (self.mem_usage(), self.cpu_load(), temp, symbol))
        
        # Updated modular element positioning

            ui.set("mem", f" {self.mem_usage()} ")
            ui.set("cpu", f" {self.cpu_load()} ")
            ui.set("temp", f" {self.cpu_load()} ")
        

        else:
            # default to horizontal
            ui.set('memtemp',
                   " mem cpu temp\n %s%% %s%%  %s%s" % (self.mem_usage(), self.cpu_load(), temp, symbol))
