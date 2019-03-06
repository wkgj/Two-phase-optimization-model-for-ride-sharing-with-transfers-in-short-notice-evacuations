# -*- coding: utf-8 -*-
"""
Created on Fri Mar 23 11:19:54 2018

@author: HUGUO
"""
from __future__ import print_function
from gams import *
import os
import sys
import networkx as nx
import numpy as np
G = nx.DiGraph()
G.add_nodes_from(list(range(1,13))+[14,15]+[1+100,3+100,4+100,2+100])
G.add_edges_from([(1+100,1),(3,3+100),(4+100,4),(2,2+100),(14,5),(11,15),(1,12),(1,5),(12,8),(12,6),(4,5),(5,6),(6,7),(7,8),(4,9),(5,9),(6,10),(7,11),(8,2),(9,10),(10,11),(11,2),(9,13),(11,3),(13,3)])

for edge in G.edges():
    G[edge[0]][edge[1]]['weight'] =20  
    
    
G[12][8]['weight']=50
G[4][9]['weight']=30
G[9][13]['weight']=30

#> Virtual weight
G[14][5]['weight']=0
G[11][15]['weight']=0

G[1+100][1]['weight']=0
G[3][3+100]['weight']=0
G[4+100][4]['weight']=0
G[2][2+100]['weight']=0


#print(G.edges(data='weight'))   
print(G.edges)  


Earliest_departure_time_set=[0,0,0]; 
Latest_arrival_time_set=[100,100,100];

pick_up_set=[14,1+100,4+100];
drop_off_set=[15,3+100,2+100];  

veh_in=[0,1,2];
veh_out=[0,1,2];

passager=[1,-1,-2];

p_dir={};

for i in range(0,len(passager)):
    test=[]
    test=[veh_in[i],veh_out[i],pick_up_set[i],drop_off_set[i],Earliest_departure_time_set[i],Latest_arrival_time_set[i]]
    p_dir[passager[i]]=test
    
 
od=[[101,103],[104,102]];

path_set=[];
for k in od:
    path=nx.shortest_path(G,source=k[0],target=k[1])
    path_set.append(path)
    print(path)

tw=[np.arange(5,20,1),np.arange(10,20,1)];

vex_set=[] 
print(G[12][8]['weight'])

time_path_set=[];
test=[0,0,0,0,0]
for i in range(0,len(path_set)):
    
    path=path_set[i]
    
    time_window_v=tw[i].tolist()
    
    time_path=[0]*len(path)
    
    for n in range(1,len(path)):
        
      for t in time_window_v:
        test=[0,0,0,0,0]
        time_path[n]= time_path[n-1]+G[path[n-1]][path[n]]['weight']
        
        test[0]=i+1
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
           if  ((vex_s[1] not in pick_up_set) and (vex_e[1] not in drop_off_set)) and((vex_e[2]-vex_s[2])== G[start][ends]['weight']):
               test=[vex_s[0],vex_e[0],start,ends,vex_s[2],vex_e[2]] 
               c.append(test)
           if ((vex_s[1] in pick_up_set) or (vex_e[1] in drop_off_set)) and((vex_e[2]-vex_s[2])>= 0): 
               test=[vex_s[0],vex_e[0],start,ends,vex_s[2],vex_e[2]] 
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
def print_txt(str0,str0_name):    # print cacualted Set，parameter and Table
    
    with open(str0_name+".txt","w") as f:
        f.write(str0)  
    f.close
    return 0


p_c=[];
for i in c:
    for p in passager:
        if (p>0) and (i[4]>=p_dir[p][4])and(i[5]<=p_dir[p][5]):

            test=[p]    
            p_c.append(test+i)
        elif (p<0) and(i[0]==i[1])and(i[0]==(-1*p)):
            test=[p];
            p_c.append(test+i)
            

driver_vehicle=[]
for p in passager:
    if p<0:
       test=[p] 
       driver_vehicle.append(test+[p_dir[p][0]])

c_cost=para_str(p_c,'c')
arcs_set=set_str(p_c,'arcs_set')
arcs_no_person=set_str(c,'arcs_no_person')
im_vex=set_str(intermediate_veh_s_t_vex,'im_vex')
or_vex=set_str(orgin_vex,'or_vex')
de_vex=set_str(destination_vex,'de_vex')
dr_veh=set_str(driver_vehicle,'dr_veh')



               
#c = list(set(c))      
print(path_set)
print(time_path) 

