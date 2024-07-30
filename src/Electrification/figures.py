import plotly.express as px
import plotly.graph_objects as go
import plotly.io as pio
import pandas as pd
import numpy as np    
import json
import os 
pd.options.mode.chained_assignment = None 

# ---------------------------------------------------------------------------------------------------------------------------------------------------
# Battery Plots 
# ---------------------------------------------------------------------------------------------------------------------------------------------------
def generate_battery_scatter_plot(Commercial_Batteries,selected_brand,selected_chemistry,selected_x_axis,selected_y_axis,switch_off): 
    template             = pio.templates["minty"] if switch_off else pio.templates["minty_dark"]  
    unique_brands        = list(Commercial_Batteries['Brand'][1:].unique())
    unique_chemistries   = list(Commercial_Batteries['Chemistry'][1:].unique())
    marker_size          = 15
    opacity_ratio        = 0.8 if switch_off else 1.0
    font_size            = 16 

    # Brand Colors: greenyellow, aquamarine, paleturquoise, lightcoral, yellow, lavender ,thistle ,orangered   
    Brand_Colors      = px.colors.qualitative.Pastel 
    Chemistry_Markers = ['square','x','circle','cross','diamond','triangle-up','triangle-down','star','hourglass'] 
    fig = go.Figure()
    if selected_brand == 'All' and  selected_chemistry == 'All':
        # for each Brand 
        for i in range(len(unique_brands)): 
            # for each chemsitry 
            for j in range(len(unique_chemistries)):
                data_1 = Commercial_Batteries.loc[ Commercial_Batteries['Brand'] == unique_brands[i]] 
                data_2 = data_1.loc[Commercial_Batteries['Chemistry'] == unique_chemistries[j]]  
                models = data_2["Model"] 
                config = data_2["Configuration"]                
                fig.add_trace(go.Scatter( x        = np.array(data_2[selected_x_axis]), 
                                     y             = np.array(data_2[selected_y_axis]),  
                                     mode          = 'markers', 
                                     name          ="",                                    
                                     marker        = dict(size=marker_size,color=Brand_Colors[i],opacity=opacity_ratio,symbol = Chemistry_Markers[j]),
                                     hovertemplate = 'Brand: ' + unique_brands[i] + '<br>' + 'Chemistry: ' + unique_chemistries[j] + '<br>' + 'Configuration: ' + config + '<br>' + 'Model: ' + models + '<br>' + selected_x_axis + ': %{x} <br>' + selected_y_axis + ': %{y}',
                                     )) 
    elif selected_brand != 'All' and  selected_chemistry == 'All':
        # for each Brand  
        for j in range(len(unique_chemistries)):
            data_1   = Commercial_Batteries.loc[ Commercial_Batteries['Brand'] == selected_brand] 
            data_2   = data_1.loc[Commercial_Batteries['Chemistry'] == unique_chemistries[j]]  
            i_index  = unique_brands.index(selected_brand)
            models   = data_2["Model"]
            config   = data_2["Configuration"]
            fig.add_trace(go.Scatter( x             = np.array(data_2[selected_x_axis]), 
                                 y             = np.array(data_2[selected_y_axis]),  
                                 mode          = 'markers',
                                 name          = "",            
                                 marker        = dict(size=marker_size,color=Brand_Colors[i_index ],opacity=opacity_ratio,symbol = Chemistry_Markers[j]),
                                 hovertemplate = 'Brand: ' + selected_brand + '<br>' + 'Chemistry: ' + unique_chemistries[j] + '<br>' + 'Configuration: ' + config + '<br>' + 'Model: ' + models + '<br>' + selected_x_axis + ': %{x} <br>' + selected_y_axis + ': %{y}',
                                 ))
    elif selected_brand == 'All' and selected_chemistry != 'All':
        # for each Brand 
        for i in range(len(unique_brands)):  
            data_1   = Commercial_Batteries.loc[ Commercial_Batteries['Brand'] == unique_brands[i]] 
            data_2   = data_1.loc[Commercial_Batteries['Chemistry'] == selected_chemistry] 
            j_index  = unique_chemistries.index(selected_chemistry)
            models   = data_2["Model"]
            config   = data_2["Configuration"]
            fig.add_trace(go.Scatter( x             = np.array(data_2[selected_x_axis]), 
                                 y             = np.array(data_2[selected_y_axis]),  
                                 mode          = 'markers',
                                 name          = "",      
                                 marker        = dict(size=marker_size,color=Brand_Colors[i],opacity=opacity_ratio,symbol = Chemistry_Markers[j_index]),
                                 hovertemplate = 'Brand: ' + unique_brands[i] + '<br>' + 'Chemistry: ' + selected_chemistry + '<br>' + 'Configuration: ' + config + '<br>' + 'Model: ' + models + '<br>' + selected_x_axis + ': %{x} <br>' + selected_y_axis + ': %{y}',
                                 ))
    else:
        data_1  = Commercial_Batteries.loc[ Commercial_Batteries['Brand'] == selected_brand ] 
        data_2  = data_1.loc[Commercial_Batteries['Chemistry'] == selected_chemistry] 
        i_index = unique_brands.index(selected_brand)
        j_index = unique_chemistries.index(selected_chemistry)
        models  = data_2["Model"]
        config  = data_2["Configuration"]
        fig.add_trace(go.Scatter( x        = np.array(data_2[selected_x_axis]), 
                             y             = np.array(data_2[selected_y_axis]),  
                             mode          = 'markers', 
                             name          = "",       
                             marker        = dict(size=marker_size,color=Brand_Colors[i_index],opacity=opacity_ratio,symbol = Chemistry_Markers[j_index]),
                             hovertemplate = 'Brand: ' + selected_brand  + '<br>' + 'Chemistry: ' + selected_chemistry + '<br>' + 'Configuration: ' + config + '<br>' + 'Model: ' + models  + '<br>' + selected_x_axis + ': %{x} <br>' + selected_y_axis + ': %{y}',
                             ))
 
    fig.update_layout(xaxis_title = selected_x_axis,
                       yaxis_title = selected_y_axis,
                       showlegend  = False, 
                       height      = 400,
                       margin      ={'t':0,'l':0,'b':0,'r':0},
                       font=dict(  size=font_size ),  
                       )     
    fig["layout"]["template"] = template 
    return fig 

