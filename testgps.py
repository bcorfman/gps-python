__author__ = 'brandon_corfman'
import unittest
from gps import Op, GPS

class TestGPS(unittest.TestCase):
    def __init__(self):
        unittest.TestCase.__init__()
        self.school_ops = [Op(action='drive-son-to-school',
                              preconds=['son-at-home', 'car-works'],
                              add_list=['son-at-school'],
                              del_list=['son-at-home']),
                           Op(action='shop-installs-battery',
                              preconds=['car-needs-battery', 'shop-knows-problem', 'shop-has-money'],
                              add_list=['car-works']),
                           Op(action='tell-shop-problem',
                              preconds=['in-communication-with-shop'],
                              add_list=['shop-knows-problem']),
                           Op(action='telephone-shop',
                              preconds=['know-phone-number'],
                              add_list=['in-communication-with-shop']),
                           Op(action='look-up-number',
                              preconds=['have-phone-book'],
                              add_list=['know-phone-number']),
                           Op(action='give-shop-money',
                              preconds=['have-money'],
                              add_list=['shop-has-money'],
                              del_list=['have-money'])]

    def testCarRepair(self):
        gps = GPS(state=['son-at-home', 'car-needs-battery', 'have-money', 'have-phone-book'],
                  goals=['son-at-school'],
                  ops=self.school_ops)
        self.assertEqual(gps.solve(), 'solved')

    def testNoPhoneBook(self):
        gps = GPS(state=['son-at-home', 'car-needs-battery', 'have-money'],
                  goals=['son-at-school'],
                  ops=self.school_ops)
        self.assertEqual(gps.solve(), "can't solve")

    def testCarWorks(self):
        gps = GPS(state=['son-at-home', 'car-works'],
                  goals=['son-at-school'],
                  ops=self.school_ops)
        self.assertEqual(gps.solve(), 'solved')
