Name:       python-django-horizon
Version:    2013.1.3
Release:    1%{?dist}.1
Summary:    Django application for talking to Openstack

Group:      Development/Libraries
# Code in horizon/horizon/utils taken from django which is BSD
License:    ASL 2.0 and BSD
URL:        http://horizon.openstack.org/
BuildArch:  noarch
Source0:     https://launchpad.net/horizon/grizzly/%{version}/+download/horizon-%{version}.tar.gz
Source1:    openstack-dashboard.conf
Source2:    openstack-dashboard-httpd-2.4.conf

# demo config for separate logging
Source4:    openstack-dashboard-httpd-logging.conf

#
# patches_base=2013.1.3
#
Patch0001: 0001-Bump-stable-grizzly-next-version-to-2013.1.4.patch
Patch0002: 0002-disable-debug-move-web-root.patch
Patch0003: 0003-Don-t-access-the-net-while-building-docs.patch

# CERN Patches
Patch1001: 1001-cern-python-django-horizon-api-quotes.patch
Patch1002: 1002-cern-python-django-horizon-openrc-cachain.patch
Patch1003: 1003-cern-python-django-horizon-disable-floating-ips.patch
Patch1004: 1004-cern-python-django-horizon-change-help-url.patch
Patch1005: 1005-cern-python-django-horizon-ticket-url.patch
Patch1006: 1006-cern-python-django-horizon-login-buttons.patch


%if 0%{?rhel}>6 || 0%{?fedora} > 18
# grizzly requires python-django14
BuildRequires:   python-django14
Requires:   python-django14 <= 1.5

%else
# epel6 has a separate Django14 package
%if 0%{?rhel}==6
Requires:   Django14
BuildRequires:   Django14
%else
BuildRequires:   Django
Requires:   Django
%endif

%endif

Requires:   python-dateutil
Requires:   python-glanceclient
Requires:   python-keystoneclient 
Requires:   python-novaclient >= 2012.1
Requires:   python-quantumclient
Requires:   python-cinderclient
Requires:   python-swiftclient
Requires:   pytz

BuildRequires: python2-devel
BuildRequires: python-setuptools

# for checks:
#BuildRequires:   python-django-nose
#BuildRequires:   python-cinderclient
#BuildRequires:   python-django-appconf
#BuildRequires:   python-django-openstack-auth
#BuildRequires:   python-django-compressor

# additional provides to be consistent with other django packages
Provides: django-horizon = %{version}-%{release}

%description
Horizon is a Django application for providing Openstack UI components.
It allows performing site administrator (viewing account resource usage,
configuring users, accounts, quotas, flavors, etc.) and end user
operations (start/stop/delete instances, create/restore snapshots, view
instance VNC console, etc.)


%package -n openstack-dashboard
Summary:    Openstack web user interface reference implementation
Group:      Applications/System

Requires:   httpd
Requires:   mod_wsgi
Requires:   python-django-horizon >= %{version}
Requires:   python-django-openstack-auth
Requires:   python-django-compressor
Requires:   python-django-appconf

BuildRequires: python2-devel
BuildRequires: python-django-openstack-auth
BuildRequires: python-django-compressor
BuildRequires: python-django-appconf
BuildRequires: nodejs
BuildRequires: nodejs-less
BuildRequires: python-netaddr
BuildRequires: python-lockfile

BuildRequires:   pytz
%description -n openstack-dashboard
Openstack Dashboard is a web user interface for Openstack. The package
provides a reference implementation using the Django Horizon project,
mostly consisting of JavaScript and CSS to tie it altogether as a standalone
site.


%package doc
Summary:    Documentation for Django Horizon
Group:      Documentation

Requires:   %{name} = %{version}-%{release}
%if 0%{?rhel}==6
BuildRequires: python-sphinx10
%else
BuildRequires: python-sphinx >= 1.1.3
%endif

