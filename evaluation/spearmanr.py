
# coding: utf-8

# In[20]:


from numpy.linalg import norm
from numpy import dot
from scipy.stats import spearmanr
import os
import sys
import numpy as np 


# In[ ]:


word_vector_model = sys.argv[1]
evaluate_data = sys.argv[2]


# In[21]:


#--------------------convert any array to float array---------
def convert_list_to_float(in_list):
    out_list = []
    for i in in_list:
        out_list.append(float(i))
    return  out_list


# In[22]:


#---------------read model.vec and create dictionery----------------

in_file = open(str(word_vector_model))
lines = in_file.read().split('\n')
word_dict = {} 
for line in lines:
    if line == '':
        continue
    line = line.split(' ')
    word_dict[line[0]] = np.array(convert_list_to_float(line[1:-1]))
in_file.close()


# In[26]:





# In[23]:


# def distance(v1, v2):
#     return (1-dot(v1,v2))
# #distance(word_dict['a'], word_dict['student.'])


# In[ ]:


#--------------------get similarty between 2 vectors (word1, word2)

def similarity(word1, word2):
    n1 = np.linalg.norm(np.array(word1))
    n2 = np.linalg.norm(np.array(word2))
    l = np.dot(np.array(word1), np.array(word2)) / (n1 * n2)
    return l


# In[ ]:


#---------------------sum vectors to calculate word vector from subwords-------------

def sum_of_vectors(vector_list):

    word_vector = vector_list[0]
    for i in range(1, len(vector_list)):
        word_vector = word_vector  + vector_list[i]
    return word_vector


# In[34]:


#-----------------------read evalate file and get words and humann judjments------------------

in_file = open(str(evaluate_data))
lines = in_file.read().split('\n')
raw_data = []
for line in lines:
    if line == "":
        continue
    line = line.split(';')
    raw_data.append(line[1:4])

in_file.close()


# In[30]:


#-----------------------calculate word spearman_original_list and spearman_target_list ----------
#------------------------ spearman_original_list calculate from words similarity ---------------

spearman_original_list = []
spearman_target_list = []
print("size of raw_data is ", len(raw_data))
for i in raw_data:
    try:
        spearman_original_list.append(similarity(word_dict[i[0]], word_dict[i[1]]))
        spearman_target_list.append(float(i[2]))
    except:
        pass
print("size of spearman_original_list is ", len(spearman_original_list))
print("size of spearman_target_list is ", len(spearman_target_list))


# In[35]:


#-------------------------calculate spearmanr with scipy module ---------------------

spearman_rho = spearmanr(spearman_target_list, spearman_original_list)
print("size of spearman_rho is ",round(spearman_rho[0], 3))