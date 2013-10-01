Name:             python-novaclient
Epoch:            1
Version:          2.10.0
Release:          2%{?dist}.1
Summary:          Python API and CLI for OpenStack Nova

Group:            Development/Languages
License:          ASL 2.0
URL:              http://pypi.python.org/pypi/python-novaclient
Source0:          http://tarballs.openstack.org/%{name}/%{name}-%{version}.tar.gz

# CERN Patches
Patch1000:        1000-cern-python-novaclient-ssl.patch

BuildArch:        noarch
BuildRequires:    python-setuptools

Requires:         python-argparse
Requires:         python-simplejson
Requires:         python-httplib2
Requires:         python-prettytable
Requires:         python-setuptools
Requires:         python-iso8601

%description
This is a client for the OpenStack Nova API. There's a Python API (the
novaclient module), and a command-line script (nova). Each implements 100% of
the OpenStack Nova API.

%package doc
Summary:          Documentation for OpenStack Nova API Client
Group:            Documentation

BuildRequires:    python-sphinx10

%description      doc
This is a client for the OpenStack Nova API. There's a Python API (the
novaclient module), and a command-line script (nova). Each implements 100% of
the OpenStack Nova API.

This package contains auto-generated documentation.

%prep
%setup -q

# CERN SSL Patch
%patch1000 -p0

# TODO: Have the following handle multi line entries
sed -i '/setup_requires/d; /install_requires/d; /dependency_links/d' setup.py

%build
%{__python} setup.py build

%install
%{__python} setup.py install -O1 --skip-build --root %{buildroot}
mv %{buildroot}/usr/novaclient/versioninfo %{buildroot}%{python_sitelib}/novaclient/versioninfo

mkdir -p %{buildroot}%{_sysconfdir}/bash_completion.d
install -pm 644 tools/nova.bash_completion %{buildroot}%{_sysconfdir}/bash_completion.d/nova

# Delete tests
rm -fr %{buildroot}%{python_sitelib}/tests

export PYTHONPATH="$( pwd ):$PYTHONPATH"
sphinx-1.0-build -b html doc/source html

# Fix hidden-file-or-dir warnings
rm -fr html/.doctrees html/.buildinfo

%files
%doc README.rst
%doc LICENSE
%{_bindir}/nova
%{python_sitelib}/novaclient
%{python_sitelib}/*.egg-info
%{_sysconfdir}/bash_completion.d

%files doc
%doc html

%changelog
* Mon Feb 04 2013 Jose Castro Leon <jose.castro.leon@cern.ch> 2.10.0-2.ai6.1
- CERN SSL Client patch

* Fri Dec 21 2012 Alan Pevec <apevec@redhat.com> 2.10.0-2
- Include bash_completion file (#872544) (Alvaro Lopez Ortega)
- Add dependency on python-iso8601 (#881515)

* Mon Dec 03 2012 Alan Pevec <apevec@redhat.com> 2.10.0-1
- Update to latest upstream release

* Thu Sep 27 2012 Pádraig Brady <P@draigBrady.com> 1:2.9.0-1
- Update to latest upstream release (aligned with Folsom)

* Wed Aug 22 2012 Pádraig Brady <P@draigBrady.com> 2012.1-2
- Add dependency on python-setuptools (#849477)

* Sun Apr 13 2012 Pádraig Brady <P@draigBrady.com> 2012.1-1
- Update to essex release
- Include LICENSE (#732695)

* Tue Aug 30 2011 Matt Domsch <mdomsch@fedoraproject.org> - 2.6.1-0.5.89bzr
- trivial changes for el6

* Wed Aug 24 2011 Mark McLoughlin <markmc@redhat.com> - 2.6.1-0.4.89bzr
- Update to latest upstream snapshot
- Don't use %%setup -n (#732694)

* Mon Aug 22 2011 Mark McLoughlin <markmc@redhat.com> - 2.6.1-0.3.83bzr
- Remove python-devel BR
- Remove the openstack-novaclient sub-package

* Fri Aug 19 2011 Mark McLoughlin <markmc@redhat.com> - 2.6.1-0.2.83bzr
- Remove argparse from egg requires.txt; no egg info for argparse available

* Wed Aug 17 2011 Mark McLoughlin <markmc@redhat.com> - 2.6.1-0.1.83bz
- Update to latest upstream

* Wed Aug 10 2011 Mark McLoughlin <markmc@redhat.com> - 2.6.1-0.1.74bzr
- Update to latest upstream

* Mon Aug  8 2011 Mark McLoughlin <markmc@redhat.com> - 2.5.1-1
- Initial package from Alexander Sakhnov <asakhnov@mirantis.com>
  with cleanups by Mark McLoughlin
