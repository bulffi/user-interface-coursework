#!flask/bin/python
################################################################################################################################
#------------------------------------------------------------------------------------------------------------------------------                                                                                                                             
# This file implements the REST layer. It uses flask micro framework for server implementation. Calls from front end reaches 
# here as json and being branched out to each projects. Basic level of validation is also being done in this file. #                                                                                                                                  	       
#-------------------------------------------------------------------------------------------------------------------------------                                                                                                                              
################################################################################################################################
from flask import Flask, jsonify, abort, request, make_response, url_for,redirect, render_template
from flask_httpauth import HTTPBasicAuth
from werkzeug.utils import secure_filename
import os
import shutil 
import numpy as np
from search import recommend
import tarfile
from datetime import datetime
from scipy import ndimage
from scipy.misc import imsave 
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])
from tensorflow.python.platform import gfile
app = Flask(__name__, static_url_path = "")
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
auth = HTTPBasicAuth()

#==============================================================================================================================
#                                                                                                                              
#    Loading the extracted feature vectors for image retrieval                                                                 
#                                                                          						        
#                                                                                                                              
#==============================================================================================================================
extracted_features=np.zeros((10000,2048),dtype=np.float32)
with open('saved_features_recom.txt') as f:
    		for i,line in enumerate(f):
        		extracted_features[i,:]=line.split()
print("loaded extracted_features") 


#==============================================================================================================================
#                                                                                                                              
#  This function is used to do the image search/image retrieval
#                                                                                                                              
#==============================================================================================================================

        
@app.route('/choose_cata',methods=['GET','POST'])
def choose_cata():
    print('choose cata')
    global image_list
    candidata = []
    if(request.method=='POST'):
        catalog_chosen = str(request.data,encoding='utf-8')
        print(catalog_chosen)
        with open(os.getcwd()+"/database/tags/"+ catalog_chosen+'.txt','r') as f:
            lines = f.readlines()
            for number in lines:
                candidata.append(int(number))
        #print(candidata[10])
        #print('original'+ str(image_list))
        for img in image_list:
            img_number= img[10:-4]
            #print(img_number)
            if(int(img_number) not in candidata):
                source = img.replace("/result\\im",r'\static\result\im',1)
                os.remove(os.getcwd()+source)
                image_list.remove(img)
        #print('new'+ str(image_list))
        image_path = "/result"
        result = 'static/result'
        image_list = [os.path.join(image_path, file) for file in os.listdir(result)
                              if not file.startswith('.')]
        answer_list = []
        for dirs in image_list:
            answer_list.append(dirs.replace("/result\\im",r'/result\im',1))
        while(len(answer_list)%9!=0):
            answer_list.append('None')
        #print(answer_list)
        images = {
			'image0':answer_list[0],
            'image1':answer_list[1],	
			'image2':answer_list[2],	
			'image3':answer_list[3],	
			'image4':answer_list[4],	
			'image5':answer_list[5],	
			'image6':answer_list[6],	
			'image7':answer_list[7],	
			'image8':answer_list[8]
		}
        print(images)				
        return jsonify(images)






@app.route('/loadFavotite',methods=['GET','POST'])
def show_favorite():
    global favorite_list
    global current_position
    current_position = 0
    favorite_list = []
    print('show favorite')
    if not gfile.Exists('./static/favorite'):
        return 'nothing'
    if request.method == 'POST':
        favorite_list = os.listdir(os.getcwd() + r'\static\favorite')
        answer_list = []
        for dirs in favorite_list:
            answer_list.append(os.path.join("/favorite",dirs))
        while(len(answer_list)%9!=0):
            answer_list.append('None')
        #print(answer_list)
        images = {
			'image0':answer_list[0],
            'image1':answer_list[1],	
			'image2':answer_list[2],	
			'image3':answer_list[3],	
			'image4':answer_list[4],	
			'image5':answer_list[5],	
			'image6':answer_list[6],	
			'image7':answer_list[7],	
			'image8':answer_list[8]
		    }
        print(images)				
        return jsonify(images)
        
@app.route('/privious_favo',methods=['GET','POST'])
def privious_favo():
    global favorite_list
    global current_position
    print('privious favo')
    if not gfile.Exists('./static/favorite'):
        return 'nothing'        
    answer_list = []
    for dirs in favorite_list:
        answer_list.append(os.path.join("/favorite",dirs))
    while(len(answer_list)%9!=0):
        answer_list.append('None')
    if request.method == 'POST':
        if(current_position == 0):
            images = {
			'image0':answer_list[0],
            'image1':answer_list[1],	
			'image2':answer_list[2],	
			'image3':answer_list[3],	
			'image4':answer_list[4],	
			'image5':answer_list[5],	
			'image6':answer_list[6],	
			'image7':answer_list[7],	
			'image8':answer_list[8]
		    }
            print(current_position)
            print(images)				
            return jsonify(images)
    
        #print(answer_list)
        current_position -= 9
        current_position = max(0,current_position)
        print(current_position)
        images = {
			'image0':answer_list[current_position + 0],
            'image1':answer_list[current_position + 1],	
			'image2':answer_list[current_position + 2],	
			'image3':answer_list[current_position + 3],	
			'image4':answer_list[current_position + 4],	
			'image5':answer_list[current_position + 5],	
			'image6':answer_list[current_position + 6],	
			'image7':answer_list[current_position + 7],	
			'image8':answer_list[current_position + 8]
		    }
        
        print(images)				
        return jsonify(images)

