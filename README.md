# GRID - Geographic Reconnaissance for Infrastructure Detection

## Setup

### Flask
First: pip install flask. Flask will allow the bridge between the interactive map (user interface) and the python script.

**REPOSITORY MUST BE USING "Alex" BRANCH FOR MODEL INTEGRATION**

After cloning the repo, in the command prompt run `flask run`. This will start the development server. Right click on the index.html file and in the pop-up window, click on 'Open with Live Server'. This will open a google chrome tab (if you are using google chrome) with the interactive google map.

### Model
In order for the model to be integrated into the UI, the model has to be downloaded and added to the repository locally. The following outputs folder has to be located in the top level directory of the repository. The pre-trained and downloaded model can found [here](https://drive.google.com/drive/folders/1suRIGF18j-WZ5ozDmskDm7XOqLPAScIp?usp=sharing). You can also train the model yourself [here](https://github.com/jcchuang2/GRID-Object-Detection-Model).

Additionally, at the top level directory you need to add a (.env) file containing your Google API key in the form `API_KEY = {Your API Key}`.

## Map Interface
At the top of the map is a *Zoom Level* indicator which lets you know what level of zoom you are currently observing. This is necessary because we trained our model at Zoom Level: 19. To the right of the zoom level indicator is the *Center Coordinates* indicator. This will display the Latitude and Longitude of the center of your current map view. At the bottom of the map is the *Boundary Coordinates* indicator. Similar to the Center Coordinates indicator, this will display the Latitude Longitude of the North East corner and South West corner of your current map view.

To the left, there are 3 buttons (excluding the map/satellite buttons which switch the map layout). The *Center Map* button will center the map automatically on San Diego. The *Training Areas* button will toggle on and off the highlighting of the locations of our training areas. The *Identify Poles* button saves an image of your current map view.  

## More Information
More information about this project can be found at our [website](https://jcchuang2.github.io/DSC180B_GRID/).
