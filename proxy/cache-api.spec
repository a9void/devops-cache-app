Name:           cache-api
Version:        1.0.0
Release:        1
Summary:        Flask caching proxy for Backend API
License:        LicenseRef-Local
BuildArch:      noarch

Source0:        cache-api.py
Source1:        config.yaml
Source2:        cache-api.service

Requires:       python3
Requires:       python3-flask
Requires:       python3-redis
Requires:       python3-requests
Requires:       python3-pyyaml
Requires:       systemd

%description
Flask proxy that caches Backend API responses in Redis.

%prep

%build

%install
install -D -m 0644 %{SOURCE0} %{buildroot}/usr/libexec/cache-api/cache-api.py
install -D -m 0644 %{SOURCE1} %{buildroot}/etc/cache-api/config.yaml
install -D -m 0644 %{SOURCE2} %{buildroot}/usr/lib/systemd/system/cache-api.service

%files
%dir /usr/libexec/cache-api
/usr/libexec/cache-api/cache-api.py

%dir /etc/cache-api
%config(noreplace) /etc/cache-api/config.yaml

/usr/lib/systemd/system/cache-api.service
