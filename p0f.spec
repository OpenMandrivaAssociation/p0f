Name:       p0f
Version:    3.07b
Release:    3
Summary:    Passive OS fingerprinting tool
License:    GPL
Group:      Networking/Other
URL:        https://lcamtuf.coredump.cx/p0f.shtml
Source0:    http://lcamtuf.coredump.cx/p0f/%{name}-%{version}.tgz
Source1:    p0f.service
Source2:    p0f.sysconfig
BuildRequires: pcap-devel

%description
p0f performs passive OS fingerprinting technique bases on information coming
from remote host when it establishes connection to our system. Captured
packets contains enough information to determine OS - and, unlike
active scanners (nmap, queSO) - it is done without sending anything to 
this host.

%prep
%setup -q

%build
%make CFLAGS='%{optflags} -DFP_FILE="%{_sysconfdir}/%{name}/p0f.fp"'

%install
install -D -m 755 p0f %{buildroot}%{_sbindir}/p0f
install -D -m 644 p0f.fp %{buildroot}%{_sysconfdir}/%{name}/%{name}.fp
install -D -m 644 %{SOURCE1} %{buildroot}%{_unitdir}/p0f.service
install -D -m 644 %{SOURCE2} %{buildroot}%{_sysconfdir}/sysconfig/p0f
mkdir -p %{buildroot}/var/run/%{name}

%pre
%_pre_useradd %{name} /var/run/%{name} /bin/false

%post
%systemd_post %{name}.service

%preun
%systemd_preun %{name}.service

%postun
%systemd_postun_with_restart %{name}.service
%_postun_userdel %{name}

%files
%doc docs/*
%dir %{_sysconfdir}/%{name}
%config(noreplace) %{_sysconfdir}/%{name}/p0f.fp
%config(noreplace) %{_sysconfdir}/sysconfig/p0f
%{_unitdir}/p0f.service
%{_sbindir}/p0f
/var/run/%{name}
