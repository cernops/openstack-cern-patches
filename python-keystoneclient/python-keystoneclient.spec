Name:       python-keystoneclient
# Since folsom-2 OpenStack clients follow their own release plan
# and restarted version numbering from 0.1.1
# https://lists.launchpad.net/openstack/msg14248.html
Epoch:      1
Version:    0.4.2
Release:    1%{?dist}.1
Summary:    Client library for OpenStack Identity API
License:    ASL 2.0
URL:        http://pypi.python.org/pypi/%{name}
Source0:    http://pypi.python.org/packages/source/p/%{name}/%{name}-%{version}.tar.gz

#
# patches_base=0.4.2
#
Patch0001: 0001-Remove-runtime-dependency-on-python-pbr.patch

# CERN Patches
Patch1001: 1001-cern-python-keystoneclient-discover-ssl.patch

BuildArch:  noarch

BuildRequires: python2-devel
BuildRequires: python-setuptools
BuildRequires: python-pbr
BuildRequires: python-d2to1

# from requirements.txt
Requires: python-argparse
Requires: python-iso8601 >= 0.1.4
Requires: python-prettytable
Requires: python-requests >= 0.8.8
Requires: python-oslo-config >= 1.1.0
Requires: python-six
Requires: python-netaddr
Requires: python-babel
# other requirements
Requires: python-setuptools
Requires: python-keyring


%description
Client library and command line utility for interacting with Openstack
Identity API.

%package doc
Summary:    Documentation for OpenStack Identity API Client
Group:      Documentation

BuildRequires: python-sphinx10

%description doc
Documentation for the client library for interacting with Openstack
Identity API.

%prep
%setup -q

%patch0001 -p1
%patch1001 -p1

# We provide version like this in order to remove runtime dep on pbr.
sed -i s/REDHATKEYSTONECLIENTVERSION/%{version}/ keystoneclient/__init__.py

# Let RPM handle the dependencies
rm -f test-requirements.txt requirements.txt

# Remove bundled egg-info
rm -rf python_keystoneclient.egg-info

%build
%{__python} setup.py build

%install
%{__python} setup.py install -O1 --skip-build --root %{buildroot}
# rhbz 888939#c7: bash-completion is not in RHEL
mkdir -p %{buildroot}%{_sysconfdir}/profile.d
install -pm 644 tools/keystone.bash_completion %{buildroot}%{_sysconfdir}/profile.d/keystone.sh

# Delete tests
rm -fr %{buildroot}%{python_sitelib}/tests

# Build HTML docs and man page
export PYTHONPATH="$( pwd ):$PYTHONPATH"
sphinx-1.0-build -b html doc/source html
sphinx-1.0-build -b man doc/source man
install -p -D -m 644 man/keystone.1 %{buildroot}%{_mandir}/man1/keystone.1

# Fix hidden-file-or-dir warnings
rm -fr html/.doctrees html/.buildinfo