def generate_battery_spider_plot(Commercial_Batteries,bat_1,bat_2,bat_3,switch_off): 
    template     = pio.templates["minty"] if switch_off else pio.templates["minty_dark"]   

    metrics_list  = ['Gravimetric Power Density (W/kg)' ,'Maximum Voltage (V)','Capacity (mAh)','Maximum Discharge Current (A)','Maximum Discharge Power (W)', 'Gravimetric Energy Density (Wh/kg)']    
    font_size     = 16     
    data_1        = Commercial_Batteries.loc[Commercial_Batteries['Battery Name'] == bat_1] 
    vals_1        = np.zeros((1,7))
    vals_1[:,:6]  = np.array(data_1[metrics_list])
    vals_1[0,6]   = vals_1[0,0]    
        
    data_2       = Commercial_Batteries.loc[ Commercial_Batteries['Battery Name'] == bat_2]  
    vals_2       = np.zeros((1,7))
    vals_2[:,:6] = np.array(data_2[metrics_list]) 
    vals_2[0,6]  = vals_2[0,0]   

    data_3       = Commercial_Batteries.loc[ Commercial_Batteries['Battery Name'] == bat_3]  
    vals_3       = np.zeros((1,7))
    vals_3[:,:6] = np.array(data_3[metrics_list]) 
    vals_3[0,6]  = vals_3[0,0] 
    
    # Stack data
    battery_data = np.vstack((vals_1,vals_2 ))    
    battery_data = np.vstack((battery_data,vals_3))    
     
    scaling = np.array([np.maximum(1000,np.max(battery_data[:,0])*1.05),
                        np.maximum(5,np.max(battery_data[:,1])*1.05) ,
                        np.maximum(5000,np.max(battery_data[:,2])*1.05),
                        np.maximum(20,np.max(battery_data[:,3])*1.05), 
                        np.maximum(50,np.max(battery_data[:,4])*1.05),
                        np.maximum(500,np.max(battery_data[:,5])*1.05),
                        np.maximum(1000,np.max(battery_data[:,6])*1.05)])
    scaling = np.tile(scaling[:,None],(1,3)).T
    fig = go.Figure()  
    
    scaled_data = np.zeros((2,len(scaling))) 
    scaled_data = battery_data/scaling 
    fig.add_trace(
                go.Scatterpolar(
                                r    = scaled_data[0],
                                theta=['Power Density <br>  (W/kg)' ,
                                       'Max Voltage <br>   (V)',
                                       'Capacity <br>  (mAh)',
                                       'Max. Discharge<br> Current (A)',
                                       'Max. Discharge <br> Power (W)',
                                       'Energy Density <br>  (Wh/kg)',
                                       'Power Density <br>  (W/kg)' ], 
                                fill      ='toself', 
                                name      = 'Battery Cell 1', 
                                marker    = None,
                                line=dict(color=px.colors.qualitative.Pastel[0],width = 4),  
                                showlegend=True, 
                                )
                )
    

    fig.add_trace(
                go.Scatterpolar(
                                r    = scaled_data[1],
                                theta=['Power Density <br>  (W/kg)' ,
                                       'Max Voltage <br>   (V)',
                                       'Capacity <br>  (mAh)',
                                       'Max. Discharge<br> Current (A)',
                                       'Max. Discharge <br> Power (W)',
                                       'Energy Density <br>  (Wh/kg)',
                                       'Power Density <br>  (W/kg)' ], 
                                fill      ='toself', 
                                name      = 'Battery Cell 2', 
                                marker    = None,
                                line=dict(color=px.colors.qualitative.Pastel[1],width = 4), 
                                showlegend=True, 
                                )
                )        


    fig.add_trace(
                go.Scatterpolar(
                                r    = scaled_data[2],
                                theta=['Power Density <br>  (W/kg)' ,
                                       'Max Voltage <br>   (V)',
                                       'Capacity <br>  (mAh)',
                                       'Max. Discharge<br> Current (A)',
                                       'Max. Discharge <br> Power (W)',
                                       'Energy Density <br>  (Wh/kg)',
                                       'Power Density <br>  (W/kg)' ], 
                                fill      ='toself', 
                                name      = 'Battery Cell 3', 
                                marker    = None,
                                line=dict(color=px.colors.qualitative.Pastel[4],width = 4),   
                                showlegend=True, 
                                )
                )        

    fig.update_layout(height      = 400, 
                       margin={'t':50},
                       font=dict(  size=font_size ),  
                           )            
    fig.update_polars(radialaxis=dict(visible=False,range=[0, 1]))  
    fig["layout"]["template"] = template 
    return fig 


