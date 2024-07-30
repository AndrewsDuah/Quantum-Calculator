import tkinter

from tkinter import ttk

from scipy import constants as const

import math

windows = tkinter.Tk()

#windows.minsize(width = 1400, height = 700)

windows.title("PHYSICS 112 CALCULATOR")


##for wavelength 

def calculate_wavelength():
    try:
        n1 = int(n1_entry.get())
        n2 = int(n2_entry.get())
        if n1<1 or n2 < 1: 
            raise ValueError('Energy levels must be positive')
        e1 = (-13.6/(n1**2))-(-13.6/(n2**2))
        e2_ev = abs(e1)
        e2_joule = e2_ev*const.eV
        wave_length = (const.h * const.c )/e2_joule
        result_label_1.config(text = f"The wavelength of the photon emitted from the transition n = {n1} to n = {n2} is {wave_length}m",font=('Sans-serif',12))
    except ValueError as ve:
          result_label_1.config(text=f"Error: {ve},Enter appropriate inputs", font=('Sans-serif', 12))
    except Exception as e:
          result_label_1.config(text=f"An unexpected error occurred: {e}", font=('Sans-serif', 12))
          
        
def frequency():
    
    try:
        n_a = int(n1_entry.get())
        n_b = int(n2_entry.get())
        if n_a<1  or n_b <1: 
            raise ValueError("Energy levels must be positive")
        e1 = (-13.6/(n_a**2))-(-13.6/(n_b**2))
        e2_ev = abs(e1)
        e2_joule = e2_ev*const.eV
        frequ_ency = e2_joule/const.h
        result_label_2.config(text=f"The frequency of the photon emitted from the transition n = {n_a} to n = {n_b} is {frequ_ency:.2f}HZ",font=('Sans-serif',12))
    except ValueError as ve:
              result_label_2.config(text=f"Error: {ve},Enter appropriate inputs", font=('Sans-serif', 12))
    except Exception as e:
              result_label_2.config(text=f"An unexpected error occurred: {e}", font=('Sans-serif', 12))
    
    
def energy():
    try:
        ne_1 = int(n1_entry.get())
        ne_2 = int(n2_entry.get())
        if ne_1 < 1 or ne_2 < 1 :
            raise ValueError("Energy levels must be positive")
        e_evv = abs((-13.6*const.eV/ne_1**2)-(-13.6*const.eV/ne_2**2))
        e_vv2 = (e_evv)/(1.6e-19)
        result_label_3.config(text=f"The energy of the photon emitted from the transition n = {ne_1} to n = {ne_2} is {e_evv} J or {e_vv2:.3f}ev", font=('Sans-serif',12))
    except ValueError as ve:
          result_label_3.config(text=f"Error: {ve},Enter appropriate inputs", font=('Sans-serif', 12))
    except Exception as e:
          result_label_3.config(text=f"An unexpected error occurred: {e}", font=('Sans-serif', 12))
         
def nuclear_physics():
    m_p = 1.007277
    m_n = 1.008665
    m_e = 0.0005486 
    try:
        ask_atom = str(np1_entry.get()) 
        ask_mass = float(np2_entry.get())
        ask_atomic_number = int(np3_entry.get())
        ask_mass_number = int(np4_entry.get())
        
        if not ask_atom.isalpha():
            raise ValueError("Please enter a valid atomic symbol")
        
        if ask_mass <= 0 or ask_atomic_number <= 0 or ask_mass_number <= 0:
            raise ValueError("Please enter positive values for mass, atomic number, and mass number")
        
        if ask_atomic_number > ask_mass_number:
            raise ValueError("Atomic number cannot be greater than mass number")

        m_system = ask_mass
        neutron_number = ask_mass_number - ask_atomic_number
        m_con = (ask_atomic_number * m_p) + (ask_atomic_number * m_e) + (neutron_number * m_n)
        m_deficit = m_con - m_system
        binding_energy_J = m_deficit * 931.48 * 10**6 * const.eV
        binding_energy_Mev = m_deficit * 931.48
        
        result_label_4.config(text=f"""Mass deficit of {ask_atom} with atomic mass {ask_mass}u = {m_deficit:.5f}u
            Binding Energy = {binding_energy_J:.4e}J or {binding_energy_Mev:.5f}MeV""", font=('Sans-serif', 12))
    except ValueError as ve:
        result_label_4.config(text=f"Error: {ve},Enter appropriate inputs", font=('Sans-serif', 12))
    except Exception as e:
        result_label_4.config(text=f"An unexpected error occurred: {e}", font=('Sans-serif', 12))

            
