"""

.. module:: wdt
     :synopsis: Tools for conducting FOM studies of the weighted delta-tracking
                method. Can be extended for any other parametric study conducted
                in Serpent

.. moduleauthor:: Joshua Rehak <jsrehak@berkeley.edu>

"""
import numpy as np
import os, sys
import core

class SerpentRun():
    """ An object containing multiple :class:`analysis.core.DataFile`
    generated by a single run of Serpent. All `res.m` files in a
    directory can be ingested, or only a portion.
    
    :param directory: location where the Serpent output files are
    :type location: string

    :param params: A list of the parameters for this run. Each must
                   be a tuple in the form (parameter name, value). This
                   is optional and is best used in a parametric study.
    :type params: list(tuple)

    :param verb: if True, prints the name of each file uploaded
    :type verb: bool
    """
    def __init__(self, directory, params = [], verb=False):
        # Verify location exists
        abs_location = os.path.abspath(os.path.expanduser(directory))
        assert os.path.exists(abs_location), "Folder does not exist"

        # Initialize files array
        self.files = []
        
        # Ingest all .m files
        for filename in [x for x in os.listdir(abs_location) if x[-2:] == '.m']:
            if verb: print("Uploading: " + filename)
            self.files.append(core.DataFile(abs_location + '/' +
                                            filename))

        # Sort files based on cycle number
        self.files.sort()

        # Attributes
        ## Number of files
        self.n = len(self.files)
        assert self.n > 0, "No .m files in that location"

        ## Cycles
        self.cycles = []
        
        ## Parameter list
        if type(params) is not list: params = [ params ]
        if len(params):
            assert all(isinstance(x, tuple) for x in params), \
                "Parameters must be tuples"
        self.params = params

        ## Original location
        self.loc = abs_location
        
        print("Uploaded " + str(self.n) + " files.")

    def __str__(self):
        # Print information about the run
        ret_str = str(self.n) + ' .m files uploaded from: ' + self.loc\
                  + '\n' + 'Parameters:\n'
        for tup in self.params:
            ret_str += '\t' + str(tup[0]) + ':\t' + str(tup[1]) + '\n'
        return ret_str[:-1]

    def get_error(self, label, grp):
        """ Returns an array with the value or error for a given
        Serpent 2 output parameter and group number

        :param label: Serpent 2 output parameter
        :type label: string

        :param grp: The energy group of interest or the location in the
                    flattened matrix. This is ENERGY GROUP not the entry
                    in the vector.
        :type grp: int

        """
        return np.array([file.get_data(label, err=True)[0][grp - 1]
                         for file in self.files])
        
