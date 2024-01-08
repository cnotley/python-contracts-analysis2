import csv

def generate_csv(data, file_name):
    """
    Generates a CSV file from the processed data.

    Args:
    data (list of dict): Processed data, where each dict represents a row in the CSV.
    file_name (str): Name of the CSV file to be generated.
    """
    if not data:
        print("No data provided for CSV generation.")
        return

    with open(file_name, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=data[0].keys())

        writer.writeheader()
        for row in data:
            writer.writerow(row)

    print(f"CSV file '{file_name}' generated successfully.")

if __name__ == "__main__":
    processed_data = [
        {'contract_type': 'Type1', 'contract_synopsis': 'Synopsis1', 'id': 1, 'title': 'Title1', 'description': 'Description1', 'quantities': '[{"value": "100", "unit": "units", "frequency": "monthly"}]', 'relevant_party': 'Party1', 'key_term_importance': 9.5, 'total_cost': 1000},
        {'contract_type': 'Type2', 'contract_synopsis': 'Synopsis2', 'id': 2, 'title': 'Title2', 'description': 'Description2', 'quantities': '[{"value": "200", "unit": "units", "frequency": "yearly"}]', 'relevant_party': 'Party2', 'key_term_importance': 8.5, 'total_cost': 2000}
    ]

    generate_csv(processed_data, 'output.csv')
