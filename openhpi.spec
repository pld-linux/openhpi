Summary:	Implementation of the Service Availability Forum's Hardware Platform Interface (HPI)
Name:		openhpi
Version:	0.3
Release:	1
License:	BSD
Group:		Libraries
Source0:	http://dl.sourceforge.net/%{name}/%{name}-%{version}.tar.gz
# Source0-md5:	a9d80104420fff8b51cedd6959cb336b
URL:		http://openhpi.sourceforge.net/
BuildRequires:	OpenIPMI-devel
BuildRequires:	glib-devel
BuildRequires:	libltdl-devel
BuildRequires:	libuuid-devel
BuildRequires:	libsysfs-devel
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
OpenHPI is an open source project created with the intent of providing
an implementation of the Service Availability Forum's Hardware Platform
Interface (HPI).  HPI provides a universal interface for creating resource
system models, typically for chassis and rack based servers, but extendable
for other problem domains such as clustering, virtualization and simulation.

%package devel
Summary:	Development part of OpenHPI Toolkit libraries
Group:		Development/Libraries
Requires:	%{name} = %{version}

%description devel
Development part of OpenHPI library.

%package static
Summary:	Static OpenHPI libraries
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}

%description static
Static OpenHPI Toolkit libraries.

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
%doc ChangeLog README TODO
%attr(755,root,root) %{_libdir}/lib*.so.*.*
%{_libdir}/%{name}
%attr(755,root,root) %{_libdir}/%{name}/lib*.so*
%attr(755,root,root) %{_bindir}/*

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/lib*.so
%{_libdir}/*.la
%{_includedir}/%{name}

%files static
%defattr(644,root,root,755)
%{_libdir}/lib*.a
