import re
import csv

def parse_vocabulary_to_csv(input_file_path: str, output_csv_path: str) -> None:
    try:
        with open(input_file_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()

        cleaned_lines: list[str] = []
        buffer_line: str = ""

        # Step 1: Clean and reconstruct broken lines
        for line in lines:
            line = line.strip()
            if not line:
                continue
                
            # Skip page numbers, book titles, and category headers
            if any(header in line for header in ["MANIPURI GRAMMAR", "The Universe", "Mankind.", "Relations."]):
                continue
            
            # If the line does not start with an English word/number, it belongs to the previous line
            if buffer_line and not re.match(r'^[A-Za-z\d]', line):
                buffer_line += " " + line
            else:
                if buffer_line:
                    cleaned_lines.append(buffer_line)
                buffer_line = line
        if buffer_line:
            cleaned_lines.append(buffer_line)

        # Explicitly typing the list of lists to prevent partially unknown types
        structured_data: list[list[str]] = []

        # Step 2: Extract English, Bengali Script, and Transliteration via Regex
        pattern = re.compile(
            r'^([A-Za-z\s()-]+?)\s+([\u0980-\u09FF\sঃ।\u200c\u200d]+)\s+([A-Za-z\s\d.,·\u00C2\u00E2\u00EE\u00F4\u00FB-]+)$'
        )

        for line in cleaned_lines:
            # Strip accidental leading numbering (e.g. '12 MANIPURI' remnants)
            line = re.sub(r'^\d+\s+', '', line)
            
            match = pattern.match(line)
            if match:
                english = match.group(1).strip()
                meitei_bengali = match.group(2).strip()
                transliteration = match.group(3).strip().rstrip('.') # Remove trailing period
                
                structured_data.append([english, meitei_bengali, transliteration])
            else:
                # Fallback: if regex match fails slightly, try splitting by double spaces
                parts = re.split(r'\s{2,}', line)
                if len(parts) >= 3:
                    structured_data.append([parts[0].strip(), parts[1].strip(), parts[2].strip().rstrip('.')])

        # Step 3: Write cleanly to CSV
        with open(output_csv_path, 'w', encoding='utf-8', newline='') as csv_file:
            writer = csv.writer(csv_file)
            # CSV Headers
            writer.writerow(["English", "Meiteilon (Bengali Script)", "Transliteration"])
            writer.writerows(structured_data)

        print(f"Success! Processed {len(structured_data)} entries.")
        print(f"CSV file saved at: {output_csv_path}")

    except FileNotFoundError:
        print(f"Error: Could not find the file '{input_file_path}'")
    except Exception as e:
        print(f"An error occurred: {e}")

def main() -> None:
    input_filename: str = "vocabulary.txt"
    output_filename: str = "meitei_dictionary.csv"
    
    print(f"Parsing data from '{input_filename}'...")
    parse_vocabulary_to_csv(input_filename, output_filename)

if __name__ == "__main__":
    main()