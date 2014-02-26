#
# This is 2013.2.2 Havana stable release
#
%global release_name havana

%global with_doc %{!?_without_doc:1}%{?_without_doc:0}

Name:           openstack-keystone
Version:        2013.2.2
Release:        1%{?dist}.3
Summary:        OpenStack Identity Service

License:        ASL 2.0
URL:            http://keystone.openstack.org/
Source0:        http://launchpad.net/keystone/%{release_name}/%{version}/+download/keystone-%{version}.tar.gz
Source1:        openstack-keystone.logrotate
Source2:        openstack-keystone.init
Source3:        openstack-keystone.upstart
Source5:        openstack-keystone-sample-data
Source20:       keystone-dist.conf
Source21:       daemon_notify.sh


#
# patches_base=2013.2.2
#
Patch0001: 0001-remove-runtime-dep-on-python-pbr.patch
Patch0002: 0002-sync-parameter-values-with-keystone-dist.conf.patch
Patch0003: 0003-Use-updated-parallel-install-versions-of-epel-packag.patch
Patch0004: 0004-improve-systemd-onready-notification.patch

# CERN Patches
Patch1001: 1001-cern-openstack-keystone-fix-ldap-v3.patch
Patch1002: 1002-cern-openstack-keystone-fix-ldap-gettoken.patch
Patch1003: 1003-cern-openstack-keystone-ldap-nested-groups.patch

BuildArch:      noarch

BuildRequires:  python2-devel
BuildRequires:  python-sphinx10
BuildRequires:  python-oslo-sphinx
BuildRequires:  python-pbr
BuildRequires:  python-d2to1
# These are required to build due to the requirements check added
BuildRequires:  python-sqlalchemy0.7
BuildRequires:  python-webob1.2
BuildRequires:  python-paste-deploy1.5
BuildRequires:  python-routes1.12

Requires:       python-keystone = %{version}-%{release}
Requires:       python-keystoneclient >= 1:0.3.0

Requires(post):   chkconfig
Requires(postun): initscripts
Requires(preun):  chkconfig
Requires(preun):  initscripts
Requires(pre):    shadow-utils

# for daemon_notify
Requires: /usr/bin/uuidgen
Requires: /bin/sleep