def elec_wavelength_velocity():
    try: 
        v_1 = float(elecv_entry.get())
        if v_1 < 0:
            raise ValueError("Speed of electron  must be positive")
        lambda_1 = ((const.h)/((const.electron_mass)*(v_1)))
        result_label_5.config(text = f"The de-Broglie wavelength of electron moving with velocity of {v_1}m/s is {lambda_1} m",font=('Sans-serif',12))
    except ValueError as ve:
         result_label_5.config(text=f"Error: {ve},Enter appropriate inputs", font=('Sans-serif', 12))
    except Exception as e:
         result_label_5.config(text=f"An unexpected error occurred: {e}", font=('Sans-serif', 12))
        
        
def elec_wavelength_ke():
    try:
        ke_1 = float(elecke_entry.get())
        if ke_1 < 0:
            raise ValueError("Kinetice Energy must be positive")
        lambda_2 = ((const.h)/math.sqrt(2*ke_1*const.eV*const.electron_mass))
        result_label_6.config(text=f"The de-Broglie wavelength of electron moving with kinetic energy of {ke_1} eV is {lambda_2} m",font=('Sans-serif',12))
    except ValueError as ve:
         result_label_6.config(text=f"Error: {ve},Enter appropriate inputs", font=('Sans-serif', 12))
    except Exception as e:
         result_label_6.config(text=f"An unexpected error occurred: {e}", font=('Sans-serif', 12))
    

def elec_wavelength_p():
    try:
         p_1 = float(elecp_entry.get())
         if p_1 < 0:
             raise ValueError("Momentum must be positive")
         lambda_3 = (const.h/p_1)
         result_label_7.config(text=f"The de-Broglie wavelength of proton moving with momentum of {p_1} kgm/s is {lambda_3} m",font=('Sans-serif',12))
    except ValueError as ve:
         result_label_7.config(text=f"Error: {ve},Enter appropriate inputs", font=('Sans-serif', 12))
    except Exception as e:
         result_label_7.config(text=f"An unexpected error occurred: {e}", font=('Sans-serif', 12))


def neutron_wavelength_v():
    try:
        v_1 = float(neutronv_entry.get())
        if v_1 < 0:
            raise ValueError("Speed of neutron must be positive")
        lambda_1 = ((const.h)/((const.neutron_mass)*(v_1)))
        result_label_8.config(text=f"The de-Broglie wavelength of neutron moving with velocity of {v_1}m/s is {lambda_1} m",font=('Sans-serif',12))
    except ValueError as ve:
         result_label_8.config(text=f"Error: {ve}, Enter appropriate inputs", font=('Sans-serif', 12))
    except Exception as e:
         result_label_8.config(text=f"An unexpected error occurred: {e}", font=('Sans-serif', 12))
         
         
         
def neutron_wavelength_ke():
    try:
         ke_1 = float(neutron_ke_entry.get())
         if ke_1 <0 :
             raise ValueError("Kinetic Energy must be positive")
         lambda_2 = ((const.h)/(math.sqrt(2*ke_1*const.eV*const.neutron_mass)))
         result_label_9.config(text=f"The de-Broglie wavelength of neutron moving with kinetic energy of {ke_1} eV is {lambda_2} m",font=('Sans-serif',12))
    except ValueError as ve:
         result_label_9.config(text=f"Error: {ve},Enter appropriate inputs", font=('Sans-serif', 12))
    except Exception as e:
         result_label_9.config(text=f"An unexpected error occurred: {e}", font=('Sans-serif', 12))
          
         
            
