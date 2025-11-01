import json
import os
from typing import Optional, List, Dict, Any

def add_ids_to_json(input_filepath: str) -> Optional[str]:
    """
    Reads a JSON file, adds a sequential 'id' to each element, and saves
    the result to an 'Outputs' folder within the input file's directory.

    Args:
        input_filepath: The path to the source JSON file.

    Returns:
        The path to the newly created modified file, or None if an error occurred.
    """
    # 1. Determine the output directory and filename
    input_dir = os.path.dirname(input_filepath)
    filename = os.path.basename(input_filepath)
    base, ext = os.path.splitext(filename)
    
    # Define the new output folder path (e.g., /path/to/file/Outputs)
    output_dir = os.path.join(input_dir, "Outputs")
    
    # Define the new output filename (e.g., /path/to/file/Outputs/original-mod.json)
    output_filename = f"{base}-mod{ext}"
    output_filepath = os.path.join(output_dir, output_filename)

    try:
        # 2. Safely create the output directory
        os.makedirs(output_dir, exist_ok=True)

        # 3. Read the data
        with open(input_filepath, 'r', encoding='utf-8') as infile:
            data: Any = json.load(infile)

        if isinstance(data, list):
            data_list: List[Dict[str, Any]] = data
            
            # 4. Add sequential IDs
            for index, entry in enumerate(data_list):
                if isinstance(entry, dict):
                    entry['id'] = index + 1  # Start numbering from 1

            # 5. Write the modified data
            with open(output_filepath, 'w', encoding='utf-8') as outfile:
                json.dump(data_list, outfile, indent=2, ensure_ascii=False)
            
            print(f"✅ Success: Processed '{filename}'")
            print(f"   Saved to '{output_filepath}'")
            return output_filepath
        else:
            print(f"⚠️ Error: The JSON data in '{filename}' is not a list/array. Skipping.")
            return None

    except FileNotFoundError:
        print(f"❌ Error: The file '{input_filepath}' was not found. Skipping.")
        return None
    except json.JSONDecodeError:
        print(f"❌ Error: Could not decode JSON from the file '{input_filepath}'. Skipping.")
        return None
    except Exception as e:
        print(f"❌ An unexpected error occurred while processing '{filename}': {e}. Skipping.")
        return None

# --- NEW FUNCTION FOR FOLDER PROCESSING ---

def process_folder(folder_path: str) -> None:
    """
    Iterates through all .json files in a directory and adds IDs to each one.

    Args:
        folder_path: The path to the directory containing JSON files.
    """
    print(f"\nProcessing all JSON files in folder: {folder_path}")
    json_files = [f for f in os.listdir(folder_path) if f.lower().endswith('.json')]
    
    if not json_files:
        print("ℹ️ No .json files found in this directory.")
        return

    for filename in json_files:
        filepath = os.path.join(folder_path, filename)
        # Ensure it's a file and not a directory that ends in .json
        if os.path.isfile(filepath):
            add_ids_to_json(filepath)
    
    print("\n🎉 Folder batch processing complete!")

# --- UPDATED MAIN FUNCTION ---

def main() -> None:
    """
    Main function to handle user input for single file or folder processing.
    """
    while True:
        print("\n" + "=" * 50)
        mode_choice = input("Process a **(F)**ile or a **(D)**irectory (Folder)? (F/D/exit): ").lower().strip()
        print("=" * 50)

        if mode_choice == 'exit':
            break
        elif mode_choice not in ('f', 'd'):
            print("⚠️ Invalid choice. Please enter 'F' for file, 'D' for directory, or 'exit'.")
            continue

        prompt = "Enter the input JSON **file** path: " if mode_choice == 'f' else "Enter the input **directory** path: "
        user_input_path = input(prompt).strip().strip('"\'')
        
        if not user_input_path:
            print("⚠️ Input cannot be empty.")
            continue

        # Normalize the path for system compatibility and use absolute path for reliability
        normalized_path = os.path.abspath(os.path.normpath(user_input_path))

        if mode_choice == 'f':
            # Single file mode
            if os.path.isfile(normalized_path) and normalized_path.lower().endswith('.json'):
                add_ids_to_json(normalized_path)
            else:
                print(f"⚠️ Invalid input: '{user_input_path}' is not a valid JSON file path or does not exist.")
        
        elif mode_choice == 'd':
            # Directory (Folder) mode
            if os.path.isdir(normalized_path):
                process_folder(normalized_path)
            else:
                print(f"⚠️ Invalid input: '{user_input_path}' is not a valid directory path or does not exist.")

        # Ask if the user wants to process another
        print("\n" + "=" * 50)
        another = input("Do you want to process another file or folder? (y/N): ").lower().strip()
        if another != 'y':
            break

    print("\n👋 Goodbye! Program terminated.")

if __name__ == "__main__":
    main()