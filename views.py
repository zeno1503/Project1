from django.shortcuts import render,redirect
from django.db import IntegrityError
from .models import Userdata
import joblib
# Load the model from the file
model = joblib.load(r"C:\Users\PrithvirajSP\AppData\Local\Programs\Python\Python312\python.exe")
print(model)

import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error
from sklearn.preprocessing import LabelEncoder
from datetime import datetime
# Create your views here.
def index(request):
    return render(request,'index.html')



from django.shortcuts import render
from django.http import HttpResponse
from sklearn.preprocessing import LabelEncoder

def pred(request):
    if request.method == 'POST':
        #date_value = request.POST.get('date')
        category = request.POST.get('category')
        size = request.POST.get('size')
        quantity = request.POST.get('quantity')
        print(type(date_value), type(category), type(size), type(quantity))
        input_data = pd.DataFrame({
            'Date': [date_value],
            'Category': [category],
            'Size': [size],
            'Qty': [quantity]
        })
        input_data['Date'] = pd.to_datetime(input_data['Date'])
        input_data['day'] = input_data['Date'].dt.day
        input_data['month'] = input_data['Date'].dt.month
        input_data['year'] = input_data['Date'].dt.year
        input_data = input_data.drop(['Date'], axis=1)
        label_encoder = LabelEncoder()
        label_encoder.fit(input_data['Category'])  # Assuming 'X' is your training DataFrame
        input_data['Category'] = label_encoder.transform(input_data['Category'])
        label_encoder_size = LabelEncoder()
        label_encoder_size.fit(input_data['Size'])
        input_data['Size'] = label_encoder_size.transform(input_data['Size'])
        # Assuming X is your DataFrame
        # label_encoder = LabelEncoder()
        # X['Category'] = label_encoder.fit_transform(X['category'])
        # X['Size'] = label_encoder.fit_transform(X['shivang'])
        # X['day'] = X['Date'].dt.day
        # X['month'] = X['Date'].dt.month
        # X['year'] = X['Date'].dt.year
        # X = X.drop(['Date'], axis=1)
        y_pred = model.predict(input_data)
        print(y_pred)
        print(type(y_pred))
        y_pred=int(y_pred[0])
        print(type(y_pred))
        price=int(y_pred)*int(quantity)
        print(price)
        return render(request, 'prediction.html',{'predict':price})
    else:
        return render(request, 'prediction.html', {'msg': 'no data'})

    


def user_register(request):
    print(request.method)
    if request.method=='POST':
        name=request.POST['name']
        email=request.POST['email']
        password=request.POST['password']
        confirm_password=request.POST['confirm_password']
        print('email: ',email)
        if password==confirm_password:
            ins=Userdata(name=name, email=email, password=password,confirm_password=confirm_password)
            querys=ins.save()
            '''
            if ins.pk is not None:
                print('yes data is save')
            else:
                print('Data is not save')
            
            return render(request,'index.html')
            '''
            try:
                querys
                msg_sucess='you have sucessfully register'
                return render(request,'index.html',{'msg_sucess':msg_sucess})
                #return redirect('user_register')
            except IntegrityError:
                print("Integrity error: Data not saved.")
            except Exception as e:
                print(f"An error occurred: {e}")
        else:
            return render(request,'index.html',{'msg_sucess':"didn't match password"})        
    else:
        return render(request,'index.html',{'msg_sucess':'failed!'})
     
def eeg_prediction(request):
    database_password=""
    database_id=""
    database_email=""
    if request.method=='POST':
        email=request.POST['email']
        password=request.POST['password']
        print('email:',email)
        print('password:',password)
        user_data=userdata(email)
        
        for user_data in user_data:
            print(user_data)
            database_password=user_data.password
            database_id=user_data.id
            database_email=user_data.email
            #print('password: ',password)
            print('db_password: ',database_password)
        if password==database_password and email==database_email:
            #set_session_value=set_session(email)
            #print('session_value',set_session_value)
            set_session_id=request.session['id']=database_id
            set_session_email=request.session['email']=database_email
            print('set_session_email: ',set_session_email)
            print('set_session_id: ',set_session_id)
            #print('email: ',email)
            #return redirect('iris')
            premsg='Hii Waiting...... now not complete code'
            return render(request,'prediction.html',{'premsg':premsg})
            #return render(request,'index.html',{'login_msg':'You are login',
            #                                        'session_msg':'Session is not set',
            #                                      'set_session_id':set_session_id,
            #                                     'set_session_email':set_session_email
                #                                   })
        
        else:
            msg="didn't match username and password"
            return render(request,'index.html',{'msg':msg})
    else:
        return render(request,'Index.html')
#def set_session(self,email):
    #   request.session['email'] =email
    #  return request.session['email']
def userdata(email):
        #print('user_email: ',email)
        user_data=Userdata.objects.filter(email=email)
        return user_data
def logout(request):
    request.session.clear()
    return redirect('log')
def session_expiered(request):
    request.session.clear()
    return redirect('log')
