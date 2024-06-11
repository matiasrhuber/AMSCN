import unittest
from counter import TimeIndependentAutocorrelationCounter, TimeIndependentCrosscorrelationCounter


class DESTest(unittest.TestCase):
    """
    This python unittest class checks the fourth part of the programming assignment for basic functionality.
    """

    def test_cross_correlation(self):
        """
        Test the basic implementation of the cross covariance counter.
        """
        ticcc = TimeIndependentCrosscorrelationCounter()

        ticcc.count(1, 5)
        ticcc.count(2, 7)
        ticcc.count(6, 3)
        ticcc.count(3, 3)
        ticcc.count(4, 5)

        self.assertAlmostEqual(-1.52, ticcc.get_cov(), delta=.01,
                               msg="Error in TimeIndependentCrosscorrelationCounter. Covariance calculation is wrong.")
        self.assertAlmostEqual(-.4722, ticcc.get_cor(), delta=.01,
                               msg="Error in TimeIndependentCrosscorrelationCounter. Correlation calculation is wrong.")

    def test_auto_correlation(self):
        """
        Test the basic implementation of the auto covariance counter.
        """
        tiacc = TimeIndependentAutocorrelationCounter(max_lag=5)

        for i in range(5000):
            tiacc.count(i % 25)

        results_cov = [52.0, 40.0, 29.0, 19.0, 10.0]
        results_cor = [0.9998, 0.7691, 0.5576, 0.3653, 0.1923]

        for lag in range(5):
            self.assertAlmostEqual(results_cov[lag], tiacc.get_auto_cov(lag), delta=.05,
                                   msg="Error in TimeIndependentAutocorrelationCounter. Covariance calculation is wrong.")
            self.assertAlmostEqual(results_cor[lag], tiacc.get_auto_cor(lag), delta=.05,
                                   msg="Error in TimeIndependentAutocorrelationCounter. Correlation calculation is wrong.")


if __name__ == '__main__':
    unittest.main()