def neutron_wavelength_p():
    try:
        p_1 = float(neutron_p_entry.get())
        if p_1 < 0 :
            raise ValueError("Momentum must be positive")
        lambda_3 = (const.h/p_1) 
        result_label_10.config(text=f"The de-Broglie wavelength of  neutron moving with momentum of {p_1} kgm/s is {lambda_3} m",font=('Sans-serif',11,"bold"))
    except ValueError as ve:
         result_label_10.config(text=f"Error: {ve},Enter appropriate inputs", font=('Sans-serif', 12))
    except Exception as e:
         result_label_10.config(text=f"An unexpected error occurred: {e}", font=('Sans-serif', 12))
         
         
def proton_wavelength_v():
    try:
       v_p = float(protonv_entry.get())
       if v_p < 0:
           raise ValueError("Speed of proton must be positive")
       lambda_1 = ((const.h)/((const.proton_mass)*(v_p)))
       result_label_11.config(text=f"The de-Broglie wavelength of proton moving with velocity of {v_p}m/s is {lambda_1} m",font=('Sans-serif',11,"bold"))
    except ValueError as ve:
     result_label_11.config(text=f"Error: {ve},Enter appropriate inputs", font=('Sans-serif', 12))
    except Exception as e:
     result_label_11.config(text=f"An unexpected error occurred: {e}", font=('Sans-serif', 12))


def proton_wavelength_ke():
    try:
        ke_1 = float(proton_ke_entry.get())
        if ke_1 < 0 :
            raise ValueError("Kinetic Energy must be postive")
        lambda_2 = ((const.h)/math.sqrt(2*ke_1*const.eV*const.proton_mass))
        result_label_12.config(text=f"The de-Broglie wavelength of proton moving with kinetic energy of {ke_1} eV is {lambda_2} m",font=('Sans-serif',12))
    except ValueError as ve:
         result_label_12.config(text=f"Error: {ve},Enter appropriate inputs", font=('Sans-serif', 12))
    except Exception as e:
         result_label_12.config(text=f"An unexpected error occurred: {e}", font=('Sans-serif', 12))
        

def proton_wavelength_p():
    try:
        p_1 = float(proton_p_entry.get())
        if p_1 < 0:
            raise ValueError("Momentum must be positive")
        lambda_3 = (const.h/p_1)         
        result_label_13.config(text=f"The de-Broglie wavelength of proton moving with ]momentum of {p_1} kgm/s is {lambda_3} m",font=('Sans-serif',12))
    except ValueError as ve:
         result_label_13.config(text=f"Error: {ve},Enter appropriate inputs", font=('Sans-serif', 12))
    except Exception as e:
         result_label_13.config(text=f"An unexpected error occurred: {e}", font=('Sans-serif', 12))
         
         
def nuclear_radius():
    try:
        n1 = nr_entry1.get()
        n2 = int(nr_entry2.get())
        n3 = int(nr_entry3.get())
        if not n1.isalpha():
            raise ValueError("Please enter valid symbol")
        elif n2 < 0 or n3 < 0: 
            raise ValueError("Atomic number or Mass number must be positive")
        elif n2 > n3: 
            raise ValueError("Atomic number cannot be greater than mass number")   
        radius = (n3 ** (1/3)) * 1.2
        def format_nuclei_radius(n3, n1, n2, radius):
            superscripts = "⁰¹²³⁴⁵⁶⁷⁸⁹"
            subscripts = "₀₁₂₃₄₅₆₇₈₉"
            
            superscript_mass = "".join(superscripts[int(digit)] for digit in str(n3))
            subscript_atomic = "".join(subscripts[int(digit)] for digit in str(n2))
    
            formatted_string = f"The radius of {n1}{superscript_mass}{subscript_atomic} nuclei is {radius:.4f} fm"
            return formatted_string
        
        formatted_radius = format_nuclei_radius(n3, n1, n2, radius)
        result_label_14.config(text=formatted_radius, font=('Sans-serif', 12))
    except ValueError as ve:
          result_label_14.config(text=f"Error: {ve},Enter appropriate inputs", font=('Sans-serif', 12))
    except Exception as e:
          result_label_14.config(text=f"An unexpected error occurred: {e}", font=('Sans-serif', 12))
          
                    
    
