import matplotlib.pyplot as plt
import pandas as pd


class MeasureDataFrames:

    def __init__(self):
        folder = "results-2"
        self.df_sync_single_vm = pd.read_csv(f"./{folder}/sync-measures-single-vm.csv")
        self.df_async_single_vm = pd.read_csv(f"./{folder}/async-measures-single-vm.csv")
        self.df_sync_diff_vm = pd.read_csv(f"./{folder}/sync-measures-diff-vm.csv")
        self.df_async_diff_vm = pd.read_csv(f"./{folder}/async-measures-diff-vm.csv")
        self.df_merge = pd.read_csv(f"./{folder}/final-measures.csv")
        self.new_sync = pd.read_csv(f"./{folder}/final-measures.csv")

    def plot(self):
        axes = plt.gca()

        self.plot_sync(axes)
        self.plot_async(axes)

    def box(self):
        self.box_sync()

    def show(self):
        plt.show()

    def box_sync(self):
        self.df_merge.boxplot(
            by='experiment-type',
            column=['elapsed_time'],
            grid=False
        )

    def plot_sync(self, axes=plt.gca()):
        self.df_sync_single_vm.rolling(3, win_type='gaussian').mean(std=1).plot(
            kind='line',
            y='mean',
            label='sync-single-vm',
            ax=axes
        )

        self.df_sync_diff_vm.rolling(3, win_type='gaussian').mean(std=1).plot(
            kind='line',
            y='mean',
            ax=axes,
            label='sync-diff-vm',
            title='Total request time per experiment',
            ylabel='total time (ms)',
        )

    def plot_async(self, axes=plt.gca()):
        self.df_async_single_vm.rolling(3, win_type='gaussian').mean(std=1).plot(
            kind='line',
            y='mean',
            label='async-single-vm',
            ax=axes
        )

        self.df_async_diff_vm.rolling(3, win_type='gaussian').mean(std=1).plot(
            kind='line',
            y='mean',
            ax=axes,
            label='async-diff-vm',
            title='Total request time per experiment',
            ylabel='total time (ms)',
        )

    def plot_new_sync(self, axes=plt.gca(), plot_ci=False):
        self.new_sync.plot(
            kind='line',
            x='i',
            y='mean',
            label='async-single-vm',
            ax=axes
        )

        if plot_ci:
            x = self.new_sync["i"].tolist()
            y = self.new_sync["mean"].tolist()
            ci = self.new_sync["ci"].tolist()

            y_plus = []
            y_minus = []
            for i in range(len(y)):
                y_plus.append(y[i] + ci[i])
                y_minus.append(y[i] - ci[i])

            axes.fill_between(x, y_minus, y_plus, color='b', alpha=.1)


if __name__ == "__main__":
    measures = MeasureDataFrames()
    measures.box()
    measures.show()
