import os
import sys
import json
from concurrent.futures import ThreadPoolExecutor


def get_queues():
    print("fetching queues...")
    result = os.popen("aws sqs list-queues").read()
    if not result:
        print("no queues found")
        return []
    response = json.loads(result)
    queues = response.get("QueueUrls", [])
    print(
        f"total queues: {len(queues)} [first 5]: {[queue.split('/')[-1] for queue in queues[:5]]}"
    )
    return queues


def clear_queue(queue_url):
    print(f"clearing queue: {queue_url}")
    os.system(f"aws sqs delete-queue --queue-url {queue_url}")
    print(f"queue {queue_url} cleared")


def clear_queues(queue_urls, max_workers):
    total = len(queue_urls)
    print(f"starting clearing of {total} queues...")

    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        for count, queue_url in enumerate(queue_urls, start=1):
            executor.submit(clear_queue, queue_url)
            print(f"queued queue {count}/{total} for clearing: {queue_url}")

    print(f"{':' * 10} all {total} queues deleted {':' * 10}")


if __name__ == "__main__":
    threads = 10
    mode = "all"
    prefix = None
    queue_list = []

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
            queue_list = sys.argv[i + 1].split(",")

    if mode == "all":
        queues = get_queues()
    elif mode == "prefix":
        all_queues = get_queues()
        queues = [
            queue for queue in all_queues if queue.split("/")[-1].startswith(prefix)
        ]
        print(f"queues matching '{prefix}': {len(queues)}")
    elif mode == "list":
        all_queues = get_queues()
        queues = [queue for queue in all_queues if queue.split("/")[-1] in queue_list]

    clear_queues(queues, threads)
