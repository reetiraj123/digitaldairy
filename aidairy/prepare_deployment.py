"""
Script to prepare all files for deployment
Creates a deployment package with all necessary files
"""

import os
import shutil
from pathlib import Path

print("Preparing SmartDairy for deployment...\n")

# Files to include
files_to_include = [
    'app.py',
    'requirements.txt',
    'README.md',
    'Procfile',
    'setup.sh',
    '.gitignore',
    'presentation.pptx'
]

# Folders to include
folders_to_include = [
    'utils',
    'templates',
    'assets',
    '.streamlit'
]

# Create deployment folder
deploy_folder = 'DEPLOY_THIS'
if os.path.exists(deploy_folder):
    shutil.rmtree(deploy_folder)
os.makedirs(deploy_folder)

print("📦 Copying files...")

# Copy files
for file in files_to_include:
    if os.path.exists(file):
        shutil.copy2(file, deploy_folder)
        print(f"  [OK] {file}")
    else:
        print(f"  [WARN] {file} not found")

# Copy folders
for folder in folders_to_include:
    if os.path.exists(folder):
        dest = os.path.join(deploy_folder, folder)
        shutil.copytree(folder, dest)
        print(f"  [OK] {folder}/")
    else:
        print(f"  [WARN] {folder}/ not found")

print(f"\n[SUCCESS] Deployment package created in: {deploy_folder}/")
print("\n📋 Next steps:")
print("1. Go to GitHub.com and create a new repository 'smartdairy' (PUBLIC)")
print("2. Click 'uploading an existing file'")
print(f"3. Upload ALL contents from: {os.path.abspath(deploy_folder)}")
print("4. Deploy on Streamlit Cloud: https://share.streamlit.io")

