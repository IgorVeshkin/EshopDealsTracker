from sqlalchemy import create_engine

from sqlalchemy.orm import sessionmaker

from SQLAlchemy_Core.models import Base, ProductInstance


if __name__ == "__main__":
    engine = create_engine('sqlite:///EshopDealsTrackerBasicDB.db', echo=False)

    Base.metadata.create_all(engine)

    session = sessionmaker(bind=engine)()

    while True:

        product_uuid = input(f"Введите uuid записи продукта, которую хотите удалить: ")

        product_record = session.query(ProductInstance).filter(ProductInstance.uuid == product_uuid).first()

        print("Запись продукта в таблице была успешно найдена...." if product_record else "Запись не была найдена....")

        if product_record:
            break

    session.delete(product_record)
    session.commit()

    print("Запись продукта была успешно удалена....")
