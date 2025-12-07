from pathlib import Path
from pprint import pprint

import requests
from sqlalchemy import create_engine

from sqlalchemy.orm import sessionmaker

from SQLAlchemy_Core.models import Base, ProductInstance, PublisherInstance, DescriptionImageInstance

import json


def form_dict(json_data: dict, field_names: list = None) -> dict:
    """
    Функция, позволяет сформировать словарь, оставив только те поля, которые указаны в перечне
    :param json_data: Входящие данные
    :param field_names: Поля, которые будут сохранены
    :return: Словарь отфильтрованных данных
    """
    if field_names is None:
        field_names = ["name", "description", "contentUrl"]

    return {key:value for key, value in json_data.items() if key in field_names}

if __name__ == "__main__":
    engine = create_engine('sqlite:///EshopDealsTrackerBasicDB.db', echo=True)

    Base.metadata.create_all(engine)

    session = sessionmaker(bind=engine)()

    path_to_files = Path('readable_json/')

    first_json = next((file for file in path_to_files.iterdir() if file.is_file() and file.suffix == '.json'), None)

    if first_json:
        with first_json.open("r", encoding="utf-8") as json_file:

            loaded_json = json.load(json_file)

            # ProductInstance
            name = loaded_json['@graph'][0]['name']
            description = loaded_json['@graph'][0]['description']
            image = loaded_json['@graph'][0]['image']
            price = loaded_json['@graph'][0]['offers']['price']
            priceCurrency = loaded_json['@graph'][0]['offers']['priceCurrency']
            url = loaded_json['@graph'][0]['offers']['url']
            gameEdition = loaded_json['@graph'][0]['gameEdition']
            applicationCategory = loaded_json['@graph'][0]['applicationCategory']

            # PublisherInstance
            publisher = loaded_json['@graph'][0]['publisher']['name']

            found_publisher = session.query(PublisherInstance).filter(PublisherInstance.name == publisher).first()

            if not found_publisher:
                publisherInstance = PublisherInstance(name=publisher)

                session.add(publisherInstance)

                session.flush()

            else:
                publisherInstance = found_publisher

            productInstance = ProductInstance(name=name, description=description, image=requests.get(image).content, price=price, price_currency=priceCurrency, game_edition=gameEdition, application_category=applicationCategory, url=url, publisher_uuid=publisherInstance.uuid)

            session.add(productInstance)

            session.flush()

            # DescriptionImageInstance
            DescriptionImageData = [{**form_dict(image_data), 'product_id': productInstance.uuid} for image_data in loaded_json['@graph'][1]]

            pprint(DescriptionImageData)

            DescriptionImageInstances = [DescriptionImageInstance(**image_data) for image_data in DescriptionImageData]

            session.add_all(DescriptionImageInstances)

            session.commit()



    else:
        print("В папке 'readable_json' отсутствуют json-файлы...")

