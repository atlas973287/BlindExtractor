from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.table import Table
from rich.prompt import Prompt
from core.extractor import read_output_parallel
import multiprocessing

console = Console()

def interactive_shell(strategy, debug_mode=False):
    """Provides an interactive shell-like environment to execute commands"""
    console.print(Panel.fit(
        "[bold cyan]Blind Exploitation Interactive Shell[/]",
        border_style="blue"
    ))
    console.print("[yellow]Type 'exit' or 'quit' to exit the shell[/]")
    console.print("[yellow]Type 'help' for available commands[/]")
    
    history = []
    
    # Set default workers based on debug mode
    if debug_mode:
        num_workers = 1
        batch_size = 1
    else:
        num_workers = min(10, multiprocessing.cpu_count())  # Default to CPU count
        batch_size = num_workers * 4
    
    while True:
        try:
            # Display prompt
            cmd = Prompt.ask("\n[bold green]$[/]")
            
            # Handle special commands
            if cmd.lower() in ['exit', 'quit']:
                console.print("[yellow]Exiting shell...[/]")
                break
                
            elif cmd.lower() == 'help':
                table = Table(title="Available Commands")
                table.add_column("Command", style="cyan")
                table.add_column("Description", style="green")
                
                table.add_row("exit/quit", "Exit the shell")
                table.add_row("help", "Display this help message")
                table.add_row("history", "Show command history")
                table.add_row("workers N", "Set number of parallel workers to N")
                table.add_row("batch N", "Set batch size to N")
                table.add_row("debug on/off", "Toggle debug mode (single thread)")
                table.add_row("Any other input", "Execute as a command on the target")
                
                console.print(table)
            
            elif cmd.lower() == 'history':
                # Show command history
                if not history:
                    console.print("[yellow]No commands in history[/]")
                else:
                    table = Table(title="Command History")
                    table.add_column("#", style="cyan")
                    table.add_column("Command", style="green")
                    
                    for i, hist_cmd in enumerate(history):
                        table.add_row(str(i+1), hist_cmd)
                    
                    console.print(table)
            
            elif cmd.lower().startswith('workers '):
                # Set number of workers
                try:
                    if debug_mode:
                        console.print("[bold yellow]Debug mode is enabled. Cannot change worker count.[/]")
                        console.print("[bold yellow]Use 'debug off' to disable debug mode first.[/]")
                        continue
                        
                    new_workers = int(cmd.split(' ')[1])
                    if new_workers < 1:
                        console.print("[bold red]Number of workers must be at least 1[/]")
                    else:
                        num_workers = new_workers
                        console.print(f"[bold green]Number of workers set to {num_workers}[/]")
                except (ValueError, IndexError):
                    console.print("[bold red]Invalid worker count. Usage: workers N[/]")
            
            elif cmd.lower().startswith('batch '):
                # Set batch size
                try:
                    if debug_mode:
                        console.print("[bold yellow]Debug mode is enabled. Cannot change batch size.[/]")
                        console.print("[bold yellow]Use 'debug off' to disable debug mode first.[/]")
                        continue
                        
                    new_batch = int(cmd.split(' ')[1])
                    if new_batch < 1:
                        console.print("[bold red]Batch size must be at least 1[/]")
                    else:
                        batch_size = new_batch
                        console.print(f"[bold green]Batch size set to {batch_size}[/]")
                except (ValueError, IndexError):
                    console.print("[bold red]Invalid batch size. Usage: batch N[/]")
            
            elif cmd.lower() == 'debug on':
                debug_mode = True
                num_workers = 1
                batch_size = 1
                console.print("[bold yellow]Debug mode enabled - using single thread[/]")
            
            elif cmd.lower() == 'debug off':
                debug_mode = False
                num_workers = min(10, multiprocessing.cpu_count())
                batch_size = num_workers * 4
                console.print("[bold green]Debug mode disabled - using multiple threads[/]")
                console.print(f"[bold]Workers set to:[/] [cyan]{num_workers}[/]")
                console.print(f"[bold]Batch size set to:[/] [cyan]{batch_size}[/]")
                    
            elif cmd.strip():
                # Add to history
                history.append(cmd)
                
                # Execute the command
                console.print(f"[bold]Executing:[/] [cyan]{cmd}[/]")
                
                if debug_mode:
                    console.print("[bold yellow]Debug mode:[/] Using single thread")
                else:
                    console.print(f"[bold]Using[/] [cyan]{num_workers}[/] parallel processes with batch size [cyan]{batch_size}[/]")
                
                result = read_output_parallel(cmd, strategy, max_workers=num_workers, batch_size=batch_size, debug_mode=debug_mode)
                console.print(Panel(result, title="[bold green]Decoded Output[/]", border_style="green"))
                
        except KeyboardInterrupt:
            console.print("\n[bold yellow]Command interrupted[/]")
        except Exception as e:
            console.print(f"[bold red]Error:[/] {str(e)}")