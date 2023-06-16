import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy.optimize import curve_fit
import csv
import sys
import ast

#Model definitions:
def gauss(x, mu, sigma, A):
    return A*np.exp(-(x-mu)**2/2/sigma**2)

def bimodal(x, mu1, sigma1, A1, mu2, sigma2, A2):
    return gauss(x,mu1,sigma1,A1)+gauss(x,mu2,sigma2,A2)

def trimodal(x, mu1, sigma1, A1, mu2, sigma2, A2, mu3, sigma3, A3):
    return gauss(x,mu1,sigma1,A1) + gauss(x,mu2,sigma2,A2) + gauss(x, mu3, sigma3, A3)

#data from csv
def csv_to_x_y(file_path):
    
    #deal with headers
    has_header = input('Header? (Y/N)')    
    csv_delimiter = input('CSV delimiter?')
    
    with open(file_path) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter = csv_delimiter)
        
        #skip headers
        if has_header in ['Y', 'y', '1']:
            next(csv_reader)
        data = pd.DataFrame(csv_reader)

        x = np.array(data[0], dtype = float)
        y = np.array(data[1], dtype = float)

        #normalize x, y to avoid overflow/underflow issues
        x_mag = np.floor(np.log10(np.abs(x))).astype(int).mode()    
        y_mag = np.floor(np.log10(np.abs(y))).astype(int).mode()
        x = x * 10 ** (-x_mag)
        y = y * 10 ** (-y_mag)

        return x,y,x_mag,y_mag

#fit gaussian
def gauss_fit(expected): #takes a tuple : (mu, s, A)
    params, cov = curve_fit(gauss, x, y, expected)
    sigma = np.sqrt(np.diag(cov))
    params_table = pd.DataFrame(data={'params': params, 'sigma': sigma}, index=gauss.__code__.co_varnames[1:])
    return params_table

#fit bimodal
def bimodal_fit(expected): #takes a tuple: (mu1, s1, A1, mu2, s2, A2)
    params, cov = curve_fit(bimodal, x, y, expected)
    sigma = np.sqrt(np.diag(cov))
    params_table = pd.DataFrame(data={'params': params, 'sigma': sigma}, index=bimodal.__code__.co_varnames[1:])
    return params_table

#fit trimodal
def trimodal_fit(expected): #takes a tuple: (mu1, s1, A1, mu2, s2, A2, mu3, s3, A3)
    params, cov = curve_fit(trimodal, x, y, expected)
    sigma = np.sqrt(np.diag(cov))
    params_table = pd.DataFrame(data={'params': params, 'sigma': sigma}, index=trimodal.__code__.co_varnames[1:])
   #return params, sigma, cov, params_table
    return params_table

#TODO: 4modal
def quadrimodal_fit(): 
    print('NOT YET IMPLEMENTED')

def pentamodal_fit():
    print('NOT YET IMPLEMENTED')

def hexamodal_fit():
    print('NOT YET IMPLEMENTED')

#get peak # from user input
def get_fit_type():
    fit_type = int(input('Number of Distributions? (1,2,3)').strip())
    i = 0 #keep track of number of attempts
    while fit_type not in (1,2,3):
        fit_type = input('Please try again').strip()
        i += 1
        if i >= 5:
            print('Too many failed attempts')
            sys.exit()
    return(fit_type)

#create function for (distr. # -> function to call)
def fit_type_to_fn(number,):
    distr_num_to_fn = {
        1: gauss_fit,
        2: bimodal_fit,
        3: trimodal_fit,
        4: quadrimodal_fit,
        5: pentamodal_fit,
        6: hexamodal_fit,
}
    expected = ast.literal_eval(input('Expected parameters? Enter a tuple:"(mu1,sigma1,A1)", no spaces'))
    return distr_num_to_fn[number](expected)

#plot the model
def plot_fit():
    #create more x values (subdivisions of the range of the models) to evaluate our model -> nicer curve
    x_fit = np.linspace(x.min(), x.max(), 500)

    #plot original data
    plt.plot(x,y, label='Original data')
    
    #plot the model
    if peak_count == 1:
        plt.plot(x_fit, gauss(x_fit, *params_table["params"]), color='red', lw=3, label='Model')
    
    elif peak_count == 2:
        plt.plot(x_fit, bimodal(x_fit, *params_table["params"]), color='red', lw=3, label='Model')

    elif peak_count == 3:
        plt.plot(x_fit, trimodal(x_fit, *params_table["params"]), color='red', lw=3, label='Model')
    
    #todo: plot 4-6 peaks

    #plot individual curves
    for i in range(0, peak_count):
        plt.plot(x_fit, gauss(x_fit, *params_table["params"][i*3:(i+1)*3]), color='red', lw=1, ls="--", label=f'Distribution {i+1}')
    
    plt.legend()


#TODO: delta mu for consecutive peaks

def extract_means():
    means = np.array([params_table["params"][3*i] for i in range(peak_count)])
    return means

def extract_sigmas():
    sigmas = np.array([params_table["sigma"][3*i] for i in range(peak_count)])
    return sigmas


def steps(means, sigmas):
    steps = (means[:-1]-means[1:]) * x_mag
    uncertainty = (sigmas[:-1]+means[1:]) * x_mag
    return steps, uncertainty



#main

x,y,x_mag,y_mag = csv_to_x_y(input('CSV location?'))
print('Close graph to proceed')
plt.plot(x,y)
plt.show()
peak_count = get_fit_type()
params_table = fit_type_to_fn(peak_count)
plot_fit()
plt.show()
print(params_table)
means = extract_means()
sigmas = extract_sigmas()
if peak_count == 2:
    heights, uncertainty = steps(means, sigmas)    
    print(f'Step height:{heights[0]} ± {uncertainty[0]} nm') #this only works for one step, will need to make it smarter for 0 or 2



