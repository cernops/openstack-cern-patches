%global _without_doc 1
%global with_doc %{!?_without_doc:1}%{?_without_doc:0}
%global pypi_name ceilometer

Name:             openstack-ceilometer
Version:          2013.1.3
Release:          1%{?dist}
Summary:          OpenStack measurement collection service

Group:            Applications/System
License:          ASL 2.0
URL:              https://wiki.openstack.org/wiki/Ceilometer
Source0:          http://tarballs.openstack.org/%{pypi_name}/%{pypi_name}-%{version}.tar.gz
Source1:          %{pypi_name}.conf
Source2:          %{pypi_name}.logrotate

Source10:         %{name}-api.init
Source100:        %{name}-api.upstart
Source11:         %{name}-collector.init
Source110:        %{name}-collector.upstart
Source12:         %{name}-compute.init
Source120:        %{name}-compute.upstart
Source13:         %{name}-central.init
Source130:        %{name}-central.upstart

#
# patches_base=2013.1.3
#
Patch0001: 0001-Ensure-we-don-t-access-the-net-when-building-docs.patch
Patch0002: 0002-avoid-code-path-causing-qpid-exchange-leaks.patch
Patch0003: 0003-added-ca-cert-parameter.patch

# This is EL6 specific and not upstream
Patch100:         openstack-ceilometer-newdeps.patch

BuildArch:        noarch
BuildRequires:    intltool
BuildRequires:    python-sphinx10
BuildRequires:    python-setuptools
BuildRequires:    python2-devel

BuildRequires:    openstack-utils

# These are required to build due to the requirements check added
BuildRequires:    python-sqlalchemy0.7
BuildRequires:    python-webob1.2


%description
OpenStack ceilometer provides services to measure and
collect metrics from OpenStack components.


%package -n       python-ceilometer
Summary:          OpenStack ceilometer python libraries
Group:            Applications/System

Requires:         python-qpid
Requires:         python-kombu
Requires:         python-amqplib

Requires:         python-eventlet
Requires:         python-greenlet
Requires:         python-iso8601
Requires:         python-lxml
Requires:         python-anyjson
Requires:         python-stevedore

Requires:         python-sqlalchemy0.7
Requires:         python-migrate

Requires:         python-webob >= 1.2
Requires:         python-oslo-config
Requires:         PyYAML

%description -n   python-ceilometer
OpenStack ceilometer provides services to measure and
collect metrics from OpenStack components.

This package contains the ceilometer python library.


%package common
Summary:          Components common to all OpenStack ceilometer services
Group:            Applications/System

Requires:         python-ceilometer = %{version}-%{release}
Requires:         openstack-utils

Requires(post):   chkconfig
Requires(postun): initscripts
Requires(preun):  chkconfig
Requires(pre):    shadow-utils



%description common
OpenStack ceilometer provides services to measure and
collect metrics from OpenStack components.

This package contains components common to all OpenStack
ceilometer services.


%package compute
Summary:          OpenStack ceilometer compute agent
Group:            Applications/System

Requires:         %{name}-common = %{version}-%{release}

Requires:         python-novaclient
Requires:         python-keystoneclient
Requires:         libvirt-python

%description compute
OpenStack ceilometer provides services to measure and
collect metrics from OpenStack components.

This package contains the ceilometer agent for
running on OpenStack compute nodes.


%package central
Summary:          OpenStack ceilometer central agent
Group:            Applications/System

Requires:         %{name}-common = %{version}-%{release}

Requires:         python-novaclient
Requires:         python-keystoneclient
Requires:         python-glanceclient
Requires:         python-swiftclient

%description central
OpenStack ceilometer provides services to measure and
collect metrics from OpenStack components.

This package contains the central ceilometer agent.


%package collector
Summary:          OpenStack ceilometer collector agent
Group:            Applications/System

Requires:         %{name}-common = %{version}-%{release}

Requires:         pymongo

%description collector
OpenStack ceilometer provides services to measure and
collect metrics from OpenStack components.

This package contains the ceilometer collector agent.


%package api
Summary:          OpenStack ceilometer API service
Group:            Applications/System

Requires:         %{name}-common = %{version}-%{release}

Requires:         pymongo
Requires:         python-flask
Requires:         python-pecan
Requires:         python-wsme

%description api
OpenStack ceilometer provides services to measure and
collect metrics from OpenStack components.

This package contains the ceilometer API service.


%if 0%{?with_doc}
%package doc
Summary:          Documentation for OpenStack ceilometer
Group:            Documentation

