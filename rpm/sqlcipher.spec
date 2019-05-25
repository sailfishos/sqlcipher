Summary: AES encryption for SQLite databases
Name: sqlcipher
Version: 3.4.1
Release: 1
License: BSD
Group: Applications/Databases
URL: http://sqlcipher.net/
Source0: %{name}-%{version}.tar.xz
BuildRequires: glibc-devel
BuildRequires: autoconf
BuildRequires: openssl-devel
BuildRequires: tcl-devel

%description
 SQLCipher is a C library that implements an encryption in the SQLite 3
 database engine.  Programs that link with the SQLCipher library can have SQL
 database access without running a separate RDBMS process.  It allows one to
 have per-database or page-by-page encryption using AES-256 from Open

 SQLCipher has a small footprint and great performance so it’s ideal for
 protecting embedded application databases and is well suited for mobile
 development.

  * as little as 5-15% overhead for encryption
  * 100% of data in the database file is encrypted
  * Uses good security practices (CBC mode, key derivation)
  * Zero-configuration and application level cryptography
  * Algorithms provided by the peer reviewed OpenSSL crypto library.

 SQLCipher has broad platform support for with C/C++, Obj-C, QT, Win32/.NET,
 Java, Python, Ruby, Linux, Mac OS X, iPhone/iOS, Android, Xamarin.iOS, and
 Xamarin.Android.

 SQLCipher v2.1.1 is based on SQLite3 v3.7.17.

%package devel
Summary: Development tools for the sqlite3 embeddable SQL database engine
Group: Development/Libraries
Requires: %{name} = %{version}-%{release}
Requires: pkgconfig

%description devel
This package contains the header files and development documentation
for %{name}. If you like to develop programs using %{name}, you will need
to install %{name}-devel.

%prep
%setup -q -n %{name}-%{version}/%{name}

%build
autoreconf -vfi
%configure                      \
    --disable-readline          \
    --disable-tcl               \
    --enable-tempstore=yes      \
    CFLAGS="-DSQLITE_HAS_CODEC" \
    LDFLAGS="-lcrypto"
make %{?_smp_mflags}

%install
rm -rf %{buildroot}
make DESTDIR=%{buildroot} install
install -D -m0644 sqlcipher.1 %{buildroot}/%{_mandir}/man1/sqlcipher.1

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%defattr(-, root, root)
%license LICENSE
%doc README.md
%{_bindir}/sqlcipher
%{_libdir}/*.so.*
%{_mandir}/man?/*

%files devel
%defattr(-, root, root)
%{_includedir}/sqlcipher/*.h
%{_libdir}/*.so
%{_libdir}/pkgconfig/*.pc
%exclude %{_libdir}/*.a
%exclude %{_libdir}/*.la

