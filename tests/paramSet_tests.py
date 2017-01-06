from nose.tools import *
import analysis.core as wdt
import numpy as np

class TestClass:

    @classmethod
    def setup_class(cls):
        st_th = 0.1
        wdt_th = 0.1
        base_dir = './tests/'
        cls.data = wdt.ParamData(st_th, wdt_th, base_dir)

    def test_ParamData_files(self):
        """ ParamData should find ten files """
        eq_(len(self.data.dataSets),10)

    def test_ParamData_cpu(self):
        """ ParamData should return the mean and stdev of CPU time """
        cpu = np.array([[ 49.71033 ], [ 0.41658582]])
        ok_(np.allclose(cpu, self.data.cpu()))

    def test_ParamData_fom_vals(self):
        """ ParamData should return the correct FOM values """
        inf_flx = np.array([[ 38851.60455084, 144060.69372554,
                              166542.71355175, 179609.88096343, 229634.67418328,
                              173867.50381264, 209243.65133516, 310828.43121905,
                              339303.87309683, 994613.56477649, 94611.2619929 ], [
                                  40896.36922749, 55606.88876857, 96299.22383066,
                                  102555.87478206, 200977.97777118, 99079.74892584,
                                  231251.046473 , 313652.78943868, 313981.08585168,
                                  1752105.49208766, 84080.79577542]])
        ok_(np.allclose(inf_flx, self.data.fom_stat('INF_FLX')))

    def test_ParamData_mat_stat_shape(self):
        """ ParamData matrix statistics should return the correct shape matrix """
        eq_(np.shape(self.data.mat_stat('INF_SP0')),(11,11))

    def test_ParamData_mat_stat_mean_value(self):
        """ ParamData matrix statistics should return the correct mean values """
        eq_(self.data.mat_stat('INF_SP0')[0,0], 322628.81124076847)
        ok_(np.allclose(self.data.mat_stat('INF_SP0')[3,3], 5203063133.0263014))
        eq_(self.data.mat_stat('INF_SP0')[7,1], 0)
        ok_(np.allclose(self.data.mat_stat('INF_SP0')[6,6], 43613021.7687))

    def test_ParamData_mat_stat_stdv_value(self):
        """ ParamData matrix statistics should return the correct stdv values """
        ok_(np.allclose(self.data.mat_stat('INF_SP0', mean = False)[0,0],229881.88117910567))
        ok_(np.allclose(self.data.mat_stat('INF_SP0', mean = False)[2,2],6683893584.0180454))
        ok_(np.allclose(self.data.mat_stat('INF_SP0', mean = False)[6,3], 0))
        ok_(np.allclose(self.data.mat_stat('INF_SP0', mean = False)[8,9],452518.24176970578))