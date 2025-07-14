# TODO
# - .spec for buidling -fw package
Summary:	iSight Firmware Tools
Name:		isight-firmware-tools
Version:	1.6
Release:	1
License:	GPL v2+
Group:		Applications
Source0:	https://launchpad.net/isight-firmware-tools/main/1.6/+download/%{name}-%{version}.tar.gz
# Source0-md5:	d2823c083dc0ef8a589ba3f84b8e9167
Patch0:		format-security.patch
URL:		http://bersace03.free.fr/ift/
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	gettext-tools
BuildRequires:	glib2-devel
BuildRequires:	hal-devel
BuildRequires:	intltool
BuildRequires:	libgcrypt-devel
BuildRequires:	libusb-compat-devel
BuildRequires:	pkgconfig
BuildRequires:	rpmbuild(macros) >= 1.228
%if "%{pld_release}" == "ti"
Requires:	udev-core >= 1:124-3
%else
Requires:	udev-core >= 1:127
%endif
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
A set of tool for firmware extraction from Mac OS X driver and loading
for use with udev. Use linux-uvc driver to access the isight. Support
all built-in iSight starting with iMac G5 iSight.

%prep
%setup -q
%patch -P0 -p1

%{__sed} -i -e 's,${libdir}/udev,/lib/udev,' configure.ac
%{__sed} -i -e 's,${sysconfdir}/udev/rules.d,/lib/udev/rules.d,' src/Makefile.am

%build
%{__aclocal}
%{__autoconf}
%{__automake}
%configure
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
%{__make} install \
	doc_DATA= \
	DESTDIR=$RPM_BUILD_ROOT

%{__rm} -f $RPM_BUILD_ROOT%{_infodir}/dir

# empty file
%{__rm} $RPM_BUILD_ROOT%{_mandir}/man1/ift-extract.1

%find_lang %{name}

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

%files -f %{name}.lang
%defattr(644,root,root,755)
%doc README HOWTO AUTHORS
%attr(755,root,root) %{_bindir}/ift-export
%attr(755,root,root) %{_bindir}/ift-extract
%attr(755,root,root) /lib/udev/ift-load
/lib/udev/rules.d/isight.rules
%{_mandir}/man1/ift-export.1*
#%{_mandir}/man1/ift-extract.1*
%{_infodir}/ift-export.info*
%{_infodir}/ift-extract.info*
