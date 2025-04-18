from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from google.oauth2 import service_account
import re

def extract_table_data(doc_content):
    """Extract coordinate and character data from the document content."""
    coordinates = []
    characters = []
    
    # Parse through document elements to find table data
    for element in doc_content.get('body', {}).get('content', []):
        if 'table' in element:
            table = element['table']
            
            for row in table['tableRows'][1:]:
                cells = row['tableCells']
                if len(cells) == 3:  
                    try:
                        x = int(cells[0]['content'][0]['paragraph']['elements'][0]['textRun']['content'].strip())
                        char = cells[1]['content'][0]['paragraph']['elements'][0]['textRun']['content'].strip()
                        y = int(cells[2]['content'][0]['paragraph']['elements'][0]['textRun']['content'].strip())
                        coordinates.append((x, y))
                        characters.append(char)
                    except (KeyError, ValueError, IndexError):
                        continue
    
    return coordinates, characters

def create_grid(coordinates, characters):
    """Create a 2D grid from coordinates and characters."""
    if not coordinates:
        return []
        
    # Find grid dimensions
    max_x = max(x for x, _ in coordinates) + 1
    max_y = max(y for _, y in coordinates) + 1
    
    # Create empty grid filled with spaces
    grid = [[' ' for _ in range(max_x)] for _ in range(max_y)]
    
    # Place characters in grid
    for (x, y), char in zip(coordinates, characters):
        grid[y][x] = char
    
    return grid

def print_grid(grid):
    """Print the grid row by row."""
    if not grid:
        print("Empty grid")
        return
        
    for row in grid:
        print(''.join(row))

def process_coordinates(coordinates_data):
    """
    Process coordinate data and print the character grid.
    
    Args:
        coordinates_data: List of tuples, each containing (x, y, char)
    """
    try:
        # Split coordinates and characters
        coordinates = [(x, y) for x, y, _ in coordinates_data]
        characters = [char for _, _, char in coordinates_data]
        
        # Create and print grid
        grid = create_grid(coordinates, characters)
        print_grid(grid)
        
    except Exception as e:
        print(f"Error processing coordinates: {str(e)}")

# Example usage:
if __name__ == "__main__":
    # Example data from the document
    example_data = [
        (0, 0, '█'),
        (0, 1, '█'),
        (0, 2, '█'),
        (1, 1, '█'),
        (1, 2, '█'),
        (2, 1, '█'),
        (2, 2, '█'),
        (3, 2, '█')
    ]
    process_coordinates(example_data) 