import os

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from SQLAlchemy_Core.models import Base, ProductInstance

if __name__ == "__main__":

    engine = create_engine('sqlite:///EshopDealsTrackerBasicDB.db', echo=False)

    Base.metadata.create_all(engine)

    session = sessionmaker(bind=engine)()

    images_count = session.query(ProductInstance).count()

    number_of_records = 0

    while True:

        try:
            number_of_records = int(input(f"Введите количество записей, которое необходимо загрузить из базы данных (до {images_count}): "))

            if number_of_records > images_count:
                print("Внимание: Введенное числовое значение превышает количество записей в базе. Будет использованы все записи")
                number_of_records = images_count

        except ValueError:
            print("Внимание: Введите числовое значение....\n")
            continue

        break

    image_records = session.query(ProductInstance).limit(number_of_records).all()

    if not os.path.exists("retrieved_images/"):
        os.makedirs("retrieved_images/")

    if image_records:
        for record in image_records:
            with open(f"retrieved_images/{record.name}.png", "wb") as img:
                img.write(record.image)

        print("Успешно выгружены все изображения обложек!")

    else:
        print("Записи не были найдены в базе данных")