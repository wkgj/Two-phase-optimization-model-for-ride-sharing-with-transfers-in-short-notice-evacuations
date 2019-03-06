# -*- coding: utf-8 -*-
"""
Created on Fri Mar 23 11:19:54 2018

@author: HUGUO
"""

from __future__ import print_function
import timeit
start_run_time = timeit.default_timer()
from gams import *
import os
import sys
import networkx as nx
import numpy as np
import xlrd
import pandas as pd
import matplotlib.pyplot as plt
from random import randint
#node = xlrd.open_workbook('C:/Users/HUGUO/Desktop/ChicagoSketch/node.xlsx')

node=pd.read_excel('C:/Users/HUGUO/Desktop/ChicagoSketch/node.xlsx')
link=pd.read_excel('C:/Users/HUGUO/Desktop/ChicagoSketch/link.xlsx')

node_ID=list(node['node'])
node_X=dict(zip(node_ID,list(node['X'])))
node_Y=dict(zip(node_ID,list(node['Y'])))

#node_left=709
#------------------------------------------------------
node_left=720
node_right=660
papameter_transfer=3;   #punishment parameter

park_time=2;

tolerance_value=0
veh_capacity=0


evacuation_veh_n=30
evacuation_p_n=12

#-------------------------------------------------------
link_st=list(link['tail node'])
link_end=list(link['head node'])
link_t=list(link['fftt(min)'])

G=nx.Graph()
G.add_nodes_from(node_ID)


for i in range(0,len(link_st)):
     G.add_edges_from([(link_st[i],link_end[i])])
     G[link_st[i]][link_end[i]]['weight'] =int(link_t[i]+1)  
#G.add_edges_from([(9+100,9),(10,10+100),(1+100,1),(3,3+100),(4+100,4),(2,2+100),(14,5),(11,15),(1,12),(1,5),(12,8),(12,6),(4,5),(5,6),(6,7),(7,8),(4,9),(5,9),(6,10),(7,11),(8,2),(9,10),(10,11),(11,2),(9,13),(11,3),(13,3)])

print(G[link_st[i]][link_end[i]]['weight'])
print(G[388][390]['weight'])

##----------------------draw this network
plt.figure(num=None, figsize=(32, 24))
draw_flag=1

if draw_flag==1:
  for edge in G.edges():
    n1=edge[0]
    n2=edge[1]
    plt.plot([node_X[n1],node_X[n2]],[node_Y[n1],node_Y[n2]],color='b')
#    plt.text(node_X[n1],node_Y[n1],str(n1))

plt.savefig("C:/Users/HUGUO/Desktop/result/ChicagoSketch.png")
plt.show()



##---------------          function to produce  dummy node and link

start=[];
end_node=[]

def dum_node(person,start_node,end_node,early,last,G):
    
    global G_update
    G_update=G
    if person>0:
       dum_st=int(str(person)+str('000')+str(start_node))
       dum_end=int(str(person)+str('000')+str(end_node))
    else:
       dum_st=int(str(-1*person)+str('01000')+str(start_node))
       dum_end=int(str(-1*person)+str('01000')+str(end_node)) 
    
    G_update.add_nodes_from([dum_st,start_node])
    G_update.add_nodes_from([end_node,dum_end])
#    print([dum_st,dum_end])
    G.add_edges_from([(dum_st,start_node)])
    G.add_edges_from([(end_node,dum_end)]) 
    
    G[dum_st][start_node]['weight']=0
    G[end_node][dum_end]['weight']=0
    
    print('kkkkkkkkkkkkkkkkkkkkkkkkkk')
    
    global Earliest_departure_time_set; 
    global Latest_arrival_time_set;
    global pick_up_set;
    global drop_off_set;  
    global veh_in;
    global veh_out;
    global passager;

    
    
    
    
    try:
       Earliest_departure_time_set.append(early)
       Latest_arrival_time_set.append(last)
       pick_up_set.append(dum_st)
       drop_off_set.append(dum_end)
    
       if person >0:
               veh_in.append(person)
               veh_out.append(person)
               passager.append(person)
       else:
               veh_in.append(0)
               veh_out.append(0)
               passager.append(person)        
    except NameError:    
       Earliest_departure_time_set=[early] 
       Latest_arrival_time_set=[last] 
       pick_up_set=[dum_st] 
       drop_off_set=[dum_end]   
       if person >0:
               veh_in=[person]
               veh_out=[person]
               passager=[person]
       else:
               veh_in=[0]
               veh_out=[0]
               passager=[person]
    
  
    return G_update,dum_st,dum_end
 



dum_end_time=range(0,1001);

    
infmat={}
                            # 
od={};
tw={};
veh=[0];
cap={};
cap[0]=1000
tolerance ={}



K_path_number=1

infmat[1]=[388,735,0,1000,5,20,3,0.5]   
infmat[-1]=[708,732,0,1000,0,20] 
infmat[-2]=[913,417,0,1000,0,30]    
infmat[2]=[890,607,0,1000,5,20,3,0.5]  
infmat[3]=[620,722,0,1000,5,20,3,0.5]  
#infmat[4]=[777,802,0,1000,5,20,3,0.5]  
#infmat[5]=[767,802,0,1000,5,20,3,0.5]  
#infmat[6]=[543,328,0,1000,5,20,3,0.5]  

evacuation_orgin=[]
evacuation_dest=[]

for no in node_ID[388:len(node_ID)]:
    if (node_X[no]<=node_X[node_left]):# and(node_Y[no]>=node_Y[node_left]):
       evacuation_dest.append(no)
    elif (node_X[no]>=node_X[node_right]) and(node_Y[no]<=node_Y[node_right]):
       evacuation_orgin.append(no)
       

select_driver_or={}
select_driver_dest={}
select_dest=[]

select_rider_or={}
select_rider_dest={}
select_p_orgin=[] 
      
for i in range(1,evacuation_veh_n+1):
       ev_or=evacuation_orgin[randint(0, len(evacuation_orgin)-1)]
       ev_de=evacuation_dest[randint(0, len(evacuation_dest)-1)]
       tolerance_value=randint(0,5)/100
       veh_capacity=randint(2,4)
       infmat[i]=[round(ev_or),round(ev_de),0,1000,randint(0,5),randint(10,15),veh_capacity,tolerance_value]  
