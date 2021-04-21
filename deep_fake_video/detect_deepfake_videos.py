# This python autopsy module extracts mp4 files from data source
# extracts frames from that videos found and evaluates them with machine
# learning in order to note if the video is manipulated or not.
# This module was made mainly for deepfake detection but can detect
# other type of manipulations too.
#
# Contact: Sara Ferreira [sara (dot) ferreira (at) fc (dot) up (dot) pt]
#
# This is free and unencumbered software released into the public domain.
#
# Anyone is free to copy, modify, publish, use, compile, sell, or
# distribute this software, either in source code form or as a compiled
# binary, for any purpose, commercial or non-commercial, and by any
# means.
#
# In jurisdictions that recognize copyright laws, the author or authors
# of this software dedicate any and all copyright interest in the
# software to the public domain. We make this dedication for the benefit
# of the public at large and to the detriment of our heirs and
# successors. We intend this dedication to be an overt act of
# relinquishment in perpetuity of all present and future rights to this
# software under copyright law.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
# IN NO EVENT SHALL THE AUTHORS BE LIABLE FOR ANY CLAIM, DAMAGES OR
# OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE,
# ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR
# OTHER DEALINGS IN THE SOFTWARE.

# Deep_fake_detector 
# April 2021
#
# Comments
#   Version 1.0 - Initial Version

import jarray
import json
import inspect
import os
import ast
import subprocess
import sys
import shutil
from subprocess import Popen, PIPE
from java.lang import System
from java.util.logging import Level
from java.io import File
from org.sleuthkit.datamodel import SleuthkitCase
from org.sleuthkit.datamodel import AbstractFile
from org.sleuthkit.datamodel import ReadContentInputStream
from org.sleuthkit.datamodel import BlackboardArtifact
from org.sleuthkit.datamodel import BlackboardAttribute
from org.sleuthkit.autopsy.datamodel import ContentUtils
from org.sleuthkit.autopsy.ingest import IngestModule
from org.sleuthkit.autopsy.ingest.IngestModule import IngestModuleException
from org.sleuthkit.autopsy.ingest import DataSourceIngestModule
from org.sleuthkit.autopsy.ingest import FileIngestModule
from org.sleuthkit.autopsy.ingest import IngestModuleFactoryAdapter
from org.sleuthkit.autopsy.ingest import IngestMessage
from org.sleuthkit.autopsy.ingest import IngestServices
from org.sleuthkit.autopsy.coreutils import Logger
from org.sleuthkit.autopsy.casemodule import Case
from org.sleuthkit.autopsy.casemodule.services import Services
from org.sleuthkit.autopsy.casemodule.services import FileManager
from org.sleuthkit.autopsy.casemodule.services import Blackboard
from org.sleuthkit.autopsy.datamodel import ContentUtils


# Factory that defines the name and details of the module and allows Autopsy
# to create instances of the modules that will do the analysis.
class SampleJythonDataSourceIngestModuleFactory(IngestModuleFactoryAdapter):

    moduleName = "Detect Deepfake videos"

    def getModuleDisplayName(self):
        return self.moduleName

    # TODO: Give it a description
    def getModuleDescription(self):
        return "Module to detect deepfake and other type of manipulations on videos"

    def getModuleVersionNumber(self):
        return "1.0"

    def isDataSourceIngestModuleFactory(self):
        return True

    def createDataSourceIngestModule(self, ingestOptions):
        # TODO: Change the class name to the name you'll make below
        return SampleJythonDataSourceIngestModule()


