import os
import importlib
import inspect

# Import all strategy classes from all .py files in the strategies directory
for file in os.listdir(os.path.dirname(__file__)):
    if file.endswith('.py') and not file.startswith('__'):
        module = importlib.import_module(f'.{file[:-3]}', package=__package__)
        for name, obj in inspect.getmembers(module):
            if inspect.isclass(obj) and name.endswith('Strategy'):
                globals()[name] = obj
