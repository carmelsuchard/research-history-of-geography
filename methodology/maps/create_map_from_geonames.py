"""
Purpose: Create a map visualization from geonames data.
Creator: Carmel
Date: 2026-08-15
"""

import sys
import os
import requests
import pandas as pd
import geopandas as gpd
import geoplot as gplt


def get_coordinates(geoname_id, username="robert"):
    url = "http://api.geonames.org/getJSON"

    params = {
        "geonameId": geoname_id,
        "username": username
    }

    try:
        r = requests.get(url, params=params)
        r.raise_for_status()  # Raise an error for bad responses
        data = r.json()
        return data.get("lat"), data.get("lng")
    except Exception as e:
        print(f"Error occurred while making the GeoNames request: {e}")
        return None, None


if __name__ == "__main__":
    coords = get_coordinates(2750405)
    geonames_with_coordinates_path = "methodology/maps/thesis_disambiguation_results_with_coordinates.gpkg"
    if not os.path.exists(geonames_with_coordinates_path):
        print(f"File {geonames_with_coordinates_path} does not exist. Creating it now.")

        spatial_path = "methodology/maps/from_thesis_disambiguation_results_with_correct_link.xlsx"
        spatial_df = pd.read_excel(spatial_path)

        spatial_df["x"], spatial_df["y"] = zip(*spatial_df["correct_geonames"].apply(lambda geoname_id: get_coordinates(geoname_id)))

        # Convert to geopackage
        gdf = gpd.GeoDataFrame(spatial_df, geometry=gpd.points_from_xy(spatial_df["x"], spatial_df["y"]))
        print(gdf.head())
        gdf.to_file(geonames_with_coordinates_path, layer="thesis_disambiguation_results", driver="GPKG")

    else: 
        spatial_locations = gpd.read_file(geonames_with_coordinates_path, layer="thesis_disambiguation_results")
        # gplt.pointplot(spatial_locations)