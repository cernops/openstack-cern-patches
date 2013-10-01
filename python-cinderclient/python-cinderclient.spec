Name:             python-cinderclient
Version:          0.2.26
Release:          1%{?dist}.1
Summary:          Python API and CLI for OpenStack cinder

Group:            Development/Languages
License:          ASL 2.0
URL:              http://github.com/openstack/python-cinderclient
Source0:          http://tarballs.openstack.org/%{name}/%{name}-%{version}.tar.gz

# CERN Patches
Patch1000:        1000-cern-python-cinderclient-ssl.patch

#
# patches_base=0.2
#

BuildArch:        noarch
BuildRequires:    python-setuptools

Requires:         python-httplib2
Requires:         python-prettytable
Requires:         python-setuptools

%description
This is a client for the OpenStack cinder API. There's a Python API (the
cinderclient module), and a command-line script (cinder). Each implements
100% of the OpenStack cinder API.

%prep
%setup -q

# CERN SSL Patch
%patch1000 -p0

# TODO: Have the following handle multi line entries
sed -i '/setup_requires/d; /install_requires/d; /dependency_links/d' setup.py

# Remove bundled egg-info
rm -rf python_cinderclient.egg-info

%build
%{__python} setup.py build

%install
%{__python} setup.py install -O1 --skip-build --root %{buildroot}

# Delete tests
rm -fr %{buildroot}%{python_sitelib}/tests

%files
%doc README.rst
%doc LICENSE
%{_bindir}/cinder
%{python_sitelib}/cinderclient
%{python_sitelib}/*.egg-info

%changelog
* Tue Feb 05 2013 Jose Castro Leon <jose.castro.leon@cern.ch> 0.2.26-1.ai6.1
- CERN SSL Client patch

* Mon Sep 25 2012 Pádraig Brady <P@draigBrady.com> 0.2.26-1
- Update to latest client to support latest cinder

* Mon Sep  3 2012 Pádraig Brady <P@draigBrady.com> 0.2-2
- Initial release
