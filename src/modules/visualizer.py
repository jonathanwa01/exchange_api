
import plotly.graph_objects as go
import pandas as pd


class Visualizer:
    '''
    Class to load and visualize the currecy data

    '''
    DATE_COLUMN = 'Date'

    def __init__(self, parquet_path: str):
        '''
        Constructor. Creates a visualizer instance.

        Args:
            parquet_path (str): path to parquet file containing
                                the currency exchange data from the API
        '''

        self.parquet_path = parquet_path
        self.df = pd.DataFrame()

    def read_fom_parquet(self) -> pd.DataFrame:
        '''
        Reads and returns data from parquet file

        Returns:
            pd.Dataframe
        '''
        if self.df.empty:
            self.df = pd.read_parquet(self.parquet_path)
        return self.df

    def create_scatter_plot(self) -> go.Figure:
        '''
        Creates a plotly scatter plot

        Returns:
            go.Figure
        '''
        df = self.df.copy()
        main_fig = go.Figure()

        for column in df.columns:
            if column == Visualizer.DATE_COLUMN:
                continue
            fig = go.Scatter(
                x=df[Visualizer.DATE_COLUMN],
                y=df[column],
                mode='lines',
                name=column
            )
            main_fig.add_trace(fig)
        main_fig.update_layout(
            title=dict(text='Exchange Rate of Euro')
        )
        main_fig.update_yaxes(
            title='Exchange Rate'
        )
        return main_fig
