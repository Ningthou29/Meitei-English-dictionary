import pdfplumber
import csv
import os

def pdf_to_csv(pdf_path: str, csv_path: str):
    data: list[dict[str, str]] = []
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            text = page.extract_text()
            if text:
                lines = text.split('\n')
                for line in lines:
                    if ':' in line:
                        key, value = line.split(':', 1)
                        data.append({'Key': key.strip(), 'Value': value.strip()})

    if not data:
        print("No data found or PDF format unrecognized.")
        return

    keys = data[0].keys()
    
    with open(csv_path, 'w', newline='', encoding='utf-8') as output_file:
        dict_writer = csv.DictWriter(output_file, fieldnames=keys)
        dict_writer.writeheader()
        dict_writer.writerows(data)

    print(f"Successfully converted {pdf_path} to {csv_path}")

def main():
    print("--- PDF Dictionary to CSV Converter ---")
    
    # Input prompt
    input_pdf = input("Enter the full path to your PDF file: ").strip().replace('"', '')
    
    if not os.path.exists(input_pdf):
        print("Error: The file path provided does not exist.")
        return

    # Output prompt
    output_csv = input("Enter the desired path for the output CSV (e.g., data.csv): ").strip()
    if not output_csv.endswith('.csv'):
        output_csv += '.csv'
    
    # Execution
    pdf_to_csv(input_pdf, output_csv)

if __name__ == "__main__":
    main()