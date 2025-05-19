#!/usr/bin/env python3
"""
Message Decoder

This module provides a solution for reading coordinate-based character data
from a Google Doc and displaying it as a grid. When displayed in a fixed-width font,
the characters form a graphic showing uppercase letters, which is the secret message.

The coordinate system used:
- (0,0) is the top-left corner of the grid
- x-coordinates increase horizontally (left to right)
- y-coordinates increase vertically (top to bottom)
- Any position without a specified character is filled with a space
"""

import sys
import re
import requests
from typing import List, Tuple
from bs4 import BeautifulSoup

def fetch_document_content(url: str) -> str:
    """
    Fetch the HTML content of a published Google Doc.
    
    Args:
        url (str): The URL of the published Google Doc
    
    Returns:
        str: The HTML content of the document
    
    Raises:
        Exception: If the document cannot be accessed
    """
    response = requests.get(url)
    if response.status_code != 200:
        raise Exception(f"Failed to access document: {response.status_code}")
    return response.text

def parse_document_data(html_content: str) -> List[Tuple[int, int, str]]:
    """
    Parse the HTML content to extract coordinates and characters.
    
    Args:
        html_content (str): The HTML content of the published Google Doc
    
    Returns:
        List[Tuple[int, int, str]]: A list of (x, y, character) tuples
    """
    soup = BeautifulSoup(html_content, 'html.parser')
    
    # Find all table rows
    rows = soup.find_all('tr')
    
    # Skip the header row
    data_rows = rows[1:] if rows else []
    
    data = []
    for row in data_rows:
        # Get all cells in the row
        cells = row.find_all('td')
        
        # Check if we have at least 3 cells (x-coordinate, character, y-coordinate)
        if len(cells) >= 3:
            try:
                x = int(cells[0].get_text().strip())
                char = cells[1].get_text().strip()
                y = int(cells[2].get_text().strip())
                data.append((x, y, char))
            except (ValueError, IndexError):
                continue
    
    # If no data was found in the table, try a more generic approach
    if not data:
        # Extract all text and try to parse it line by line
        text_content = soup.get_text()
        lines = text_content.strip().split('\n')
        
        # Find the header line
        header_index = -1
        for i, line in enumerate(lines):
            if "x-coordinate" in line.lower() and "y-coordinate" in line.lower():
                header_index = i
                break
        
        if header_index != -1:
            # Process data lines after the header
            for line in lines[header_index + 1:]:
                # Skip empty lines
                if not line.strip():
                    continue
                
                # Try to extract x-coordinate, character, y-coordinate
                parts = re.split(r'\s+', line.strip())
                if len(parts) >= 3:
                    try:
                        x = int(parts[0])
                        char = parts[1]
                        y = int(parts[2])
                        data.append((x, y, char))
                    except (ValueError, IndexError):
                        continue
    
    return data

def create_grid(grid_data: List[Tuple[int, int, str]]) -> List[List[str]]:
    """
    Create a grid of characters based on coordinate data.
    
    Args:
        grid_data (List[Tuple[int, int, str]]): A list of (x, y, character) tuples
    
    Returns:
        List[List[str]]: A 2D grid of characters
    """
    if not grid_data:
        return []
    
    # Find grid dimensions
    max_x = max([x for x, _, _ in grid_data])
    max_y = max([y for _, y, _ in grid_data])
    
    # Initialize grid with spaces
    grid = [[' ' for _ in range(max_x + 1)] for _ in range(max_y + 1)]
    
    # Place characters in the grid
    for x, y, char in grid_data:
        grid[y][x] = char
    
    return grid

def display_grid(url: str) -> None:
    """
    Retrieve and parse a Google Doc, then display a grid of characters.
    
    This function takes a Google Doc URL, retrieves the document content,
    extracts coordinate-based character data, and prints the resulting grid.
    Any positions in the grid that do not have a specified character
    are filled with space characters.
    
    The coordinate system follows these rules:
    - (0,0) is the top-left corner of the grid
    - x-coordinates increase horizontally (left to right)
    - y-coordinates increase vertically (top to bottom)
    
    When printed in a fixed-width font, the characters in the grid will form
    a graphic showing a sequence of uppercase letters, which is the secret message.
    
    Example:
    For a document defining character positions that form the letter 'F':
    ```
    x-coordinate Character y-coordinate
    0           █         0
    0           █         1
    0           █         2
    1           ▀         1
    1           ▀         2
    2           ▀         1
    2           ▀         2
    3           ▀         2
    ```
    
    The output would be:
    ```
    █   
    █▀▀ 
    █▀▀▀
    ```
    
    Args:
        url (str): URL of the Google Doc containing coordinate data
        
    Returns:
        None: The function prints the grid to stdout
        
    Raises:
        Exception: If any error occurs during processing
    """
    try:
        html_content = fetch_document_content(url)
        grid_data = parse_document_data(html_content)
        
        if not grid_data:
            print("No valid grid data found in the document.")
            return
        
        grid = create_grid(grid_data)
        
        # Print the grid
        for row in grid:
            print(''.join(row))
            
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

# Example usage
if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python message_decoder.py <google_doc_url>")
        sys.exit(1)
        
    url = sys.argv[1]
    display_grid(url) 