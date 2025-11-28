"""Architecture enforcement tests.

These tests ensure the clean separation between core game logic and
platform-specific code. The core package should have NO dependencies on:
- File I/O (pathlib.Path operations, open(), etc.)
- Platform-specific libraries (textual, sounddevice, vosk, etc.)
- Storage implementations
"""

import ast
import importlib
from pathlib import Path

# Imports that are forbidden in core/
FORBIDDEN_IN_CORE = {
    # Platform-specific UI
    "textual",
    # Platform-specific audio
    "sounddevice",
    "vosk",
    # Storage implementations (core should use protocol only)
    "flashy.storage.file_storage",
    "flashy.history",
    # File I/O modules that indicate direct I/O
    # (Note: pathlib itself is OK for type hints, but Path operations are not)
}

# These core modules should be completely pure
CORE_MODULES = [
    "flashy.core.levels",
    "flashy.core.models",
    "flashy.core.number_parser",
    "flashy.core.problems",
    "flashy.core.scoring",
    "flashy.core.worlds",
]


def get_imports_from_file(file_path: Path) -> set[str]:
    """Extract all import statements from a Python file."""
    with open(file_path) as f:
        tree = ast.parse(f.read())

    imports = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                imports.add(alias.name.split(".")[0])
                imports.add(alias.name)
        elif isinstance(node, ast.ImportFrom):
            if node.module:
                imports.add(node.module.split(".")[0])
                imports.add(node.module)

    return imports


class TestCoreModulePurity:
    """Tests that core modules have no forbidden dependencies."""

    def test_core_modules_have_no_forbidden_imports(self) -> None:
        """Core modules should not import platform-specific code."""
        core_dir = Path(__file__).parent.parent / "flashy" / "core"

        violations = []
        for py_file in core_dir.glob("*.py"):
            if py_file.name == "__init__.py":
                continue

            imports = get_imports_from_file(py_file)
            for forbidden in FORBIDDEN_IN_CORE:
                if forbidden in imports:
                    violations.append(f"{py_file.name} imports {forbidden}")

        assert not violations, "Forbidden imports in core:\n" + "\n".join(violations)

    def test_core_modules_are_importable(self) -> None:
        """All core modules should be importable without side effects."""
        for module_name in CORE_MODULES:
            module = importlib.import_module(module_name)
            assert module is not None

    def test_core_does_not_import_storage_implementation(self) -> None:
        """Core should not import storage implementation, only protocol."""
        core_dir = Path(__file__).parent.parent / "flashy" / "core"

        for py_file in core_dir.glob("*.py"):
            imports = get_imports_from_file(py_file)
            assert "flashy.storage.file_storage" not in imports, (
                f"{py_file.name} imports file_storage directly"
            )
            assert "flashy.history" not in imports, (
                f"{py_file.name} imports history module"
            )


class TestStorageAbstraction:
    """Tests for proper storage abstraction."""

    def test_storage_protocol_exists(self) -> None:
        """StorageBackend protocol should be defined."""
        from flashy.storage.protocol import StorageBackend

        # Check it has the required methods
        assert hasattr(StorageBackend, "load_progress")
        assert hasattr(StorageBackend, "save_progress")
        assert hasattr(StorageBackend, "log_session")
        assert hasattr(StorageBackend, "list_players")
        assert hasattr(StorageBackend, "player_exists")

    def test_file_storage_implements_protocol(self) -> None:
        """FileStorage should implement StorageBackend protocol."""
        # Create an instance to verify it works
        import tempfile

        from flashy.storage import FileStorage

        with tempfile.TemporaryDirectory() as tmpdir:
            storage = FileStorage(base_dir=Path(tmpdir))

            # Test basic operations
            players = storage.list_players()
            assert isinstance(players, list)

            assert not storage.player_exists("nonexistent")


class TestGameControllerDependencyInjection:
    """Tests for GameController dependency injection."""

    def test_controller_accepts_storage(self) -> None:
        """GameController should accept a storage backend."""
        from unittest.mock import MagicMock

        from flashy.game import GameController

        mock_storage = MagicMock()
        controller = GameController("test", 1, storage=mock_storage)

        assert controller._storage is mock_storage

    def test_controller_uses_default_storage_when_none(self) -> None:
        """GameController should use default storage when none provided."""
        from flashy.game import GameController
        from flashy.storage import FileStorage

        controller = GameController("test", 1)

        # Access the storage property to trigger lazy loading
        storage = controller.storage

        assert isinstance(storage, FileStorage)
