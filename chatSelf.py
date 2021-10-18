import requests 
from requests.structures import CaseInsensitiveDict
import csv
import time

# api setting
url = 'https://api-inference.huggingface.co/models/facebook/blenderbot-400M-distill'
headers = CaseInsensitiveDict()
headers["authorization"] = "Bearer api_WekdxpzeyQSGDByUfNgoRzlpOnIbssfRLU"

# each robot reply number
talkround = 50
postround = talkround * 2

# default start input
startText = ""

# data structure init--robot A
generated_responses_A = []
past_user_inputs_A = []
test_A = startText

# data structure init--robot B
generated_responses_B = []
past_user_inputs_B = []
test_B = ""

# req--robot A
myobj_A = {"inputs":{"generated_responses":generated_responses_A,"past_user_inputs":past_user_inputs_A,"text":test_A}}
# req--robot B
myobj_B = {"inputs":{"generated_responses":generated_responses_B,"past_user_inputs":past_user_inputs_B,"text":test_B}}

# Start talking
for i in range(postround):

    if i%2 == 0:
        x = requests.post(url, json = myobj_A, headers=headers)
        res = x.json()
        print("{:02d}".format(i), "A: ", res["generated_text"])
        gen_res = res["generated_text"]
        past_user_inputs_A.append(myobj_A["inputs"]["text"])
        generated_responses_A.append(gen_res)

        myobj_B["inputs"]["text"] = gen_res
          
    else:
        x = requests.post(url, json = myobj_B, headers=headers)
        res = x.json()
        print("{:02d}".format(i), "B: ", res["generated_text"])
        gen_res = res["generated_text"]
        past_user_inputs_B.append(myobj_B["inputs"]["text"])
        generated_responses_B.append(gen_res)

        myobj_A["inputs"]["text"] = gen_res

# record
result = []
for x in range(talkround):
    result.append(["A:",past_user_inputs_A[x]])
    result.append(["B:",past_user_inputs_B[x]])

# write in csv
with open('botChatSelf.csv', 'w+', encoding='UTF8', newline='') as f:
    writer = csv.writer(f)
    for i in range(len(result)):
        writer.writerow([result[i]])
    f.close()




