import pytest
import toml
from readToml import ConfigReader

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

def test_load_config_file(valid_config_file):
    reader = ConfigReader(valid_config_file)
    reader.load_config_file()
    assert reader.config is not None

def test_load_config_file_missing_file():
    reader = ConfigReader("non_existent.toml")
    with pytest.raises(FileNotFoundError):
        reader.load_config_file()

def test_validate_config_valid_file(valid_config_file):
    reader = ConfigReader(valid_config_file)
    reader.load_config_file()
    reader.validate_config()  # Should not raise any exceptions

def test_validate_config_invalid_file(invalid_config_file):
    reader = ConfigReader(invalid_config_file)
    reader.load_config_file()
    with pytest.raises(ValueError):
        reader.validate_config()

def test_get_value(valid_config_file):
    reader = ConfigReader(valid_config_file)
    reader.load_config_file()
    n_steps = reader.get_value('settings', 'nSteps')
    assert n_steps == 100

def test_get_value_missing_key(valid_config_file):
    reader = ConfigReader(valid_config_file)
    reader.load_config_file()
    value = reader.get_value('settings', 'missingKey')
    assert value is None

def test_get_value_missing_section(valid_config_file):
    reader = ConfigReader(valid_config_file)
    reader.load_config_file()
    with pytest.raises(KeyError):
        reader.get_value('missingSection', 'nSteps')
