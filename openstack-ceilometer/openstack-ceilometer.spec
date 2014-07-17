%global _without_doc 1
%global with_doc %{!?_without_doc:1}%{?_without_doc:0}
%global pypi_name ceilometer

Name:             openstack-ceilometer
Version:          2014.1.1
Release:          4%{?dist}
Summary:          OpenStack measurement collection service

Group:            Applications/System
License:          ASL 2.0
URL:              https://wiki.openstack.org/wiki/Ceilometer
Source0:          http://tarballs.openstack.org/%{pypi_name}/%{pypi_name}-%{version}.tar.gz
Source1:          %{pypi_name}-dist.conf
Source2:          %{pypi_name}.logrotate

Source10:         %{name}-api.init
Source100:        %{name}-api.upstart
Source11:         %{name}-collector.init
Source110:        %{name}-collector.upstart
Source12:         %{name}-compute.init
Source120:        %{name}-compute.upstart
Source13:         %{name}-central.init
Source130:        %{name}-central.upstart
Source14:         %{name}-alarm-notifier.init
Source140:        %{name}-alarm-notifier.upstart
Source15:         %{name}-alarm-evaluator.init
Source150:        %{name}-alarm-evaluator.upstart
Source16:         %{name}-notification.init
Source160:        %{name}-notification.upstart

#
# patches_base=2014.1.1
#
Patch0001: 0001-Ensure-routing-key-is-specified-in-the-address-for-a.patch
Patch0002: 0002-remove-token-from-notifier-middleware.patch
Patch0003: 0003-Introduce-separator-parameter-in-hbase.patch
Patch0004: 0004-Patches-to-allow-icehouse-ceilometer-to-run-with-hav.patch

# This is EL6 specific and not upstream
Patch100:         openstack-ceilometer-newdeps.patch

BuildArch:        noarch
BuildRequires:    intltool
BuildRequires:    python-sphinx10
BuildRequires:    python-setuptools
BuildRequires:    python-pbr
BuildRequires:    python-d2to1
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

Requires:         python-babel
Requires:         python-eventlet
Requires:         python-greenlet
Requires:         python-iso8601
Requires:         python-lxml
Requires:         python-anyjson
Requires:         python-jsonpath-rw
Requires:         python-stevedore >= 0.14
Requires:         python-msgpack
Requires:         python-six >= 1.6
Requires:         PyYAML

Requires:         python-sqlalchemy0.7
Requires:         python-alembic
Requires:         python-migrate

Requires:         python-webob >= 1.2

Requires:         python-oslo-config >= 1:1.2.0

Requires:         pysnmp
Requires:         pytz
Requires:         python-croniter

# These were only added as global dependencies
# at the end of the Icehouse cycle with the change
# to cli.py referenced from in http://pad.lv/1317210
Requires:         python-pymongo
Requires:         python-flask
Requires:         python-pecan >= 0.4.5
Requires:         python-wsme >= 0.6
Requires:         python-novaclient
Requires:         python-keystoneclient
Requires:         python-glanceclient
Requires:         python-swiftclient
Requires:         python-ceilometerclient
Requires:         libvirt-python

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
Summary:          OpenStack ceilometer collector
Group:            Applications/System

Requires:         %{name}-common = %{version}-%{release}

# For compat with older provisioning tools.
# Remove when all reference the notification package explicitly
Requires:         %{name}-notification

Requires:         python-pymongo

%description collector
OpenStack ceilometer provides services to measure and
collect metrics from OpenStack components.

This package contains the ceilometer collector service
which collects metrics from the various agents.


%package notification
Summary:          OpenStack ceilometer notification agent
Group:            Applications/System

Requires:         %{name}-common = %{version}-%{release}

%description notification
OpenStack ceilometer provides services to measure and
collect metrics from OpenStack components.

This package contains the ceilometer notification agent
which pushes metrics to the collector service from the
various OpenStack services.


%package api
Summary:          OpenStack ceilometer API service
Group:            Applications/System

Requires:         %{name}-common = %{version}-%{release}

Requires:         python-pymongo
Requires:         python-flask
Requires:         python-pecan >= 0.4.5
Requires:         python-wsme >= 0.6

%description api
OpenStack ceilometer provides services to measure and
collect metrics from OpenStack components.

This package contains the ceilometer API service.


%package alarm
Summary:          OpenStack ceilometer alarm services
Group:            Applications/System

Requires:         %{name}-common = %{version}-%{release}
Requires:         python-ceilometerclient

%description alarm
OpenStack ceilometer provides services to measure and
collect metrics from OpenStack components.

This package contains the ceilometer alarm notification
and evaluation services.


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
%patch0004 -p1

# Apply EL6 patch
%patch100 -p1

find . \( -name .gitignore -o -name .placeholder \) -delete

find ceilometer -name \*.py -exec sed -i '/\/usr\/bin\/env python/{d;q}' {} +

# TODO: Have the following handle multi line entries
sed -i '/setup_requires/d; /install_requires/d; /dependency_links/d' setup.py

