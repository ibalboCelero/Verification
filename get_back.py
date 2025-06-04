import shutil
from pathlib import Path

# Get path of this script
script_path = Path(__file__).resolve()
script_dir  = script_path.parent
parent_dir  = script_dir.parent

fxp_dir = Path("Monzafxp") / "modules_fxp" / "dsp_rx"

# -------- source in COMMON --------
src_doc    = parent_dir / "farina_tc_dsp" / "common"  / "MonzaFxp" / "modules_fxp" / "dsp_rx" / "doc" / "fxpSignals.xlsx"
src_test   = parent_dir / "farina_tc_dsp" / "common"  / "MonzaFxp" / "modules_fxp" / "dsp_rx" / "tests" / "validation" / "rtl_vm_test.py"
src_tb_dir = parent_dir / "farina_tc_dsp" / "common"  / "MonzaFxp" / "modules_fxp" / "dsp_rx" / "usim" / "testbench" / "tb_rtl_vm"
dest_path_logs     = parent_dir / "farina_tc_dsp" / "common" / "MonzaFxp" / "libs" / "log_rx_rtl.py" 

# -------- destination in VERIFICATION --------
dst_doc    = script_dir / fxp_dir / "doc" / "fxpSignals.xlsx"
dst_test   = script_dir / fxp_dir / "test" / "validation" / "rtl_vm_test.py"
dst_tb_dir = script_dir / fxp_dir / "usim" / "tb" / "tb_rtl_vm"
target_file_logs   = script_dir / "Monzafxp" / "libs" / "log_rx_rtl.py"

def copy_item(src: Path, dst: Path, is_dir: bool = False):
    print(f"\n→ {src}  →  {dst}")

    if not src.exists():
        print(f"   ✖  source does not exist")
        return

    dst.parent.mkdir(parents=True, exist_ok=True)

    if dst.exists() or dst.is_symlink():
        if dst.is_symlink():
            dst.unlink()
        elif dst.is_dir():
            shutil.rmtree(dst)
        else:
            dst.unlink()

    try:
        if is_dir:
            shutil.copytree(src, dst)
        else:
            shutil.copy2(src, dst)
        print("   ✔  copied")
    except Exception as e:
        print(f"   ✖  failed: {e}")

# Perform reverse copy
copy_item(src_doc,    dst_doc,    is_dir=False)
copy_item(src_test,   dst_test,   is_dir=False)
copy_item(src_tb_dir, dst_tb_dir, is_dir=True)
copy_item(dest_path_logs, target_file_logs, is_dir=False)