@app.route('/next_favo',methods=['GET','POST'])
def next_favo():
    global favorite_list
    global current_position
    print('next favo')
    if not gfile.Exists('./static/favorite'):
        return 'nothing'
    answer_list = []
    for dirs in favorite_list:
        answer_list.append(os.path.join("/favorite",dirs))
    while(len(answer_list)%9!=0):
        answer_list.append('None')
    if request.method == 'POST':
        if(len(favorite_list) < current_position):
            images = {
			'image0':answer_list[current_position - 9 + 0],
            'image1':answer_list[current_position - 9 + 1],	
			'image2':answer_list[current_position - 9 + 2],	
			'image3':answer_list[current_position - 9 + 3],	
			'image4':answer_list[current_position - 9 + 4],	
			'image5':answer_list[current_position - 9 + 5],	
			'image6':answer_list[current_position - 9 + 6],	
			'image7':answer_list[current_position - 9 + 7],	
			'image8':answer_list[current_position - 9 + 8]
		    }
            print(current_position)
            print(images)			
            return jsonify(images)

        current_position += 9
        current_position = min((len(favorite_list)//9)*9 ,current_position)
        if(len(favorite_list)%9==0):
            current_position = min(len(favorite_list)-9,current_position)
				
        #print(answer_list)        
        print(current_position)
        images = {
			'image0':answer_list[current_position + 0],
            'image1':answer_list[current_position + 1],	
			'image2':answer_list[current_position + 2],	
			'image3':answer_list[current_position + 3],	
			'image4':answer_list[current_position + 4],	
			'image5':answer_list[current_position + 5],	
			'image6':answer_list[current_position + 6],	
			'image7':answer_list[current_position + 7],	
			'image8':answer_list[current_position + 8]
		    }
        print(images)
        return jsonify(images)

@app.route('/add_favorite',methods=['GET','POST'])

def add_favorite():
    print("add favorite")
    if not gfile.Exists('./static/result/favorite'):
        os.makedirs('./static/result/favorite')
    
    if request.method == 'POST':
        #print(request.data)
        favorite_number = str(request.data,encoding='utf-8').split('|')
        favo_list = []
        if '9/' in favorite_number:
            favorite_number.remove('9/')
            favorite_number.append('9')
        for num_str in favorite_number:
            favo_list.append(int(num_str))
        #print(image_list)
        #print(os.getcwd())
        for num in favo_list:
            source = image_list[num-1].replace("/result\\im",r'\static\result\im',1)
            shutil.copy(os.getcwd()+source , os.getcwd()+r'\static\favorite')
            #os.popen('copy '+source +' '+'./static/favorite')
            #mycopyfile(source,os.getcwd()+r'\static\favorite')


        return 'nothing'



@app.route('/imgUpload', methods=['GET', 'POST'])
#def allowed_file(filename):
#    return '.' in filename and \
#           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def upload_img():
    print("image upload")
    result = 'static/result'
    if not gfile.Exists(result):
          os.mkdir(result)
    shutil.rmtree(result)
 
    if request.method == 'POST' or request.method == 'GET':
        print(request.method)
        # check if the post request has the file part
        if 'file' not in request.files:
            print('No file part')
            return redirect(request.url)
        
        file = request.files['file']
        print(file.filename)
        # if user does not select file, browser also
        # submit a empty part without filename
        if file.filename == '':
           
            print('No selected file')
            return redirect(request.url)
        if file:# and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            inputloc = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            recommend(inputloc, extracted_features)
            os.remove(inputloc)
            image_path = "/result"
            global image_list
            image_list = [os.path.join(image_path, file) for file in os.listdir(result)
                              if not file.startswith('.')]
            print(image_list)
            images = {
			'image0':image_list[0],
            'image1':image_list[1],	
			'image2':image_list[2],	
			'image3':image_list[3],	
			'image4':image_list[4],	
			'image5':image_list[5],	
			'image6':image_list[6],	
			'image7':image_list[7],	
			'image8':image_list[8]
		      }
            print(images)				
            return jsonify(images)



#==============================================================================================================================
#                                                                                                                              
#                                           Main function                                                        	            #						     									       
#  				                                                                                                
#==============================================================================================================================
@app.route("/")
def main():
    
    return render_template("main.html")   
if __name__ == '__main__':
    app.run(debug = True, host= '127.0.0.1')
