Summary: AES encryption for SQLite databases
Name: sqlcipher
Version: 4.18.0
Release: 1
License: BSD
URL: https://github.com/sailfishos/sqlcipher
Source0: %{name}-%{version}.tar.xz
BuildRequires: glibc-devel
BuildRequires: autoconf
BuildRequires: openssl-devel
BuildRequires: tcl-devel
BuildRequires: pkgconfig(icu-i18n)

%define        sover 0

# SQLCipher uses a custom configure tooling which doesn't accept "--target=..."
%global configure_no_target %(rpm --eval '%%configure' | sed 's/--target=[^ ]*//')

%description
 SQLCipher is a C library that implements an encryption in the SQLite 3
 database engine.  Programs that link with the SQLCipher library can have SQL
 database access without running a separate RDBMS process.  It allows one to
 have per-database or page-by-page encryption using AES-256.

 SQLCipher has a small footprint and great performance so it’s ideal for
 protecting embedded application databases and is well suited for mobile
 development.

 SQLCipher v4.18.0 is based on SQLite3 v3.53.4.

%package devel
Summary: Development tools for the sqlite3 embeddable SQL database engine
Requires: %{name} = %{version}-%{release}
Requires: pkgconfig

%description devel
This package contains the header files and development documentation
for %{name}. If you like to develop programs using %{name}, you will need
to install %{name}-devel.

%prep
%autosetup -n %{name}-%{version}/%{name}

%build
# Add SQLCipher-related flags and use the original library and binary names.
# Upstream defaults to sqlite3, libsqlite.so etc. for easy drop-in replacement, presumably.
export CFLAGS="$CFLAGS %{optflags} -DSQLITE_HAS_CODEC -DSQLITE_ENABLE_ICU -DSQLITE_EXTRA_INIT=sqlcipher_extra_init -DSQLITE_EXTRA_SHUTDOWN=sqlcipher_extra_shutdown"
export LDFLAGS="$LDFLAGS -lcrypto $(icu-config --ldflags-libsonly) -Wl,-soname,libsqlcipher.so.%{sover}"
export CC=gcc
export CXX=g++
%define _lto_cflags %{nil}

# %%configure includes --target=
%configure_no_target \
    --disable-static \
    --disable-readline \
    --disable-tcl \
    --with-tempstore=yes \
    --dll-basename=libsqlcipher
%make_build

%install
%make_install

mv %{buildroot}%{_bindir}/sqlite3 %{buildroot}%{_bindir}/sqlcipher
mv %{buildroot}%{_mandir}/man1/sqlite3.1 %{buildroot}%{_mandir}/man1/sqlcipher.1
mv %{buildroot}%{_libdir}/pkgconfig/sqlite3.pc %{buildroot}%{_libdir}/pkgconfig/sqlcipher.pc
mkdir -p %{buildroot}%{_includedir}/sqlcipher
mv %{buildroot}%{_includedir}/sqlite3.h %{buildroot}%{_includedir}/sqlcipher/
mv %{buildroot}%{_includedir}/sqlite3ext.h %{buildroot}%{_includedir}/sqlcipher/

sed -i \
  -e 's/-lsqlite3/-lsqlcipher/g' \
  -e 's|^includedir=.*|includedir=%{_includedir}/sqlcipher|' \
  %{buildroot}%{_libdir}/pkgconfig/sqlcipher.pc
find %{buildroot} -type f -name "*.la" -delete -print

install -D -m0644 sqlcipher.1 %{buildroot}/%{_mandir}/man1/sqlcipher.1

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%license LICENSE.md
%doc README.md
%{_bindir}/sqlcipher
%{_libdir}/*.so.*

%files devel
%{_includedir}/sqlcipher/*.h
%{_libdir}/*.so
%{_libdir}/pkgconfig/*.pc
%{_mandir}/man?/*
%exclude %{_libdir}/*.a
%exclude %{_libdir}/*.la
