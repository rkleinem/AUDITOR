Name:           auditor-slurm-collector
Version:        %{version_}
Release:        1%{?dist}
Summary:        Slurm collector for AUDITOR
BuildArch:      x86_64

License:        MIT or Apache-2.0

%description
Slurm collector for Auditor

%global confdir %{_sysconfdir}/auditor
%global statedir %{_localstatedir}/lib/%{name}
%global unitdir /usr/lib/systemd/system
%global user %{name}

%pre
# On install
if [ "$1" -eq 1 ]; then
    getent group %{user} || groupadd --system %{user}
    getent passwd %{user} || useradd --system --no-create-home --gid %{user} --shell /sbin/nologin %{user}
fi

%post
# On install
if [ "$1" -eq 1 ]; then
    systemctl --no-reload preset %{name}
fi

%preun
# On uninstall
if [ "$1" -eq 0 ]; then
    systemctl --no-reload disable --now --no-warn %{name}
fi

%postun
# On update
if [ "$1" -ge 1 ]; then
    systemctl set-property %{name} Markers=+needs-restart
fi
# On uninstall
if [ "$1" -eq 0 ]; then
    # Clean up /etc/auditor (there might stuff not belonging to this package)
    rmdir %{confdir} || true
    # Only remove our own files
    runuser -u %{user} -- rm -rf %{statedir}/*
    rmdir %{statedir} || echo "There are leftover files under %{statedir}!"
    USERGROUPS_ENAB=yes userdel %{user}
fi

%install
install -d -D -m 0750 $RPM_BUILD_ROOT/%{statedir}
install -p -D -m 0755 -t $RPM_BUILD_ROOT/%{_bindir} %{name} 
install -p -D -m 0644 -t $RPM_BUILD_ROOT/%{confdir} %{name}.yaml
install -p -D -m 0644 -t $RPM_BUILD_ROOT/%{unitdir} %{name}.service
pwd
ls

%clean
rm -rf $RPM_BUILD_ROOT

%files
%dir %attr(0750,%{user},%{user}) %{statedir}
%{_bindir}/%{name}
%config(noreplace) %{confdir}/%{name}.yaml
%{unitdir}/%{name}.service

%changelog
* Wed May 14 2025 Dirk Sammel <dirk.sammel@physik.uni-freiburg.de> - 0.9.3
  - Release v0.9.3 - see https://github.com/ALU-Schumacher/AUDITOR/blob/main/CHANGELOG.md for changes
* Thu Apr 10 2025 Raghuvar Vijayakumar <raghuvar.vijayakumar@physik.uni-freiburg.de> - 0.9.2
  - Release v0.9.2 - see https://github.com/ALU-Schumacher/AUDITOR/blob/main/CHANGELOG.md for changes
* Mon Mar 31 2025 Raghuvar Vijayakumar <raghuvar.vijayakumar@physik.uni-freiburg.de> - 0.9.1
  - Release v0.9.1 - see https://github.com/ALU-Schumacher/AUDITOR/blob/main/CHANGELOG.md for changes
* Thu Mar 27 2025 Raghuvar Vijayakumar <raghuvar.vijayakumar@physik.uni-freiburg.de> - 0.9.0
  - Release v0.9.0 - see https://github.com/ALU-Schumacher/AUDITOR/blob/main/CHANGELOG.md for changes
* Mon Mar 03 2025 Dirk Sammel <dirk.sammel@physik.uni-freiburg.de> - 0.8.0
  - Release v0.8.0 - see https://github.com/ALU-Schumacher/AUDITOR/blob/main/CHANGELOG.md for changes
* Thu Feb 27 2025 Raghuvar Vijayakumar <raghuvar.vijayakumar@physik.uni-freiburg.de> - 0.7.1
  - Release v0.7.1 - see https://github.com/ALU-Schumacher/AUDITOR/blob/main/CHANGELOG.md for changes
* Mon Jan 27 2025 Dirk Sammel <dirk.sammel@physik.uni-freiburg.de> - 0.7.0
  - Release v0.7.0 - see https://github.com/ALU-Schumacher/AUDITOR/blob/main/CHANGELOG.md for changes
* Wed Oct 30 2024 Dirk Sammel <dirk.sammel@physik.uni-freiburg.de> - 0.6.3
  - Release v0.6.3 - see https://github.com/ALU-Schumacher/AUDITOR/blob/main/CHANGELOG.md for changes
* Mon Jul 29 2024 Raghuvar Vijayakumar <raghuvar.vijayakumar@physik.uni-freiburg.de> - 0.6.2
  - Release v0.6.2 - see https://github.com/ALU-Schumacher/AUDITOR/blob/main/CHANGELOG.md for changes
* Tue Apr 23 2024 Dirk Sammel <dirk.sammel@physik.uni-freiburg.de> - 0.5.0
  - Release v0.5.0 - see https://github.com/ALU-Schumacher/AUDITOR/blob/main/CHANGELOG.md for changes
* Wed Jan 31 2024 Raghuvar Vijayakumar <raghuvar.vijayakumar@physik.uni-freiburg.de> - 0.4.0
  - Release v0.4.0 - see https://github.com/ALU-Schumacher/AUDITOR/blob/main/CHANGELOG.md for changes
* Fri Nov 24 2023 Benjamin Rottler <benjamin.rottler@physik.uni-freiburg.de> - 0.3.1
  - Release v0.3.1 - see https://github.com/ALU-Schumacher/AUDITOR/blob/main/CHANGELOG.md for changes
* Fri Nov 17 2023 Benjamin Rottler <benjamin.rottler@physik.uni-freiburg.de> - 0.3.0
  - Release v0.3.0 - see https://github.com/ALU-Schumacher/AUDITOR/blob/main/CHANGELOG.md for changes
* Thu Sep 21 2023 Benjamin Rottler <benjamin.rottler@physik.uni-freiburg.de> - 0.2.0
  - Release v0.2.0 - see https://github.com/ALU-Schumacher/AUDITOR/blob/main/CHANGELOG.md for changes
* Wed Dec 01 2022 Stefan Kroboth <stefan.kroboth@gmail.com> - 0.1.0
  - First version in a package