# Data Source-level ingest module.  One gets created per data source.
class SampleJythonDataSourceIngestModule(DataSourceIngestModule):

    _logger = Logger.getLogger(SampleJythonDataSourceIngestModuleFactory.moduleName)

    def log(self, level, msg):
        self._logger.logp(level, self.__class__.__name__, inspect.stack()[1][3], msg)

    def __init__(self):
        self.context = None

    # Where any setup and configuration is done
    def startUp(self, context):
        
        # Throw an IngestModule.IngestModuleException exception if there was a problem setting up
        # raise IngestModuleException("Oh No!")
        self.context = context

    # Where the analysis is done.
    def process(self, dataSource, progressBar):

        # we don't know how much work there is yet
        progressBar.switchToIndeterminate()

        # Use blackboard class to index blackboard artifacts for keyword search
        blackboard = Case.getCurrentCase().getServices().getBlackboard()

        #Use FileManager to get all files with the extension .mp4 
        # TODO: Add more extensions
        fileManager = Case.getCurrentCase().getServices().getFileManager()
        files = fileManager.findFiles(dataSource, "%.mp4")

        numFiles = len(files)
        self.log(Level.INFO, "found " + str(numFiles) + "videos")
        progressBar.switchToDeterminate(numFiles)
        fileCount = 0

        #Exit if the data source dont have videos
        if str(numFiles)=="0":
            self.log(Level.INFO, "found " + str(numFiles) + "videos")
            exit()

        #CREATE TEMP DIRECTORY
        Temp_Dir = Case.getCurrentCase().getTempDirectory()
        self.log(Level.INFO, "create Directory " + Temp_Dir)
        temp_dir = os.path.join(Temp_Dir, "videos")
        self.log(Level.INFO, "Path already exists?"+ str(os.path.exists(temp_dir)))
        try:
            if not os.path.exists(temp_dir):
                os.makedirs(temp_dir)
            else:
                shutil.rmtree(temp_dir)# Removes all the subdirectories!
                os.makedirs(temp_dir)
        except:
		    self.log(Level.INFO, "Error creating directory " + temp_dir)

        #CREATE dir to put video frames to classify
        temp_dir2 = os.path.join(temp_dir, "video_frames")
        self.log(Level.INFO, "Path already exists?"+ str(os.path.exists(temp_dir)))
        try:
            if not os.path.exists(temp_dir2):
                os.makedirs(temp_dir2)
            else:
                shutil.rmtree(temp_dir2)# Removes all the subdirectories!
                os.makedirs(temp_dir2)
        except:
		    self.log(Level.INFO, "Error creating directory " + temp_dir)
 

        #Save all images in temp directory
        for file in files:

            # Check if the user pressed cancel while we were busy
            if self.context.isJobCancelled():
                return IngestModule.ProcessResult.OK

            self.log(Level.INFO, "Processing file: " + file.getName())
            fileCount += 1

            # Make an artifact on the blackboard.  TSK_INTERESTING_FILE_HIT is a generic type of
            # artfifact. 
            art = file.newArtifact(BlackboardArtifact.ARTIFACT_TYPE.TSK_INTERESTING_FILE_HIT)
            att = BlackboardAttribute(BlackboardAttribute.ATTRIBUTE_TYPE.TSK_SET_NAME, SampleJythonDataSourceIngestModuleFactory.moduleName, "video found")
            art.addAttribute(att)

            try:
                # index the artifact for keyword search
                blackboard.indexArtifact(art)
            except Blackboard.BlackboardException as e:
                self.log(Level.SEVERE, "Error indexing artifact " + art.getDisplayName())

            

            lclDbPath = os.path.join(temp_dir, file.getName())
            self.log(Level.INFO, file.getName() + ' ==> ' + str(file.getId()) + ' ==> ' + file.getUniquePath()) 
            ContentUtils.writeToFile(file, File(lclDbPath))

            # Update the progress bar
            progressBar.progress(fileCount)

        videos_found=[]
        for subdir, dirs, files in os.walk(temp_dir):
            for file in files:
                videos_found.append(file)
                self.log(Level.INFO, "video found : "+file)

        seed=0
        for file in videos_found:
            seed=seed+1
            #filename= file.getName()
            #self.log(Level.INFO,"filename: "+file)

            #Run exec to extract frames from videos
            self.log(Level.INFO, "dir : "+os.path.dirname(os.path.abspath(__file__)))
            path_to_exe=str(os.path.dirname(os.path.abspath(__file__))).replace('/',"//")+"//dist//video_to_image//video_to_image.exe"
            self.log(Level.INFO, "exec : "+path_to_exe)
            #temp_dir = os.path.join(Temp_Dir, "Images_found")
            self.log(Level.INFO, "Exec file to run: "+ path_to_exe)
            self.log(Level.INFO, "Running program on data source parm 1 ==> " + file)
            pipe = Popen([path_to_exe, file, temp_dir, temp_dir2, str(seed)],stdout=PIPE)
            out_text = pipe.communicate()[0]
            self.log(Level.INFO, "Output from run is ==> " + out_text) 


            #run exec to create data from temp directory 
            self.log(Level.INFO, "dir : "+os.path.dirname(os.path.abspath(__file__)))
            path_to_exe=str(os.path.dirname(os.path.abspath(__file__))).replace('/',"//")+"//dist//create_test_data//create_test_data.exe"
            self.log(Level.INFO, "exec : "+path_to_exe)
            #temp_dir = os.path.join(Temp_Dir, "Images_found")
            self.log(Level.INFO, "Exec file to run: "+ path_to_exe)
            self.log(Level.INFO, "Running program on data source parm 1 ==> " + temp_dir2)
            pipe = Popen([path_to_exe, temp_dir2],stdout=PIPE)
            out_text = pipe.communicate()[0]
            #self.log(Level.INFO, "Output from run is ==> " + out_text)  

            #Sanitization of the output of exec file
            out_text = out_text.replace("'", "\"")
            out_text=json.loads(out_text)
      
            #Data to test
            data=out_text
            X_test= data["data"]
            # TODO: We cant pass this many data in shell, how to pass that? Use file maybe?
            X_test=X_test[:len(X_test)//2]
            self.log(Level.INFO, "Data to pass to model ==> " + str(X_test))
            y_test= data["label"]
            y_test=y_test[:len(y_test)//2]
            self.log(Level.INFO, "Labels to pass to model ==> " + str(y_test))

            self.log(Level.INFO, "Number of fotos to test ==> " + str(len(X_test)))
            #Run exec with the classification algorithm for all images found in the case
            #Train file needs to be in this path
            path_to_exe=str(os.path.dirname(os.path.abspath(__file__))).replace('/',"//")+"//dist//model//model.exe"
            #self.log(Level.INFO, "exec : "+path_to_exe)
            #command= [path_to_exe, str(X_test), str(y_test)]
            pipe = Popen([path_to_exe, str(X_test), str(y_test)],stdout=PIPE)
            out_text = pipe.communicate()[0]
            self.log(Level.INFO, "Output from run is ==> " + str(out_text))

            predictions=[]
            #Predictions of the model
            for i in out_text:
                if i.isnumeric():
                    predictions.append(int(i))

            self.log(Level.INFO, "out_text " + str(predictions))

            # Use blackboard class to index blackboard artifacts 
            blackboard = Case.getCurrentCase().getServices().getBlackboard()

            #create artifact
            artId = blackboard.getOrAddArtifactType("TSK_DEEP_FAKE_DETECT", "Deep fake Detections")
            artifact = dataSource.newArtifact(artId.getTypeID())
            #create attribute
            attId = blackboard.getOrAddAttributeType("TSK_DEEP_FAKE_SCORE", BlackboardAttribute.TSK_BLACKBOARD_ATTRIBUTE_VALUE_TYPE.STRING, "Probability of being manipulated")


            count_fake=0
            for pred in predictions:
                #self.log(Level.INFO, "pred " + str(pred))
                if str(pred)=="0":
                    count_fake=count_fake+1

            self.log(Level.INFO, "number of fake frames: "+ str(count_fake))
            self.log(Level.INFO, "number of frames: "+str(len(predictions)))



            if count_fake>=(len(predictions)//3): 
                artifact_content= file+" is probably fake"
            else:
                artifact_content= file+" is probably real"

            self.log(Level.INFO, "Classification: "+ artifact_content)


            #Add data to atribute
            atribute=BlackboardAttribute(attId, SampleJythonDataSourceIngestModuleFactory.moduleName,  artifact_content)

            try:
                #Add atribute to artifact
                artifact.addAttribute(atribute)
            except:
                self.log(Level.INFO, "Error adding attribute to artifact")

            try:
                #Post artifact in the blackboard
                blackboard.postArtifact(artifact, SampleJythonDataSourceIngestModuleFactory.moduleName)
            except:
                self.log(Level.INFO, "Error indexing artifact") 


        #Code to get artifacts with all contents being classified at the same time
        """  i=0
        for subdir, dirs, files in os.walk(temp_dir):
            for file in files:
                filename = os.path.join(subdir, file)
                #self.log(Level.INFO, "Filename ==> " + str(filename))
                self.log(Level.INFO, "Prediction for this image ==> " + str(predictions[i]))
                if predictions[i]==0:
                    self.log(Level.INFO, "entraste ou nao pah " + "sim")
                    artifact_content= filename.split("\\")[-1]+" is fake"
                elif predictions[i]==1:
                    artifact_content= filename.split("\\")[-1]+" is real"
                else:
                    artifact_content= "Can't classify "+filename.split("\\")[-1]
                i=i+1

                #Add data to atribute
                atribute=BlackboardAttribute(attId, SampleJythonDataSourceIngestModuleFactory.moduleName,  artifact_content)

                try:
                    #Add atribute to artifact
                    artifact.addAttribute(atribute)
                except:
                    self.log(Level.INFO, "Error adding attribute to artifact") """
 
        try:
            #Post artifact in the blackboard
            blackboard.postArtifact(artifact, SampleJythonDataSourceIngestModuleFactory.moduleName)
        except:
            self.log(Level.INFO, "Error indexing artifact") 
        
        #Post a message to the ingest messages in box.
        message = IngestMessage.createMessage(IngestMessage.MessageType.DATA,
            "Sample Jython Data Source Ingest Module", "Found %d images" % fileCount)
        IngestServices.getInstance().postMessage(message)

        message = IngestMessage.createMessage(IngestMessage.MessageType.DATA,
            "Sample Jython Data Source Ingest Module", "Prediciton: %s" % predictions)
        IngestServices.getInstance().postMessage(message)

        return IngestModule.ProcessResult.OK