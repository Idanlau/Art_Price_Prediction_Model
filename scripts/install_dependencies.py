import sys
import subprocess


requirements = open("../requirements.txt", "r").read().split("\n")
packages = [package.split("==")[0] for package in requirements if len(package) > 0]
for package in packages:
    subprocess.check_call([sys.executable, "-m", "pip", "install", package])
