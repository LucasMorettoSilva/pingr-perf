# pingr-perf

Scripts to measure the performance of Pingr operations.

## perf.py

This script is used to run experiments in the Pingr system. It tries to connect
to the chat microservice to send a message between two users.

```txt
usage: perf.py [-h] [--url URL] [--runs RUNS] [--output OUTPUT]

Run Experiments in the Chat Microservice

options:
  -h, --help       show this help message and exit
  --url URL        target message API url
  --runs RUNS      how many experiments should run
  --output OUTPUT  output file path

```

## merge.py

This script is used to merge the result files from the previous script into a single
.csv file. You can run it by doing:

```shell
python merge.py results/async-measures-single-vm.csv results/async-measures-diff-vm.csv results/sync-measures-single-vm.csv results/sync-measures-diff-vm.csv
```

## plot.py

This script can be used to plot a graph from the results files from the previous scripts.
You can run it by doing:

```shell
python plot.py
```
