import requests

BASE='http://127.0.0.1:5000/'    #location of the api the server is running on.

data=[
    {'views':345,'name':'Messi','likes':345},
    {'views':32,'name':'Ronaldo','likes':13},
    {'views':194,'name':'Neymar','likes':99},
    {'views':542,'name':'Zlatan','likes':348}
]

for i in range(len(data)):
    response=requests.put(BASE+'video/'+str(i),data[i])
    print("response for put",i,': ',response.json()) 

    print((requests.get(BASE+'video/'+str(i)).json()))
    

input()
response=requests.get(BASE+'video/6')
print("response of get : ",response.json()) 

input()
response=requests.delete(BASE+'video/3')
print("response of delete : ",response) 

input()
response=requests.patch(BASE+'video/3',{'name':'Edinson Cavani','views':990})
print("response of update/patch : ",response.json()) 

