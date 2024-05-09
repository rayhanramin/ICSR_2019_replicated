import google.generativeai as palm
import os
import pandas as pd
import numpy as np

#put the API key here
API_KEY = ""

palm.configure(api_key=API_KEY)

with open(os.path.join(os.getcwd(), 'shortlisted_requirements_browser.txt'), 'r') as f:
    df = pd.read_csv(f, delimiter='\t')


print("In total, we have", len(df) , "requirements!")

x = input("How many Large Language Model generated requirements you want to see? ")
y = []

for i in range(int(x)):
    y.append(np.random.choice(range(0, len(df)), replace=False))

print(y)

#for row in df.iterrows():
    #print(row[1])

reqs = df['New Requirements']
#print(reqs)

new_df = pd.DataFrame(columns= ['Given Requirements', 'AI generated requirements'])

for i in y:
    reply = palm.chat(messages=["Can you tell me if the following sentence is meaningful? {}  In any case, can you make it meaningful and give some more suggestion?".format(reqs[i])])
    print(reply.last)
    print('*********************************************')

#a= "The system shall provide user with ability to build advanced heuristic analysis malicious program."

#


#response = palm.generate_text(prompt="Can you tell me if the following sentence is meaningful? {}  In any case, can you make it meaningful and give some more suggestion?".format(a))
#print(response.result)