def bohr_radius():
    try:
        n_input = int(br_entry.get())
        if n_input < 1 :
            raise ValueError("Energy level must be postive")
        bohr_r = (52.9*n_input**2) 
        result_label_15.config(text=f"The Bohr radius for energy level {n_input} is {bohr_r:.4f}pm",font=('Sans-serif', 12))
    except ValueError as ve:
          result_label_15.config(text=f"Error: {ve},Enter appropriate inputs", font=('Sans-serif', 12))
    except Exception as e:
          result_label_15.config(text=f"An unexpected error occurred: {e}", font=('Sans-serif', 12))
          
          
def fah_to_cel():
    try: 
        n1 = float(td_entry1.get())
        cel = (5/9)*(n1-32)
        result_label_16.config(text=f"{n1}°F is {cel:.4f}°C",font=('Sans-serif', 12))
    except ValueError:
        result_label_16.config(text="Please enter a valid input",font=('Sans-serif', 12))
        
        
def cel_to_fah():
    try: 
        n1 = float(td_entry1.get())
        fah = (9/5)*n1 + 32
        result_label_17.config(text=f"{n1}°C is {fah:.4f}°F",font=('Sans-serif', 12))
    except ValueError:
        result_label_17.config(text="Please enter a valid input",font=('Sans-serif', 12))
          
        
def cel_to_k():
    try: 
        n1 = float(td_entry1.get())
        k = n1 +273.15
        result_label_18.config(text=f"{n1}°C is {k:.4f}K",font=('Sans-serif', 12))
    except ValueError:
        result_label_18.config(text="Please enter a valid input",font=('Sans-serif', 12))
          
        
def fah_to_k():
    try: 
        n1 = float(td_entry1.get())
        k = ((5/9)*(n1-32))+273.15
        result_label_19.config(text=f"{n1}°F is {k:.4f}K",font=('Sans-serif', 12))
    except ValueError:
        result_label_19.config(text="Please enter a valid input",font=('Sans-serif', 12))
        
        
def ideal_gas_law():
    try:
        P = float(ideal_gas_P_entry.get())
        if P< 0:
            raise ValueError("Pressure must be positive")
        V = float(ideal_gas_V_entry.get())
        if V<0:
            raise ValueError("Volume must be positive")
        n = float(ideal_gas_n_entry.get())
        if n<0:
            raise ValueError("Number of moles must be positive")
        T = float(ideal_gas_T_entry.get())
        
        R = const.R  
        
        if P == 0:
            P = (n * R * T) / V
            result_label_ideal_gas.config(text=f"Pressure P = {P:.4f} Pa",font=('Sans-serif', 12))
        elif V == 0:
            V = (n * R * T) / P
            result_label_ideal_gas.config(text=f"Volume V = {V:.4f} m³",font=('Sans-serif', 12))
        elif n == 0:
            n = (P * V) / (R * T)
            result_label_ideal_gas.config(text=f"Moles n = {n:.4f} mol",font=('Sans-serif', 12))
        elif T == 0:
            T = (P * V) / (n * R)
            result_label_ideal_gas.config(text=f"Temperature T = {T:.4f} K",font=('Sans-serif', 12))
        else:
            result_label_ideal_gas.config(text="Please set one variable to 0 for calculation.",font=('Sans-serif', 12))
    except ValueError as ve :
        result_label_ideal_gas.config(text=f"Error : {ve}, Please enter valid inputs.",font=('Sans-serif', 12))
    except Exception as e: 
         result_label_ideal_gas.config(text=f"Error : {e}, Please enter valid inputs.",font=('Sans-serif', 12))
         
def carnot_efficiency():
    try:
        temp1 = float(eng_entry1.get())
        temp2 = float(eng_entry2.get())
        
        eff = 1-(temp1/temp2)
        eff_1 = eff *100
        eng_result_label.config(text=f"The efficiency of the engine is {eff_1:.2f}%",font=('Sans-serif', 12))
    except ValueError:
        eng_result_label.config(text="Please enter a valid temperature value",font=('Sans-serif', 12))
    except Exception as e: 
        eng_result_label.config(text=f"Error: {e}, Enter valid inputs",font=('Sans-serif', 12))
    
          

    
