"""
🐕 YUKI WATCHDOG 🐕
Monitors 'yuki_ultimate_test.py'.
If it crashes or stops, it restarts it immediately (resuming from state file).
Auto-checks every run.
"""
import subprocess
import time
from rich.console import Console

console = Console()
CMD = "python yuki_ultimate_test.py"
CWD = "c:/Yuki_Local/Cosplay_Lab/Brain"

def watch():
    console.print("[bold red]🐕 YUKI WATCHDOG ACTIVE: guarding the generator...[/bold red]")
    
    while True:
        console.print(f"\n[yellow]🚀 Launching {CMD}...[/yellow]")
        try:
            # Run blocking call - wait for it to finish/crash
            subprocess.run(CMD, cwd=CWD, shell=True)
            
            console.print("[red]⚠️ Process exited! Restarting in 30s...[/red]")
            time.sleep(30)
            
        except KeyboardInterrupt:
            console.print("[green]🐕 Watchdog sleeping.[/green]")
            break
        except Exception as e:
            console.print(f"[red]❌ Watchdog Error: {e}[/red]")
            time.sleep(60)

if __name__ == "__main__":
    watch()
