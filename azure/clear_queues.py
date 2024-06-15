import os
import sys
import json
from concurrent.futures import ThreadPoolExecutor


def get_all_queues(connection_string):
    print("fetching all queues...")
    result = os.popen(
        f"az storage queue list --connection-string '{connection_string}'"
    ).read()
    queues = json.loads(result)
    print(f"total queues: {len(queues)}")
    return [queue["name"] for queue in queues]


def delete_queue(connection_string, queue_name):
    print(f"deleting queue: {queue_name}")
    os.system(
        f"az storage queue delete --name {queue_name} --connection-string '{connection_string}'"
    )
    print(f"queue {queue_name} deleted")


def delete_queues(connection_string, queue_names, max_workers):
    total = len(queue_names)
    if total == 0:
        print("no queues found")
        return
    print(f"starting deletion of {total} queues...")

    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        for count, queue_name in enumerate(queue_names, start=1):
            executor.submit(delete_queue, connection_string, queue_name)
            print(f"Queued queue {count}/{total} for deletion: {queue_name}")

    print(f"{':' * 10} all {total} queues deleted {':' * 10}")


def get_connection_string(storage_account_name, resource_group):
    print(f"fetching connection string for storage account: {storage_account_name}")
    result = os.popen(
        f"az storage account show-connection-string --name {storage_account_name} --resource-group {resource_group} --query connectionString"
    ).read()
    connection_string = json.loads(result)
    connection_string = connection_string.replace("\n", "")

    return connection_string


if __name__ == "__main__":
    threads = 10
    storage_account_name = None
    resource_group = None
    mode = "all"
    prefix = None
    queue_list = []

    for i in range(1, len(sys.argv)):
        if sys.argv[i] == "--threads":
            threads = int(sys.argv[i + 1])
        elif sys.argv[i] == "--storage-account":
            storage_account_name = sys.argv[i + 1]
        elif sys.argv[i] == "--resource-group":
            resource_group = sys.argv[i + 1]
        elif sys.argv[i] == "--all":
            mode = "all"
        elif sys.argv[i] == "--prefix":
            mode = "prefix"
            prefix = sys.argv[i + 1]
        elif sys.argv[i] == "--list":
            mode = "list"
            queue_list = sys.argv[i + 1].split(",")

    if storage_account_name is None or resource_group is None:
        print("Error: --storage-account and --resource-group arguments are required")
        sys.exit(1)

    connection_string = get_connection_string(storage_account_name, resource_group)

    if mode == "all":
        queues = get_all_queues(connection_string)
    elif mode == "prefix":
        all_queues = get_all_queues(connection_string)
        queues = [queue for queue in all_queues if queue.startswith(prefix)]
    elif mode == "list":
        queues = queue_list

    delete_queues(connection_string, queues, threads)