#       distance=nx.shortest_path_length(G,source=ev_or,target=ev_de, weight='weight')
       
#       infmat[i]=[round(ev_or),round(ev_de),0,1000,randint(0,5),randint(round(distance),round(distance)+10),3,tolerance_value] 
       
       select_driver_or[i]=ev_or
       select_driver_dest[i]=ev_de
       select_dest.append(ev_de)
for i in range (1,evacuation_p_n+1):
       ev_or=evacuation_orgin[randint(0, len(evacuation_orgin)-1)]
       ev_de=select_dest[randint(0, len(select_dest)-1)]
       infmat[i*(-1)]=[ev_or,ev_de,0,1000,randint(0,5),randint(10,20)]  
       
#-----------------------[randint(0,5),randint(15,25)] departutr time window
#       distance=nx.shortest_path_length(G,source=ev_or,target=ev_de, weight='weight')       
#       infmat[i*(-1)]=[ev_or,ev_de,0,1000,randint(0,20),randint(round(distance),round(distance)+30)]  
       select_rider_or[i*(-1)]=ev_or
       select_rider_dest[i*(-1)]=ev_de     
       select_p_orgin.append(ev_or)
       
 

Earliest_departure_time_set=[]; 
Latest_arrival_time_set=[];
pick_up_set=[];
drop_off_set=[];  
veh_in=[];
veh_out=[];
passager=[];
rider=[];
driver=[];
veh=[0];
G_update=G;   
   
for  p in infmat.keys():
    (G_update,dum_st,dum_end)= dum_node(p,infmat[p][0],infmat[p][1],infmat[p][2],infmat[p][3],G)
 
    
#-----------------------------caculate all node-space vextex
    
     # start window  arange[strat_1，start_2，step]
    if p>0:
       veh.append(p);
       cap[p]=infmat[p][6]
       driver.append(p)
       od[p]=[dum_st,dum_end]
       tw[p]=np.arange(infmat[p][4],infmat[p][5],1)
       tolerance[p]=infmat[p][7]

    else:
       rider.append(p)      
       
G= G_update


#-------------------------------------------------------------------------------------show a figure for  riders' and drivers' information
plt.figure(num=822, figsize=(32, 24))
draw_flag=0
if  draw_flag==1:
    for edge in G.edges():
        n1=edge[0]
        n2=edge[1]
        if  (n1<=1000000) and (n2<=1000000):
            plt.plot([node_X[n1],node_X[n2]],[node_Y[n1],node_Y[n2]],color='b')
    for i in select_rider_or.keys():
        
        plt.text(node_X[select_rider_or[i]],node_Y[select_rider_or[i]],str(i),color='g')
        plt.text(node_X[select_rider_dest[i]],node_Y[select_rider_dest[i]],str(i),color='g')
    for i in select_driver_or.keys():
        
        plt.text(node_X[select_driver_or[i]],node_Y[select_driver_or[i]],str(i),color='r')
        plt.text(node_X[select_driver_dest[i]],node_Y[select_driver_dest[i]],str(i),color='r')
        
#    plt.text(node_X[n1],node_Y[n1],str(n1))

    plt.savefig("C:/Users/HUGUO/Desktop/My paper/person_information_result.png")
    plt.show()
    
    


#-----------------------------caculate the basic information of each person
p_dir={};

for i in range(0,len(passager)):
    test=[]
    test=[veh_in[i],veh_out[i],pick_up_set[i],drop_off_set[i],Earliest_departure_time_set[i],Latest_arrival_time_set[i]]
    p_dir[passager[i]]=test
    



#----------------------------------function for K shorest path 
from itertools import islice
def k_shortest_paths(G, source, target, k, weight=None):
     return list(islice(nx.shortest_simple_paths(G, source, target, weight=weight), k))
#for path in k_shortest_paths(G, 0, 3, 2):
#...     print(path)
#-----------------------------caculate the shortest path in each od pair


path_set=[];
for k in od.keys():
    path=nx.shortest_path(G,source=od[k][0],target=od[k][1],weight='weight')
    path_set.append(path)
    distance=nx.shortest_path_length(G,source=od[k][0],target=od[k][1], weight='weight')
    if distance>=1000:
        print(' distance>=1000 seconds')
        update_p=passager.index(k)
        latest_arrival_time_set[update_p]=distance+100
    print(path[0])
    
    
    

path_set={};

for k in od.keys():
#    path_set[k]=k_shortest_paths(G,od[k][0],od[k][1],K_path_number)
    path_set[k]=[nx.shortest_path(G,od[k][0],od[k][1],weight='weight')]
    
      
    for  detour_node in select_p_orgin:
         path_pre=nx.shortest_path(G,source=od[k][0],target=detour_node, weight='weight')
         path_lat=nx.shortest_path(G,source=detour_node,target=od[k][1], weight='weight')
         detour_path=[]  
         detour_path=path_pre+path_lat[1:len(path_lat)]
         path_set[k].append(detour_path)
         
             
    
    path=path_set[k][0]
    distance0=0
    for n in range(1,len(path)): 
          
        distance0= distance0+G[path[n-1]][path[n]]['weight']    
        
    print('_____________')
    print(distance0)
    print('**************')  
    path_remove_list=[]
    tolerance[k]=infmat[k][7]
    for path in path_set[k][1:len(path_set[k])]:
        distance=0
        
        for n in range(1,len(path)): 
            distance= distance+G[path[n-1]][path[n]]['weight']  
        print(distance)
        if distance>=distance0*(1+tolerance[k]):
            path_remove_list.append(path)
 
    for path in  path_remove_list:
        path_set[k].remove(path)
        
     
#        print(distance0)
#        print('oooooooooooooooooooooo')
#        print(distance)

#-----------------------------------------------------

time_path_set=[];
test=[0,0,0,0,0]
for p in path_set.keys():
    
    paths=path_set[p]
    
    time_window_v=tw[p].tolist()
    
    for path in  paths: 
    
        time_path=[0]*len(path)
        
        for n in range(1,len(path)):   # n is the vehicle number
            
          for t in time_window_v:
            test=[0,0,0,0,0]
            time_path[n]= time_path[n-1]+G[path[n-1]][path[n]]['weight']
            
            test[0]=p
            test[1]=path[n-1]
            test[2]=path[n]
            
            test[3]=time_path[n-1]+round(t,2)
            test[4]=time_path[n]+round(t,2)
            
            time_path_set.append(test)





