%define upstream_name mtr

Summary: my traceroute, an advanced traceroute utility
Name: openrepos-mtr
Version: 0.93
Release: 1
License: GPL
#Group: System Environment/Base
URL: https://github.com/traviscross/mtr

Source0: https://github.com/traviscross/%{upstream_name}/archive/v%{version}.tar.gz
#Source1: %%{name}.desktop
#Source2: %%{name}_86.png
#Source3: %%{name}_100.png
#Source4: %%{name}_256.png

BuildRoot: %{_tmppath}/%{upstream_name}-%{version}-%{release}-root

BuildRequires: ncurses-devel
BuildRequires: autoconf
BuildRequires: automake
Requires: ncurses-libs
Requires: libstdc++

%description
mtr combines the functionality of the 'traceroute' and 'ping' programs in a
single network diagnostic tool.

As mtr starts, it investigates the network connection between the host mtr runs
on and a user-specified destination host. After it determines the address of
each network hop between the machines, it sends a sequence of ICMP ECHO
requests to each one to determine the quality of the link to each machine. As
it does this, it prints running statistics about each machine.

%prep
%autosetup -p1 -n %{upstream_name}-%{version}
aclocal $ACLOCAL_OPTS
autoheader
automake --add-missing --copy --foreign
autoconf --force

%build
%configure -q -C \
	--program-prefix=openrepos- \
	--disable-bash-completion \
	--without-gtk \
	--enable-ipv6

make %{?_smp_mflags} -s -l4.8

%install
%{__rm} -rf %{buildroot}
# install calls install-exec-hook which calls setcap which can not be executed as a normal user building the package.
# so sets only install the binaries:
%{__make} install-sbinPROGRAMS DESTDIR="%{buildroot}"
#install -p -D -m 644 %%{SOURCE1} $RPM_BUILD_ROOT/%%{_datadir}/applications/%%{name}.desktop
#install -p -D -m 644 %%{SOURCE2} $RPM_BUILD_ROOT/%%{_datadir}/icons/hicolor/86x86/apps/%%{name}.png
#install -p -D -m 644 %%{SOURCE3} $RPM_BUILD_ROOT/%%{_datadir}/icons/hicolor/108x108/apps/%%{name}.png
#install -p -D -m 644 %%{SOURCE4} $RPM_BUILD_ROOT/%%{_datadir}/icons/hicolor/256x256/apps/%%{name}.png


%clean
%{__rm} -rf %{buildroot}

%files
%defattr(-, root, root, 0755)
%license COPYING
%{_sbindir}/%{name}
%{_sbindir}/%{name}-packet
#%%defattr(-, root, root, 0644)
#%%{_datadir}/icons/hicolor/86x86/apps/%%{name}.png
#%%{_datadir}/icons/hicolor/108x108/apps/%%{name}.png
#%%{_datadir}/icons/hicolor/256x256/apps/%%{name}.png
#%%{_datadir}/applications/%%{name}.desktop


%post
if [ -x /usr/sbin/setcap ]; then
  /usr/sbin/setcap cap_net_raw+ep %{_sbindir}/%{name}-packet || :
else
  chmod 1777   %{_sbindir}/%{name}-packet || :
fi
#/usr/bin/update-desktop-database -q || :


%postun
#/usr/bin/update-desktop-database -q || :


%changelog
* Wed Apr  8 08:48:46 CEST 2020 Nephros <sailfish@nephros.org> - 0.93-1
- first build
