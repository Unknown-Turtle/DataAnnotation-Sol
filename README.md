# Grid Character Printer

This Python script takes coordinate and character data and prints a grid of characters that forms a message made of uppercase letters.

## Usage

The script provides a `process_coordinates()` function that takes a list of coordinate data and prints the resulting grid. Each coordinate is specified as a tuple of (x, y, character).

```python
from grid_printer import process_coordinates

# Example data
data = [
    (0, 0, '█'),  # (x, y, character)
    (0, 1, '█'),
    (0, 2, '█'),
    (1, 1, '█'),
    (1, 2, '█'),
    (2, 1, '█'),
    (2, 2, '█'),
    (3, 2, '█')
]

process_coordinates(data)
```

The script will print the grid of characters, revealing the hidden message.

## Example Output

For the example input data above, the output will be:
```
█▀▀▀
█▀▀ 
█   
```

This forms the letter 'F'.

## How it Works

1. The script takes a list of (x, y, character) coordinates
2. Creates a grid large enough to fit all coordinates
3. Places each character at its specified position
4. Fills empty positions with spaces
5. Prints the resulting grid 