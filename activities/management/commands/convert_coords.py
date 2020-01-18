# Run reset.sh to rebuild the database if you also need that done.
from django.core.management.base import BaseCommand
from django.db import connection
from haversine import haversine, Unit

class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        # Recreate our conversion table and index
        with connection.cursor() as cursor:
            cursor.execute("DELETE FROM activities_activitydistrictdistance")
            cursor.execute("SELECT id, postcode, latitude, longitude FROM distcitlatlng")
            districts = cursor.fetchall()

            cursor.execute("SELECT id, address_postcode FROM activities_activity")
            rows = cursor.fetchall()
            for activity in rows:
                activity_id = activity[0]
                postcode = activity[1]

                # Insert a space if there isn't one
                index = postcode.find(" ")
                if index == -1:
                    postcode = postcode[:len(postcode) - 3] + " " + postcode[len(postcode) - 3:]

                print(postcode)
                cursor.execute("SELECT latitude, longitude FROM postcodelatlng WHERE postcode=%s", [postcode])
                postcode_latlng = cursor.fetchone()
                lat = postcode_latlng[0]
                lng = postcode_latlng[1]

                if postcode_latlng:
                    cursor.execute("UPDATE activities_activity SET address_latitudinal=%s, address_longitudinal=%s,address_postcode=%s  WHERE id=%s", [lat, lng, postcode, activity_id])
                else:
                    print("No mapping found for postcode %s - this activity won't show up in any searches" % (postcode))


                print("Now calculating distance to all disctricts for postcode %s with lat %f and long %f" % (postcode, lat, lng))
                i = 0
                for district in districts:
                    distance = haversine((lat, lng), (district[2], district[3]), unit=Unit.KILOMETERS)
                    cursor.execute("INSERT INTO activities_activitydistrictdistance (postcode, distance, activity_id) VALUES (%s, %s, %s)", [district[1], distance, activity_id])
                    i = i + 1

                print("Calculated %i distances to lat/long coords for activity %d" % (i, activity_id))

