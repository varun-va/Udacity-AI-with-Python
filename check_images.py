#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# */AIPND/intropylab-classifying-images/check_images.py
#                                                                             
# TODO: 0. Fill in your information in the programming header below
# PROGRAMMER: Varun V.
# DATE CREATED: 7/19/2018
# REVISED DATE:             <=(Date Revised - if any)
# REVISED DATE: 05/14/2018 - added import statement that imports the print 
#                           functions that can be used to check the lab
# PURPOSE: Check images & report results: read them in, predict their
#          content (classifier), compare prediction to actual value labels
#          and output results
#
# Use argparse Expected Call with <> indicating expected user input:
#      python check_images.py --dir <directory with images> --arch <model>
#             --dogfile <file that contains dognames>
#   Example call:
#    python check_images.py --dir pet_images/ --arch vgg --dogfile dognames.txt
##

# Imports python modules
import argparse
from time import time, sleep
from os import listdir

# regexp for findall
import re
# Imports classifier function for using CNN to classify images 
from classifier import classifier 

# Imports print functions that check the lab
from print_functions_for_lab_checks import *

# Main program function defined below
def main():
    # TODO: 1. Define start_time to measure total program runtime by
    # collecting start time
    start_time = time()
   
    # TODO: 2. Define get_input_args() function to create & retrieve command
    # line arguments
    in_arg = get_input_args()
    #print("Command Line Arguments:\n   dir=",in_arg.dir,"\n   arch=",in_arg.arch,"\n dogfile=",in_arg.dogfile)
    
    # TODO: 3. Define get_pet_labels() function to create pet image labels by
    # creating a dictionary with key=filename and value=file label to be used
    # to check the accuracy of the classifier function
    
    answers_dic = get_pet_labels(in_arg.dir)
    # verify data and print 10 records
    #print("answer_dic has", len(answers_dic)," key-value pairs. \nBelow are 10 of them")
    '''
    prnt = 0
    for key in answers_dic:
        #if prnt < 10:
        #print("%2d key: %-30s label: %-26s" %(prnt+1, key, answers_dic[key]) )
        prnt +=1
      '''

    # TODO: 4. Define classify_images() function to create the classifier 
    # labels with the classifier function uisng in_arg.arch, comparing the 
    # labels, and creating a dictionary of results (result_dic)
    results_dict = classify_images(in_arg.dir,answers_dic,in_arg.arch)
    '''
    print("\n   MATCH: ")
    n_match = 0
    n_nomatch = 0
    
    
    for key in results_dict:
        if results_dict[key][2] == 1:
            n_match += 1
            print("Real: %-26s  Classifier: %-30s" %(results_dict[key][0],results_dict[key][1]))
    
    print("\n NOT MATCHED:")
    for key in results_dict:
        if results_dict[key][2] == 0:
            n_nomatch += 1
            print("Real: %-26s  Classifier: %-30s" %(results_dict[key][0],results_dict[key][1]))
                  
    print("\n# Total Images", n_match + n_nomatch, "# Matches: ",n_match ,"# NOT Matches: ",n_nomatch)
    
    print("\n",results_dict)
    '''
    # temp code to check the data
    
    # TODO: 5. Define adjust_results4_isadog() function to adjust the results
    # dictionary(result_dic) to determine if classifier correctly classified
    # images as 'a dog' or 'not a dog'. This demonstrates if the model can
    # correctly classify dog images as dogs (regardless of breed)
    adjust_results4_isadog(results_dict, in_arg.dogfile)
    '''
    #temp code to check for results
    print("\n   MATCH: ")
    n_match = 0
    n_nomatch = 0
    
    for key in results_dict:
        if results_dict[key][2] == 1:
            n_match += 1
            print("Real: %-26s  Classifier: %-30s   PetlabelDog: %1d    ClassifierLabel: %1d" 
                  %(results_dict[key][0],results_dict[key][1],results_dict[key][3],results_dict[key][4]))
    
    print("\n NOT MATCHED:")
    for key in results_dict:
        if results_dict[key][2] == 0:
            n_nomatch += 1
            print("Real: %-26s  Classifier: %-30s   PetlabelDog: %1d    ClassifierLabel: %1d" 
                  %(results_dict[key][0],results_dict[key][1],results_dict[key][3],results_dict[key][4]))
                  
    print("\n# Total Images", n_match + n_nomatch, "# Matches: ",n_match ,"# NOT Matches: ",n_nomatch)            
    
    print("\n",results_dict)
    '''

    # TODO: 6. Define calculates_results_stats() function to calculate
    # results of run and puts statistics in a results statistics
    # dictionary (results_stats_dic)
    results_stats_dic = calculates_results_stats(results_dict)

      # Code for checking results_stats_dic -
    # Checks calculations of counts & percentages BY using results_dict
    # to re-calculate the values and then compare to the values
    # in results_stats_dic

    # Initialize counters to zero and number of images total
    n_images = len(results_dict)
    n_pet_dog = 0
    n_class_cdog = 0
    n_class_cnotd = 0
    n_match_breed = 0

    # Interates through results_dict dictionary to recompute the statistics
    # outside of the calculates_results_stats() function
    for key in results_dict:

        # match (if dog then breed match)
        if results_dict[key][2] == 1:

            # isa dog (pet label) & breed match
            if results_dict[key][3] == 1:
                n_pet_dog += 1

                # isa dog (classifier label) & breed match
                if results_dict[key][4] == 1:
                    n_class_cdog += 1
                    n_match_breed += 1

            # NOT dog (pet_label)
            else:

                # NOT dog (classifier label)
                if results_dict[key][4] == 0:
                    n_class_cnotd += 1

        # NOT - match (not a breed match if a dog)
        else:

            # NOT - match
            # isa dog (pet label)
            if results_dict[key][3] == 1:
                n_pet_dog += 1

                # isa dog (classifier label)
                if results_dict[key][4] == 1:
                    n_class_cdog += 1

            # NOT dog (pet_label)
            else:

                # NOT dog (classifier label)
                if results_dict[key][4] == 0:
                    n_class_cnotd += 1


    # calculates statistics based upon counters from above
    n_pet_notd = n_images - n_pet_dog
    pct_corr_dog = ( n_class_cdog / n_pet_dog )*100
    pct_corr_notdog = ( n_class_cnotd / n_pet_notd )*100
    pct_corr_breed = ( n_match_breed / n_pet_dog )*100

    # prints calculated statistics
    print("\n ** Statistics from calculates_results_stats() function:")
    print("N Images: %2d  N Dog Images: %2d  N NotDog Images: %2d \nPct Corr dog: %5.1f Pct Corr NOTdog: %5.1f  Pct Corr Breed: %5.1f"
          % (results_stats_dic['n_images'], results_stats_dic['n_dog_images'],
             results_stats_dic['n_notdogs_img'], results_stats_dic['pct_correct_dogs'],
             results_stats_dic['pct_correct_notdogs'],
             results_stats_dic['pct_correct_breed']))
    print("\n ** Check Statistics - calculated from this function as a check:")
    print("N Images: %2d  N Dog Images: %2d  N NotDog Images: %2d \nPct Corr dog: %5.1f  Pct Corr NOTdog: %5.1f  Pct Corr Breed: %5.1f"
          % (n_images, n_pet_dog, n_pet_notd, pct_corr_dog, pct_corr_notdog,
             pct_corr_breed))


    # TODO: 7. Define print_results() function to print summary results, 
    # incorrect classifications of dogs and breeds if requested.
    print_results(results_dict,results_stats_dic,in_arg.arch,True,True)

    # TODO: 1. Define end_time to measure total program runtime
    # by collecting end time
    end_time = time()

    # TODO: 1. Define tot_time to computes overall runtime in
    # seconds & prints it in hh:mm:ss format
    tot_time = end_time - start_time
    print("\n** Total Elapsed Runtime:", tot_time)



