import shutil
from pathlib import Path

# Get the absolute path of the current Python file
script_path = Path(__file__).resolve()

script_dir = script_path.parent
parent_dir = script_dir.parent

fxp_dir = Path("Monzafxp") / "modules_fxp" / "dsp_rx"

# Define targets
target_file_doc    = script_dir / fxp_dir / "doc" / "fxpSignals.xlsx"
target_file_test   = script_dir / fxp_dir / "test" / "validation" / "rtl_vm_test.py"
target_file_gen   = script_dir / fxp_dir / "test" / "validation" / "generate_sv_test.py"
target_file_tb_dir = script_dir / fxp_dir / "usim" / "tb" / "tb_rtl_vm"
target_file_logs   = script_dir / "Monzafxp" / "libs" / "log_rx_rtl.py"

# Define destination paths
dest_path_doc      = parent_dir / "farina_tc_dsp" / "common" / "MonzaFxp" / "modules_fxp" / "dsp_rx" / "doc" / "fxpSignals.xlsx"
dest_path_test     = parent_dir / "farina_tc_dsp" / "common" / "MonzaFxp" / "modules_fxp" / "dsp_rx" / "tests" / "validation" / "rtl_vm_test.py"
dest_path_gen      = parent_dir / "farina_tc_dsp" / "common" / "MonzaFxp" / "modules_fxp" / "dsp_rx" / "tests" / "generate_sv_test.py"
dest_path_tb_dir   = parent_dir / "farina_tc_dsp" / "common" / "MonzaFxp" / "modules_fxp" / "dsp_rx" / "usim" / "testbench" / "tb_rtl_vm"
dest_path_logs     = parent_dir / "farina_tc_dsp" / "common" / "MonzaFxp" / "libs" / "log_rx_rtl.py" 

def copy_item(target, dest_path, is_dir=False):
    try:
        print(f"\nProcessing: {target}")
        print(f"Target exists? {target.exists()}")

        if not target.exists():
            print(f"❌ Target does not exist: {target}")
            return

        # Ensure parent directory exists
        dest_path.parent.mkdir(parents=True, exist_ok=True)

        # Remove existing destination
        if dest_path.exists():
            if dest_path.is_dir():
                shutil.rmtree(dest_path)
            else:
                dest_path.unlink()

        # Copy file or directory
        if is_dir:
            shutil.copytree(target, dest_path)
        else:
            shutil.copy2(target, dest_path)

        print(f"✅ Copied to: {dest_path}")
    except Exception as e:
        print(f"❌ Failed to copy {target} to {dest_path}: {e}")

# Perform the copies
copy_item(target_file_doc,    dest_path_doc,    is_dir=False)
copy_item(target_file_test,   dest_path_test,   is_dir=False)
copy_item(target_file_gen,   dest_path_gen,   is_dir=False)
copy_item(target_file_tb_dir, dest_path_tb_dir, is_dir=True)
copy_item(target_file_logs,   dest_path_logs,   is_dir=False)
