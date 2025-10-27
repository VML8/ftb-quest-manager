import os
import sys
from typing import Dict, Any
from pydantic import ValidationError

# Assuming your package structure means quest_models is available via relative import
# NOTE: This line must be updated if Chapter is not in the same package root.
from ..model.quest_models import Chapter 

# Assuming ftb_snbt_lib is installed or available in the environment
# If fslib is a global module, this import is correct.
import ftb_snbt_lib as fslib 


# --- Path Discovery Logic (Integrated from previous steps) ---

# The standard relative path from the modpack root to the chapters directory
FTB_QUESTS_REL_PATH = os.path.join("config", "ftbquests", "quests", "chapters")

def is_valid_chapters_dir(path: str) -> bool:
    """Checks if the given path is a readable directory containing SNBT files."""
    if not os.path.isdir(path):
        return False
    # Check for presence of at least one expected quest file (.snbt)
    try:
        if any(f.endswith(".snbt") for f in os.listdir(path)):
            return True
    except OSError:
        # Handles potential PermissionError during os.listdir
        return False
    return False

def find_chapters_directory() -> str:
    """
    Attempts to find the FTB Quests chapters directory using the desired multi-stage approach.
    """
    print("\n--- Starting Directory Discovery ---")

    # Attempt 1: Check relative to the current working directory (CWD)
    # This assumes the script is run from inside the modpack directory.
    cwd_path = os.path.join(os.getcwd(), FTB_QUESTS_REL_PATH)
    if is_valid_chapters_dir(cwd_path):
        print(f"Found Quests: Using CWD path: {cwd_path}")
        return cwd_path

    # Attempt 2: Check relative to the script's location 
    # This helps if the script is run via a symlink or launcher shortcut.
    script_dir = os.path.abspath(os.path.dirname(sys.argv[0]))
    script_relative_path = os.path.join(script_dir, FTB_QUESTS_REL_PATH)
    if is_valid_chapters_dir(script_relative_path):
        print(f"Found Quests: Using script-relative path: {script_relative_path}")
        return script_relative_path
        
    print("Could not automatically detect FTB Quests config.")
    
    # Fallback: User Input Loop
    while True:
        print("\n--- Manual Directory Input ---")
        print("Please provide the absolute path to your modpack's 'chapters' directory.")
        print(f"Example target path: .../modpack_dir/{os.path.join('config', 'ftbquests', 'quests', 'chapters')}")
        print("Type 'EXIT' to quit.")
        
        user_path = input("Enter Absolute Path: ").strip()
        
        if user_path.lower() == 'exit':
            sys.exit("Quitting program as requested.")
        
        if is_valid_chapters_dir(user_path):
            print(f"Success! Loading from: {user_path}")
            return user_path
        else:
            print(f"Directory invalid or not found. Path checked: {user_path}")
            print("Ensure the path leads directly to the folder containing .snbt files.")


# --- Modified Loading and Parsing Logic ---

def load_chapter_data(chapters_dir_path: str) -> Dict[str, Any]:
    """
    Load and parse FTB quest chapter data from SNBT files using the discovered path.
    """
    raw_chapter_data = {}
    
    try:
        # List files in the discovered directory path
        for chapter_file in os.listdir(chapters_dir_path):
            if chapter_file.endswith(".snbt"):
                # Construct the full path using os.path.join for safety
                full_path = os.path.join(chapters_dir_path, chapter_file)
                
                # Open the file and pass the handle to fslib.load
                with open(full_path, "r", encoding="utf-8") as f:
                    raw_chapter_data[chapter_file] = fslib.load(f)

    except PermissionError:
        print(f"Permission denied accessing directory: {chapters_dir_path}")
    except FileNotFoundError:
        print(f"Directory not found: {chapters_dir_path}")
    except Exception as e:
        print(f"Unexpected error during file loading: {e}")

    return raw_chapter_data

def parse_chapters(raw_chapter_data: Dict[str, Any]) -> Dict[str, Chapter]:
    """Parse raw chapter data into Chapter objects (Pydantic mounting)."""
    parsed_chapters = {}

    for chapter_filename, chapter_dict in raw_chapter_data.items():
        # Use the filename (minus extension) as the clean key
        chapter_key = chapter_filename.replace(".snbt", "")
        try:
            chapter_object = Chapter.model_validate(chapter_dict)
            parsed_chapters[chapter_key] = chapter_object
            # print(f"Successfully mounted chapter: {chapter_key}") # Commented for cleaner output
        except ValidationError as e:
            # Catch specific Pydantic errors for better debugging
            print(f"Failed to mount chapter {chapter_key} due to Validation Error.")
            print(e)
        except Exception as e:
            print(f"Failed to mount chapter {chapter_key}: {e}")

    return parsed_chapters

def load_and_parse_all() -> Dict[str, Chapter]:
    """Orchestrates the path finding, loading, and parsing process."""
    
    # Step 1: Discover the correct directory path
    chapters_path = find_chapters_directory()
    
    # Step 2: Load the raw data using the discovered path
    raw_data = load_chapter_data(chapters_path)
    
    if not raw_data:
        print("No quest files were loaded. Exiting.")
        return {}
        
    # Step 3: Parse and mount the data into Pydantic objects
    return parse_chapters(raw_data)

# NOTE: Your main application script should now call load_and_parse_all() 
# to get the fully structured and mounted data.
