import shippo
from django.conf import settings
from shippo.models import components


shippo_sdk = shippo.Shippo(api_key_header=settings.SHIPPO_SECRET_KEY)

class DeliveryShippo():
    def __init__(self, name, street1, city, state, zip, country):
        self.name = name
        self.street1 = street1
        self.city = city
        self.state = state
        self.zip = zip
        self.country = country
        self.address_from = None
        self.address_to = None
        self.parcel = None
        self.shipment = None
        self.rate_id = None
    
    def create_address_from(self):
        self.address_from = shippo_sdk.addresses.create(components.AddressCreateRequest(
            name=settings.SHIPPING_ADDRESS_PERSON_NAME,
            street1=settings.SHIPPING_ADDRESS_STREET,
            city=settings.SHIPPING_ADDRESS_CITY,
            state=settings.SHIPPING_ADDRESS_STATE,
            zip=settings.SHIPPING_ADDRESS_ZIP,
            country=settings.SHIPPING_COUNTRY,
            phone=settings.SHIPPING_PHONE_NUMBER,
            email=settings.SHIPPING_EMAIL
        ))
    
        
    def create_address_to(self):
        self.address_to = shippo_sdk.addresses.create(components.AddressCreateRequest(
                name=self.name,
                street1=self.street1,
                city=self.city,
                state=self.state,
                zip=self.zip,
                country=self.country
            ))
        
    def create_parcel(self):
        self.parcel = shippo_sdk.parcels.create(components.ParcelCreateRequest(
                length="5",
                width="5",
                height="5",
                distance_unit=components.DistanceUnitEnum.IN,
                weight="2",
                mass_unit=components.WeightUnitEnum.LB
            ))
        
    def create_shipment(self):
        self.shipment = shippo_sdk.shipments.create(
                components.ShipmentCreateRequest(
                    address_from=self.address_from,
                    address_to=self.address_to,
                    parcels=[self.parcel],
                    async_=False
                ))
        
        return self.shipment
    
    def create_transaction(self):
        transaction = shippo_sdk.transactions.create(
            components.TransactionCreateRequest(
                rate=self.rate_id,
                label_file_type=components.LabelFileTypeEnum.PDF,
                async_=False
            )
        )
        
        return transaction
        
delivery_shippo = DeliveryShippo(name=None, street1=None, city=None, state=None, zip=None, country=None)
                    