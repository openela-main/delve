Name:                   delve
Version:                1.9.1
Release:                1%{?dist}
Summary:                A debugger for the Go programming language

License:                MIT
URL:                    https://github.com/go-delve/delve
Source0:                https://github.com/go-delve/delve/archive/v%{version}.tar.gz#/%{name}-%{version}.tar.gz

ExcludeArch:            ppc64le s390x aarch64 %{ix86} armv7hl

BuildRequires:          compiler(go-compiler)
BuildRequires:          git
BuildRequires:          lsof

Provides:               dlv = %{version}


%description
Delve is a debugger for the Go programming language. The goal of the project 
is to provide a simple, full featured debugging tool for Go. Delve should be 
easy to invoke and easy to use. Chances are if you're using a debugger, things 
aren't going your way. With that in mind, Delve should stay out of your way as 
much as possible.


%prep
%setup -q

rm -rf go.mod
mv vendor %{_builddir}/src
mkdir -p "%{_builddir}/src/github.com/go-delve/"
cp -r %{_builddir}/%{name}-%{version} %{_builddir}/src/github.com/go-delve/%{name}
mkdir -p %{_builddir}/%{name}-%{version}/_build
mv %{_builddir}/src %{_builddir}/%{name}-%{version}/_build/src


%build
export GO111MODULE=off
export GOPATH="%{_builddir}/%{name}-%{version}/_build"
%gobuild -o bin/dlv github.com/go-delve/delve/cmd/dlv


%install
export GO111MODULE=off
export GOPATH="%{_builddir}/%{name}-%{version}/_build"
install -Dpm 0755 bin/dlv %{buildroot}%{_bindir}/dlv


%check
export GO111MODULE=off
export GOPATH="%{_builddir}/%{name}-%{version}/_build"
cd "_build/src/github.com/go-delve/%{name}"
for d in $(go list ./... | grep -v cmd | grep -v scripts); do
    go test ${d}
done


%files
%license LICENSE
%doc CONTRIBUTING.md CHANGELOG.md
%doc Documentation/*
%{_bindir}/dlv


%changelog
* Fri Sep 30 2022 Alejandro Sáez <asm@redhat.com> - 1.9.1-1
- Rebase to 1.9.1
- Related: rhbz#2131026

* Wed Apr 27 2022 Alejandro Sáez <asm@redhat.com> - 1.8.3-1
- Rebase to 1.8.3
- Resolves: rhbz#2077956
- Resolves: rhbz#2076501

* Thu Oct 14 2021 Alejandro Sáez <asm@redhat.com> - 1.7.2-1
- Rebase to 1.7.2
- Related: rhbz#2014088

* Wed Mar 17 2021 Alejandro Sáez <asm@redhat.com> - 1.6.0-1
- Rebase to 1.6.0
- Resolves: rhbz#1938071
- Removes golang-1.15.4-TestStepIntoWrapperForEmbeddedPointer.patch

* Tue Nov 24 2020 David Benoit <dbenoit@redhat.com> - 1.5.0-2
- Add golang-1.15.4 related patch
- Resolves: rhbz#1901189

* Wed Sep 09 2020 Alejandro Sáez <asm@redhat.com> - 1.5.0-1
- Rebase to 1.5.0
- Related: rhbz#1870531

* Mon May 25 2020 Alejandro Sáez <asm@redhat.com> - 1.4.1-1
- Rebase to 1.4.1
- Resolves: rhbz#1821281
- Related: rhbz#1820596

* Fri May 22 2020 Alejandro Sáez <asm@redhat.com> - 1.4.0-2
- Change i686 to a better macro
- Related: rhbz#1820596

* Tue Apr 28 2020 Alejandro Sáez <asm@redhat.com> - 1.4.0-1
- Rebase to 1.4.0
- Remove Patch1781
- Related: rhbz#1820596

* Thu Jan 16 2020 Alejandro Sáez <asm@redhat.com> - 1.3.2-3
- Resolves: rhbz#1758612
- Resolves: rhbz#1780554
- Add patch: 1781-pkg-terminal-Fix-exit-status.patch

* Wed Jan 15 2020 Alejandro Sáez <asm@redhat.com> - 1.3.2-2
- Added tests
- Related: rhbz#1758612

* Wed Nov 27 2019 Alejandro Sáez <asm@redhat.com> - 1.3.2-1
- First package for RHEL
- Related: rhbz#1758612
