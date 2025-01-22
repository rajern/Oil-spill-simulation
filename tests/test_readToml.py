import pytest
import toml
from packages.simulation.readToml import ConfigReader

# Creates valid config file for testing
@pytest.fixture
def valid_config_file(tmp_path):
    """
    Fixture to create a valid configuration file for testing.
    The file includes all necessary sections and keys.
    Returns the path to the created file.
    """
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
    """
    Fixture to create an invalid configuration file for testing.
    The file is missing required sections or keys.
    Returns the path to the created file.
    """
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
    """
    Fixture to create a configuration file that includes both
    'restartFile' and 'tStart' for testing specific validation cases.
    Returns the path to the created file.
    """
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
    """
    Fixture to create a configuration file that includes 'tStart'
    but does not include 'restartFile', to test validation failures.
    Returns the path to the created file.
    """
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
    """
    Fixture to create multiple configuration files with slight variations
    for testing scenarios involving multiple files.
    Returns a list of file paths.
    """
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
    """
    Test that the configuration file loads correctly when it is valid.
    """
    reader = ConfigReader(valid_config_file)
    reader.load_config_file()
    assert reader.config is not None

# Testing that FileNotFoundError is raised for missing config file
def test_load_config_file_missing_file():
    """
    Test that a FileNotFoundError is raised when attempting to load
    a non-existent config file.
    """
    reader = ConfigReader("non_existent.toml")
    with pytest.raises(FileNotFoundError):
        reader.load_config_file()

# Testing for validate_config method with a valid config file
def test_validate_config_valid_file(valid_config_file):
    """
    Test that the validate_config method works correctly for a valid config file.
    """
    reader = ConfigReader(valid_config_file)
    reader.load_config_file()
    reader.validate_config()

# Ensures validation fails for invalid config file
def test_validate_config_invalid_file(invalid_config_file):
    """
    Test that the validate_config method raises a ValueError
    when the config file is missing required sections or keys.
    """
    reader = ConfigReader(invalid_config_file)
    with pytest.raises(ValueError, match="missing required section"):
        reader.load_config_file()

# Tests get_value method with a valid key
def test_get_value(valid_config_file):
    """
    Test that the get_value method correctly retrieves a value for a valid key.
    """
    reader = ConfigReader(valid_config_file)
    reader.load_config_file()
    n_steps = reader.get_value('settings', 'nSteps')
    assert n_steps == 100

# Tests get_value method with a missing key
def test_get_value_missing_key(valid_config_file):
    """
    Test that the get_value method returns None when the key is missing.
    """
    reader = ConfigReader(valid_config_file)
    reader.load_config_file()
    value = reader.get_value('settings', 'missingKey')
    assert value is None

# Checks that KeyError is raised for a missing section
def test_get_value_missing_section(valid_config_file):
    """
    Test that the get_value method raises a KeyError when the section is missing.
    """
    reader = ConfigReader(valid_config_file)
    reader.load_config_file()
    with pytest.raises(KeyError):
        reader.get_value('missingSection', 'nSteps')

# Test for loading and validating multiple config files
def test_load_multiple_config_files(multiple_config_files):
    """
    Test that multiple config files can be loaded and validated correctly.
    """
    for file_path in multiple_config_files:
        reader = ConfigReader(file_path)
        reader.load_config_file()
        assert reader.config is not None

# Validates that ValueError is raised when tStart is provided but restartFile is missing
def test_start_time_without_restart_file(config_without_restart_file):
    """
    Test that a ValueError is raised when tStart is provided but restartFile is not included.
    """
    reader = ConfigReader(config_without_restart_file)
    with pytest.raises(ValueError, match='If start time is provided restart file must also be.'):
        reader.load_config_file()

# Validates that ValueError is raised when restartFile is provided but tStart is missing
def test_restart_file_without_start_time(config_with_restart_file, tmp_path):
    """
    Test that a ValueError is raised when a restartFile is provided but tStart is not specified.
    """
    # Modify the provided config file to remove tStart
    config_data = {
        'settings': {
            'nSteps': 100,
            'tEnd': 100  # tStart intentionally removed
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
    file_path = tmp_path / "invalid_restart_file.toml"
    with open(file_path, 'w') as file:
        toml.dump(config_data, file)

    reader = ConfigReader(file_path)
    with pytest.raises(ValueError, match='If restart file is provided start time must also be.'):
        reader.load_config_file()