Name:             python-ceilometerclient
Version:          1.0.1
Release:          3%{?dist}
Summary:          Python API and CLI for OpenStack Ceilometer

Group:            Development/Languages
License:          ASL 2.0
URL:              https://github.com/openstack/%{name}
Source0:          https://pypi.python.org/packages/source/p/%{name}/%{name}-%{version}.tar.gz

BuildArch:        noarch
BuildRequires:    python-setuptools
BuildRequires:    python2-devel
BuildRequires:    python-pbr
BuildRequires:    python-d2to1

Requires:         python-setuptools
Requires:         python-argparse
Requires:         python-prettytable
Requires:         python-iso8601
Requires:         python-keystoneclient

#
# patches_base=1.0.1
#
Patch0001: 0001-Remove-runtime-dependency-on-python-pbr.patch
Patch0002: 0002-Add-support-to-private-CA.patch

%description
This is a client library for Ceilometer built on the Ceilometer API. It
provides a Python API (the ceilometerclient module) and a command-line tool
(ceilometer).


%package doc
Summary:          Documentation for OpenStack Ceilometer API Client
Group:            Documentation

BuildRequires:    python-sphinx

%description      doc
This is a client library for Ceilometer built on the Ceilometer API. It
provides a Python API (the ceilometerclient module) and a command-line tool
(ceilometer).

This package contains auto-generated documentation.


%prep
%setup -q

%patch0001 -p1
%patch0002 -p1

# Remove the requirements file so that pbr hooks don't add it
# to distutils requiers_dist config.
rm -rf {test-,}requirements.txt tools/{pip,test}-requires

sed -i s/REDHATCEILOMETERCLIENTVERSION/%{version}/ ceilometerclient/__init__.py

# "nature" theme is not available in epel sphinx distribution
sed -i "s/^\(html_theme = 'nature'\)$/#\1/" doc/source/conf.py

%build
%{__python} setup.py build

%install
%{__python} setup.py install -O1 --skip-build --root %{buildroot}

export PYTHONPATH="$( pwd ):$PYTHONPATH"
sphinx-build -b html doc/source html

# Fix hidden-file-or-dir warnings
rm -rf html/.doctrees html/.buildinfo

%files
%doc README.md
%doc LICENSE
%{_bindir}/ceilometer
%{python_sitelib}/ceilometerclient
%{python_sitelib}/*.egg-info

%files doc
%doc html

%changelog
* Mon Aug 05 2013 Stefano Zilli <stefano.zilli@cern.ch> 1.0.1-3
- Added support to private CA

* Tue Jul 16 2013 Jakub Ruzicka <jruzicka@redhat.com> 1.0.1-2
- New build requires: python-d2to1, python-pbr.

* Tue Jul 16 2013 Jakub Ruzicka <jruzicka@redhat.com> 1.0.1-1
- Update to upstream version 1.0.1.
- Remove new runtime dependency on python-pbr.
- Remove requirements file.
- Make requires generic instead of requiring specific versions.

* Mon Apr 01 2013 Jakub Ruzicka <jruzicka@redhat.com> 1.0.0
- Update to upstream version 1.0.0.
- Added Requires: python-keystoneclient >= 0.1.2.
- 'nature' theme is not available in current sphinx version, use default.

* Tue Mar 26 2013 Jakub Ruzicka <jruzicka@redhat.com> 0.0.10-0.2.gitd84fd99
- Add BuildRequires: python2-devel.

* Tue Mar 26 2013 Jakub Ruzicka <jruzicka@redhat.com> 0.0.10-0.1.gitd84fd99
- Initial package based on python-novaclient.
