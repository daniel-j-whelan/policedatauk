import asyncio
from api.police import PoliceAPI
from utils.dataframe import crime_reports_to_df, crimes_with_outcomes_to_df
import polars as pl


async def test_crimes():
    police = PoliceAPI()
    # postcode = "yo253yq"
    postcode = str(input("Please enter your postcode: "))
    postcode_info = await police.postcodes.get_postcode_info(postcode)
    print(postcode_info)
    # crime_date = "2024-01"
    crime_date = str(input("Please enter a date (YYYY-MM): "))
    poly_crimes = await police.crimes.get_crimes_by_location(
        lat=postcode_info.latitude,
        lon=postcode_info.longitude,
        radius=3000,
        date=crime_date,
    )
    df = crime_reports_to_df(poly_crimes)
    for id in [*df["persistent_id"]]:
        full_crime = await police.crimes.get_crime_by_id(id)
        with pl.Config(tbl_cols=-1):
            print(crimes_with_outcomes_to_df(full_crime, id))


async def test_forces():
    police = PoliceAPI()
    forces = await police.forces.get_all_forces()
    for force in forces[10:13]:  # Test some that contain actual people
        full_force = await police.forces.get_force(force.id)
        print(full_force)
        people = await police.forces.get_people(force.id)
        for person in people:
            print(person)


async def test_neighbourhood():
    test_force = "lincolnshire"
    police = PoliceAPI()
    neighbourhoods = await police.neighbourhoods.get_all_neighbourhoods(test_force)
    print(neighbourhoods[0])
    neighbourhood_staff = await police.neighbourhoods.get_people(
        test_force, neighbourhoods[0].id
    )
    for person in neighbourhood_staff:
        print(person)
    _, polygon = await police.neighbourhoods.get_boundary(
        test_force, neighbourhoods[0].id
    )
    # print(geojson_boundary)
    print(polygon)
    crimes = await police.crimes.get_crimes_by_location(poly=polygon, date="2024-01")
    for crime in crimes:
        print(crime)


async def test_all():
    police = PoliceAPI()
    postcode = input("Please enter your postcode: ").lower().replace(" ", "")
    postcode_info = await police.postcodes.get_postcode_info(postcode)
    print("Details of your postcode: ")
    print(postcode_info)
    neighbourhood_result = await police.neighbourhoods.locate_neighbourhood(
        lat=postcode_info.latitude, lon=postcode_info.longitude
    )
    print("Your local force: ")
    print(neighbourhood_result.force)
    print("Your local neighbourhood ID: ")
    print(neighbourhood_result.neighbourhood)
    neighbourhood_detailed = await police.neighbourhoods.get_neighbourhood(
        neighbourhood_result.force, neighbourhood_result.neighbourhood
    )
    print("Your local neighbourhood name: ")
    print(neighbourhood_detailed.name)
    print("Staff in your area: ")
    neighbourhood_staff = await police.neighbourhoods.get_people(
        neighbourhood_result.force, neighbourhood_result.neighbourhood
    )
    for person in neighbourhood_staff:
        print(person)
    geojson_boundary, polygon = await police.neighbourhoods.get_boundary(
        neighbourhood_result.force, neighbourhood_result.neighbourhood
    )
    print("Boundary of your area for mapping tools: ")
    print(geojson_boundary)

    crimes = await police.crimes.get_crimes_by_location(poly=polygon, date="2024-01")
    for crime in crimes:
        print(crime)


asyncio.run(test_all())
