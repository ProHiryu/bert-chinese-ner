"""
Validation tests to ensure the testing infrastructure is properly set up.
"""
import os
import sys
import importlib
import pytest
from pathlib import Path


class TestInfrastructureSetup:
    """Test class to validate the testing infrastructure."""
    
    def test_pytest_installed(self):
        """Verify pytest is available."""
        assert 'pytest' in sys.modules or importlib.util.find_spec('pytest') is not None
    
    def test_pytest_cov_installed(self):
        """Verify pytest-cov is available."""
        try:
            import pytest_cov
            assert True
        except ImportError:
            # Check if it's available as a plugin
            assert any('coverage' in str(p) for p in pytest.plugin.get_plugins())
    
    def test_pytest_mock_installed(self):
        """Verify pytest-mock is available."""
        try:
            import pytest_mock
            assert True
        except ImportError:
            # Check if the mocker fixture is available
            pass  # Will be verified in test_mocker_fixture
    
    def test_project_structure(self):
        """Verify the expected project structure exists."""
        project_root = Path(__file__).parent.parent
        
        # Check main directories
        assert (project_root / "tests").exists()
        assert (project_root / "tests" / "unit").exists()
        assert (project_root / "tests" / "integration").exists()
        
        # Check __init__.py files
        assert (project_root / "tests" / "__init__.py").exists()
        assert (project_root / "tests" / "unit" / "__init__.py").exists()
        assert (project_root / "tests" / "integration" / "__init__.py").exists()
        
        # Check conftest.py
        assert (project_root / "tests" / "conftest.py").exists()
        
        # Check pyproject.toml
        assert (project_root / "pyproject.toml").exists()
    
    def test_fixtures_available(self, temp_dir, mock_config):
        """Verify custom fixtures are available and working."""
        # Test temp_dir fixture
        assert temp_dir.exists()
        assert temp_dir.is_dir()
        
        # Test mock_config fixture
        assert isinstance(mock_config, dict)
        assert "data_dir" in mock_config
        assert "output_dir" in mock_config
    
    def test_mocker_fixture(self, mocker):
        """Verify the mocker fixture from pytest-mock is available."""
        # Create a simple mock
        mock_func = mocker.Mock(return_value=42)
        assert mock_func() == 42
        mock_func.assert_called_once()
    
    @pytest.mark.unit
    def test_unit_marker(self):
        """Verify unit test marker works."""
        assert True
    
    @pytest.mark.integration
    def test_integration_marker(self):
        """Verify integration test marker works."""
        assert True
    
    @pytest.mark.slow
    def test_slow_marker(self):
        """Verify slow test marker works."""
        assert True
    
    def test_coverage_configured(self):
        """Verify coverage is properly configured."""
        project_root = Path(__file__).parent.parent
        pyproject_path = project_root / "pyproject.toml"
        
        assert pyproject_path.exists()
        
        # Read pyproject.toml and check for coverage configuration
        content = pyproject_path.read_text()
        assert "[tool.coverage.run]" in content
        assert "[tool.coverage.report]" in content
        assert "[tool.pytest.ini_options]" in content
        assert "--cov" in content
    
    def test_gitignore_configured(self):
        """Verify .gitignore includes testing-related entries."""
        project_root = Path(__file__).parent.parent
        gitignore_path = project_root / ".gitignore"
        
        if gitignore_path.exists():
            content = gitignore_path.read_text()
            # Check for testing-related entries
            assert ".pytest_cache" in content
            assert ".coverage" in content
            assert "htmlcov" in content
            assert "coverage.xml" in content
            assert ".claude" in content
    
    def test_poetry_commands_configured(self):
        """Verify Poetry test commands are configured."""
        project_root = Path(__file__).parent.parent
        pyproject_path = project_root / "pyproject.toml"
        
        content = pyproject_path.read_text()
        assert '[tool.poetry.scripts]' in content
        assert 'test = "pytest:main"' in content
        assert 'tests = "pytest:main"' in content


class TestSampleFunctionality:
    """Sample tests to demonstrate the testing framework."""
    
    def test_simple_assertion(self):
        """A simple test to verify basic assertions work."""
        assert 1 + 1 == 2
    
    def test_with_fixture(self, temp_dir):
        """Test using a fixture."""
        test_file = temp_dir / "test.txt"
        test_file.write_text("Hello, World!")
        
        assert test_file.exists()
        assert test_file.read_text() == "Hello, World!"
    
    def test_with_parametrize(self):
        """Test using pytest parametrize."""
        @pytest.mark.parametrize("input,expected", [
            (1, 2),
            (2, 4),
            (3, 6),
        ])
        def inner_test(input, expected):
            assert input * 2 == expected
        
        # Run the parametrized test
        inner_test(1, 2)
        inner_test(2, 4)
        inner_test(3, 6)


if __name__ == "__main__":
    # Allow running this file directly for quick validation
    pytest.main([__file__, "-v"])