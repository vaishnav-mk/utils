import os
import sys
import json
from concurrent.futures import ThreadPoolExecutor


def get_all_accounts(resource_group):
    print(f"fetching all storage accounts in resource group: {resource_group}")
    result = os.popen(
        f"az storage account list --resource-group {resource_group} --query '[].name' --output json"
    ).read()
    if not result:
        print("no storage accounts found")
        return []
    storage_accounts = json.loads(result)
    print(f"total storage accounts: {len(storage_accounts)}")
    return storage_accounts


def delete_sa(resource_group, storage_account_name):
    print(f"deleting storage account: {storage_account_name}")
    os.system(
        f"az storage account delete --name {storage_account_name} --resource-group {resource_group} --yes"
    )
    print(f"storage account {storage_account_name} deleted")


def delete_sas(resource_group, storage_accounts, max_workers):
    total = len(storage_accounts)
    print(f"starting deletion of {total} storage accounts...")

    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        for count, storage_account_name in enumerate(storage_accounts, start=1):
            executor.submit(
                delete_sa, resource_group, storage_account_name
            )
            print(
                f"queued storage account {count}/{total} for deletion: {storage_account_name}"
            )

    print(f"{':' * 10} all {total} sas deleted {':' * 10}")


if __name__ == "__main__":
    threads = 10
    resource_group = None

    for i in range(1, len(sys.argv)):
        if sys.argv[i] == "--threads":
            threads = int(sys.argv[i + 1])
        elif sys.argv[i] == "--resource-group":
            resource_group = sys.argv[i + 1]

    if resource_group is None:
        print("Error: --resource-group argument is required")
        sys.exit(1)

    storage_accounts = get_all_accounts(resource_group)
    if len(storage_accounts) == 0:
        print("no storage accounts to delete")
        sys.exit(0)
    delete_sas(resource_group, storage_accounts, threads)
