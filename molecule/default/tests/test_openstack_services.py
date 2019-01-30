# -*- coding: utf-8 -*-
# ==============================================================================
# Imports
# ==============================================================================
import pytest
from pprint import pformat
from munch import unmunchify


# ==============================================================================
# Test Cases
# ==============================================================================
@pytest.mark.test_id('b2e417ee-23ea-11e9-aad3-9cdc71d6c120')
@pytest.mark.jira('asc-1505')
def test_openstack_services(os_api_conn, openstack_properties):
    """Test to verify that all expected services are enabled

    Args:
        os_api_conn (openstack.connection.Connection): An authorized API
            connection to the 'default' cloud on the OpenStack infrastructure.
        openstack_properties(dict): OpenStack facts and variables from Ansible
            which can be used to manipulate OpenStack objects.
    """
    # Getting the right cinder service to check:
    #    Cinder API V1 was removed in Queens release (os_version_major == 17)
    #    (https://docs.openstack.org/releasenotes/horizon/rocky.html)
    #
    #    Cinder API V2 is deprecated in Rocky (os_version_major == 18)
    #    https://developer.openstack.org/api-ref/block-storage/
    #
    #    Cinder API V3 is already in Queens and later.

    services_not_found = []
    services_not_enabled = []

    if openstack_properties['os_version_major'] < 17:
        cinder_service = 'cinder'
    else:
        cinder_service = 'cinderv3'

    # List of OpenStack services that need to be checked:
    checked_services = [cinder_service,
                        'keystone',
                        'neutron',
                        'swift',
                        'heat',
                        'glance',
                        'nova']

    # Getting the list of all services
    # (returning the list of Munch Python dictionaries)
    all_services_list = os_api_conn.list_services()

    for service in checked_services:
        filtered_services = list(filter(lambda d:
                                        d['name'].lower() == service,
                                        all_services_list))

        if len(filtered_services) == 0:
            services_not_found.append(service)
        else:
            if not filtered_services[0]['enabled']:
                services_not_enabled.append(service)

    assert len(services_not_found) < 1,\
        "\nServices not found:\n{}\nServices not enabled\n{}\n" \
        "All services returned by list_service api: \n" \
        "{}".format(services_not_found,
                    services_not_enabled,
                    pformat(unmunchify(all_services_list)))

    assert len(services_not_enabled) < 1, \
        "\nServices not enabled\n{}\n" \
        "All services returned by list_service api: \n" \
        "{}".format(services_not_enabled,
                    pformat(unmunchify(all_services_list)))