# Doc building basically means we have to mirror Requires:
BuildRequires: python-dateutil
BuildRequires: python-glanceclient
BuildRequires: python-keystoneclient
BuildRequires: python-novaclient >= 2012.1
BuildRequires: python-quantumclient
BuildRequires: python-cinderclient
BuildRequires: python-swiftclient

%description doc
Documentation for the Django Horizon application for talking with Openstack


%prep
%setup -q -n horizon-%{version}

%patch0001 -p1
%patch0002 -p1
%patch0003 -p1

# CERN Patches
%patch1001 -p1
%patch1002 -p1
%patch1003 -p1
%patch1004 -p1
%patch1005 -p1
%patch1006 -p1

# remove unnecessary .po files
find . -name "django*.po" -exec rm -f '{}' \;

# drop config snippet
cp -p %{SOURCE4} .

%build
%{__python} setup.py build

%install
%{__python} setup.py install -O1 --skip-build --root %{buildroot}

# drop httpd-conf snippet
%if 0%{?rhel} || 0%{?fedora} <18
install -m 0644 -D -p %{SOURCE1} %{buildroot}%{_sysconfdir}/httpd/conf.d/openstack-dashboard.conf
%else
# httpd-2.4 changed the syntax
install -m 0644 -D -p %{SOURCE2} %{buildroot}%{_sysconfdir}/httpd/conf.d/openstack-dashboard.conf
%endif

export PYTHONPATH="$( pwd ):$PYTHONPATH"
%if 0%{?rhel}==6
sphinx-1.0-build -b html doc/source html
%else
sphinx-build -b html doc/source html
%endif

# Fix hidden-file-or-dir warnings
rm -fr html/.doctrees html/.buildinfo

install -d -m 755 %{buildroot}%{_datadir}/openstack-dashboard
install -d -m 755 %{buildroot}%{_sharedstatedir}/openstack-dashboard
install -d -m 755 %{buildroot}%{_sysconfdir}/openstack-dashboard

# Copy everything to /usr/share
mv %{buildroot}%{python_sitelib}/openstack_dashboard \
   %{buildroot}%{_datadir}/openstack-dashboard
mv manage.py %{buildroot}%{_datadir}/openstack-dashboard
rm -rf %{buildroot}%{python_sitelib}/openstack_dashboard


# Move config to /etc, symlink it back to /usr/share
mv %{buildroot}%{_datadir}/openstack-dashboard/openstack_dashboard/local/local_settings.py.example %{buildroot}%{_sysconfdir}/openstack-dashboard/local_settings
ln -s %{_sysconfdir}/openstack-dashboard/local_settings %{buildroot}%{_datadir}/openstack-dashboard/openstack_dashboard/local/local_settings.py

%if 0%{?rhel} > 6 || 0%{?fedora} >= 16
%find_lang django
%find_lang djangojs
%else
# Handling locale files
# This is adapted from the %%find_lang macro, which cannot be directly
# used since Django locale files are not located in %%{_datadir}
#
# The rest of the packaging guideline still apply -- do not list
# locale files by hand!
(cd $RPM_BUILD_ROOT && find . -name 'django*.mo') | %{__sed} -e 's|^.||' |
%{__sed} -e \
   's:\(.*/locale/\)\([^/_]\+\)\(.*\.mo$\):%lang(\2) \1\2\3:' \
      >> django.lang
%endif

grep "\/usr\/share\/openstack-dashboard" django.lang > dashboard.lang
grep "\/site-packages\/horizon" django.lang > horizon.lang

%if 0%{?rhel} > 6 || 0%{?fedora} >= 16
cat djangojs.lang >> horizon.lang
%endif

