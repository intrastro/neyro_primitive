import requests
import math
import random

#some constants
#1 layer
Q_C = 1
Q_INTRO = 84
#2 layer
Q_CONNEC = 14
Q_HIDDEN = 11
#3 layer
Q_C_H = 11
Q_HEADER = 1


class neyro:
  #all that contains the connections with prev. level of neyro
  intr = list ()
  
  intr_w = []

  #some technical values
  summ_intr = 0
  summ_intr_w = 1
  intr = []
  intr_w = []
  
  #the meaning, that exactly this neyro contains
  #as summ composition of intr and intr_w
  extr = 0

  #initializing the neyro
  def __init__(self, intr_list, q_connec): 
    self.intr = [intr_list [0] for i in range (0, q_connec)]
    self.intr_w = [1 for i in range (0, q_connec)]

    #print (len (self.intr))
    #print (len (self.intr_w))

  def __str__(self):
    return str (self.extr)

  def edit_extr(self):
    #some summ of variables, than are contained here
    self.summ_intr = 0
    self.summ_intr_w = 0
    for i in range (0, len (self.intr)):
      self.summ_intr_w += self.intr_w [i]
      self.summ_intr += (self.intr [i] * self.intr_w [i])
    self.extr = self.summ_intr / self.summ_intr_w

  def hook(self, number):
    #hook function for debug
    self.summ_intr = 0
    for i in range (0, len (self.intr)):
      self.summ_intr = self.summ_intr +(self.intr [i] * self.intr_w [i])
      print ("hook says " + str (self.intr [i]))
      print ("hook says " + str (self.intr_w [i]))
      print ("hook says " + str (self.summ_intr))
      
    self.extr = self.summ_intr / len (self.intr)  

  def punish(self, delta):
    #Russian knut and pryanik :D
    for i in range (0, len (self.intr)):
      variating = (1/(1 + 2.71828**(-(delta)     * abs (self.intr_w [i] * self.intr [i] - (self.extr + delta)))) - 0.5)
      self.intr_w[i] -= variating

      #if (delta < 0):
      #  print (variating)
 
      
  
#Parsing part.   getting the texr with data  
url = "https://psv4.userapi.com/c834603/u285624510/docs/d8/629f35ade840/vtb.txt?extra=3gmX2TOmQDO6AYEkZlXWbIQ-bmT3vWBck61cX5k4edo89NfyximOhMQjXwzJrJa6J9jgATMtizNRDeKTf-q29IE-h8Wpqjy4O_9YF-eZoTf-dlxf-k_3Q70iD2N2TrS0b_cwMkmetw5K4iOa&dl=1"
r = requests.get(url)
t = r.text


lst = []
s = ""
flag = False

for i in t:
    if i == ";":
        if flag == False:
            flag = True
        else:
            flag = False                    
            lst.append(float(s))
            s = ""
    elif flag == True:
        s += i

      

summ_plus = 0
summ_minus = 0
q_plus = 0
q_minus = 0
for i in range (1, len (lst)):
    #print (str (lst [i]))
    if (round ((lst [i] - lst [i - 1]), 5) >= 0):
        summ_plus += round ((lst [i] - lst [i - 1]), 7)
        q_plus += 1
    elif (round ((lst [i] - lst [i - 1]), 5) < 0):    
        summ_minus += round ((lst [i] - lst [i - 1]), 7)
        q_minus += 1

print (str (summ_plus / q_plus))
print (str (summ_minus / q_minus))

plus_porog = 3 * summ_plus / q_plus
minus_porog = 3 * summ_minus / q_minus

i = 0
size_of_arr = len (lst) - 1
while i < size_of_arr:
    #print (str (i) + "  " + str (len (lst))+ "  " + str (size_of_arr))
    lst [i] = lst [i] - lst [i - 1]
    if not (round ((lst [i] - lst [i - 1]), 5) <= plus_porog and round ((lst [i] - lst [i - 1]), 5) >= minus_porog):
      del lst[i]
      size_of_arr = size_of_arr - 1
    i = i + 1  

print ("finished the parsing part")


#Beginning of neyropart. Creating neyrons

#Attention! When we initialize some neyro, 2nd argument, a list is not completely used, only 1st symbol
neyro_intr_layer = [neyro ([0], Q_C) for i in range(Q_INTRO)]
neyro_hidden_layer = [neyro ([0], Q_CONNEC) for i in range(Q_HIDDEN)]
neyro_header_layer = [neyro ([0], Q_C_H) for i in range(Q_HEADER)]
print ("neyrons created")

