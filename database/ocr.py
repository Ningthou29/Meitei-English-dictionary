from PIL import Image, ImageOps
import pytesseract # type: ignore
import pandas as pd
import re
from pathlib import Path
from typing import Union, cast

# Set Tesseract binary path
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

MAX_WORDS: int = 38 

def sentence_aware_chunks(text: str, max_words: int = MAX_WORDS) -> list[str]:
    text = re.sub(r'\s+', ' ', text).strip()
    if not text:
        return []

    sentences: list[str] = re.split(r'(?<=[.!?])\s+', text)
    
    chunks: list[str] = []
    current: list[str] = []
    count: int = 0

    for s in sentences:
        words: list[str] = s.split()

        if len(words) > max_words:
            if current:
                chunks.append(" ".join(current))
                current, count = [], 0
            for i in range(0, len(words), max_words):
                chunks.append(" ".join(words[i:i+max_words]))
            continue

        if count + len(words) > max_words:
            chunks.append(" ".join(current))
            current, count = [s], len(words)
        else:
            current.append(s)
            count += len(words)

    if current:
        chunks.append(" ".join(current))

    return chunks

def process_image(image_path: Union[str, Path]) -> list[str]:
    img: Image.Image = Image.open(image_path).convert("L")
    img = ImageOps.autocontrast(img)
    text: str = cast(str, pytesseract.image_to_string(img, lang="eng")) # type: ignore
    return sentence_aware_chunks(text)

def main() -> None:
    folder_name: str = input("Enter the image folder name: ").strip()
    folder: Path = Path(folder_name)

    if not folder.exists() or not folder.is_dir():
        print("Folder does not exist.")
        return

    # Gather all target images
    all_images: list[Path] = (
        list(folder.glob("*.jpg")) + 
        list(folder.glob("*.jpeg")) + 
        list(folder.glob("*.jp2"))
    )
    
    if not all_images:
        print("No JPG/JPEG/JP2 files found in the folder.")
        return

    # Files for tracking progress and final output
    progress_csv: Path = folder / f"{folder.name}_checkpoint.csv"
    output_excel: Path = folder / f"{folder.name}_output.xlsx"

    processed_files: set[str] = set()

    # Feature: Load pre-existing progress if the checkpoint file exists
    if progress_csv.exists():
        try:
            existing_df = pd.read_csv(progress_csv)
            if "image_name" in existing_df.columns:
                processed_files = set(existing_df["image_name"].dropna().unique())
                print(f"Resuming progress: Found {len(processed_files)} already processed images.")
        except Exception:
            print("Checkpoint file corrupted or unreadable. Starting fresh.")

    # Filter out images that are already processed
    images_to_process: list[Path] = [img for img in all_images if img.name not in processed_files]

    if not images_to_process:
        print("All images in this folder have already been processed!")
    else:
        print(f"Total images: {len(all_images)} | Already Done: {len(processed_files)} | Remaining to Process: {len(images_to_process)}")
        
        # Open CSV in append mode ('a') to save progress instantly
        with open(progress_csv, mode="a", encoding="utf-8", newline="") as f:
            for img in images_to_process:
                print(f"Processing: {img.name}")
                try:
                    chunks: list[str] = process_image(img)
                    
                    # Write each text chunk mapped to its image name immediately
                    for chunk in chunks:
                        # Simple escaping for CSV safety
                        clean_chunk = chunk.replace('"', '""')
                        f.write(f'"{img.name}","{clean_chunk}"\n')
                    
                    # If an image has no text chunks, log it anyway so it gets skipped next time
                    if not chunks:
                        f.write(f'"{img.name}",""\n')
                        
                    f.flush() # Force write out to the hard drive immediately
                except Exception as e:
                    print(f"Failed to process {img.name}. Error: {e}. Skipping for now...")

    # Step 3: Compile the final Excel spreadsheet using the progress backup
    if progress_csv.exists():
        print("\nCompiling final Excel file...")
        try:
            final_df = pd.read_csv(progress_csv, names=["image_name", "english"], header=None)
            # Filter out any blank text placeholders
            final_df = final_df.dropna(subset=["english"])
            
            # Export strictly the 'english' column to match your original layout
            df_excel = final_df[["english"]]
            df_excel.to_excel(output_excel, index=False) # type: ignore
            
            print("Excel file created successfully!")
            print(f"Output file path: {output_excel}")
            print(f"Total text chunks extracted: {len(df_excel)}")
            
            # Optional: Clean up checkpoint file after successful compilation
            # os.remove(progress_csv)
            
        except Exception as e:
            print(f"Could not generate Excel file from progress backup: {e}")

if __name__ == "__main__":
    main()