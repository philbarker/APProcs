import csv

class APProcs(list):
    """ The application profile as a list of dicts, one for each statement, and methods and methods to read, display and process that AP.
    """

    def __init__(self, infile):
        if (infile):
            self.read_input(infile)
        else:
            print("no input file specified")
        return

    def read_input(self, infile):
        """read a csv into list of dicts, one for each row in csv except for first row which is used as keys."""
        with open(infile) as csvfile:
            apreader = csv.DictReader(csvfile)
            last_entity = ''
            last_type=''
            for row in apreader:
                if (row['Type']):
                    last_type = row['Type']
                else:
                    row['Type'] = last_type
                if ('entity' == row['Type'].lower()):
                    last_entity = row['ID']
                else:
                    row['on entity'] = last_entity
                self.append(row)
        return

    def dump(self):
        """print key: value pairs for all dicts"""
        for row in self :
            for key in row.keys():
                print(key+', '+row[key])
            print('-----')
        return
