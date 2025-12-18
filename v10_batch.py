"""Batch generate V10 images 2-9 with full face replacement"""
import asyncio
import subprocess
import sys
import os

os.environ['PYTHONIOENCODING'] = 'utf-8'

async def batch_generate():
    for i in range(2, 10):
        print(f"\n{'='*50}")
        print(f"Regenerating image {i}/9 with FULL REPLACEMENT prompt...")
        print(f"{'='*50}")
        
        result = subprocess.run(
            [sys.executable, "v10_generate_one.py", str(i)],
            cwd="c:/Yuki_Local",
            capture_output=True,
            text=True,
            encoding='utf-8',
            errors='replace'
        )
        print(result.stdout)
        if result.returncode != 0 and result.stderr:
            print(f"Error: {result.stderr[:500]}")
        
        if i < 9:
            print(f"Waiting 45s before next...")
            await asyncio.sleep(45)
    
    print("\n" + "="*50)
    print("BATCH COMPLETE! Generated images 2-9")
    print("="*50)

if __name__ == "__main__":
    asyncio.run(batch_generate())
