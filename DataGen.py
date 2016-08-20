import random

veg=['apple','beer','orange','rice','maple','wine','bread']
nonveg=['beef','chicken','egg','mutton','pork','duck','prawn']
c=['v','nv','ov']

def generate_set(itemset_file, classes_file, row_count):
    item_stream=open(itemset_file,"w")
    class_stream=open(classes_file,"w")
    for j in range(row_count):
        
        itemlist=[]
        c1=str(c[random.randint(0,len(c)-1)])
        itemcount=random.randint(1,7)
        if(c1=='v'):
                for i in range(itemcount):
                        itemlist.append(veg[random.randint(0,len(veg)-1)])
        elif(c1=='nv'):
                for i in range(itemcount):
                        itemlist.append(nonveg[random.randint(0,len(nonveg)-1)])
        else:
                #n1=random.randint(0,itemcount-1)
                for i in range(1+itemcount//2):
                        itemlist.append(veg[random.randint(0,len(veg)-1)])
                for i in range(1+itemcount//2):
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

def main(train_dataset_size , test_dataset_size):
    generate_set("Itemset_train.txt", "Classes_train.txt", train_dataset_size)
    generate_set("Itemset_test.txt", "Classes_test.txt",test_dataset_size)

if __name__ == "__main__":
    main(1500, 500)
