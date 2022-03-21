Summary:	A Wayland kiosk
Name:		cage
Version:	0.1.4
Release:	3
License:	MIT
Group:		Applications
Source0:	https://github.com/Hjdskes/cage/releases/download/v%{version}/%{name}-%{version}.tar.gz
# Source0-md5:	b5874157dbded445cfe674a54805bca9
Patch0:		wlroots-0.15.patch
URL:		https://www.hjdskes.nl/projects/cage/
BuildRequires:	meson
BuildRequires:	ninja
BuildRequires:	pixman-devel
BuildRequires:	rpmbuild(macros) >= 1.736
BuildRequires:	scdoc >= 1.9.2
BuildRequires:	wayland-devel
BuildRequires:	wayland-protocols >= 1.14
BuildRequires:	wlroots-devel >= 0.15.0
BuildRequires:	xorg-lib-libxkbcommon-devel
Requires:	wlroots >= 0.14.0
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
%setup -q
%patch0 -p1

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
