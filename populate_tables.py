from tester import *
from faker import Faker
from itertools import product
#initialze database
fake = Faker()

def add_stores():
    for i in range(100):
        store = Store(
            name = fake.company(),
            address = fake.street_address(),
            type = fake.url(),
            )
        session.add(store)
    session.commit()

def add_products():
    for i in range(100):
        product = Product(
            name = fake.name(),
            description = fake.paragraph(nb_sentences = 3),
            image = fake.file_name(category='image'),
            msrp = 19.95
            #msrp = fake.pricetag(),
            )
        session.add(product)
    session.commit()
#populate tables
add_stores()
add_products()
