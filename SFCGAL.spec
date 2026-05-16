#
# Conditional build:
%bcond_without	apidocs		# API documentation
%bcond_without	osg		# OpenSceneGraph support
#
Summary:	C++ wrapper around CGAL library
Summary(pl.UTF-8):	Obudowanie C++ do biblioteki CGAL
Name:		SFCGAL
Version:	2.2.0
Release:	1
License:	LGPL v2.0+
Group:		Libraries
#Source0Download: https://gitlab.com/sfcgal/SFCGAL/-/releases
Source0:	https://gitlab.com/sfcgal/SFCGAL/-/archive/v%{version}/%{name}-v%{version}.tar.bz2
# Source0-md5:	ef0a4397a6f5bf06299c6c8c5ab77f62
URL:		https://sfcgal.gitlab.io/SFCGAL
# osgDB osgUtil
%{?with_osg:BuildRequires:	OpenSceneGraph-devel}
# thread system serialization %{?with_osg: chrono unit_test_framework filesystem program_options timer}
BuildRequires:	boost-devel
BuildRequires:	cmake >= 3.6
%{?with_apidocs:BuildRequires:	doxygen}
BuildRequires:	libstdc++-devel >= 6:7
BuildRequires:	rpm-build >= 4.6
BuildRequires:	rpmbuild(macros) >= 1.605
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
SFCGAL is a C++ wrapper library around CGAL with the aim of supporting
ISO 19107:2019 and OGC Simple Features Access for 3D operations.

%description -l pl.UTF-8
SFCGAL to biblioteka obudowująca C++ dla CGAL, mająca na celu obsługę
ISO 19107:2019 oraz OGC Simple Features Access dla operacji 3D.

%package devel
Summary:	Header files for SFCGAL library
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki SFCGAL
Group:		Development/Libraries
Requires:	%{name}%{?_isa} = %{version}-%{release}
Requires:	boost-devel
Requires:	libstdc++-devel >= 6:7

%description devel
Header files for SFCGAL library.

%description devel -l pl.UTF-8
Pliki nagłówkowe biblioteki SFCGAL.

%package osg
Summary:	SFCGAL OpenGraphics support library
Summary(pl.UTF-8):	Biblioteka SGCGAL do obsługi OpenGraphics
Group:		Libraries
Requires:	%{name}%{?_isa} = %{version}-%{release}

%description osg
SFCGAL OpenGraphics support library.

%description osg -l pl.UTF-8
Biblioteka SGCGAL do obsługi OpenGraphics.

%package osg-devel
Summary:	Header files for SFCGAL OpenGraphics support library
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki SGCGAL do obsługi OpenGraphics
Group:		Development/Libraries
Requires:	%{name}-devel%{?_isa} = %{version}-%{release}
Requires:	%{name}-osg%{?_isa} = %{version}-%{release}
Requires:	OpenSceneGraph-devel%{?_isa}

%description osg-devel
Header files for SFCGAL OpenGraphics support library.

%description osg-devel -l pl.UTF-8
Pliki nagłówkowe biblioteki SGCGAL do obsługi OpenGraphics.

%package apidocs
Summary:	API documentation for SFCGAL library
Summary(pl.UTF-8):	Dokumentacja API biblioteki SFCGAL
Group:		Documentation
BuildArch:	noarch

%description apidocs
API documentation for SFCGAL library.

%description apidocs -l pl.UTF-8
Dokumentacja API biblioteki SFCGAL.

%prep
%setup -q -n %{name}-v%{version}

%build
install -d build
cd build
%cmake .. \
	%{?with_apidocs:-DSFCGAL_BUILD_DOC=ON} \
	%{?with_osg:-DSFCGAL_WITH_OSG=ON}

%{__make}

%if %{with apidocs}
%{__make} doc
%endif

%install
rm -rf $RPM_BUILD_ROOT

%{__make} -C build install \
	DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%post	osg -p /sbin/ldconfig
%postun	osg -p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc AUTHORS NEWS PSC.md README.md SECURITY.md
%{_libdir}/libSFCGAL.so.*.*.*
%ghost %{_libdir}/libSFCGAL.so.2

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/sfcgal-config
%{_libdir}/libSFCGAL.so
%{_includedir}/SFCGAL
%exclude %{_includedir}/SFCGAL/detail/io/OsgFactory.h
%exclude %{_includedir}/SFCGAL/io/osg.h
%{_libdir}/cmake/SFCGAL
%{_pkgconfigdir}/sfcgal.pc

%if %{with osg}
%files osg
%defattr(644,root,root,755)
%{_libdir}/libSFCGAL-osg.so.*.*.*
%ghost %{_libdir}/libSFCGAL-osg.so.2

%files osg-devel
%defattr(644,root,root,755)
%{_libdir}/libSFCGAL-osg.so
%{_includedir}/SFCGAL/detail/io/OsgFactory.h
%{_includedir}/SFCGAL/io/osg.h
%endif

%if %{with apidocs}
%files apidocs
%defattr(644,root,root,755)
%doc doc/html/*.{css,html,js,png}
%endif
