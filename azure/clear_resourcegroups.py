import os
import sys
import json
from concurrent.futures import ThreadPoolExecutor


def get_all_rg():
    print("fetching all resource groups...")
    result = os.popen("az group list --query '[].name' --output json").read()
    resource_groups = json.loads(result)
    print(f"total resource groups: {len(resource_groups)}")
    return resource_groups


def delete_rg(resource_group_name):
    print(f"deleting resource group: {resource_group_name}")
    os.system(f"az group delete --name {resource_group_name} --yes --no-wait")
    print(f"resource group {resource_group_name} deletion started")


def delete_rgs(resource_groups, max_workers):
    total = len(resource_groups)
    print(f"starting deletion of {total} resource groups...")

    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        for count, resource_group_name in enumerate(resource_groups, start=1):
            executor.submit(delete_rg, resource_group_name)
            print(
                f"queued resource group {count}/{total} for deletion: {resource_group_name}"
            )

    print(f"{':' * 10} all {total} rgs deleted {':' * 10}")


if __name__ == "__main__":
    threads = 10
    mode = "all"
    prefix = None
    group_list = []

    for i in range(1, len(sys.argv)):
        if sys.argv[i] == "--threads":
            threads = int(sys.argv[i + 1])
        elif sys.argv[i] == "--all":
            mode = "all"
        elif sys.argv[i] == "--prefix":
            mode = "prefix"
            prefix = sys.argv[i + 1]
        elif sys.argv[i] == "--list":
            mode = "list"
            group_list = sys.argv[i + 1].split(",")

    if mode == "all":
        resource_groups = get_all_rg()
    elif mode == "prefix":
        all_resource_groups = get_all_rg()
        resource_groups = [
            group for group in all_resource_groups if group.startswith(prefix)
        ]
    elif mode == "list":
        resource_groups = group_list

    delete_rgs(resource_groups, threads)