my_notebook = ttk.Notebook(windows)
my_notebook.grid()

## frame 1

frame_1 = tkinter.Frame(my_notebook)
my_notebook.add(frame_1, text = "Atomic Transition Calculations")

n1_label = tkinter.Label(frame_1,text="Initial energy level (n1)",font=('Sans-serif',11,"bold"))
n1_label.grid(row=0, column= 0,pady=5,padx=5)
n1_entry = tkinter.Entry(frame_1)
n1_entry.grid(row=0,column=1)

n2_label = tkinter.Label(frame_1,text="Final energy level (n2)",font=('Sans-serif',11,"bold"))
n2_label.grid(row=1,column=0,padx=5,pady=5)
n2_entry = tkinter.Entry(frame_1)
n2_entry.grid(row=1, column=1, padx=5, pady=5)

button_1 = tkinter.Button(frame_1,text="Calculate wavelength", command=calculate_wavelength,font=('Sans-serif',10))
button_1.grid(row=2, column=1)

result_label_1 = tkinter.Label(frame_1, text = "")
result_label_1.grid(row=4)

button_2 = tkinter.Button(frame_1, text = "Calculate frequency", command= frequency,font=('Sans-serif',10))
button_2.grid(row=2, column=2)

result_label_2 = tkinter.Label(frame_1, text="")
result_label_2.grid(row=5)

button_3 =tkinter.Button(frame_1,text="Calculate energy",font=('Sans-serif',10),command=energy)
button_3.grid(row=2 , column=3)

result_label_3 = tkinter.Label(frame_1,text="")
result_label_3.grid(row=6)



###frame2
frame_2 = tkinter.Frame(my_notebook)
my_notebook.add(frame_2, text = "Binding Energy & Mass Deficit")

np1_label = tkinter.Label(frame_2, text="Symbol of atom",font=('Sans-serif',10,"bold"))
np1_label.grid(row=0,column=0,padx=5,pady=5,)
np1_entry = tkinter.Entry(frame_2)
np1_entry.grid(row=0,column=1)

np2_label = tkinter.Label(frame_2,text="Atomic mass of the atom (without units(u))",font=('Sans-serif',11,"bold"))
np2_label.grid(row=1,column=0, padx=5,pady=5)
np2_entry = tkinter.Entry(frame_2)
np2_entry.grid(row=1,column=1,padx=5,pady=5)

np3_label = tkinter.Label(frame_2,text="Atomic number",font=('Sans-serif',11,"bold"))
np3_label.grid(row=2,column=0,padx=5,pady=5)
np3_entry = tkinter.Entry(frame_2)
np3_entry.grid(row=2,column=1,padx=5,pady=5)

np4_label = tkinter.Label(frame_2, text="Mass number",font=('Sans-serif',11,"bold"))
np4_label.grid(row=3,column=0, padx=5, pady=5)
np4_entry = tkinter.Entry(frame_2)
np4_entry.grid(row=3, column=1,padx=5,pady=5)

button_4 = tkinter.Button(frame_2,text="Calculate",command=nuclear_physics,font=('Sans-serif',10))
button_4.grid(row=4, column=1)

result_label_4 = tkinter.Label(frame_2, text="")
result_label_4.grid(row=5)


## frame 3

frame_3 = tkinter.Frame(my_notebook)
my_notebook.add(frame_3, text = "Electron`s de-Broglie Wavelength")

elecv_label_1 = tkinter.Label(frame_3,text="Enter the velocity of electron (without units)",font=('Sans-serif',11,"bold"))
elecv_label_1.grid(row=0,column=0,padx=5,pady=5)
elecv_entry = tkinter.Entry(frame_3)
elecv_entry.grid(row=0,column=1,padx=5,pady=5)

button_5 = tkinter.Button(frame_3,text="Calculate wavelength",command=elec_wavelength_velocity,font=('Sans-serif',10))
button_5.grid(row=2,column=1)

result_label_5 = tkinter.Label(frame_3, text="")
result_label_5.grid(row=3)

