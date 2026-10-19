# Exercise 5 - Docker Security with AppArmor and Python

Build a Flask image, apply a restrictive AppArmor profile, and verify that the container cannot read `/etc/passwd` or execute `/bin/bash`.

This exercise requires a **Linux Docker host with AppArmor enabled**. Docker Desktop on Windows does not provide a host AppArmor profile parser.

## Run

Check that AppArmor is enabled before continuing:

```bash
sudo aa-status
```

From this directory on the supported Linux host:

```bash
sudo cp my-apparmor-profile /etc/apparmor.d/my-apparmor-profile
sudo apparmor_parser -r /etc/apparmor.d/my-apparmor-profile
python3 -m pip install -r requirements.txt
python3 apply_apparmor.py
python3 test_restricted_actions.py
```

The SDK script builds the image, runs the container with the profile, verifies Docker's security options, and removes the container. The restriction test expects reading `/etc/passwd` and executing the installed `/bin/bash` to be denied; it fails if either action is allowed. No credentials are stored in the repository.
