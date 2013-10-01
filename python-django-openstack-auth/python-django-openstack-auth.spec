%global pypi_name django_openstack_auth

Name:           python-django-openstack-auth
Version:        1.0.2
Release:        3%{?dist}.2
Summary:        Django authentication backend for OpenStack Keystone 

License:        BSD
URL:            http://pypi.python.org/pypi/django_openstack_auth/1.0.2
Source0:        http://pypi.python.org/packages/source/d/%{pypi_name}/%{pypi_name}-%{version}.tar.gz

# CERN Patches
Patch1000:      1000-cern-python-django-openstack-auth-ssl.patch

BuildArch:      noarch
 
BuildRequires:  python2-devel
%if 0%{?rhel}==6
BuildRequires:  python-sphinx10
%else
BuildRequires:  python-sphinx
%endif
BuildRequires:  python-mox
BuildRequires:  python-keystoneclient

%if 0%{?rhel}<7 || 0%{?fedora} < 18
%if 0%{?rhel}==6
Requires:   Django14
BuildRequires: Django14
%else
Requires:   Django
BuildRequires:   Django
%endif
%else
Requires:   python-django
BuildRequires:   python-django
%endif
 
Requires:       python-keystoneclient

%description
Django OpenStack Auth is a pluggable Django authentication backend that
works with Django's ``contrib.auth`` framework to authenticate a user against
OpenStack's Keystone Identity API.

The current version is designed to work with the
Keystone V2 API.

%prep
%setup -q -n %{pypi_name}-%{version}

# CERN Patches
%patch1000 -p0

# Remove bundled egg-info
rm -rf %{pypi_name}.egg-info

# remove unnecessary .po files
find . -name "django.po" -exec rm -f '{}' \;


%build
%{__python} setup.py build

# generate html docs 
%if 0%{?rhel}==6
PYTHONPATH=.:$PYTHONPATH sphinx-1.0-build docs html
%else
PYTHONPATH=.:$PYTHONPATH sphinx-build docs html
%endif

%install
%{__python} setup.py install --skip-build --root %{buildroot}

%if 0%{?rhel}==6
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
%else
%find_lang django
%endif
# don't include tests in the RPM
rm -rf %{buildroot}/%{python_sitelib}/openstack_auth/tests

%check
%{__python} setup.py test

%files -f django.lang
%doc README.rst LICENSE
%dir %{python_sitelib}/openstack_auth
%{python_sitelib}/openstack_auth/*.py*
%{python_sitelib}/%{pypi_name}-%{version}-py?.?.egg-info

%changelog
* Tue Feb 05 2013 Jose Castro Leon <jose.castro.leon@cern.ch> - 1.0.2-3.ai6.2
- Solve issues with SSL validation

* Tue Feb 05 2013 Jose Castro Leon <jose.castro.leon@cern.ch> - 1.0.2-3.ai6.1
- Include CERN client patch for SSL validation

* Tue Oct 16 2012 Matthias Runge <mrunge@redhat.com> - 1.0.2-3
- fix build on EPEL6, require Django14 package on EPEL6
- handle languages by hand on EL6

* Mon Sep 24 2012 Matthias Runge <mrunge@redhat.com> - 1.0.2-2
- also support f17, el6

* Tue Sep 11 2012 Matthias Runge <mrunge@redhat.com> - 1.0.2-1
- Initial package.