elecke_label_1 = tkinter.Label(frame_3,text="Enter the value of the kinetic energy in eV",font=('Sans-serif',11,"bold"))
elecke_label_1.grid(row=6,column=0,padx=5,pady=5)
elecke_entry = tkinter.Entry(frame_3)
elecke_entry.grid(row=6,column=1)

button_6 = tkinter.Button(frame_3,text="Calculate wavelength", command=elec_wavelength_ke,font=('Sans-serif',10))
button_6.grid(row=7, column=1)

result_label_6 = tkinter.Label(frame_3, text= "")
result_label_6.grid(row=8)

elecp_label_1 = tkinter.Label(frame_3,text="Enter the value of the momentum (without units)",font=('Sans-serif',11,"bold"))
elecp_label_1.grid(row=10,column=0,padx=5,pady=5)
elecp_entry = tkinter.Entry(frame_3)
elecp_entry.grid(row=10,column=1, padx=5,pady=5)

button_7 = tkinter.Button(frame_3, command=elec_wavelength_p, font=('Sans-serif',10),text="Calculate wavelength")
button_7.grid(row=11,column=1,padx=5,pady=5)

result_label_7 = tkinter.Label(frame_3,text="")
result_label_7.grid(row=12)




    
##frame 4
frame_4 = tkinter.Frame(my_notebook)
my_notebook.add(frame_4, text = "Neutron`s de-Broglie Wavelength")

neutronv_label_1 = tkinter.Label(frame_4,text="Enter the velocity of neutron (without units)",font=('Sans-serif',11,"bold"))
neutronv_label_1.grid(row=0,column=0,padx=5,pady=5)
neutronv_entry = tkinter.Entry(frame_4)
neutronv_entry.grid(row=0,column=1,padx=5,pady=5)


button_8 = tkinter.Button(frame_4,text="Calculate wavelength",command=neutron_wavelength_v,font=('Sans-serif',10))
button_8.grid(row=2,column=1)

result_label_8 = tkinter.Label(frame_4,text="")
result_label_8.grid(row=3)

neutron_ke_label_1 = tkinter.Label(frame_4,text="Enter the value of the kinetic energy in eV",font=('Sans-serif',11,"bold"))
neutron_ke_label_1.grid(row=6,column=0,padx=5,pady=5)
neutron_ke_entry = tkinter.Entry(frame_4)
neutron_ke_entry.grid(row=6,column=1,padx=5,pady=5)

button_9 = tkinter.Button(frame_4,text="Calculate wavelength",command=neutron_wavelength_ke,font=('Sans-serif',10))
button_9.grid(row=7,column=1,padx=5,pady=5)

result_label_9 = tkinter.Label(frame_4,text="")
result_label_9.grid(row=8)

neutron_p_label_1 = tkinter.Label(frame_4,text="Enter the value of the momentum (without units)",font=('Sans-serif',11,"bold"))
neutron_p_label_1.grid(row=10,column=0,padx=5,pady=5)
neutron_p_entry = tkinter.Entry(frame_4)
neutron_p_entry.grid(row=10,column=1, padx=5,pady=5)

button_10 = tkinter.Button(frame_4, command=neutron_wavelength_p, font=('Sans-serif',10),text="Calculate wavelength")
button_10.grid(row=11,column=1,padx=5,pady=5)

result_label_10 = tkinter.Label(frame_4,text="")
result_label_10.grid(row=12)



###frame 5
frame_5= tkinter.Frame(my_notebook)
my_notebook.add(frame_5, text = "Proton`s de-Broglie Wavelength")

protonv_label_1 = tkinter.Label(frame_5,text="Enter the velocity of proton (without units)",font=('Sans-serif',11,"bold"))
protonv_label_1.grid(row=0,column=0,padx=5,pady=5)
protonv_entry = tkinter.Entry(frame_5)
protonv_entry.grid(row=0,column=1,padx=5,pady=5)

button_11 = tkinter.Button(frame_5,text="Calculate wavelength",command=proton_wavelength_v,font=('Sans-serif',10))
button_11.grid(row=2,column=1)

