###########################################################################################
# Image Parser program to prompt the user for a jpg file to parse and extract the camera
# make and model used to take the picture
###########################################################################################

import ImageManager as im
import os

###########################################################################################
# Method to check the existence of a file called 'PhotosFolderPath.txt' in current
# working directory. Error message displayed if it does not exist. If it does exist, it will
# read the path that it contains. If contained path does not exist, error is displayed. 
# 
# Returns True if path in PhotosFolderPath.txt exists and also returns that path
# Returns False if PhotosFolderPath.txt does not exist or if contained path in that file
# does not exist
############################################################################################
def retrievePhotosFilePath():
    try:
        # Check existence of PhotosFolderPath data file, abort if does not exist
        folderLocationFound = False
        photosFolderLocation = ''
        if(os.path.isfile('PhotosFolderPath.txt')):
            photosPathFile = open('PhotosFolderPath.txt', 'r')
            photosFolderLocation = photosPathFile.read()
            print("PhotosFolder data file exists. Reading directory location: " + photosFolderLocation)
            photosPathFile.close()
            if(os.path.isdir(photosFolderLocation)):
                folderLocationFound = True
            else:
                print("Photos directory location: " + photosFolderLocation + " does not exist. Aborting.")    
        else:
            print("PhotosFolder data file does not exist. Aborting")

        return folderLocationFound, photosFolderLocation

    except Exception as err:
        print("Unknown error in ImageParser::retrievePhotosFilePath: {0}".format(err))
    


###########################################################################################
# Method to iterate through an inputted directory and return the amount of .jpg files found
# and a dictionary of the files themselves
#
# photoOptions dictionary format (embedded dictionary of filenames and filepaths):
# { 1 : {'filename':filename1, 'filepath':filepath1} }
# { 2 : {'filename':filename2, 'filepath':filepath2} }
# { 3 : {'filename':filename3, 'filepath':filepath3} }
# etc....
############################################################################################
def retrievePhotosList(photosDir):
    try:
        photoOptions = {}
        counter = 0
        for root, dirs, files in os.walk(photosDir):
            for file in files:
                if(file.find(".jpg") > -1):
                    # if a .jpg file is found, create a dictionary listing for it including its
                    # filename (for display purposes) and path (for parsing purposes)
                    filePropertiesDict = {}
                    counter += 1
                    filePropertiesDict['fileName'] = file
                    filePropertiesDict['filePath'] = os.path.join(root, file)
                    # add the filePropertiesDict to the photoOptions Dictionary
                    photoOptions[counter] = filePropertiesDict
        
        return counter, photoOptions

    except Exception as err:
        print("Unknown error in ImageParser::retrievePhotosList: {0}".format(err))


###########################################################################################
# Main method to collect .jpg files in given folder and prompt user for one to parse
# Camera Make and Model as well as Endian value of the selected .jpg file will be 
# outputted
###########################################################################################
try:
    # if photos directory exists in input file (PhotosFolderPath.txt)
    photosDirectoryFound, photosDirectory = retrievePhotosFilePath()
    if(photosDirectoryFound == True):
        # retrieve the dictionary of numbered .jpg files and their names and paths
        numberOfPhotos, photoFileDict = retrievePhotosList(photosDirectory)
        if(numberOfPhotos > 0):
            selection = ''
            # continue to prompt until user quits with '0' or 'q'
            while (selection != '0') and (selection != 'q'):
                print("\nPlease enter a number of the photo you would like to process (0 or q to quit):")
                for key, value in photoFileDict.items():
                    photoOptions = photoFileDict[key]['fileName']
                    print(key, photoOptions)

                selection = input("What is your choice? ")
                if(selection != '0') and (selection != 'q'):
                    # ensure entered value is valid
                    if((selection.isdigit() == False) or (int(selection) > numberOfPhotos)):
                        print("INVALID ENTRY!")
                    else:
                        # valid selection, so parse the .jpg file selected
                        parsedImage = im.ImageManager(photoFileDict[int(selection)]['filePath'])
                        parsedImage.parseImage()
                        print("Camera Make:", parsedImage.cameraMake)
                        print("Camera Model:", parsedImage.cameraModel)
                        print("Endian:", parsedImage.endian)
        else:
            print("No Jpg Photos Exist. Aborting")
            
except Exception as err:
    print("Unknown error in ImageParser::Main: {0}".format(err))
    im.ImageManager.printMoreErrInfo(err)

