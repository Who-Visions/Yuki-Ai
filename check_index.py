
from pathlib import Path

ref_dir = Path("c:/Yuki_Local/Cosplay_Lab/References")
refs = sorted(list(ref_dir.glob("*.[jJ][pP][gG]")))

for i, ref in enumerate(refs, 1):
    print(f"{i}: {ref.name}")
