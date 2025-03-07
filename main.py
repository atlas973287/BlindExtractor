import multiprocessing
import argparse
from rich.console import Console
from strategies import *
from core.shell import interactive_shell

console = Console()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Blind exploitation tool")
    parser.add_argument("--debug", action="store_true", help="Enable debug mode (single thread)")
    args = parser.parse_args()

    # Set the start method for multiprocessing
    try:
        multiprocessing.set_start_method('spawn')
    except RuntimeError:
        # The start method may have already been set
        pass

    # Choose your strategy here - uncomment the one you want to use
    # strategy = JavaRCEStrategy(url="http://localhost/")  # For Java RCE
    # strategy = PickleRCEStrategy(url="http://localhost/")  # For Pickle RCE
    # strategy = SQLiStrategy(url="http://localhost/")  # For SQL Injection
    strategy = LocalTestStrategy()  # For local testing
    debug_mode = args.debug
    if debug_mode:
        console.print("[bold yellow]Debug mode enabled - using single thread[/]")
        
    try:
        interactive_shell(strategy, debug_mode=debug_mode)
    except KeyboardInterrupt:
        console.print("\n[bold yellow]Operation cancelled by user[/]")
    except Exception as e:
        console.print(f"[bold red]Unhandled exception:[/] {str(e)}")
    finally:
        console.print("[yellow]Exiting program[/]")