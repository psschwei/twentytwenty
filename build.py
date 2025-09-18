#!/usr/bin/env python3
"""
Main build orchestrator for twentytwenty
Builds packages for all supported platforms
"""
import argparse
import sys
import subprocess
from pathlib import Path
import platform

def run_script(script_path, description):
    """Run a build script and report results"""
    print(f"\n🔨 {description}")
    print("=" * 50)

    try:
        if script_path.suffix == ".py":
            result = subprocess.run([sys.executable, str(script_path)], check=True)
        elif script_path.suffix == ".sh":
            result = subprocess.run(["bash", str(script_path)], check=True)
        elif script_path.suffix == ".bat":
            result = subprocess.run([str(script_path)], shell=True, check=True)
        else:
            print(f"❌ Unknown script type: {script_path}")
            return False

        print(f"✅ {description} completed successfully!")
        return True

    except subprocess.CalledProcessError as e:
        print(f"❌ {description} failed with exit code {e.returncode}")
        return False
    except FileNotFoundError:
        print(f"❌ Script not found: {script_path}")
        return False

def main():
    parser = argparse.ArgumentParser(description="Build twentytwenty packages")
    parser.add_argument("--platform", choices=["linux", "windows", "macos", "all"],
                       default="all", help="Platform to build for")
    parser.add_argument("--format", choices=["rpm", "deb", "exe", "msi", "app", "dmg", "all"],
                       help="Specific format to build (platform-dependent)")
    parser.add_argument("--list", action="store_true", help="List available build targets")

    args = parser.parse_args()

    script_dir = Path(__file__).parent
    current_platform = platform.system().lower()

    # Build target definitions
    targets = {
        "linux": {
            "rpm": (script_dir / "build/linux/build-rpm.sh", "Building RPM package"),
            "deb": (script_dir / "build/linux/build-deb.sh", "Building DEB package"),
        },
        "windows": {
            "exe": (script_dir / "build/windows/build-windows.py", "Building Windows executable"),
            "msi": (script_dir / "build/windows/build-windows.py", "Building Windows MSI installer"),
        },
        "macos": {
            "app": (script_dir / "build/macos/build-macos.py", "Building macOS app bundle"),
            "dmg": (script_dir / "build/macos/build-macos.py", "Building macOS DMG installer"),
        }
    }

    if args.list:
        print("Available build targets:")
        for platform_name, formats in targets.items():
            print(f"\n{platform_name.upper()}:")
            for format_name, (script, desc) in formats.items():
                status = "✅" if script.exists() else "❌"
                print(f"  {status} {format_name}: {desc}")
        return

    print("🏗️  TwentyTwenty Build System")
    print("=" * 40)
    print(f"Current platform: {current_platform}")
    print(f"Target platform: {args.platform}")

    # Determine what to build
    builds_to_run = []

    if args.platform == "all":
        # Build for all platforms
        for platform_name, formats in targets.items():
            for format_name, (script, desc) in formats.items():
                if script.exists():
                    builds_to_run.append((script, desc))
    else:
        # Build for specific platform
        platform_targets = targets.get(args.platform, {})
        if not platform_targets:
            print(f"❌ Unknown platform: {args.platform}")
            return 1

        if args.format and args.format != "all":
            # Specific format
            if args.format in platform_targets:
                script, desc = platform_targets[args.format]
                if script.exists():
                    builds_to_run.append((script, desc))
                else:
                    print(f"❌ Build script not found: {script}")
                    return 1
            else:
                print(f"❌ Format '{args.format}' not available for platform '{args.platform}'")
                return 1
        else:
            # All formats for the platform
            for format_name, (script, desc) in platform_targets.items():
                if script.exists():
                    builds_to_run.append((script, desc))

    if not builds_to_run:
        print("❌ No build targets found!")
        return 1

    # Warning for cross-platform builds
    if args.platform != "all" and args.platform != current_platform:
        print(f"⚠️  Warning: Building {args.platform} packages on {current_platform}")
        print("   Some features may not work correctly.")

    # Run builds
    successful = 0
    failed = 0

    for script, description in builds_to_run:
        if run_script(script, description):
            successful += 1
        else:
            failed += 1

    # Summary
    print("\n" + "=" * 50)
    print("📊 Build Summary")
    print(f"✅ Successful: {successful}")
    print(f"❌ Failed: {failed}")

    if failed == 0:
        print("🎉 All builds completed successfully!")
        print(f"📦 Check the dist/ directory for your packages")
        return 0
    else:
        print("⚠️  Some builds failed. Check the output above for details.")
        return 1

if __name__ == "__main__":
    sys.exit(main())