vehicle_space_time=[[],[]];   # [[starts],[ends]]
intermediate_veh_s_t_vex=[];
veh_s_t_vex=[];

#vehicle_space_time=[]
test0=[0,0,0]
test1=[0,0,0]

for tp in time_path_set:
    test0=[0,0,0]
    test1=[0,0,0]
    
    test0[0]=tp[0]
    test0[1]=tp[1] 
    test0[2]=tp[3] 
    
    test1[0]=tp[0]
    test1[1]=tp[2] 
    test1[2]=tp[4]
    
    vehicle_space_time[0].append(test0)
    vehicle_space_time[1].append(test1)
    
    veh_s_t_vex.append(test0)
    veh_s_t_vex.append(test1)
    
#    if test0[1]not in[5,11]:
    if  (test0[1] not in pick_up_set) and (test0[2] not in Earliest_departure_time_set):
        intermediate_veh_s_t_vex.append(test0)
#   if test1[1]not in[5,11]: 
    if  (test1[1] not in drop_off_set) and (test1[2] not in Latest_arrival_time_set):  
        intermediate_veh_s_t_vex.append(test1)

##------------------------------------------------------------->
##------------------------------------------------------------->  


orgin_vex=[];
destination_vex=[];


for  indata in range(0,len(veh_in)): 
    
    Earliest_departure_time=Earliest_departure_time_set[indata]
    Latest_arrival_time=Latest_arrival_time_set[indata]
    pick_up=pick_up_set[indata]
    drop_off=drop_off_set[indata]
    v_in=veh_in[indata]
    v_out=veh_out[indata]
    
    
    vehicle_space_time[0].append([v_in,pick_up,Earliest_departure_time])
    vehicle_space_time[0].append([v_out,drop_off,Latest_arrival_time])

    vehicle_space_time[1].append([v_in,pick_up,Earliest_departure_time])   
    vehicle_space_time[1].append([v_out,drop_off,Latest_arrival_time])    

    veh_s_t_vex.append([v_in,pick_up,Earliest_departure_time])
    veh_s_t_vex.append([v_out,drop_off,Latest_arrival_time])
    
    orgin_vex.append([passager[indata],v_in,pick_up,Earliest_departure_time])
    destination_vex.append([passager[indata],v_out,drop_off,Latest_arrival_time])
    
c=[]

#for vex_s in veh_s_t_vex[0:(len(veh_s_t_vex)-1)]:
#    for vex_e in veh_s_t_vex[1:len(veh_s_t_vex)]:
        
for vex_s in vehicle_space_time[0]:
    for vex_e in vehicle_space_time[1]:       
    
       start=vex_s[1]
       ends=vex_e[1]
       
       
       if [vex_s[1],vex_e[1]] in G.edges:
           
#           if(vex_s[1] in pick_up_set) or (vex_e[1] in drop_off_set):
#               print([vex_s[1],vex_e[1]])
           
#(vex_e[2]-vex_s[2])>0 and
           
           ##
           ##          >=
           ##          ==
           
           
           
           if  ((vex_s[1] not in pick_up_set) and (vex_e[1] not in drop_off_set)) and((vex_e[2]-vex_s[2])<= (G[start][ends]['weight']+park_time)) and ((vex_e[2]-vex_s[2])>= (G[start][ends]['weight'])):
               test=[vex_s[0],vex_e[0],start,ends,vex_s[2],vex_e[2]] 
               c.append(test)
              
           if (vex_s[1] in pick_up_set) and((vex_e[2]-vex_s[2])>0): 
               
               location=pick_up_set.index(vex_s[1])
               test=[vex_s[0],vex_e[0],start,ends,Earliest_departure_time_set[location],vex_e[2]] 
               c.append(test)
               
           if (vex_e[1] in drop_off_set) and((vex_e[2]-vex_s[2])>0): 
               location=drop_off_set.index(vex_e[1])
               test=[vex_s[0],vex_e[0],start,ends,vex_s[2],Latest_arrival_time_set[location]] 
               c.append(test)           

def para_str(list0,list0_name):      # list into a parameter in Gams
    str_space=''
    str1=''
    try:

       for num in range(0,len(list0)):    
 #          print(list0[num])
           for dem in range(0,len(list0[num])):
              
              str1=str1+'\''+str(list0[num][dem]) +'\',' 
              
               
           str1=list0_name+'(' +str1[0:(len(str1)-2)]+'\')='+str(round(list0[num][5]-list0[num][4],2))+';\n' 
               
           str_space=str_space+str1    
           str1=''
    except TypeError or IndexError:
       print('error may be in len(list0[num]) or str(list0[num][dem])')
           
    return  str_space 


def c_cost_str(list0,list0_name,p_dir):      # list into a parameter in Gams
    str_space=''
    str1=''
    try:

       for num in range(0,len(list0)):    
 #          print(list0[num])
           for dem in range(0,len(list0[num])):
              
              str1=str1+'\''+str(list0[num][dem]) +'\',' 
              
           p_v=list0[num]
           
           if (p_dir[p_v[0]][3]==p_v[4]) and (p_dir[p_v[0]][2]==p_v[3]):
               cost=10000;

           elif (p_dir[p_v[0]][3]==p_v[4]) and (p_dir[p_v[0]][2]!=p_v[3]): 
               
               cost=0;
           elif (p_v[1]!=p_v[2]) and(p_v[1]!=0) and(p_v[2]!=0):
               cost=papameter_transfer*(list0[num][6]-list0[num][5]);    
           else:
               
               cost=list0[num][6]-list0[num][5];                         
            
           str1=list0_name+'(' +str1[0:(len(str1)-2)]+'\')='+str(round(cost,2))+';\n' 
               
           str_space=str_space+str1    
           str1=''
    except TypeError or IndexError:
       print('error may be in len(list0[num]) or str(list0[num][dem])')
           
    return  str_space 


