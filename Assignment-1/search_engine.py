#-------------------------------------------------------------------------
# AUTHOR: Isaiah Hessler
# FILENAME: Assignment-1
# SPECIFICATION: Complete the Python program (search_engine.py) that will read the file collection.csv and output the precision/recall of a proposed search engine given the query q = {cat and dogs}.
# FOR: CS 4250- Assignment #1
# TIME SPENT: 5 hours
#-----------------------------------------------------------*/

#IMPORTANT NOTE: DO NOT USE ANY ADVANCED PYTHON LIBRARY TO COMPLETE THIS CODE SUCH AS numpy OR pandas. You have to work here only with standard arrays

#importing some Python libraries
import csv
import math #for log10()

documents = []
labels = []
query = "cat and dog"

#reading the data in a csv file
with open('collection.csv', 'r') as csvfile:
  reader = csv.reader(csvfile)
  for i, row in enumerate(reader):
         if i > 0:  # skipping the header
            documents.append (row[0])
            labels.append(row[1])

#Conduct stopword removal.
stopWords = {'I ', 'and ', 'She ', 'They ', 'her ', 'their '}
for j in range(len(documents)):
    for i in stopWords:
      x = documents[j].replace(i, '')
      documents[j] = x
for i in stopWords:
   query = query.replace(i, '')
#print(documents)
#print(query)

#Conduct stemming.
stemming = {
  "cats": "cat",
  "dogs": "dog",
  "loves": "love",
}
for j in range(len(documents)):
    for i in stemming:
      x = documents[j].replace(i, stemming[i])
      documents[j] = x
for i in stemming:
   query = query.replace(i, stemming[i])
#print(documents)
#print(query)

#Identify the index terms.
terms = []
temp = []
count_values = []
for j in range(len(documents)):
  temp = documents[j].split()
  terms = terms + temp
count_values = terms
terms = list(set(terms))
terms.sort()
query = query.split()
temp.clear()
#print(query)
#print(terms)

#Build the tf-idf term weights matrix.
docMatrix = []
total = []
query_values = terms
for n in range(len(documents)):
   docMatrix.append([])
for j in range(len(documents)):
   temp = documents[j].split()
   for i in terms:
      x = 0
      docMatrix[j].append(temp.count(i))
      x += 1
   temp.clear()
for i in terms:
   x = 0
   total.append(count_values.count(i))
   x += 1
counter = 0
docNumber = []
for j in range(len(documents)):
   for i in range(len(documents)):
      if docMatrix[j][i] == 0:
          counter += 1
      docMatrix[j][i] = docMatrix[j][i]/total[i]
   docNumber.append(len(documents) - counter)
   counter = 0
for j in range(len(documents)):
   total[j] = math.log10(len(documents)/docNumber[j])
for j in range(len(documents)):
   for i in range(len(documents)):
      docMatrix[j][i] = docMatrix[j][i] * total[j]
for j in range(len(terms)):
   for i in range(len(query)):
      if query[i] == terms[j]:
         query_values[j] = 1
   if query_values[j] != 1:
      query_values[j] = 0

#print(docNumber)
#print(total)
#print(docMatrix)
#print(query_values)

#Calculate the document scores (ranking) using document weigths (tf-idf) calculated before and query weights (binary - have or not the term).
docScores = []
for j in range(len(documents)):
   temp_value = 0
   for i in range(len(documents)):
      temp_value = temp_value + (docMatrix[i][j] * query_values[i])
   docScores.append(temp_value)
#print(docScores)

#Calculate the precision and recall of the model by considering that the search engine will return all documents with scores >= 0.1.
hit, miss, noise, reject = 0, 0, 0, 0

for i in range(len(docScores)):
   #print(docScores[i])
   if docScores[i] >= 0.1:
      #print(labels[i])
      if labels[i] == 'R':
         hit += 1
      else:
         noise += 1
   else:
      if labels[i] == 'R':
         miss += 1
      else:
         reject += 1

recall = (hit/(hit + miss)) * 100
precision = (hit/(hit + noise)) * 100
print(f'Query: cat and dog')
print(f'Recall: {recall}%')
print(f'Precision: {precision}%')
