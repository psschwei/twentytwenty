#!/usr/bin/env python3
"""
Build script for creating standalone binaries of the twentytwenty application.
"""

import sys
import os
import shutil
import subprocess
import argparse
from pathlib import Path
import tempfile


def run_command(cmd, cwd=None):
    """Run a command and return success status"""
    print(f"Running: {' '.join(cmd)}")
    try:
        result = subprocess.run(cmd, cwd=cwd, check=True, capture_output=True, text=True)
        print(f"✓ Success: {' '.join(cmd)}")
        return True
    except subprocess.CalledProcessError as e:
        print(f"✗ Failed: {' '.join(cmd)}")
        print(f"Error: {e.stderr}")
        return False


def build_binary(onefile=True, console=False):
    """Build binary using PyInstaller"""

    # Clean previous builds
    dist_dir = Path("dist")
    build_dir = Path("build")
    if dist_dir.exists():
        shutil.rmtree(dist_dir)
    if build_dir.exists():
        shutil.rmtree(build_dir)

    # PyInstaller command
    cmd = [
        "uv", "run", "pyinstaller",
        "--name", "twentytwenty",
        "--clean",
    ]

    if onefile:
        cmd.append("--onefile")

    if not console:
        cmd.append("--windowed")  # No console window

    # Add the main script
    cmd.append("twentytwenty.py")

    print("Building binary with PyInstaller...")
    success = run_command(cmd)

    if success:
        if onefile:
            binary_path = dist_dir / "twentytwenty"
            if sys.platform == "win32":
                binary_path = binary_path.with_suffix(".exe")
        else:
            binary_path = dist_dir / "twentytwenty"

        if binary_path.exists():
            print(f"✓ Binary built successfully: {binary_path}")

            # Make executable on Unix systems
            if sys.platform != "win32":
                os.chmod(binary_path, 0o755)

            return binary_path
        else:
            print("✗ Binary not found after build")
            return None
    else:
        return None


def create_simple_icon():
    """Create a simple eye icon using PyQt5"""
    try:
        # Set up minimal QApplication for headless operation
        from PyQt5.QtWidgets import QApplication
        from PyQt5.QtGui import QPixmap, QPainter, QColor, QFont
        from PyQt5.QtCore import Qt

        # Create minimal QApplication if none exists
        app = QApplication.instance()
        if app is None:
            app = QApplication([])
            app.setQuitOnLastWindowClosed(False)

        # Create a 64x64 icon
        pixmap = QPixmap(64, 64)
        pixmap.fill(QColor(255, 255, 255, 0))  # Transparent background

        painter = QPainter(pixmap)
        painter.setRenderHint(QPainter.Antialiasing)

        # Draw a simple eye shape
        painter.setPen(QColor(0, 0, 0))
        painter.setBrush(QColor(100, 150, 255))

        # Eye outline (ellipse)
        painter.drawEllipse(8, 24, 48, 16)

        # Pupil
        painter.setBrush(QColor(0, 0, 0))
        painter.drawEllipse(28, 28, 8, 8)

        # Add "20" text
        painter.setFont(QFont('Arial', 12, QFont.Bold))
        painter.setPen(QColor(0, 0, 0))
        painter.drawText(16, 52, "20")

        painter.end()

        # Save as PNG
        icon_path = Path("twentytwenty.png")
        pixmap.save(str(icon_path), "PNG")
        return icon_path

    except Exception as e:
        print(f"Warning: Could not create icon: {e}")
        return None


def create_desktop_file(binary_path, icon_path=None):
    """Create a .desktop file for Linux desktop integration"""
    if sys.platform != "linux":
        return None

    desktop_content = f"""[Desktop Entry]
Name=Twenty Twenty
Comment=20-20-20 Eye Break Timer
Exec={binary_path.absolute()}
Icon={icon_path.absolute() if icon_path else 'applications-utilities'}
Type=Application
Categories=Utility;Health;
StartupNotify=true
Terminal=false
Keywords=eye;break;timer;health;strain;
"""

    desktop_file = Path("twentytwenty.desktop")
    with open(desktop_file, 'w') as f:
        f.write(desktop_content)

    # Make executable
    os.chmod(desktop_file, 0o755)

    print(f"✓ Desktop file created: {desktop_file}")
    return desktop_file