# TODO: 2.-to-7. Define all the function below. Notice that the input 
# paramaters and return values have been left in the function's docstrings. 
# This is to provide guidance for acheiving a solution similar to the 
# instructor provided solution. Feel free to ignore this guidance as long as 
# you are able to acheive the desired outcomes with this lab.

def get_input_args():
    """
    Retrieves and parses the command line arguments created and defined using
    the argparse module. This function returns these arguments as an
    ArgumentParser object. 
     3 command line arguements are created:
       dir - Path to the pet image files(default- 'pet_images/')
       arch - CNN model architecture to use for image classification(default-
              pick any of the following vgg, alexnet, resnet)
       dogfile - Text file that contains all labels associated to dogs(default-
                'dognames.txt'
    Parameters:
     None - simply using argparse module to create & store command line arguments
    Returns:
     parse_args() -data structure that stores the command line arguments object  
    """
    parser = argparse.ArgumentParser()
    #argument 1
    parser.add_argument('--dir', type=str, default='my_folder/', help="path to the folder mt_folder")
    #argument 2
    parser.add_argument('--arch', type=str, default='vgg', help='chosen model')
    #argument 3
    parser.add_argument('--dogfile', type=str, default='dognames.txt', help='text file that has dog names')

    args = parser.parse_args()

    return args


