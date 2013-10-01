%global with_doc %{!?_without_doc:1}%{?_without_doc:0}

Name:             openstack-nova
Version:          2012.2.2
Release:          1%{?dist}.6
Summary:          OpenStack Compute (nova)

Group:            Applications/System
License:          ASL 2.0
URL:              http://openstack.org/projects/compute/
Source0:          http://launchpad.net/nova/folsom/%{version}/+download/nova-%{version}.tar.gz

Source1:          nova.conf
Source6:          nova.logrotate

Source10:         openstack-nova-api.init
Source100:        openstack-nova-api.upstart
Source11:         openstack-nova-cert.init
Source110:        openstack-nova-cert.upstart
Source12:         openstack-nova-compute.init
Source120:        openstack-nova-compute.upstart
Source13:         openstack-nova-network.init
Source130:        openstack-nova-network.upstart
Source14:         openstack-nova-objectstore.init
Source140:        openstack-nova-objectstore.upstart
Source15:         openstack-nova-scheduler.init
Source150:        openstack-nova-scheduler.upstart
Source16:         openstack-nova-volume.init
Source160:        openstack-nova-volume.upstart
Source18:         openstack-nova-xvpvncproxy.init
Source180:        openstack-nova-xvpvncproxy.upstart
Source19:         openstack-nova-console.init
Source190:        openstack-nova-console.upstart
Source24:         openstack-nova-consoleauth.init
Source240:        openstack-nova-consoleauth.upstart
Source25:         openstack-nova-metadata-api.init
Source250:        openstack-nova-metadata-api.upstart

Source20:         nova-sudoers
Source21:         nova-polkit.pkla
Source22:         nova-ifc-template

#
# patches_base=2012.2.2
#
Patch0001: 0001-Ensure-we-don-t-access-the-net-when-building-docs.patch

# This is EPEL specific and not upstream
Patch100:         openstack-nova-newdeps.patch

# CERN patch
Patch1000: 1000-cern-nova.patch

BuildArch:        noarch
BuildRequires:    intltool
BuildRequires:    python-sphinx10
BuildRequires:    python-setuptools
BuildRequires:    python-netaddr
BuildRequires:    openstack-utils
# These are required to build due to the requirements check added
BuildRequires:    python-paste-deploy1.5
BuildRequires:    python-routes1.12
BuildRequires:    python-sqlalchemy0.7
BuildRequires:    python-webob1.0

Requires:         openstack-nova-compute = %{version}-%{release}
Requires:         openstack-nova-cert = %{version}-%{release}
Requires:         openstack-nova-scheduler = %{version}-%{release}
Requires:         openstack-nova-volume = %{version}-%{release}
Requires:         openstack-nova-api = %{version}-%{release}
Requires:         openstack-nova-network = %{version}-%{release}
Requires:         openstack-nova-objectstore = %{version}-%{release}
Requires:         openstack-nova-console = %{version}-%{release}


%description
OpenStack Compute (codename Nova) is open source software designed to
provision and manage large networks of virtual machines, creating a
redundant and scalable cloud computing platform. It gives you the
software, control panels, and APIs required to orchestrate a cloud,
including running instances, managing networks, and controlling access
through users and projects. OpenStack Compute strives to be both
hardware and hypervisor agnostic, currently supporting a variety of
standard hardware configurations and seven major hypervisors.

%package common
Summary:          Components common to all OpenStack Nova services
Group:            Applications/System

Requires:         openstack-utils
Requires:         python-nova = %{version}-%{release}

Requires(post):   chkconfig
Requires(postun): initscripts
Requires(preun):  chkconfig
Requires(pre):    shadow-utils

Requires:         python-setuptools
# CERN: for landb interaction
Requires:         python-suds

%description common
OpenStack Compute (codename Nova) is open source software designed to
provision and manage large networks of virtual machines, creating a
redundant and scalable cloud computing platform. It gives you the
software, control panels, and APIs required to orchestrate a cloud,
including running instances, managing networks, and controlling access
through users and projects. OpenStack Compute strives to be both
hardware and hypervisor agnostic, currently supporting a variety of
standard hardware configurations and seven major hypervisors.

This package contains scripts, config and dependencies shared
between all the OpenStack nova services.


%package compute
Summary:          OpenStack Nova Virtual Machine control service
Group:            Applications/System

Requires:         openstack-nova-common = %{version}-%{release}
Requires:         curl
Requires:         iscsi-initiator-utils
Requires:         iptables iptables-ipv6
Requires:         vconfig
# tunctl is needed where `ip tuntap` is not available
Requires:         tunctl
Requires:         libguestfs-mount >= 1.7.17
# The fuse dependency should be added to libguestfs-mount
Requires:         fuse
Requires:         libvirt >= 0.9.6
Requires:         libvirt-python
Requires:         openssh-clients
Requires:         rsync
Requires(pre):    qemu-kvm

%description compute
OpenStack Compute (codename Nova) is open source software designed to
provision and manage large networks of virtual machines, creating a
redundant and scalable cloud computing platform. It gives you the
software, control panels, and APIs required to orchestrate a cloud,
including running instances, managing networks, and controlling access
through users and projects. OpenStack Compute strives to be both
hardware and hypervisor agnostic, currently supporting a variety of
standard hardware configurations and seven major hypervisors.

This package contains the Nova service for controlling Virtual Machines.


%package network
Summary:          OpenStack Nova Network control service
Group:            Applications/System

Requires:         openstack-nova-common = %{version}-%{release}
Requires:         vconfig
Requires:         radvd
Requires:         bridge-utils
Requires:         dnsmasq
#TODO: Enable when available in RHEL 6.3
#Requires:         dnsmasq-utils
# tunctl is needed where `ip tuntap` is not available
Requires:         tunctl

