# -*- coding: utf-8 -*-
# ==============================================================================
# Imports
# ==============================================================================
import pytest_rpc.helpers as helpers
import os
import pytest
import testinfra.utils.ansible_runner

# ==============================================================================
# Globals
# ==============================================================================
testinfra_hosts = testinfra.utils.ansible_runner.AnsibleRunner(
    os.environ['MOLECULE_INVENTORY_FILE']).get_hosts('shared-infra_hosts')[:1]


# ==============================================================================
# Helpers
# ==============================================================================
def service_enabled(service, run_on_host):
    """ Verify if a service is enabled

    Args:
        service (str): an openstack service to query (e.g 'nova', 'glance')
        run_on_host (testinfra.host.Host): Testinfra host fixture

    Return:
        bool: whether the queried service is enabled

    """

    cmd = ". openrc ; openstack service show -f value -c enabled {}".format(
        service)
    result = helpers.run_on_container(cmd, 'utility', run_on_host)

    if result.stdout.lower() == 'true':
        return True
    else:
        return False

# ==============================================================================
# Test Cases
# ==============================================================================
@pytest.mark.test_id('b2e417ee-23ea-11e9-aad3-9cdc71d6c120')
@pytest.mark.jira('asc-1505', 'asc-1555')
def test_openstack_nova_service(host):
    """Test to verify that Nova service is enabled

    Args:
        host (testinfra.host.Host): Testinfra host fixture
    """

    assert service_enabled('nova', host)


@pytest.mark.test_id('d8e0c200-2a78-11e9-aad3-9cdc71d6c120')
@pytest.mark.jira('asc-1505', 'asc-1555')
def test_openstack_glance_service(host):
    """Test to verify that Nova service is enabled

    Args:
        host (testinfra.host.Host): Testinfra host fixture
    """

    assert service_enabled('glance', host)


@pytest.mark.test_id('c66d7b5e-2a78-11e9-aad3-9cdc71d6c120')
@pytest.mark.jira('asc-1505', 'asc-1555')
def test_openstack_neutron_service(host):
    """Test to verify that Nova service is enabled

    Args:
        host (testinfra.host.Host): Testinfra host fixture
    """

    assert service_enabled('neutron', host)


@pytest.mark.test_id('b82ef310-2a78-11e9-aad3-9cdc71d6c120')
@pytest.mark.jira('asc-1505', 'asc-1555')
def test_openstack_keystone_service(host):
    """Test to verify that Nova service is enabled

    Args:
        host (testinfra.host.Host): Testinfra host fixture
    """

    assert service_enabled('keystone', host)


@pytest.mark.test_id('aadcb274-2a78-11e9-aad3-9cdc71d6c120')
@pytest.mark.jira('asc-1505', 'asc-1555')
def test_openstack_swift_service(host):
    """Test to verify that Nova service is enabled

    Args:
        host (testinfra.host.Host): Testinfra host fixture
    """

    assert service_enabled('swift', host)


@pytest.mark.test_id('89d09a96-2a78-11e9-aad3-9cdc71d6c120')
@pytest.mark.jira('asc-1505', 'asc-1555')
def test_openstack_heat_service(host):
    """Test to verify that Nova service is enabled

    Args:
        host (testinfra.host.Host): Testinfra host fixture
    """

    assert service_enabled('heat', host)

# TODO: will add cinder service in the list after resolving the
# TODO: os_version_major for healthcheck, tech-debt ticket ASC-1627