# Remove the requirements file so that pbr hooks don't add it
# to distutils requires_dist config
rm -rf {test-,}requirements.txt tools/{pip,test}-requires

# Programmatically update defaults in sample config
# which is installed at /etc/ceilometer/ceilometer.conf
# TODO: Make this more robust
# Note it only edits the first occurance, so assumes a section ordering in sample
# and also doesn't support multi-valued variables.
while read name eq value; do
  test "$name" && test "$value" || continue
  sed -i "0,/^# *$name=/{s!^# *$name=.*!#$name=$value!}" etc/ceilometer/ceilometer.conf.sample
done < %{SOURCE1}

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
install -p -D -m 640 %{SOURCE1} %{buildroot}%{_datadir}/ceilometer/ceilometer-dist.conf
install -p -D -m 640 etc/ceilometer/ceilometer.conf.sample %{buildroot}%{_sysconfdir}/ceilometer/ceilometer.conf
install -p -D -m 640 etc/ceilometer/policy.json %{buildroot}%{_sysconfdir}/ceilometer/policy.json
install -p -D -m 640 etc/ceilometer/sources.json %{buildroot}%{_sysconfdir}/ceilometer/sources.json
install -p -D -m 640 etc/ceilometer/pipeline.yaml %{buildroot}%{_sysconfdir}/ceilometer/pipeline.yaml

# Install initscripts for services
install -p -D -m 755 %{SOURCE10} %{buildroot}%{_initrddir}/%{name}-api
install -p -D -m 755 %{SOURCE11} %{buildroot}%{_initrddir}/%{name}-collector
install -p -D -m 755 %{SOURCE12} %{buildroot}%{_initrddir}/%{name}-compute
install -p -D -m 755 %{SOURCE13} %{buildroot}%{_initrddir}/%{name}-central
install -p -D -m 755 %{SOURCE14} %{buildroot}%{_initrddir}/%{name}-alarm-notifier
install -p -D -m 755 %{SOURCE15} %{buildroot}%{_initrddir}/%{name}-alarm-evaluator
install -p -D -m 755 %{SOURCE16} %{buildroot}%{_initrddir}/%{name}-notification

# Install upstart jobs examples
install -d -m 755 %{buildroot}%{_datadir}/ceilometer
install -p -m 644 %{SOURCE100} %{buildroot}%{_datadir}/ceilometer/
install -p -m 644 %{SOURCE110} %{buildroot}%{_datadir}/ceilometer/
install -p -m 644 %{SOURCE120} %{buildroot}%{_datadir}/ceilometer/
install -p -m 644 %{SOURCE130} %{buildroot}%{_datadir}/ceilometer/
install -p -m 644 %{SOURCE140} %{buildroot}%{_datadir}/ceilometer/
install -p -m 644 %{SOURCE150} %{buildroot}%{_datadir}/ceilometer/
install -p -m 644 %{SOURCE160} %{buildroot}%{_datadir}/ceilometer/

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

%post notification
if [ $1 -eq 1 ] ; then
    # Initial installation
    /sbin/chkconfig --add %{name}-notification
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

%post alarm
if [ $1 -eq 1 ] ; then
    # Initial installation
    for svc in alarm-notifier alarm-evaluator; do
        /sbin/chkconfig --add %{name}-${svc}
    done
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

%preun notification
if [ $1 -eq 0 ] ; then
    for svc in notification; do
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

%preun alarm
if [ $1 -eq 0 ] ; then
    for svc in alarm-notifier alarm-evaluator; do
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

%postun notification
if [ $1 -ge 1 ] ; then
    # Package upgrade, not uninstall
    for svc in notification; do
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

%postun alarm
/bin/systemctl daemon-reload >/dev/null 2>&1 || :
if [ $1 -ge 1 ] ; then
    # Package upgrade, not uninstall
    for svc in alarm-notifier alarm-evaluator; do
        /sbin/service %{name}-${svc} condrestart > /dev/null 2>&1 || :
    done
fi


%files common
%doc LICENSE
%dir %{_sysconfdir}/ceilometer
%attr(-, root, ceilometer) %{_datadir}/ceilometer/ceilometer-dist.conf
%config(noreplace) %attr(-, root, ceilometer) %{_sysconfdir}/ceilometer/ceilometer.conf
%config(noreplace) %attr(-, root, ceilometer) %{_sysconfdir}/ceilometer/policy.json
%config(noreplace) %attr(-, root, ceilometer) %{_sysconfdir}/ceilometer/sources.json
%config(noreplace) %attr(-, root, ceilometer) %{_sysconfdir}/ceilometer/pipeline.yaml
%config(noreplace) %{_sysconfdir}/logrotate.d/%{name}

%dir %attr(0755, ceilometer, root) %{_localstatedir}/log/ceilometer
%dir %attr(0755, ceilometer, root) %{_localstatedir}/run/ceilometer

%{_bindir}/ceilometer-dbsync
%{_bindir}/ceilometer-expirer
%{_bindir}/ceilometer-send-sample


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
%{_bindir}/ceilometer-collector*
%{_initrddir}/%{name}-collector
%{_datarootdir}/ceilometer/%{name}-collector.upstart