# Required to build module documents
BuildRequires:    python-eventlet
BuildRequires:    python-sqlalchemy0.7
BuildRequires:    python-webob
# while not strictly required, quiets the build down when building docs.
BuildRequires:    python-migrate, python-iso8601

%description      doc
OpenStack ceilometer provides services to measure and
collect metrics from OpenStack components.

This package contains documentation files for ceilometer.
%endif

%prep
%setup -q -n ceilometer-%{version}

%patch0001 -p1
%patch0002 -p1
%patch0003 -p1

# Apply EL6 patch
%patch100 -p1

find . \( -name .gitignore -o -name .placeholder \) -delete

find ceilometer -name \*.py -exec sed -i '/\/usr\/bin\/env python/{d;q}' {} +

# TODO: Have the following handle multi line entries
sed -i '/setup_requires/d; /install_requires/d; /dependency_links/d' setup.py

%build
%{__python} setup.py build

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

popd

# Setup directories
install -d -m 755 %{buildroot}%{_sharedstatedir}/ceilometer
install -d -m 755 %{buildroot}%{_sharedstatedir}/ceilometer/tmp
install -d -m 755 %{buildroot}%{_localstatedir}/log/ceilometer

# Install config files
install -d -m 755 %{buildroot}%{_sysconfdir}/ceilometer
install -p -D -m 640 %{SOURCE1} %{buildroot}%{_sysconfdir}/ceilometer/ceilometer.conf
install -p -D -m 640 etc/ceilometer/policy.json %{buildroot}%{_sysconfdir}/ceilometer/policy.json
install -p -D -m 640 etc/ceilometer/sources.json %{buildroot}%{_sysconfdir}/ceilometer/sources.json
install -p -D -m 640 etc/ceilometer/pipeline.yaml %{buildroot}%{_sysconfdir}/ceilometer/pipeline.yaml

# Install initscripts for services
install -p -D -m 755 %{SOURCE10} %{buildroot}%{_initrddir}/%{name}-api
install -p -D -m 755 %{SOURCE11} %{buildroot}%{_initrddir}/%{name}-collector
install -p -D -m 755 %{SOURCE12} %{buildroot}%{_initrddir}/%{name}-compute
install -p -D -m 755 %{SOURCE13} %{buildroot}%{_initrddir}/%{name}-central

# Install upstart jobs examples
install -d -m 755 %{buildroot}%{_datadir}/ceilometer
install -p -m 644 %{SOURCE100} %{buildroot}%{_datadir}/ceilometer/
install -p -m 644 %{SOURCE110} %{buildroot}%{_datadir}/ceilometer/
install -p -m 644 %{SOURCE120} %{buildroot}%{_datadir}/ceilometer/
install -p -m 644 %{SOURCE130} %{buildroot}%{_datadir}/ceilometer/

# Install logrotate
install -p -D -m 644 %{SOURCE2} %{buildroot}%{_sysconfdir}/logrotate.d/%{name}

# Install pid directory
install -d -m 755 %{buildroot}%{_localstatedir}/run/ceilometer

# Remove unneeded in production stuff
rm -f %{buildroot}%{_bindir}/ceilometer-debug
rm -fr %{buildroot}%{python_sitelib}/tests/
rm -fr %{buildroot}%{python_sitelib}/run_tests.*
rm -f %{buildroot}/usr/share/doc/ceilometer/README*
rm -f %{buildroot}/%{python_sitelib}/ceilometer/api/v1/static/LICENSE.*


%pre common
getent group ceilometer >/dev/null || groupadd -r ceilometer --gid 166
if ! getent passwd ceilometer >/dev/null; then
  # Id reservation request: https://bugzilla.redhat.com/923891
  useradd -u 166 -r -g ceilometer -G ceilometer,nobody -d %{_sharedstatedir}/ceilometer -s /sbin/nologin -c "OpenStack ceilometer Daemons" ceilometer
fi
exit 0

%post compute
if [ $1 -eq 1 ] ; then
    # Initial installation
    /sbin/chkconfig --add %{name}-compute
fi

%post collector
if [ $1 -eq 1 ] ; then
    # Initial installation
    /sbin/chkconfig --add %{name}-collector
fi

%post api
if [ $1 -eq 1 ] ; then
    # Initial installation
    /sbin/chkconfig --add %{name}-api
fi

%post central
if [ $1 -eq 1 ] ; then
    # Initial installation
    /sbin/chkconfig --add %{name}-central
fi

%preun compute
if [ $1 -eq 0 ] ; then
    for svc in compute; do
        /sbin/service %{name}-${svc} stop > /dev/null 2>&1
        /sbin/chkconfig --del %{name}-${svc}
    done
