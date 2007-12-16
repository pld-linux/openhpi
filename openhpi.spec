Summary:	Service Availability Forum's Hardware Platform Interface (HPI) implementation
Summary(pl.UTF-8):	Implementacja HPI (Hardware Platform Interface) Service Availability Forum
Name:		openhpi
Version:	2.10.1
Release:	3
License:	BSD
Group:		Libraries
Source0:	http://dl.sourceforge.net/openhpi/%{name}-%{version}.tar.gz
# Source0-md5:	b8b771b310046bb14db8113fd1720431
Patch0:		%{name}-types.patch
Patch1:		%{name}-sh.patch
Patch2:		%{name}-align.patch
Patch3:		%{name}-proto.patch
Patch4:		%{name}-configure.patch
Patch5:		%{name}-rtas.patch
Patch6:		%{name}-c++.patch
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
%ifarch ppc ppc64
BuildRequires:	librtas-devel
%endif
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

%description -l pl.UTF-8
OpenHPI to otwarty projekt stworzony z zamiarem dostarczenia
implementacji HPI (Hardware Platform Interface - interfejsu platformy
sprzętowej) Service Availability Forum. HPI udostępnia uniwersalny
interfejs do tworzenia modeli systemów zasobów, zwykle dla serwerów
w ramach i szafach, ale rozszerzalny dla innego rodzaju problemów,
takich jak klastrowanie, wirtualizacja czy symulacja.

%package devel
Summary:	Development part of OpenHPI Toolkit library
Summary(pl.UTF-8):	Programistyczna część biblioteki OpenHPI
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	glib2-devel >= 1:2.2.0
Requires:	libltdl-devel
# for libosahpi
Requires:	libstdc++-devel
Requires:	libuuid-devel

%description devel
Development part of OpenHPI library.

%description devel -l pl.UTF-8
Programistyczna część biblioteki OpenHPI.

%package static
Summary:	Static OpenHPI library
Summary(pl.UTF-8):	Statyczna biblioteka OpenHPI
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static OpenHPI Toolkit libraries.

%description static -l pl.UTF-8
Statyczna biblioteka OpenHPI.

%package plugin-ipmi
Summary:	ipmi plugin for OpenHPI
Summary(pl.UTF-8):	Wtyczka ipmi dla OpenHPI
Group:		Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	OpenIPMI >= 1.4.20

%description plugin-ipmi
ipmi plugin for OpenHPI.

%description plugin-ipmi -l pl.UTF-8
Wtyczka ipmi dla OpenHPI.

%package plugin-ipmidirect
Summary:	ipmidirect plugin for OpenHPI
Summary(pl.UTF-8):	Wtyczka ipmidirect dla OpenHPI
Group:		Libraries
Requires:	%{name} = %{version}-%{release}

%description plugin-ipmidirect
ipmidirect plugin for OpenHPI.

%description plugin-ipmidirect -l pl.UTF-8
Wtyczka ipmidirect dla OpenHPI.

%package plugin-rtas
Summary:	RTAS plugin for OpenHPI
Summary(pl.UTF-8):	Wtyczka RTAS dla OpenHPI
Group:		Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	lsvpd

%description plugin-rtas
RTAS plugin for OpenHPI.

%description plugin-rtas -l pl.UTF-8
Wtyczka RTAS dla OpenHPI.

%package plugin-simulator
Summary:	simulator plugin for OpenHPI
Summary(pl.UTF-8):	Wtyczka simulator dla OpenHPI
Group:		Libraries
Requires:	%{name} = %{version}-%{release}

%description plugin-simulator
simulator plugin for OpenHPI.

%description plugin-simulator -l pl.UTF-8
Wtyczka simulator dla OpenHPI.

%package plugin-snmp
Summary:	SNMP plugins for OpenHPI
Summary(pl.UTF-8):	Wtyczki SNMP dla OpenHPI
Group:		Libraries
Requires:	%{name} = %{version}-%{release}

%description plugin-snmp
SNMP plugins for OpenHPI: snmp_bc.

%description plugin-snmp -l pl.UTF-8
Wtyczki SNMP dla OpenHPI: snmp_bc.

