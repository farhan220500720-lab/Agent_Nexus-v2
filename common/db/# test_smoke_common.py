import sys
import os

current_dir = os.path.dirname(os.path.abspath(__file__))
root_dir = os.path.abspath(os.path.join(current_dir, "../../"))
sys.path.append(root_dir)

def test_common_imports():
    print("🚀 STARTING SMOKE TEST...")
    
    try:
        # Attempting imports
        import common.db.postgres as pg
        import common.db.vector_store as vs
        import common.logger as lg
        import common.schemas.memory as ms

        # Verifying they loaded
        assert pg is not None
        assert vs is not None
        assert lg is not None
        assert ms is not None
        
        print("✅ SUCCESS: All agent modules imported correctly!")
        print(f"   - Database URL set: {'DATABASE_URL' in os.environ or 'Default Used'}")
        print(f"   - Log Directory: {lg.LOG_DIR}")
        
    except ImportError as e:
        print(f"❌ IMPORT ERROR: Python cannot find the module.\nDetails: {e}")
        print("   -> Tip: Check your sys.path or folder structure.")
    except Exception as e:
        print(f"❌ UNKNOWN ERROR: {e}")

if __name__ == "__main__":
    test_common_imports()