# copy static files to %{_datadir}/openstack-dashboard/static
mkdir -p %{buildroot}%{_datadir}/openstack-dashboard/static
cp -a openstack_dashboard/static/* %{buildroot}%{_datadir}/openstack-dashboard/static
cp -a horizon/static/* %{buildroot}%{_datadir}/openstack-dashboard/static 

# compress css, js etc.
cd %{buildroot}%{_datadir}/openstack-dashboard
%{__python} manage.py collectstatic --noinput --pythonpath=../../lib/python2.6/site-packages/
%{__python} manage.py compress --pythonpath=../../lib/python2.6/site-packages/

%files -f horizon.lang
%doc LICENSE README.rst openstack-dashboard-httpd-logging.conf
%dir %{python_sitelib}/horizon
%{python_sitelib}/horizon/*.py*
%{python_sitelib}/horizon/browsers
%{python_sitelib}/horizon/conf
%{python_sitelib}/horizon/forms
%{python_sitelib}/horizon/management
%{python_sitelib}/horizon/static
%{python_sitelib}/horizon/tables
%{python_sitelib}/horizon/tabs
%{python_sitelib}/horizon/templates
%{python_sitelib}/horizon/templatetags
%{python_sitelib}/horizon/test
%{python_sitelib}/horizon/utils
%{python_sitelib}/horizon/workflows
%{python_sitelib}/*.egg-info
%exclude %{python_sitelib}/bin

%files -n openstack-dashboard -f dashboard.lang
%dir %{_datadir}/openstack-dashboard/
%{_datadir}/openstack-dashboard/*.py*
%{_datadir}/openstack-dashboard/static
%{_datadir}/openstack-dashboard/openstack_dashboard/*.py*
%{_datadir}/openstack-dashboard/openstack_dashboard/api
%{_datadir}/openstack-dashboard/openstack_dashboard/dashboards
%{_datadir}/openstack-dashboard/openstack_dashboard/local
%{_datadir}/openstack-dashboard/openstack_dashboard/openstack
%{_datadir}/openstack-dashboard/openstack_dashboard/static
%{_datadir}/openstack-dashboard/openstack_dashboard/templates
%{_datadir}/openstack-dashboard/openstack_dashboard/test
%{_datadir}/openstack-dashboard/openstack_dashboard/usage
%{_datadir}/openstack-dashboard/openstack_dashboard/wsgi
%dir %{_datadir}/openstack-dashboard/openstack_dashboard/locale
%dir %{_datadir}/openstack-dashboard/openstack_dashboard/locale/??
%dir %{_datadir}/openstack-dashboard/openstack_dashboard/locale/??_??
%dir %{_datadir}/openstack-dashboard/openstack_dashboard/locale/??/LC_MESSAGES

%{_sharedstatedir}/openstack-dashboard
%dir %attr(0750, root, apache) %{_sysconfdir}/openstack-dashboard
%config(noreplace) %{_sysconfdir}/httpd/conf.d/openstack-dashboard.conf
%config(noreplace) %attr(0640, root, apache) %{_sysconfdir}/openstack-dashboard/local_settings

%files doc
%doc html

%changelog
* Thu Aug 22 2013 Jose Castro Leon <jose.castro.leon@cern.ch> - 2013.1.3-1.slc6.1
- fix for openrc and ec2 credentials download of projects with blanks
- include CERN CA certificate chain in openrc
- disable floating IP panel and actions
- change help url to user guide
- include access to service now
- add buttons for subscribe and help in login panel

* Mon Aug 12 2013 Matthias Runge <mrunge@redhat.com> - 2013.1.3-1
- rebase to 2013.1.3

* Mon May 13 2013 Matthias Runge <mrunge@redhat.com> - 2013.1.1-1
- update to 2013.1.1 stable release
- move to compression using node.js/less

* Mon Apr 08 2013 Matthias Runge <mrunge@redhat.com> - 2013.1-1
- update to grizzly final

* Thu Mar 14 2013 Matthias Runge <mrunge@redhat.com> - 2013.1-0.7.g3
- fix compressed css (rhbz#921036)
- enable compression in httpd file
- set expires in httpd config file

* Fri Mar 08 2013 Matthias Runge <mrunge@redhat.com> - 2013.1-0.6.g3
- fix a syntax error in config file

* Wed Feb 27 2013 Matthias Runge <mrunge@redhat.com> - 2013.1-0.5.g3
- update to grizzly-3

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2013.1-0.4.g2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Sat Jan 19 2013 Matthias Runge <mrunge@redhat.com> - 2013.1-0.4.g2
- update to grizzly-2
- fix compression during build

* Mon Jan 07 2013 Matthias Runge <mrunge@redhat.com> - 2013.1-0.3.g1
- use nodejs/lessjs to compress

* Fri Dec 14 2012 Matthias Runge <mrunge@redhat.com> - 2013.1-0.2.g1
- add config example snippet to enable logging to separate files

* Thu Nov 29 2012 Matthias Runge <mrunge@redhat.com> - 2013.1-0.1.g1
- update to grizzly-1 milestone

* Tue Nov 13 2012 Matthias Runge <mrunge@redhat.com> - 2012.2-4
- drop dependency to python-cloudfiles
- fix /etc/openstack-dashboard permission CVE-2012-5474 (rhbz#873120)

* Mon Oct 22 2012 Matthias Runge <mrunge@redhat.com> - 2012.2-3
- require Django14 for EPEL6
- finally move login/logout to /dashboard/auth/login
- adapt httpd config to httpd-2.4 (bz 868408)

* Mon Oct 15 2012 Matthias Runge <mrunge@redhat.com> - 2012.2-2
- fix static img, static fonts issue

* Wed Sep 26 2012 Matthias Runge <mrunge@redhat.com> - 2012.2-0.10.rc2
- more el6 compatibility

* Tue Sep 25 2012 Matthias Runge <mrunge@redhat.com> - 2012.2-0.9.rc2
- remove %%post section

* Mon Sep 24 2012 Matthias Runge <mrunge@redhat.com> - 2012.2-0.8.rc2
- also require pytz

* Fri Sep 21 2012 Matthias Runge <mrunge@redhat.com> - 2012.2-0.7.rc2
- update to release folsom rc2

* Fri Sep 21 2012 Matthias Runge <mrunge@redhat.com> - 2012.2-0.6.rc1
- fix compressing issue

* Mon Sep 17 2012 Matthias Runge <mrunge@redhat.com> - 2012.2-0.5.rc1
- update to folsom rc1
- require python-django instead of Django
- add requirements to python-django-compressor, python-django-openstack-auth
- add requirements to python-swiftclient
- use compressed js, css files

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2012.2-0.4.f1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Tue Jun 26 2012 Matthias Runge <mrunge@matthias-runge.de> - 2012.2-0.3.f1
- add additional provides django-horizon

* Wed Jun 06 2012 Pádraig Brady <P@draigBrady.com> - 2012.2-0.2.f1
- Update to folsom milestone 1

* Wed May 09 2012 Alan Pevec <apevec@redhat.com> - 2012.1-4
- Remove the currently uneeded dependency on python-django-nose

* Thu May 03 2012 Pádraig Brady <P@draigBrady.com> - 2012.1-3
- CVE-2012-2144 session reuse vulnerability

* Tue Apr 17 2012 Pádraig Brady <P@draigBrady.com> - 2012.1-2
- CVE-2012-2094 XSS vulnerability in Horizon log viewer
- Configure the default database to use

* Mon Apr 09 2012 Cole Robinson <crobinso@redhat.com> - 2012.1-1
- Update to essex final release
- Package manage.py (bz 808219)
- Properly access all needed javascript (bz 807567)

* Sat Mar 03 2012 Cole Robinson <crobinso@redhat.com> - 2012.1-0.1.rc1
- Update to rc1 snapshot
- Drop no longer needed packages
- Change default URL to http://localhost/dashboard
- Add dep on newly packaged python-django-nose
- Fix static content viewing (patch from Jan van Eldik) (bz 788567)

* Mon Jan 30 2012 Cole Robinson <crobinso@redhat.com> - 2012.1-0.1.e3
- Initial package
