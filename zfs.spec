%define name             zfs
%define version          0.6.0
%define release          rc12
%define debug_package    %{nil}
%define _prefix          /
%define _libexecdir      /usr/libexec
%define _datadir         /usr/share
%define _mandir          %{_datadir}/man
%define _includedir      /usr/include
%define _udevdir         /lib/udev

Summary:         ZFS Library and Utils
Group:           Utilities/System
Name:            %{name}
Version:         %{version}
Release:         %{release}%{?dist}
License:         CDDL
URL:             git://github.com/zfsonlinux/zfs.git
BuildRoot:       %{_tmppath}/%{name}-%{version}-%{release}-%(%{__id} -un)
Source:          %{name}-%{version}.tar.gz
Requires:        zfs-modules spl zlib e2fsprogs
BuildRequires:   zlib-devel e2fsprogs-devel

%description
The %{name} package contains the libzfs library and support utilities
for the zfs file system.

%package devel
Summary:         ZFS File System User Headers
Group:           Development/Libraries
%if %{defined ch5} || %{defined el6} || %{defined fc12}
Requires:        zfs zlib libuuid libblkid
BuildRequires:   zlib-devel libuuid-devel libblkid-devel
%else
Requires:        zfs zlib e2fsprogs
BuildRequires:   zlib-devel e2fsprogs-devel
%endif

%description devel
The %{name}-devel package contains the header files needed for building
additional applications against the %{name} libraries.

%package test
Summary:         ZFS File System Test Infrastructure
Group:           Utilities/System
Requires:        zfs parted lsscsi mdadm bc

%description test
The %{name}-test package contains a test infrastructure for zpios which
can be used to simplfy the benchmarking of various hardware and software
configurations.  The test infrastructure additionally integrates with
various system profiling tools to facilitate an in depth analysis.

%package dracut
Summary:         ZFS Dracut Module
Group:           System Environment/Base
Requires:        zfs dracut

%description dracut
The %{name}-dracut package allows dracut to construct initramfs images
which are ZFS aware.

%prep
%setup
%build
%configure --with-config=user --without-blkid --with-udevdir=%{_udevdir}
make

%install
rm -rf $RPM_BUILD_ROOT
make DESTDIR=$RPM_BUILD_ROOT install

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-, root, root)
%{_sbindir}/*
%{_bindir}/*
%{_libdir}/*
%{_mandir}/man5/*
%{_mandir}/man8/*
%{_udevdir}/*

%config %{_sysconfdir}/init.d/*
%config %{_sysconfdir}/zfs/*
%config(noreplace) %{_sysconfdir}/zfs/zdev.conf

%doc AUTHORS ChangeLog COPYING COPYRIGHT DISCLAIMER
%doc OPENSOLARIS.LICENSE README.markdown ZFS.RELEASE

%files devel
%defattr(-,root,root)
%{_includedir}/*

%files test
%defattr(-,root,root)
%{_libexecdir}/zfs/*

%files dracut
%defattr(-,root,root)
%{_datadir}/dracut/*

%post
[ -x /sbin/chkconfig ] && /sbin/chkconfig --add zfs
exit 0

%preun
[ "$1" = 0 ] && [ -x /sbin/chkconfig ] && /sbin/chkconfig --del zfs
exit 0
