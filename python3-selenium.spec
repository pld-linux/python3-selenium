%define		module	selenium
Summary:	Python bindings for Selenium
Summary(pl.UTF-8):	Wiązania Pythona do Selenium
Name:		python3-%{module}
Version:	4.39.0
Release:	1
License:	Apache v2.0
Group:		Development/Languages/Python
#Source0Download: https://pypi.org/simple/selenium/
Source0:	https://files.pythonhosted.org/packages/source/s/selenium/%{module}-%{version}.tar.gz
# Source0-md5:	334b7d61d8bc8c8937a001fb2f503674
# cargo vendor-filterer --platform='*-unknown-linux-*' --tier=2
Source1:	selenium-%{version}-vendor.tar.xz
# Source1-md5:	c537a42e1cb8981e9d40209a3e0937c3
URL:		https://pypi.org/project/selenium/
BuildRequires:	python3-modules >= 1:3.10
BuildRequires:	python3-setuptools
BuildRequires:	python3-setuptools_rust
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 2.050
BuildRequires:	rust
%{?rust_req}
Requires:	python3-modules >= 1:3.10
%ifarch %{x8664}
Suggests:	chromedriver
%endif
%ifarch %{ix86} %{x8664}
Suggests:	firefox-geckodriver
%endif
ExclusiveArch:	%{rust_arches}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Python language bindings for Selenium WebDriver.

The selenium package is used to automate web browser interaction from
Python.

%description -l pl.UTF-8
Wiązania Pythona do sterownika Selenium WebDriver.

Pakiet selenium służy automatyzacji interakcji z przeglądarką WWW z
poziomu Pythona.

%prep
%setup -q -n %{module}-%{version} -a1

# use our offline registry
export CARGO_HOME="$(pwd)/.cargo"

mkdir -p "$CARGO_HOME"
cat >.cargo/config.toml <<EOF
[source.crates-io]
replace-with = 'vendored-sources'

[source.vendored-sources]
directory = '$PWD/vendor'
EOF

%build
export CARGO_HOME="$(pwd)"
export CARGO_OFFLINE=true
export CARGO_TERM_VERBOSE=true
%ifarch x32
export CARGO_BUILD_TARGET=x86_64-unknown-linux-gnux32
export PKG_CONFIG_ALLOW_CROSS=1
export PYO3_CROSS_LIB_DIR=%{_libdir}
%endif

%py3_build_pyproject

%install
rm -rf $RPM_BUILD_ROOT

export CARGO_HOME="$(pwd)"
export CARGO_OFFLINE=true
export CARGO_TERM_VERBOSE=true
%ifarch x32
export CARGO_BUILD_TARGET=x86_64-unknown-linux-gnux32
export PKG_CONFIG_ALLOW_CROSS=1
%endif

%py3_install_pyproject

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc CHANGES README.rst
%dir %{py3_sitedir}/selenium
%{py3_sitedir}/selenium/*.py
%{py3_sitedir}/selenium/py.typed
%{py3_sitedir}/selenium/__pycache__
%{py3_sitedir}/selenium/common
%dir %{py3_sitedir}/selenium/webdriver
%{py3_sitedir}/selenium/webdriver/*.py
%{py3_sitedir}/selenium/webdriver/__pycache__
%{py3_sitedir}/selenium/webdriver/chrome
%{py3_sitedir}/selenium/webdriver/chromium
%dir %{py3_sitedir}/selenium/webdriver/common
%attr(755,root,root) %{py3_sitedir}/selenium/webdriver/common/selenium-manager
%{py3_sitedir}/selenium/webdriver/common/*.js
%{py3_sitedir}/selenium/webdriver/common/*.py
%{py3_sitedir}/selenium/webdriver/common/__pycache__
%{py3_sitedir}/selenium/webdriver/common/actions
%{py3_sitedir}/selenium/webdriver/common/bidi
%{py3_sitedir}/selenium/webdriver/common/devtools
%{py3_sitedir}/selenium/webdriver/common/fedcm
%{py3_sitedir}/selenium/webdriver/edge
%{py3_sitedir}/selenium/webdriver/firefox
%{py3_sitedir}/selenium/webdriver/ie
%{py3_sitedir}/selenium/webdriver/remote
%{py3_sitedir}/selenium/webdriver/safari
%{py3_sitedir}/selenium/webdriver/support
%{py3_sitedir}/selenium/webdriver/webkitgtk
%{py3_sitedir}/selenium/webdriver/wpewebkit
%{py3_sitedir}/selenium-%{version}.dist-info
