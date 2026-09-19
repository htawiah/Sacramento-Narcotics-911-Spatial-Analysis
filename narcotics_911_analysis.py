"""
Narcotics-Related 911 Call Spatial Analysis
Sacramento, California

Purpose:
Use Python and ArcPy to identify narcotics-related 911 calls,
analyze their spatial distribution across neighborhoods, and
summarize incident frequency by day of the week.
"""

import arcpy
from collections import Counter

# ------------------------------------------------------------
# WORKSPACE
# ------------------------------------------------------------

gdb = r"PATH_TO_YOUR\Sacramento_911_Analysis.gdb"
arcpy.env.workspace = gdb
arcpy.env.overwriteOutput = True

calls = "911_Calls"
neighborhoods = "Neighborhoods"

# ------------------------------------------------------------
# SELECT NARCOTICS-RELATED CALLS
# ------------------------------------------------------------

calls_layer = "calls_layer"

arcpy.management.MakeFeatureLayer(
    calls,
    calls_layer
)

# Select records classified as narcotics-related incidents.
arcpy.management.SelectLayerByAttribute(
    calls_layer,
    "NEW_SELECTION",
    "CALLTYPE = 'Narcotics'"
)

narcotics_calls = "Narcotics_911_Calls"

arcpy.management.CopyFeatures(
    calls_layer,
    narcotics_calls
)

call_count = int(
    arcpy.management.GetCount(narcotics_calls)[0]
)

print(f"Narcotics-related 911 calls identified: {call_count}")

# ------------------------------------------------------------
# SPATIAL ANALYSIS BY NEIGHBORHOOD
# ------------------------------------------------------------

neighborhood_layer = "neighborhood_layer"

arcpy.management.MakeFeatureLayer(
    neighborhoods,
    neighborhood_layer
)

arcpy.management.SelectLayerByLocation(
    neighborhood_layer,
    "INTERSECT",
    narcotics_calls
)

selected_neighborhoods = "Neighborhoods_With_Narcotics_Calls"

arcpy.management.CopyFeatures(
    neighborhood_layer,
    selected_neighborhoods
)

neighborhood_count = int(
    arcpy.management.GetCount(selected_neighborhoods)[0]
)

print(
    f"Neighborhoods containing narcotics-related calls: "
    f"{neighborhood_count}"
)

# ------------------------------------------------------------
# SUMMARIZE INCIDENTS BY DAY OF WEEK
# ------------------------------------------------------------

day_counts = Counter()

with arcpy.da.SearchCursor(
    narcotics_calls,
    ["DAY_OF_WEEK"]
) as cursor:

    for row in cursor:
        if row[0]:
            day_counts[row[0]] += 1

print("\nNarcotics-related calls by day of week:")

for day, count in sorted(day_counts.items()):
    print(f"{day}: {count}")

# ------------------------------------------------------------
# FINAL SUMMARY
# ------------------------------------------------------------

print("\nAnalysis complete.")
print(f"Total narcotics-related calls: {call_count}")
