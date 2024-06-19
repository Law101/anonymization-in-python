from faker import Faker
import pandas as pd
from uuid import uuid4
import logging
 
fake = Faker()
Faker.seed(2024)

# configure basic logging
logging.basicConfig(level=logging.INFO)
 
def fake_data_generator(x):
    '''
    Function for generating fake customer data
    '''
    data = pd.DataFrame()
    for i in range(0, x):
        data.loc[i,'user_id']= uuid4()
        data.loc[i,'name']= fake.name()
        data.loc[i,'email']= fake.email(safe=False)
        data.loc[i,'residential_address']= fake.address()
        data.loc[i,'credit_card']= str(fake.credit_card_number())
        data.loc[i,'phone_number']= str(fake.phone_number())
    logging.info(f"Successfuly generated data of {x} customers")
    return data
   


if __name__ == '__main__':
    customer_data = fake_data_generator(10000)
    logging.info("Saving generated data to .CSV ......................")
    customer_data.to_csv('customer_data.csv', index=False)
    logging.info("Completed!")
