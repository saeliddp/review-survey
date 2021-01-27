from v1.models import Product
from bs4 import BeautifulSoup


#max_name = [0, "none"]
#max_desc = [0, "none"]
#max_rev = [0, "none"]

"""
with open("v1/data.csv", "r", newline="") as fr:
    linereader = csv.reader(fr, quotechar="｜")
    for row in linereader:
        if len(row) != 5:
            print(str(count))
        count += 1
        
        

"""
def upload():
    count = 0
    with open("v1/data.txt", "r") as fr:
        lines = fr.readlines()

    while len(lines) > 0:
        count += 1
        curr_line = lines.pop(0)
        line_buf = []
        while curr_line != '\n' or len(line_buf) < 5:
            line_buf.append(curr_line)
            if len(lines) > 0:
                curr_line = lines.pop(0)
            else:
                break
        
        #print(line_buf[0])
        #print(line_buf[-1])
        #print()
        """
        if len(line_buf[0]) > max_name[0]:
            max_name[0] = len(line_buf[0])
            max_name[1] = line_buf[0]
        
        for rev in line_buf[-3:]:
            if len(rev) > max_rev[0]:
                max_rev[0] = len(rev)
                max_rev[1] = rev
        """
        #print(line_buf)
        desc = line_buf[1]
        for piece in line_buf[2:-3]:
            desc = desc + piece
        desc = BeautifulSoup(desc.strip()).text
        """
        if len(desc) > max_desc[0]:
            max_desc[0] = len(desc)
            max_desc[1] = desc
        """
        Product(name=BeautifulSoup(line_buf[0].strip()).text, description=desc.strip(), review1=line_buf[-3].strip(), review2=line_buf[-2].strip(), review3=line_buf[-1].strip()).save() 
        
    print(count)
#print(str(max_name))
#print(str(max_desc))
#print(str(max_rev))
