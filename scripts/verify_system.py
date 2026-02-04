
import sys
import os
from pathlib import Path
import subprocess

# Add project root to python path
project_root = Path.cwd()
sys.path.insert(0, str(project_root))

from tools.labeling.config import get_labels

def run_command(command):
    print(f"\n🚀 Running: {command}")
    try:
        # Use shell=True for complex commands with arguments
        result = subprocess.run(command, shell=True, check=True, text=True, capture_output=True)
        print("✅ Success")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Error: {e}")
        print(f"   Stderr: {e.stderr}")
        return False

def verify_id_consistency():
    print("\n🔍 Verifying ID Consistency...")
    labels4 = get_labels("4_labels")
    labels5 = get_labels("5_labels")
    
    consistent = True
    
    # Check 0-3 match
    for i in range(4):
        if labels4[i] != labels5[i]:
            print(f"❌ Mismatch at ID {i}: {labels4[i]} vs {labels5[i]}")
            consistent = False
            
    # Check ID 4 in 5-labels
    if labels5.get(4) != "Multiple Voices":
        print(f"❌ ID 4 is not Multiple Voices: {labels5.get(4)}")
        consistent = False
        
    if consistent:
        print("✅ IDs 0-3 match perfectly between configs.")
        print("✅ ID 4 is correctly assigned to 'Multiple Voices'.")
    return consistent

def main():
    print("="*60)
    print("VIRTUOSO ARCHITECT - FINAL SYSTEM VERIFICATION")
    print("="*60)
    
    # 1. Verify Logic
    if not verify_id_consistency():
        print("\n❌ Critical Logic Failure. Aborting.")
        sys.exit(1)
        
    python_exe = sys.executable
    
    # 2. Test 4-Label Pipeline
    print("\n" + "="*40)
    print("TESTING 4-LABEL PIPELINE")
    print("="*40)
    
    cmds_4 = [
        f'"{python_exe}" tools/labeling/auto/auto_label.py --config 4_labels --overwrite',
        f'"{python_exe}" scripts/train_with_labels.py --labels auto_4_labels.csv',
        f'"{python_exe}" scripts/evaluate_model.py --labels auto_4_labels.csv'
    ]
    
    for cmd in cmds_4:
        if not run_command(cmd):
            print("❌ 4-Label Pipeline Failed!")
            sys.exit(1)
            
    # 3. Test 5-Label Pipeline
    print("\n" + "="*40)
    print("TESTING 5-LABEL PIPELINE")
    print("="*40)
    
    cmds_5 = [
        f'"{python_exe}" tools/labeling/auto/auto_label.py --config 5_labels --overwrite',
        f'"{python_exe}" scripts/train_with_labels.py --labels auto_5_labels.csv',
        f'"{python_exe}" scripts/evaluate_model.py --labels auto_5_labels.csv'
    ]
    
    for cmd in cmds_5:
        if not run_command(cmd):
            print("❌ 5-Label Pipeline Failed!")
            sys.exit(1)
            
    print("\n" + "="*60)
    print("🎉 ALL SYSTEMS GO! VERIFICATION COMPLETE.")
    print("="*60)

if __name__ == "__main__":
    main()
