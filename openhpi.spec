# TODO:
# - rtas (BR: librtas) on ppc/ppc64
# - C++ wrappers (needs patching, at least "extra qualification" errors)
Summary:	Service Availability Forum's Hardware Platform Interface (HPI) implementation
Summary(pl):	Implementacja HPI (Hardware Platform Interface) Service Availability Forum
Name:		openhpi
Version:	2.7.2
Release:	1
License:	BSD
Group:		Libraries
Source0:	http://dl.sourceforge.net/openhpi/%{name}-%{version}.tar.gz
# Source0-md5:	0d980f24efde840412a68c987bd7d909
Patch0:		%{name}-types.patch
Patch1:		%{name}-sh.patch
Patch2:		%{name}-align.patch
Patch3:		%{name}-proto.patch
Patch4:		%{name}-sysfs2.patch
URL:		http://openhpi.sourceforge.net/
BuildRequires:	OpenIPMI-devel >= 1.4.20
BuildRequires:	autoconf >= 2.57
BuildRequires:	automake >= 1:1.8
BuildRequires:	docbook-dtd41-sgml
BuildRequires:	docbook-utils
BuildRequires:	fam-devel
BuildRequires:	gcc >= 5:3.2.0
BuildRequires:	glib2-devel >= 1:2.2.0
BuildRequires:	libltdl-devel
BuildRequires:	libstdc++-devel
BuildRequires:	libtool
BuildRequires:	libuuid-devel
BuildRequires:	net-snmp-devel
BuildRequires:	openssl-devel
BuildRequires:	pkgconfig
BuildRequires:	sysfsutils-devel >= 1.3.0-3
Requires:	glib2 >= 1:2.2.0
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		specflags	-fno-strict-aliasing

%description
OpenHPI is an open source project created with the intent of providing
an implementation of the Service Availability Forum's Hardware
Platform Interface (HPI). HPI provides a universal interface for
creating resource system models, typically for chassis and rack based
servers, but extendable for other problem domains such as clustering,
virtualization and simulation.

%description -l pl
OpenHPI to otwarty projekt stworzony z zamiarem dostarczenia
implementacji HPI (Hardware Platform Interface - interfejsu platformy
sprzêtowej) Service Availability Forum. HPI udostêpnia uniwersalny
interfejs do tworzenia modeli systemów zasobów, zwykle dla serwerów
w ramach i szafach, ale rozszerzalny dla innego rodzaju problemów,
takich jak klastrowanie, wirtualizacja czy symulacja.

%package devel
Summary:	Development part of OpenHPI Toolkit library
Summary(pl):	Programistyczna czê¶æ biblioteki OpenHPI
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	glib2-devel >= 1:2.2.0
Requires:	libltdl-devel

%description devel
Development part of OpenHPI library.

%description devel -l pl
Programistyczna czê¶æ biblioteki OpenHPI.

%package static
Summary:	Static OpenHPI library
Summary(pl):	Statyczna biblioteka OpenHPI
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static OpenHPI Toolkit libraries.

%description static -l pl
Statyczna biblioteka OpenHPI.

%package plugin-ipmi
Summary:	ipmi plugin for OpenHPI
Summary(pl):	Wtyczka ipmi dla OpenHPI
Group:		Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	OpenIPMI >= 1.4.20

%description plugin-ipmi
ipmi plugin for OpenHPI.

%description plugin-ipmi -l pl
Wtyczka ipmi dla OpenHPI.

%package plugin-ipmidirect
Summary:	ipmidirect plugin for OpenHPI
Summary(pl):	Wtyczka ipmidirect dla OpenHPI
Group:		Libraries
Requires:	%{name} = %{version}-%{release}

%description plugin-ipmidirect
ipmidirect plugin for OpenHPI.

%description plugin-ipmidirect -l pl
Wtyczka ipmidirect dla OpenHPI.

%package plugin-snmp
Summary:	SNMP plugins for OpenHPI
Summary(pl):	Wtyczki SNMP dla OpenHPI
Group:		Libraries
Requires:	%{name} = %{version}-%{release}

%description plugin-snmp
SNMP plugins for OpenHPI: snmp_bc.

%description plugin-snmp -l pl
Wtyczki SNMP dla OpenHPI: snmp_bc.

%package plugin-simulator
Summary:	simulator plugin for OpenHPI
Summary(pl):	Wtyczka simulator dla OpenHPI
Group:		Libraries
Requires:	%{name} = %{version}-%{release}

%description plugin-simulator
simulator plugin for OpenHPI.

%description plugin-simulator -l pl
Wtyczka simulator dla OpenHPI.

%package plugin-sysfs
Summary:	sysfs plugin for OpenHPI
Summary(pl):	Wtyczka sysfs dla OpenHPI
Group:		Libraries
Requires:	%{name} = %{version}-%{release}

%description plugin-sysfs
sysfs plugin for OpenHPI.

%description plugin-sysfs -l pl
Wtyczka sysfs dla OpenHPI.

%prep
%setup -q
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1

# speed up build, lower disk space usage
for f in `find . -name Makefile.am | xargs grep -l 'AM_CFLAGS.* -g '`; do
	%{__perl} -pi -e 's/^(AM_CFLAGS.* )-g /$1 /' $f
done

%build
%{__libtoolize}
%{__aclocal}
%{__autoconf}
%{__autoheader}
%{__automake}
%configure \
	--enable-daemon \
	--enable-dummy \
	--enable-simulator

%{__make}

%{__make} -C docs/hld openhpi-manual/book1.html

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

# remove useless static plugins (but *.la are used by lt_dlopen)
rm -f $RPM_BUILD_ROOT%{_libdir}/%{name}/*.a

%clean
rm -rf $RPM_BUILD_ROOT

%post   -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc COPYING README docs/hld/openhpi-manual
%attr(755,root,root) %{_bindir}/*
%attr(755,root,root) %{_sbindir}/openhpid
%attr(755,root,root) %{_libdir}/lib*.so.*.*.*
%dir %{_libdir}/%{name}
%attr(755,root,root) %{_libdir}/%{name}/libwatchdog.so*
%{_libdir}/%{name}/libwatchdog.la
%dir %{_sysconfdir}/openhpi
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/openhpi/openhpi.conf
#%attr(754,root,root) /etc/rc.d/init.d/openhpid
%dir %{_localstatedir}/lib/%{name}
%{_mandir}/man7/openhpi.7*

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/lib*.so
%{_libdir}/lib*.la
%{_includedir}/%{name}
%{_pkgconfigdir}/*.pc

%files static
%defattr(644,root,root,755)
%{_libdir}/lib*.a

%files plugin-ipmi
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/%{name}/libipmi.so*
%{_libdir}/%{name}/libipmi.la

%files plugin-ipmidirect
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/%{name}/libipmidirect.so*
%{_libdir}/%{name}/libipmidirect.la

%files plugin-simulator
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/%{name}/libsimulator.so*
%{_libdir}/%{name}/libsimulator.la

%files plugin-snmp
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/%{name}/libsnmp_bc.so*
%{_libdir}/%{name}/libsnmp_bc.la

%files plugin-sysfs
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/%{name}/libsysfs2hpi.so*
%{_libdir}/%{name}/libsysfs2hpi.la
