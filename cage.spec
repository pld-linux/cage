%define		gitref	5f4c43db04093edf8452efb3b04c3a3c720c78de

Summary:	A Wayland kiosk
Name:		cage
Version:	0.1.4
Release:	4
License:	MIT
Group:		Applications
Source0:	https://github.com/Hjdskes/cage/archive/%{gitref}/%{name}-%{gitref}.tar.gz
# Source0-md5:	75a49decbf2022e849b5eaa66c8bc763
URL:		https://www.hjdskes.nl/projects/cage/
BuildRequires:	meson >= 0.58.1
BuildRequires:	ninja
BuildRequires:	pixman-devel
BuildRequires:	pkgconfig
BuildRequires:	rpmbuild(macros) >= 1.736
BuildRequires:	scdoc >= 1.9.2
BuildRequires:	wayland-devel
BuildRequires:	wayland-protocols >= 1.14
BuildRequires:	wlroots-devel >= 0.16.0
BuildRequires:	xorg-lib-libxkbcommon-devel
Requires:	wlroots >= 0.16.0
Requires:	xorg-xserver-Xwayland
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Cage is a kiosk compositor for Wayland. A kiosk is a window manager
(in the X11 world) or compositor (in the Wayland world) that is
designed for a user experience wherein user interaction and activities
outside the scope of the running application are prevented. That is, a
kiosk compositor displays a single maximized application at a time and
prevents the user from interacting with anything but this application.

%prep
%setup -q -n %{name}-%{gitref}

%build
%meson build \
	-Dxwayland=true

%ninja_build -C build

%install
rm -rf $RPM_BUILD_ROOT

%ninja_install -C build

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc README.md
%attr(755,root,root) %{_bindir}/cage
%{_mandir}/man1/cage.1*
