#
Summary:	iSight Firmware Tools
Name:		isight-firmware-tools
Version:	1.0.2
Release:	5
License:	GPLv2+
Group:		Applications
Source0:	http://bersace03.free.fr/ift/%{name}-%{version}.tar.gz
# Source0-md5:	b8d1e80cf8d47f9aa4f683b995cd359c
URL:		http://bersace03.free.fr/ift/
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	libgcrypt-devel
BuildRequires:	rpmbuild(macros) >= 1.228
Requires:	udev-core >= 1:127
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
This project provide tools to manipulate firmware for Built-in iSight
found on Apple machine since iMac G5 iSight.

%prep
%setup -q
%{__sed} -i -e 's#@udevdir@#/lib/udev#g' isight.rules.in

%build
%{__aclocal}
%{__autoconf}
%{__automake}
%configure
%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT \
	libudevdir=/lib/udev

#%find_lang %{name}

%clean
rm -rf $RPM_BUILD_ROOT

%post
if [ "$1" = 1 ]; then
%banner %{name} -e <<EOF
NOTE:
In order to get a working Built-in iSight camera
you need to copy the iSight Firmware from your Mac OS X.
It is usually the file /System/Library/Extensions/IOUSBFamily.kext/Contents/PlugIns/AppleUSBVideoSupport.kext/Contents/MacOS/AppleUSBVideoSupport

EOF
fi

#%files -f %{name}.lang
%files
%defattr(644,root,root,755)
%doc README HOWTO AUTHORS ABOUT-NLS
%attr(755,root,root) %{_bindir}/ift-*
%attr(755,root,root) /lib/udev/ift-load
/etc/udev/rules.d/isight.rules
%{_infodir}/ift-export.info.gz
%{_infodir}/ift-extract.info.gz
%{_mandir}/man1/ift-export.1*
%{_mandir}/man1/ift-extract.1*
