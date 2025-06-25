"""
Shared pytest fixtures and configuration for all tests.
"""
import os
import tempfile
import shutil
from pathlib import Path
from typing import Generator, Dict, Any
import pytest


@pytest.fixture
def temp_dir() -> Generator[Path, None, None]:
    """
    Create a temporary directory for test files.
    
    Yields:
        Path: Path object pointing to the temporary directory
    """
    temp_path = tempfile.mkdtemp()
    yield Path(temp_path)
    shutil.rmtree(temp_path)


@pytest.fixture
def mock_config() -> Dict[str, Any]:
    """
    Provide a mock configuration dictionary for testing.
    
    Returns:
        Dict[str, Any]: Mock configuration with common settings
    """
    return {
        "data_dir": "/tmp/test_data",
        "output_dir": "/tmp/test_output",
        "bert_config_file": "/tmp/bert_config.json",
        "init_checkpoint": "/tmp/bert_model.ckpt",
        "vocab_file": "/tmp/vocab.txt",
        "max_seq_length": 128,
        "train_batch_size": 32,
        "learning_rate": 5e-5,
        "num_train_epochs": 3.0,
        "warmup_proportion": 0.1,
    }


@pytest.fixture
def sample_data_file(temp_dir: Path) -> Path:
    """
    Create a sample data file for testing.
    
    Args:
        temp_dir: Temporary directory fixture
        
    Returns:
        Path: Path to the created sample data file
    """
    data_file = temp_dir / "sample_data.txt"
    sample_content = """O O O O O O O B-PER I-PER O O B-LOC O O O O O O O
O O B-MISC I-MISC O O O O O O B-ORG I-ORG I-ORG O O O O O
"""
    data_file.write_text(sample_content)
    return data_file


@pytest.fixture
def mock_vocab_file(temp_dir: Path) -> Path:
    """
    Create a mock vocabulary file for testing.
    
    Args:
        temp_dir: Temporary directory fixture
        
    Returns:
        Path: Path to the created vocabulary file
    """
    vocab_file = temp_dir / "vocab.txt"
    vocab_content = """[PAD]
[UNK]
[CLS]
[SEP]
[MASK]
the
of
and
to
a
in
that
"""
    vocab_file.write_text(vocab_content)
    return vocab_file


@pytest.fixture(autouse=True)
def reset_tensorflow_graph():
    """
    Reset TensorFlow graph before each test to ensure clean state.
    """
    try:
        import tensorflow as tf
        if hasattr(tf, 'reset_default_graph'):
            tf.reset_default_graph()
        elif hasattr(tf, 'compat') and hasattr(tf.compat.v1, 'reset_default_graph'):
            tf.compat.v1.reset_default_graph()
    except ImportError:
        pass
    yield


@pytest.fixture
def mock_environment_variables(monkeypatch):
    """
    Set up mock environment variables for testing.
    
    Args:
        monkeypatch: pytest monkeypatch fixture
    """
    test_env_vars = {
        "CUDA_VISIBLE_DEVICES": "-1",  # Force CPU for tests
        "TF_CPP_MIN_LOG_LEVEL": "3",   # Suppress TF warnings
    }
    
    for key, value in test_env_vars.items():
        monkeypatch.setenv(key, value)
    
    yield
    
    # Cleanup happens automatically with monkeypatch


@pytest.fixture
def capture_stdout(monkeypatch):
    """
    Capture stdout for testing print statements.
    """
    import io
    import sys
    
    captured_output = io.StringIO()
    monkeypatch.setattr(sys, 'stdout', captured_output)
    
    yield captured_output
    
    # Cleanup happens automatically with monkeypatch


# Pytest configuration hooks
def pytest_configure(config):
    """
    Configure pytest with custom settings.
    """
    config.addinivalue_line(
        "markers", "gpu: tests that require GPU (deselect with '-m \"not gpu\"')"
    )
    config.addinivalue_line(
        "markers", "slow: slow running tests (deselect with '-m \"not slow\"')"
    )
    

def pytest_collection_modifyitems(config, items):
    """
    Modify test collection to add markers based on test location.
    """
    for item in items:
        # Add unit/integration markers based on test location
        if "unit" in str(item.fspath):
            item.add_marker(pytest.mark.unit)
        elif "integration" in str(item.fspath):
            item.add_marker(pytest.mark.integration)