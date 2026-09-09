#MATPOTLIB:
from matplotlib import pyplot as pt

name=["SUMIT","SHAURYA","MANJIT","VINEET","RAVI"]
marks=[55,66,77,44,55]
pt.plot(name,marks)
pt.show()
______________________________________________________________________________________________
#With formatting
import matplotlib.pyplot as plt
x=[1,2,3,4,5]
y=[2,4,6,8,10]
plt.plot(x,y,color='red',linestyle='--',linewidth=2,marker='o')
plt.title('Basic Plot Line')
plt.xlabel('X Axis')
plt.ylabel('Y Axis')
plt.grid(True)
plt.show()

#line chart
x=[1,2,3,4,5]
y=[3,7,4,8,6]
plt.plot(x,y,marker='o')
plt.title('Line Chart Example')
plt.show()

#Multiple Line chart
x=[1,2,3,4,5]
y1=[2,4,6,8,10]
y2=[1,3,5,7,9]
plt.plot(x,y1,label='even',color='blue',linestyle='--',linewidth=2,marker='*')
plt.plot(x,y2,label='odd',color='green')

plt.legend()
plt.show()

#Bar Chart
categories=['A','B','C','D']
values=[10,20,15,25]
plt.bar(categories,values,color='orange')
plt.title('Bar Chart')
plt.show()
plt.barh(categories,values,color='purple')
plt.show()

#Pie Chart
sizes=[40,30,20,10]
labels=['Apple','Banana','Mango','Grapes']
plt.pie(sizes,labels=labels,autopct='%1.1f%%')
plt.title('Pie Chart')
plt.show()
import numpy as np

data=np.random.randn(1000)
plt.hist(data,bins=30,color='skyblue',edgecolor='black')
plt.title('Histograph')
plt.show()

#Scatter Plot
x=np.random.rand(50)
y=np.random.rand(50)
plt.scatter(x,y,color='red')
plt.title('Scatter Plot')
plt.show()

#Area Chart
x=[1,2,3,4]
y=[10,20,15,25]
plt.fill_between(x,y,color='lightblue')
plt.show()

#Stack Plot
x=[1,2,3,4]
y=[3,4,5,6]
y1=[2,2,3,3]
plt.stackplot(x,y,y1,labels=['A','B'])
plt.legend()
plt.show()

#Box Plot
data=[np.random.normal(0,1,100)for _ in range(4)]
plt.boxplot(data)
plt.title('Box Plot')
plt.show()

#violin plot
plt.violinplot(data)
plt.title('Violin Plot')
plt.show()

#Error Bar Chart
x=[1,2,3,4]
y=[5,7,6,8]
error=[0.5,0.3,0.4,0.2]
plt.errorbar(x,y,yerr=error,fmt='o')
plt.show()

#Multiple Chart in One figure(Subplots)
fig,ax=plt.subplots(2,2)
ax[0,0].plot([1,2,3],[4,5,6])
ax[0,1].bar(['A','B'],[3,7])
ax[1,0].scatter([1,2,3],[3,1,5])
ax[1,1].hist(np.random.randn(100))
plt.tight_layout()
plt.show()
