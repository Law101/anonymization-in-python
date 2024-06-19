# Data Anonymization and Unanonymization

## Code structure and implementation

The implementation utilized standard libraries in python aside from Pandas which is use to specificaly for IO operations and Faker for generating fake customer data.

- ``data_generator.py`` is responsible for generating fake customer data (including PII) using the Faker library. This file can be modified to generate even large amount of data, currently the default is set to 10,000.
- ``anonymization_utils.py`` contains utility functions for anonymizing the data. The implementation inlcudes hashing algorithms SHA256 - a highly secured hashing algorithm for encrypting sentive information. A ramdom salt was also reated to add as extra security layer.
- ``main_script.py`` includes both the anonymization and unanonymization functions, each of the function is designed to also save the generated data to disk after specific opeartions. The anoymize function leverage multiprocessing to effectively anonymizing large amount of data.

## How to run the code

- Create a virtual environment and activate the virtual environment
- Install all dependencies from ``requirements.txt`` into the virtual environment.
- Run ``data_generator.py`` to generate fake customer data. The default is 10,000.
- Run ``main_script.py`` to anonymize and unanonymize the fake customer data generated in the preceding step. The default columns for anynonymization are ``['email', 'credit_card', 'phone_number']``.
