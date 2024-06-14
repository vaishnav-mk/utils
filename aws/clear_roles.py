import os
import sys
import json
from concurrent.futures import ThreadPoolExecutor


def get_roles(prefix):
    print("fetching roles...")
    result = os.popen("aws iam list-roles").read()
    response = json.loads(result)
    roles = response["Roles"]

    while "Marker" in response:
        print("fetching more roles...")
        result = os.popen(f"aws iam list-roles --marker {response['Marker']}").read()
        response = json.loads(result)
        roles.extend(response["Roles"])

    filtered = [role for role in roles if role["RoleName"].startswith(prefix or "")]
    print(f"total roles: {len(roles)}")
    print(f"roles matching '{prefix}': {len(filtered)}")
    return filtered


def delete(name):
    print(f"deleting role: {name}")

    result = os.popen(f"aws iam list-attached-role-policies --role-name {name}").read()
    a_policies = json.loads(result)
    for policy in a_policies["AttachedPolicies"]:
        print(f"detaching policy {policy['PolicyArn']} from role {name}")
        os.system(
            f"aws iam detach-role-policy --role-name {name} --policy-arn {policy['PolicyArn']}"
        )

    result = os.popen(f"aws iam list-role-policies --role-name {name}").read()
    i_policies = json.loads(result)
    for policy_name in i_policies["PolicyNames"]:
        print(f"deleting inline policy {policy_name} from role {name}")
        os.system(
            f"aws iam delete-role-policy --role-name {name} --policy-name {policy_name}"
        )

    result = os.popen(
        f"aws iam list-instance-profiles-for-role --role-name {name}"
    ).read()
    profiles = json.loads(result)
    for profile in profiles["InstanceProfiles"]:
        print(
            f"removing role {name} from instance profile {profile['InstanceProfileName']}"
        )
        os.system(
            f"aws iam remove-role-from-instance-profile --instance-profile-name {profile['InstanceProfileName']} --role-name {name}"
        )

    os.system(f"aws iam delete-role --role-name {name}")
    print(f"role {name} deleted")


def delete_all(prefix, max_workers):
    roles = get_roles(prefix)
    total = len(roles)

    if total == 0:
        print("no roles to delete")
        return
    print(f"deleting {total} roles...")

    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        for count, role in enumerate(roles, start=1):
            name = role["RoleName"]
            executor.submit(delete, name)
            print(f"queued role {count}/{total} for deletion: {name}")

    print(f"{':' * 10} all {total} roles deleted {':' * 10}")


if __name__ == "__main__":
    threads = 10
    prefix = None

    for i in range(1, len(sys.argv)):
        if sys.argv[i] == "--threads":
            threads = int(sys.argv[i + 1])
        elif sys.argv[i] == "--role-name":
            prefix = sys.argv[i + 1]

    delete_all(prefix, threads)
