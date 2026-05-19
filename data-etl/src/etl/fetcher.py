import requests
import zipfile
import io
import re
import logging
from geojson import load
from src.config.settings import settings

logger = logging.getLogger(__name__)

def fetch_metadata():
    response = requests.get(settings.data_api_url)
    response.raise_for_status()
    return response.json()


def fetch_geojson():
    logger.info(f"Fetching GeoJSON ZIP from {settings.geojson_url}")
    response = requests.get(settings.geojson_url)
    response.raise_for_status()
    
    filename_pattern = r"Building_Outline_Public_v\d+_Building_converted\.geojson"
    
    with zipfile.ZipFile(io.BytesIO(response.content)) as z:
        filenames = z.namelist()
        geojson_filename = next((f for f in filenames if re.match(filename_pattern, f)), None)
        
        if not geojson_filename:
            logger.error("Target GeoJSON file not found in ZIP")
            raise FileNotFoundError("GeoJSON file not found in zip")
        
        logger.info(f"Extracting {geojson_filename}")
        with z.open(geojson_filename) as f:
            return load(f)

