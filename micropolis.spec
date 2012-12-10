
%define name	micropolis
# activity/activity.info = 7
# src/sim/sim.c and about = 4.0
%define version	4.0
%define rel	10

Summary:	City simulation based on Maxis SimCity
Name:		%{name}
Version:	%{version}
Release:	%mkrel %{rel}
Group:		Games/Strategy
URL:		http://www.donhopkins.com/home/micropolis/
# Also see http://dev.laptop.org/git?p=projects/micropolis-activity
Source:		http://www.donhopkins.com/home/micropolis/micropolis-activity-source.tgz
Patch1:		micropolis-path.patch
# From debian, optflags patch:
Patch2:		micropolis-makefile.patch
# (Anssi 01/2008): Fix some 64bit pointer warnings. It is likely they are
# harmless corner cases, but this code is so old I don't take any chances.
Patch3:		micropolis-64bit-warns.patch
Patch4:		micropolis-printf-format.patch
# Lots of fixes from
# http://git.zerfleddert.de/cgi-bin/gitweb.cgi/micropolis
# curl http://rmdir.de/~michael/micropolis_git.patch > micropolis-zerfleddert.$(date +%Y%m%d).patch
Patch0:		micropolis-zerfleddert.20080302.patch
License:	GPLv3+ with additional terms
BuildRoot:	%{_tmppath}/%{name}-root
BuildRequires:	libxpm-devel
BuildRequires:	libx11-devel
BuildRequires:	libxext-devel
BuildRequires:	SDL-devel
BuildRequires:	SDL_mixer-devel
BuildRequires:	bison
BuildRequires:	imagemagick

%description
City-building simulation game originally released as SimCity by
Maxis and subsequently released as free software, renamed to
Micropolis.

%prep
%setup -q -n micropolis-activity
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1

#[ $(sed -n 's,activity_version = ,,p' activity/activity.info) = %version ]
[ $(sed -r -n 's,^.*MicropolisVersion = "(.+)".*$,\1,p' src/sim/sim.c) = %version ]

perl -pi -e 's,GAMESDATADIR,%{_gamesdatadir},;s,LIBDIR,%{_libdir},' Micropolis

# Re-enable air crash:
perl -pi -e 's,-DNO_AIRCRASH,,' src/sim/makefile

%build
%make OPTFLAGS="%optflags" -C src

%install
rm -rf %{buildroot}
install -d -m755 %{buildroot}%{_gamesbindir}
install -d -m755 %{buildroot}%{_gamesdatadir}/%{name}
install -d -m755 %{buildroot}%{_libdir}/%{name}

install -m755 src/sim/sim %{buildroot}%{_libdir}/%{name}
install -m755 Micropolis %{buildroot}%{_gamesbindir}/%{name}

cp -a cities images res %{buildroot}%{_gamesdatadir}/%{name}
chmod +x %{buildroot}%{_gamesdatadir}/%{name}/res/sounds/player

install -d -m755 %{buildroot}%{_miconsdir}
install -d -m755 %{buildroot}%{_iconsdir}
install -d -m755 %{buildroot}%{_liconsdir}

convert Micropolis.png -resize x16 %{buildroot}%{_miconsdir}/%{name}.png
convert Micropolis.png -resize x32 %{buildroot}%{_iconsdir}/%{name}.png
convert Micropolis.png -resize x48 %{buildroot}%{_liconsdir}/%{name}.png

mkdir -p %{buildroot}%{_datadir}/applications
cat > %{buildroot}%{_datadir}/applications/mandriva-%{name}.desktop <<EOF
[Desktop Entry]
Name=Micropolis
GenericName=City simulation
Exec=%{_gamesbindir}/%{name}
Icon=%{name}
Terminal=false
Type=Application
StartupNotify=false
Categories=Game;StrategyGame;
EOF

%clean
rm -rf %{buildroot}

%if %mdkversion < 200900
%post
%update_menus
%endif

%if %mdkversion < 200900
%postun
%clean_menus
%endif

%files
%defattr(-,root,root)
%doc manual/*
%{_gamesbindir}/%{name}
%{_gamesdatadir}/%{name}
%{_libdir}/%{name}
%{_miconsdir}/%{name}.png
%{_iconsdir}/%{name}.png
%{_liconsdir}/%{name}.png
%{_datadir}/applications/mandriva-%{name}.desktop


%changelog
* Fri Dec 10 2010 Oden Eriksson <oeriksson@mandriva.com> 4.0-10mdv2011.0
+ Revision: 620326
- the mass rebuild of 2010.0 packages

* Mon Sep 14 2009 Thierry Vignaud <tv@mandriva.org> 4.0-9mdv2010.0
+ Revision: 439802
- rebuild

* Sat Mar 07 2009 Anssi Hannula <anssi@mandriva.org> 4.0-8mdv2009.1
+ Revision: 351774
- fix printf format string (printf-format.patch)
- rebuild

  + Oden Eriksson <oeriksson@mandriva.com>
    - lowercase ImageMagick

  + Pixel <pixel@mandriva.com>
    - rpm filetriggers deprecates update_menus/update_scrollkeeper/update_mime_database/update_icon_cache/update_desktop_database/post_install_gconf_schemas

* Sun Mar 02 2008 Anssi Hannula <anssi@mandriva.org> 4.0-7mdv2008.1
+ Revision: 177743
- sync new fixes from Michael Gernoth's git repo

* Sun Jan 27 2008 Anssi Hannula <anssi@mandriva.org> 4.0-6mdv2008.1
+ Revision: 158681
- more fixes from Michael Gernoth
- re-enable air crash disaster

* Tue Jan 22 2008 Anssi Hannula <anssi@mandriva.org> 4.0-5mdv2008.1
+ Revision: 156365
- update buildrequires for backportability

* Mon Jan 21 2008 Anssi Hannula <anssi@mandriva.org> 4.0-4mdv2008.1
+ Revision: 155569
- fix start script on lib64 (Jean-Claude Stiegler)

* Sun Jan 20 2008 Anssi Hannula <anssi@mandriva.org> 4.0-3mdv
+ Revision: 155307
- fixes from Michael Gernoth's git repository:
  o fix typo in crime alert
  o fix modifier problems (like NumLock) by ignoring hateMod

* Sun Jan 20 2008 Anssi Hannula <anssi@mandriva.org> 4.0-2mdv2008.1
+ Revision: 155210
- fix some 64bit pointer warnings

* Sun Jan 20 2008 Anssi Hannula <anssi@mandriva.org> 4.0-1mdv2008.1
+ Revision: 155188
- initial Mandriva release