result_label_11 = tkinter.Label(frame_5,text="")
result_label_11.grid(row=3)

proton_ke_label_1 = tkinter.Label(frame_5,text="Enter the value of the kinetic energy in eV",font=('Sans-serif',11,"bold"))
proton_ke_label_1.grid(row=6,column=0,padx=5,pady=5)
proton_ke_entry = tkinter.Entry(frame_5)
proton_ke_entry.grid(row=6,column=1,padx=5,pady=5)

button_12 = tkinter.Button(frame_5,text="Calculate wavelength",command=proton_wavelength_ke,font=('Sans-serif',10))
button_12.grid(row=7,column=1,padx=5,pady=5)

result_label_12 = tkinter.Label(frame_5,text="")
result_label_12.grid(row=8)


proton_p_label_1 = tkinter.Label(frame_5,text="Enter the value of the momentum (without units)",font=('Sans-serif',11,"bold"))
proton_p_label_1.grid(row=10,column=0,padx=5,pady=5)
proton_p_entry = tkinter.Entry(frame_5)
proton_p_entry.grid(row=10,column=1, padx=5,pady=5)

button_13 = tkinter.Button(frame_5, command=proton_wavelength_p, font=('Sans-serif',10),text="Calculate wavelength")
button_13.grid(row=11,column=1,padx=5,pady=5)

result_label_13 = tkinter.Label(frame_5,text="")
result_label_13.grid(row=12)


###frame 6 

frame_6 = tkinter.Frame(my_notebook)
my_notebook.add(frame_6,text = "Nuclei & Bohr Radius")

nr_label1= tkinter.Label(frame_6,text="Enter the symbol of element",font=('Sans-serif',11,"bold"))
nr_label1.grid(row=0,column=0,padx=5,pady=5)
nr_entry1 = tkinter.Entry(frame_6)
nr_entry1.grid(row=0, column=1)

nr_label2= tkinter.Label(frame_6,text="Enter the atomic number of the nuclei",font=('Sans-serif',11,"bold"))
nr_label2.grid(row=1,column=0,padx=5,pady=5)
nr_entry2 = tkinter.Entry(frame_6)
nr_entry2.grid(row=1, column=1)

nr_label3= tkinter.Label(frame_6,text="Enter the mass number of the nuclei",font=('Sans-serif',11,"bold"))
nr_label3.grid(row=2,column=0,padx=5,pady=5)
nr_entry3 = tkinter.Entry(frame_6)
nr_entry3.grid(row=2, column=1)

button_14 = tkinter.Button(frame_6,command=nuclear_radius,text="Calculate Nuclear Radius",font=('Sans-serif',10))
button_14.grid(row=3,column=1,padx=5,pady=5)


result_label_14 = tkinter.Label(frame_6,text="")
result_label_14.grid(row=5)


br_label1 = tkinter.Label(frame_6, text="Please enter the energy level of the electron",font=('Sans-serif',11,"bold"))
br_label1.grid(row = 7, column=0,padx=5,pady=5)
br_entry = tkinter.Entry(frame_6)
br_entry.grid(row=7, column=1)

button_15 = tkinter.Button(frame_6,text="Calculate Bohr Radius",command="",font=('Sans-serif',10))
button_15.grid(row=8, column=1,padx=5,pady= 5 )


result_label_15 = tkinter.Label(frame_6,text ="")
result_label_15.grid(row = 10)


## frame 7 
frame_7 = tkinter.Frame(my_notebook)
my_notebook.add(frame_7, text = "Thermodynamics")


td_label1 = tkinter.Label(frame_7, text="Enter temperature",font=('Sans-serif',10,"bold"))
td_label1.grid(row=0,column=0,padx=5,pady=5)

td_entry1 = tkinter.Entry(frame_7)
td_entry1.grid(row=0,column=1,padx=5,pady=5)

button_16 = tkinter.Button(frame_7,text="°F to °C",font=('Sans-serif',10),command=fah_to_cel)
button_16.grid(row=1 ,column=1,sticky='ew')

result_label_16 = tkinter.Label(frame_7,text="")
result_label_16.grid(row=3)