%files notification
%{_bindir}/ceilometer-agent-notification
%{_initrddir}/%{name}-notification
%{_datarootdir}/ceilometer/%{name}-notification.upstart


%files api
%doc ceilometer/api/v1/static/LICENSE.*
%{_bindir}/ceilometer-api
%{_initrddir}/%{name}-api
%{_datarootdir}/ceilometer/%{name}-api.upstart


%files central
%{_bindir}/ceilometer-agent-central
%{_initrddir}/%{name}-central
%{_datarootdir}/ceilometer/%{name}-central.upstart


%files alarm
%{_bindir}/ceilometer-alarm-notifier
%{_bindir}/ceilometer-alarm-evaluator
%{_initrddir}/%{name}-alarm-notifier
%{_datarootdir}/ceilometer/%{name}-alarm-notifier.upstart
%{_initrddir}/%{name}-alarm-evaluator
%{_datarootdir}/ceilometer/%{name}-alarm-evaluator.upstart


%changelog
* Wed Jun 11 2014 Steve Linabery <slinaber@redhat.com> - 2014.1.1-2
- Update to upstream 2014.1.1
- fix message routing with newer QPID (rhbz#1103800)

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2014.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Wed May 07 2014 Pádraig Brady <pbrady@redhat.com> - 2014.1-2
- Avoid dependency issues with distributed installs (#1095414)

* Thu Apr 17 2014 Pádraig Brady <pbrady@redhat.com> - 2014.1-1
- Update to Icehouse release

* Fri Apr 11 2014 Pádraig Brady <pbrady@redhat.com> - 2014.1-0.7.rc2
- Update to upstream 2014.1.rc2
- Remove qpid as default rpc backend
- Split out openstack-ceilometer-notification subpackage from collector

* Mon Mar 31 2014 Pádraig Brady <P@draigBrady.com> 2014.1-0.6.rc1
- Update to upstream 2014.1.rc1

* Fri Mar 14 2014 Pádraig Brady <pbrady@redhat.com> - 2014.1-0.5.b3
- Update to Icehouse milestone 3

* Tue Feb 04 2014 Pádraig Brady <pbrady@redhat.com> - 2014.1-0.4.b2
- Fix missing dependency on python-babel

* Mon Jan 27 2014 Pádraig Brady <pbrady@redhat.com> - 2014.1-0.3.b2
- Update to Icehouse milestone 2

* Mon Jan 06 2014 Pádraig Brady <pbrady@redhat.com> - 2014.1-0.2.b1
- Set python-six min version to ensure updated

* Mon Dec 23 2013 Pádraig Brady <pbrady@redhat.com> - 2014.1-0.1.b1
- Update to Icehouse milestone 1

* Tue Dec 17 2013 Pádraig Brady <pbrady@redhat.com> - 2013.2.1-1
- Update to Havana stable release 2013.2.1

* Thu Oct 17 2013 Pádraig Brady <pbrady@redhat.com> - 2013.2-1
- Update to Havana release

* Tue Oct 15 2013 Pádraig Brady <pbrady@redhat.com> - 2013.2-0.12.rc2
- Update to Havana rc2
- openstack-ceilometer-alarm now depends on python-ceilometerclient

* Thu Oct 03 2013 Pádraig Brady <pbrady@redhat.com> - 2013.2-0.12.rc1
- Update to Havana rc1
- Separate out the new alarm services to the 'alarm' subpackage

* Fri Sep 13 2013 Pádraig Brady <pbrady@redhat.com> - 2013.2-0.10.b3
- Depend on python-oslo-config >= 1:1.2.0 so it upgraded automatically

* Mon Sep 10 2013 Pádraig Brady <pbrady@redhat.com> - 2013.2-0.8.b3
- Depend on python-pymongo rather than pymongo to avoid a puppet bug

* Mon Sep 9 2013 Pádraig Brady <pbrady@redhat.com> - 2013.2-0.7.b3
- Depend on python-alembic

* Mon Sep 9 2013 Pádraig Brady <pbrady@redhat.com> - 2013.2-0.6.b3
- Distribute dist defaults in ceilometer-dist.conf separate to user ceilometer.conf

* Mon Sep 9 2013 Pádraig Brady <pbrady@redhat.com> - 2013.2-0.5.b3
- Update to Havana milestone 3

* Tue Aug 27 2013 Pádraig Brady <pbrady@redhat.com> - 2013.2-0.4.b1
- Avoid python runtime dependency management

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2013.2-0.3.b1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Jun  6 2013 Pádraig Brady <P@draigBrady.com> - 2013.2-0.2.b1
- Fix uninstall for openstack-ceilometer-central

* Fri May 31 2013 Pádraig Brady <P@draigBrady.com> - 2013.2-0.1.b1
- Havana milestone 1

* Mon Apr  8 2013 Pádraig Brady <P@draigBrady.com> - 2013.1-2
- Grizzly release

* Tue Mar 26 2013 Pádraig Brady <P@draigBrady.com> - 2013.1-0.5.g3
- Initial package
