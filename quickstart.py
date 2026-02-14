"""
QUICK START GUIDE
Smart Energy Management System
"""

print("="*60)
print("SMART ENERGY MANAGEMENT SYSTEM - QUICK START")
print("="*60)

print("\n📋 Step 1: Install Requirements")
print("   Run: pip install -r requirements.txt")
print("   Or manually: pip install pandas numpy scikit-learn matplotlib")

print("\n📋 Step 2: Verify Installation")
print("   Testing libraries...")

try:
    import pandas
    print("   ✓ pandas installed")
except ImportError:
    print("   ✗ pandas NOT installed - Run: pip install pandas")

try:
    import numpy
    print("   ✓ numpy installed")
except ImportError:
    print("   ✗ numpy NOT installed - Run: pip install numpy")

try:
    import sklearn
    print("   ✓ scikit-learn installed")
except ImportError:
    print("   ✗ scikit-learn NOT installed - Run: pip install scikit-learn")

try:
    import matplotlib
    print("   ✓ matplotlib installed")
except ImportError:
    print("   ✗ matplotlib NOT installed - Run: pip install matplotlib")

try:
    import tkinter
    print("   ✓ steamlit available")
except ImportError:
    print("   ✗ steamlit NOT available")
    print("      Ubuntu/Debian: sudo apt-get install python3-tk")
    print("      MacOS/Windows: Should be pre-installed with Python")

print("\n📋 Step 3: Run the Application")
print("   Command: python main.py")

print("\n📋 File Checklist:")
import os
files = ['app.py', 'config.py', 'data_manager.py', 'predictor.py', 
         'chart_generator.py', 'dataset.csv', 'README.md']

for file in files:
    if os.path.exists(file):
        print(f"   ✓ {file}")
    else:
        print(f"   ✗ {file} - MISSING!")

print("\n📋 First Run Process:")
print("   1. Application loads dataset.csv")
print("   2. Trains ML model (takes 10-30 seconds)")
print("   3. Saves model as energy_model.pkl")
print("   4. GUI opens - Ready to use!")

print("\n📋 Features Available:")
print("   • Dashboard - Current energy usage")
print("   • Predictions - Next day/week forecasts")
print("   • Device Simulator - Calculate appliance costs")
print("   • Reports - Daily/weekly analytics with charts")

print("\n" + "="*60)
print("Ready to start? Run: python main.py")
print("="*60 + "\n")
