%if 0%{?fedora} > 12 || 0%{?rhel} > 6
# This code doesn't automatically convert cleanly, leaving it so we can try
# again later.
# http://jira.mongodb.org/browse/PYTHON-84
%global with_python3 0
%endif

# Fix private-shared-object-provides error
%{?filter_setup:
%filter_provides_in %{python_sitearch}.*\.so$
%filter_setup
}

Name:           pymongo
Version:        2.5.2
Release:        1%{?dist}
Summary:        Python driver for MongoDB

Group:          Development/Languages
# All code is ASL 2.0 except bson/time64*.{c,h} which is MIT
License:        ASL 2.0 and MIT
URL:            http://api.mongodb.org/python
Source0:        http://pypi.python.org/packages/source/p/pymongo/%{name}-%{version}.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
Requires:       python-bson = %{version}-%{release}

Provides:       pymongo = %{version}-%{release}
Obsoletes:      pymongo <= 2.1.1-4

BuildRequires:  python2-devel
BuildRequires:  python-nose
BuildRequires:  python-setuptools

%if 0%{?with_python3}
BuildRequires:  python-tools
BuildRequires:  python3-devel
BuildRequires:  python3-setuptools
%endif # if with_python3

# Mongodb must run on a little-endian CPU (see bug #630898)
ExcludeArch:    ppc ppc64 %{sparc} s390 s390x

%description
The Python driver for MongoDB.

%if 0%{?with_python3}
%package -n python3-pymongo
Summary:        Python driver for MongoDB
Group:          Development/Languages
Requires:       python3-bson = %{version}-%{release}

%description -n python3-pymongo
The Python driver for MongoDB.  This package contains the python3 version of
this module.
%endif # with_python3

%package gridfs
Summary:        Python GridFS driver for MongoDB
Group:          Development/Libraries
Requires:       %{name}%{?_isa} = %{version}-%{release}
Provides:       pymongo-gridfs = %{version}-%{release}
Obsoletes:      pymongo-gridfs <= 2.1.1-4

%description gridfs
GridFS is a storage specification for large objects in MongoDB.

%if 0%{?with_python3}
%package -n python3-pymongo-gridfs
Summary:        Python GridFS driver for MongoDB
Group:          Development/Libraries
Requires:       python3-pymongo%{?_isa} = %{version}-%{release}

%description -n python3-pymongo-gridfs
GridFS is a storage specification for large objects in MongoDB.  This package
contains the python3 version of this module.
%endif # with_python3

%package -n python-bson
Summary:        Python bson library
Group:          Development/Libraries

%description -n python-bson
BSON is a binary-encoded serialization of JSON-like documents. BSON is designed
to be lightweight, traversable, and efficient. BSON, like JSON, supports the
embedding of objects and arrays within other objects and arrays.

%if 0%{?with_python3}
%package -n python3-bson
Summary:        Python bson library
Group:          Development/Libraries

%description -n python3-bson
BSON is a binary-encoded serialization of JSON-like documents. BSON is designed
to be lightweight, traversable, and efficient. BSON, like JSON, supports the
embedding of objects and arrays within other objects and arrays.  This package
contains the python3 version of this module.
%endif # with_python3

%prep
%setup -q -n pymongo-%{version}
rm -r pymongo.egg-info

%if 0%{?with_python3}
rm -rf %{py3dir}
cp -a . %{py3dir}
2to3 --write --nobackups --no-diffs %{py3dir}
%endif # with_python3

%build
CFLAGS="%{optflags}" %{__python} setup.py build

%if 0%{?with_python3}
pushd %{py3dir}
CFLAGS="%{optflags}" %{__python3} setup.py build
popd
%endif # with_python3

%install
rm -rf %{buildroot}
%{__python} setup.py install --skip-build --root $RPM_BUILD_ROOT

%if 0%{?with_python3}
pushd %{py3dir}
%{__python3} setup.py install --skip-build --root $RPM_BUILD_ROOT
popd
%endif # with_python3

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
%doc LICENSE PKG-INFO README.rst doc
%{python_sitearch}/pymongo
%{python_sitearch}/pymongo-%{version}-*.egg-info

%if 0%{?with_python3}
%files -n python3-pymongo
%defattr(-,root,root,-)
%doc LICENSE PKG-INFO README.rst doc
%{python3_sitearch}/pymongo
%{python3_sitearch}/pymongo-%{version}-*.egg-info
%endif # with_python3

%files gridfs
%defattr(-,root,root,-)
%doc LICENSE PKG-INFO README.rst doc
%{python_sitearch}/gridfs

%if 0%{?with_python3}
%files -n python3-pymongo-gridfs
%defattr(-,root,root,-)
%doc LICENSE PKG-INFO README.rst doc
%{python3_sitearch}/gridfs
%endif # with_python3

