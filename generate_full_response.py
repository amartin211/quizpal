# python -m virtualenv envsp
# source env/bin/activate
# pip freeze > requirements.txt


import numpy as np
import os
from mathpix import ocr_mathpix
from pathlib import Path  



from image_preprocessing import (detect_vertical_band_simplified, 
                                 preprocessing_raw_image, 
                                 split_if_band)

from utils import (check_folder_empty, 
                   create_folder, 
                   empty_folder, 
                   similarityscore, 
                   create_tuple_from_string, 
                   is_text_missing)

from prompt_engineering_refined import (get_completion, 
                                        merge_two_texts_into_one,
                                        text_cleaner,
                                        question_cleaner,
                                        structure_response,

                                        answer_ps_question, 
                                        answer_ds_question, 
                                        answer_rc_question, 
                                        answer_cr_question, 
                                        answer_sc_question)


def get_response_from_raw_image(file_path):

    file_name = Path(file_path).name

    dir_path = "static/uploads/"
    create_folder(dir_path)
    
    path_to_image = file_path

    processed_folder = "processed_folder"
    full_text_folder = "previous_full_passage"
    missign_text_folder = "missing_passage_folder"

    path_to_processed= f"{dir_path}/{processed_folder}"
    path_to_previous_text = f"{dir_path}/{full_text_folder}"
    path_to_missing_text = f"{dir_path}/{missign_text_folder}"

    create_folder(path_to_processed)
    create_folder(path_to_previous_text)
    create_folder(path_to_missing_text)

    print("ok")

    file_path = path_to_image
    file_path_processed = os.path.join(path_to_processed, file_name)
    file_path_processed_cropped = (os.path.join(path_to_processed, f"left_{file_name}"), os.path.join(path_to_processed, f"right_{file_name}"))

    processed_img = preprocessing_raw_image(file_path, file_path_processed)

    ## STEP 2 : DETECT ANY VERTICAL BAND 
    if detect_vertical_band_simplified(processed_img):
        print("BAND DETECTED")
        left_crop, right_crop = split_if_band(processed_img, file_path_processed_cropped)
    
        text = ocr_mathpix(file_path_processed_cropped[0])
        question = ocr_mathpix(file_path_processed_cropped[1])


        # CHECK IF A MISSING TEXT HAS ALREADY BEEN RETRIEVED
        if not check_folder_empty(path_to_missing_text):
            initial_text = open(f"{path_to_missing_text}/missing_passage.txt","r").read()
            score = similarityscore(initial_text, text)
            print(score)

            if score > 0.99:
     
                print("a missing text already exist, we'll complete this text and save it")
                combined_text = f"{initial_text}+///+{text}"
                clean_text = merge_two_texts_into_one(combined_text)
            
                with open(f"{path_to_previous_text}/prior_full_passage.txt", 'w') as f:
                    f.write(clean_text)

                empty_folder(path_to_missing_text)
                


        # CHECK IF A FULL TEXT HAS ALREADY BEEN RETRIEVED
        if not check_folder_empty(path_to_previous_text):
            text1 = open(f"{path_to_previous_text}/prior_full_passage.txt","r").read()
            score = similarityscore(text1, text)
            print(score)

            if score > 0.99:
                print("a full text already exist, we'll use this text")
                # TEXT ALREADY COMPLETE : WE CAN GENERATE THE ANSWER 
                formated_question = question_cleaner(question)
                full_question = f"{text1}\n{formated_question}"
             
                
                print(full_question)
                final_response = answer_rc_question(full_question)
                answer_choice = structure_response(final_response)

                print(final_response)
                return file_path, file_path_processed, full_question, final_response, answer_choice
        
            else:
                # THE TEXT IS NEW 
                clean_text = text_cleaner(text) 
                print(text)
                print(clean_text)

        else:
            # THE TEXT IS NEW 
            clean_text = text_cleaner(text)
            print(text)
            print(clean_text)


        # Is the text full ? 
        if is_text_missing(clean_text):
            print("some text are missing, we are saving this part")
            with open(f"{path_to_missing_text}/missing_passage.txt", 'w') as f:
                f.write(clean_text)
            return "waiting for the next image to complete the text"


        formated_question = question_cleaner(question)
        clean_question = f"{clean_text}+\n+{formated_question}"

        #clean_question = get_completion(full_question)
     
        final_response = answer_rc_question(clean_question)
        answer_choice = structure_response(final_response)
        print(final_response)
        return file_path, file_path_processed, clean_question, final_response, answer_choice


    else:
        print("NO BAND DETECTED")
        text_question = ocr_mathpix(file_path_processed)
        print(text_question)
        output = get_completion(text_question)
        print(output)
        question_type, clean_question = create_tuple_from_string(output)

        print(question_type)
        print(clean_question)
    
    #    
        if question_type == 'critical reasoning':
            final_response = answer_cr_question(clean_question)
        elif question_type == 'problem solving':
            final_response = answer_ps_question(clean_question)
        elif question_type == 'data sufficiency':
            final_response = answer_ds_question(clean_question)
        elif question_type == 'sentence correction':
            final_response = answer_sc_question(clean_question)


        answer_choice = structure_response(final_response)

        print(final_response)
        print(answer_choice)
        return file_path, file_path_processed, clean_question, final_response, answer_choice
    

#file_path = "/home/aime/python-environments/exam_script_deploy/static/uploads/20230831105609.jpeg"
#get_response_from_raw_image(file_path)