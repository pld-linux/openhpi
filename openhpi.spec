Summary:	Service Availability Forum's Hardware Platform Interface (HPI) implementation
Summary(pl):	Implementacja HPI (Hardware Platform Interface) Service Availability Forum
Name:		openhpi
Version:	0.3
Release:	1
License:	BSD
Group:		Libraries
Source0:	http://dl.sourceforge.net/%{name}/%{name}-%{version}.tar.gz
# Source0-md5:	a9d80104420fff8b51cedd6959cb336b
URL:		http://openhpi.sourceforge.net/
BuildRequires:	OpenIPMI-devel
BuildRequires:	autoconf >= 2.50
BuildRequires:	automake
BuildRequires:	glib-devel
BuildRequires:	libltdl-devel
BuildRequires:	libtool
BuildRequires:	libuuid-devel
#BuildRequires:	net-snmp-devel
BuildRequires:	pkgconfig
BuildRequires:	sysfsutils-devel >= 0.2.0
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

%prep
%setup -q

%build
%{__libtoolize}
%{__aclocal}
%{__autoconf}
%{__automake}
%configure \
	--disable-snmp_bc
	
%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%post   -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc COPYING ChangeLog README TODO
%attr(755,root,root) %{_bindir}/*
%attr(755,root,root) %{_libdir}/lib*.so.*.*
%dir %{_libdir}/%{name}
%attr(755,root,root) %{_libdir}/%{name}/lib*.so*

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/lib*.so
%{_libdir}/*.la
%{_includedir}/%{name}

%files static
%defattr(644,root,root,755)
%{_libdir}/lib*.a
