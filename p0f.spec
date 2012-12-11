%define name p0f
%define version 2.0.8
%define release %mkrel 7
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
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot
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
rm -Rf %{buildroot}
%setup -q -n %{name}

%build
%make -f mk/Linux CFLAGS='%optflags -DUSE_BPF=\"pcap-bpf.h\"'

%install
%__install -d %{buildroot}{%{_sysconfdir}/sysconfig,%{_sysconfdir}/%{name},%{_initrddir}}
%__install -d %{buildroot}/%{_bindir}
%__install -d %{buildroot}/%{_sbindir}
%__install -d %{buildroot}/%{_mandir}/man1/
%__cp -p p0f.fp %{buildroot}/%{_sysconfdir}/%{name}
bzcat %{SOURCE1} > %{buildroot}/%{_initrddir}/%{name}
bzcat %{SOURCE2} > %{buildroot}/%{_sysconfdir}/sysconfig/%{name}

# ugly hack, to correct the fact that p0f doesn't go by himself in the background.
# easier to code than a patch ( at least, for me )
# this script is called by the init script
echo '#!/bin/sh
p0f -q $* &
com=$!
sleep 3
# if the command is still here( ie not crashed )
# grep will return a good return value
ps | awk "{print \$1}" | grep $com 1>/dev/null 2>&1'> %{buildroot}/%{_sbindir}/%{daemon}
chmod +x %{buildroot}/%{_sbindir}/%{daemon}

%__cp -p p0f p0frep %{buildroot}/%{_bindir}
%__cp -p p0f.1 %{buildroot}/%{_mandir}/man1/

%clean
rm -rf %{buildroot}

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




%changelog
* Mon Sep 14 2009 Thierry Vignaud <tvignaud@mandriva.com> 2.0.8-7mdv2010.0
+ Revision: 440468
- rebuild

* Tue Mar 10 2009 Emmanuel Andry <eandry@mandriva.org> 2.0.8-6mdv2009.1
+ Revision: 353465
- fix initscript (#26333)

* Wed Oct 29 2008 Oden Eriksson <oeriksson@mandriva.com> 2.0.8-5mdv2009.1
+ Revision: 298327
- rebuilt against libpcap-1.0.0

* Wed Jul 23 2008 Thierry Vignaud <tvignaud@mandriva.com> 2.0.8-4mdv2009.0
+ Revision: 241131
- rebuild
- kill re-definition of %%buildroot on Pixel's request

  + Olivier Blin <oblin@mandriva.com>
    - restore BuildRoot

* Thu Aug 23 2007 Thierry Vignaud <tvignaud@mandriva.com> 2.0.8-2mdv2008.0
+ Revision: 70388
- fileutils, sh-utils & textutils have been obsoleted by coreutils a long time ago


* Wed Sep 06 2006 Olivier Thauvin <nanardon@mandriva.org>
+ 2006-09-06 17:46:41 (60384)
- 2.0.8

* Wed Sep 06 2006 Olivier Thauvin <nanardon@mandriva.org>
+ 2006-09-06 17:41:27 (60383)
Import p0f

* Fri Mar 10 2006 Olivier Thauvin <nanardon@mandriva.org> 2.0.6-2mdk
- fix prereq

* Fri Mar 10 2006 Olivier Thauvin <nanardon@mandriva.org> 2.0.6-1mdk
- 2.0.6

* Wed Jul 13 2005 Oden Eriksson <oeriksson@mandriva.com> 2.0.5-3mdk
- rebuilt against new libpcap-0.9.1 (aka. a "play safe" rebuild)

* Sat Apr 16 2005 Giuseppe Ghibò <ghibo@mandriva.com> 2.0.5-2mdk
- removed libpcap0 explicit requires (for X86-64).

* Tue Sep 14 2004 Olivier Thauvin <thauvin@aerov.jussieu.fr> 2.0.5-1mdk
* Mon Jul 12 2004 Tibor Pittich <Tibor.Pittich@mandrake.org> 2.0.4-2mdk
- corect location of fingerprint file
- added man page

* Sun Jul 11 2004 Michael Scherer <misc@mandrake.org> 2.0.4-1mdk
- New release 2.0.4
- use the good tarball

* Mon Apr 26 2004 Olivier Thauvin <thauvin@aerov.jussieu.fr> 2.0.3-2mdk
- patch0 (renamed pcap include) Bug #9600

* Mon Nov 03 2003 Olivier Thauvin <thauvin@aerov.jussieu.fr> 2.0.3-1mdk
- 2.0.3

