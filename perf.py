import argparse
import requests
import time
import numpy as np

default_output_file = "measures.csv"
default_api_url = "http://localhost:9086/api/chats/messages"
default_runs = 101
default_exp = 101
default_interval = 0


class PerfStats:

    def __init__(self, index, measures):
        self.samples = 1.0 * np.array(measures)
        self.mean = np.mean(self.samples)
        self.std = np.std(self.samples)
        self.ci = 1.96 * (self.std / np.sqrt(len(self.samples)))
        self.index = index

    def __str__(self):
        return f"{self.index},{self.mean},{self.std},{self.ci}"


class Stopwatch:

    def __init__(self):
        self.start_time = time.time()
        self.end_time = 0.0
        self.elapsed_time = 0.0

    def stop(self):
        self.end_time = time.time()
        self.elapsed_time = self.end_time - self.start_time

    def __str__(self):
        return f"{self.start_time},{self.end_time},{self.elapsed_time}"


def call_api(api_url):
    stopwatch = Stopwatch()

    response = requests.post(
        api_url,
        json={
            "senderEmail": "user2@email.com",
            "recipientEmail": "user1@email.com",
            "message": "hey, how are you?"
        }
    )

    stopwatch.stop()

    if 299 < response.status_code < 200:
        print(f"[-][-] call failed : {response}")
        exit(1)

    return stopwatch.elapsed_time


def run_experiments(api_url, runs, exp, simple):
    stats = []

    for e in range(exp):
        measures = []
        for i in range(runs):
            print(f"running experiment {e} [run {i} of {runs}]...")
            measures.append(call_api(api_url))
            time.sleep(default_interval)
        if simple:
            return measures[1:]

        stats.append(PerfStats(e, measures[1:]))

    return stats


def save_stats(filename, measures, simple):
    print(f"writing stats in file: {filename}")

    with open(filename, 'w') as file:
        file.write("i,mean,std,ci\n")

        for index, m in enumerate(measures):
            if simple:
                file.write(f"{index},{m}\n")
            else:
                file.write(f"{m}\n")

    print("finished writing file")


def save_measures(filename, measures):
    print(f"writing measures in file: {filename}")

    with open(filename, 'w') as file:
        file.write("start_time,end_time,elapsed_time\n")

        for m in measures:
            file.write(f"{m}\n")

    print("finished writing file")


def main():
    parser = argparse.ArgumentParser(description='Run Experiments')

    parser.add_argument(
        '--url',
        help='target url',
        default=default_api_url
    )

    parser.add_argument(
        '--exp',
        help='how many experiments should run',
        default=default_exp
    )

    parser.add_argument(
        '--runs',
        help='how many measurements should be done by experiment',
        default=default_runs
    )

    parser.add_argument(
        '--output',
        help='output file path',
        default=default_output_file
    )

    parser.add_argument(
        '--simple',
        help='simple experiment',
        default=False
    )

    url_arg = parser.parse_args().url
    output_file = parser.parse_args().output
    runs = parser.parse_args().runs
    exp = parser.parse_args().exp
    simple = bool(parser.parse_args().simple)

    try:
        measures = run_experiments(url_arg, runs, exp, simple)
        save_stats(output_file, measures, simple)

        print("Process completed")
    except Exception as e:
        print(e)


if __name__ == '__main__':
    main()
