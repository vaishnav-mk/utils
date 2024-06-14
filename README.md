# utils

This repository contains various utility scripts for different tasks. The aim is to provide a collection of scripts that can be used to automate repetitive tasks without any external dependencies.

## Table of Contents

- [Graph](#graph)
  - [Bar Graph](#bar-graph)
- [AWS](#aws)
  - [Clear Roles](#clear-roles)
  - [Clear Queues](#clear-queues)
  - [Clear State Machines](#clear-state-machines)
- [Azure](#azure)


## Graph

### Bar Graph

A script to generate a bar chart from data stored in a JSON file.

![chart](https://github.com/vaishnav-mk/utils/assets/84540554/663ecae1-2383-41f2-bc97-22b892293b2f)

* `--path`: Path to the JSON file containing data. (Default: `data.json`)
* `--filename`: Name of the output file. (Default: `chart.png`)
* `--title`: Title of the chart. (Default: `Chart`)
* `--xlabel`: Label for the x-axis. (Default: `entries`)
* `--ylabel`: Label for the y-axis. (Default: `vals (Seconds)`)

**Commands:**
```bash
cd graph/bar
python main.py [--path {path to JSON file}] [--filename {name of the output file}] [--title {title of the chart}] [--xlabel {label for x-axis}] [--ylabel {label for y-axis}]
```

**Files:**
- `main.py`: Python script to generate the bar chart.
- `data.json`: JSON file containing data for the chart.
- `chart.png`: Generated chart image.

## AWS

### Clear Roles

A script to delete AWS IAM roles.

* `--threads`: Number of threads to use for deletion. (Default: 10)
* `--role-name`: Prefix of the roles to delete. (Default: None) (delete all roles if not provided)

**Commands:**
```bash
cd aws
python clear_roles.py [--threads {number}] [--role-name {prefix}]
```

**Example:**
```bash
python clear_roles.py --role-name "XFaaS" # Delete roles with prefix "XFaaS"
```

### Clear Queues

A script to clear AWS SQS queues.

* `--threads`: Number of threads to use for deletion. (Default: 10)
* `--all`: Delete all queues. (Default: True)
* `--prefix`: Prefix of the queues to delete. (Default: None)
* `--list`: Comma-separated list of queue URLs to delete. (Default: None)

**Commands:**
```bash
cd aws
python clear_queues.py [--threads {number}] [--all | --prefix {prefix} | --list {comma-separated-queue-names}]
```

**Example:**
```bash
python clear_queues.py --prefix "ab" # Delete queues with prefix "ab"
```

### Clear State Machines

A script to delete AWS Step Functions state machines.

* `--threads`: Number of threads to use for deletion. (Default: 10)
* `--all`: Delete all state machines. (Default: True)
* `--prefix`: Prefix of the state machines to delete. (Default: None) (delete all state machines if not provided)

**Commands:**
```bash
cd aws
python clear_statemachines.py [--threads {number}] [--all | --prefix {prefix}]
```

**Example:**
```bash
python clear_statemachines.py --prefix "ab" # Delete state machines with prefix "ab"
```

## Azure

No scripts available currently under Azure. (Work in progress)
