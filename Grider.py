print("")
print("This Programm had been created by Benoît de Keyn as part of an Algosup project")
print("")
print("")
print("")
print("It is used to convert a picture already pixelised, to as many sheets as wanted to provide to as many teams we want to be able to create their part of a rubik's cube art.")
print("")
print("I know it's very unclear, but in a nutshell, if you come from Algosup 2023-2024 year, you'll understand.")
print("")
print("So, You need a file which is the picture well dimensioned of your rubik's artwork, on which we can see the pixels of the fresco.")
print("")
print("Then, Let's go !")
print("")
print("")
print("")
print(" !!! If there is any problem !!!  it's mainly caused by a weird path with apostrophe or spaces for instance. \n Actually the better is to just copy your image into the folder where this executable is located, and just put  : \"picture.png\" for instance")
# Your image (ex : images/image.jpg or C:/Users/John/Pictures/picture.png)
image_path = input("\nYour image's path (ex : image.jpg or C:/Users/John/Pictures/picture.png)  : ")
print("")


# witdh an height in rubiks cubes of your pictures
print("Now, you have to give the dimensions of the fresco, by counting in rubik's cubes")
r_width = int(input("what is the width of the fresco (in number of rubik's cubes) : ")) #width in rubik's cubes
r_height = int(input("what is the height of the fresco (in number of rubik's cubes) : ")) #height in rubik's cubes
print("")

#settings of cutting the picture for the different teams
print("Finally, in order to divide the fresco equally between the different teams, you need to indicate how many columns and how many rows the image should be divided into (e.g. for 8 teams and a ratio of 1:3, an ideal division would be 4 columns and 2 rows ;) )")
columns = int(input("how many columns : "))
rows = int(input("how many rows : "))
print("")
print("Wait...")
print("")

f_border = 3 # facets border size from 1 to 10
r_border = 9 # rubiks border size from 1 to 10












from PIL import Image, ImageDraw, ImageFont, ImageOps
import os
import shutil

f_width = int(r_width*3) #width, in facets of cubes, aka number of fresco's pixels in width
f_height = int(r_height*3) #height, in facets of cubes, aka number of fresco's pixels in height
picture = Image.open(image_path)
draw = ImageDraw.Draw(picture)

p_width = picture.width
p_height = picture.height

if(p_width/r_width == p_height/r_height):
    pixel_size = int(p_width/r_width/3)
else : 
    print("proportions of the picture are wrong", p_width, r_width, f_width, p_height, r_height, f_height)

abscissa_numbering = [
    "01","02","03","04","05","06","07","08","09","10",
    "11","12","13","14","15","16","17","18","19","10",
    "21","22","23","24","25","26","27","28","29","30",
    "31","32","33","34","35","36","37","38","39","40",
]
ordinate_numbering = [
    "A","B","C","D","E","F","G","H","I",
    "J","K","L","M","N","O","P","Q","R",
    "S","T","U","V","W","X","Y","Z"
]

# simple grid for each pixel

for i in range(1,f_width) :
    n = i*pixel_size
    draw.line((n, 0, n, picture.height), fill=(0, 0, 0), width=f_border)

for j in range(1,f_height) :
    m = j*pixel_size
    draw.line((0, m, picture.width, m), fill=(0, 0, 0), width=f_border)
    
    
    
# bold grid for each rubik's cube

for i in range(1,int(f_width/3)) :
    n = i*3*pixel_size
    draw.line((n, 0, n, picture.height), fill=(0, 0, 0), width=r_border)

for j in range(1,int(f_height/3)) :
    m = j*3*pixel_size
    draw.line((0, m, picture.width, m), fill=(0, 0, 0), width=r_border)


#save the squared picture

if os.path.exists('results'):
    shutil.rmtree('results')
os.makedirs("results/"+str(rows*columns)+" work schemes")
picture.save("results/squared_picture.png","PNG")















#cut the picture in x parts

squaredPic = Image.open("results/squared_picture.png")

w_cut = []
h_cut = []


w_modulo = r_width%columns
h_modulo = r_height%rows

lessWcut = int(r_width/columns)*3*pixel_size
lessHcut = int(r_height/rows)*3*pixel_size


for i in range(w_modulo) :
    w_cut.append(lessWcut+3*pixel_size)
for i in range(columns - w_modulo) :
    w_cut.append(lessWcut)
for i in range(h_modulo) :
    h_cut.append(lessHcut+3*pixel_size)
for i in range(rows - h_modulo) :
    h_cut.append(lessHcut)


set = []

for j in range (rows) :
    for i in range (columns):
        newpic = squaredPic.crop((w_cut[i]*i,h_cut[j]*j,w_cut[i]*(i+1),h_cut[j]*(j+1)))
        set.append(newpic)

for i in range (rows*columns) :
    set[i].save(("results/"+str(rows*columns)+" work schemes/team "+str(i+1)+".png"),"PNG")













#Add border with the columns and rows references, to the 8 pictures

white_border = 150

for i in range (rows * columns) :
    set[i] = ImageOps.expand(set[i], border=r_border, fill='black')
    set[i] = ImageOps.expand(set[i], border=white_border, fill='white')

Font = ImageFont.truetype('gadugi.ttf', 100)


for i in range(rows):
    for j in range(columns) :
        k=columns*i+j
        height = set[k].height
        for column in range (int(w_cut[j]/3/pixel_size)):
                ImageDraw.Draw(set[k]).text((white_border+(0.5+column*3)*pixel_size, 0), abscissa_numbering[column], fill='black', font = Font)
                ImageDraw.Draw(set[k]).text((white_border+(0.5+column*3)*pixel_size, height-white_border), abscissa_numbering[column], fill='black', font = Font)


for i in range(columns):
    for j in range(rows) :
        k=rows*i+j
        width = set[k].width
        for row in range (int(h_cut[j]/3/pixel_size)):
                ImageDraw.Draw(set[k]).text((30,white_border+(0.4+row*3)*pixel_size), ordinate_numbering[row], fill='black', font = Font)
                ImageDraw.Draw(set[k]).text((width-white_border+25,white_border+(0.4+row*3)*pixel_size), ordinate_numbering[row], fill='black', font = Font)
                
                
for i in range (rows * columns) :
    set[i].save(("results/"+str(rows*columns)+" work schemes/team "+str(i+1)+".png"),"PNG")
    
print ("DONE !")

current = os.getcwd()
os.startfile(current+"\\results")