def set_str(list0,list0_name):      # list into a Set in Gams
    str_space=''
    str1=''
    try:

       for num in range(0,len(list0)):
           
 #          print(list0[num])
           for dem in range(0,len(list0[num])):
              
              str1=str1+'\''+str(list0[num][dem]) +'\',' 
              
               
           str1=list0_name+'(' +str1[0:(len(str1)-2)]+'\')=1;\n' 
               
           str_space=str_space+str1    
           str1=''
    except TypeError or IndexError:
       print('error may be in len(list0[num]) or str(list0[num][dem])')
           
    return  str_space     

def delete_same_list(lis):
    
    lis_out=[]
    for i in lis:
        if i not in lis_out:
            lis_out.append(i)
    return lis_out



c=delete_same_list(c)

p_c=[];
for i in c:
    for p in passager:
        if (p<0) and (i[4]>=p_dir[p][4])and(i[5]<=p_dir[p][5]) and(i[2]<10000) and(i[3]<10000):

            test=[p]    
            p_c.append(test+i)
        elif(p<0)and((i[2]==p_dir[p][2])or(i[3]==p_dir[p][3])):
            test=[p]    
            p_c.append(test+i)
        elif (p>0) and(i[0]==i[1])and(i[0]==p):
            test=[p];
            p_c.append(test+i)


# add to virtual vehcile arcs             
for p in passager:
    if p<0:
        p_c.append([p]+p_dir[p]) 
        
        
        
driver_vehicle=[]
for p in passager:
    if p>0:
       test=[p] 
       driver_vehicle.append(test+[p_dir[p][0]])


c_cost=c_cost_str(p_c,'c',p_dir)
#c_cost=para_str(p_c,'c')
arcs_set=set_str(p_c,'arcs_set')
arcs_no_person=set_str(c,'arcs_no_person')
im_vex=set_str(intermediate_veh_s_t_vex,'im_vex')
or_vex=set_str(orgin_vex,'or_vex')
de_vex=set_str(destination_vex,'de_vex')
dr_veh=set_str(driver_vehicle,'dr_veh')




               
#c = list(set(c))      
print(path_set)
print(time_path) 

def domain_set(set_list,set_name,describe):  #set_name  and describe is  a string
    set_str='set '+set_name +' '+describe+' /';
    flag=0;
    for i in set_list:
        set_str=set_str+str(i)+','
        if i<=0:
            flag=1
        
    set_str=set_str[0:(len(set_str)-1)]+'/;'
    
    if flag==1:
       set_str=''
       set_str='set '+set_name +' '+describe+' /';
       for i in set_list:
            set_str=set_str+'\''+str(i)+'\''+','
            
       set_str=set_str[0:(len(set_str)-1)]+'/;'
         
    return set_str

def parameter_one_input(para_dir,set_name,para_name): #para_name is  a string
    
    para_str='parameter '+ para_name+'('+set_name+');'+'\n'
    for i in para_dir.keys():
        para_str=para_str+para_name+'(\''+str(i)+'\')='+str(para_dir[i])+';'+'\n'
    return para_str
    

i_str=domain_set(G.nodes(),'i','nodes')
s_str=domain_set(dum_end_time,'s','times')
v_str=domain_set(veh,'v','vehicle')
p_str=domain_set(passager,'p','passager')

cap_str=parameter_one_input(cap,'v','cap')

rider_str=domain_set(rider,'rider(p)','rider')
driver_str=domain_set(driver,'driver(p)','driver')


def print_txt(str0,str0_name):    # print cacualted Set，parameter and Table
    
    with open(str0_name+".txt","w") as f:
        f.write(str0)  
    f.close
    return 0

def get_data_text():
    Part_A=i_str+'\n'+s_str+'\n'+v_str+'\n'+p_str+'\n'+cap_str+'\n'
    print_txt(Part_A,'Part_A')
    return Part_A 

def get_model_text(c_cost,im_vex,arcs_set):
    Part_B= ''' 
set i ;
set s ;
set v ;
set p ;

parameter cap(v);

$if not set incname $abort 'no include file name for data file provided'
$include %incname%


Option MIP=cplex;
option limcol = 100;
option limrow = 100;


alias (i, j);
alias (s, t);
alias (v, u);

alias (i,ii);
alias (s,ss);
alias (v,vv);
alias (p,pp);


set im_vex(v,i,s)  intermediate;'''+'\n' +\
    im_vex+ '\n' +\
'''set arcs_set(p,v,u,i,j,s,t)  arcs_set;'''+'\n' +\
    arcs_set+ '\n' +\
'''parameter c(p,v,u,i,j,s,t);
'''+'\n' +\
    c_cost+ '\n' +\
'''set or_vex(p,v,i,s)  or_vex;'''+'\n' +\
    or_vex+ '\n' +\
'''set de_vex(p,v,i,s)  de_vex;'''+'\n' +\
    de_vex+ '\n' +\
'''set arcs_no_person(v,u,i,j,s,t)  arcs_no_person;'''+'\n' +\
    arcs_no_person+ '\n' +\
'''set dr_veh(p,v)  dr_veh;'''+'\n' +\
    dr_veh+ '\n' +\
    rider_str+'\n' +\
    driver_str+'\n' +\
