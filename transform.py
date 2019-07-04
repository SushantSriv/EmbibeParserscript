import requests
import json
from pprint import pprint
import glob

# docx_files = [f for f in glob.glob("**/*.docx", recursive=True)]

docx_files =  ['NEET Pre UG M_04012016_90_komal file.docx']

for file_name in docx_files:
    files = {
        'file': (file_name, open(file_name, 'rb')),
    }

    response = requests.post('http://staging2ms.embibe.com/content_ms/v1/embibe/en/ingetion/parser/upload', files=files)
    # while(len(response.json['questions']))
    d = response.json()
    # print(d)
    len1 = len(d["parsed_data"]['questions'])
    js = {}
    js1 = []
    d1 = ''
    for i in range(len1): #change to len1 later
        if(not d['parsed_data']['questions'][i]['errors']):

            ans = []
            if(d['parsed_data']['questions'][i]['question_type'] == 'Single Choice' or d['parsed_data']['questions'][i]['question_type'] == 'Multiple Choice'):
                for j in range(len(d['parsed_data']['questions'][i]['options'])):
                    d1 = list(d['parsed_data']['questions'][i]['options'][j].values())
                    # print(d1[0]['is_correct'])
                    if(d1[0]['is_correct']):
                        ans.append({"is_correct":d1[0]['is_correct'] ,
                                    "answerinfo":d1[0]['body'],
                                    "answer_explaination":d['parsed_data']['questions'][i]['explanation']})
                    else:
                        ans.append({"is_correct": d1[0]['is_correct'],
                                    "answerinfo": d1[0]['body'],
                                    "answer_explaination": ""})
                    #     if(d['parsed_data']['questions'][i]['answer'] == 'A'):
                    #         ans.append({"is_correct":True,
                    #                     "answerinfo":d['parsed_data']['questions'][0]['options'][0]['A']['body'],
                    #                     "answer_explaination":d['parsed_data']['questions'][i]['explanation']})
                    #         f = 1
                    #
                    #     elif(d['parsed_data']['questions'][i]['answer'] == 'B'):
                    #         ans.append({"is_correct":True,
                    #                     "answerinfo":d['parsed_data']['questions'][0]['options'][1]['B']['body'],
                    #                     "answer_explaination":d['parsed_data']['questions'][i]['explanation']})
                    #         f = 1
                    #     elif (d['parsed_data']['questions'][i]['answer'] == 'C'):
                    #         ans.append({"is_correct": True,
                    #                     "answerinfo": d['parsed_data']['questions'][0]['options'][2]['C']['body'],
                    #                     "answer_explaination": d['parsed_data']['questions'][i]['explanation']})
                    #         f = 1
                    #     elif (d['parsed_data']['questions'][i]['answer'] == 'D'):
                    #         ans.append({"is_correct": True,
                    #                     "answerinfo": d['parsed_data']['questions'][0]['options'][3]['D']['body'],
                    #                     "answer_explaination": d['parsed_data']['questions'][i]['explanation']})
                    #         f = 1
                    # else:
                    #     if(d['parsed_data']['questions'][0]['options'][0])
            elif(d['parsed_data']['questions'][i]['question_type'] == 'Integer Type') or (d['parsed_data']['questions'][i]['question_type'] == 'Subjective Numerical Type'):
                ans.append({"is_correct": True,
                            "answerinfo":d['parsed_data']['questions'][i]['answer'],
                            "answer_explaination": d['parsed_data']['questions'][i]['explanation']})
            # key_concept_ids = []
            # key_concept_ids.append({"key_concept_id":d['parsed_data']['questions'][i]['question_tags']["key_concept_tag"]})
            # key_concept_ids.append({"sequencenumber":1})
            metafields = []
            #metafields.append({"idealtime":d['parsed_data']['questions'][i]['question_tags']["ideal_time"]})
            metafields.append({"idealtime":0})
            #metafields.append({"difficultylevel":d['parsed_data']['questions'][i]['question_tags']["difficulty_level"]})
            metafields.append({"difficultylevel":0})
             #metafields.append({"topic_id":d['parsed_data']['questions'][i]['question_tags']["topic_code"]})
            metafields.append({"topic_id":""})
            # metafields.append(key_concept_ids)
            js1.append({
                                "question_type_value": d['parsed_data']['questions'][i]['question_type'],
                                "questioninfo": d['parsed_data']['questions'][i]['q_body'],
                                "answers": ans,
                                "metafields":metafields
                                })
            #     print(d['parsed_data']['questions'][i]['options'][j].values())
    js = {"questions":js1 }
    js2 = json.dumps(js)
    print(js2)
    f = open(file_name.rstrip(".docx")+".json", 'w')

    d = json.dumps(js)
    f.write(d)