%description network
OpenStack Compute (codename Nova) is open source software designed to
provision and manage large networks of virtual machines, creating a
redundant and scalable cloud computing platform. It gives you the
software, control panels, and APIs required to orchestrate a cloud,
including running instances, managing networks, and controlling access
through users and projects. OpenStack Compute strives to be both
hardware and hypervisor agnostic, currently supporting a variety of
standard hardware configurations and seven major hypervisors.

This package contains the Nova service for controlling networking.


%package volume
Summary:          OpenStack Nova storage volume control service
Group:            Applications/System

Requires:         openstack-nova-common = %{version}-%{release}
Requires:         lvm2
Requires:         scsi-target-utils

%description volume
OpenStack Compute (codename Nova) is open source software designed to
provision and manage large networks of virtual machines, creating a
redundant and scalable cloud computing platform. It gives you the
software, control panels, and APIs required to orchestrate a cloud,
including running instances, managing networks, and controlling access
through users and projects. OpenStack Compute strives to be both
hardware and hypervisor agnostic, currently supporting a variety of
standard hardware configurations and seven major hypervisors.

This package contains the Nova service for controlling storage volumes.


%package scheduler
Summary:          OpenStack Nova VM distribution service
Group:            Applications/System

Requires:         openstack-nova-common = %{version}-%{release}

%description scheduler
OpenStack Compute (codename Nova) is open source software designed to
provision and manage large networks of virtual machines, creating a
redundant and scalable cloud computing platform. It gives you the
software, control panels, and APIs required to orchestrate a cloud,
including running instances, managing networks, and controlling access
through users and projects. OpenStack Compute strives to be both
hardware and hypervisor agnostic, currently supporting a variety of
standard hardware configurations and seven major hypervisors.

This package contains the service for scheduling where
to run Virtual Machines in the cloud.


%package cert
Summary:          OpenStack Nova certificate management service
Group:            Applications/System

Requires:         openstack-nova-common = %{version}-%{release}

%description cert
OpenStack Compute (codename Nova) is open source software designed to
provision and manage large networks of virtual machines, creating a
redundant and scalable cloud computing platform. It gives you the
software, control panels, and APIs required to orchestrate a cloud,
including running instances, managing networks, and controlling access
through users and projects. OpenStack Compute strives to be both
hardware and hypervisor agnostic, currently supporting a variety of
standard hardware configurations and seven major hypervisors.

This package contains the Nova service for managing certificates.


%package api
Summary:          OpenStack Nova API services
Group:            Applications/System

Requires:         openstack-nova-common = %{version}-%{release}

%description api
OpenStack Compute (codename Nova) is open source software designed to
provision and manage large networks of virtual machines, creating a
redundant and scalable cloud computing platform. It gives you the
software, control panels, and APIs required to orchestrate a cloud,
including running instances, managing networks, and controlling access
through users and projects. OpenStack Compute strives to be both
hardware and hypervisor agnostic, currently supporting a variety of
standard hardware configurations and seven major hypervisors.

This package contains the Nova services providing programmatic access.


%package objectstore
Summary:          OpenStack Nova simple object store service
Group:            Applications/System

Requires:         openstack-nova-common = %{version}-%{release}

%description objectstore
OpenStack Compute (codename Nova) is open source software designed to
provision and manage large networks of virtual machines, creating a
redundant and scalable cloud computing platform. It gives you the
software, control panels, and APIs required to orchestrate a cloud,
including running instances, managing networks, and controlling access
through users and projects. OpenStack Compute strives to be both
hardware and hypervisor agnostic, currently supporting a variety of
standard hardware configurations and seven major hypervisors.

This package contains the Nova service providing a simple object store.


%package console
Summary:          OpenStack Nova console access services
Group:            Applications/System

Requires:         openstack-nova-common = %{version}-%{release}

%description console
OpenStack Compute (codename Nova) is open source software designed to
provision and manage large networks of virtual machines, creating a
redundant and scalable cloud computing platform. It gives you the
software, control panels, and APIs required to orchestrate a cloud,
including running instances, managing networks, and controlling access
through users and projects. OpenStack Compute strives to be both
hardware and hypervisor agnostic, currently supporting a variety of
standard hardware configurations and seven major hypervisors.

This package contains the Nova services providing
console access services to Virtual Machines.


%package -n       python-nova
Summary:          Nova Python libraries
Group:            Applications/System

Requires:         openssl
# Require openssh for ssh-keygen
Requires:         openssh
Requires:         sudo

Requires:         MySQL-python

Requires:         python-paramiko

Requires:         python-qpid
Requires:         python-kombu
Requires:         python-amqplib

Requires:         python-eventlet
Requires:         python-greenlet
Requires:         python-iso8601
Requires:         python-netaddr
Requires:         python-lxml
Requires:         python-anyjson
Requires:         python-boto
Requires:         python-cheetah
Requires:         python-ldap

Requires:         python-memcached

Requires:         python-sqlalchemy0.7
Requires:         python-migrate

Requires:         python-paste-deploy1.5
Requires:         python-routes1.12
Requires:         python-webob1.0

Requires:         python-glanceclient >= 1:0
Requires:         python-quantumclient >= 1:2
Requires:         python-novaclient

%description -n   python-nova
OpenStack Compute (codename Nova) is open source software designed to
provision and manage large networks of virtual machines, creating a
redundant and scalable cloud computing platform.

This package contains the nova Python library.

%if 0%{?with_doc}
%package doc
Summary:          Documentation for OpenStack Compute
Group:            Documentation

Requires:         %{name} = %{version}-%{release}

BuildRequires:    graphviz

# Required to build module documents
BuildRequires:    python-boto
BuildRequires:    python-eventlet
# while not strictly required, quiets the build down when building docs.
BuildRequires:    python-migrate, python-iso8601

%description      doc
OpenStack Compute (codename Nova) is open source software designed to
provision and manage large networks of virtual machines, creating a
redundant and scalable cloud computing platform.

This package contains documentation files for nova.
%endif

%prep
%setup -q -n nova-%{version}