'''

parameter relax_in(v,i,s) relax_in;
parameter relax_out(v,i,s) relax_out;
parameter c_update(p,v,u,i,j,s,t)  c update;

relax_in(v,i,s)=0;
relax_out(v,i,s)=0;

relax_in(v,i,s)$im_vex(v,i,s)=0;
relax_out(v,i,s)$im_vex(v,i,s)=0;




*-------------------------------------------------------------------------------LR model
variable z;
binary variable y(p,v,u,i,j,s,t)  ;

equations

obj                                   define objective function


flow_on_node_intermediate(p,v,i,s)   intermediate node flow on node i at time t

flow_on_node_origin(p,v,i,s)         origin node flow on node i at time t
flow_on_node_destination(p,v,i,s)      destination node flow on node i at time t


cap_in(v,i,s)   capacity in
cap_out(v,i,s)  capacity out

;


obj.. z =e=sum((p,v,u,i,j,s,t)$arcs_set(p,v,u,i,j,s,t), c(p,v,u,i,j,s,t)*y(p,v,u,i,j,s,t)$(arcs_set(p,v,u,i,j,s,t)))+sum((v,i,s)$(im_vex(v,i,s)),relax_in(v,i,s)*(sum((p,im_vex(u,j,t)),y(p,v,u,i,j,s,t)$arcs_set(p,v,u,i,j,s,t))-sum((pp,ii,ss),cap(v)*y(pp,v,v,i,ii,s,ss)$(arcs_set(pp,v,v,i,ii,s,ss)and dr_veh(pp,v)))))+sum((v,i,s)$(im_vex(v,i,s)),relax_out(v,i,s)*(sum((p,im_vex(u,j,t)),y(p,u,v,j,i,t,s)$arcs_set(p,u,v,j,i,t,s))-sum((pp,ii,ss),cap(v)*y(pp,v,v,ii,i,ss,s)$(arcs_set(pp,v,v,ii,i,ss,s)and dr_veh(pp,v)))));

flow_on_node_intermediate(p,v,i,s)$im_vex(v,i,s).. sum((u,j,t),y(p,v,u,i,j,s,t)$arcs_set(p,v,u,i,j,s,t))=e=sum((u,j,t),y(p,u,v,j,i,t,s)$arcs_set(p,u,v,j,i,t,s));
flow_on_node_origin(p,v,i,s)$or_vex(p,v,i,s).. sum((u,j,t),y(p,v,u,i,j,s,t)$arcs_set(p,v,u,i,j,s,t)$or_vex(p,v,i,s))=e=1;
flow_on_node_destination(p,v,i,s)$de_vex(p,v,i,s)..sum((u,j,t),y(p,u,v,j,i,t,s)$arcs_set(p,u,v,j,i,t,s))=e=1;


cap_out(v,i,s)$(im_vex(v,i,s))..sum((p,im_vex(u,j,t)),y(p,v,u,i,j,s,t)$arcs_set(p,v,u,i,j,s,t))=l=sum((pp,ii,ss),cap(v)*y(pp,v,v,i,ii,s,ss)$(arcs_set(pp,v,v,i,ii,s,ss)and dr_veh(pp,v)));
cap_in(v,i,s)$(im_vex(v,i,s))..sum((p,im_vex(u,j,t)),y(p,u,v,j,i,t,s)$arcs_set(p,u,v,j,i,t,s))=l=sum((pp,ii,ss),cap(v)*y(pp,v,v,ii,i,ss,s)$(arcs_set(pp,v,v,ii,i,ss,s)and dr_veh(pp,v)));


Model LR_optimization /obj,flow_on_node_intermediate,flow_on_node_origin,flow_on_node_destination/;
solve LR_optimization using MIP  minimizing z;


**----------------------------------------------------------------------------- iteration parameters
parameter z_lower_first, z_lower,z_upper,iter_n,lamda,lamda0,z_u,iter_upper;
z_lower_first=-100;
iter_n=1;
z_lower=-80;

z_upper=1000000;
lamda=2;
lamda0=2;

set flag /'w1'*'w600'/;
parameter ub(flag);
ub(flag)=0;

parameter lb(flag);
lb(flag)=0;



**------------------------------------------------------------------------------ gradient in LR
parameter  gradient_in(v,i,s);
parameter  gradient_out(u,j,t);

gradient_in(v,i,s)=-1;
gradient_out(u,j,t)=-1;



*-------------------------------------------------------------------------------feasiable total cost for riders and drivers respectively, and feasiable toatal cost of two 
parameter  z_rider_up,z_driver,z_feasiable;
z_rider_up=1000000;
z_driver=0;
z_feasiable=1000000;
09999999999999999999999990
**----------------------------------------------------------------------------- submodel for finding a feasiable soluation, opimize rider trips.
binary variable x(rider,v,u,i,j,s,t);
variable z_rider;
equations

rider_obj                                   define objective function

rider_flow_on_node_intermediate(rider,v,i,s)   intermediate node flow on node i at time t
rider_flow_on_node_origin(rider,v,i,s)         origin node flow on node i at time t
rider_flow_on_node_destination(rider,v,i,s)    destination node flow on node i at time t  
rider_capacity_into(v,i,s)                    capacity constarints
rider_capacity_out_to(v,i,s)                    capacity constarints;

rider_obj.. z_rider =e=sum((rider,v,u,i,j,s,t)$(arcs_set(rider,v,u,i,j,s,t) ), c(rider,v,u,i,j,s,t)*x(rider,v,u,i,j,s,t)$(arcs_set(rider,v,u,i,j,s,t)));
rider_flow_on_node_intermediate(rider,v,i,s)$im_vex(v,i,s).. sum((u,j,t),x(rider,v,u,i,j,s,t)$arcs_set(rider,v,u,i,j,s,t))=e=sum((u,j,t),x(rider,u,v,j,i,t,s)$arcs_set(rider,u,v,j,i,t,s));
rider_flow_on_node_origin(rider,v,i,s)$or_vex(rider,v,i,s).. sum((u,j,t),x(rider,v,u,i,j,s,t)$arcs_set(rider,v,u,i,j,s,t))=e=1;
rider_flow_on_node_destination(rider,v,i,s)$de_vex(rider,v,i,s)..sum((u,j,t),x(rider,u,v,j,i,t,s)$arcs_set(rider,u,v,j,i,t,s))=e=1;
rider_capacity_into(v,i,s)$im_vex(v,i,s).. sum((rider,u,j,t),x(rider,v,u,i,j,s,t)$arcs_set(rider,v,u,i,j,s,t))=l=sum((driver(p),u,j,t),(cap(u)-1)*y.l(driver,v,u,i,j,s,t));    
rider_capacity_out_to(v,i,s)$im_vex(v,i,s).. sum((rider,u,j,t),x(rider,u,v,j,i,t,s)$arcs_set(rider,u,v,j,i,t,s))=l=sum((driver(p),u,j,t),(cap(u)-1)*y.l(driver,u,v,j,i,t,s));   
Model optimization /rider_obj,rider_flow_on_node_intermediate,rider_flow_on_node_origin,rider_flow_on_node_destination,rider_capacity_into,rider_capacity_out_to/;
***----------------------------------------------------------------------------end submodel


***-----------------------------------------------------record soluation
binary variable result_opt(p,v,u,i,j,s,t);

***-----------------------------------------------------record vertexes and arcs
set  im_vex_2(v,i,s);
set  arcs_set_2(rider,v,u,i,j,s,t);
im_vex_2(v,i,s)=im_vex(v,i,s);
arcs_set_2(rider,v,u,i,j,s,t)=arcs_set(rider,v,u,i,j,s,t);


*-----------------------------------------------------iteration information
z_rider.l=1000000;
*iter_upper=80;

iter_upper=60;

parameter  repetition_number;
 
repetition_number=0;

while((iter_n<iter_upper),

    gradient_in(v,i,s)$(im_vex(v,i,s))= sum((p,im_vex(u,j,t)),y.l(p,v,u,i,j,s,t)$arcs_set(p,v,u,i,j,s,t))-sum((pp,ii,ss),(cap(v))*y.l(pp,v,v,i,ii,s,ss)$(arcs_set(pp,v,v,i,ii,s,ss)and dr_veh(pp,v))) ;
    gradient_out(u,j,t)$(im_vex(u,j,t))=sum((p,im_vex(v,i,s)),y.l(p,v,u,i,j,s,t)$arcs_set(p,v,u,i,j,s,t))-sum((pp,ii,ss),(cap(u))*y.l(pp,u,u,ii,j,ss,t)$(arcs_set(pp,u,u,ii,j,ss,t)and dr_veh(pp,u))) ;


**-------------------------------------------------------------------------    update mutit_piler
    relax_in(v,i,s)=max(0, relax_in(v,i,s)+lamda*gradient_in(v,i,s));
    relax_out(u,j,t)=max(0,relax_out(u,j,t)+lamda*gradient_out(u,j,t));




*   c_update(p,v,u,i,j,s,t)$arcs_set(p,v,u,i,j,s,t)=c(p,v,u,i,j,s,t)-cap(p)*(relax_in(v,i,s)$im_vex(v,i,s)+relax_out(u,j,t)$im_vex(u,j,t));
   
****----------------------------------------------------------------------------solve for drivers

****---------------y.l(p,v,u,i,j,s,t)=0;    
solve LR_optimization using MIP  minimizing z;
****----------------------------------------------------------------------------end


    z_u=sum((p,v,u,i,j,s,t), c(p,v,u,i,j,s,t)* y.l(p,v,u,i,j,s,t)$(arcs_set(p,v,u,i,j,s,t)));
    
    z_upper=min(z_u,z_upper);
    z_upper=min(z_feasiable,z_upper);


    ub(flag)$(ord(flag) eq iter_n)=z_upper;



    z_lower_first=z_lower;
    z_lower=z.l;



    lb(flag)$(ord(flag) eq iter_n)=z_lower;


    lamda=lamda0*(z_upper-z_lower)/(sum((v,i,s)$im_vex(v,i,s),sqr(gradient_in(v,i,s))) +sum((u,j,t)$im_vex(u,j,t),sqr(gradient_out(u,j,t))));

    iter_n=iter_n+1;
    
    
****----------------------------------------------------------------------------solve for riders

*im_vex(v,i,s)=0;
*arcs_set(rider,v,u,i,j,s,t)=0;


im_vex(v,i,s)$(sum((driver(p),im_vex_2(u,j,t)),y.l(driver,v,u,i,j,s,t)))=1$(im_vex_2(v,i,s));
im_vex(u,j,t)$(sum((driver(p),im_vex_2(v,i,s)),y.l(driver,v,u,i,j,s,t)))=1$(im_vex_2(u,j,t));



arcs_set(rider,v,u,i,j,s,t)$(im_vex(v,i,s) and im_vex(u,j,t))=arcs_set_2(rider,v,u,i,j,s,t);
arcs_set(rider,'0','0',i,j,s,t)=arcs_set_2(rider,'0','0',i,j,s,t);
arcs_set(rider,'0',u,i,j,s,t)$(im_vex(u,j,t))=arcs_set_2(rider,'0',u,i,j,s,t);
arcs_set(rider,v,'0',i,j,s,t)$(im_vex(v,i,s))=arcs_set_2(rider,v,'0',i,j,s,t);


*------------x.l(rider,v,u,i,j,s,t)=0;
solve optimization using MIP  minimizing z_rider;    
****----------------------------------------------------------------------------end   
****---------------------------------------------------------------------------return original im_vex, and  arcs_set 
im_vex(v,i,s)=im_vex_2(v,i,s);  
arcs_set(rider,v,u,i,j,s,t)=arcs_set_2(rider,v,u,i,j,s,t);  

****----------------------------------------------------------------------------record results   
if(z_rider_up>z_rider.l,
z_rider_up=z_rider.l;

result_opt.l(rider,v,u,i,j,s,t)=x.l(rider,v,u,i,j,s,t);
result_opt.l(driver,v,u,i,j,s,t)=y.l(driver,v,u,i,j,s,t);
z_driver=sum((driver,v,u,i,j,s,t)$arcs_set(driver,v,u,i,j,s,t), c(driver,v,u,i,j,s,t)*y.l(driver,v,u,i,j,s,t));

z_feasiable=z_rider_up+z_driver;
repetition_number=0;
)


if(z_rider_up<=z_rider.l,
repetition_number=repetition_number+1;
)

if(repetition_number>=10,
iter_n=1000;
)



)




display z_upper;
display ub;
display lb;
display result_opt.l;

''' 
    print_txt(Part_B,'Part_B')
    return Part_B

