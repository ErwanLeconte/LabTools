#EXPORT DATA SO THERE IS ONLY ONE ROW OF HEADERS. Alternatively, skip more than one line at line 42 

#Improvements: add a pedestal (line w/ slope = 0) or slope to the fit
#TODO: replace sigmas by curve sigma

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy.optimize import curve_fit
import scipy.stats as stats
import csv
import sys
import ast

def modal_magnitude(array):    #returns modal power of 10 of an array for normalizing, necessary to avoid underflow issues (numbers so small that they're rounded to 0)
    powers = np.floor(np.log10(np.abs(array))).astype(int)
    modal_power = stats.mode(powers)[0]
    return modal_power
    

#Model definitions:             TODO: use only gaussian and unpack + pass expected params three at a time to separate gaussian models. recombine at the end for the table
def gauss(x, mu, sigma, A):     #simple gaussian model
    return A*np.exp(-(x-mu)**2/2/sigma**2)

def bimodal(x, mu1, sigma1, A1, mu2, sigma2, A2):       #sum of two gaussians
    return gauss(x,mu1,sigma1,A1)+gauss(x,mu2,sigma2,A2)

def trimodal(x, mu1, sigma1, A1, mu2, sigma2, A2, mu3, sigma3, A3):     #three gaussians
    return gauss(x,mu1,sigma1,A1) + gauss(x,mu2,sigma2,A2) + gauss(x, mu3, sigma3, A3)

#get data from csv (comma separated values : widely used data format and used by gwyddion, imageJ when exporting data)
def csv_to_x_y(file_path):
    
    #prompt for headers and csv delimiter
    has_header = input('Header? (Y/N)')
    csv_delimiter = input('CSV delimiter?')
    
    with open(file_path) as csv_file:       #using a with statements is best practice for ressource management (I think?) but probably isn't necessary here
        csv_reader = csv.reader(csv_file, delimiter = csv_delimiter)
        
        #skip headers
        if has_header in ['Y', 'y', '1']:
            next(csv_reader)    #if there is a header, skips the first line. export data so that there is only one header row, or skip more lines in this line
        data = pd.DataFrame(csv_reader)

        #declare x and y values for plotting and fitting
        x = np.array(data[0], dtype = float)
        y = np.array(data[1], dtype = float)

        #normalize x, y to avoid overflow/underflow issues
        x_mag = float(modal_magnitude(x))
        y_mag = float(modal_magnitude(y))

        x = x * 10 ** (-x_mag)
        y = y * 10 ** (-y_mag)

        return x,y,x_mag,y_mag  #these values are returned by the function and are later assigned to global variables of the same name

#fit gaussian
def gauss_fit(expected): #takes a tuple : (mu, s, A). TODO: make this smarter (user inputs numbers and create a tuple from that?)
    params, cov = curve_fit(gauss, x, y, expected)  #params: parameters of the best fit found by scipy black magic. cov: covariance matrix. contains sigma squared
    sigma = np.sqrt(np.diag(cov))       #recover sigma from covariance matrix
    params_table = pd.DataFrame(data={'params': params, 'sigma': sigma}, index=gauss.__code__.co_varnames[1:])  #make a nice table with the parameters and sigmas
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

#TODO: 4modal and above
# def quadrimodal_fit(): 
#     print('NOT YET IMPLEMENTED')

# def pentamodal_fit():
#     print('NOT YET IMPLEMENTED')

# def hexamodal_fit():
#     print('NOT YET IMPLEMENTED')

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
def fit_type_to_fn(number):
    distr_num_to_fn = {
        1: gauss_fit,
        2: bimodal_fit,
        3: trimodal_fit,
#         4: quadrimodal_fit,
#         5: pentamodal_fit,
#         6: hexamodal_fit,
}
    #prompt for expected parameters and apply the chosen fit
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
    
    plt.legend()    #display legend


#TODO: steps for several consecutive peaks


def steps(means, sigmas):   #merge the means and sigmas
    steps = (means[:-1]-means[1:]) * x_mag
    uncertainty = (sigmas[:-1]+means[1:]) * x_mag
    return steps, uncertainty



#===main===

#from csv, get x,y columns and their magnitudes to de-normalize later
x,y,x_mag,y_mag = csv_to_x_y(input('CSV location?').strip('\"\''))
#plot for user reference to give fit number and expected parameters
plt.plot(x,y)
plt.show(block=False)
#get fit type and fit that with expected parameters as a starting point. no need to be precise
peak_count = get_fit_type()
params_table = fit_type_to_fn(peak_count)
plt.clf()   #clear the previous plot to make room for the new one
plt.close() #close the window of the previous plot
plot_fit()  #plot the fit and its components
plt.show(block=False)   #show the plot

#report step heights
means_array = np.array([params_table["params"][3*i] for i in range(peak_count)])
steps_array = np.array([(means_array[i+1] - means_array[i])for i in range(peak_count-1)])

sigma_array = np.array([(abs(params_table['params'][3*i+1]) + abs(params_table['params'][3*i+4])) for i in range(peak_count-1)])

#print stuff
print(f'params:{params_table}')
print(f'means:{means_array}')
print(f'steps:{steps_array}')
print(f'uncertainty:{sigma_array}')

#currently useless
# means = extract_means()
# sigmas = extract_sigmas()

#THIS IS WRONG
# if peak_count == 2:
#     heights, uncertainty = steps(means, sigmas)    
#     print(f'Step height:{heights[0]} ± {uncertainty[0]} nm') #this only works for one step, will need to make it smarter for 0 or 2


#Prompt user to exit. Otherwise, the graph is closed as soon as it is displayed becasue the end of the code would be reached
if input('Clear? y/n') in ['yes', 'y', '1']:
    sys.exit()