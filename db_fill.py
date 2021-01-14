import csv

from models import db, Migrate, User, Dish, Category, Order


def csv_dict_reader(file_obj):
    """
    Read a CSV file using csv.DictReader and add data in data_base
    """
    reader = csv.reader(file_obj)
    for line in reader:
        #print(line["id"], line['title'], line['price'], line['description'], line[picture], line[category_id]),
        print(line)

if __name__ == "__main__":
    with open("delivery_items.csv") as f_obj:
        csv_dict_reader(f_obj)
