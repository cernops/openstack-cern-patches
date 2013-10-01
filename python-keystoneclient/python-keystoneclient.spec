Name:       python-keystoneclient
# Since folsom-2 OpenStack clients follow their own release plan
# and restarted version numbering from 0.1.1
# https://lists.launchpad.net/openstack/msg14248.html
Epoch:      1
Version:    0.1.3.27
Release:    1%{?dist}.2
Summary:    Python API and CLI for OpenStack Keystone

Group:      Development/Languages
License:    ASL 2.0
URL:        https://github.com/openstack/python-keystoneclient
BuildArch:  noarch

#Source0:    https://launchpad.net/%{name}/trunk/%{version}/+download/%{name}-%{version}.tar.gz
Source0:    http://tarballs.openstack.org/%{name}/%{name}-%{version}.tar.gz


# https://review.openstack.org/5353
Patch1: avoid-No-handlers-could-be-found.patch

# CERN Patches
Patch1000:        1000-cern-python-keystoneclient.patch

Requires:   python-httplib2 >= 0.7
Requires:   python-prettytable
# For python < 2.7 rhbz#808413
Requires:    python-argparse
Requires:   python-setuptools
Requires:   python-simplejson

BuildRequires: python2-devel
BuildRequires: python-setuptools

%description
Client library and command line utility for interacting with Openstack
Keystone's API.

%package doc
Summary:    Documentation for OpenStack Keystone API Client
Group:      Documentation

BuildRequires: python-sphinx10

%description doc
Documentation for the client library for interacting with Openstack
Keystone's API.

%prep
%setup -q
%patch1 -p1
%patch1000 -p0

# Remove bundled egg-info
rm -rf python_keystoneclient.egg-info

%build
%{__python} setup.py build

%install
%{__python} setup.py install -O1 --skip-build --root %{buildroot}

# Delete tests
rm -fr %{buildroot}%{python_sitelib}/tests

export PYTHONPATH="$( pwd ):$PYTHONPATH"
pushd doc
if [ -x /usr/bin/sphinx-apidoc ]; then
    make html
else
    make html SPHINXAPIDOC=echo SPHINXBUILD=sphinx-1.0-build
fi
popd
# Fix hidden-file-or-dir warnings
rm -fr doc/build/html/.doctrees doc/build/html/.buildinfo

%files
%doc README.rst
%{_bindir}/keystone
%{python_sitelib}/keystoneclient
%{python_sitelib}/*.egg-info

%files doc
%doc LICENSE doc/build/html

%changelog
* Thu Feb 07 2013 Jose Castro Leon <jose.castro.leon@cern.ch> 0.1.3.27-1.ai6.2
- Minor fix in unscoped token service catalog

* Tue Feb 04 2013 Jose Castro Leon <jose.castro.leon@cern.ch> 0.1.3.27-1.ai6.1
- Minor fix in environment variable

* Tue Oct 16 2012 Alan Pevec <apevec@redhat.com> 0.1.3.27-1
- Allow empty description for tenants (lp#1025929)
- Documentation updates
- change default  wrap for tokens from 78 characters to 0 (lp#1061514)
- bootstrap a keystone user in one cmd
- Useful message when missing catalog (lp#949904)

* Thu Sep 27 2012 Alan Pevec <apevec@redhat.com> 1:0.1.3.9-1
- Handle "503 Service Unavailable" exception (lp#1028799)
- add --wrap option for long PKI tokens (lp#1053728)
- remove deprecated Diablo options
- add --os-token and --os-endpoint options to match
  http://wiki.openstack.org/UnifiedCLI/Authentication

* Sun Sep 23 2012 Alan Pevec <apevec@redhat.com> 1:0.1.3-1
- Change underscores in new cert options to dashes (lp#1040162)

* Wed Aug 22 2012 Alan Pevec <apevec@redhat.com> 1:0.1.2-1
- Add dependency on python-setuptools (#850842)
- New upstream release.

* Mon Jul 23 2012 Alan Pevec <apevec@redhat.com> 1:0.1.1-1
- New upstream release.

* Fri Apr 27 2012 Alan Pevec <apevec@redhat.com> 2012.1-2
- fix FTBFS due to wrong Sphinx version rhbz# 815055

* Thu Apr 05 2012 Alan Pevec <apevec@redhat.com> 2012.1-1
- Essex release

* Thu Apr 05 2012 Alan Pevec <apevec@redhat.com> 2012.1-0.8.rc2
- essex rc2

* Sat Mar 24 2012 Alan Pevec <apevec@redhat.com> 2012.1-0.7.rc1
- update to final essex rc1

* Wed Mar 21 2012 Alan Pevec <apevec@redhat.com> 2012.1-0.6.rc1
- essex rc1

* Thu Mar 01 2012 Alan Pevec <apevec@redhat.com> 2012.1-0.5.e4
- essex-4 milestone

* Tue Feb 28 2012 Alan Pevec <apevec@redhat.com> 2012.1-0.4.e4
- Endpoints: Add create, delete, list support
  https://review.openstack.org/4594

* Fri Feb 24 2012 Alan Pevec <apevec@redhat.com> 2012.1-0.3.e4
- Improve usability of CLI. https://review.openstack.org/4375

* Mon Feb 20 2012 Alan Pevec <apevec@redhat.com> 2012.1-0.2.e4
- pre essex-4 snapshot, for keystone rebase

* Thu Jan 26 2012 Cole Robinson <crobinso@redhat.com> - 2012.1-0.1.e3
- Initial package
