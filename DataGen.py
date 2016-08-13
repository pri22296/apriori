import random

veg=['apple','beer','orange','rice','maple','wine','bread']
nonveg=['beef','chicken','egg','mutton','pork','duck','prawn']
c=['v','nv','ov']

def generate_set():
	item_stream=open("Itemset.txt","w")
	class_stream=open("Classes.txt","w")
	for j in range(100):
			
	
		itemlist=[]
		c1=str(c[random.randint(0,len(c)-1)])
		itemcount=random.randint(3,7)
		if(c1=='v'):
			for i in range(itemcount):
				itemlist.append(veg[random.randint(0,len(veg)-1)])
		elif(c1=='nv'):
			for i in range(itemcount):
				itemlist.append(nonveg[random.randint(0,len(nonveg)-1)])
		else:
			n1=random.randint(0,itemcount-1)
			for i in range(n1):
				itemlist.append(veg[random.randint(0,len(veg)-1)])
			for i in range(itemcount-n1):
				itemlist.append(nonveg[random.randint(0,len(nonveg)-1)])	
		itemlist=list(set(itemlist))		
		
		buffer=""
		for i in itemlist:
			buffer+=str(i)+","
		buffer=buffer.rstrip(',')		
		#buffer[len(buffer)-1]="\n"					
		item_stream.write(buffer+"\n")
		class_stream.write(c1+"\n")
	item_stream.close()
	class_stream.close()

generate_set()
