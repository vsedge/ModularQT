import PyInstaller.__main__
import sys
import os
from pathlib import Path

desktop_path = Path.home() / "Desktop"
spec_path = desktop_path / "ModularInstaller.spec"

if not spec_path.exists():
    print("Error: ModularInstaller.spec not found!")
    sys.exit(1)

print("Starting build process...")
PyInstaller.__main__.run([str(spec_path)])
print("Build complete! Check the Desktop/dist folder for your executable.")
