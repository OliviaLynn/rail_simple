"""An example module containing simplistic functions."""

import random
import plotly.express as px
import pandas as pd

from rail.creation.engine import Modeler, Creator
from rail.core.data import TableHandle, ModelHandle


class SimpleModeler(Modeler):
    """A very simple modeler
    
    Not yet implemented"""
    name = "SimpleModeler"
    inputs = []
    outputs = [("model", ModelHandle)]

    def __init__(self, args, comm=None):
        """Initialize Modeler
        
        Modelers can either use:
        1. a catalog (which it will take as input)
        2. just physics (needs no input)
        """
        Modeler.__init__(self, args, comm=comm)
        self.model = dict()
        self.model["percent_blue"] = 0.25
        self.model["percent_white"] = 1.0 - self.model["percent_blue"]
        self.add_data('model', self.model)

    def __str__(self):
        return "SimpleModeler str (to implement)"

    def visualize(self):
        """Create a pie chart showing the proportions"""
        print("visualizing...")
        colors = ['#AAAAAA', '#0074D9'] # gray, blue
        fig = px.pie(
            values=list(self.model.values()),
            names=list(self.model.keys()),
            title='Model Dictionary Visualization',
            color_discrete_sequence=colors
        )
        fig.show()



class SimpleCreator(Creator):
    name = "SimpleCreator"
    inputs = [("model", ModelHandle)]
    outputs = [("output", TableHandle)]

    def __init__(self, args, comm=None):
        """Initialize Simple Creator"""
        Creator.__init__(self, args)

    def sample(self, n_samples: int, seed: int = None, min_x: int = 100, **kwargs):
        self.config["n_samples"] = n_samples
        self.config["seed"] = seed
        self.config["min_x"] = min_x
        self.config.update(**kwargs)
        self.run()
        self.finalize()
        return self.get_handle("output")

    def run(self):
        # TODO probably antipattern, check how to make this work with sample()
        samples = []
        model = self.get_data("model")
        for _ in range(self.config["n_samples"]):
            r = random.random()
            min_x = self.config.min_x
            #get_btwn_x_and_one = lambda x : random.random()*(1.0-x) + x
            get_btwn_x_and_one = lambda x : random.randrange(min_x, 255)
            if r < model.model["percent_blue"]:
                samples.append([0, 0, get_btwn_x_and_one(min_x)])
            else: # white
                x = get_btwn_x_and_one(min_x)
                samples.append([x,
                                x,
                                x]
                              )
        self.samples = samples
        print("created:")
        print(',\n'.join(map(str, samples)))
        self.add_data("output", samples)
        
    def visualize(self):
        samples =  self.samples
        """
        for sample in samples:
            for i in range(len(sample)):
                sample[i] = int(sample[i]*255)
        """
        

        # Convert the RGB values to a list of RGB tuples
        rgb_tuples = [(r, g, b) for r, g, b in samples]

        # Create a DataFrame with the RGB tuples
        df = pd.DataFrame({'RGB': rgb_tuples})

        # Create a scatter plot using Plotly with marker_color
        fig = px.scatter(df, x=df.index, y=[0] * len(df), title='RGB Color Scatter Plot')

        # Set the marker color to match the RGB values
        fig.update_traces(marker=dict(size=12, opacity=1.0, color=rgb_tuples))

        # Show the scatter plot
        fig.show()
