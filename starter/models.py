class NearEarthObject(object):
    """
    Object containing data describing a Near Earth Object and it's orbits.

    # TODO: You may be adding instance methods to NearEarthObject to help you implement search and output data.
    """

    def __init__(self, **kwargs):
        """
        :param kwargs:    dict of attributes about a given Near Earth Object, only a subset of attributes used
        """
        # TODO: What instance variables will be useful for storing on the Near Earth Object?
        self.id = kwargs["id"]
        self.name = kwargs["name"]
        self.diameter_min_km = float(kwargs["estimated_diameter_min_kilometers"])
        self.diameter_max_km = float(kwargs["estimated_diameter_max_kilometers"])
        self.diameter_min_meter = float(kwargs["estimated_diameter_min_meters"])
        self.diameter_min_meter = float(kwargs["estimated_diameter_max_meters"])
        self.diameter_min_miles = float(kwargs["estimated_diameter_min_miles"])
        self.diameter_max_miles = float(kwargs["estimated_diameter_max_miles"])

        # Handling boolean `is_potentially_hazardous_asteroid`
        self.is_potentially_hazardous_asteroid = None
        if str(kwargs["is_potentially_hazardous_asteroid"]) in ["False", "FALSE", "false"]:
            self.is_potentially_hazardous_asteroid = False
        elif str(kwargs["is_potentially_hazardous_asteroid"]) in ["True", "TRUE", "true"]:
            self.is_potentially_hazardous_asteroid = True
        self.orbits = []  # Storing OrbitPath information

    def __str__(self):
        return "Neo Id: {} Neo Name: {} Orbits: {} Orbit Date: {}".\
            format(str(self.id), str(self.name), str(len(self.orbits)), str(", ".join(map(lambda o: o.close_approach_date, self.orbits))))

    def update_orbits(self, orbit, overwrite):
        """
        Adds an orbit path information to a Near Earth Object list of orbits

        :param overwrite: boolean flag to indicate whether to overwrite old orbits or append to old orbits
        :param orbit: OrbitPath
        :return: None
        """

        # TODO: How do we connect orbits back to the Near Earth Object?
        if overwrite:
            self.orbits = orbit
        else:
            self.orbits.append(orbit)


class OrbitPath(object):
    """
    Object containing data describing a Near Earth Object orbit.

    # TODO: You may be adding instance methods to OrbitPath to help you implement search and output data.
    """

    def __init__(self, **kwargs):
        """
        :param kwargs:    dict of attributes about a given orbit, only a subset of attributes used
        """
        # TODO: What instance variables will be useful for storing on the Near Earth Object?
        self.neo_id = kwargs["id"]
        self.neo_name = kwargs["name"]
        self.orbiting_body = kwargs["orbiting_body"]
        self.close_approach_date = kwargs["close_approach_date"]
        self.miss_distance_kilometers = float(kwargs["miss_distance_kilometers"])
        self.miss_distance_miles = float(kwargs["miss_distance_miles"])

    def __str__(self):
        return "Neo Name: {} Miss Distance (km): {} Orbit Date: {}".\
            format(str(self.neo_name), str(self.miss_distance_kilometers), str(self.close_approach_date))
