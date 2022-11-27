%{?!python3_pkgversion:%global python3_pkgversion 3}

%global srcname input-remapper

Name:          input-remapper 
# Version:       %{git_tag} 
Version:       1.5.0 
Release:       1%{?dist}
Summary:       A tool to change the mapping of your input device buttons 
License:       GPL-3.0
URL:           https://github.com/sezanzeb/input-remapper 
Source0:       input-remapper-1.5.0.tar.gz 

BuildArch:     noarch 

BuildRequires:  systemd
BuildRequires:  systemd-rpm-macros
BuildRequires:  gettext
BuildRequires:  python%{python3_pkgversion}-devel
BuildRequires:  python%{python3_pkgversion}-setuptools
BuildRequires:  python%{python3_pkgversion}-evdev
BuildRequires:  python%{python3_pkgversion}-pydbus
BuildRequires:  python%{python3_pkgversion}-gobject
BuildRequires:  python%{python3_pkgversion}-pydantic

%{?python_enable_dependency_generator}

%description
...


%package -n python%{python3_pkgversion}-%{srcname}
Summary:        %{summary}
%{?python_provide:%python_provide python3-%{srcname}}

%if %{undefined python_enable_dependency_generator} && %{undefined python_disable_dependency_generator}
# Put manual requires here:
Requires:       systemd
Requires:       dbus
Requires:       python%{python3_pkgversion}-pydbus
Requires:       gtk
Requires:       python%{python3_pkgversion}-gobject
Requires:       python%{python3_pkgversion}-evdev
Requires:       python%{python3_pkgversion}-pydantic
%endif

%description -n python%{python3_pkgversion}-%{srcname}
An easy to use tool to change the mapping of your input device buttons.
Supports mice, keyboards, gamepads, X11, Wayland, combined buttons and
programmable macros.
Allows mapping non-keyboard events (click, joystick, wheel) to keys of
keyboard devices.


%prep
%autosetup -p1 -n %{srcname}-%{version}


%build
# % py3_shebang_fix
%py3_build


%install
rm -rf $RPM_BUILD_ROOT
%py3_install
rm $RPM_BUILD_ROOT/usr/share/input-remapper/99-input-remapper.rules
rm $RPM_BUILD_ROOT/usr/share/input-remapper/input-remapper-autoload.desktop
rm $RPM_BUILD_ROOT/usr/share/input-remapper/input-remapper.desktop
rm $RPM_BUILD_ROOT/usr/share/input-remapper/input-remapper.policy
rm $RPM_BUILD_ROOT/usr/share/input-remapper/input-remapper.service
rm $RPM_BUILD_ROOT/usr/share/input-remapper/inputremapper.Control.conf

%check
# %{__python3} setup.py test


%post
%systemd_post %{name}.service


%preun
%systemd_preun %{name}.service


%postun
%systemd_postun_with_restart %{name}.service


%files -n  python%{python3_pkgversion}-%{srcname}
%license LICENSE
%doc README.md 
%{python3_sitelib}/inputremapper/
%{python3_sitelib}/input_remapper-%{version}-py%{python3_version}.egg-info/
%{_datadir}/%{name}/
%doc %lang(it_IT) %{_datadir}/%{name}/lang/it_IT/LC_MESSAGES/input-remapper.mo
%doc %lang(sk_SK) %{_datadir}/%{name}/lang/sk_SK/LC_MESSAGES/input-remapper.mo
%doc %lang(zh_CN) %{_datadir}/%{name}/lang/zh_CN/LC_MESSAGES/input-remapper.mo
%{_datadir}/applications/%{name}.desktop
%{_datadir}/polkit-1/actions/%{name}.policy
%{_unitdir}/%{name}.service
%config(noreplace) %{_sysconfdir}/dbus-1/system.d/inputremapper.Control.conf
%config(noreplace) %{_sysconfdir}/xdg/autostart/%{name}-autoload.desktop
%{_udevrulesdir}/99-%{name}.rules
%{_bindir}/input-remapper-gtk
%{_bindir}/input-remapper-service
%{_bindir}/input-remapper-control
%{_bindir}/input-remapper-helper
# those will be deleted at some point:
%{_bindir}/key-mapper-gtk
%{_bindir}/key-mapper-service
%{_bindir}/key-mapper-control


%changelog
* Fri Nov 04 2022 Arnošt Dudek <arnost@arnostdudek.cz> - 1.5.0
- initial build
