import docker

PROFILE = "my-apparmor-profile"
IMAGE = "flask-apparmor"

client = docker.from_env()
container = client.containers.run(
    IMAGE,
    detach=True,
    security_opt=[f"apparmor={PROFILE}"],
)

try:
    read_passwd = container.exec_run(
        [
            "python",
            "-c",
            "from pathlib import Path; "
            "exec(\"try:\\n Path('/etc/passwd').read_text()\\n"
            "except PermissionError:\\n print('DENIED')\\n"
            "else:\\n raise SystemExit(1)\")",
        ]
    )
    if read_passwd.exit_code != 0 or b"DENIED" not in read_passwd.output:
        raise RuntimeError(
            f"Expected /etc/passwd access to be denied: {read_passwd.output!r}"
        )
    print("Read /etc/passwd: denied")

    try:
        execute_bash = container.exec_run(["/bin/bash", "-c", "true"])
    except docker.errors.APIError as error:
        message = str(error).lower()
        if "permission denied" not in message and "operation not permitted" not in message:
            raise
        print("Execute /bin/bash: denied by AppArmor")
    else:
        if execute_bash.exit_code == 0:
            raise RuntimeError("AppArmor unexpectedly allowed /bin/bash to execute")
        print(f"Execute /bin/bash: denied (exit {execute_bash.exit_code})")
finally:
    container.remove(force=True)
