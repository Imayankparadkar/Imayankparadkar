import sys
import os

def image_to_ascii(image_path=None, num_lines=69, num_cols=100):
    ascii_file = "user_pasted_ascii.txt"
    if not os.path.exists(ascii_file):
        print(f"Error: {ascii_file} not found in workspace.")
        return None
        
    with open(ascii_file, "r", encoding="utf-8") as f:
        lines = [line.rstrip("\r\n") for line in f.readlines()]
        
    height = len(lines)
    width = len(lines[0]) if height > 0 else 0
    
    # Convert lines to a 2D list of characters
    grid = [list(line) for line in lines]
    
    # Flood fill background '@' to ' ' starting from top, left, and right edges
    # We restrict it to y < 45 to prevent flooding the shirt at the bottom
    visited = set()
    queue = []
    
    # Add top border points
    for x in range(width):
        if grid[0][x] == '@':
            queue.append((x, 0))
            visited.add((x, 0))
            
    # Add left and right border points (only up to y=44)
    for y in range(min(height, 45)):
        if grid[y][0] == '@':
            queue.append((0, y))
            visited.add((0, y))
        if grid[y][width-1] == '@':
            queue.append((width-1, y))
            visited.add((width-1, y))
            
    # Perform flood fill
    while queue:
        x, y = queue.pop(0)
        grid[y][x] = ' '
        
        # Check neighbors
        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            nx, ny = x + dx, y + dy
            if 0 <= nx < width and 0 <= ny < min(height, 45):
                if (nx, ny) not in visited and grid[ny][nx] == '@':
                    visited.add((nx, ny))
                    queue.append((nx, ny))
                    
    # Clean up any remaining '@' on the outer corners
    for y in range(45, height):
        for x in range(width):
            if (x < 24 or x > 76) and grid[y][x] == '@':
                grid[y][x] = ' '
                
    # Reconstruct cleaned lines
    cleaned_lines = ["".join(row) for row in grid]
    
    # Calculate the minimum leading spaces among non-empty lines to trim empty left margin
    non_empty_lines = [line for line in cleaned_lines if line.strip()]
    if non_empty_lines:
        min_leading = min(len(line) - len(line.lstrip()) for line in non_empty_lines)
    else:
        min_leading = 0
        
    print(f"Trimming {min_leading} leading spaces to shift ASCII art left")
    
    # Trim leading spaces and apply a safety right-side limit at column 84
    final_lines = []
    for line in cleaned_lines:
        trimmed = line[min_leading:].rstrip()
        if len(trimmed) > 84:
            trimmed = trimmed[:84]
        final_lines.append(trimmed)
        
    return final_lines

if __name__ == "__main__":
    lines = image_to_ascii()
    if lines:
        # Save as the active ascii_art.txt
        with open("ascii_art.txt", "w", encoding="utf-8") as f:
            for line in lines:
                f.write(line + "\n")
        print("Successfully processed, trimmed, and saved 100x69 ascii_art.txt")
