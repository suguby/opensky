Open Sky Measurer
========
Tool for measure distance to goal from geographic coordinates.

Install
========
pip install opensky

Usage
========

```python
from opensky import get_list_of_planes_near_goal
for row in get_list_of_planes_near_goal():
    print('callsign {callsign} longitude {longitude} latitude {latitude} '
          'distance to Paris {distance}'.format(**row))
```

get_list_of_planes_near_goal take three params

* longitude  - longitude of goal place, is sent None - Paris longitude
* latitude   - latitude of goal place, is sent None - Paris latitude
* min_radius - minmal radius from goal place, is sent None - 400 km
* max_radius - maximal radius from goal place, is sent None - 500 km
* ordered    - need order result by distance to goal, default False

get_list_of_planes_near_goal return list of dictionaries with keys

* callsign  - plane callsign
* longitude - plane longitude
* latitude  - plane latitude
* distance  - distance to goal place, km
