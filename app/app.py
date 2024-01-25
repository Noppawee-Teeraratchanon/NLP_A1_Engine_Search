from flask import Flask, render_template, request
import torch
import json

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])




# #let's write a function to get embedding given a word
# def get_embed(model,word):
#     with open('app/word2index_dict', 'r') as json_file:
#         word2index = json.load(json_file) 

#     id_tensor = torch.LongTensor([word2index[word]])
#     v_embed = model.center_embedding(id_tensor)
#     u_embed = model.outside_embedding(id_tensor) 
#     word_embed = (v_embed + u_embed) / 2 
#     x, y = word_embed[0][0].item(), word_embed[0][1].item()

#     return x, y

# from numpy import dot
# from numpy.linalg import norm

# def cos_sim(a, b):
#     cos_sim = dot(a, b)/(norm(a)*norm(b))
#     return cos_sim

# def similarity10(word_input):    
#     model = torch.load('glove_model_new.pth')
#     model.eval()
#     with open('app/vocabs_list', 'r') as json_file2:
#         vocabs = json.load(json_file2) 

#     try:
#         if len(word_input.split())==1:

#             word_emb=get_embed(model,word_input)
#             data=[]
#             with open('app/harry-potter.txt') as file:
#                 for word in file:
#                     data += word.split()
            
#             similarity_dict = {}
#             for a in data:
#                 if a in vocabs:
#                     a_emb = get_embed(model,a)
#                     value = cos_sim(word_emb,a_emb)
#                     similarity_dict[a] = value
#                 else:
#                     continue

#             similarity_dict_sorted = sorted(similarity_dict.items(), key=lambda x: x[1], reverse=True)
            
#             output = []
#             for i in range(10):
#                 output.append(similarity_dict_sorted[i][0])
            

#         else:
#             output = "the system can search with 1 word only"
                    
#     except:
#          output = "the word is not in my corpus. Please enter the new word"
#     return output

def index():
    search_query = None
    if request.method == 'POST':
        search_query = request.form['search_query']
        # output = similarity10(search_query)
        # for i in range(10):
        #     print(1,output[i])

  



    


    return render_template('index.html', search_query=search_query)

if __name__ == '__main__':
    app.run(debug=True)