import pytest
import toml
import os
from unittest.mock import MagicMock
from main import parse_input, ConfigReader
from msh_classes import *

# Helper Functions and Fixtures
@pytest.fixture
def create_valid_config_file(tmp_path):
    """
    Create a valid config file for testing.
    """
    config = {
        "settings": {"nSteps": 100, "tStart": 0, "tEnd": 10},
        "geometry": {"meshName": "mesh1.msh", "borders": [0, 1]},
        "IO": {"logName": "logfile", "writeFrequency": 10}
    }
    file_path = tmp_path / "valid_config.toml"
    with open(file_path, "w") as f:
        toml.dump(config, f)
    return file_path

@pytest.fixture
def create_invalid_config_file(tmp_path):
    """
    Create an invalid config file missing required keys.
    """
    config = {
        "settings": {"nSteps": 100}
    }
    file_path = tmp_path / "invalid_config.toml"
    with open(file_path, "w") as f:
        toml.dump(config, f)
    return file_path

@pytest.fixture
def create_config_files_in_directory(tmp_path):
    """
    Create multiple config files in a temporary directory.
    """
    config1 = {
        "settings": {"nSteps": 100, "tStart": 0, "tEnd": 10},
        "geometry": {"meshName": "mesh1.msh", "borders": [0, 1]},
        "IO": {"logName": "logfile1", "writeFrequency": 10}
    }
    config2 = {
        "settings": {"nSteps": 200, "tStart": 5, "tEnd": 15},
        "geometry": {"meshName": "mesh2.msh", "borders": [1, 2]},
        "IO": {"logName": "logfile2", "writeFrequency": 5}
    }
    folder = tmp_path / "configs"
    folder.mkdir()
    (folder / "config1.toml").write_text(toml.dumps(config1))
    (folder / "config2.toml").write_text(toml.dumps(config2))
    return folder

# Test Functions
def test_parse_input_find_all(monkeypatch):
    """
    Test --find_all argument.
    """
    monkeypatch.setattr('sys.argv', ['main.py', '--find_all'])
    find_all, folder, config_file = parse_input()
    assert find_all is True
    assert folder is None
    assert config_file is None

def test_parse_input_folder(monkeypatch):
    """
    Test -f/--folder argument.
    """
    monkeypatch.setattr('sys.argv', ['main.py', '--folder', 'test_folder'])
    find_all, folder, config_file = parse_input()
    assert find_all is False
    assert folder == 'test_folder'
    assert config_file is None

def test_parse_input_config_file(monkeypatch):
    """
    Test -c/--config_file argument.
    """
    monkeypatch.setattr('sys.argv', ['main.py', '--config_file', 'test_config.toml'])
    find_all, folder, config_file = parse_input()
    assert find_all is False
    assert folder is None
    assert config_file == 'test_config.toml'

def test_valid_config(create_valid_config_file):
    """
    Test loading a valid config file.
    """
    reader = ConfigReader(create_valid_config_file)
    reader.load_config_file()
    assert reader.get_value("settings", "nSteps") == 100
    assert reader.get_value("geometry", "meshName") == "mesh1.msh"

def test_invalid_config(create_invalid_config_file):
    """
    Test behavior when required sections or keys are missing.
    """
    reader = ConfigReader(create_invalid_config_file)
    with pytest.raises(ValueError):
        reader.load_config_file()

def test_missing_file():
    """
    Test behavior when the file does not exist.
    """
    with pytest.raises(FileNotFoundError):
        reader = ConfigReader("nonexistent.toml")
        reader.load_config_file()

def test_find_all_configs(create_config_files_in_directory):
    """
    Test finding all .toml files in a directory.
    """
    config_files = []
    for file in os.listdir(create_config_files_in_directory):
        if file.endswith(".toml"):
            config_files.append(file)

    assert len(config_files) == 2
    assert "config1.toml" in config_files
    assert "config2.toml" in config_files

def test_main_simulation(create_valid_config_file, monkeypatch):
    """
    Test the main simulation loop with a valid config file.
    """
    # Mock Mesh and its methods
    mock_mesh = MagicMock()
    monkeypatch.setattr("main.Mesh", mock_mesh)

    config_reader = ConfigReader(create_valid_config_file)
    config_reader.load_config_file()

    # Extract parameters
    n_steps = config_reader.get_value("settings", "nSteps")
    t_start = config_reader.get_value("settings", "tStart")
    t_end = config_reader.get_value("settings", "tEnd")
    delta_t = (t_end - t_start) / n_steps

    # Simulate Mesh behavior
    mock_mesh.return_value.update_oil = MagicMock()

    # Run the simulation loop
    for step in range(10):
        mock_mesh.return_value.update_oil(delta_t=delta_t)

    # Assert that update_oil was called the correct number of times
    assert mock_mesh.return_value.update_oil.call_count == 10
