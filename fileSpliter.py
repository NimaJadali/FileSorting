import os
import unittest
from typing import Tuple


def produce(filename: str, numberOfAgents = 3) -> Tuple[str, str, str]:
    """Takes in a filename and make a default of three or other number of files and returns the output filenames.
    """
    #initialize important values
    #Note, the resulting files are split into two types, those with minChunkSize missing and those with minChunkSize + 1 missing
    #For the 3 agent example, since a file is being split for 3 individuals, an example situation could be two individuals will have 1 more byte of #information than the other one if the file size is divided by 3 and leaves a remained of 2. If the remainder was one (e.g. file size 7 byte)
    #then only one agent would have a missing cluster of data of size 3 and the two remaining agents will have size 2. This minimizes overlap and #filesizes
    
    fileLength = os.path.getsize(filename)
    minChunkSize = fileLength // numberOfAgents
    chunkRemainder = fileLength % numberOfAgents
    splitFilesList = [None] * numberOfAgents
    with open (filename, "rb") as readFile:
        for index in range(numberOfAgents):
            fileNameSplit = 'splitfile_' + str(fileLength) + '_' + str(numberOfAgents) + '_' + str(index)
            splitFilesList[splitIndex] = fileName   
            a = index
            rem = chunkRemainder
            #firstChunk is the first portion of the readFile that gets read and written to the returnFile at the current index
            firstChunk = 0
            while (a and rem):
                firstChunk += minChunkSize + 1
                a -= 1
                rem -= 1
            while a:
                firstChunk += minChunkSize
                a -= 1
            readFilePart = readFile.read(firstChunk)
            with open(fileNameSplit, "wb") as splitFile:
                splitFile.write(readFilePart)
            #remainingChunk is the last portion of the readFile that gets read and written to the returnFile at the current index
            #The readFilePart.read(minChunkSize) or (minChunkSize + 1) skips the cluster of data that is not recorded in the current
            #index file to keep the files incomplete.
            if (index > chunkRemainder):
                readFilePart.read(minChunkSize)
                remainingChunk = minChunkSize + firstChunk
            else:
                readFilePart.read(minChunkSize + 1)
                remainingChunk = minChunkSize + 1 + firstChunk
                
            readFilePart = readFile.read(remainingChunk)
            with open(fileNameSplit, "wb") as splitFile:
                splitFile.write(readFilePart)                
    return tuple(splitFilesList)


def combine(filename1: str, filename2: str) -> str:
    """Takes in any two binary input files from produce and recreates the files and returns the output filename.
    """
    #Parse file names to get useful information
    #[splitfile, wholefileLength, numberOfAgents, index]
    listFile1 = filename1.split("_")
    listFile2 = filename2.split("_")
    
    fileLength = listFile1[1]
    minChunkSize = fileLength // listFile1[2]
    chunkRemainder = fileLength % listFile1[2]
    cRem = chunkRemainder
    
    index1 = listFile1[3]
    firstChunk = 0
    
    returnFile = 'returnFile'
    
    #Was rushing so much of the code names need to be changed to make more clear
    #The two files are recombined by using the parsed file information to find where the missing cluster of data
    #from the first file is. This missing cluster is filled in by the second file which is guarenteed to have this data,
    #since no two files are missing the same data.    
    while (index1 and chunkRemainder):
        firstChunk += minChunkSize + 1
        index1 -= 1
        chunkRemainder -= 1
    while index1:
        firstChunk += minChunkSize
        index1 -= 1
    with open (filename1, "rb") as readFile:
        readFilePart = readFile.read(firstChunk)
        with open(returnFile, "wb") as returnFile:
            returnFile.write(readFilePart)
        
    with open (filename2, "rb") as readFile:
        if (listFile1[3] > cRem):
            readFilePart = readFilePart.read(minChunkSize)
            remainingChunk = minChunkSize + firstChunk
        else:
            readFilePart = readFilePart.read(minChunkSize + 1)
            remainingChunk = minChunkSize + 1 + firstChunk    
        with open(returnFile, "wb") as returnFile:
            returnFile.write(readFilePart)
            with open(filename1, "rb") as readFileLast:
                readFilePart = readFileLast.read(remainingChunk)
                returnFile.write(readFilePart)    
    return returnFile


#The unit tests check for spliting and combination errors.
#tests might not be functional since bitarrays are different from binary files.

class TestMe(unittest.TestCase):
    newFileArray = [3, 2, 81, 32]
    newFileBytes = bytearray(newFileArray)
    newFile = open("testFile1", "wb")
    newFile.write(newFileBytes)
    
    file1, file2, file3 = produce(newFile)
    
    def test_file1_and_2(self):
        recombineF12 = combine(file1, file2)
        self.assertEqual(recombineF12, newFile, "recombination of File 1 and 2 Failed")
        
    def test_file1_and_3(self):
        recombineF13 = combine(file1, file3)
        self.assertEqual(recombineF13, newFile, "recombination of File 1 and 3 Failed")
    
    def test_file2_and_3(self):
        recombineF23 = combine(file2, file3)
        self.assertEqual(recombineF23, newFile, "recombination of File 2 and 3 Failed")
    
    def test_file11(self):
        recombineF11 = combine(file1, file1)
        self.assertNotEqual(recombineF11, newFile, "File 1 is complete on its own")

    def test_file11(self):
        recombineF11 = combine(file2, file2)
        self.assertNotEqual(recombineF11, newFile, "File 2 is complete on its own")
        
    def test_file11(self):
        recombineF11 = combine(file3, file3)
        self.assertNotEqual(recombineF11, newFile, "File 3 is complete on its own")
        
    

if __name__ == "__main__":
    unittest.main()

