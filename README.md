# Data Annotation Solution

This project provides a solution for reading coordinate-based character data from a Google Doc and displaying it as a grid. When displayed in a fixed-width font, the characters form a graphic showing uppercase letters, which is the secret message.


## Setup

1. Clone this repository
2. Create and activate a virtual environment:
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
3. Install the required packages:
   ```
   pip install -r requirements.txt
   ```

## Usage

Run the script with a Google Doc URL:

```
python decoder_solution.py <google_doc_url>
```

### Authentication

The script uses OAuth2 for Google Docs API authentication:
- On first run, it will prompt you to authorize access
- Credentials will be saved to `token.pickle` for future use
- You'll need a `credentials.json` file from the Google API Console

## How it Works

1. The script extracts the document ID from the provided Google Doc URL
2. It retrieves the document content using the Google Docs API
3. Parses the document to extract coordinate-based character data
4. Creates a grid and places each character at its specified position
5. Prints the resulting grid, revealing the hidden message

## Coordinate System

- (0,0) is the top-left corner of the grid
- x-coordinates increase horizontally (left to right)
- y-coordinates increase vertically (top to bottom)
- Any position without a specified character is filled with a space

## Example

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