def get_pet_labels(image_dir):
    """
    Creates a dictionary of pet labels based upon the filenames of the image 
    files. Reads in pet filenames and extracts the pet image labels from the 
    filenames and returns these label as petlabel_dic. This is used to check 
    the accuracy of the image classifier model.
    Parameters:
     image_dir - The (full) path to the folder of images that are to be
                 classified by pretrained CNN models (string)
    Returns:
     petlabels_dic - Dictionary storing image filename (as key) and Pet Image
                     Labels (as value)  
    """
    # Create list of files in directory
    file_names = listdir(image_dir)
    
    #process each of the files to create a dictonary where the key is filename and value is picture lable
    
    #create empty directory for lables
    pet_dict = dict()
    
    # process through each file of the directory, extracting only 
    # the words of the file that contain pet image label
    
    for i in range(0, len(file_names),1):
        #skip file that starts with . as in Mac, because it is not a pet image file
        if file_names[i][0] != ".":
            
            #use split to extract file names into a list called image_names and 
            #convert the names to lower
            image_names = file_names[i].lower().split("_")
            
            # create a temp label variable to hold pet lable name extracted
            pet_label = ""
            
            #process each of char strings split by _ in image_names list
            #only if word is all letters, then process by putting blanks between words
            
            for word in image_names:
                if word.isalpha():
                    pet_label += word + " "
                    
            # strip trailing whice space
            pet_label.strip()
            
            #If filename already does not exist in pet_dict, add it
            #Report duplicates
            
            if file_names[i] not in pet_dict:
                pet_dict[file_names[i]] = pet_label
            else:
                print("Warning: There are duplicate files in directory", file_names[i])
    
    # return dict of labels
    return(pet_dict)
               
    

