import pytest
import os
import toml
from readToml import ConfigReader

# Creates valid config file for testing
@pytest.fixture
def valid_config_file(tmp_path):
    config_data = {
        'settings': {
            'nSteps': 100,
            'tStart': 0,
            'tEnd': 100
        },
        'geometry': {
            'meshName': 'mesh1',
            'borders': 'borders1'
        },
        'IO': {
            'logName': 'logfile',
            'writeFrequency': 10
        }
    }
    file_path = tmp_path / "valid_config.toml"
    with open(file_path, 'w') as file:
        toml.dump(config_data, file)
    return file_path

# Creates invalid config file for testing
@pytest.fixture
def invalid_config_file(tmp_path):
    config_data = {
        'settings': {
            'nSteps': 100
        },
        'geometry': {
            'meshName': 'mesh1'
        }
    }
    file_path = tmp_path / "invalid_config.toml"
    with open(file_path, 'w') as file:
        toml.dump(config_data, file)
    return file_path

# Creates a config file with restartFile and tStart
@pytest.fixture
def config_with_restart_file(tmp_path):
    config_data = {
        'settings': {
            'nSteps': 100,
            'tStart': 10,
            'tEnd': 100
        },
        'geometry': {
            'meshName': 'mesh1',
            'borders': 'borders1'
        },
        'IO': {
            'logName': 'logfile',
            'writeFrequency': 10,
            'restartFile': 'restart.dat'
        }
    }
    file_path = tmp_path / "config_with_restart_file.toml"
    with open(file_path, 'w') as file:
        toml.dump(config_data, file)
    return file_path

# Creates config file with tStart, but without restartFile
@pytest.fixture
def config_without_restart_file(tmp_path):
    config_data = {
        'settings': {
            'nSteps': 100,
            'tStart': 10,
            'tEnd': 100
        },
        'geometry': {
            'meshName': 'mesh1',
            'borders': 'borders1'
        },
        'IO': {
            'logName': 'logfile',
            'writeFrequency': 10
        }
    }
    file_path = tmp_path / "config_without_restart_file.toml"
    with open(file_path, 'w') as file:
        toml.dump(config_data, file)
    return file_path

# Creates multiple config files
@pytest.fixture
def multiple_config_files(tmp_path):
    file_paths = []
    for i in range(3):
        config_data = {
            'settings': {
                'nSteps': 100 + i,
                'tStart': 0,
                'tEnd': 100 + i * 10
            },
            'geometry': {
                'meshName': f'mesh{i}',
                'borders': f'borders{i}'
            },
            'IO': {
                'logName': f'logfile{i}',
                'writeFrequency': 10 + i
            }
        }
        file_path = tmp_path / f"config_file_{i}.toml"
        with open(file_path, 'w') as file:
            toml.dump(config_data, file)
        file_paths.append(file_path)
    return file_paths

# Testing that valid config file loads correctly
def test_load_config_file(valid_config_file):
    reader = ConfigReader(valid_config_file)
    reader.load_config_file()
    assert reader.config is not None

# Testing that FileNotFoundError is raised for missing config file
def test_load_config_file_missing_file():
    reader = ConfigReader("non_existent.toml")
    with pytest.raises(FileNotFoundError):
        reader.load_config_file()

# Testing for validate_config method with a valid config file
def test_validate_config_valid_file(valid_config_file):
    reader = ConfigReader(valid_config_file)
    reader.load_config_file()
    reader.validate_config()

# Ensures validation fails for invalid config file
def test_validate_config_invalid_file(invalid_config_file):
    reader = ConfigReader(invalid_config_file)
    with pytest.raises(ValueError, match="missing required section"):
        reader.load_config_file()

# Tests get_value method with valid a valid key
def test_get_value(valid_config_file):
    reader = ConfigReader(valid_config_file)
    reader.load_config_file()
    n_steps = reader.get_value('settings', 'nSteps')
    assert n_steps == 100

# Tests get_value method with a missing key
def test_get_value_missing_key(valid_config_file):
    reader = ConfigReader(valid_config_file)
    reader.load_config_file()
    value = reader.get_value('settings', 'missingKey')
    assert value is None

# Checks that KeyError is raised for a missing section
def test_get_value_missing_section(valid_config_file):
    reader = ConfigReader(valid_config_file)
    reader.load_config_file()
    with pytest.raises(KeyError):
        reader.get_value('missingSection', 'nSteps')

# Test for loading and validating multiple config files
def test_load_multiple_config_files(multiple_config_files):
    for file_path in multiple_config_files:
        reader = ConfigReader(file_path)
        reader.load_config_file()
        assert reader.config is not None

# Validates with valid input of start time and restart file
def test_start_time_with_restart_file(config_with_restart_file):
    reader = ConfigReader(config_with_restart_file)
    reader.load_config_file()
    reader.validate_config()

# Checks that ValueError is raised when start time is provided and not restart file
def test_start_time_without_restart_file(config_without_restart_file):
    reader = ConfigReader(config_without_restart_file)
    with pytest.raises(ValueError, match='If start time is provided restart file must also be.'):
        reader.load_config_file()

# Checks that ValueError is raised when restart file is provided and not start time
def test_restart_file_without_start_time(valid_config_file):
    reader = ConfigReader(valid_config_file)
    reader.load_config_file()
    reader.config['IO']['restartFile'] = 'restart.dat'
    with pytest.raises(ValueError, match='If restart file is provided start time must also be.'):
        reader.validate_config()