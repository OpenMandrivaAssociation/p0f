%define name p0f
%define version 2.0.8
%define release %mkrel 2
%define daemon %{name}d

# TODO
# * mysql support => depedency, config file and so on.
# * for mysql version, should create the database at first connection.
#   use a mysql | wc -l, or something like that.
# * don't forget the permission of the config for mysql !
#
Name: %{name}
Summary: Passive OS fingerprinting tool
Version: %{version}
Release: %{release}
License: GPL
Group: Networking/Other
Source0: http://lcamtuf.coredump.cx/p0f/%{name}-%{version}.tar.bz2
Source1: %{name}.init.mdk.bz2
Source2: %{name}.sysconfig.bz2
URL: http://lcamtuf.coredump.cx/p0f.shtml
BuildRoot: %{_tmppath}/%{name}-buildroot
BuildRequires: libpcap-devel
Requires: chkconfig
Requires: coreutils
Requires: grep
Requires: awk
Requires(post): rpm-helper
Requires(preun): rpm-helper

%description
p0f performs passive OS fingerprinting technique bases on information coming
from remote host when it establishes connection to our system. Captured
packets contains enough information to determine OS - and, unlike
active scanners (nmap, queSO) - it is done without sending anything to 
this host.

%prep
rm -Rf $RPM_BUILD_ROOT
%setup -q -n %{name}

%build
%make -f mk/Linux CFLAGS='%optflags -DUSE_BPF=\"pcap-bpf.h\"'

%install
%__install -d $RPM_BUILD_ROOT{%{_sysconfdir}/sysconfig,%{_sysconfdir}/%{name},%{_initrddir}}
%__install -d $RPM_BUILD_ROOT/%{_bindir}
%__install -d $RPM_BUILD_ROOT/%{_sbindir}
%__install -d $RPM_BUILD_ROOT/%{_mandir}/man1/
%__cp -p p0f.fp $RPM_BUILD_ROOT/%{_sysconfdir}/%{name}
bzcat %{SOURCE1} > $RPM_BUILD_ROOT/%{_initrddir}/%{name}
bzcat %{SOURCE2} > $RPM_BUILD_ROOT/%{_sysconfdir}/sysconfig/%{name}

# ugly hack, to correct the fact that p0f doesn't go by himself in the background.
# easier to code than a patch ( at least, for me )
# this script is called by the init script
echo '#!/bin/sh
p0f -q $* &
com=$!
sleep 3
# if the command is still here( ie not crashed )
# grep will return a good return value
ps | awk "{print \$1}" | grep $com 1>/dev/null 2>&1'> $RPM_BUILD_ROOT/%{_sbindir}/%{daemon}
chmod +x $RPM_BUILD_ROOT/%{_sbindir}/%{daemon}

%__cp -p p0f p0frep $RPM_BUILD_ROOT/%{_bindir}
%__cp -p p0f.1 $RPM_BUILD_ROOT/%{_mandir}/man1/

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root,755)
%doc doc/COPYING doc/CREDITS doc/INSTALL.Win32 doc/KNOWN_BUGS doc/README 
%doc doc/TODO 
%config(noreplace) %attr(644,root,root) %{_sysconfdir}/sysconfig/%{name}
%dir %attr(755,root,root) %{_sysconfdir}/%{name}
%config(noreplace) %attr(644,root,root) %{_sysconfdir}/%{name}/p0f.fp
%config(noreplace) %attr(755,root,root) %{_initrddir}/%{name}
%{_bindir}/p0frep
%{_bindir}/p0f
%{_sbindir}/%{daemon}
%{_mandir}/man1/*

%post
%_post_service %{name}

%preun
%_preun_service %{name}