if len(sys.argv) > 1:
        ws = GamsWorkspace(system_directory = sys.argv[1])
else:
        ws = GamsWorkspace()
    
#    passagers=2
    
file = open(os.path.join(ws.working_directory, "tdata.gms"), "w")
file.write(get_data_text())
file.close()
    
t2 = ws.add_job_from_string(get_model_text(c_cost,im_vex,arcs_set))
opt = ws.add_options()

opt.defines["incname"] = "tdata"
    

t2.run(opt)


#----------------------------run time
stop_run_time = timeit.default_timer()
run_time=stop_run_time-start_run_time


#------------------------------output result
print('======================================')



for rec in t2.out_db["y"]:
        if (rec.level>0) and (int(rec.key(0))>0) and (int(rec.key(0))==1):
           print("y(" + rec.key(0) + "," + rec.key(1) +  "," + \
                 rec.key(2) +"," + rec.key(3)+ "," + rec.key(4)\
                 + ","+rec.key(5)+","+rec.key(6)+"): =" + str(rec.level) )

for rec in t2.out_db["x"]:
        if (rec.level>0) and(int(rec.key(0))==-6):
           print("x(" + rec.key(0) + "," + rec.key(1) +  "," + \
                 rec.key(2) +"," + rec.key(3)+ "," + rec.key(4)\
                 + ","+rec.key(5)+","+rec.key(6)+"): =" + str(rec.level) )
           
