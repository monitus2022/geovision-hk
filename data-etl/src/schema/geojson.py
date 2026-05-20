from typing import Any

def validate_geojson(data: Any):
    """
    Validates that the provided data is a list of GeoJSON features 
    based on the structure in tests/fixtures/geojson.json.
    """
    if not isinstance(data, list):
        raise ValueError("GeoJSON must be a list of features")
    
    for feature in data:
        if not isinstance(feature, dict):
            raise ValueError("Feature must be a dictionary")
        if feature.get("type") != "Feature":
            raise ValueError("Feature type must be 'Feature'")
        if "geometry" not in feature or "properties" not in feature:
            raise ValueError("Feature must have geometry and properties")
        
        properties = feature.get("properties", {})
        required_properties = [
            "OBJECTID", "Shape_Length", "Shape_Area", "GeoRefNo", 
            "DateCreate", "BuildingCSUID", "BuildingID", 
            "Status", "DateStamp"
        ]
        
        for prop in required_properties:
            if prop not in properties:
                raise ValueError(f"Feature property missing required field: {prop}")
                
    return True