def classify_images(images_dir,pet_dict,model):
    """
    Creates classifier labels with classifier function, compares labels, and 
    creates a dictionary containing both labels and comparison of them to be
    returned.
     PLEASE NOTE: This function uses the classifier() function defined in 
     classifier.py within this function. The proper use of this function is
     in test_classifier.py Please refer to this program prior to using the 
     classifier() function to classify images in this function. 
     Parameters: 
      images_dir - The (full) path to the folder of images that are to be
                   classified by pretrained CNN models (string)
      petlabel_dic - Dictionary that contains the pet image(true) labels
                     that classify what's in the image, where its' key is the
                     pet image filename & it's value is pet image label where
                     label is lowercase with space between each word in label 
      model - pretrained CNN whose architecture is indicated by this parameter,
              values must be: resnet alexnet vgg (string)
     Returns:
      results_dic - Dictionary with key as image filename and value as a List 
             (index)idx 0 = pet image label (string)
                    idx 1 = classifier label (string)
                    idx 2 = 1/0 (int)   where 1 = match between pet image and 
                    classifer labels and 0 = no match between labels
    """
    # create a results dict that will have all results key = filename
    # value = list [Pet label, Classifier label, , Match[1=yes, 0 = No]]
    results_dict = dict()
    model_label_1 = list()
    # process all the files from pet_dict , use image_dir to give full path
    for key in pet_dict:
        
        # run the classifier function to classify the images classifier
        # inputs = path + filename  and model, returns model label
        # as classifier label
        
        model_label = classifier(images_dir+key, model)
        #print('model_label - ',model_label)
        
        #process the results so that they can be compared with pet image labels
        model_label = model_label.lower()
        model_label = model_label.strip()
        
        # try and find the pet lables within model label returned
        # use regexp function findall for this match
        pet_label_value = pet_dict[key].strip()
        #print("p-",pet_label_value, "length",len(pet_label_value))
        #print("m-",model_label, "length",len(model_label))
        
        #found = model_label.find(pet_label_value)
        #print("found -",found)
        match = re.findall('\\b'+pet_label_value+'\\b',model_label)
        #print("match",match)
        if len(match) > 0:
            #found label as stand-alone term
            if key not in results_dict:
                results_dict[key] = [pet_label_value,model_label,1]
        else:
            if key not in results_dict:
                results_dict[key] = [pet_label_value,model_label,0]
        #model_label_1.append()= model_label +","
        
    #return the result dict
    #print('model_label_1 - ',model_label_1)
    return(results_dict)

def adjust_results4_isadog(results_dict, dogsfile):
    """
    Adjusts the results dictionary to determine if classifier correctly 
    classified images 'as a dog' or 'not a dog' especially when not a match. 
    Demonstrates if model architecture correctly classifies dog images even if
    it gets dog breed wrong (not a match).
    Parameters:
      results_dic - Dictionary with key as image filename and value as a List 
             (index)idx 0 = pet image label (string)
                    idx 1 = classifier label (string)
                    idx 2 = 1/0 (int)  where 1 = match between pet image and 
                            classifer labels and 0 = no match between labels
                    --- where idx 3 & idx 4 are added by this function ---
                    idx 3 = 1/0 (int)  where 1 = pet image 'is-a' dog and 
                            0 = pet Image 'is-NOT-a' dog. 
                    idx 4 = 1/0 (int)  where 1 = Classifier classifies image 
                            'as-a' dog and 0 = Classifier classifies image  
                            'as-NOT-a' dog.
     dogsfile - A text file that contains names of all dogs from ImageNet 
                1000 labels (used by classifier model) and dog names from
                the pet image files. This file has one dog name per line
                dog names are all in lowercase with spaces separating the 
                distinct words of the dogname. This file should have been
                passed in as a command line argument. (string - indicates 
                text file's name)
    Returns:
           None - results_dic is mutable data type so no return needed.
    """
    dognames_dict = dict()

    # read the file dognames.txt
    with open(dogsfile,'r') as infile:
        line =infile.readline()

        #process each line till eof is reached
        while line != "":

            #strip newline from each line
            line = line.rstrip()
            #add dogsname to dognames_dict if it does not exists
            if line not in dognames_dict:
                dognames_dict[line] = 1
            else:
                print("**Warning, duplicate dognames",line)

            #read in next line from the txt file till eof is reached
            line = infile.readline()

        for key in results_dict:
            #PET image label is of dog(e.g. found in dognames_dict
            if results_dict[key][0] in dognames_dict:

                #classifier label is of dog(e.g. found in dognames_dict
                #appends (1,1) because both labels are dog
                if results_dict[key][1] in dognames_dict:
                    results_dict[key].extend((1,1))
                    
                #classifier label is not of a dog(e.g. NOT in dognames_dict)
                #appends(1,0) because only pet label is dog
                else:
                    
                    results_dict[key].extend((1,0))
                    
            #Pet image label is not a dog image(e.g. NOT found in dognames_dict)
            else:
                #Classifier label is of dog
                #appends(0,1) because only classifier label is of dog
                if results_dict[key][1] in dognames_dict:
                    results_dict[key].extend((0,1))
                #classifier label is NOT of a dog
                #appends (0,0) because both labels are not dog
                else:
                    results_dict[key].extend((0,0))
                    
    #pass