button_17 = tkinter.Button(frame_7, text="°C to °F",command=cel_to_fah,font=('Sans-serif',10))
button_17.grid(row=1,column=2)

result_label_17 = tkinter.Label(frame_7, text= "")
result_label_17.grid(row=4)


button_18 = tkinter.Button(frame_7,text="°C to K", command=cel_to_k,font=('Sans-serif',10))
button_18.grid(row=1,column=3)


result_label_18 = tkinter.Label(frame_7, text="")
result_label_18.grid(row=5)

button_19= tkinter.Button(frame_7,text="°F to K",command=fah_to_k,font=('Sans-serif',10))
button_19.grid(row=1,column=4)

result_label_19 = tkinter.Label(frame_7,text="")
result_label_19.grid(row=6)

header_label = tkinter.Label(frame_7,text="Ideal Gas Law",font=('Sans-serif',13,"bold"))
header_label.grid(row= 9,column=0,padx=5,pady=5)

instruction_label = tkinter.Label(frame_7,text="Enter 0 for the parameter you want to calculate",font=('Sans-serif',11,"bold"))
instruction_label.grid(row=11,column=0,padx=5,pady=5)

ideal_label1 = tkinter.Label(frame_7, text="Enter the of Pressure of the gas(without units)",font=('Sans-serif',10,"bold"))
ideal_label1.grid(row=14, column=0,padx=5,pady=5)

ideal_gas_P_entry = tkinter.Entry(frame_7)
ideal_gas_P_entry.grid(row=14, column=1, padx=5, pady=5)

ideal_label2 = tkinter.Label(frame_7,text="Enter the Volume of the gas in m³(without units)",font=('Sans-serif',10,"bold"))
ideal_label2.grid(row=15, column=0,padx= 5,pady=5)

ideal_gas_V_entry = tkinter.Entry(frame_7)
ideal_gas_V_entry.grid(row=15, column=1,padx=5,pady=5)

ideal_label3 = tkinter.Label(frame_7, text="Enter the number of moles of the gas(without units)",font=('Sans-serif',10,"bold"))
ideal_label3.grid(row=16,column=0,padx=5,pady=5)

ideal_gas_n_entry = tkinter.Entry(frame_7)
ideal_gas_n_entry.grid(row=16,column=1,padx=5,pady=5)

ideal_label4 = tkinter.Label(frame_7,text="Enter the temperature of the gas(in K)",font=('Sans-serif',10,"bold"))
ideal_label4.grid(row=17,column=0,padx=5,pady=5)

ideal_gas_T_entry = tkinter.Entry(frame_7)
ideal_gas_T_entry.grid(row=17,column=1)

ideal_button = tkinter.Button(frame_7,command=ideal_gas_law,font=('Sans-serif',10),text="Calculate")
ideal_button.grid(row=18,column=1)

result_label_ideal_gas = tkinter.Label(frame_7,text="")
result_label_ideal_gas.grid(row=20)


eng_label1 = tkinter.Label(frame_7,text="Efficiency of a Carnot Engine",font=('Sans-serif',13,"bold"))
eng_label1.grid(row = 25, column=0 ,padx=5,pady=5)

eng_label2 = tkinter.Label(frame_7,text="Temperature of cold reservoir(in Kelvin)",font=('Sans-serif',10,"bold"))
eng_label2.grid(row=27,column=0)

eng_entry1 =tkinter.Entry(frame_7)
eng_entry1.grid(row=27,column=1,padx=5,pady=5)

eng_label3 = tkinter.Label(frame_7,text="Temperature of hot reservoir(in Kelvin)",font=('Sans-serif',10,"bold"))
eng_label3.grid(row=28,column=0,padx=5,pady=5)

eng_entry2 = tkinter.Entry(frame_7)
eng_entry2.grid(row=28, column=1,padx=5,pady=5)

eng_button = tkinter.Button(frame_7,command=carnot_efficiency,text="Calculate Efficiency",font=('Sans-serif',10))
eng_button.grid(row=29,column=1)

eng_result_label = tkinter.Label(frame_7,text="")
eng_result_label.grid(row = 31)


windows.mainloop()