%patch0001 -p1

# Apply EPEL patch
%patch100 -p1

# Apply CERN patch
%patch1000 -p0

find . \( -name .gitignore -o -name .placeholder \) -delete

find nova -name \*.py -exec sed -i '/\/usr\/bin\/env python/{d;q}' {} +

sed -i '/setuptools_git/d' setup.py

sed -i s/LOCALBRANCH:LOCALREVISION/%{release}/ nova/version.py

%build
%{__python} setup.py build

# Move authtoken configuration out of paste.ini
openstack-config --del etc/nova/api-paste.ini filter:authtoken admin_tenant_name
openstack-config --del etc/nova/api-paste.ini filter:authtoken admin_user
openstack-config --del etc/nova/api-paste.ini filter:authtoken admin_password
openstack-config --del etc/nova/api-paste.ini filter:authtoken auth_host
openstack-config --del etc/nova/api-paste.ini filter:authtoken auth_port
openstack-config --del etc/nova/api-paste.ini filter:authtoken auth_protocol
openstack-config --del etc/nova/api-paste.ini filter:authtoken signing_dir

%install
%{__python} setup.py install -O1 --skip-build --root %{buildroot}

# docs generation requires everything to be installed first
export PYTHONPATH="$( pwd ):$PYTHONPATH"

pushd doc

%if 0%{?with_doc}
SPHINX_DEBUG=1 sphinx-1.0-build -b html source build/html
# Fix hidden-file-or-dir warnings
rm -fr build/html/.doctrees build/html/.buildinfo
%endif