%files -n python-bson
%defattr(-,root,root,-)
%doc LICENSE PKG-INFO README.rst doc
%{python_sitearch}/bson

%if 0%{?with_python3}
%files -n python3-bson
%defattr(-,root,root,-)
%doc LICENSE PKG-INFO README.rst doc
%{python3_sitearch}/bson
%endif # with_python3

%check
# Exclude tests that require an active MongoDB connection
 exclude='(^test_auth_from_uri$'
exclude+='|^test_auto_auth_login$'
exclude+='|^test_auto_reconnect_exception_when_read_preference_is_secondary$'
exclude+='|^test_auto_start_request$'
exclude+='|^test_binary$'
exclude+='|^test_client$'
exclude+='|^test_collection$'
exclude+='|^test_common$'
exclude+='|^test_config_ssl$'
exclude+='|^test_connect$'
exclude+='|^test_connection$'
exclude+='|^test_constants$'
exclude+='|^test_contextlib$'
exclude+='|^test_copy_db$'
exclude+='|^test_cursor$'
exclude+='|^test_database$'
exclude+='|^test_database_names$'
exclude+='|^test_delegated_auth$'
exclude+='|^test_disconnect$'
exclude+='|^test_document_class$'
exclude+='|^test_drop_database$'
exclude+='|^test_equality$'
exclude+='|^test_fork$'
exclude+='|^test_from_uri$'
exclude+='|^test_fsync_lock_unlock$'
exclude+='|^test_get_db$'
exclude+='|^test_getters$'
exclude+='|^test_grid_file$'
exclude+='|^test_gridfs$'
exclude+='|^test_host_w_port$'
exclude+='|^test_interrupt_signal$'
exclude+='|^test_ipv6$'
exclude+='|^test_iteration$'
exclude+='|^test_json_util$'
exclude+='|^test_kill_cursor_explicit_primary$'
exclude+='|^test_kill_cursor_explicit_secondary$'
exclude+='|^test_master_slave_connection$'
exclude+='|^test_nested_request$'
exclude+='|^test_network_timeout$'
exclude+='|^test_network_timeout_validation$'
exclude+='|^test_operation_failure_with_request$'
exclude+='|^test_operation_failure_without_request$'
exclude+='|^test_operations$'
exclude+='|^test_pinned_member$'
exclude+='|^test_pooling$'
exclude+='|^test_pooling_gevent$'
exclude+='|^test_properties$'
exclude+='|^test_pymongo$'
exclude+='|^test_read_preferences$'
exclude+='|^test_replica_set_client$'
exclude+='|^test_replica_set_connection$'
exclude+='|^test_replica_set_connection_alias$'
exclude+='|^test_repr$'
exclude+='|^test_request_threads$'
exclude+='|^test_safe_insert$'
exclude+='|^test_safe_update$'
exclude+='|^test_schedule_refresh$'
exclude+='|^test_server_disconnect$'
exclude+='|^test_son_manipulator$'
exclude+='|^test_threading$'
exclude+='|^test_threads$'
exclude+='|^test_threads_replica_set_connection$'
exclude+='|^test_timeouts$'
exclude+='|^test_tz_aware$'
exclude+='|^test_uri_options$'
exclude+='|^test_use_greenlets$'
exclude+='|^test_with_start_request$'
exclude+=')'
pushd test
nosetests --exclude="$exclude"
popd

%changelog
* Tue Aug 12 2013 Stefano Zilli <stefano.zilli@cern.ch> -2.5.2-1
- Update to 2.5.2

* Tue Apr 10 2012 Silas Sewell <silas@sewell.org> - 2.1.1-1
- Update to 2.1.1

* Mon Nov 08 2010 Silas Sewell <silas@sewell.ch> - 1.9-6
- Make path conditional (more big endian issues)

* Mon Nov 08 2010 Silas Sewell <silas@sewell.ch> - 1.9-5
- Disable .so fixes for ppc64 (no big endian support)

* Tue Oct 26 2010 Silas Sewell <silas@sewell.ch> - 1.9-4
- Add comment about multi-license

* Thu Oct 21 2010 Silas Sewell <silas@sewell.ch> - 1.9-3
- Fixed tests so they actually run
- Change python-devel to python2-devel

* Wed Oct 20 2010 Silas Sewell <silas@sewell.ch> - 1.9-2
- Add check section
- Use correct .so filter
- Added python3 stuff (although disabled)

* Tue Sep 28 2010 Silas Sewell <silas@sewell.ch> - 1.9-1
- Update to 1.9

* Tue Sep 28 2010 Silas Sewell <silas@sewell.ch> - 1.8.1-1
- Update to 1.8.1

* Sat Dec 05 2009 Silas Sewell <silas@sewell.ch> - 1.1.2-1
- Initial build