"""
Script tự động cài đặt dependencies và chạy analysis
"""
import subprocess
import sys
import os

def install_requirements():
    """Cài đặt các package cần thiết"""
    try:
        import matplotlib
        import seaborn
        import pandas
        import numpy
        print("All required packages are already installed.")
        return True
    except ImportError:
        print("Installing required packages...")
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
            return True
        except subprocess.CalledProcessError:
            print("Failed to install packages. Please install manually:")
            print("pip install matplotlib seaborn pandas numpy")
            return False

def main():
    """Main function"""
    print("Material Tier Distribution Analyzer")
    print("====================================")
    
    if not install_requirements():
        return
    
    # Import after ensuring packages are installed
    from tier_distribution_analyzer import main as run_analysis
    
    print("\nRunning tier distribution analysis...")
    run_analysis()

if __name__ == "__main__":
    main()
