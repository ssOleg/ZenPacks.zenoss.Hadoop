##############################################################################
#
# Copyright (C) Zenoss, Inc. 2014, all rights reserved.
#
# This content is made available according to terms specified in
# License.zenoss under the directory where your Zenoss product is installed.
#
##############################################################################

import os.path

from zope.event import notify
from Products.Zuul.catalog.events import IndexingEvent


def load_data(filename):
    path = os.path.join(os.path.dirname(__file__), 'data', filename)
    with open(path, 'r') as f:
        return f.read()


def add_obj(relationship, obj):
    """
    Add obj to relationship, index it, then returns the persistent
    object.
    """
    relationship._setObject(obj.id, obj)
    obj = relationship._getOb(obj.id)
    obj.index_object()
    notify(IndexingEvent(obj))
    return obj


def test_device(dmd, factor=1):
    """
     Return an example SolarisMonitorDevice with a set of example components.
    """

    from ZenPacks.zenoss.Hadoop.HadoopDataNode import HadoopDataNode
    from ZenPacks.zenoss.Hadoop.HadoopServiceNode import HadoopServiceNode

    dc = dmd.Devices.createOrganizer('/Server')

    device = dc.createInstance('hadoop_test_device')
    device.setPerformanceMonitor('localhost')
    device.index_object()
    notify(IndexingEvent(device))

    # Data Nodes
    for data_node_id in range(factor):
        data_node = add_obj(
            device.hadoop_data_nodes,
            HadoopDataNode('data_node%s' % (data_node_id))
        )

    # Service Nodes
    for service_node_id in range(factor):
        service_node = add_obj(
            device.hadoop_service_nodes,
            HadoopServiceNode('table%s' % (service_node_id))
        )

    return device