def generate_battery_dev_map(Battery_Development,selected_sector,selected_type,switch_off): 
    template            = pio.templates["minty"] if switch_off else pio.templates["minty_dark"]    
    map_style           = None if switch_off else 'dark' 
    unique_sectors      = ['Industry', 'Academia', 'Government']
    unique_types        = ['Li-Ion','Li-Sulphur','Metal-Air','Li-Silicon']  
    sector_colors       = px.colors.qualitative.Pastel 
    mapbox_access_token = "pk.eyJ1IjoibWFjbGFya2UiLCJhIjoiY2xyanpiNHN6MDhsYTJqb3h6YmJjY2w5MyJ9.pQed7pZ9CnJL-mtqm1X8DQ" 
    
    fig = go.Figure()
    if selected_sector == 'All' and  selected_type == 'All': 
        for i in range(len(unique_sectors)):
            for j in range(len(unique_types)):
                data_1 = Battery_Development.loc[Battery_Development['Sector'] == unique_sectors[i]] 
                data_2 = data_1.loc[Battery_Development[unique_types[j]] == 1]   
                fig2   = px.scatter_mapbox(data_2, lat="Latitude", lon="Longitude",
                                          hover_name="Entity",
                                          hover_data=["City"],
                                         color_discrete_sequence=[sector_colors[i]], zoom=1 ,)
                fig.add_trace(fig2.data[0])
    
    elif selected_sector == 'All' and  selected_type != 'All': 
        for i in range(len(unique_sectors)): 
            data_1 = Battery_Development.loc[Battery_Development['Sector'] == unique_sectors[i]] 
            data_2 = data_1.loc[Battery_Development[selected_type] == 1]   
            fig2   = px.scatter_mapbox(data_2, lat="Latitude", lon="Longitude",
                                      hover_name="Entity",
                                      hover_data=["City"],
                                     color_discrete_sequence=[sector_colors[i]], zoom=1 ,)
            fig.add_trace(fig2.data[0])
            
    
    elif selected_sector != 'All' and  selected_type == 'All': 
        color_idx = unique_sectors.index(selected_sector)
        for j in range(len(unique_sectors)): 
            data_1 = Battery_Development.loc[Battery_Development['Sector'] == selected_sector] 
            data_2 = data_1.loc[Battery_Development[unique_types[j]] == 1]  
            fig2   = px.scatter_mapbox(data_2, lat="Latitude", lon="Longitude",
                                      hover_name="Entity",
                                      hover_data=["City"],
                                     color_discrete_sequence=[sector_colors[color_idx]], zoom=1 ,)
            fig.add_trace(fig2.data[0])      
    
    else:  
        color_idx = unique_sectors.index(selected_sector)
        data_1    = Battery_Development.loc[Battery_Development['Sector'] == selected_sector] 
        data_2    = data_1.loc[Battery_Development[selected_type] == 1]
        fig2      = px.scatter_mapbox(data_2, lat="Latitude", lon="Longitude",
                                  hover_name="Entity",
                                  hover_data=["City"],
                                 color_discrete_sequence=[sector_colors[color_idx]], zoom=1 ,)
        fig.add_trace(fig2.data[0])          

    
    fig.update_traces(marker={"size": 10})
    fig.update_layout(mapbox_style  = "open-street-map",      
                      showlegend    = False, 
                      height        = 300, 
                      margin        = {'t':0,'l':0,'b':0,'r':0}, 
                      mapbox        = dict( accesstoken=mapbox_access_token,style=map_style,
                                          center=go.layout.mapbox.Center( lat=20, lon= 200 ))  )     

    fig["layout"]["template"] = template 
    return fig

# ---------------------------------------------------------------------------------------------------------------------------------------------------
# Flight Operations Plots 
# ---------------------------------------------------------------------------------------------------------------------------------------------------
 
def generate_US_bat_temperature_map(US_Temperature_F,month_no,switch_off):  
    template  = pio.templates["minty"] if switch_off else pio.templates["minty_dark"]    
    font_size = 16
    separator = os.path.sep
    file_path = '..'+ separator +'Data'+ separator +'US_County'+ separator +'counties_fips.json'
    f = open(file_path) 
    counties = json.load(f) 
    month = list(US_Temperature_F.columns.values)[6:18][month_no]  
    US_Temperature_F['FIPS'] = US_Temperature_F['FIPS'].apply('{:0>5}'.format)
    us_temperature_map= px.choropleth(US_Temperature_F, geojson=counties, locations='FIPS', color = month,
                           color_continuous_scale="RdYlBu_r", 
                           hover_data=["Name","State", month],
                           scope='usa',
                           range_color=(0, 90),  
                          )   
    us_temperature_map.update_layout(coloraxis_colorbar=dict(title=" "),
                                     coloraxis_colorbar_x=0.85, 
                                     height    = 400, 
                                     margin={'t':0,'l':0,'b':0,'r':0},                              
                              )  
    us_temperature_map.update_coloraxes( colorbar_tickvals= np.linspace(0,90,11),
                                        colorbar_tickfont_size=font_size) 

    us_temperature_map["layout"]["template"] = template     
    return us_temperature_map


