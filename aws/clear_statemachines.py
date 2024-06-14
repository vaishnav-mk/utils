import os
import sys
import json
from concurrent.futures import ThreadPoolExecutor


def get_sm():
    print("fetching sms...")
    result = os.popen("aws stepfunctions list-state-machines").read()
    response = json.loads(result)
    state_machines = response.get("stateMachines", [])
    print(f"total sm: {len(state_machines)}")
    return state_machines


def delete_sm(state_machine_arn):
    print(f"deleting sm: {state_machine_arn}")
    os.system(
        f"aws stepfunctions delete-state-machine --state-machine-arn {state_machine_arn}"
    )
    print(f"sm {state_machine_arn} deleted")


def delete_sm(state_machine_arns, max_workers):
    total = len(state_machine_arns)
    print(f"starting deletion of {total} sms...")

    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        for count, state_machine_arn in enumerate(state_machine_arns, start=1):
            executor.submit(delete_sm, state_machine_arn)
            print(f"queued sm {count}/{total} for deletion: {state_machine_arn}")

    print(f"{':' * 10} all {total} sms deleted {':' * 10}")


if __name__ == "__main__":
    threads = 10
    mode = "all"
    prefix = None

    for i in range(1, len(sys.argv)):
        if sys.argv[i] == "--threads":
            threads = int(sys.argv[i + 1])
        elif sys.argv[i] == "--all":
            mode = "all"
        elif sys.argv[i] == "--prefix":
            mode = "prefix"
            prefix = sys.argv[i + 1]

    if mode == "all":
        state_machines = get_sm()
        state_machine_arns = [sm["stateMachineArn"] for sm in state_machines]
    elif mode == "prefix":
        all_state_machines = get_sm()
        state_machine_arns = [
            sm["stateMachineArn"]
            for sm in all_state_machines
            if sm["name"].startswith(prefix)
        ]
        if not state_machine_arns:
            print("no sms found with the given prefix")
            sys.exit(0)

    delete_sm(state_machine_arns, threads)
