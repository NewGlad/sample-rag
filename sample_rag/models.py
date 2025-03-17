
from pydantic import BaseModel


# Pydantic class for structural representation for each PDF document (AI-generated)
class Item(BaseModel):
    # Product Information
    product_name: str
    product_family: str
    color_temperature: str          # e.g., "~6000 K (Daylight)"
    power_range: str                  # e.g., "450…10,000 W"
    color_rendering_index: str         # e.g., "High (Ra > ...)"
    description: str

    # Product Family Advantages (List of Advantages)
    advantages: str

    # Application Areas (List of Areas)
    application_areas: str

    # Technical Data (Electrical, Dimensions, Operating, etc.)
    rated_current: float              # in Amperes (e.g., 75.00 A)
    current_control_min: float          # lower bound (e.g., 50 A)
    current_control_max: float          # upper bound (e.g., 85 A)
    rated_power: float                  # in Watts (e.g., 2000.00 W)
    rated_voltage: float                # in Volts (e.g., 25.0 V)
    diameter: float                     # in mm (e.g., 46.0 mm)
    length: float                       # in mm (e.g., 236.0 mm)
    length_excluding_base: float        # in mm (e.g., 220.0 mm)
    light_center_length: float          # in mm (e.g., 95.0 mm)
    electrode_gap: float                # in mm (e.g., 5.0 mm)
    product_weight: float               # in grams (e.g., 391.00 g)
    cable_length: float                 # in mm (e.g., 265.0 mm)
    max_ambient_temperature: float      # in °C (e.g., 230 °C)
    lifespan: float                     # in hours (e.g., 2000 h)
    anode_socket: str                 # e.g., "SK27/50"
    cathode_socket: str               # e.g., "SFcX27-8"

    # Environmental Information
    reach_declaration_date: str         # e.g., "10-02-2023"
    primary_product_number: str         # e.g., "4008321082077"
    candidate_substance: str            # e.g., "Lead"
    candidate_substance_cas: str        # e.g., "7439-92-1"
    scip_declaration_number: str        # e.g., "d7d8f0b3-9cce-48bc-b9a2-a440e89f5b64"

    # Country-Specific Information
    ean: str                            # e.g., "4008321082077"
    metel_code: str                     # e.g., "OSRXBO2000SHSCOFR"

    # Packaging Information
    packaging_product_code: str         # e.g., "4008321082077"
    packaging_product_name: str         # e.g., "XBO 2000 W/SHSC OFR"
    packaging_unit: int                 # Pieces per unit (e.g., 1)
    dimension_length: float             # in mm (e.g., 410 mm)
    dimension_width: float              # in mm (e.g., 184 mm)
    dimension_height: float             # in mm (e.g., 180 mm)
    volume: float                       # in dm³ (e.g., 13.58 dm³)
    gross_weight: float                 # in grams (e.g., 955.00 g)
