from enum import Enum
import csv
import os
import pathlib

PROJECT_ROOT = pathlib.Path(__file__).parent.absolute()

class OutputFormat(Enum):
    """
    Enum representing supported output formatting options for search results.
    """
    display = 'display'
    csv_file = 'csv_file'

    @staticmethod
    def list():
        """
        :return: list of string representations of OutputFormat enums
        """
        return list(map(lambda output: output.value, OutputFormat))


class NEOWriter(object):
    """
    Python object use to write the results from supported output formatting options.
    """

    def __init__(self):
        # TODO: How can we use the OutputFormat in the NEOWriter?
        pass

    def write(self, format, data, **kwargs):
        """
        Generic write interface that, depending on the OutputFormat selected calls the
        appropriate instance write function

        :param format: str representing the OutputFormat
        :param data: collection of NearEarthObject or OrbitPath results
        :param kwargs: Additional attributes used for formatting output e.g. filename
        :return: bool representing if write successful or not
        """
        # TODO: Using the OutputFormat, how can we organize our 'write' logic for output to stdout vs to csvfile
        # TODO: into instance methods for NEOWriter? Write instance methods that write() can call to do the necessary
        # TODO: output format.

        output_options = OutputFormat.list()
        if format in output_options:
            # Display in the console
            if format == "display":
                if not data:
                    print("No Data to Display :(")
                else:
                    for row in data:
                        print(row)
            # Write to the CSV file
            elif format == "csv_file":
                if not data:
                    print("No Data to Write :(")
                else:
                    output_type = type(data[0]).__name__
                    # Write NearEarthObject Object
                    if output_type == "NearEarthObject":
                        output_filename = f'{PROJECT_ROOT}/data/neo_output.csv'
                        print("Writing data to: {}".format(output_filename))
                        header = ["Neo Id", "Neo Name", "Orbits", "Orbit Date"]
                        with open(output_filename, mode='w') as neo_file:
                            neo_writer = csv.writer(neo_file, delimiter=',')
                            neo_writer.writerow(header)
                            for row in data:
                                neo_writer.writerow([str(row.id), str(row.name), str(len(row.orbits)), str(", ".join(map(lambda o: o.close_approach_date, row.orbits)))])
                        print("Written data to: {}".format(output_filename))
                    # Write OrbitPath Object
                    elif output_type == "OrbitPath":
                        output_filename = f'{PROJECT_ROOT}/data/neo_output.csv'
                        print("Writing data to: {}".format(output_filename))
                        header = ["Neo Name", "Miss Distance (km)", "Orbit Date"]
                        with open(output_filename, mode='w') as orbit_file:
                            orbit_writer = csv.writer(orbit_file, delimiter=',')
                            orbit_writer.writerow(header)
                            for row in data:
                                orbit_writer.writerow([str(row.neo_name), str(row.miss_distance_kilometers), str(row.close_approach_date)])
                        print("Written data to: {}".format(output_filename))

            return True
        else:
            raise Exception("format: `{}` not supported. Available format: `{}`".format(str(format), str(", ".join(output_options))))