def generate_flight_ops_map(Routes_and_Temp,Commercial_Batteries,aircraft,battery_choice,weight_fraction,system_voltage,propulsive_efficiency,percent_adoption,month_no,cost_of_electricity,switch_off): 
    mapbox_access_token  = "pk.eyJ1IjoibWFjbGFya2UiLCJhIjoiY2xyanpiNHN6MDhsYTJqb3h6YmJjY2w5MyJ9.pQed7pZ9CnJL-mtqm1X8DQ"     
    map_style            = None if switch_off else 'dark'  
    template             = pio.templates["minty"] if switch_off else pio.templates["minty_dark"]    
    font_size            = 16      

    if aircraft == 'ATR 72-600': 
        P_max           = 1568083 
        W_0             = 23000   
        thrust_coef     = 0.000017678 # incorrect  
        fuel_volume     = 6410.2
        fuel_economy    = 3.27 
        passengers      = 72 
        CL_cruise       = 0.55   # incorrect  
        CD_cruise       = 0.035  # incorrect  
        S_ref           = 61.0   
        L_div_D         = CL_cruise/CD_cruise 
        
    #elif aircraft == 'Embraer 190': 
        #P_max           =  
        #W_0             = 52290 
        #thrust_coef     = 0.000017678 # incorrect    
        #fuel_volume     = 16629 
        #fuel_economy    = 3.54 
        #passengers      = 100 
        #CL_cruise       = 0.55   # incorrect 
        #CD_cruise       = 0.035  # incorrect 
        #S_ref           = 92.53 
        #L_div_D         = CL_cruise/CD_cruise  
        
    elif aircraft == "Boeing 737 MAX-8":
        P_max           = 15000000 
        W_0             = 79015.8   
        thrust_coef     = 0.000017678  
        fuel_volume     = 26024 
        fuel_economy    = 2.04 
        passengers      = 162  
        CL_cruise       = 0.55 
        CD_cruise       = 0.035
        S_ref           = 127 
        L_div_D         = CL_cruise/CD_cruise
        
    elif aircraft == 'Airbus A320 neo': 
        P_max           = 15000000 
        W_0             = 78000
        thrust_coef     = 0.000017678  
        fuel_volume     = 26024  
        fuel_economy    = 2.04  
        passengers      = 162
        W_0             = 79015.8  
        CL_cruise       = 0.55 
        CD_cruise       = 0.035
        S_ref           = 127   
        L_div_D         = CL_cruise/CD_cruise
        
    #elif aircraft == "Boeing 787-8": 
        #P_max           =  
        #thrust_coef     = 0.000017678 
        #fuel_volume     = 126206  
        #fuel_economy    = 2.68    
        #passengers      = 238
        #W_0             = 227900   
        #CL_cruise       = 0.055 
        #CD_cruise       = 0.035
        #S_ref           = 377
        #L_div_D         = CL_cruise/CD_cruise
        
    #elif aircraft == 'Airbus A350-1000':
        #P_max          =  
        #thrust_coef    = 0.000017678   
        #fuel_volume    = 166488        # liters 
        #fuel_economy   = 2.85          # L/100km per Pax 
        #passengers     = 327  
        #W_0            = 322050  
        #CL_cruise      = 0.055 
        #CD_cruise      = 0.035
        #S_ref          = 464.3
        #L_div_D        = CL_cruise/CD_cruise      
             
    CO2e_per_passenger_mile     = 0.0002         # in Ton  0.4 lb per passenger/ mile  Refhttps://8billiontrees.com/carbon-offsets-credits/carbon-ecological-footprint-calculators/carbon-footprint-driving-vs-flying/#:~:text=It%20is%20estimated%20that%20the,2%20per%20mile%20per%20passenger.
    Wh_per_kg_to_J              = 3600.0
    Ah_to_C                     = 3600.0  
    V_bat                       = system_voltage*1000
    eta_0                       = propulsive_efficiency/100 
    
    #================================================================================================================================================  
    # Compute Feasible Routes 
    #================================================================================================================================================    
    # Compute Range
    data            = Commercial_Batteries[Commercial_Batteries['Battery Name'] == battery_choice]  
    data            = Commercial_Batteries[Commercial_Batteries['Battery Name'] == battery_choice] 
    V_cell          = np.array(data['Nominal Voltage (V)'])[0]
    e_cell          = np.array(data['Gravimetric Energy Density (Wh/kg)'])[0] *Wh_per_kg_to_J
    q_cell          = np.array(data['Capacity (mAh)'])[0]/1000 * Ah_to_C  # conversion to coulombs
    i_max           = np.array(data['Maximum Discharge Current (A)'])[0] # amps   
    Min_Temp        = np.array(data['Minimum Disharge Temperature (°C)'])[0]*9/5 + 32
    Max_Temp        = np.array(data['Maximum Discharge Temperature (°C)'])[0]*9/5 + 32  
    I_bat           = P_max/ V_bat
    n_series        = V_bat/V_cell
    W_bat           = (weight_fraction/100) * W_0
    E_bat           = W_bat * e_cell  
    Q_bat           = E_bat /V_bat
    n_parallel      = Q_bat/q_cell 
    n_parallel_min  = I_bat/i_max 
    
    if n_parallel_min  <  n_parallel: 
        Range = (e_cell/9.81) * L_div_D * (weight_fraction/100)* eta_0
    else:  
        Range = 0 
    Range_mi = Range * 0.000621371 
    
    # Compute distances between departure and destimation points   
    months               = ['January', 'February', 'March', 'April', 'May', 'June', 'July','August', 'September', 'October', 'November', 'December']      
    month                = months[month_no]  
    
    
    Routes_and_Temp_Mo                   = Routes_and_Temp[Routes_and_Temp['Month'] == month_no+1 ]     
    Jet_A_density                        = 800.0 #  kg/m3
    fuel_volume_L                        = Routes_and_Temp_Mo['Fuel Consumed Per Flight (Liters)']  
    fuel_volume_m_3                      = fuel_volume_L*0.001  
    W_f                                  = Jet_A_density*fuel_volume_m_3
    W_residual                           = W_bat-W_f  
    weight_per_pass                      = 158.757 # in kg  (250 lb for person, 100 lb for luggage) 
    passenger_reductions                 = np.ceil(np.array(W_residual)/weight_per_pass)   
    passenger_reductions[passenger_reductions < 0] = 0
    original_Pax_volume                  = np.array(Routes_and_Temp_Mo['Passengers'])
    remaining_Pax                        = original_Pax_volume - passenger_reductions*np.array(Routes_and_Temp_Mo['No of Flights Per Month'])
    remaining_Pax[remaining_Pax<0]       = 0
    Routes_and_Temp_Mo['E_Passengers']   = remaining_Pax   

    Feasible_Routes_0    = Routes_and_Temp_Mo[Routes_and_Temp_Mo['E_Passengers'] > 0 ] 
    Infeasible_Routes_0  = Routes_and_Temp_Mo[Routes_and_Temp_Mo['E_Passengers'] < 0 ]   
    Feasible_Routes_1    = Feasible_Routes_0[Feasible_Routes_0['Distance (miles)'] < Range_mi ] 
    Infeasible_Routes_1  = Feasible_Routes_0[Feasible_Routes_0['Distance (miles)'] > Range_mi ]  
    Feasible_Routes_2    = Feasible_Routes_1[Feasible_Routes_1['Origin ' + month] > Min_Temp] 
    Infeasible_Routes_2  = Feasible_Routes_1[Feasible_Routes_1['Origin ' + month] < Min_Temp] 
    Feasible_Routes_3    = Feasible_Routes_2[Feasible_Routes_2['Origin ' + month] < Max_Temp] 
    Infeasible_Routes_3  = Feasible_Routes_2[Feasible_Routes_2['Origin ' + month] > Max_Temp]  
    Feasible_Routes_4    = Feasible_Routes_3[Feasible_Routes_3['Destination ' + month] > Min_Temp] 
    Infeasible_Routes_4  = Feasible_Routes_3[Feasible_Routes_3['Destination ' + month] < Min_Temp] 
    Feasible_Routes_5    = Feasible_Routes_4[Feasible_Routes_4['Destination ' + month] < Max_Temp] 
    Infeasible_Routes_5  = Feasible_Routes_4[Feasible_Routes_4['Destination ' + month] > Max_Temp] 
    Feasible_Routes      = Feasible_Routes_5.head(int(len(Feasible_Routes_5)*percent_adoption/100 )) 
    Infeasible_Routes_6  = Feasible_Routes_5.tail(int(len(Feasible_Routes_5)*(100 - percent_adoption)/100 ))
    Infeasible_Routes    = pd.concat([Infeasible_Routes_0,Infeasible_Routes_1,Infeasible_Routes_2,Infeasible_Routes_3,Infeasible_Routes_4,Infeasible_Routes_5,Infeasible_Routes_6])    
        
    #================================================================================================================================================  
    # Plot Routes 
    #================================================================================================================================================          
    # Routes     
    fig_4                = go.Figure()
    airport_marker_size  = 5
    airport_marker_color = "white"
    colors               = px.colors.qualitative.Pastel  
 
    # Flight Paths 
    lons       = np.empty(3 * len(Infeasible_Routes))
    lons[::3]  = Infeasible_Routes['Origin Longitude (Deg.)']
    lons[1::3] = Infeasible_Routes['Destination Longitude (Deg.)']
    lons[2::3] = None
    lats       = np.empty(3 * len(Infeasible_Routes))
    lats[::3]  = Infeasible_Routes['Origin Latitude (Deg.)']
    lats[1::3] = Infeasible_Routes['Destination Latitude (Deg.)']
    lats[2::3] = None    
  
    fig_4.add_trace(
        go.Scattergeo( 
            lon = lons,
            lat = lats,
            mode = 'lines',
            line = dict(width = 0.1,color = 'grey'),))
    
    lons       = np.empty(3 * len(Feasible_Routes))
    lons[::3]  = Feasible_Routes['Origin Longitude (Deg.)']
    lons[1::3] = Feasible_Routes['Destination Longitude (Deg.)']
    lons[2::3] = None
    lats       = np.empty(3 * len(Feasible_Routes))
    lats[::3]  = Feasible_Routes['Origin Latitude (Deg.)']
    lats[1::3] = Feasible_Routes['Destination Latitude (Deg.)']
    lats[2::3] = None    
  
    fig_4.add_trace(
        go.Scattergeo( 
            lon = lons,
            lat = lats,
            mode = 'lines',
            line = dict(width = 2,color = "aquamarine"),)) 
 
    # Airports  
    fig_4.add_trace(go.Scattergeo( 
        lon = Routes_and_Temp['Destination Longitude (Deg.)'],
        lat = Routes_and_Temp['Destination Latitude (Deg.)'], 
        text = Routes_and_Temp['Destination City'],
        mode = 'markers',
        marker = dict(
            size = airport_marker_size,
            color = airport_marker_color,))) 

    fig_4.add_trace(go.Scattergeo( 
        lon = Routes_and_Temp['Origin Longitude (Deg.)'],
        lat = Routes_and_Temp['Origin Latitude (Deg.)'], 
        text = Routes_and_Temp['Origin City'],
        mode = 'markers',
        marker = dict(
            size = airport_marker_size,
            color = airport_marker_color, ))) 
     
    # Flight Paths 
    fig_4.update_layout(mapbox_style  = "open-street-map",      
                      showlegend    = False, 
                      height        = 400, 
                      geo_scope     ='usa',
                      margin        = {'t':0,'l':0,'b':0,'r':0},  
                      mapbox        = dict( accesstoken=mapbox_access_token,style=map_style,
                                            center=go.layout.mapbox.Center( lat=30, lon= 230 ))  )     
    #================================================================================================================================================      
    # Passenger vs Distance Traveled 
    #================================================================================================================================================     
    fig_5               = go.Figure() 
    fig_5.add_trace(go.Histogram(histfunc="sum",
                               x= Feasible_Routes['Distance (miles)'],
                               y = Feasible_Routes['E_Passengers'],
                               name='All-Electric', 
                               xbins=dict(start=0, end=4000, size=500),
                               marker_color=colors[0],))
    fig_5.add_trace(go.Histogram(histfunc="sum",
                               x= Infeasible_Routes['Distance (miles)'],
                               y = Infeasible_Routes['Passengers'],
                               name='Fossil Fuels',  
                               xbins=dict(start=0, end=4000, size=500),
                               marker_color=colors[10],)) 
    
    # The two histograms are drawn on top of another
    fig_5.update_layout(barmode='stack', 
                      xaxis_title_text='Distance (miles)', 
                      yaxis_title_text='Passengers',
                      height        = 300, 
                      width         = 600, 
                      margin        = {'t':0,'l':0,'b':0,'r':0},  
                      bargap        = 0.1, 
                      yaxis=dict(range=[0,3E6], autorange=False),  
                      font=dict(  size=font_size ),
                      legend=dict(
                          yanchor="top",
                          y=0.99,
                          xanchor="center",
                          x=0.85 ))   

    #================================================================================================================================================      
    # Busiest Airports 
    #================================================================================================================================================    
    fig_6 = go.Figure()  
    Airport_Routes     = Feasible_Routes[['E_Passengers','Origin Airport','Destination City']]
    Cumulative_Flights = Airport_Routes.groupby(['Origin Airport']).sum()
    Busiest_Airports   = Cumulative_Flights.sort_values(by=['E_Passengers'], ascending = False).head(10) 
    Alphabetical_List  = Busiest_Airports.sort_values(by=['Origin Airport'])  
    fig_6.add_trace(go.Bar( x=list(Alphabetical_List['E_Passengers'].index),
                       y=np.array(Alphabetical_List['E_Passengers']),
                       marker_color=colors[0])) 
    fig_6.update_layout(xaxis_title_text='Airport', 
                      yaxis_title_text='Passengers', 
                      height        = 300, 
                      width         = 600, 
                      yaxis=dict(range=[0,5E4], autorange=False), 
                      margin        = {'t':0,'l':0,'b':0,'r':0},  
                      bargap        = 0.1,
                      font=dict(  size=font_size ))  

    #================================================================================================================================================      
    # Determine Ratio of Electrified to Jet-A Routes
    #================================================================================================================================================    
    fig_7                       = go.Figure()
    Feasible_Passenger_Miles    = np.sum(np.array(Feasible_Routes['E_Passengers'])* np.array(Feasible_Routes['Distance (miles)']))
    Infeasible_Passenger_Miles  = np.sum(np.array(Infeasible_Routes[['Passengers']])* np.array(Infeasible_Routes[['Distance (miles)']])) 
    labels                      = ["All-Electric", "Fossil Fuels"] 
    fig_7.add_trace(go.Pie(labels=labels,
                         values=[Feasible_Passenger_Miles, Infeasible_Passenger_Miles],
                         marker_colors=[colors[0],colors[10]])) 
    fig_7.update_traces(hole=.4, hoverinfo="label+percent+name") 
    fig_7.update_layout( height     = 400, 
                      width         = 600, 
                      margin        = {'t':50,'l':0,'b':0,'r':0},  
                      font=dict(  size=font_size ),
                      legend=dict(
                          yanchor="top",
                          y=0.99,
                          xanchor="center",
                          x=0.95 ))  
     
    #================================================================================================================================================      
    # Monthly Analysis
    #================================================================================================================================================   
    w_electrification   = np.zeros(12)
    w_o_electriciation  = np.zeros(12) 
    CASM_jet_A          = np.zeros(12) 
    CASM_electric       = np.zeros(12) 

    for m_i in range(12): 
        Routes_and_Temp_Mo                   = Routes_and_Temp.loc[Routes_and_Temp['Month'] == m_i+1 ]   
        fuel_volume_L                        = Routes_and_Temp_Mo['Fuel Consumed Per Flight (Liters)']  
        fuel_volume_m_3                      = fuel_volume_L*0.001  
        W_f                                  = Jet_A_density*fuel_volume_m_3
        W_residual                           = W_bat-W_f  
        weight_per_pass                      = 158.757 # in kg  (250 lb for person, 100 lb for luggage) kg 
        passenger_reductions                 = np.ceil(np.array(W_residual)/weight_per_pass)   
        passenger_reductions[passenger_reductions < 0] = 0
        original_Pax_volume                  = np.array(Routes_and_Temp_Mo['Passengers'])
        remaining_Pax                        = original_Pax_volume - passenger_reductions*np.array(Routes_and_Temp_Mo['No of Flights Per Month'])
        remaining_Pax[remaining_Pax<0]       = 0
        Routes_and_Temp_Mo['E_Passengers']   = remaining_Pax  
        
        Feasible_Routes_0    = Routes_and_Temp_Mo[Routes_and_Temp_Mo['E_Passengers'] > 0 ] 
        Infeasible_Routes_0  = Routes_and_Temp_Mo[Routes_and_Temp_Mo['E_Passengers'] < 0 ]   
        Feasible_Routes_1    = Feasible_Routes_0[Feasible_Routes_0['Distance (miles)'] < Range_mi ] 
        Infeasible_Routes_1  = Feasible_Routes_0[Feasible_Routes_0['Distance (miles)'] > Range_mi ]  
        Feasible_Routes_2    = Feasible_Routes_1[Feasible_Routes_1['Origin ' + month] > Min_Temp] 
        Infeasible_Routes_2  = Feasible_Routes_1[Feasible_Routes_1['Origin ' + month] < Min_Temp] 
        Feasible_Routes_3    = Feasible_Routes_2[Feasible_Routes_2['Origin ' + month] < Max_Temp] 
        Infeasible_Routes_3  = Feasible_Routes_2[Feasible_Routes_2['Origin ' + month] > Max_Temp]  
        Feasible_Routes_4    = Feasible_Routes_3[Feasible_Routes_3['Destination ' + month] > Min_Temp] 
        Infeasible_Routes_4  = Feasible_Routes_3[Feasible_Routes_3['Destination ' + month] < Min_Temp] 
        Feasible_Routes_5    = Feasible_Routes_4[Feasible_Routes_4['Destination ' + month] < Max_Temp] 
        Infeasible_Routes_5  = Feasible_Routes_4[Feasible_Routes_4['Destination ' + month] > Max_Temp] 
        Feasible_Routes      = Feasible_Routes_5.head(int(len(Feasible_Routes_5)*percent_adoption/100 )) 
        Infeasible_Routes_6  = Feasible_Routes_5.tail(int(len(Feasible_Routes_5)*(100 - percent_adoption)/100 ))
        Infeasible_Routes    = pd.concat([Infeasible_Routes_0,Infeasible_Routes_1,Infeasible_Routes_2,Infeasible_Routes_3,Infeasible_Routes_4,Infeasible_Routes_5,Infeasible_Routes_6])     

           
        ## concatenate feasible and infeasible routes    
        Infeasible_Passenger_Miles  = np.sum(np.array(Infeasible_Routes[['Distance (miles)']])*np.array(Infeasible_Routes[['Passengers']])       )  
        w_electrification[m_i]      = Infeasible_Passenger_Miles * CO2e_per_passenger_mile  # only infeasbile routes since feasible routes dont pollute! 
        w_o_electriciation[m_i]     =  np.sum( np.array(Routes_and_Temp_Mo[['Distance (miles)']])*np.array(Routes_and_Temp_Mo[['Passengers']]))* CO2e_per_passenger_mile   
        # Infeasible Routes (Fuel) Energy Carrier Cost Per Seat Mile 
        ASM_jet_A             = np.sum(Infeasible_Routes['Distance (miles)'] * Infeasible_Routes['Passengers'])
        Total_Fuel_Cost_jet_A = np.sum(Infeasible_Routes['Fuel Cost'])
        
        # Compute electric CASM
        CASM_jet_A[m_i]       = 100*Total_Fuel_Cost_jet_A/ASM_jet_A    
        
        # Compute electric CASM
        if len(Feasible_Routes['E_Passengers']) == 0:
            electric_flight_passengers = 0
            CASM_electric[m_i]         = 0
        else: 
            electric_flight_passengers = Feasible_Routes['E_Passengers']  
            joule_to_kWh               = 2.77778e-7
            Total_Fuel_Cost_electric   = sum( (E_bat*joule_to_kWh*cost_of_electricity) * np.array(Feasible_Routes['No of Flights Per Month']) )
            ASM_electric               = sum(Feasible_Routes['Distance (miles)'] * electric_flight_passengers)
            CASM_electric[m_i]         = 100*Total_Fuel_Cost_electric/ASM_electric         
               
    
    #================================================================================================================================================      
    # Monthly Emissions
    #================================================================================================================================================                  
    month_names         = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']      
    fig_8               = go.Figure() 
    fig_8.add_trace(go.Scatter(x=month_names, y=w_electrification, name = 'All-Electric Aircraft Fleet',
                             line=dict(color=colors[0], width=4)))  
    fig_8.add_trace(go.Scatter(x=month_names, y=w_o_electriciation, name='Conventional Aircraft Fleet',
                             line=dict(color=colors[10], width=4)))   
    fig_8.update_layout( 
                      height           = 400, 
                      width            = 600, 
                      margin           = {'t':50,'l':0,'b':0,'r':0},
                      yaxis_title_text ='CO2e (Ton)', # yaxis label 
                      font=dict(  size=font_size ),
                      legend=dict(
                          yanchor="top",
                          y=0.99,
                          xanchor="center",
                          x=0.25)) 
    
    #================================================================================================================================================      
    # Cost Per Seat Mile
    #================================================================================================================================================   
    fig_9 = go.Figure()       
    fig_9.add_trace(go.Scatter(x=month_names, y=CASM_jet_A, name='Fossil Fuels',
                             line=dict(color=colors[10], width=4)))  
    fig_9.add_trace(go.Scatter(x=month_names, y=CASM_electric, name = 'All-Electric',
                             line=dict(color=colors[0], width=4)))  
    fig_9.update_layout( 
                      height           = 400, 
                      width            = 600, 
                      margin           = {'t':50,'l':0,'b':0,'r':0},
                      yaxis_title_text ='Cost Per Seat Mile (cents)', # yaxis label
                      yaxis_range      = [0,30],
                      font=dict(  size=font_size ),
                      legend=dict(
                          yanchor="top",
                          y=0.99,
                          xanchor="center",
                          x=0.85 )) 
    
    fig_4["layout"]["template"] = template   
    fig_5["layout"]["template"] = template         
    fig_6["layout"]["template"] = template    
    fig_7["layout"]["template"] = template 
    fig_8["layout"]["template"] = template  
    fig_9["layout"]["template"] = template  
    
    return fig_4,fig_5,fig_6,fig_7,fig_8,fig_9  

