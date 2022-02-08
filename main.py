# IMPORTS
import os
from knife_point_horror import Story

# Create story objects
stories = []
synopses = [f for f in os.listdir("./Synopses") if f[0] != "_"]
for synopsis in synopses:
    stories.append(Story(synopsis_filename=synopsis))

# Do cool stuff
for story in stories:
    pass