fi

%preun collector
if [ $1 -eq 0 ] ; then
    for svc in collector; do
        /sbin/service %{name}-${svc} stop > /dev/null 2>&1
        /sbin/chkconfig --del %{name}-${svc}
    done
fi

%preun api
if [ $1 -eq 0 ] ; then
    for svc in api; do
        /sbin/service %{name}-${svc} stop > /dev/null 2>&1
        /sbin/chkconfig --del %{name}-${svc}
    done
fi

%preun central
if [ $1 -eq 0 ] ; then
    for svc in central; do
        /sbin/service %{name}-${svc} stop > /dev/null 2>&1
        /sbin/chkconfig --del %{name}-${svc}
    done
fi

%postun compute
if [ $1 -ge 1 ] ; then
    # Package upgrade, not uninstall
    for svc in compute; do
        /sbin/service %{name}-${svc} condrestart > /dev/null 2>&1 || :
    done
fi

%postun collector
if [ $1 -ge 1 ] ; then
    # Package upgrade, not uninstall
    for svc in collector; do
        /sbin/service %{name}-${svc} condrestart > /dev/null 2>&1 || :
    done
fi

%postun api
if [ $1 -ge 1 ] ; then
    # Package upgrade, not uninstall
    for svc in api; do
        /sbin/service %{name}-${svc} condrestart > /dev/null 2>&1 || :
    done
fi

%postun central
if [ $1 -ge 1 ] ; then
    # Package upgrade, not uninstall
    for svc in central; do
        /sbin/service %{name}-${svc} condrestart > /dev/null 2>&1 || :
    done
fi


%files common
%doc LICENSE
%dir %{_sysconfdir}/ceilometer
%config(noreplace) %attr(-, root, ceilometer) %{_sysconfdir}/ceilometer/ceilometer.conf
%config(noreplace) %attr(-, root, ceilometer) %{_sysconfdir}/ceilometer/policy.json
%config(noreplace) %attr(-, root, ceilometer) %{_sysconfdir}/ceilometer/sources.json
%config(noreplace) %attr(-, root, ceilometer) %{_sysconfdir}/ceilometer/pipeline.yaml
%config(noreplace) %{_sysconfdir}/logrotate.d/%{name}

%dir %attr(0755, ceilometer, root) %{_localstatedir}/log/ceilometer
%dir %attr(0755, ceilometer, root) %{_localstatedir}/run/ceilometer

%{_bindir}/ceilometer-*

%defattr(-, ceilometer, ceilometer, -)
%dir %{_sharedstatedir}/ceilometer
%dir %{_sharedstatedir}/ceilometer/tmp


%files -n python-ceilometer
%{python_sitelib}/ceilometer
%{python_sitelib}/ceilometer-%{version}*.egg-info


%if 0%{?with_doc}
%files doc
%doc doc/build/html
%endif


%files compute
%{_bindir}/ceilometer-agent-compute
%{_initrddir}/%{name}-compute
%{_datarootdir}/ceilometer/%{name}-compute.upstart


%files collector
%{_bindir}/ceilometer-collector
%{_initrddir}/%{name}-collector
%{_datarootdir}/ceilometer/%{name}-collector.upstart


%files api
%doc ceilometer/api/v1/static/LICENSE.*
%{_bindir}/ceilometer-api
%{_initrddir}/%{name}-api
%{_datarootdir}/ceilometer/%{name}-api.upstart


%files central
%{_bindir}/ceilometer-agent-central
%{_initrddir}/%{name}-central
%{_datarootdir}/ceilometer/%{name}-central.upstart


%changelog
* Thu Aug 15 2013 Stefano Zilli <stefano.zilli@cern.ch> - 2013.1.3-1
- Upgraded to 2013.1.3

* Mon Jul 22 2013 Stefano Zilli <stefano.zilli@cern.ch> - 2013.1.2-2.1
- Added cacert parameter

* Fri Jun 21 2013 Pádraig Brady <P@draigBrady.com> - 2013.1.2-2
- Avoid qpid exchange leaks

* Thu Jun  6 2013 Pádraig Brady <P@draigBrady.com> - 2013.1.2-1
- Update to stable/grizzly release 2013.1.2

* Thu Jun  6 2013 Pádraig Brady <P@draigBrady.com> - 2013.1-3
- Fix uninstall for openstack-ceilometer-central

* Mon Apr  8 2013 Pádraig Brady <P@draigBrady.com> - 2013.1-2
- Grizzly release

* Tue Mar 26 2013 Pádraig Brady <P@draigBrady.com> - 2013.1-0.5.g3
- Initial package
