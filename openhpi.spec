Summary:	Service Availability Forum's Hardware Platform Interface (HPI) implementation
Summary(pl):	Implementacja HPI (Hardware Platform Interface) Service Availability Forum
Name:		openhpi
Version:	0.4
Release:	1
License:	BSD
Group:		Libraries
Source0:	http://dl.sourceforge.net/openhpi/%{name}-%{version}.tar.gz
# Source0-md5:	0ef94d2de5ae619d20cd8b72ccfa7003
Patch0:		%{name}-snmp.patch
URL:		http://openhpi.sourceforge.net/
#BuildRequires:	OpenIPMI-devel >= 1.1.8
BuildRequires:	autoconf >= 2.50
BuildRequires:	automake >= 1.5
BuildRequires:	docbook-dtd41-sgml
BuildRequires:	docbook-utils
BuildRequires:	glib2-devel >= 2.0.0
BuildRequires:	libltdl-devel
BuildRequires:	libstdc++-devel
BuildRequires:	libtool
BuildRequires:	libuuid-devel
BuildRequires:	net-snmp-devel
BuildRequires:	pkgconfig
BuildRequires:	sysfsutils-devel >= 0.3.0
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
OpenHPI is an open source project created with the intent of providing
an implementation of the Service Availability Forum's Hardware
Platform Interface (HPI). HPI provides a universal interface for
creating resource system models, typically for chassis and rack based
servers, but extendable for other problem domains such as clustering,
virtualization and simulation.

%description -l pl
OpenHPI to otwarty projekt strorzony z zamiarem dostarczenia
implementacji HPI (Hardware Platform Interface - interfejsu platformy
sprzêtowej) Service Availability Forum. HPI udostêpnia uniwersjalny
interfejs do tworzenia modeli systemów zasobów, zwykle dla serwerów w
ramach i szafach, ale rozszerzalny dla innego rodzaju problemów,
takich jak klastrowanie, wirtualizacja czy symulacja.

%package devel
Summary:	Development part of OpenHPI Toolkit library
Summary(pl):	Programistyczna czê¶æ biblioteki OpenHPI
Group:		Development/Libraries
Requires:	%{name} = %{version}
Requires:	glib2-devel >= 2.0.0
Requires:	libltdl-devel

%description devel
Development part of OpenHPI library.

%description devel -l pl
Programistyczna czê¶æ biblioteki OpenHPI.

%package static
Summary:	Static OpenHPI library
Summary(pl):	Statyczna biblioteka OpenHPI
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}

%description static
Static OpenHPI Toolkit libraries.

%description static -l pl
Statyczna biblioteka OpenHPI.

%package plugin-ipmi
Summary:	ipmi plugin for OpenHPI
Summary(pl):	Wtyczka ipmi dla OpenHPI
Group:		Libraries
Requires:	%{name} = %{version}

%description plugin-ipmi
ipmi plugin for OpenHPI.

%description plugin-ipmi -l pl
Wtyczka ipmi dla OpenHPI.

%package plugin-ipmidirect
Summary:	ipmidirect plugin for OpenHPI
Summary(pl):	Wtyczka ipmidirect dla OpenHPI
Group:		Libraries
Requires:	%{name} = %{version}

%description plugin-ipmidirect
ipmidirect plugin for OpenHPI.

%description plugin-ipmidirect -l pl
Wtyczka ipmidirect dla OpenHPI.

%package plugin-snmp
Summary:	SNMP plugins for OpenHPI
Summary(pl):	Wtyczki SNMP dla OpenHPI
Group:		Libraries
Requires:	%{name} = %{version}

%description plugin-snmp
SNMP plugins for OpenHPI: snmp_bc and snmp_client.

%description plugin-snmp -l pl
Wtyczki SNMP dla OpenHPI: snmp_bc oraz snmp_client.

%package plugin-sysfs
Summary:	sysfs plugin for OpenHPI
Summary(pl):	Wtyczka sysfs dla OpenHPI
Group:		Libraries
Requires:	%{name} = %{version}

%description plugin-sysfs
sysfs plugin for OpenHPI.

%description plugin-sysfs -l pl
Wtyczka sysfs dla OpenHPI.

%prep
%setup -q
%patch0 -p1

# speed up build, lower disk space usage
for f in `find . -name Makefile.am | xargs grep -l 'AM_CFLAGS.* -g '`; do
	%{__perl} -pi -e 's/^(AM_CFLAGS.* )-g /$1 /' $f
done

%build
%{__libtoolize}
%{__aclocal}
%{__autoconf}
%{__automake}
# ipmi requires unreleased OpenIPMI > 1.1.7 - disable for now
%configure \
	--disable-ipmi \
	--with-glib=2.0.0
	
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
%doc COPYING ChangeLog README docs/hld/openhpi-manual
%attr(755,root,root) %{_bindir}/*
%attr(755,root,root) %{_libdir}/lib*.so.*.*
%dir %{_libdir}/%{name}
%attr(755,root,root) %{_libdir}/%{name}/libdummy.so*
%{_libdir}/%{name}/libdummy.la
%attr(755,root,root) %{_libdir}/%{name}/libwatchdog.so*
%{_libdir}/%{name}/libwatchdog.la
%dir %{_sysconfdir}/openhpi
%config(noreplace) %verify(not size mtime md5) %{_sysconfdir}/openhpi/openhpi.conf

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/lib*.so
%{_libdir}/*.la
%{_includedir}/%{name}
%{_pkgconfigdir}/*.pc

%files static
%defattr(644,root,root,755)
%{_libdir}/lib*.a

%if 0
%files plugin-ipmi
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/%{name}/libipmi.so*
%{_libdir}/%{name}/libipmi.la
%endif

%files plugin-ipmidirect
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/%{name}/libipmidirect.so*
%{_libdir}/%{name}/libipmidirect.la

%files plugin-snmp
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/%{name}/libsnmp_bc.so*
%{_libdir}/%{name}/libsnmp_bc.la
%attr(755,root,root) %{_libdir}/%{name}/libsnmp_client.so*
%{_libdir}/%{name}/libsnmp_client.la

%files plugin-sysfs
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/%{name}/libsysfs2hpi.so*
%{_libdir}/%{name}/libsysfs2hpi.la
