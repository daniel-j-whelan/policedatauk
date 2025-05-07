from pydantic import BaseModel, Field
from typing import Dict

class PostCode(BaseModel):
    """Represents a postcode in the UK.

    Args:
        postcode (str): The postcode.

        quality (int): The quality of the postcode.

        eastings (int): The eastings of the postcode.

        northings (int): The northings of the postcode.

        country (str): The country of the postcode.

        nhs_ha (str): The NHS Health Authority of the postcode.

        longitude (float): The longitude of the postcode.

        latitude (float): The latitude of the postcode.
        
        european_electoral_region (str): The European electoral region of the postcode.
        
        primary_care_trust (str): The primary care trust of the postcode.
        
        region (str): The region of the postcode.
        
        lsoa (str): The Lower Layer Super Output Area of the postcode.
        
        msoa (str): The Middle Layer Super Output Area of the postcode.
        
        incode (str): The incode of the postcode.
        
        outcode (str): The outcode of the postcode.
        
        parliamentary_constituency (str): The parliamentary constituency of the postcode.
        
        admin_district (str): The administrative district of the postcode.
        
        parish (str): The parish of the postcode.
        
        administrative_county (str): The administrative county of the postcode.
        
        date_of_introduction (str): The date of introduction of the postcode.
        
        admin_ward (str): The administrative ward of the postcode.
        
        ced (str): The Community and Environment Department of the postcode.
        
        ccg (str): The Clinical Commissioning Group of the postcode.
        
        nuts (str): The Nomenclature of Territorial Units for Statistics of the postcode.
        
        pfa (str): The Police and Fire Authority of the postcode.
        
        codes (dict): The codes of the postcode.
        
    Returns:
        None

    Exceptions:
        ValidationError: If the data is invalid.
    """
    postcode: str = Field(
        ..., description="Postcode.", examples=["HX6 4JT"]
    )
    quality: int = Field(
        ..., description="Quality of the postcode.", examples=[1]
    )
    eastings: int = Field(
        ...,
        description="Eastings of the postcode.",
        examples=[403582],
    )
    northings: int = Field(
        ...,
        description="Northings of the postcode.",
        examples=[419513],
    )
    country: str = Field(
        ...,
        description="Country of the postcode.",
        examples=["England"],
    )
    nhs_ha: str = Field(
        ..., description="NHS Health Authority of the postcode.",
    )
    longitude: float = Field(
        ...,
        description="Longitude of the postcode.",
        examples=[-1.234567],
    )
    latitude: float = Field(
        ...,
        description="Latitude of the postcode.",
        examples=[52.123456],
    )
    european_electoral_region: str = Field(
        ...,
        description="European electoral region of the postcode.",
        examples=["Yorkshire and The Humber"],
    )
    primary_care_trust: str = Field(
        ...,
        description="Primary care trust of the postcode.",
        examples=["Calderdale"],
    )
    region: str = Field(
        ...,
        description="Region of the postcode.",
        examples=["Yorkshire and The Humber"],
    )
    lsoa: str = Field(
        ...,
        description="Lower Layer Super Output Area of the postcode.",
        examples=["Calderdale 027C"],
    )
    msoa: str = Field(
        ...,
        description="Middle Layer Super Output Area of the postcode.",
        examples=["Calderdale 027"],
    )
    incode: str = Field(
        ..., description="Incode of the postcode.", examples=["4JT"]
    )
    outcode: str = Field(
        ..., description="Outcode of the postcode.", examples=["HX6"]
    )
    parliamentary_constituency: str = Field(
        ...,
        description="Parliamentary constituency of the postcode.",
        examples=["Calder Valley"],
    )
    admin_district: str = Field(
        ...,
        description="Administrative district of the postcode.",
        examples=["Calderdale"],
    )
    parish: str = Field(
        ...,
        description="Parish of the postcode.",
        examples=["Leicester"],
    )
    admin_county: str | None = Field(
        None,
        description="Administrative county of the postcode.",
        examples=["West Yorkshire"],
    )
    date_of_introduction: str = Field(
        ...,
        description="Date of introduction of the postcode.",
        examples=["198001"],
    )
    admin_ward: str = Field(
        ...,
        description="Administrative ward of the postcode.",
        examples=["Ryburn"],
    )
    ced: str | None = Field(
        None,
        description="Community and Environment Department of the postcode.",
        examples=["Calderdale"],
    )
    ccg: str = Field(
        ...,
        description="Clinical Commissioning Group of the postcode.",
        examples=["NHS West Yorkshire"],
    )
    nuts: str = Field(
        ...,
        description="Nomenclature of Territorial Units for Statistics of the postcode.",
        examples=["Calderdale"],
    )
    pfa: str = Field(
        ...,
        description="Police and Fire Authority of the postcode.",
        examples=["West Yorkshire"],
    )
    codes: Dict[str, str] = Field(
        ...,
        description="Codes of the postcode.",
        examples=[{"admin_district": "Calderdale", "admin_ward": "Ryburn"}],
    )