%package plugin-sysfs
Summary:	sysfs plugin for OpenHPI
Summary(pl.UTF-8):	Wtyczka sysfs dla OpenHPI
Group:		Libraries
Requires:	%{name} = %{version}-%{release}

%description plugin-sysfs
sysfs plugin for OpenHPI.

%description plugin-sysfs -l pl.UTF-8
Wtyczka sysfs dla OpenHPI.

%prep
%setup -q
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1
%patch5 -p1
%patch6 -p1

# speed up build, lower disk space usage
for f in $(find -name Makefile.am | xargs grep -l 'AM_CFLAGS.* -g '); do
	%{__sed} -i -e 's/^\(AM_CFLAGS.* \)-g /\1 /' $f
done

%ifarch alpha sparc
# event.c: In function `process_hpi_event':
# event.c:236: warning: cast increases required alignment of target type
# event.c: In function `oh_process_events':
# event.c:410: warning: cast increases required alignment of target type
# make[1]: *** [event.lo] Error 1
# for this code:
# sid = g_array_index(sessions, SaHpiSessionIdT, i);
# where:
# typedef SaHpiUint32T SaHpiSessionIdT;
# and:
# #define g_array_index(a,t,i)      (((t*) (a)->data) [(i)])
%{__sed} -i -e 's/-Werror//' configure.ac
%endif

%build
%{__libtoolize}
%{__aclocal}
%{__autoconf}
%{__autoheader}
%{__automake}
%configure \
	--enable-cpp_wrappers \
	--enable-daemon \
	--enable-dummy \
%ifarch ppc ppc64
	--enable-rtas \
%endif
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
%attr(755,root,root) %{_bindir}/hpi*
%attr(755,root,root) %{_sbindir}/openhpid
%attr(755,root,root) %{_libdir}/libohtcpconnx.so.*.*.*
%attr(755,root,root) %{_libdir}/libohudpconnx.so.*.*.*
%attr(755,root,root) %{_libdir}/libopenhpi*.so.*.*.*
%attr(755,root,root) %{_libdir}/libosahpi.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libohtcpconnx.so.2
%attr(755,root,root) %ghost %{_libdir}/libohudpconnx.so.2
%attr(755,root,root) %ghost %{_libdir}/libopenhpi*.so.2
%attr(755,root,root) %ghost %{_libdir}/libosahpi.so.2
%dir %{_libdir}/%{name}
%attr(755,root,root) %{_libdir}/%{name}/libwatchdog.so*
%{_libdir}/%{name}/libwatchdog.la
%dir %{_sysconfdir}/openhpi
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/openhpi/openhpi.conf
#%attr(754,root,root) /etc/rc.d/init.d/openhpid
%dir %{_localstatedir}/lib/%{name}
%{_mandir}/man7/openhpi.7*
%{_mandir}/man8/openhpid.8*

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libohtcpconnx.so
%attr(755,root,root) %{_libdir}/libohudpconnx.so
%attr(755,root,root) %{_libdir}/libopenhpi*.so
%attr(755,root,root) %{_libdir}/libosahpi.so
%{_libdir}/libohtcpconnx.la
%{_libdir}/libohudpconnx.la
%{_libdir}/libopenhpi*.la
%{_libdir}/libosahpi.la
%dir %{_includedir}/openhpi
%{_includedir}/openhpi/*.h
%{_includedir}/openhpi/oSaHpi*.hpp
%{_pkgconfigdir}/openhpi.pc
%{_pkgconfigdir}/openhpiutils.pc

%files static
%defattr(644,root,root,755)
%{_libdir}/libohtcpconnx.a
%{_libdir}/libohudpconnx.a
%{_libdir}/libopenhpi*.a
%{_libdir}/libosahpi.a

%files plugin-ipmi
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/%{name}/libipmi.so*
%{_libdir}/%{name}/libipmi.la

%files plugin-ipmidirect
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/%{name}/libipmidirect.so*
%{_libdir}/%{name}/libipmidirect.la

%ifarch ppc ppc64
%files plugin-rtas
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/%{name}/librtas2hpi.so*
%{_libdir}/%{name}/librtas2hpi.la
%endif

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