# Create dir link to avoid a sphinx-build exception
mkdir -p build/man/.doctrees/
ln -s .  build/man/.doctrees/man
SPHINX_DEBUG=1 sphinx-1.0-build -b man -c source source/man build/man
mkdir -p %{buildroot}%{_mandir}/man1
install -p -D -m 644 build/man/*.1 %{buildroot}%{_mandir}/man1/

popd

# Setup directories
install -d -m 755 %{buildroot}%{_sharedstatedir}/nova
install -d -m 755 %{buildroot}%{_sharedstatedir}/nova/buckets
install -d -m 755 %{buildroot}%{_sharedstatedir}/nova/images
install -d -m 755 %{buildroot}%{_sharedstatedir}/nova/instances
install -d -m 755 %{buildroot}%{_sharedstatedir}/nova/keys
install -d -m 755 %{buildroot}%{_sharedstatedir}/nova/networks
install -d -m 755 %{buildroot}%{_sharedstatedir}/nova/tmp
install -d -m 755 %{buildroot}%{_localstatedir}/log/nova

# Setup ghost CA cert
install -d -m 755 %{buildroot}%{_sharedstatedir}/nova/CA
install -p -m 755 nova/CA/*.sh %{buildroot}%{_sharedstatedir}/nova/CA
install -p -m 644 nova/CA/openssl.cnf.tmpl %{buildroot}%{_sharedstatedir}/nova/CA
install -d -m 755 %{buildroot}%{_sharedstatedir}/nova/CA/{certs,crl,newcerts,projects,reqs}
touch %{buildroot}%{_sharedstatedir}/nova/CA/{cacert.pem,crl.pem,index.txt,openssl.cnf,serial}
install -d -m 750 %{buildroot}%{_sharedstatedir}/nova/CA/private
touch %{buildroot}%{_sharedstatedir}/nova/CA/private/cakey.pem

# Install config files
install -d -m 755 %{buildroot}%{_sysconfdir}/nova
install -p -D -m 640 %{SOURCE1} %{buildroot}%{_sysconfdir}/nova/nova.conf
install -d -m 755 %{buildroot}%{_sysconfdir}/nova/volumes
install -p -D -m 640 etc/nova/rootwrap.conf %{buildroot}%{_sysconfdir}/nova/rootwrap.conf
install -p -D -m 640 etc/nova/api-paste.ini %{buildroot}%{_sysconfdir}/nova/api-paste.ini
install -p -D -m 640 etc/nova/policy.json %{buildroot}%{_sysconfdir}/nova/policy.json

# Install initscripts for Nova services
install -p -D -m 755 %{SOURCE10} %{buildroot}%{_initrddir}/openstack-nova-api
install -p -D -m 755 %{SOURCE11} %{buildroot}%{_initrddir}/openstack-nova-cert
install -p -D -m 755 %{SOURCE12} %{buildroot}%{_initrddir}/openstack-nova-compute
install -p -D -m 755 %{SOURCE13} %{buildroot}%{_initrddir}/openstack-nova-network
install -p -D -m 755 %{SOURCE14} %{buildroot}%{_initrddir}/openstack-nova-objectstore
install -p -D -m 755 %{SOURCE15} %{buildroot}%{_initrddir}/openstack-nova-scheduler
install -p -D -m 755 %{SOURCE16} %{buildroot}%{_initrddir}/openstack-nova-volume
install -p -D -m 755 %{SOURCE18} %{buildroot}%{_initrddir}/openstack-nova-xvpvncproxy
install -p -D -m 755 %{SOURCE19} %{buildroot}%{_initrddir}/openstack-nova-console
install -p -D -m 755 %{SOURCE24} %{buildroot}%{_initrddir}/openstack-nova-consoleauth
install -p -D -m 755 %{SOURCE25} %{buildroot}%{_initrddir}/openstack-nova-metadata-api

# Install sudoers
install -p -D -m 440 %{SOURCE20} %{buildroot}%{_sysconfdir}/sudoers.d/nova

# Install logrotate
install -p -D -m 644 %{SOURCE6} %{buildroot}%{_sysconfdir}/logrotate.d/openstack-nova

# Install pid directory
install -d -m 755 %{buildroot}%{_localstatedir}/run/nova

# Install template files
install -p -D -m 644 nova/cloudpipe/client.ovpn.template %{buildroot}%{_datarootdir}/nova/client.ovpn.template
install -p -D -m 644 %{SOURCE22} %{buildroot}%{_datarootdir}/nova/interfaces.template

# Install upstart jobs examples
install -p -m 644 %{SOURCE100} %{buildroot}%{_datadir}/nova/
install -p -m 644 %{SOURCE110} %{buildroot}%{_datadir}/nova/
install -p -m 644 %{SOURCE120} %{buildroot}%{_datadir}/nova/
install -p -m 644 %{SOURCE130} %{buildroot}%{_datadir}/nova/
install -p -m 644 %{SOURCE140} %{buildroot}%{_datadir}/nova/
install -p -m 644 %{SOURCE150} %{buildroot}%{_datadir}/nova/
install -p -m 644 %{SOURCE160} %{buildroot}%{_datadir}/nova/
install -p -m 644 %{SOURCE180} %{buildroot}%{_datadir}/nova/
install -p -m 644 %{SOURCE190} %{buildroot}%{_datadir}/nova/
install -p -m 644 %{SOURCE240} %{buildroot}%{_datadir}/nova/
install -p -m 644 %{SOURCE250} %{buildroot}%{_datadir}/nova/

# Install rootwrap files in /usr/share/nova/rootwrap
mkdir -p %{buildroot}%{_datarootdir}/nova/rootwrap/
install -p -D -m 644 etc/nova/rootwrap.d/* %{buildroot}%{_datarootdir}/nova/rootwrap/

install -d -m 755 %{buildroot}%{_sysconfdir}/polkit-1/localauthority/50-local.d
install -p -D -m 644 %{SOURCE21} %{buildroot}%{_sysconfdir}/polkit-1/localauthority/50-local.d/50-nova.pkla

# Remove unneeded in production stuff
rm -f %{buildroot}%{_bindir}/nova-debug
rm -fr %{buildroot}%{python_sitelib}/nova/tests/
rm -fr %{buildroot}%{python_sitelib}/run_tests.*
rm -f %{buildroot}%{_bindir}/nova-combined
rm -f %{buildroot}/usr/share/doc/nova/README*

# We currently use the equivalent file from the novnc package
rm -f %{buildroot}%{_bindir}/nova-novncproxy

%pre common
getent group nova >/dev/null || groupadd -r nova --gid 162
if ! getent passwd nova >/dev/null; then
  useradd -u 162 -r -g nova -G nova,nobody -d %{_sharedstatedir}/nova -s /sbin/nologin -c "OpenStack Nova Daemons" nova
fi
exit 0

%pre compute
usermod -a -G qemu nova
# Add nova to the fuse group (if present) to support guestmount
if getent group fuse >/dev/null; then
  usermod -a -G fuse nova
fi
exit 0

%post compute
/sbin/chkconfig --add openstack-nova-compute
%post network
/sbin/chkconfig --add openstack-nova-network
%post volume
/sbin/chkconfig --add openstack-nova-volume
%post scheduler
/sbin/chkconfig --add openstack-nova-scheduler
%post cert
/sbin/chkconfig --add openstack-nova-cert
%post api
for svc in api metadata-api; do
    /sbin/chkconfig --add openstack-nova-$svc
done
%post objectstore
/sbin/chkconfig --add openstack-nova-objectstore
%post console
for svc in console consoleauth xvpvncproxy; do
    /sbin/chkconfig --add openstack-nova-$svc
done

%preun compute
if [ $1 -eq 0 ] ; then
    for svc in compute; do
        /sbin/service openstack-nova-${svc} stop >/dev/null 2>&1
        /sbin/chkconfig --del openstack-nova-${svc}
    done
fi
%preun network
if [ $1 -eq 0 ] ; then
    for svc in network; do
        /sbin/service openstack-nova-${svc} stop >/dev/null 2>&1
        /sbin/chkconfig --del openstack-nova-${svc}
    done
fi
%preun volume
if [ $1 -eq 0 ] ; then
    for svc in volume; do
        /sbin/service openstack-nova-${svc} stop >/dev/null 2>&1
        /sbin/chkconfig --del openstack-nova-${svc}
    done
fi
%preun scheduler
if [ $1 -eq 0 ] ; then
    for svc in scheduler; do
        /sbin/service openstack-nova-${svc} stop >/dev/null 2>&1
        /sbin/chkconfig --del openstack-nova-${svc}
    done
fi
%preun cert
if [ $1 -eq 0 ] ; then
    for svc in cert; do
        /sbin/service openstack-nova-${svc} stop >/dev/null 2>&1
        /sbin/chkconfig --del openstack-nova-${svc}
    done
fi
%preun api
if [ $1 -eq 0 ] ; then
    for svc in api metadata-api; do
        /sbin/service openstack-nova-${svc} stop >/dev/null 2>&1
        /sbin/chkconfig --del openstack-nova-${svc}
    done
fi
%preun objectstore
if [ $1 -eq 0 ] ; then
    for svc in objectstore; do
        /sbin/service openstack-nova-${svc} stop >/dev/null 2>&1
        /sbin/chkconfig --del openstack-nova-${svc}
    done
fi
%preun console
if [ $1 -eq 0 ] ; then
    for svc in console consoleauth xvpvncproxy; do
        /sbin/service openstack-nova-${svc} stop >/dev/null 2>&1
        /sbin/chkconfig --del openstack-nova-${svc}
    done
fi

%postun compute
if [ $1 -ge 1 ] ; then
    # Package upgrade, not uninstall
    for svc in compute; do
        /sbin/service openstack-nova-${svc} condrestart > /dev/null 2>&1 || :
    done
fi
%postun network
if [ $1 -ge 1 ] ; then
    # Package upgrade, not uninstall
    for svc in network; do
        /sbin/service openstack-nova-${svc} condrestart > /dev/null 2>&1 || :
    done
fi
%postun volume
if [ $1 -ge 1 ] ; then
    # Package upgrade, not uninstall
    for svc in volume; do
        /sbin/service openstack-nova-${svc} condrestart > /dev/null 2>&1 || :
    done
fi
%postun scheduler
if [ $1 -ge 1 ] ; then
    # Package upgrade, not uninstall
    for svc in scheduler; do
        /sbin/service openstack-nova-${svc} condrestart > /dev/null 2>&1 || :
    done
fi
%postun cert
if [ $1 -ge 1 ] ; then
    # Package upgrade, not uninstall
    for svc in cert; do
        /sbin/service openstack-nova-${svc} condrestart > /dev/null 2>&1 || :
    done
fi
%postun api
if [ $1 -ge 1 ] ; then
    # Package upgrade, not uninstall
    for svc in api metadata-api; do
        /sbin/service openstack-nova-${svc} condrestart > /dev/null 2>&1 || :
    done
fi
%postun objectstore
if [ $1 -ge 1 ] ; then
    # Package upgrade, not uninstall
    for svc in objectstore; do
        /sbin/service openstack-nova-${svc} condrestart > /dev/null 2>&1 || :
    done
fi
%postun console
if [ $1 -ge 1 ] ; then
    # Package upgrade, not uninstall
    for svc in console consoleauth xvpvncproxy; do
        /sbin/service openstack-nova-${svc} condrestart > /dev/null 2>&1 || :
    done
fi

%files
%doc LICENSE
%{_bindir}/nova-all

%files common
%doc LICENSE
%dir %{_sysconfdir}/nova
%config(noreplace) %attr(-, root, nova) %{_sysconfdir}/nova/nova.conf
%config(noreplace) %attr(-, root, nova) %{_sysconfdir}/nova/api-paste.ini
%config(noreplace) %attr(-, root, nova) %{_sysconfdir}/nova/rootwrap.conf
%config(noreplace) %attr(-, root, nova) %{_sysconfdir}/nova/policy.json
%config(noreplace) %{_sysconfdir}/logrotate.d/openstack-nova
%config(noreplace) %{_sysconfdir}/sudoers.d/nova
%config(noreplace) %{_sysconfdir}/polkit-1/localauthority/50-local.d/50-nova.pkla

%dir %attr(0755, nova, root) %{_localstatedir}/log/nova
%dir %attr(0755, nova, root) %{_localstatedir}/run/nova

%{_bindir}/nova-clear-rabbit-queues
# TODO. zmq-receiver may need its own service?
%{_bindir}/nova-rpc-zmq-receiver
%{_bindir}/nova-manage
%{_bindir}/nova-rootwrap

%exclude %{_datarootdir}/nova/*.upstart
%{_datarootdir}/nova
%{_mandir}/man1/nova*.1.gz

%defattr(-, nova, nova, -)
%dir %{_sharedstatedir}/nova
%dir %{_sharedstatedir}/nova/buckets
%dir %{_sharedstatedir}/nova/images
%dir %{_sharedstatedir}/nova/instances
%dir %{_sharedstatedir}/nova/keys
%dir %{_sharedstatedir}/nova/networks
%dir %{_sharedstatedir}/nova/tmp

%files compute
%{_bindir}/nova-compute
%{_initrddir}/openstack-nova-compute
%{_datarootdir}/nova/openstack-nova-compute.upstart
%{_datarootdir}/nova/rootwrap/compute.filters

%files network
%{_bindir}/nova-network
%{_bindir}/nova-dhcpbridge
%{_initrddir}/openstack-nova-network
%{_datarootdir}/nova/openstack-nova-network.upstart
%{_datarootdir}/nova/rootwrap/network.filters

%files volume
%{_bindir}/nova-volume
%{_initrddir}/openstack-nova-volume
%{_bindir}/nova-volume-usage-audit
%{_datarootdir}/nova/openstack-nova-volume.upstart
%{_datarootdir}/nova/rootwrap/volume.filters
%dir %attr(0755, nova, root) %{_sysconfdir}/nova/volumes

%files scheduler
%{_bindir}/nova-scheduler
%{_initrddir}/openstack-nova-scheduler
%{_datarootdir}/nova/openstack-nova-scheduler.upstart

%files cert
%{_bindir}/nova-cert
%{_initrddir}/openstack-nova-cert
%{_datarootdir}/nova/openstack-nova-cert.upstart
%defattr(-, nova, nova, -)
%dir %{_sharedstatedir}/nova/CA/
%dir %{_sharedstatedir}/nova/CA/certs
%dir %{_sharedstatedir}/nova/CA/crl
%dir %{_sharedstatedir}/nova/CA/newcerts
%dir %{_sharedstatedir}/nova/CA/projects
%dir %{_sharedstatedir}/nova/CA/reqs
%{_sharedstatedir}/nova/CA/*.sh
%{_sharedstatedir}/nova/CA/openssl.cnf.tmpl
%ghost %config(missingok,noreplace) %verify(not md5 size mtime) %{_sharedstatedir}/nova/CA/cacert.pem
%ghost %config(missingok,noreplace) %verify(not md5 size mtime) %{_sharedstatedir}/nova/CA/crl.pem
%ghost %config(missingok,noreplace) %verify(not md5 size mtime) %{_sharedstatedir}/nova/CA/index.txt
%ghost %config(missingok,noreplace) %verify(not md5 size mtime) %{_sharedstatedir}/nova/CA/openssl.cnf
%ghost %config(missingok,noreplace) %verify(not md5 size mtime) %{_sharedstatedir}/nova/CA/serial
%dir %attr(0750, -, -) %{_sharedstatedir}/nova/CA/private
%ghost %config(missingok,noreplace) %verify(not md5 size mtime) %{_sharedstatedir}/nova/CA/private/cakey.pem

%files api
%{_bindir}/nova-api*
%{_initrddir}/openstack-nova-*api
%{_datarootdir}/nova/openstack-nova-*api.upstart
%{_datarootdir}/nova/rootwrap/api-metadata.filters

%files objectstore
%{_bindir}/nova-objectstore
%{_initrddir}/openstack-nova-objectstore
%{_datarootdir}/nova/openstack-nova-objectstore.upstart

%files console
%{_bindir}/nova-console*
%{_bindir}/nova-xvpvncproxy
%{_initrddir}/openstack-nova-console*
%{_datarootdir}/nova/openstack-nova-console*.upstart
%{_initrddir}/openstack-nova-xvpvncproxy
%{_datarootdir}/nova/openstack-nova-xvpvncproxy.upstart

%files -n python-nova
%defattr(-,root,root,-)
%doc LICENSE
%{python_sitelib}/nova
%{python_sitelib}/nova-%{version}-*.egg-info

%if 0%{?with_doc}
%files doc
%doc LICENSE doc/build/html
%endif

%changelog
* Thu Feb 21 2013 Belmiro Moreira <belmiro.moreira@cern.ch> - 2012.2.2-1-6 
- don't change hostname to follow RFC 1123; 
- change cern_services to cern-services;
- default OS for landb is Linux; 
- add availability zones support for hyperV;
- multi-zones support;

* Mon Feb 11 2013 Belmiro Moreira <belmiro.moreira@cern.ch> - 2012.2.2-1.5
- change default cern_landb to True

* Tue Feb 04 2013 Belmiro Moreira <belmiro.moreira@cern.ch> - 2012.2.2-1.4
- define landb OS to windows or linux;
- define landb Departmant and Group for responsable person;
- fix vm start;

* Mon Feb 03 2013 Belmiro Moreira <belmiro.moreira@cern.ch> - 2012.2.2-1.3
- fix host declaration for networking 

* Thu Jan 31 2013 Belmiro Moreira <belmiro.moreira@cern.ch> - 2012.2.2-1.2
- suds for clients
- multitenancy isolation filter

* Mon Jan 22 2013 Belmiro Moreira <belmiro.moreira@cern.ch> - 2012.2.2-1.1
- cern_landb, cern_dns, cern_active_directory flags
- Refactor network administration
- Common landb auth
- EC2 api creates cattle machines
- Instance name always updated to landb
- Public availability zone is the default
- Resize/migrate integration with landb
- Wait for DNS and AD before booting
- Live migration integration with landb

* Fri Dec 14 2012 Pádraig Brady <pbrady@redhat.com> - 2012.2.2-1
- Update to folsom stable release 2 (fixes CVE-2012-5625)

* Thu Dec 06 2012 Nikola Đipanov <ndipanov@redhat.com> - 2012.2.1-3
- signing_dir renamed from incorrect signing_dirname in default nova.conf

* Tue Dec 04 2012 Nikola Đipanov <ndipanov@redhat.com> - 2012.2.1-2
- Fix rpc_control_exchange regression

* Fri Nov 30 2012 Nikola Đipanov <ndipanov@redhat.com> - 2012.2.1-1
- Update to folsom stable release 1

* Tue Oct 30 2012 Pádraig Brady <pbrady@redhat.com> - 2012.2-2
- Add support for python-migrate-0.6

* Thu Oct 12 2012 Pádraig Brady <pbrady@redhat.com> - 2012.2-1
- Update to folsom final

* Fri Oct 12 2012 Nikola Dipanov <ndipanov@redhat.com> - 2012.1.3-1
- Restore libvirt block storage connections on reboot
- Fix libvirt volume attachment error logging
- Ensure instances with deleted floating IPs can be deleted
- Ensure can contact floating IP after instance snapshot
- Fix tenant usage time accounting
- Ensure correct disk definitions are used on volume attach/detach
- Improve concurrency of long running tasks
- Fix unmounting of LXC containers in the presence of symlinks
- Fix external lock corruption in the presence of SELinux
- Allow snapshotting images that are deleted in glance
- Ensure the correct fixed IP is deallocated when deleting VMs

* Fri Aug 10 2012 Pádraig Brady <P@draigBrady.com> - 2012.1.1-15
- Fix package versions to ensure update dependencies are correct
- Fix CA cert permissions issue introduced in 2012.1.1-10

* Wed Aug  8 2012 Pádraig Brady <P@draigBrady.com> - 2012.1.1-13
- Log live migration errors
- Prohibit host file corruption through file injection (CVE-2012-3447)

* Mon Aug  6 2012 Pádraig Brady <P@draigBrady.com> - 2012.1.1-12
- Fix group installation issue introduced in 2012.1.1-10

* Sun Jul 30 2012 Pádraig Brady <P@draigBrady.com> - 2012.1.1-11
- Update from stable upstream including...
- Fix metadata file injection with xen
- Fix affinity filters when hints is None
- Fix marker behavior for flavors
- Handle local remote exceptions consistently
- Fix qcow2 size on libvirt live block migration
- Fix for API listing of os hosts
- Avoid lazy loading errors on instance_type
- Avoid casts in network manager to prevent races
- Conditionally allow queries for deleted flavours
- Fix wrong regex in cleanup_file_locks
- Add net rules to VMs on compute service start
- Tolerate parsing null connection info in BDM
- Support EC2 CreateImage API for boot from volume
- EC2 DescribeImages reports correct rootDeviceType
- Reject EC2 CreateImage for instance store
- Fix EC2 CreateImage no_reboot logic
- Convert remaining network API casts to calls
- Move where the fixed ip deallocation happens
- Fix the qpid_heartbeat option so that it's effective

* Fri Jul 27 2012 Pádraig Brady <P@draigBrady.com> - 2012.1.1-10
- Split out into more sub packages

* Fri Jul 20 2012 Pádraig Brady <P@draigBrady.com> - 2012.1.1-4
- Enable auto cleanup of old cached instance images
- Fix ram_allocation_ratio based over subscription
- Expose over quota exceptions via native API
- Return 413 status on over quota in the native API
- Fix call to network_get_all_by_uuids
- Fix libvirt get_memory_mb_total with xen
- Use compute_api.get_all in affinity filters (CVE-2012-3371)
- Use default qemu img cluster size in libvirt connect
- Ensure libguestfs has completed before proceeding

* Thu Jul  5 2012 Pádraig Brady <P@draigBrady.com> - 2012.1.1-3
- Distinguish volume overlimit exceptions
- Prohibit host file corruption through file injection (CVE-2012-3360, CVE-2012-3361)

* Wed Jun 27 2012 Pádraig Brady <P@draigBrady.com> - 2012.1.1-2
- Update to latest essex stable branch
- Support injecting new .ssh/authorized_keys files to SELinux enabled guests

* Fri Jun 22 2012 Pádraig Brady <P@draigBrady.com> - 2012.1.1-1
- Update to essex stable release 2012.1.1
- Improve performance and stability of file injection
- add upstart jobs, alternative to sysv initscripts

* Fri Jun 15 2012 Pádraig Brady <P@draigBrady.com> - 2012.1-12
- update performance and stability fixes from essex stable

* Mon Jun 11 2012 Pádraig Brady <P@draigBrady.com> - 2012.1-11
- fix an exception caused by the fix for CVE-2012-2654
- fix the encoding of the dns_domains table (requires a db sync)
- fix a crash due to a nova services startup race (#825051)

* Wed Jun 08 2012 Pádraig Brady <P@draigBrady.com> - 2012.1-10
- Enable libguestfs image inspection

* Wed Jun 06 2012 Pádraig Brady <P@draigBrady.com> - 2012.1-9
- Sync up with Essex stable branch, including...
- Fix for protocol case handling (#829441, CVE-2012-2654)

* Wed May 16 2012 Alan Pevec <apevec@redhat.com> - 2012.1-8
- Remove m2crypto and other dependencies no loner needed by Essex

* Wed May 16 2012 Pádraig Brady <P@draigBrady.com> - 2012.1-7
- Depend on tunctl which can be used when `ip tuntap` is unavailable
- Sync up with Essex stable branch
- Handle updated qemu-img info output
- Replace openstack-nova-db-setup with openstack-db

* Wed May 09 2012 Alan Pevec <apevec@redhat.com> - 2012.1-6
- Remove the socat dependency no longer needed by Essex

* Tue May 01 2012 Pádraig Brady <P@draigBrady.com> - 2012.1-5
- Start the services later in the boot sequence

* Wed Apr 27 2012 Pádraig Brady <P@draigBrady.com> - 2012.1-4
- Fix install issues with new Essex init scripts

* Wed Apr 25 2012 Pádraig Brady <P@draigBrady.com> - 2012.1-3
- Use parallel installed versions of python-routes and python-paste-deploy

* Thu Apr 19 2012 Pádraig Brady <P@draigBrady.com> - 2012.1-2
- Sync up with Essex stable branch
- Support more flexible guest image file injection
- Enforce quota on security group rules (#814275, CVE-2012-2101)
- Provide startup scripts for the Essex VNC services
- Provide a startup script for the separated metadata api service

* Fri Apr 13 2012 Pádraig Brady <P@draigBrady.com> - 2012.1-1
- Update to Essex release

* Mon Apr 01 2012 Pádraig Brady <P@draigBrady.com> - 2012.1-0.1.rc1
- Update to Essex release candidate 1

* Thu Mar 29 2012 Pádraig Brady <P@draigBrady.com> - 2011.3.1-8
- Remove the dependency on the not yet available dnsmasq-utils

* Thu Mar 29 2012 Russell Bryant <rbryant@redhat.com> - 2011.3.1-7
- CVE-2012-1585 - Long server names grow nova-api log files significantly
- Resolves: rhbz#808148

* Mon Mar  6 2012 Pádraig Brady <P@draigBrady.com> - 2011.3.1-5
- Require bridge-utils

* Mon Feb 13 2012 Pádraig Brady <P@draigBrady.com> - 2011.3.1-4
- Support --force_dhcp_release (#788485)

* Fri Jan 27 2012 Pádraig Brady <P@draigBrady.com> - 2011.3.1-3
- Suppress erroneous output to stdout on package install (#785115)

* Mon Jan 23 2012 Pádraig Brady <P@draigBrady.com> - 2011.3.1-2
- Fix a REST API v1.0 bug causing a regression with deltacloud

* Fri Jan 20 2012 Pádraig Brady <P@draigBrady.com> - 2011.3.1-1
- Update to 2011.3.1 release
- Allow empty mysql root password in mysql setup script
- Enable mysqld at boot in mysql setup script

* Wed Jan 18 2012 Mark McLoughlin <markmc@redhat.com> - 2011.3.1-0.4.10818%{?dist}
- Update to latest 2011.3.1 release candidate
- Re-add nova-{clear-rabbit-queues,instance-usage-audit}

* Tue Jan 17 2012 Mark McLoughlin <markmc@redhat.com> - 2011.3.1-0.3.10814
- nova-stack isn't missing after all

* Tue Jan 17 2012 Mark McLoughlin <markmc@redhat.com> - 2011.3.1-0.2.10814
- nova-{stack,clear-rabbit-queues,instance-usage-audit} temporarily removed because of lp#917676

* Tue Jan 17 2012 Mark McLoughlin <markmc@redhat.com> - 2011.3.1-0.1.10814
- Update to 2011.3.1 release candidate
- Only adds 4 patches from upstream which we didn't already have

* Wed Jan 11 2012 Pádraig Brady <P@draigBrady.com> - 2011.3-19
- Fix libguestfs support for specified partitions
- Fix tenant bypass by authenticated users using API (#772202, CVE-2012-0030)

* Fri Jan  6 2012 Mark McLoughlin <markmc@redhat.com> - 2011.3-18
- Fix up recent patches which don't apply

* Fri Jan  6 2012 Mark McLoughlin <markmc@redhat.com> - 2011.3-17
- Backport tgtadm off-by-one fix from upstream (#752709)

* Fri Jan  6 2012 Mark McLoughlin <markmc@redhat.com> - 2011.3-16
- Rebase to latest upstream stable/diablo, pulling in ~50 patches

* Fri Jan  6 2012 Mark McLoughlin <markmc@redhat.com> - 2011.3-15
- Move recent patches into git (no functional changes)

* Fri Dec 30 2011 Pádraig Brady <P@draigBrady.com> - 2011.3-14
- Don't require the fuse group (#770927)
- Require the fuse package (to avoid #767852)

* Tue Dec 14 2011 Pádraig Brady <P@draigBrady.com> - 2011.3-13
- Sanitize EC2 manifests and image tarballs (#767236, CVE 2011-4596)
- update libguestfs support

* Tue Dec 06 2011 Russell Bryant <rbryant@redhat.com> - 2011.3-11
- Add --yes, --rootpw, and --novapw options to openstack-nova-db-setup.

* Wed Nov 30 2011 Pádraig Brady <P@draigBrady.com> - 2011.3-10
- Use updated parallel install versions of epel packages
- Add libguestfs support

* Tue Nov 29 2011 Pádraig Brady <P@draigBrady.com> - 2011.3-9
- Update the libvirt dependency from 0.8.2 to 0.8.7
- Ensure we don't access the net when building docs

* Tue Nov 29 2011 Russell Bryant <rbryant@redhat.com> - 2011.3-8
- Change default database to mysql. (#735012)

* Mon Nov 14 2011 Mark McLoughlin <markmc@redhat.com> - 2011.3-8
- Add ~20 significant fixes from upstream stable branch

* Wed Oct 26 2011 Mark McLoughlin <markmc@redhat.com> - 2011.3-7
- Fix password leak in EC2 API (#749385, CVE 2011-4076)

* Mon Oct 24 2011 Mark McLoughlin <markmc@redhat.com> - 2011.3-5
- Fix block migration (#741690)

* Fri Oct 21 2011 David Busby <oneiroi@fedoraproject.org> 2011.3-5
- Changed requirement from python-sphinx, to python-sphinx10
- Switch back to SysV init for el6

* Mon Oct 17 2011 Bob Kukura <rkukura@redhat.com> - 2011.3-4
- Add dependency on python-amqplib (#746685)

* Wed Sep 28 2011 Mark McLoughlin <markmc@redhat.com> - 2011.3-3
- Fix lazy load exception with security groups (#741307)
- Fix issue with nova-network deleting the default route (#741686)
- Fix errors caused by MySQL connection pooling (#741312)

* Mon Sep 26 2011 Mark McLoughlin <markmc@redhat.com> - 2011.3-2
- Manage the package's patches in git; no functional changes.

* Thu Sep 22 2011 Mark McLoughlin <markmc@redhat.com> - 2011.3-1
- Update to Diablo final.
- Drop some upstreamed patches.
- Update the metadata-accept patch to what's proposed for essex.
- Switch rpc impl from carrot to kombu.

* Mon Sep 19 2011 Mark McLoughlin <markmc@redhat.com> - 2011.3-0.10.d4
- Use tgtadm instead of ietadm (#737046)

* Wed Sep 14 2011 Mark McLoughlin <markmc@redhat.com> - 2011.3-0.9.d4
- Remove python-libguestfs dependency (#738187)

* Mon Sep  5 2011 Mark McLoughlin <markmc@redhat.com> - 2011.3-0.8.d4
- Add iptables rule to allow EC2 metadata requests (#734347)

* Sat Sep  3 2011 Mark McLoughlin <markmc@redhat.com> - 2011.3-0.7.d4
- Add iptables rules to allow requests to dnsmasq (#734347)

* Wed Aug 31 2011 Angus Salkeld <asalkeld@redhat.com> - 2011.3-0.6.d4
- Add the one man page provided by nova.
- Start services with --flagfile rather than --flag-file (#735070)

* Tue Aug 30 2011 Angus Salkeld <asalkeld@redhat.com> - 2011.3-0.5.d4
- Switch from SysV init scripts to systemd units (#734345)

* Mon Aug 29 2011 Mark McLoughlin <markmc@redhat.com> - 2011.3-0.4.d4
- Don't generate root CA during %%post (#707199)
- The nobody group shouldn't own files in /var/lib/nova
- Add workaround for sphinx-build segfault

* Fri Aug 26 2011 Mark McLoughlin <markmc@redhat.com> - 2011.3-0.3.d4
- Update to diablo-4 milestone
- Use statically assigned uid:gid 162:162 (#732442)
- Collapse all sub-packages into openstack-nova; w/o upgrade path
- Reduce use of macros
- Rename stack to nova-stack
- Fix openssl.cnf.tmpl script-without-shebang rpmlint warning
- Really remove ajaxterm
- Mark polkit file as %%config

* Mon Aug 22 2011 Mark McLoughlin <markmc@redhat.com> - 2011.3-0.2.1449bzr
- Remove dependency on python-novaclient

* Wed Aug 17 2011 Mark McLoughlin <markmc@redhat.com> - 2011.3-0.1.1449bzr
- Update to latest upstream.
- nova-import-canonical-imagestore has been removed
- nova-clear-rabbit-queues was added

* Tue Aug  9 2011 Mark McLoughlin <markmc@redhat.com> - 2011.3-0.2.1409bzr
- Update to newer upstream
- nova-instancemonitor has been removed
- nova-instance-usage-audit added

* Tue Aug  9 2011 Mark McLoughlin <markmc@redhat.com> - 2011.3-0.1.bzr1130
- More cleanups
- Change release tag to reflect pre-release status

* Wed Jun 29 2011 Matt Domsch <mdomsch@fedoraproject.org> - 2011.3-1087.1
- Initial package from Alexander Sakhnov <asakhnov@mirantis.com>
  with cleanups by Matt Domsch
