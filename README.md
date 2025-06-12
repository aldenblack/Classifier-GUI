# ![egg icon](https://github.com/aldenblack/Classifier-GUI/blob/main/egg_icon.png?raw=true) Fecundity Data Classifier GUI ![egg icon](https://github.com/aldenblack/Classifier-GUI/blob/main/egg_icon.png?raw=true)

This is a GUI designed to help with classifying images by the amount of a given object in them. The intended use case is for counting fly eggs from images from a fecundity assay. Each image is split into 100 tiles, each of which should be counted according to the number of eggs more than halfway on screen. 

![classifier interface](https://github.com/aldenblack/Classifier-GUI/blob/main/Classifier-GUI-screenshot.png?raw=true)

## How to Use

### Opening Your File

First, drag the folder of images you want to classify over to the Classifier GUI window. If the folder contains full cap images, a new file called 
\<filename>-sliced, which contains all of the tiles, will be generated in the same directory as the original. An additional file called <filename>.csv will be generated in that directory, which contains all of the counts for your data. Do not manually edit this — this is the file you will send when you finish counting a dataset. 

If your folder contains tiles already, then make sure its name is of the form "\<filename>-sliced", and that there is another folder in the same directory named \<filename>. If you do this, you will be able to see each tile side by side with the source image, which can help with discerning confusing details on a tile.

### Classifying Tiles

To classify the tiles, you can use the buttons available or the certain hotkeys on your keyboard. All progress is immediately and automatically saved in your csv file, so do not worry about closing the GUI and opening it later.

#### Numerical Classification

To assign your count number to the image, the "0 Eggs", "1 Egg", and "Custom" buttons can be clicked. Alternately, any of the number keys work as hotkeys for classifying tiles with 0-9 eggs. For images with 10 or more eggs, use the arrow keys (up and down) to increase or decrease the amount of eggs on the "Custom" button. Then, either click the "Custom" button or click the 'C' or 'S' key on your keyboard.

#### Click to Count

You can also create custom counts by clicking on parts of the tile to mark them with a dot. Click dots again to remove them. This is useful if you have an especially dense tile (e.g. 20+ eggs) and you want to keep track of the amount you've counted. Click 'C', 'S', 'Enter', 'Space', or the "Custom" button to submit counts. You can add or remove from the tally you count with the arrow keys, like in the previous section. 

![dense cluster](https://github.com/aldenblack/Classifier-GUI/blob/main/Classifier-GUI-cluster.png?raw=true)


#### Unsure

If you are unsure about the number of eggs you have - and especially if you are unsure whether the image has an egg or not - click the "Unsure" button or the 'U' key on your keyboard. 

#### Undo

To undo, click the "Undo" button or the 'Z' key on your keyboard. 

Note that the GUI automatically ignores tiles with too much whitespace, which is why some areas will get skipped when counting, and why the progress bar already shows classified tiles when you first open it.

## Installation

[Windows Download](https://github.com/aldenblack/Classifier-GUI/releases/download/v1.1.0/classifier_gui_windows_v1.1.0.zip) 

[Mac Download](https://github.com/aldenblack/Classifier-GUI/releases/download/v1.1.0/classifier_gui_mac_v1.1.0.zip)
