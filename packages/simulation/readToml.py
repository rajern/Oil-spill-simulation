import toml
import argparse
import os

def parse_input():
    parser = argparse.ArgumentParser(description = 'Simulation configuration')

    # Add command-line arguments
    parser.add_argument(
        '--find_all', action='store_true', help = 'Find all config files in the main program folder'
    )
    parser.add_argument(
        '-f', '--folder', help = 'Specify folder to search for config files', type=str   
    )
    parser.add_argument(
        '-c', '--config_file', help = 'Specify a single config file to read', type=str
    )
    args = parser.parse_args()

    find_all = args.find_all
    folder = args.folder
    config_file = args.config_file

    return find_all, folder, config_file

class ConfigReader:
    def __init__(self, file_path):
        self.file_path = file_path
        self.config = None

    def load_config_file(self):
        if not os.path.exists(self.file_path):
            raise FileNotFoundError(f'Config file {self.file_path} does not exist.')
        with open(self.file_path, 'r') as file: 
            self.config = toml.load(file)

        self.validate_config()

    def validate_config(self):
        '''
        Validate TOML file to fulfill all requirements. 
        '''
        required_sections = ['settings', 'geometry', 'IO']
        for section in required_sections:
            if section not in self.config: 
                raise ValueError(f'{self.config} is missing required section: {section}.')
            
        # Validate settings section
        settings = self.config['settings']
        if 'nSteps' not in settings:
            raise ValueError('nSteps is not provided.')
        if 'tStart' not in settings: 
            settings['tStart'] = 0
        if 'tEnd' not in settings: 
            raise ValueError('tEnd is not provided.')
        

        # Validate geometry section
        geometry = self.config['geometry']
        if 'meshName' not in geometry or 'borders' not in geometry: 
            raise ValueError('Missing keys in geometry section.')
        
        # Validate IO section
        IO = self.config['IO']
        if 'logName' not in IO:
            IO['logName'] = 'logfile'

        """restart_file = 'restartFile' in IO and IO['restartFile']
        start_time = 'tStart' in settings and settings['tStart'] > 0"""

        restart_file = IO.get('restartFile')
        start_time = settings.get('tStart', 0) > 0

        # Validate restartFile existence
        if restart_file and not os.path.exists(restart_file):
            settings['tStart'] = 0
            print('Continues with tStart = 0')
            # raise ValueError(f'Restart file {restart_file} does not exist.')

        if restart_file and not start_time:
            raise ValueError('If restart file is provided start time must also be.')
        if start_time and not restart_file: 
            raise ValueError('If start time is provided restart file must also be.')


        write_frequency = IO.get('writeFrequency', 0) # Sets writeFrequency to 0 if it is undefined
        if not isinstance(write_frequency, (int, float)) or write_frequency <= 0: 
            print('"writeFrequency" is not provided or is unvalid. No video will be recorded.')
        
    def get_value(self, section, key):
        return self.config[section].get(key) # config['settings'].get('nSteps') = 500 for example