def install_desktop_application(binary_path, desktop_file, icon_path=None):
    """Install the application to the system (optional)"""
    if sys.platform != "linux":
        return False

    home = Path.home()

    # Install locations
    local_bin = home / ".local" / "bin"
    local_applications = home / ".local" / "share" / "applications"
    local_icons = home / ".local" / "share" / "icons"

    try:
        # Create directories if they don't exist
        local_bin.mkdir(parents=True, exist_ok=True)
        local_applications.mkdir(parents=True, exist_ok=True)
        if icon_path:
            local_icons.mkdir(parents=True, exist_ok=True)

        # Copy binary
        installed_binary = local_bin / "twentytwenty"
        shutil.copy2(binary_path, installed_binary)
        os.chmod(installed_binary, 0o755)

        # Copy desktop file (update Exec path)
        desktop_content = desktop_file.read_text()
        desktop_content = desktop_content.replace(str(binary_path.absolute()), str(installed_binary))

        if icon_path:
            installed_icon = local_icons / icon_path.name
            shutil.copy2(icon_path, installed_icon)
            desktop_content = desktop_content.replace(str(icon_path.absolute()), str(installed_icon))

        installed_desktop = local_applications / desktop_file.name
        installed_desktop.write_text(desktop_content)
        os.chmod(installed_desktop, 0o755)

        # Update desktop database
        run_command(["update-desktop-database", str(local_applications)])

        print(f"✓ Application installed to:")
        print(f"  Binary: {installed_binary}")
        print(f"  Desktop: {installed_desktop}")
        if icon_path:
            print(f"  Icon: {installed_icon}")

        return True

    except Exception as e:
        print(f"✗ Installation failed: {e}")
        return False


def main():
    parser = argparse.ArgumentParser(description="Build twentytwenty binary")
    parser.add_argument("--dir", action="store_true",
                       help="Create directory distribution instead of single file")
    parser.add_argument("--console", action="store_true",
                       help="Show console window (useful for debugging)")
    parser.add_argument("--install", action="store_true",
                       help="Install as desktop application (Linux only)")

    args = parser.parse_args()

    print("=" * 50)
    print("Building twentytwenty binary")
    print("=" * 50)

    # Build binary
    binary_path = build_binary(
        onefile=not args.dir,
        console=args.console
    )

    if binary_path:
        print(f"\n✓ Build complete!")
        print(f"Binary location: {binary_path}")
        print(f"File size: {binary_path.stat().st_size / 1024 / 1024:.1f} MB")

        # Test the binary
        print("\nTesting binary (--help)...")
        test_cmd = [str(binary_path), "--help"]
        if run_command(test_cmd):
            print("✓ Binary test successful!")
        else:
            print("✗ Binary test failed")

        # Create desktop integration (Linux only)
        if sys.platform == "linux":
            print("\nCreating desktop integration...")

            # Create icon
            icon_path = create_simple_icon()
            if icon_path:
                print(f"✓ Icon created: {icon_path}")

            # Create desktop file
            desktop_file = create_desktop_file(binary_path, icon_path)

            if desktop_file:
                print(f"✓ Desktop file created: {desktop_file}")

                # Install if requested
                if args.install:
                    print("\nInstalling desktop application...")
                    if install_desktop_application(binary_path, desktop_file, icon_path):
                        print("✓ Desktop application installed!")
                        print("You can now find 'Twenty Twenty' in your applications menu.")
                    else:
                        print("✗ Desktop application installation failed")
                else:
                    print("\nTo install as desktop application, run:")
                    print("  python build.py --install")
                    print(f"Or manually copy files:")
                    print(f"  cp {binary_path} ~/.local/bin/")
                    print(f"  cp {desktop_file} ~/.local/share/applications/")
                    if icon_path:
                        print(f"  cp {icon_path} ~/.local/share/icons/")

    else:
        print("\n✗ Build failed!")
        sys.exit(1)


if __name__ == "__main__":
    main()