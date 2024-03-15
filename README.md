# GRID - Geographic Reconnaissance for Infrastructure Detection

## Setup

### Model
In order for the model to be integrated into the UI, the model has to be downloaded and added to the repository locally. The following outputs folder has to be located in the top level directory of the repository. The pre-trained and downloaded model can found [here](https://drive.google.com/drive/folders/1suRIGF18j-WZ5ozDmskDm7XOqLPAScIp?usp=sharing). 

You can also train the model by following this Github [repo](https://github.com/jcchuang2/GRID-Object-Detection-Model).

### Applying the model
After making sure you have the proper outputs/checkpoint.pth file from downloading the file above, open Google Maps in satellite view either in an app or through a webpage. Click on "Layers" in the bottom left corner to view the satellite images. 

The model captures the left half of the screen, and has a pop-up window on the right half. It may be needed to split screen accordingly.

Afterwards, zoom in on any area where the user may want to detect poles and begin running 'mssCapture_DETR.py'

Press "q" in the application pop-up window to exit. 


## More Information
More information about this project can be found at our [website](https://jcchuang2.github.io/DSC180B_GRID/).
