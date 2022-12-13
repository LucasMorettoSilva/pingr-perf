import matplotlib.pyplot as plt
import pandas as pd


class MeasureDataFrames:

    def __init__(self):
        folder = "results"
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
        self.box_plot()

    def show(self):
        plt.show()

    def box_plot(self):
        self.df_merge.boxplot(
            by='experiment-type',
            column=['elapsed_time'],
            grid=False
        )

    def plot_sync(self, axes=plt.gca()):
        self.df_sync_single_vm.rolling(3, win_type='gaussian').mean(std=1).plot(
            kind='line',
            y='elapsed_time',
            label='sync-single-vm',
            ax=axes
        )

        self.df_sync_diff_vm.rolling(3, win_type='gaussian').mean(std=1).plot(
            kind='line',
            y='elapsed_time',
            ax=axes,
            label='sync-diff-vm',
            title='Total request time per experiment',
            ylabel='total time (ms)',
        )

    def plot_async(self, axes=plt.gca()):
        self.df_async_single_vm.rolling(3, win_type='gaussian').mean(std=1).plot(
            kind='line',
            y='elapsed_time',
            label='async-single-vm',
            ax=axes
        )

        self.df_async_diff_vm.rolling(3, win_type='gaussian').mean(std=1).plot(
            kind='line',
            y='elapsed_time',
            ax=axes,
            label='async-diff-vm',
            title='Total request time per experiment',
            ylabel='total time (ms)',
        )


if __name__ == "__main__":
    measures = MeasureDataFrames()
    measures.plot()
    measures.show()