def get_data_text():
    Part_A='''
set i nodes /1*15,101,102,103,104/;
set s times /0*110/;
set v vehicle /0*2/;
set p passenger /1,'-1','-2'/;
set po(i) source node /14/;
set pd(i) sink node /15/;

parameter cap(p);
cap('-1')=2;
cap('-2')=2;
 '''
    print_txt(Part_A,'Part_A')
    return Part_A 

def get_model_text(c_cost,im_vex,arcs_set):
    Part_B= ''' 
set i ;
set s ;
set v ;
set p ;
set po(i) ;
set pd(i) ;
parameter cap(p);

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
'''
set dr_veh(p,v)  dr_veh;
dr_veh('-1','1')=1;
dr_veh('-2','2')=1;




parameter relax_in(v,i,s) relax_in;
parameter relax_out(v,i,s) relax_out;


variable z;
binary variable y(p,v,u,i,j,s,t)  ;

equations

obj                                   define objective function


flow_on_node_intermediate(p,v,i,s)   intermediate node flow on node i at time t

flow_on_node_origin(p,v,i)         origin node flow on node i at time t
flow_on_node_destination(p,v,i)      destination node flow on node i at time t

cap_in(v,i,s)   capacity in
cap_out(v,i,s)  capacity out

;

obj.. z =e= sum((p,v,u,i,j,s,t), c(p,v,u,i,j,s,t)* y(p,v,u,i,j,s,t)$(arcs_set(p,v,u,i,j,s,t)));

flow_on_node_intermediate(p,v,i,s)$im_vex(v,i,s).. sum((u,j,t),y(p,v,u,i,j,s,t)$arcs_set(p,v,u,i,j,s,t))=e=sum((u,j,t),y(p,u,v,j,i,t,s)$arcs_set(p,u,v,j,i,t,s));

flow_on_node_origin(p,v,i)$sum(s,or_vex(p,v,i,s)).. sum((u,j,s,t),y(p,v,u,i,j,s,t)$arcs_set(p,v,u,i,j,s,t))=e=1;
flow_on_node_destination(p,v,i)$sum(s,de_vex(p,v,i,s))..sum((u,j,t,s),y(p,u,v,j,i,t,s)$arcs_set(p,u,v,j,i,t,s))=e=1;

cap_out(v,i,s)$(im_vex(v,i,s))..sum((p,im_vex(u,j,t)),y(p,v,u,i,j,s,t)$arcs_set(p,v,u,i,j,s,t))=l=sum((pp,ii,ss),cap(pp)*y(pp,v,v,i,ii,s,ss)$(arcs_set(pp,v,v,i,ii,s,ss)and dr_veh(pp,v)));
cap_in(v,i,s)$(im_vex(v,i,s))..sum((p,im_vex(u,j,t)),y(p,u,v,j,i,t,s)$arcs_set(p,u,v,j,i,t,s))=l=sum((pp,ii,ss),cap(pp)*y(pp,v,v,ii,i,ss,s)$(arcs_set(pp,v,v,ii,i,ss,s)and dr_veh(pp,v)));


Model customized_bueses_optimization /all/;

solve customized_bueses_optimization using MIP  minimizing z ;
display y.l;
display z.l;




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
print('======================================')
#    for rec in t2.out_db["space_time_state_str"]:
#           print("y(" + rec.key(0) + "," + rec.key(1) +  "," + \
#                 rec.key(2) +"," + rec.key(3)+ "," + rec.key(4)\
#                 + ","+rec.key(5)+"): =" + str(rec) )

print('======================================')
for rec in t2.out_db["y"]:
        if (rec.level>0):
           print("y(" + rec.key(0) + "," + rec.key(1) +  "," + \
                 rec.key(2) +"," + rec.key(3)+ "," + rec.key(4)\
                 + ","+rec.key(5)+","+rec.key(6)+"): =" + str(rec.level) )
           
print('======================================')
for rec in t2.out_db["z"]:
        print("The minimum cost：" +  str(rec.level) )