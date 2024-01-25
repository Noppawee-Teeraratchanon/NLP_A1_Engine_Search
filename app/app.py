from flask import Flask, render_template, request
import torch
import json
from numpy import dot
from numpy.linalg import norm
import torch.nn as nn

app = Flask(__name__)

# glove module
class Glove(nn.Module):
    
    def __init__(self, voc_size, emb_size):
        super(Glove, self).__init__()
        self.center_embedding  = nn.Embedding(voc_size, emb_size)
        self.outside_embedding = nn.Embedding(voc_size, emb_size)
        
        self.center_bias       = nn.Embedding(voc_size, 1) 
        self.outside_bias      = nn.Embedding(voc_size, 1)
    
    def forward(self, center, outside, coocs, weighting):
        center_embeds  = self.center_embedding(center) #(batch_size, 1, emb_size)
        outside_embeds = self.outside_embedding(outside) #(batch_size, 1, emb_size)
        
        center_bias    = self.center_bias(center).squeeze(1)
        target_bias    = self.outside_bias(outside).squeeze(1)
        
        inner_product  = outside_embeds.bmm(center_embeds.transpose(1, 2)).squeeze(2)
        #(batch_size, 1, emb_size) @ (batch_size, emb_size, 1) = (batch_size, 1, 1) = (batch_size, 1)
        
        # calculate loss
        loss = weighting * torch.pow(inner_product + center_bias + target_bias - coocs, 2)
        
        return torch.sum(loss)

def get_embed(model, word):
    with open('app/word2index_dict', 'r') as json_file:
        word2index = json.load(json_file) 

    id_tensor = torch.LongTensor([word2index[word]])
    v_embed = model.center_embedding(id_tensor)
    u_embed = model.outside_embedding(id_tensor) 
    word_embed = (v_embed + u_embed) / 2 
    x, y = word_embed[0][0].item(), word_embed[0][1].item()

    return x, y

# function for calculate cosine similarity
def cos_sim(a, b):
    cos_sim = dot(a, b)/(norm(a)*norm(b))
    return cos_sim

# function for printing 10 most similarity with word input
def similarity10(word_input):
    with open('app/vocabs_list', 'r') as json_file:
        vocabs = json.load(json_file) 

    model = torch.load('glove_model.pth')
    model.eval()
    try:
        if len(word_input.split()) == 1:
            word_emb = get_embed(model, word_input)
            data = []
            with open('app/harry-potter.txt') as file:
                for word in file:
                    data += word.split()
            similarity_dict = {}
            for a in data:
                if a in vocabs:
                    a_emb = get_embed(model, a)
                    value = cos_sim(word_emb, a_emb)
                    similarity_dict[a] = value
                else:
                    continue
            similarity_dict_sorted = sorted(similarity_dict.items(), key=lambda x: x[1], reverse=True)
            output = [f"{i+1}. {similarity_dict_sorted[i][0]} ({similarity_dict_sorted[i][1]:.4f})" for i in range(10)]
            return output
        else:
            return ["The system can search with 1 word only"]
    except:
        return ["The word is not in my corpus. Please enter a new word"]

@app.route('/', methods=['GET', 'POST'])
def index():
    search_query = None
    output = None
    
    if request.method == 'POST':
        search_query = request.form['search_query']
        output = similarity10(search_query)

    return render_template('index.html', search_query=search_query,output=output)

if __name__ == '__main__':
    app.run(debug=True)