%files
%doc LICENSE README.rst
%{_bindir}/keystone
%{_sysconfdir}/profile.d/keystone.sh
%{python_sitelib}/keystoneclient
%{python_sitelib}/*.egg-info
%{_mandir}/man1/keystone.1*

%files doc
%doc LICENSE html

%changelog
* Tue Jan 21 2014 Jose Castro Leon <jose.castro.leon@cern.ch> 0.4.2-1.slc6.1
- Fix keystone discover when retrieving servers with ssl enabled

* Mon Jan 13 2014 Jakub Ruzicka <jruzicka@redhat.com> 0.4.2-1
- Update to upstream 0.4.2
- Align doc build with other client packages

* Fri Jan 03 2014 Jakub Ruzicka <jruzicka@redhat.com> 0.4.1-4
- Don't require an email address when creating a user
- Put bash completion in /etc/profile.d (rhbz#1024581)

* Mon Oct 28 2013 Jakub Ruzicka <jruzicka@redhat.com> 0.4.1-3
- Remove unused requires: d2to1, simplejson

* Mon Oct 21 2013 Alan Pevec <apevec@redhat.com> 0.4.1-2
- webob is no longer used in authtoken

* Fri Oct 18 2013 Jakub Ruzicka <jruzicka@redhat.com> 0.4.1-1
- Update to upstream 0.4.1

* Wed Sep 18 2013 Jakub Ruzicka <jruzicka@redhat.com> 0.3.2-6
- Include upstream man page.

* Wed Sep 18 2013 Jakub Ruzicka <jruzicka@redhat.com> 0.3.2-5
- Really remove bogus python-httplib2 dependency.

* Mon Sep 16 2013 Jakub Ruzicka <jruzicka@redhat.com> 0.3.2-4
- Add python-netaddr dependency.
- Remove bogus python-httplib2 dependency.

* Tue Sep 10 2013 Jakub Ruzicka <jruzicka@redhat.com> 0.3.2-3
- Add python-httplib2 dependency.

* Mon Sep 09 2013 Jakub Ruzicka <jruzicka@redhat.com> 0.3.2-2
- Update to upstream 0.3.2.
- Remove pbr deps in the patch instead of this spec file.
- Ec2Signer patch is included in this version.

* Mon Aug 05 2013 Jakub Ruzicka <jruzicka@redhat.com> 0.3.1-4
- Ec2Signer: Allow signature verification for older boto versions. (#984752)

* Fri Aug 02 2013 Jakub Ruzicka <jruzicka@redhat.com> 0.3.1-3
- Remove requirements files.

* Mon Jul 08 2013 Jakub Ruzicka <jruzicka@redhat.com> 0.3.1-1
- Update to upstream version 0.3.1.

* Tue Jun 25 2013 Jakub Ruzicka <jruzicka@redhat.com> 0.2.5-2
- Remove runtime dependency on python-pbr.

* Tue Jun 25 2013 Jakub Ruzicka <jruzicka@redhat.com> 0.2.5-1
- Update to latest upstream. (0.2.5 + patches)
- Add new python requires from requirements.txt. (d2to1, pbr, six)

* Tue May 28 2013 Jakub Ruzicka <jruzicka@redhat.com> 0.2.3-4
- Check token expiry. (CVE-2013-2104)

* Thu May 02 2013 Jakub Ruzicka <jruzicka@redhat.com> 0.2.3-3
- Config value for revocation list timeout. (#923519)

* Thu Apr 04 2013 Jakub Ruzicka <jruzicka@redhat.com> 0.2.3-2
- Update requires. (#948244)

* Tue Mar 19 2013 Alan Pevec <apevec@redhat.com> 0.2.3-1
- New upstream release.

* Wed Jan 30 2013 Alan Pevec <apevec@redhat.com> 0.2.2-1
- New upstream release.

* Thu Jan 17 2013 Alan Pevec <apevec@redhat.com> 0.2.1-2
- Add dependency on python-requests.
- Add python-keyring RPM dependency.

* Fri Dec 21 2012 Alan Pevec <apevec@redhat.com> 0.2.1-1
- New upstream release.
- Add bash completion support

* Fri Nov 23 2012 Alan Pevec <apevec@redhat.com> 0.2.0-1
- New upstream release.
- Identity API v3 support
- add service_id column to endpoint-list
- avoid ValueError exception for 400 or 404 lp#1067512
- use system default CA certificates lp#106483
- keep original IP lp#1046837
- avoid exception for an expected empty catalog lp#1070493
- fix keystoneclient against Rackspace Cloud Files lp#1074784
- blueprint solidify-python-api
- blueprint authtoken-to-keystoneclient-repo
- fix auth_ref initialization lp#1078589
- warn about bypassing auth on CLI lp#1076225
- check creds before token/endpoint lp#1076233
- check for auth URL before password lp#1076235
- fix scoped auth for non-admins lp#1081192

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

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2012.2-0.2.f1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

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
