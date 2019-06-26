
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
sns.set_style('white')
sns.set_context('talk')

import pyNetLogo

netlogo = pyNetLogo.NetLogoLink(gui=True)

netlogo.load_model('Wolf Sheep Predation.nlogo')
#netlogo.command('setup')