#The teaching part
for o in range (0, 100):
    for i in range (0, (len (lst) - Q_INTRO) - 1, Q_INTRO):
        #1st layer
        for y in range (0, Q_INTRO):
            for z in range (0, Q_C): 
              (neyro_intr_layer [y]).intr[z] = lst [i + y]
            (neyro_intr_layer [y]).edit_extr ()

        #2nd layer   
        for y in range (0, Q_HIDDEN):
            for z in range (0, Q_CONNEC):
              #print (str (7 * y + z) + "   " + str (Q_INTRO) + "   " + str (len ((neyro_hidden_layer[y]).intr)))
              (neyro_hidden_layer[y]).intr[z] = (neyro_intr_layer [7 * y + z]).extr
            (neyro_hidden_layer[y]).edit_extr ()

        #3rd layer
        for y in range (0, Q_HEADER):
            for z in range (0, Q_C_H):     
              (neyro_header_layer[y]).intr[z] = (neyro_hidden_layer [z]).extr
            (neyro_header_layer[y]).edit_extr ()

        #de-facto output the header state
        #print ((neyro_header_layer[y]))

        #learning - marking
        t = 0
        if ((neyro_header_layer[t].extr) > (lst [i + Q_INTRO - 1] * 1.00005)):
          delta = neyro_header_layer[y].extr - lst [i + Q_INTRO - 1]
          for y in range (0, Q_HEADER):
              (neyro_header_layer[y]).punish (delta)
          
          for y in range (0, Q_HIDDEN):
              (neyro_hidden_layer[y]).punish (delta)     
              

        if ((neyro_header_layer[t].extr) < (lst [i + Q_INTRO - 1] * 0.99995)):
          delta = (neyro_header_layer[y].extr - lst [i + Q_INTRO - 1])
          for y in range (0, Q_HEADER):
              (neyro_header_layer[y]).punish (delta)
              
          for y in range (0, Q_HIDDEN):
              (neyro_hidden_layer[y]).punish (delta)     
      

        #clearing
        for y in range (0, Q_INTRO):
            (neyro_intr_layer [y]).summ_intr = 0
            for z in range (0, Q_C): 
              (neyro_intr_layer [y]).intr[z] = 0
            (neyro_intr_layer [y]).edit_extr ()

        #2nd layer   
        for y in range (0, Q_HIDDEN):
            (neyro_hidden_layer [y]).summ_intr = 0
            for z in range (0, Q_CONNEC):
              #print (str (7 * y + z) + "   " + str (Q_INTRO) + "   " + str (len ((neyro_hidden_layer[y]).intr)))
              (neyro_hidden_layer[y]).intr[z] = 0
            (neyro_hidden_layer[y]).edit_extr ()

        #3rd layer
        for y in range (0, Q_HEADER):
            (neyro_header_layer [y]).summ_intr = 0
            for z in range (0, Q_C_H):     
              (neyro_header_layer[y]).intr[z] = 0
            (neyro_header_layer[y]).edit_extr ()



#____TEST_PART_____

test_lst =  [1 for i in range (0, 84)]
test_lst [80] = 0

for o in range (0, 84):
  for y in range (0, Q_INTRO):
    for z in range (0, Q_C): 
      (neyro_intr_layer [y]).intr[0] = test_lst [y]
    
    (neyro_intr_layer [y]).edit_extr ()
      
  #print (str (neyro_intr_layer [10]))

    #2nd layer   
  for y in range (0, Q_HIDDEN):
    for z in range (0, Q_CONNEC):
      #print (str (7 * y + z) + "   " + str (Q_INTRO) + "   " + str (len ((neyro_hidden_layer[y]).intr)))
      (neyro_hidden_layer[y]).intr[z] = (neyro_intr_layer [7 * y + z]).extr
    (neyro_hidden_layer[y]).edit_extr ()

          #3rd layer
  for y in range (0, Q_HEADER):
    for z in range (0, Q_C_H):     
      (neyro_header_layer[y]).intr[z] = (neyro_hidden_layer [z]).extr
    (neyro_header_layer[y]).edit_extr ()

    #edit
  for y in range (0, 83):
    test_lst [y] = test_lst [y + 1]

  test_lst [83] = neyro_header_layer[0].extr



  #print ("__________________________")


    #clearing
  for y in range (0, Q_INTRO):
      (neyro_intr_layer [y]).summ_intr = 0
      for z in range (0, Q_C):
        (neyro_intr_layer [y]).intr[z] = 0
      (neyro_intr_layer [y]).edit_extr ()

        #2nd layer   
  for y in range (0, Q_HIDDEN):
      (neyro_hidden_layer [y]).summ_intr = 0
      for z in range (0, Q_CONNEC):
        #print (str (7 * y + z) + "   " + str (Q_INTRO) + "   " + str (len ((neyro_hidden_layer[y]).intr)))
        (neyro_hidden_layer[y]).intr[z] = 0
      (neyro_hidden_layer[y]).edit_extr ()

        #3rd layer
  for y in range (0, Q_HEADER):
      (neyro_header_layer [y]).summ_intr = 0
      for z in range (0, Q_C_H):     
        (neyro_header_layer[y]).intr[z] = 0
      (neyro_header_layer[y]).edit_extr ()

  #print (test_lst)
  #print ("___________________")

print (test_lst)
print ("___________________")





    













