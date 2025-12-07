from sqlalchemy.orm import relationship

from sqlalchemy import Column, String, Float, LargeBinary, ForeignKey, DateTime, func

from sqlalchemy.orm import declarative_base


Base = declarative_base()


import uuid as _uuid

class ProductInstance(Base):
    __tablename__ = "Product"

    uuid = Column(String(36), primary_key = True, nullable=False)
    name = Column(String(256), nullable=False)
    description = Column(String(1024), nullable=False)
    image = Column(LargeBinary, nullable=True)
    price = Column(Float(), nullable=False)
    priceCurrency = Column(String(16), nullable=False)
    gameEdition = Column(String(64), nullable=False)
    applicationCategory = Column(String(64), nullable=False)
    url = Column(String(1024), nullable=False)
    publisher_uuid = Column(String(36), ForeignKey("Publisher.uuid"))
    publisher = relationship("PublisherInstance", back_populates="product")
    description_images = relationship("DescriptionImageInstance", back_populates="product", cascade='all, delete')
    created_at = Column(DateTime, default=func.now(), nullable=False)

    def __init__(self, name, description, image, price, price_currency, game_edition, application_category, url, publisher_uuid, uuid=None, **kwargs):
        if not uuid:
            uuid = str(_uuid.uuid4().hex)

        super().__init__(uuid=uuid, **kwargs)

        self.name = name
        self.description = description
        self.image = image
        self.price = price
        self.priceCurrency = price_currency
        self.gameEdition = game_edition
        self.applicationCategory = application_category
        self.url = "nintendo.com" + url
        self.publisher_uuid = publisher_uuid



class PublisherInstance(Base):
    __tablename__ = "Publisher"

    uuid = Column(String(36), primary_key=True)
    name = Column(String(256), nullable=False)
    created_at = Column(DateTime, default=func.now(), nullable=False)

    product = relationship("ProductInstance", back_populates="publisher")

    def __init__(self, name, uuid=None, **kwargs):
        if not uuid:
            uuid = str(_uuid.uuid4().hex)

        super().__init__(uuid=uuid, **kwargs)

        self.name = name


class DescriptionImageInstance(Base):
    __tablename__ = "DescriptionImage"

    uuid = Column(String(36), primary_key=True, nullable=False)
    name = Column(String(256), nullable=False)
    description = Column(String(1024), nullable=False)
    contentUrl = Column(String(1024), nullable=False)
    productId = Column(String, ForeignKey("Product.uuid"))
    product = relationship("ProductInstance", back_populates="description_images")

    def __init__(self, name, description, contentUrl, product_id, uuid=None, **kwargs):
        if not uuid:
            uuid = str(_uuid.uuid4().hex)

        super().__init__(uuid=uuid, **kwargs)

        self.name = name
        self.description = description
        self.contentUrl = contentUrl
        self.productId = product_id