from nose.tools import *
import analysis.core as core
import analysis.fom as fom
import numpy as np
import os

class TestClass:

    @classmethod
    def setup_class(cls):
        cls.base_dir = './tests/fom_data/'
        cls.test_analyzer = fom.Analyzer(cls.base_dir)
        cls.cycles = [10, 20, 30]
        cls.cpu    = np.array([10.5, 20.5, 30.5])
        cls.error1  = np.array([0.00030, 0.00020, 0.00010])
        cls.error2  = np.array([0.00032, 0.00022, 0.00012])
        cls.materror11 = np.array([ 0.00030, 0.00020, 0.00010])
        cls.materror12 = np.array([ 0.00032, 0.00022, 0.00012])
        cls.materror21 = np.array([ 0.00034, 0.00024, 0.00014])
        cls.materror22 = np.array([ 0.00036, 0.00026, 0.00016])

    
    def test_fom_file_upload(self):
        """ FOM Analyzer should upload all the correct files in a directory """
        files = self.test_analyzer.get_filenames()
        file_loc = os.path.abspath(self.base_dir) + '/'
        
        eq_(len(files), 3)
        ok_(all([file_loc + e in files for e in ['res_10.m', 'res_20.m', 'res_30.m']]))
        
    @raises(AssertionError)
    def test_fom_bad_location(self):
        """ FOM Analyzer should return an error if a non-existent folder
        is given """
        base_dir = './wrong_file_name/'
        new_analyzer = fom.Analyzer(base_dir)

    def test_fom_good_locations(self):
        """ FOM Analyzer should work for locations without slash"""
        base_dir = './tests/fom_data'
        new_analyzer = fom.Analyzer(base_dir)

    def test_fom_fom_values(self):
        ans    = np.power(self.cpu * np.power(self.error1, 2), -1)
        func   = self.test_analyzer.get_data('TEST_VAL', 1)
        ok_(all([e in func[:,1] for e in ans]))
        ok_(all([c in func[:,0] for c in self.cycles]))

    def test_fom_fom_values_grp(self):
        ans    = np.power(self.cpu * np.power(self.error2, 2), -1)
        func   = self.test_analyzer.get_data('TEST_VAL', 2)
        ok_(all([e in func[:,1] for e in ans]))
        ok_(all([c in func[:,0] for c in self.cycles]))

    def test_fom_fom_values_cpu(self):
        ans    = np.power(self.cpu * np.power(self.error1, 2), -1)
        func   = self.test_analyzer.get_data('TEST_VAL', 1, cycle = False)
        ok_(all([e in func[:,1] for e in ans]))
        ok_(all([c in func[:,0] for c in self.cpu]))

    def test_fom_fom_length(self):
        eq_(np.shape(self.test_analyzer.get_data('TEST_VAL', 1)), (3,2))

    def test_fom_err_values(self):
        func = self.test_analyzer.get_data('TEST_VAL', 1, fom = False)
        ok_(all([e in func[:,1] for e in self.error1]))
        ok_(all([c in func[:,0] for c in self.cycles]))

    def test_fom_err_size(self):
        eq_(np.shape(self.test_analyzer.get_data('TEST_VAL', 1, fom = False)), (3,2))

    def test_fom_fom_multigroup(self):
        """ FOM data should return the correct values for multiple groups """
        ans1   = np.power(self.cpu * np.power(self.error1, 2), -1)
        ans2   = np.power(self.cpu * np.power(self.error2, 2), -1)
        func   = self.test_analyzer.get_data('TEST_VAL', [1,2], fom = True)
        eq_(np.shape(func), (3,3))
        ok_(all([c in func[:,0] for c in self.cycles]))
        ok_(all([e in func[:,1] for e in ans1]))
        ok_(all([e in func[:,2] for e in ans2]))

    def test_fom_err_mat(self):
        """ FOM data should return the correct error values"""
        func = self.test_analyzer.get_data('TEST_MAT', [(1,1),(1,2),(2,1),(2,2)], fom = False)
        eq_(np.shape(func), (3,5))
        ok_(all([c in func[:,0] for c in self.cycles]))
        ok_(all([e in func[:,1] for e in self.materror11]))
        ok_(all([e in func[:,2] for e in self.materror12]))
        ok_(all([e in func[:,3] for e in self.materror21]))
        ok_(all([e in func[:,4] for e in self.materror22]))

    def test_fom_err_mat_entry(self):
        """ FOM data should work for single entries """
        func = self.test_analyzer.get_data('TEST_MAT', (1,1), fom = False)
        eq_(np.shape(func), (3,2))
        ok_(all([c in func[:,0] for c in self.cycles]))
        ok_(all([e in func[:,1] for e in self.materror11]))

    def test_fom_err_mat_shape(self):
        """ FOM data should return the correct shape of err"""
        func = self.test_analyzer.get_data('TEST_MAT', [(1,1),(1,2),(2,1),(2,2)], fom = False)
        eq_(np.shape(func), (3,5))

    @raises(AssertionError)
    def test_fom_err_mat_nonmatrix(self):
        """ FOM data should throw an assertion error if entries of a non-matrix
        quantity is requested """
        func = self.test_analyzer.get_data('TEST_VAL', [(1,1),(1,2),(2,1),(2,2)], fom = False)

    @raises(AssertionError)
    def test_fom_err_mat_invalid_entries(self):
        """ FOM data should throw an assertion error if invalid entries
        are passed """
        func = self.test_analyzer.get_data('TEST_MAT', [(3,1), (1,1),
                                                    (5,2)], fom = False)

    def test_fom_fom_mat(self):
        """ FOM data should return the correct FOM values"""
        func = self.test_analyzer.get_data('TEST_MAT', [(1,1),(1,2),(2,1),(2,2)], fom = True)
        ans11 = np.power(self.cpu * np.power(self.materror11, 2), -1)
        ans21 = np.power(self.cpu * np.power(self.materror21, 2), -1)
        ans12 = np.power(self.cpu * np.power(self.materror12, 2), -1)
        ans22 = np.power(self.cpu * np.power(self.materror22, 2), -1)
        eq_(np.shape(func), (3,5))
        ok_(all([c in func[:,0] for c in self.cycles]))
        ok_(all([e in func[:,1] for e in ans11]))
        ok_(all([e in func[:,2] for e in ans12]))
        ok_(all([e in func[:,3] for e in ans21]))
        ok_(all([e in func[:,4] for e in ans22]))

    def test_fom_average_fom(self):
        """ Average FOM should return the correct value on non-matrix """
        avg = self.test_analyzer.get_avg('TEST_VAL', 1)
        ok_(np.isclose(avg,1852133.92597))

    def test_fom_average_with_n(self):
        """ Average FOM should return correct value for the last n-entries """
        avg = self.test_analyzer.get_avg('TEST_VAL',1,2)
        ok_(np.isclose(avg, 2249100.3598560574))

    def test_collapse_type(self):
        """ Collapsed group errors should return a numpy array """
        data = self.test_analyzer.get_collapse('TEST_VAL', [1,2])
        ok_(isinstance(data, np.ndarray))

    def test_collapse_shapes(self):
        """ Collapsed group errors should return the correct shape """
        data = self.test_analyzer.get_collapse('TEST_MAT', [1,3,2])
        eq_(np.shape(data), (3,2))

    def test_collapse_values(self):
        """ Collapsed group errors should return the correct values """
        data = self.test_analyzer.get_collapse('TEST_MAT', [1,3,2], fom = False)
        ans = self.materror11 + self.materror12 + self.materror21
        ok_(all([c in data[:,0] for c in self.cycles]))
        ok_(np.allclose(np.sort(data[:,1]), np.sort(ans)))

    def test_collapse_fom(self):
        """ Collapsed group fom should return the correct values """
        data = self.test_analyzer.get_collapse('TEST_MAT', [1,3,2], fom = True)
        sum = np.power(self.materror11,2) + np.power(self.materror12,2) + np.power(self.materror21,2)
        ans = np.power(np.multiply(sum, self.cpu), -1)
        ok_(all([c in data[:,0] for c in self.cycles]))
        ok_(np.allclose(np.sort(data[:,1]), np.sort(ans)))

    def test_collapse_avg(self):
        """ Collapsed average should return the correct fom value """
        avg = self.test_analyzer.get_collapse_avg('TEST_MAT', [1,3,2])
        sum = np.power(self.materror11,2) + np.power(self.materror12,2) + np.power(self.materror21,2)
        ans = np.power(np.multiply(sum, self.cpu), -1)
        ok_(np.isclose(np.mean(ans), avg))

    def test_collapse_avg_n(self):
        """ Collapsed average should return the correct fom value with n """
        avg = self.test_analyzer.get_collapse_avg('TEST_MAT', [1,3,2], 1)
        sum = np.power(self.materror11,2) + np.power(self.materror12,2) + np.power(self.materror21,2)
        ans = np.power(np.multiply(sum, self.cpu), -1)        
        ok_(np.isclose(np.mean(ans[-1:]), avg))

    def test_fom_var(self):
        """ Figure of merit variance should return the correct value """
        ans = np.var(np.power(self.cpu * np.power(self.error1, 2), -1))
        var = self.test_analyzer.get_var('TEST_VAL', 1, start=-1, end=0)
        ok_(np.isclose(ans, var))

    def test_fom_var_no_range(self):
        """ Figure of merit variance should return the correct value """
        fom = np.power(self.cpu * np.power(self.error1, 2), -1)
        ans = np.var(fom[1:3])
        var = self.test_analyzer.get_var('TEST_VAL', 1)
        ok_(np.isclose(ans, var))
