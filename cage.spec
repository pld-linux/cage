# Conditional build:
%bcond_with	system_wlroots	# Link with system wlroots

%define		wlroots_ver	0.16.2

Summary:	A Wayland kiosk
Name:		cage
Version:	0.1.5
Release:	2
License:	MIT
Group:		Applications
Source0:	https://github.com/cage-kiosk/cage/releases/download/v%{version}/%{name}-%{version}.tar.gz
# Source0-md5:	616bde2178a3c88f3238d9d26446a259
Source1:	https://gitlab.freedesktop.org/wlroots/wlroots/-/releases/%{wlroots_ver}/downloads/wlroots-%{wlroots_ver}.tar.gz
# Source1-md5:	cea876a8833d60ab65548ef60aae14b7
Patch0:		wlroots-version.patch
Patch1:		wlroots-x32.patch
Patch2:		wlroots-gcc14.patch
URL:		https://www.hjdskes.nl/projects/cage/
BuildRequires:	meson >= 0.58.1
BuildRequires:	ninja
BuildRequires:	pixman-devel
BuildRequires:	pkgconfig
BuildRequires:	rpmbuild(macros) >= 1.736
BuildRequires:	scdoc >= 1.9.2
BuildRequires:	wayland-devel
BuildRequires:	wayland-protocols >= 1.14
BuildRequires:	xorg-lib-libxkbcommon-devel
%if %{with system_wlroots}
BuildRequires:	wlroots-devel >= 0.16.0
BuildRequires:	wlroots-devel < 0.17.0
%else
BuildRequires:	EGL-devel
BuildRequires:	Mesa-libgbm-devel >= 21.1.0
BuildRequires:	OpenGLESv2-devel
BuildRequires:	Vulkan-Loader-devel >= 1.2.182
BuildRequires:	glslang >= 11.0.0
BuildRequires:	hwdata >= 0.364
BuildRequires:	libdrm-devel >= 2.4.113
BuildRequires:	libinput-devel >= 1.19.0
BuildRequires:	libseat-devel >= 0.2.0
BuildRequires:	libxcb-devel
BuildRequires:	pixman-devel
BuildRequires:	udev-devel
BuildRequires:	wayland-protocols >= 1.27
BuildRequires:	xcb-util-errors-devel
BuildRequires:	xcb-util-renderutil-devel
BuildRequires:	xcb-util-wm-devel
BuildRequires:	xorg-xserver-Xwayland-devel
%endif
%{?with_system_wlroots:Requires:	wlroots >= 0.16.0}
Requires:	xorg-xserver-Xwayland
%if %{without system_wlroots}
Requires:	Mesa-libgbm >= 21.1.0
Requires:	Vulkan-Loader >= 1.2.182
Requires:	libdrm >= 2.4.113
Requires:	libinput >= 1.19.0
Requires:	libseat >= 0.2.0
Requires:	wayland >= 1.21
%endif
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Cage is a kiosk compositor for Wayland. A kiosk is a window manager
(in the X11 world) or compositor (in the Wayland world) that is
designed for a user experience wherein user interaction and activities
outside the scope of the running application are prevented. That is, a
kiosk compositor displays a single maximized application at a time and
prevents the user from interacting with anything but this application.

%prep
%setup -q %{!?with_system_wlroots:-a1}

%patch0 -p1

%if %{without system_wlroots}
%{__mkdir} subprojects
%{__mv} wlroots-%{wlroots_ver} subprojects/wlroots
%patch1 -p1 -d subprojects/wlroots
%patch2 -p1 -d subprojects/wlroots
%endif

%build
%meson build \
	-Dxwayland=true \
%if %{without system_wlroots}
	--force-fallback-for=wlroots \
	-Dwlroots:default_library=static \
	-Dwlroots:examples=false
%endif

%ninja_build -C build

%install
rm -rf $RPM_BUILD_ROOT

%ninja_install -C build

%if %{without system_wlroots}
%{__rm} -r $RPM_BUILD_ROOT{%{_includedir}/wlr,%{_libdir}/libwlroots.a,%{_pkgconfigdir}/wlroots.pc}
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc README.md
%attr(755,root,root) %{_bindir}/cage
%{_mandir}/man1/cage.1*
