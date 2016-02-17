from .core.utils import (
    check_input,
    is_positive,
    is_one_to_eight
)

class SRSettings(object):
    """ SR Settings """
    def __init__(self, **args):
        self._settings = {
            'energy_min': check_input(float, is_positive, args.get('energy_min', 1.0E3)),
            'output_type': check_input(int, is_one_to_eight, args.get('output_type', 1)),
            'output_filename': args.get('output_filename', 'SR_OUTPUT.txt'),
            'correction': check_input(float, is_positive, args.get('correction', 1.0))
        }

    def __getattr__(self, attr):
        return self._settings[attr]
    

class SR(object):
    """ Automate SR Calculations """
    def __init__(self, layer, ion, **args):
        self.settings = SRSettings(**args)
        self.layer = layer
        self.ion = ion

    def  _write_input_file(self):
        """ Write necissary SR input file for calculation """
        SRInput(self).write()

    def run(self, srim_directory=SRIM_DIRECTORY):
        current_directory = os.getcwd()
        os.chdir(os.pach.join(srim_directory, 'SR Module'))
        self._write_input_file()
        # Make sure compatible with Windows, OSX, and Linux
        subprocess.check_call([str(os.path.join('.', 'SRModule.exe'))])
        os.chdir(current_directory)