# ---------------------------------------------------------------------------------------------------------------------------------------------------
# Motor Plots
# ---------------------------------------------------------------------------------------------------------------------------------------------------
def generate_motor_scatter_plot(Electric_Motor_Development,selected_x_axis,selected_y_axis,switch_off): 
    template             = pio.templates["minty"] if switch_off else pio.templates["minty_dark"]  
    unique_manufacturers = list(Electric_Motor_Development['Manufacturer'][1:].unique())
    unique_motor_types   = list(Electric_Motor_Development['Motor Type'][1:].unique())
    marker_size          = 15
    opacity_ratio        = 0.8 if switch_off else 1.0
    font_size            = 16 

    # Brand Colors: greenyellow, aquamarine, paleturquoise, lightcoral, yellow, lavender ,thistle ,orangered   
    Brand_Colors      = px.colors.qualitative.Pastel 
    Motor_Type_Markers = ['square','x','circle','cross','diamond','triangle-up','triangle-down','star','hourglass'] 
    fig = go.Figure()  
    for i in range(len(unique_manufacturers)):  
        for j in range(len(unique_motor_types)):
            data_1    = Electric_Motor_Development.loc[Electric_Motor_Development['Manufacturer'] == unique_manufacturers[i]] 
            data_2    = data_1.loc[Electric_Motor_Development['Motor Type'] == unique_motor_types[j]]  
            developer = data_2["Manufacturer"]                 
            coolant   = data_2["Coolant"]                 
            fig.add_trace(go.Scatter( x        = np.array(data_2[selected_x_axis]), 
                                 y             = np.array(data_2[selected_y_axis]),  
                                 mode          = 'markers', 
                                 name          ="",                                    
                                 marker        = dict(size=marker_size,color=Brand_Colors[i],opacity=opacity_ratio,symbol = Motor_Type_Markers[j]),
                                 hovertemplate = 'Manufacturer: ' + developer  + '<br>' + 'Motor Type: ' + unique_motor_types[j] + '<br>' + 'Coolant: ' + coolant   + '<br>'  + selected_x_axis + ': %{x} <br>' + selected_y_axis + ': %{y}',
                                 ))  
 
    fig.update_layout(xaxis_title = selected_x_axis,
                       yaxis_title = selected_y_axis,
                       showlegend  = False, 
                       height      = 400,
                       margin      ={'t':0,'l':0,'b':0,'r':0},
                       font=dict(  size=font_size ),  
                       )     
    fig["layout"]["template"] = template 
    return fig 