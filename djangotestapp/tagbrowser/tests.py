

import unittest

from .models import ResourceEdgeType, ResourceEdge, Resource


class TestModels(unittest.TestCase):
    def test_resource(self):
        r1 = Resource(url="http://localhost/#r1")
        r2 = Resource(url="http://localhost/#r2")
        r3 = Resource(url="http://localhost/#r3")

        t1 = ResourceEdgeType(name='t1')

        # r1.edges_out.add(
        #     ResourceEdge(type=t1))

    def test_ResourceEdge(self):
        obj = Resource(
            url="https://wrdrd.com/docs",
            # name="WRD R&D Documentation",
            description="Page <b>description</b>.")
        self.assertIsInstance(obj, Resource)