def calculates_results_stats(results_dict):
    """
    Calculates statistics of the results of the run using classifier's model 
    architecture on classifying images. Then puts the results statistics in a 
    dictionary (results_stats) so that it's returned for printing as to help
    the user to determine the 'best' model for classifying images. Note that 
    the statistics calculated as the results are either percentages or counts.
    Parameters:
      results_dic - Dictionary with key as image filename and value as a List 
             (index)idx 0 = pet image label (string)
                    idx 1 = classifier label (string)
                    idx 2 = 1/0 (int)  where 1 = match between pet image and 
                            classifer labels and 0 = no match between labels
                    idx 3 = 1/0 (int)  where 1 = pet image 'is-a' dog and 
                            0 = pet Image 'is-NOT-a' dog. 
                    idx 4 = 1/0 (int)  where 1 = Classifier classifies image 
                            'as-a' dog and 0 = Classifier classifies image  
                            'as-NOT-a' dog.
    Returns:
     results_stats - Dictionary that contains the results statistics (either a
                     percentage or a count) where the key is the statistic's 
                     name (starting with 'pct' for percentage or 'n' for count)
                     and the value is the statistic's value 
    """
    results_stats = dict()
    results_stats['n_dog_images'] = 0
    results_stats['n_match'] = 0
    results_stats['n_correct_dogs'] = 0
    results_stats['n_correct_notdogs'] = 0
    results_stats['n_correct_breed'] = 0

    #print('results_dict - ',results_dict)

    for key in results_dict:

        # labels match - results_dict[key][2] == 1
        if results_dict[key][2] == 1:
            results_stats['n_match'] += 1
        # pet image label is a DOG and Labels match  - counts correct breed

        if sum(results_dict[key][2:]) == 3:
            results_stats['n_correct_breed'] += 1

        #pet image label is a DOG - count the number of dog images
        #print('results_dict_key3',results_dict[key][3])
        if results_dict[key][3] == 1:
            results_stats ['n_dog_images'] += 1

            # classifier classifies images as DOG
            # counts the number of correct dog classification
            #print('n_correct_dogs',results_dict[key][4])
            if results_dict[key][4] == 1:

                results_stats['n_correct_dogs'] += 1

        #Pet image label is not a DOG
        else:
            #classifier classifies image as NOT a dog
            #count the number of correct NOT DOG classification
            if results_dict[key][4] == 0:
                results_stats['n_correct_notdogs'] += 1
        results_stats['n_images'] = len(results_dict)

    # calculate number of non-dog images using  - images and dog images counts
    results_stats['n_notdogs_img'] = (results_stats['n_images'] - results_stats['n_dog_images'])

    #calculate % correct for matches
    results_stats['pct_match'] = (results_stats['n_match']/results_stats['n_images'])*100.0

    #calculare % correct dogs
    results_stats['pct_correct_dogs'] = (results_stats['n_correct_dogs']/results_stats['n_dog_images'])* 100.0

    #calculate % correct breed of dog
    results_stats['pct_correct_breed'] = (results_stats['n_correct_breed']/results_stats['n_dog_images'])*100.0

    #calculate % correct not-a-dog images
    #use if else when no 'not a dog' images are submitted
    if results_stats['n_notdogs_img'] > 0:
        results_stats['pct_correct_notdogs'] = (results_stats['n_correct_notdogs']/results_stats['n_notdogs_img'])* 100.0
    else:
        results_stats['pct_correct_notdogs'] = 0.0

    #print(results_stats)
    return results_stats


