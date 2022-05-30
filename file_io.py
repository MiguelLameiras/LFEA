from lib import dependencies

ALLOWED_EXTENSIONS = {'txt', 'csv'}

def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def check_float(potential_float):
    try:
        float(potential_float)
        return True
    except ValueError:
        return False

def read(file_path,num_cols,x_gain,y_gain):
  
    file = open(file_path,'r')
    leitura = []
    for line in file:
        lido = line.strip().split(",")
        if(check_float(lido[0]) == False):
            leitura.append(lido)
        else:
            leitura.append(lido)

    file.close()

    x,y,errx,erry = [],[],[],[]

    if num_cols == 4:
        for i in leitura:
            x.append(float(i[0])*x_gain)
            y.append(float(i[1])*y_gain)
            errx.append(float(i[2])*x_gain)
            erry.append(float(i[3])*y_gain) 

    if num_cols == 2:
        for i in leitura:
            #print(i)
            x.append(float(i[0])*x_gain)
            y.append(float(i[1])*y_gain)


    return x,y,errx,erry