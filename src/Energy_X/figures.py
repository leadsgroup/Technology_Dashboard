import plotly.express as px
import plotly.graph_objects as go
import plotly.io as pio
import pandas as pd
import numpy as np    
import plotly.graph_objects as go
import json  
import os 

# ---------------------------------------------------------------------------------------------------------------------------------------------------
# Flight Operations Plots 
# ---------------------------------------------------------------------------------------------------------------------------------------------------
 
def generate_US_EX_temperature_map(US_Temperature_F,month_no,switch_off):  
    template             = pio.templates["minty"] if switch_off else pio.templates["minty_dark"]    
    font_size            = 16   
    separator            = os.path.sep
    file_path            = '..'+ separator +'Data'+ separator +'US_County'+ separator +'counties_fips.json'
    f = open(file_path) 
    counties = json.load(f) 
    month = list(US_Temperature_F.columns.values)[3:][month_no] 
    fips  = list(US_Temperature_F['FIPS'])  
    US_Temperature_F['FIPS'] = ["%05d" % i for i in fips] 
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

def generate_EX_aircraft_flight_ops(Routes_and_Temp,TOGW,L_D,Max_P,system_V,weight_fraction,propulsive_efficiency,cell_V,
                                              capacity,cell_C_max,cell_e0,cell_Temp,percent_adoption,month_no,cost_of_electricity,switch_off): 
    mapbox_access_token  = "pk.eyJ1IjoibWFjbGFya2UiLCJhIjoiY2xyanpiNHN6MDhsYTJqb3h6YmJjY2w5MyJ9.pQed7pZ9CnJL-mtqm1X8DQ"     
    map_style            = None if switch_off else 'dark'  
    template             = pio.templates["minty"] if switch_off else pio.templates["minty_dark"]    
    font_size            = 16       

    # ---------------------------------------------------------------- ---------------------------------------------------------------------
    # Compute Aircraft Properties 
    # ---------------------------------------------------------------- ---------------------------------------------------------------------     
    P_max                   = Max_P*1000000
    W_0                     = TOGW*907.185 # conversion of Ton to kg
    L_div_D                 = L_D 
    CO2e_per_passenger_mile = 0.0002         # in Ton  0.4 lb per passenger/ mile  Refhttps://8billiontrees.com/carbon-offsets-credits/carbon-ecological-footprint-calculators/carbon-footprint-driving-vs-flying/#:~:text=It%20is%20estimated%20that%20the,2%20per%20mile%20per%20passenger.                 
    Wh_per_kg_to_J          = 3600.0
    Ah_to_C                 = 3600.0  
    V_bat                   = system_V*1000
    eta_0                   = propulsive_efficiency/100   
    V_cell                  = cell_V
    e_cell                  = cell_e0 *Wh_per_kg_to_J
    q_cell                  = capacity * Ah_to_C  # conversion to coulombs
    i_max                   = (capacity*cell_C_max) # amps   
    Min_Temp                = cell_Temp[0]
    Max_Temp                = cell_Temp[1]
    I_bat                   = P_max/V_bat
    n_series                = V_bat/V_cell
    W_bat                   = (weight_fraction/100) * W_0
    E_bat                   = W_bat * e_cell  
    Q_bat                   = E_bat /V_bat
    n_parallel              = Q_bat/q_cell 
    n_parallel_min          = I_bat/i_max 
    
    if n_parallel_min  <  n_parallel: 
        Range    = (e_cell/9.81) * L_div_D * (weight_fraction/100)* eta_0
    else:  
        Range = 0   
    Range_mi = Range * 0.000621371 
    
    # Compute distances between departure and destimation points 
    months               = ['January', 'February', 'March', 'April', 'May', 'June', 'July','August', 'September', 'October', 'November', 'December']      
    month                =  months[month_no]  

    Routes_and_Temp_Mo                    = Routes_and_Temp[Routes_and_Temp['Month'] == month_no+1 ]     

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
    colors2               = px.colors.qualitative.T10
 
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
            line = dict(width = 2,color = colors2[7]),)) 
 
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
                               marker_color=colors2[7],))
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
                      yaxis=dict(range=[0,4E6], autorange=False),  
                      height        = 300, 
                      width         = 600, 
                      margin        = {'t':0,'l':0,'b':0,'r':0},  
                      bargap        = 0.1,
                      font=dict(  size=font_size ))  

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
                       marker_color=colors2[7])) 
    fig_6.update_layout(xaxis_title_text='Airport', 
                      yaxis_title_text='Passengers', 
                      height        = 300, 
                      width         = 600, 
                      margin        = {'t':0,'l':0,'b':0,'r':0},  
                      bargap        = 0.1, 
                      yaxis=dict(range=[0,1E6], autorange=False),  
                      font=dict(  size=font_size ),
                      legend=dict(
                          yanchor="top",
                          y=0.99,
                          xanchor="center",
                          x=0.85 ))  

    #================================================================================================================================================      
    # Determine Ratio of Electrified to Jet-A Routes
    #================================================================================================================================================    
    fig_7                       = go.Figure()
    Feasible_Passenger_Miles    = np.sum(np.array(Feasible_Routes['E_Passengers'])* np.array(Feasible_Routes['Distance (miles)']))
    Infeasible_Passenger_Miles  = np.sum(np.array(Infeasible_Routes[['Passengers']])* np.array(Infeasible_Routes[['Distance (miles)']])) 
    labels                      = ["All-Electric", "Fossil Fuels"] 
    fig_7.add_trace(go.Pie(labels=labels,
                         values=[Feasible_Passenger_Miles, Infeasible_Passenger_Miles],
                         marker_colors=[colors2[7],colors[10]])) 
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

   
        # concatenate feasible and infeasible routes 
        Infeasible_Routes           = pd.concat([Infeasible_Routes_1,Infeasible_Routes_2,Infeasible_Routes_3,Infeasible_Routes_4,Infeasible_Routes_5,Infeasible_Routes_6])    
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
            Total_Fuel_Cost_electric   = sum((E_bat*joule_to_kWh*cost_of_electricity) * np.array(Feasible_Routes['No of Flights Per Month']))
            ASM_electric               = sum(Feasible_Routes['Distance (miles)'] * electric_flight_passengers)
            CASM_electric[m_i]         = 100*Total_Fuel_Cost_electric/ASM_electric    
               
    #================================================================================================================================================      
    # Monthly Emissions
    #================================================================================================================================================                  
    month_names         = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']      
    fig_8               = go.Figure() 
    fig_8.add_trace(go.Scatter(x=month_names, y=w_electrification, name = 'Fleet with All-Electric Aircraft',
                             line=dict(color=colors2[7], width=4)))  
    fig_8.add_trace(go.Scatter(x=month_names, y=w_o_electriciation, name='All Conventional Aircraft Fleet',
                             line=dict(color=colors[10], width=4)))   
    fig_8.update_layout( 
                      height           = 400, 
                      width            = 600, 
                      margin           = {'t':50,'l':0,'b':0,'r':0},
                      yaxis_title_text ='CO2e (Ton)', # yaxis label 
                      yaxis_range      = [0.5E6,3E6],
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
                             line=dict(color=colors2[7], width=4)))  
    fig_9.update_layout( 
                      height           = 400, 
                      width            = 600, 
                      margin           = {'t':50,'l':0,'b':0,'r':0},
                      yaxis_title_text ='Cost Per Seat Mile (cents)', # yaxis label
                      yaxis_range      = [0,10],
                      font=dict(  size=font_size ),
                      legend=dict(
                          yanchor="top",
                          y=0.99,
                          xanchor="center",
                          x=0.4 )) 
    
    fig_4["layout"]["template"] = template   
    fig_5["layout"]["template"] = template         
    fig_6["layout"]["template"] = template    
    fig_7["layout"]["template"] = template 
    fig_8["layout"]["template"] = template  
    fig_9["layout"]["template"] = template  
    
    return fig_4,fig_5,fig_6,fig_7,fig_8,fig_9  
