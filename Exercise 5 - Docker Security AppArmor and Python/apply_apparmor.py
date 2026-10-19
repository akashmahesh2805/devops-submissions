import docker

PROFILE = "my-apparmor-profile"
IMAGE = "flask-apparmor"

client = docker.from_env()
client.images.build(path=".", tag=IMAGE)

container = client.containers.run(
    IMAGE,
    detach=True,
    ports={"5000/tcp": 5000},
    security_opt=[f"apparmor={PROFILE}"],
)

try:
    security_options = client.api.inspect_container(container.id)["HostConfig"][
        "SecurityOpt"
    ]
    if f"apparmor={PROFILE}" not in security_options:
        raise RuntimeError(f"AppArmor profile was not applied: {security_options}")
    print(f"AppArmor profile applied: {security_options}")
finally:
    container.remove(force=True)