print('======================================')           
for rec in t2.out_db["result_opt"]:
        if (rec.level>0) and (int(rec.key(0))==10):
           print("result_opt(" + rec.key(0) + "," + rec.key(1) +  "," + \
                 rec.key(2) +"," + rec.key(3)+ "," + rec.key(4)\
                 + ","+rec.key(5)+","+rec.key(6)+"): =" + str(rec.level) )

for rec in t2.out_db["result_opt"]:
        if (rec.level>0) and(int(rec.key(0))==-9):
           print("result_opt(" + rec.key(0) + "," + rec.key(1) +  "," + \
                 rec.key(2) +"," + rec.key(3)+ "," + rec.key(4)\
                 + ","+rec.key(5)+","+rec.key(6)+"): =" + str(rec.level) )
           
print('======================================')
for rec in t2.out_db["z"]:
        print("The minimum cost：" +  str(rec.level) )




#--------------------------------  draw picture
##_------------------------------------------------------------------------------
#_-------------------------------------------------------------------------------       
import matplotlib.colors as colors
import matplotlib.patches as mpatches
import matplotlib.patches as patches


colors_list = list(colors._colors_full_map.values())




plt.figure(num=3, figsize=(20,max([6,round(len(driver)/3)])))

patch=[]


for rec in t2.out_db["y"]:
    if (rec.level>0) and(int(rec.key(0))>0):
        if len(rec.key(3))>=4:
           node_st=int(rec.key(3)[(len(rec.key(3))-3):len(rec.key(3))])
        else:
           node_st= int(rec.key(3))
           
        if len(rec.key(4))>=4:
           node_end=int(rec.key(4)[(len(rec.key(4))-3):len(rec.key(4))])
        else:
           node_end= int(rec.key(4))
           
        time_st=int(rec.key(5))
        time_end=int(rec.key(6))
        
#        plt.plot([time_st,time_end],[node_st,node_end],color=colors_list[person_plot])
        
        if int(rec.key(0))<0:
            person_plot=len(colors_list)+int(rec.key(0))
        else:
            person_plot=int(rec.key(0))
            
        
        plt.plot([time_st,time_end],[node_st,node_end],color=colors_list[person_plot])
        
        
for  person_plot in driver:       
    patch.append(mpatches.Patch(color=colors_list[person_plot], label='Vehicle'+str(person_plot)))        



plt.legend(handles=patch,loc=1)
plt.xlabel('Time', fontsize=18)
plt.ylabel('Node ID', fontsize=18)

plt.savefig("C:/Users/HUGUO/Desktop/My paper/LR_vehicle path.png")
#-------------------------------------------------------------------------------------
#-------------------------------------------------------------------------------------


fig9 = plt.figure(num=5,figsize=(20,max([6,round(len(driver)/3)])))
ax9 = plt.Axes(fig9, [0., 0., 1., 1.])
#x9 = plt.gca()
#ax9 = fig9.add_subplot(111, aspect='equal')
for rec in t2.out_db["x"]:
    if (rec.level>0) and(int(rec.key(0))<0):
        
  
        if len(rec.key(3))>=4:
           node_st=int(rec.key(3)[(len(rec.key(3))-3):len(rec.key(3))])
        else:
           node_st= int(rec.key(3))
           
        if len(rec.key(4))>=4:
           node_end=int(rec.key(4)[(len(rec.key(4))-3):len(rec.key(4))])
        else:
           node_end= int(rec.key(4))
           
        time_st=int(rec.key(5))
        time_end=int(rec.key(6))

        vehicle_pick=int(rec.key(1))
        
        if int(rec.key(2))==0:
            vehicle_pick=0
        
        
        
        rectangle_left_start_x=time_st
        rectangle_left_start_y=int(rec.key(0))*(-1)-0.3
        rectangle_length=time_end-time_st
        
        
        ax9.add_patch(patches.Rectangle((rectangle_left_start_x, rectangle_left_start_y), rectangle_length, 0.6, color=colors_list[vehicle_pick], linestyle='solid'  ))

fig9.add_axes(ax9)
plt.xlim([0, 1000])
plt.ylim([0, len(rider)+1])
plt.xlabel('Time', fontsize=18)
plt.ylabel('Rider ID', fontsize=18)
patch.append(mpatches.Patch(color=colors_list[0], label='Vehicle'+str('0')))
plt.legend(handles=patch,loc=1)

fig9.savefig('C:/Users/HUGUO/Desktop/My paper/LR_rect5.png', dpi=90, bbox_inches='tight')
fig9.show()


###-----------------------------save infmat

df = pd.DataFrame.from_dict(infmat, orient='index')
pd.DataFrame(df).to_csv('C:/Users/HUGUO/Desktop/My paper/LR_OUTPUT.csv')

########--------------------------------result analysis



#----------------------------------------------------------converage

ub=[]
lb=[]
for rec in t2.out_db["ub"]:
        #print("ub：" +  str(rec.value) )
        #print("ub：" +  str(rec) )
        ub.append(rec.value)
#print('======================================')

for rec in t2.out_db["lb"]:
        #print("lb：" +  str(rec.value) )
        lb.append(rec.value)


plt.figure(num=22, figsize=(20,max([round(len(ub)/3),6])))
plt.plot(ub,'b-')
plt.plot(lb,'r-')
plt.savefig("C:/Users/HUGUO/Desktop/My paper/LR_coverage.png")

#--------------------------------------------------------display optimal solution for each driver
plt.figure(num=23, figsize=(20,max([6,round(len(driver)/3)+2])))

