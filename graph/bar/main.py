import matplotlib.pyplot as plt
import numpy as np
import sys


def plot(data_path="data.json", name="chart.png", **kwargs):
    xlabel = kwargs.get("xlabel", "entries")
    ylabel = kwargs.get("ylabel", "vals (Seconds)")
    title = kwargs.get("title")

    data = []

    try:
        with open(data_path, "r") as f:
            data = eval(f.read())
    except FileNotFoundError:
        print("File not found")
        return

    keys = list(data[0].keys())
    entries = len(data)
    totalk = len(keys)

    width = 0.8 / totalk
    x = np.arange(entries)

    fig, ax = plt.subplots()

    for i, key in enumerate(keys):
        values = [entry[key] for entry in data]
        ax.bar(x + i * width, values, width, label=key)

    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    if title:
        ax.set_title(title)
    ax.set_xticks(x + width * (totalk - 1) / 2)
    ax.set_xticklabels([f"{i+1}" for i in range(entries)])
    ax.legend()

    plt.savefig(name)
    print(f"saved - {name}")


args = sys.argv[1:]
path = args[args.index("--path") + 1] if "--path" in args else "data.json"
filename = args[args.index("--filename") + 1] if "--filename" in args else "chart.png"
xlabel = args[args.index("--xlabel") + 1] if "--xlabel" in args else "entries"
ylabel = args[args.index("--ylabel") + 1] if "--ylabel" in args else "vals (Seconds)"
title = args[args.index("--title") + 1] if "--title" in args else None

plot(path, filename, xlabel=xlabel, ylabel=ylabel, title=title)
