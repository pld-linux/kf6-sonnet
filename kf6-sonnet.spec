#
# Conditional build:
%bcond_with	tests		# build with tests
# TODO:
# - fix build with aspell
%define		kdeframever	6.5
%define		qtver		5.15.2
%define		kfname		sonnet

Summary:	Multi-language spell checker
Summary(pl.UTF-8):	Wielojęzyczne narzędzie do sprawdzania pisowni
Name:		kf6-%{kfname}
Version:	6.5.0
Release:	1
License:	LGPL v2.1+
Group:		X11/Libraries
Source0:	https://download.kde.org/stable/frameworks/%{kdeframever}/%{kfname}-%{version}.tar.xz
# Source0-md5:	afe1cc49342b0b78993172c8a9e1dc20
URL:		http://www.kde.org/
BuildRequires:	Qt6Core-devel >= %{qtver}
BuildRequires:	Qt6Test-devel >= %{qtver}
BuildRequires:	Qt6Widgets-devel >= %{qtver}
BuildRequires:	aspell
BuildRequires:	aspell-devel
BuildRequires:	cmake >= 3.16
BuildRequires:	hspell-devel
BuildRequires:	hunspell-devel
BuildRequires:	kf6-extra-cmake-modules >= %{version}
BuildRequires:	libvoikko-devel
BuildRequires:	ninja
BuildRequires:	qt6-linguist >= %{qtver}
BuildRequires:	rpmbuild(macros) >= 1.736
BuildRequires:	tar >= 1:1.22
BuildRequires:	xz
BuildRequires:	zlib-devel
Requires:	Qt6Core >= %{qtver}
Requires:	Qt6Widgets >= %{qtver}
Requires:	kf6-dirs
#Obsoletes:	kf5-%{kfname} < %{version}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		qt6dir		%{_libdir}/qt6

%description
Sonnet is a plugin-based spell checking library for Qt-based
applications. It supports several different plugins, including HSpell,
ASpell and HUNSPELL.

It also supports automated language detection, based on a combination
of different algorithms.

The simplest way to use Sonnet in your application is to use the
SpellCheckDecorator class on your QTextEdit.

%description -l pl.UTF-8
Sonnet to oparta na wtyczkach biblioteka do sprawdzania pisowni dla
aplikacji opartych na Qt. Obsługuje kilka różnych wtyzek, w tym
HSpell, ASpell i HUNSPELL.

Pozwala automatycznie wykrywać język w oparciu o połączenie
różnych algorytmów.

Najprostszy sposób użycia Sonneta w aplikacji to użycie klasy
SpellCheckDecorator w obiekcie QTextEdit.

%package devel
Summary:	Header files for %{kfname} development
Summary(pl.UTF-8):	Pliki nagłówkowe dla programistów używających %{kfname}
Group:		X11/Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	Qt6Core-devel >= %{qtver}
#Obsoletes:	kf5-%{kfname}-devel < %{version}

%description devel
Header files for %{kfname} development.

%description devel -l pl.UTF-8
Pliki nagłówkowe dla programistów używających %{kfname}.

%prep
%setup -q -n %{kfname}-%{version}

%build
%cmake -B build \
	-G Ninja \
	%{!?with_tests:-DBUILD_TESTING=OFF} \
	-DKDE_INSTALL_USE_QT_SYS_PATHS=ON

%ninja_build -C build

%if %{with tests}
%ninja_build -C build test
%endif


%install
rm -rf $RPM_BUILD_ROOT
%ninja_install -C build

%find_lang %{kfname}6_qt --with-qm --all-name --with-kde

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files -f %{kfname}6_qt.lang
%defattr(644,root,root,755)
%doc README.md
%attr(755,root,root) %{_bindir}/parsetrigrams6
%ghost %{_libdir}/libKF6SonnetCore.so.6
%attr(755,root,root) %{_libdir}/libKF6SonnetCore.so.*.*
%ghost %{_libdir}/libKF6SonnetUi.so.6
%attr(755,root,root) %{_libdir}/libKF6SonnetUi.so.*.*
%dir %{qt6dir}/plugins/kf6/sonnet
%attr(755,root,root) %{qt6dir}/plugins/kf6/sonnet/sonnet_aspell.so
%attr(755,root,root) %{qt6dir}/plugins/kf6/sonnet/sonnet_hspell.so
%attr(755,root,root) %{qt6dir}/plugins/kf6/sonnet/sonnet_hunspell.so
%attr(755,root,root) %{qt6dir}/plugins/kf6/sonnet/sonnet_voikko.so
%attr(755,root,root) %{_libdir}/qt6/plugins/designer/sonnet6widgets.so
%attr(755,root,root) %{_libdir}/qt6/qml/org/kde/sonnet/libsonnetquickplugin.so
%dir %{_libdir}/qt6/qml/org/kde/sonnet
%{_libdir}/qt6/qml/org/kde/sonnet/qmldir
%{_libdir}/qt6/qml/org/kde/sonnet/kde-qmlmodule.version
%{_libdir}/qt6/qml/org/kde/sonnet/sonnetquickplugin.qmltypes
%{_datadir}/qlogging-categories6/sonnet.categories
%{_datadir}/qlogging-categories6/sonnet.renamecategories

%files devel
%defattr(644,root,root,755)
%{_includedir}/KF6/SonnetCore
%{_includedir}/KF6/SonnetUi
%{_includedir}/KF6/Sonnet
%{_libdir}/cmake/KF6Sonnet
%{_libdir}/libKF6SonnetCore.so
%{_libdir}/libKF6SonnetUi.so
