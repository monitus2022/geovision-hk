from src.etl import fetch_metadata, fetch_geojson, transform_geojson, load_to_staging, replace_table


def main():
    metadata = fetch_metadata()
    geojson_data = fetch_geojson()
    transformed = transform_geojson(geojson_data)
    load_to_staging(transformed)
    replace_table()


if __name__ == "__main__":
    main()
