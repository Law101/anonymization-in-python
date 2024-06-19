import pandas as pd
import random
import string
import logging
import json
from concurrent.futures import ProcessPoolExecutor, as_completed
from typing import Tuple, Dict, List
from anonymization_utils import anonymize_column

# configure basic logging
logging.basicConfig(level=logging.INFO)

def anonymize(dataset: pd.DataFrame, columns_to_anonymize: list) -> Tuple[pd.DataFrame, Dict[str, Dict[str, str]]]:
    anonymize_dataset, anonymization_map = None, None
    
    # Implement the anonymization logic here

    # Check if the columns to be anonymized are present in the dataframe
    if not set(columns_to_anonymize).issubset(dataset.columns):
        raise ValueError('One or more columns not present in the dataset provided! Column(s) mismatch')

    # Recreate expected result with datatype
    anonymize_dataset = dataset.copy()
    anonymization_map = {}

    # Create a salt for hashing values
    salt = ''.join(random.choices(string.ascii_letters + string.digits, k=16))

    # Run anonymization in parrallel to effectively handle even large data
    with ProcessPoolExecutor() as executor:
        future_to_column = {
            executor.submit(anonymize_column, anonymize_dataset[column].tolist(), salt): column for column in columns_to_anonymize
        }
        for future in as_completed(future_to_column):
            column = future_to_column[future]
            try:
                anonymized_column, value_to_anonymize = future.result()
                anonymize_dataset[column] = anonymized_column
                anonymization_map[column] = value_to_anonymize
            except Exception as e:
                logging.error(f"An error occurred while processing column {column}: {e}")
                raise
    logging.info('Anonymization completed successfully!')
    
    # Save data
    anonymize_dataset.to_csv('anonymize_dataset.csv', index=False)
    json.dump(anonymization_map, open( "anonymization_map.json", 'w' ) )
    return anonymize_dataset, anonymization_map


def unanonymize(anonymized_dataset: pd.DataFrame, anonymization_map: Dict[str, Dict[str, str]]) -> pd.DataFrame:
    dataset = None
    
    # Implement the unanonymization logic here

    # Check if columns are present in both input data
    if not set(anonymization_map.keys()).issubset(anonymized_dataset.columns):
        raise ValueError('Could not unanonymize data due to column(s) mismatch!')
    dataset = anonymized_dataset.copy()

    # Unanonymize the data based on the map
    for column, anon_map in anonymization_map.items():
        anonymized_to_value = {v: k for k, v in anon_map.items()}
        dataset[column] = anonymized_dataset[column].map(anonymized_to_value)
    logging.info('Unanonymization completed successfully.')
    dataset.to_csv('unanonymize_dataset.csv', index=False)
    return dataset


if __name__ == '__main__':
    # Define the columns to anonymize
    columns_to_anonymize = ['email', 'credit_card', 'phone_number']

    # Read the data to be anonymized
    customer_data = pd.read_csv('customer_data.csv')

    # Annonymize the dataset
    anonymize_dataset_1, anonymization_map_1 = anonymize(customer_data, columns_to_anonymize)

    # Unanonymize the data
    dataset = unanonymize(anonymize_dataset_1, anonymization_map_1)