patch=[]


for rec in t2.out_db["result_opt"]:
    if (rec.level>0) and(int(rec.key(0))>0):
        if len(rec.key(3))>=4:
           node_st=int(rec.key(3)[(len(rec.key(3))-3):len(rec.key(3))])
        else:
           node_st= int(rec.key(3))
           
        if len(rec.key(4))>=4:
           node_end=int(rec.key(4)[(len(rec.key(4))-3):len(rec.key(4))])
        else:
           node_end= int(rec.key(4))
           
        time_st=int(rec.key(5))
        time_end=int(rec.key(6))
        
#        plt.plot([time_st,time_end],[node_st,node_end],color=colors_list[person_plot])
        
        if int(rec.key(0))<0:
            person_plot=len(colors_list)+int(rec.key(0))
        else:
            person_plot=int(rec.key(0))
            
        
        plt.plot([time_st,time_end],[node_st,node_end],color=colors_list[person_plot])
        
        
for  person_plot in driver:       
    patch.append(mpatches.Patch(color=colors_list[person_plot], label='Vehicle'+str(person_plot)))        


plt.xlim([0, 300])
plt.legend(handles=patch,loc=1,prop={'size':14})
plt.xticks(fontsize=14)
plt.yticks(fontsize=14)
plt.xlabel('Time', fontsize=18)
plt.ylabel('Node ID', fontsize=18)

plt.savefig("C:/Users/HUGUO/Desktop/My paper/LR_Find_Feasiable_LR_vehicle path.png")

##--------------------------------------------------------display optimal solution for each rider
fig9 = plt.figure(num=26,figsize=(20,max([6,round(len(driver)/3)+5])))
ax9 = plt.Axes(fig9, [0., 0., 1., 1.])
#x9 = plt.gca()
#ax9 = fig9.add_subplot(111, aspect='equal')

for rec in t2.out_db["result_opt"]:
    if (rec.level>0) and(int(rec.key(0))<0):
        
  
        if len(rec.key(3))>=4:
           node_st=int(rec.key(3)[(len(rec.key(3))-3):len(rec.key(3))])
        else:
           node_st= int(rec.key(3))
           
        if len(rec.key(4))>=4:
           node_end=int(rec.key(4)[(len(rec.key(4))-3):len(rec.key(4))])
        else:
           node_end= int(rec.key(4))
           
        time_st=int(rec.key(5))
        time_end=int(rec.key(6))

        vehicle_pick=int(rec.key(1))
        
        if int(rec.key(2))==0:
            vehicle_pick=0
        
        
        
        rectangle_left_start_x=time_st
        rectangle_left_start_y=int(rec.key(0))*(-1)-0.3
        rectangle_length=time_end-time_st
        
        
        ax9.add_patch(patches.Rectangle((rectangle_left_start_x, rectangle_left_start_y), rectangle_length, 0.6, color=colors_list[vehicle_pick], linestyle='solid'  ))

fig9.add_axes(ax9)
plt.xlim([0, 300])
plt.ylim([0, len(rider)+1])
plt.xticks(fontsize=16)
plt.yticks(fontsize=16)
plt.xlabel('Time', fontsize=18)
plt.ylabel('Rider ID', fontsize=18)

patch.append(mpatches.Patch(color=colors_list[0], label='Vehicle'+str('0')))
plt.legend(handles=patch,loc=1,prop={'size':18})

fig9.savefig('C:/Users/HUGUO/Desktop/My paper/LR_Find_Feasiable_LR_rect5.png', dpi=90, bbox_inches='tight')
fig9.show()

##--------------------------------------------------------display optimal solution for each rider
fig9 = plt.figure(num=2226,figsize=(20,max([6,round(len(driver)/3)+2])))
ax9 = plt.Axes(fig9, [0., 0., 1., 1.])
#x9 = plt.gca()
#ax9 = fig9.add_subplot(111, aspect='equal')
patch=[]

for  person_plot in driver:       
    patch.append(mpatches.Patch(color=colors_list[person_plot], label='Vehicle'+str(person_plot)))        


for rec in t2.out_db["result_opt"]:
    if (rec.level>0) and(int(rec.key(0))<0):
        
  
        if len(rec.key(3))>=4:
           node_st=int(rec.key(3)[(len(rec.key(3))-3):len(rec.key(3))])
        else:
           node_st= int(rec.key(3))
           
        if len(rec.key(4))>=4:
           node_end=int(rec.key(4)[(len(rec.key(4))-3):len(rec.key(4))])
        else:
           node_end= int(rec.key(4))
           
        time_st=int(rec.key(5))
        time_end=int(rec.key(6))

        vehicle_pick=int(rec.key(1))
        vehicle_drop=int(rec.key(2))
        if int(rec.key(2))==0:
            vehicle_pick=0
        
        
        
        rectangle_left_start_x=time_st
        rectangle_left_start_y=int(rec.key(0))*(-1)-0.3
#        rectangle_length=time_end-time_st
        
        if (vehicle_pick!=vehicle_drop) and(vehicle_pick!=0):
            
            rectangle_length=G[node_st][node_end]['weight']    
            
            if (time_end-time_st)>rectangle_length:
                print('parking here')
                print(rec.key(0))
                print(time_end)
                print(time_end-time_st-rectangle_length)
        else:
            rectangle_length=time_end-time_st
        ax9.add_patch(patches.Rectangle((rectangle_left_start_x, rectangle_left_start_y), rectangle_length, 0.6, color=colors_list[vehicle_pick], linestyle='solid'  ))

fig9.add_axes(ax9)
plt.xlim([0, 300])
plt.ylim([0, len(rider)+1])
plt.xticks(fontsize=16)
plt.yticks(fontsize=16)
plt.xlabel('Time', fontsize=18)
plt.ylabel('Rider ID', fontsize=18)

patch.append(mpatches.Patch(color=colors_list[0], label='Vehicle'+str('0')))
plt.legend(handles=patch,loc=1,prop={'size':18})

fig9.savefig('C:/Users/HUGUO/Desktop/My paper/LR_Find_Feasiable_park_time.png', dpi=90, bbox_inches='tight')
fig9.show()

#---------------------output run_time
print('run time is :'+str(run_time))