def print_results(results_dict,result_stats,model,print_incorrect_dogs = False,print_incorrect_breed = False):
    """
    Prints summary results on the classification and then prints incorrectly
    classified dogs and incorrectly classified dog breeds if user indicates
    they want those printouts (use non-default values)
    Parameters:
      results_dict - Dictionary with key as image filename and value as a List
             (index)idx 0 = pet image label (string)
                    idx 1 = classifier label (string)
                    idx 2 = 1/0 (int)  where 1 = match between pet image and
                            classifer labels and 0 = no match between labels
                    idx 3 = 1/0 (int)  where 1 = pet image 'is-a' dog and
                            0 = pet Image 'is-NOT-a' dog.
                    idx 4 = 1/0 (int)  where 1 = Classifier classifies image
                            'as-a' dog and 0 = Classifier classifies image
                            'as-NOT-a' dog.
      results_stats - Dictionary that contains the results statistics (either a
                     percentage or a count) where the key is the statistic's
                     name (starting with 'pct' for percentage or 'n' for count)
                     and the value is the statistic's value
      model - pretrained CNN whose architecture is indicated by this parameter,
              values must be: resnet alexnet vgg (string)
      print_incorrect_dogs - True prints incorrectly classified dog images and
                             False doesn't print anything(default) (bool)
      print_incorrect_breed - True prints incorrectly classified dog breeds and
                              False doesn't print anything(default) (bool)
    Returns:
           None - simply printing results.
    """

    #print summary
    print("\n\nResults summary for CNN Model Architecture",model.upper())
    print("%20s: %3d" %('N Images',result_stats['n_images']))
    print("%20s: %3d" %('N Dog Images',result_stats['n_dog_images']))
    print("%20s: %3d" %('N Not-Dog Images',result_stats['n_notdogs_img']))

    #Print summary stats on Model run
    print(" ")
    for key in result_stats:
        if key[0] == "p":
            #print("key, value",(key,result_stats[key]))
            print("%20s: %5.1f" %(key,result_stats[key]))

    # if print_incorrect_dogs = True and if images were incorrectly classified
    # as dogs or vice versa, print here

    #print("print_incorrect_dogs",print_incorrect_dogs)
    #print("n_correct_dogs",result_stats['n_correct_dogs'])
    #print("n_correct_notdogs",result_stats['n_correct_notdogs'])
    #print("n_images",result_stats['n_images'])

    if(print_incorrect_dogs and ((result_stats['n_correct_dogs'] +
                                  result_stats['n_correct_notdogs']) != result_stats['n_images'])):
        print("\n Incorrect Dog/Not Dog classifications:")

        #run through results_dict for results
        for key in results_dict:

            #Pet image label is a DOG, classified as NOT A DOG - OR -
            # per image label is NOT a dog, classified as a DOG
            if sum(results_dict[key][3:]) == 1:
                print("Real: %-26s  Classifier: %-30s" %(results_dict[key][0],results_dict[key][1]))

    #if print_incorrect_breed = True and if dog breeds were incorrectly classified
    if(print_incorrect_breed and (result_stats['n_correct_dogs'] != result_stats['n_correct_breed'] )):
        print("\n Incorrect Dog Breed classifications:")

        for key in results_dict:
            #print("sum_3",sum(results_dict[key][3:]))
            #print("key_2",results_dict[key][2])

            # Pet image lable = Dog, Classified= Dog, but wrong breed
            if (sum(results_dict[key][3:]) == 2 and results_dict[key][2] == 0):
                print("Real: %-26s  Classifier: %-30s"%(results_dict[key][0],results_dict[key][1]))

                
                
# Call to main function to run the program
if __name__ == "__main__":
    main()
