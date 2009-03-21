%define rname           mozTrayBiff
%define pkgname         moztraybiff
%define tbver           2.0.0.21
%define tbdir           %{_libdir}/thunderbird-%{tbver}
%define tbextdir        %{tbdir}-extensions
%define tbextuuid       \{2e1b75f1-6b5a-4f1d-89b4-424f636e4fba\}
%define xpi             0

Name:           mozilla-thunderbird-%{pkgname}
Version:        1.2.4
Release:        %mkrel 4
Epoch:          0
Summary:        Mozilla New Mail Icon
URL:            http://moztraybiff.mozdev.org/
Source0:        http://downloads.mozdev.org/moztraybiff/mozTrayBiff-%{version}.tar.gz
Source1:        %{name}-chrome.manifest
Patch0:         %{name}-nspr.patch
License:        LGPL
Group:          Networking/Mail
Requires(post):   mozilla-thunderbird = 0:%{tbver}
Requires(postun): mozilla-thunderbird = 0:%{tbver}
BuildRequires:  gtk2-devel
BuildRequires:  mozilla-thunderbird-devel = 0:%{tbver}
BuildRequires:  libnspr-devel
BuildRequires:  zip
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-buildroot

%description
Mozilla New Mail Icon is an extension which displays an icon in the 
system tray when new mail arrives in your Mozilla or Mozilla 
Thunderbird. It supports the standard (FreeDesktop.org) system tray, as 
used by GNOME, KDE and IceWM.

This extension was previously called Mozilla Free Desktop Integration.

%prep
%setup -q -n %{rname}-%{version}
%patch0 -p1

%build
%{make} MOZ_TRUNK=1 MOZILLA_PLATFORM=tbird MULTI_PLATFORM=0 REAL_CONFIG=%{_bindir}/thunderbird-config

%install
%{__rm} -rf %{buildroot}
%{__mkdir_p} %{buildroot}%{tbextdir}
%if !%{xpi}
%{__mkdir_p} %{buildroot}%{tbdir}/extensions/%{tbextuuid}
%{_bindir}/unzip -qq mozTrayBiff-%{version}-tb%{tbver}-Linux_-gcc3.xpi -d %{buildroot}%{tbdir}/extensions/%{tbextuuid}
%{__install} -m 644 %{SOURCE1} %{buildroot}%{tbdir}/extensions/%{tbextuuid}/chrome.manifest
%else
%{__install} -m 644 mozTrayBiff-%{version}-tb%{tbver}-Linux_-gcc3.xpi %{buildroot}%{tbextdir}
%endif

%clean
%{__rm} -rf %{buildroot}

%post
if [ -f %{tbdir}/components/compreg.dat ]; then
    %{__rm} -f %{tbdir}/components/compreg.dat
fi

if [ -f %{tbdir}/components/xpti.dat ]; then
    %{__rm} -f %{tbdir}/components/xpti.dat
fi

TMPDIR= TB_TMPDIR=`/bin/mktemp -d -q -p /tmp -t %{name}.XXXXXXXXXX` && {
%if %{xpi}
    HOME="$TB_TMPDIR" LD_LIBRARY_PATH="%{tbdir}" %{tbdir}/thunderbird-bin -nox -install-global-extension %{tbextdir}/mozTrayBiff-%{version}-tb%{tbver}-Linux_-gcc3.xpi
%endif
    HOME="$TB_TMPDIR" LD_LIBRARY_PATH="%{tbdir}" %{tbdir}/thunderbird-bin -nox -register
    test -d "$TB_TMPDIR" && %{__rm} -rf -- "$TB_TMPDIR"
}

%postun
if [ -f %{tbdir}/components/xpti.dat ]; then
    %{__rm} -f %{tbdir}/components/xpti.dat
fi

if [ -f %{tbdir}/components/compreg.dat ]; then
    %{__rm} -f %{tbdir}/components/compreg.dat
fi

TMPDIR= TB_TMPDIR=`/bin/mktemp -d -q -p /tmp -t %{name}.XXXXXXXXXX` && {
%if %{xpi}
    HOME="$TB_TMPDIR" LD_LIBRARY_PATH="%{tbdir}" %{tbdir}/thunderbird-bin -nox -install-global-extension %{tbextdir}/mozTrayBiff-%{version}-tb%{tbver}-Linux_-gcc3.xpi
%endif
    HOME="$TB_TMPDIR" LD_LIBRARY_PATH="%{tbdir}" %{tbdir}/thunderbird-bin -nox -register
    test -d "$TB_TMPDIR" && %{__rm} -rf -- "$TB_TMPDIR"
}

%files
%defattr(-,root,root)
%doc changelog README
%if !%{xpi}
%{tbdir}/extensions/%{tbextuuid}
%else
%{tbextdir}/mozTrayBiff-%{version}-tb%{tbver}-Linux_-gcc3.xpi
%endif