%description
Keystone is a Python implementation of the OpenStack
(http://www.openstack.org) identity service API.

This package contains the Keystone daemon.

%package -n       python-keystone
Summary:          Keystone Python libraries
Group:            Applications/System

Requires:       python-eventlet
Requires:       python-ldap
Requires:       python-lxml
Requires:       python-memcached
Requires:       python-migrate
Requires:       python-paste-deploy1.5
Requires:       python-routes1.12
Requires:       python-sqlalchemy0.7
Requires:       python-webob1.2
Requires:       python-passlib
Requires:       python-setuptools
Requires:       MySQL-python
Requires:       PyPAM
Requires:       python-iso8601
Requires:       python-oslo-config >= 1:1.2.0
Requires:       openssl
Requires:       python-netaddr
Requires:       python-six
Requires:       python-babel >= 0.9.4
Requires:       python-oauth2
Requires:       python-dogpile-cache >= 0.5.0

%description -n   python-keystone
Keystone is a Python implementation of the OpenStack
(http://www.openstack.org) identity service API.

This package contains the Keystone Python library.

%if 0%{?with_doc}
%package doc
Summary:        Documentation for OpenStack Identity Service
Group:          Documentation

%description doc
Keystone is a Python implementation of the OpenStack
(http://www.openstack.org) identity service API.

This package contains documentation for Keystone.
%endif

%prep
%setup -q -n keystone-%{version}

%patch0001 -p1
%patch0002 -p1
%patch0003 -p1
%patch0004 -p1

# Apply CERN Patches
%patch1001 -p1
%patch1002 -p1
%patch1003 -p1

find . \( -name .gitignore -o -name .placeholder \) -delete
find keystone -name \*.py -exec sed -i '/\/usr\/bin\/env python/d' {} \;
# Remove bundled egg-info
rm -rf keystone.egg-info

# Remove dependency on pbr and set version as per rpm
sed -i s/REDHATKEYSTONEVERSION/%{version}/ bin/keystone-all keystone/cli.py


%build
cp etc/keystone.conf.sample etc/keystone.conf
# distribution defaults are located in keystone-dist.conf

%{__python} setup.py build

%install
%{__python} setup.py install --skip-build --root %{buildroot}

# Delete tests
rm -fr %{buildroot}%{python_sitelib}/tests
rm -fr %{buildroot}%{python_sitelib}/run_tests.*

install -d -m 755 %{buildroot}%{_sysconfdir}/keystone
install -p -D -m 640 etc/keystone.conf %{buildroot}%{_sysconfdir}/keystone/keystone.conf
install -p -D -m 644 etc/keystone-paste.ini %{buildroot}%{_datadir}/keystone/keystone-dist-paste.ini
install -p -D -m 644 %{SOURCE20} %{buildroot}%{_datadir}/keystone/keystone-dist.conf
install -p -D -m 640 etc/logging.conf.sample %{buildroot}%{_sysconfdir}/keystone/logging.conf
install -p -D -m 640 etc/default_catalog.templates %{buildroot}%{_sysconfdir}/keystone/default_catalog.templates
install -p -D -m 640 etc/policy.json %{buildroot}%{_sysconfdir}/keystone/policy.json
install -p -D -m 644 %{SOURCE1} %{buildroot}%{_sysconfdir}/logrotate.d/openstack-keystone
install -p -D -m 755 %{SOURCE2} %{buildroot}%{_initrddir}/openstack-keystone
# Install sample data script.
install -p -D -m 755 tools/sample_data.sh %{buildroot}%{_datadir}/keystone/sample_data.sh
# Install service readiness wrapper
install -p -D -m 755 %{SOURCE21} %{buildroot}%{_datadir}/keystone/daemon_notify.sh
install -p -D -m 644 %{SOURCE3} %{buildroot}%{_datadir}/keystone/%{name}.upstart
install -p -D -m 755 %{SOURCE5} %{buildroot}%{_bindir}/openstack-keystone-sample-data
# Install sample HTTPD integration files
install -p -D -m 644 httpd/keystone.py  %{buildroot}%{_datadir}/keystone/keystone.wsgi
install -p -D -m 644 httpd/wsgi-keystone.conf  %{buildroot}%{_datadir}/keystone/

install -d -m 755 %{buildroot}%{_sharedstatedir}/keystone
install -d -m 755 %{buildroot}%{_localstatedir}/log/keystone
install -d -m 755 %{buildroot}%{_localstatedir}/run/keystone

# docs generation requires everything to be installed first
export PYTHONPATH="$( pwd ):$PYTHONPATH"
pushd doc
if [ -x /usr/bin/sphinx-apidoc ]; then
    make html
    make man
else
    make html SPHINXAPIDOC=echo SPHINXBUILD=sphinx-1.0-build
    make man SPHINXAPIDOC=echo SPHINXBUILD=sphinx-1.0-build
fi
mkdir -p %{buildroot}%{_mandir}/man1
install -p -D -m 644 build/man/*.1 %{buildroot}%{_mandir}/man1/
popd
# Fix hidden-file-or-dir warnings
rm -fr doc/build/html/.doctrees doc/build/html/.buildinfo

%pre
# 163:163 for keystone (openstack-keystone) - rhbz#752842
getent group keystone >/dev/null || groupadd -r --gid 163 keystone
getent passwd keystone >/dev/null || \
useradd --uid 163 -r -g keystone -d %{_sharedstatedir}/keystone -s /sbin/nologin \
-c "OpenStack Keystone Daemons" keystone
exit 0

%post
if [ $1 -eq 1 ] ; then
    # Initial installation
%if 0%{?fedora} >= 15
    /bin/systemctl daemon-reload >/dev/null 2>&1 || :
%else
    /sbin/chkconfig --add openstack-keystone
%endif
fi

%preun
if [ $1 -eq 0 ] ; then
    # Package removal, not upgrade
%if 0%{?fedora} >= 15
    /bin/systemctl --no-reload disable openstack-keystone.service > /dev/null 2>&1 || :
    /bin/systemctl stop openstack-keystone.service > /dev/null 2>&1 || :
%else
    /sbin/service openstack-keystone stop >/dev/null 2>&1
    /sbin/chkconfig --del openstack-keystone
%endif
fi

%postun
/bin/systemctl daemon-reload >/dev/null 2>&1 || :
if [ $1 -ge 1 ] ; then
    # Package upgrade, not uninstall
%if 0%{?fedora} >= 15
    /bin/systemctl try-restart openstack-keystone.service >/dev/null 2>&1 || :
%else
    /sbin/service openstack-keystone condrestart >/dev/null 2>&1 || :
%endif
fi

%files
%doc LICENSE
%doc README.rst
%{_mandir}/man1/keystone*.1.gz
%{_bindir}/keystone-all
%{_bindir}/keystone-manage
%{_bindir}/openstack-keystone-sample-data
%dir %{_datadir}/keystone
%attr(0644, root, keystone) %{_datadir}/keystone/keystone-dist.conf
%attr(0644, root, keystone) %{_datadir}/keystone/keystone-dist-paste.ini
%attr(0755, root, root) %{_datadir}/keystone/sample_data.sh
%attr(0755, root, root) %{_datadir}/keystone/daemon_notify.sh
%{_datadir}/keystone/%{name}.upstart
%{_initrddir}/openstack-keystone
%attr(0644, root, keystone) %{_datadir}/keystone/keystone.wsgi
%attr(0644, root, keystone) %{_datadir}/keystone/wsgi-keystone.conf
%dir %attr(0750, root, keystone) %{_sysconfdir}/keystone
%config(noreplace) %attr(0640, root, keystone) %{_sysconfdir}/keystone/keystone.conf
%config(noreplace) %attr(0640, root, keystone) %{_sysconfdir}/keystone/logging.conf
%config(noreplace) %attr(0640, root, keystone) %{_sysconfdir}/keystone/default_catalog.templates
%config(noreplace) %attr(0640, keystone, keystone) %{_sysconfdir}/keystone/policy.json
%config(noreplace) %{_sysconfdir}/logrotate.d/openstack-keystone
%dir %attr(-, keystone, keystone) %{_sharedstatedir}/keystone
%dir %attr(0750, keystone, keystone) %{_localstatedir}/log/keystone
%dir %attr(-, keystone, keystone) %{_localstatedir}/run/keystone

%files -n python-keystone
%defattr(-,root,root,-)
%doc LICENSE
%{python_sitelib}/keystone
%{python_sitelib}/keystone-%{version}-*.egg-info

%if 0%{?with_doc}
%files doc
%doc LICENSE doc/build/html
%endif

%changelog
* Tue Feb 25 2014 Jose Castro Leon <jose.castro.leon@cern.ch> 2013.2.2-1.slc6.3
- added performance improvement in nested group search

* Tue Feb 25 2014 Jose Castro Leon <jose.castro.leon@cern.ch> 2013.2.2-1.slc6.2
- fixes on list groups assignments on LDAP

* Tue Feb 17 2014 Jose Castro Leon <jose.castro.leon@cern.ch> 2013.2.2-1.slc6.1
- backport patch to enable nested groups on LDAP
- backport patch to enable v3 get token on LDAP

* Fri Feb 14 2014 Alan Pevec <apevec@redhat.com> 2013.2.2-1
- updated to stable havana 2013.2.2 release

* Fri Jan 10 2014 Alan Pevec <apevec@redhat.com> 2013.2.1-2
- use service readiness notification in initscript rhbz#1036515

* Tue Dec 17 2013 Alan Pevec <apevec@redhat.com> 2013.2.1-1
- updated to stable havana 2013.2.1 release CVE-2013-6391

* Wed Oct 30 2013 Alan Pevec <apevec@redhat.com> 2013.2-2
- unintentional role granting with Keystone LDAP backend CVE-2013-4477

* Thu Oct 17 2013 Alan Pevec <apevec@redhat.com> - 2013.2-1
- Update to havana final

* Mon Oct 07 2013 Alan Pevec <apevec@redhat.com> - 2013.2-0.14.rc1
- rename HTTPD integration to keystone.wsgi
- HTTPD integration files
- Havana release candidate

* Wed Sep 11 2013 Alan Pevec <apevec@redhat.com> - 2013.2-0.11.b3
- require webob1.2 rhbz#1006768

* Mon Sep 09 2013 Alan Pevec <apevec@redhat.com> - 2013.2-0.10.b3
- havana-3 milestone
- drop pbr run-time dependency
- set distribution defaults in keystone-dist.conf

* Tue Jul 23 2013 pbrady@redhat.com 2013.2-0.5.b2
- Ensure service start waits until service is available

* Thu Jul 18 2013 pbrady@redhat.com 2013.2-0.4.b2
- havana-2 milestone

* Mon Jun 24 2013 apevec@redhat.com 2013.2-0.3.b1
- restrict /var/log/keystone/ rhbz#956814

* Sat Jun 22 2013 apevec@redhat.com 2013.2-0.2.b1
- Force simple Bind for authentication CVE-2013-2157

* Fri Jun 07 2013 Alan Pevec <apevec@redhat.com> 2013.2-0.1.h1
- havana-1 milestone

* Fri May 10 2013 Alan Pevec <apevec@redhat.com> 2013.1.1-1
- updated to stable grizzly 2013.1.1 release CVE-2013-2006 CVE-2013-2059

* Thu Apr 04 2013 Alan Pevec <apevec@redhat.com> 2013.1-1
- Update to grizzly final

* Wed Apr 03 2013 Alan Pevec <apevec@redhat.com> 2013.1-0.10.rc3
- grizzly rc3

* Fri Mar 29 2013 Alan Pevec <apevec@redhat.com> 2013.1-0.9.rc2
- grizzly rc2

* Wed Mar 20 2013 Pádraig Brady <pbrady@redhat.com> 2013.1-0.8.g3
- fix a grizzly issue with int/str config mismatch

* Mon Mar 11 2013 Alan Pevec <apevec@redhat.com> 2013.1-0.7.g3
- openssl is required for PKI tokens rhbz#918757

* Mon Mar 11 2013 Alan Pevec <apevec@redhat.com> 2013.1-0.6.g3
- remove python-sqlalchemy restriction

* Sun Feb 24 2013 Alan Pevec <apevec@redhat.com> 2013.1-0.5.g3
- update dependencies

* Sat Feb 23 2013 Alan Pevec <apevec@redhat.com> 2013.1-0.4.g3
- grizzly-3 milestone

* Fri Jan 11 2013 Alan Pevec <apevec@redhat.com> 2013.1-0.2.g2
- grizzly-2 milestone

* Mon Dec 03 2012 Alan Pevec <apevec@redhat.com> 2013.1-0.1.g1
- grizzly-1 milestone

* Wed Nov 28 2012 Alan Pevec <apevec@redhat.com> 2012.2.1-1
- updated to stable folsom release 2012.2.1 CVE-2012-5563 CVE-2012-5571

* Fri Nov 16 2012 Alan Pevec <apevec@redhat.com> 2012.2-5
- fix /etc/keystone directory permission CVE-2012-5483 (rhbz#873447)

* Mon Nov 12 2012 Alan Pevec <apevec@redhat.com> 2012.2-4
- readd iso8601 dependency (from openstack-common timeutils)

* Fri Nov 09 2012 Alan Pevec <apevec@redhat.com> 2012.2-3
- remove auth-token subpackage (rhbz#868357)

* Thu Nov 08 2012 Alan Pevec <apevec@redhat.com> 2012.2-2
- Fix default port for identity.internalURL in sample script

* Thu Oct 18 2012 Alan Pevec <apevec@redhat.com> 2012.2-1
- Update to folsom

* Fri Oct 12 2012 Alan Pevec <apevec@redhat.com> 2012.1.3-1
- updated to stable essex release 2012.1.3

* Sun Sep 16 2012 Alan Pevec <apevec@redhat.com> 2012.1.2-4
- Limit token revocation to tenant (lp#1050025)

* Wed Sep 12 2012 Alan Pevec <apevec@redhat.com> 2012.1.2-3
- Delete user tokens after role grant/revoke (CVE-2012-4413)

* Thu Aug 30 2012 Alan Pevec <apevec@redhat.com> 2012.1.2-2
- Require authz to update user's tenant (CVE-2012-3542)

* Mon Aug 13 2012 Alan Pevec <apevec@redhat.com> 2012.1.2-1
- updated to stable essex release 2012.1.2

* Fri Jun 22 2012 Alan Pevec <apevec@redhat.com> 2012.1.1-1
- updated to stable essex release 2012.1.1 (CVE-2012-3426)

* Thu Jun 21 2012 Alan Pevec <apevec@redhat.com> 2012.1-9
- add upstart job, alternative to sysv initscript

* Fri Jun 15 2012 Alan Pevec <apevec@redhat.com> 2012.1-8
- fix upgrade case with python-keystone-auth-token (rhbz#824034#c20)

* Mon Jun 11 2012 Alan Pevec <apevec@redhat.com> 2012.1-7
- Corrects url conversion in export_legacy_catalog (lp#994936)
- Invalidate user tokens when password is changed (lp#996595)
- Invalidate user tokens when a user is disabled (lp#997194)
- Carrying over token expiry time when token chaining (lp#998185)

* Tue May 29 2012 Alan Pevec <apevec@redhat.com> 2012.1-6
- python-keystone-auth-token subpackage (rhbz#824034)
- use reserved user id for keystone (rhbz#752842)
- fix paste.deploy dependency (rhbz#826120)

* Mon May 21 2012 Alan Pevec <apevec@redhat.com> 2012.1-5
- Sync up with Essex stable branch
- Remove dependencies no loner needed by Essex

* Tue May 01 2012 Pádraig Brady <P@draigBrady.com> 2012.1-4
- Start the services later in the boot sequence

* Sun Apr 29 2012 Pádraig Brady <P@draigBrady.com> 2012.1-3
- Add the lookup for the parallel install of python-routes

* Thu Apr 26 2012 Pádraig Brady <P@draigBrady.com> 2012.1-2
- Use parallel installed versions of python-paste-deploy and python-routes

* Thu Apr 05 2012 Alan Pevec <apevec@redhat.com> 2012.1-1
- Essex release

* Wed Apr 04 2012 Alan Pevec <apevec@redhat.com> 2012.1-0.13.rc2
- essex rc2

* Sat Mar 24 2012 Alan Pevec <apevec@redhat.com> 2012.1-0.12.rc1
- update to final essex rc1

* Wed Mar 21 2012 Alan Pevec <apevec@redhat.com> 2012.1-0.11.rc1
- essex rc1

* Thu Mar 08 2012 Alan Pevec <apevec@redhat.com> 2012.1-0.10.e4
- change default catalog backend to sql rhbz#800704
- update sample-data script
- add missing keystoneclient dependency

* Thu Mar 01 2012 Alan Pevec <apevec@redhat.com> 2012.1-0.9.e4
- essex-4 milestone
- change default database to mysql
- switch all backends to sql
- separate library to python-keystone

* Sun Dec 04 2011 Alan Pevec <apevec@redhat.com> 2011.3.1-4
- fix initscript for keystone

* Wed Nov 30 2011 Alan Pevec <apevec@redhat.com> 2011.3.1-3
- Use updated parallel install versions of epel packages (pbrady)
- Ensure the docs aren't built with the system glance module (pbrady)
- Ensure we don't access the net when building docs (pbrady)

* Thu Nov 24 2011 Alan Pevec <apevec@redhat.com> 2011.3.1-2
- include LICENSE, update package description from README.md

* Mon Nov 21 2011 Alan Pevec <apevec@redhat.com> 2011.3.1-1
- Update to 2011.3.1 stable/diablo release

* Fri Nov 11 2011 Alan Pevec <apevec@redhat.com> 2011.3-2
- Update to the latest stable/diablo snapshot

* Fri Oct 21 2011 David Busby <oneiroi@fedoraproject.com> - 2011.3-1
- Update to Diablo Final d3

* Wed Oct 19 2011 Matt Domsch <Matt_Domsch@dell.com> - 1.0-0.4.d4.1213
- add Requires: python-passlib

* Mon Oct 3 2011 Matt Domsch <Matt_Domsch@dell.com> - 1.0-0.2.d4.1213
- update to diablo release.
- BR systemd-units for _unitdir

* Fri Sep  2 2011 Mark McLoughlin <markmc@redhat.com> - 1.0-0.2.d4.1078
- Use upstream snapshot tarball
- No need to define python_sitelib anymore
- BR python2-devel
- Remove BRs only needed for unit tests
- No need to clean buildroot in install anymore
- Use slightly more canonical site for URL tag
- Prettify the requires tags
- Cherry-pick tools.tracer patch from upstream
- Add config file
- Add keystone user and group
- Ensure log file is in /var/log/keystone
- Ensure the sqlite db is in /var/lib/keystone
- Add logrotate support
- Add system units

* Thu Sep  1 2011 Matt Domsch <Matt_Domsch@dell.com> - 1.0-0.1.20110901git396f0bfd%{?dist}
- initial packaging
