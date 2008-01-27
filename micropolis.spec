
%define name	micropolis
# activity/activity.info = 7
# src/sim/sim.c and about = 4.0
%define version	4.0
%define rel	6

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
# Lots of fixes from
# http://git.zerfleddert.de/cgi-bin/gitweb.cgi/micropolis
Patch0:		micropolis-zerfleddert.20080120.patch
# And more fixes as incremental patches:
# git clone git://git.zerfleddert.de/micropolis
# cd micropolis
# git-format-patch -o .. 06fa6a70a8ac0c94b675f748d91f968ed6c6578e
Patch101:	0001-fix-typo-in-crime-alert.patch
Patch102:	0002-fix-modifier-problems-like-NumLock-by-ignoring-hat.patch
Patch103:	0003-make-double-click-work-on-OS-X.patch
Patch104:	0004-allow-scenario-window-to-be-closed.patch
Patch105:	0005-draw-a-solid-overlay-when-requested.patch
Patch106:	0006-re-add-disabled-air-crash-disaster.patch
Patch107:	0007-fix-remaining-NumLock-problems-by-teaching-tk-to-det.patch
Patch108:	0008-fix-power-grid-overlay-on-big-endian-X-servers.patch
Patch109:	0009-Add-Pause-to-Priority-menu.patch
Patch110:	0010-handle-spaces-in-filenames.patch
Patch111:	0011-handle-spaces-in-path-names-too.patch
Patch112:	0012-still-more-NumLock-fixes-this-time-for-scrollbars-a.patch
Patch113:	0013-fix-fire-coverage-overlay-by-iterating-over-the-whol.patch
Patch114:	0014-show-description-including-time-limit-when-hoverin.patch
Patch115:	0015-don-t-quit-immediately-when-the-user-loses-a-scenari.patch
License:	GPLv3+ with additional terms
BuildRoot:	%{_tmppath}/%{name}-root
BuildRequires:	libxpm-devel
BuildRequires:	libx11-devel
BuildRequires:	libxext-devel
BuildRequires:	bison
BuildRequires:	ImageMagick
# Plays audio through aplay:
Requires:	alsa-utils

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
%patch101 -p1
%patch102 -p1
%patch103 -p1
%patch104 -p1
%patch105 -p1
%patch106 -p1
%patch107 -p1
%patch108 -p1
%patch109 -p1
%patch110 -p1
%patch111 -p1
%patch112 -p1
%patch113 -p1
%patch114 -p1
%patch115 -p1

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

%post
%update_menus

%postun
%clean_menus

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
