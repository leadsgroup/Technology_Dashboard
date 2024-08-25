import plotly.express as px
import plotly.graph_objects as go
import plotly.io as pio
import pandas as pd
import numpy as np    
import json    
import os 
     
# ---------------------------------------------------------------------------------------------------------------------------------------------------
# SAF Plots 
# ---------------------------------------------------------------------------------------------------------------------------------------------------
def generate_saf_scatter_plot(Commercial_SAF,selected_process,selected_feedstock,selected_x_axis,selected_y_axis,switch_off): 
    template             = pio.templates["minty"] if switch_off else pio.templates["minty_dark"]  
    unique_processes     = list(Commercial_SAF['Process'][1:].unique())
    unique_feedstocks    = list(Commercial_SAF['Feedstock'][1:].unique())
    marker_size          = 15
    opacity_ratio        = 0.8 if switch_off else 1.0
    font_size            = 16 

    # Process Colors: greenyellow, aquamarine, paleturquoise, lightcoral, yellow, lavender ,thistle ,orangered   
    Process_Colors      = px.colors.qualitative.Pastel 
    Feedstock_Markers  = ['square','x','circle','cross','diamond','triangle-up','triangle-down','star','hourglass'] 
    fig = go.Figure()
    if selected_process == 'All' and  selected_feedstock == 'All':
        # for each Process 
        for i in range(len(unique_processes)): 
            # for each chemsitry 
            for j in range(len(unique_feedstocks)):
                data_1 = Commercial_SAF.loc[ Commercial_SAF['Process'] == unique_processes[i]] 
                data_2 = data_1.loc[Commercial_SAF['Feedstock'] == unique_feedstocks[j]]   
                fig.add_trace(go.Scatter( x        = np.array(data_2[selected_x_axis]), 
                                     y             = np.array(data_2[selected_y_axis]),  
                                     mode          = 'markers', 
                                     name          ="",                                    
                                     marker        = dict(size=marker_size,color=Process_Colors[i],opacity=opacity_ratio,symbol = Feedstock_Markers[j]),
                                     hovertemplate = 'Process: ' + unique_processes[i] + '<br>' + 'Feedstock: ' + unique_feedstocks[j] + '<br>' + selected_x_axis + ': %{x} <br>' + selected_y_axis + ': %{y}',
                                     )) 
    elif selected_process != 'All' and  selected_feedstock == 'All':
        # for each Process  
        for j in range(len(unique_feedstocks)):
            data_1   = Commercial_SAF.loc[ Commercial_SAF['Process'] == selected_process] 
            data_2   = data_1.loc[Commercial_SAF['Feedstock'] == unique_feedstocks[j]]  
            i_index  = unique_processes.index(selected_process) 
            fig.add_trace(go.Scatter( x             = np.array(data_2[selected_x_axis]), 
                                 y             = np.array(data_2[selected_y_axis]),  
                                 mode          = 'markers',
                                 name          = "",            
                                 marker        = dict(size=marker_size,color=Process_Colors[i_index ],opacity=opacity_ratio,symbol = Feedstock_Markers[j]),
                                 hovertemplate = 'Process: ' + selected_process + '<br>' + 'Feedstock: ' + unique_feedstocks[j] + '<br>' + selected_x_axis + ': %{x} <br>' + selected_y_axis + ': %{y}',
                                 ))
    elif selected_process == 'All' and selected_feedstock != 'All':
        # for each Process 
        for i in range(len(unique_processes)):  
            data_1   = Commercial_SAF.loc[ Commercial_SAF['Process'] == unique_processes[i]] 
            data_2   = data_1.loc[Commercial_SAF['Feedstock'] == selected_feedstock] 
            j_index  = unique_feedstocks.index(selected_feedstock)
            models   = data_2["Model"]
            config   = data_2["Configuration"]
            fig.add_trace(go.Scatter( x             = np.array(data_2[selected_x_axis]), 
                                 y             = np.array(data_2[selected_y_axis]),  
                                 mode          = 'markers',
                                 name          = "",      
                                 marker        = dict(size=marker_size,color=Process_Colors[i],opacity=opacity_ratio,symbol = Feedstock_Markers[j_index]),
                                 hovertemplate = 'Process: ' + unique_processes[i] + '<br>' + 'Feedstock: ' + selected_feedstock + '<br>' + 'Configuration: ' + config + '<br>' + 'Model: ' + models + '<br>' + selected_x_axis + ': %{x} <br>' + selected_y_axis + ': %{y}',
                                 ))
    else:
        data_1  = Commercial_SAF.loc[ Commercial_SAF['Process'] == selected_process ] 
        data_2  = data_1.loc[Commercial_SAF['Feedstock'] == selected_feedstock] 
        i_index = unique_processes.index(selected_process)
        j_index = unique_feedstocks.index(selected_feedstock) 
        fig.add_trace(go.Scatter( x        = np.array(data_2[selected_x_axis]), 
                             y             = np.array(data_2[selected_y_axis]),  
                             mode          = 'markers', 
                             name          = "",       
                             marker        = dict(size=marker_size,color=Process_Colors[i_index],opacity=opacity_ratio,symbol = Feedstock_Markers[j_index]),
                             hovertemplate = 'Process: ' + selected_process  + '<br>' + 'Feedstock: ' + selected_feedstock + '<br>' + selected_x_axis + ': %{x} <br>' + selected_y_axis + ': %{y}',
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

def generate_saf_dev_map(Commercial_SAF,selected_feedstock,selected_process,switch_off): 
    template            = pio.templates["minty"] if switch_off else pio.templates["minty_dark"]    
    map_style           = None if switch_off else 'dark' 
    unique_feedstocks   = list(Commercial_SAF['Feedstock'][1:].unique())
    unique_process      = list(Commercial_SAF['Process'][1:].unique())   
    sector_colors       = px.colors.qualitative.Pastel 
    mapbox_access_token = "pk.eyJ1IjoibWFjbGFya2UiLCJhIjoiY2xyanpiNHN6MDhsYTJqb3h6YmJjY2w5MyJ9.pQed7pZ9CnJL-mtqm1X8DQ" 
    
    fig = go.Figure()
    if selected_feedstock == 'All' and  selected_process == 'All': 
        for i in range(len(unique_feedstocks)):
            for j in range(len(unique_process)):
                data_1 = Commercial_SAF.loc[Commercial_SAF['Feedstock'] == unique_feedstocks[i]] 
                data_2 = data_1.loc[Commercial_SAF['Process'] == unique_process[j]]   
                fig2   = px.scatter_mapbox(data_2, lat="Latitude", lon="Longitude",
                                          hover_name="Fuel Name",
                                          hover_data=['Feedstock','Process','Source','Maximum Blend Ratio','LCA Value'],
                                         color_discrete_sequence=[sector_colors[i]], zoom=1 ,)
                fig.add_trace(fig2.data[0])
    
    elif selected_feedstock == 'All' and  selected_process != 'All': 
        for i in range(len(unique_feedstocks)): 
            data_1 = Commercial_SAF.loc[Commercial_SAF['Feedstock'] == unique_feedstocks[i]] 
            data_2 = data_1.loc[Commercial_SAF['Process'] == selected_process]   
            fig2   = px.scatter_mapbox(data_2, lat="Latitude", lon="Longitude",
                                      hover_name="Fuel Name",
                                      hover_data=['Feedstock','Process','Source','Maximum Blend Ratio','LCA Value'],
                                     color_discrete_sequence=[sector_colors[i]], zoom=1 ,)
            fig.add_trace(fig2.data[0])
            
    
    elif selected_feedstock != 'All' and  selected_process == 'All': 
        color_idx = unique_feedstocks.index(selected_feedstock)
        for j in range(len(unique_process)): 
            data_1 = Commercial_SAF.loc[Commercial_SAF['Feedstock'] == selected_feedstock] 
            data_2 = data_1.loc[Commercial_SAF['Process'] == unique_process[j]]  
            fig2   = px.scatter_mapbox(data_2, lat="Latitude", lon="Longitude",
                                      hover_name="Fuel Name",
                                      hover_data=['Feedstock','Process','Source','Maximum Blend Ratio','LCA Value'],
                                     color_discrete_sequence=[sector_colors[color_idx]], zoom=1 ,)
            fig.add_trace(fig2.data[0])      
    
    else:  
        color_idx = unique_feedstocks.index(selected_feedstock)
        data_1    = Commercial_SAF.loc[Commercial_SAF['Feedstock'] == selected_feedstock] 
        data_2    = data_1.loc[Commercial_SAF['Process'] == selected_process]
        fig2      = px.scatter_mapbox(data_2, lat="Latitude", lon="Longitude",
                                  hover_name="Fuel Name",
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

 
def generate_saf_flight_operations_plots(Flight_Ops,Commercial_SAF,feedstocks,selected_fuels,selected_feedstock, 
                                    percent_fuel_use, feedstock_producing_states,selected_airpots,
                                    percent_adoption,SAF_dollars_per_gal,switch_off):   
     
    template             = pio.templates["minty"] if switch_off else pio.templates["minty_dark"]    
    map_style            = None if switch_off else 'dark'     
    font_size            = 16  
    mapbox_access_token  = "pk.eyJ1IjoibWFjbGFya2UiLCJhIjoiY2xyanpiNHN6MDhsYTJqb3h6YmJjY2w5MyJ9.pQed7pZ9CnJL-mtqm1X8DQ"
    separator = os.path.sep
    file_path = '..'+ separator +'Data'+ separator +'US_County'+ separator +'counties_fips.json'
    f = open(file_path) 
    counties = json.load(f)

    #================================================================================================================================================  
    # Unit Conversions 
    #================================================================================================================================================     
    JetA_GHG               = 4.36466 # CO2e/kg fuel 
    gallons_to_Liters      = 3.78541
    liters_to_cubic_meters = 0.001
    Jet_A_density          = 800.0  
    density_JetA           = 820.0  # kg /m3  
    kg_to_Megaton          = 1E-9 
    g_to_kg                = 0.001
    
    # Compute the percentages of different types of fuels used 
    fuel_percentages_list = [0]
    fuel_percentages_list += percent_fuel_use
    fuel_percentages_list += [100]
    fuels_percentages     = np.diff(np.array(fuel_percentages_list))/100  
    
    # Determine the percentage of neat (pure) saf and Jet-A1 using blending ratios   
    if Commercial_SAF['Fuel Name'][0] not in selected_fuels:  
        selected_fuels    = [Commercial_SAF['Fuel Name'][0]] + selected_fuels
        fuels_percentages = np.hstack((np.array([0]),fuels_percentages)) 
    mask                = Commercial_SAF['Fuel Name'].isin(selected_fuels)
    fuels_used          = Commercial_SAF[mask] 
    
    num_fuels = len(selected_fuels)
    cumulative_fuel_use   = np.zeros(num_fuels) 
    SAF_LCA_val           = np.zeros(num_fuels) 
    Jet_A_LCA_val         = np.zeros(num_fuels)  

    # Loop through fuels and get percentage of fuel used by each type    
    for i in range(1,num_fuels):
        blend_ratio             = np.array(Commercial_SAF.loc[Commercial_SAF['Fuel Name'] == selected_fuels[i]]['Maximum Blend Ratio']) 
        cumulative_fuel_use[i]  = fuels_percentages[i]* blend_ratio/100
        SAF_LCA_val[i]          = Commercial_SAF[Commercial_SAF['Fuel Name'] == selected_fuels[i]]['LCA Value']
    cumulative_fuel_use[0]      = 1 - np.sum(cumulative_fuel_use[1:])
    SAF_LCA_val[0]   = 89
    Jet_A_LCA_val[0] = 89
        
    # Filter flight data based on option selected: i.e. top 10, top 20, top 50, all airpots 
    Airport_Routes     = Flight_Ops[['Passengers','Origin Airport','Destination City Name']]
    Cumulative_Flights = Airport_Routes.groupby('Origin Airport', as_index=False).sum()[Airport_Routes.columns]
    if  selected_airpots == " Top 5 Airports":
        Busiest_Airports   = Cumulative_Flights.sort_values(by=['Passengers'], ascending = False).head(5) 
    if  selected_airpots == " Top 10 Airports":
        Busiest_Airports   = Cumulative_Flights.sort_values(by=['Passengers'], ascending = False).head(10) 
    elif  selected_airpots ==" Top 20 Airports":
        Busiest_Airports   = Cumulative_Flights.sort_values(by=['Passengers'], ascending = False).head(20) 
    elif  selected_airpots == " Top 50 Airports":
        Busiest_Airports   = Cumulative_Flights.sort_values(by=['Passengers'], ascending = False).head(50) 
    elif  selected_airpots == " All Airports":
        Busiest_Airports   = Cumulative_Flights.sort_values(by=['Passengers'], ascending = False) 
    Airport_List = list(Busiest_Airports['Origin Airport'])
    
    # Filter airports that will support SAF and those that wont support SAF 
    mask_1                = Flight_Ops['Origin Airport'].isin(Airport_List)
    SAF_Airports          = Flight_Ops[mask_1]
    Non_SAF_Airports      = Flight_Ops[~mask_1]  
    
    # Out of SAF supporting airports, use the percent adoption to determine how many flights at that airport will use SAF 
    Flight_at_SAF_Airports_Using_SAF      = SAF_Airports.sample(frac=(percent_adoption/100))
    Flight_at_SAF_Airports_Using_Jet_A    = SAF_Airports[~SAF_Airports.index.isin(Flight_at_SAF_Airports_Using_SAF.index)]
    Non_SAF_Flights                       = pd.concat([Non_SAF_Airports, Flight_at_SAF_Airports_Using_Jet_A] )   # add list of flights from non supporting airports to non-SAF flights  
     
    # Get total volume of each SAF required at the airports 
    total_fuel_volume_required = np.sum(np.array(Flight_at_SAF_Airports_Using_SAF['Total Fuel Per Route (Gal)']))
    fuel_volumes               = cumulative_fuel_use*total_fuel_volume_required  
    
    # Sort SAF's by feedstock and sum all fuel volumes based on fuel   
    fuels_used['Total Fuel Volume']   = fuel_volumes 
    relative_crop_area                = fuels_used['Total Fuel Volume']/fuels_used['SAF Gallons per Acre']
    fuels_used['Requires Acres']      = relative_crop_area
    select_fuels                      = fuels_used[['Source','Total Fuel Volume','Requires Acres']].groupby('Source', as_index=False).sum()[fuels_used[['Source','Total Fuel Volume','Requires Acres']].columns]
    required_crop_area                = np.array(select_fuels.loc[select_fuels['Source'] == selected_feedstock]['Requires Acres'])
    
    # Determine how many states will source the feedstock under consideration  
    crop_data  = feedstocks[selected_feedstock]   
    crop_data['FIPS'] = crop_data['FIPS'].apply('{:0>5}'.format)
    
    # Filter out states have not been selected and get number of states  
    mask                  = crop_data['State'].isin(feedstock_producing_states)
    feedstock_states      = crop_data[mask]    
    non_feedstock_states  = crop_data[~mask]   
    non_feedstock_states["Feedstock Usage"] = list(np.ones(len(non_feedstock_states)))

    # Randomize tracts in terms of crop area/usage then Recursively add rows until requied volume is met 
    Used_Feedstock        = feedstock_states.sample(frac = 1) 
    Used_Feedstock["Feedstock Usage"] =  np.ones(len(feedstock_states))
    
    idx        = 0
    total_vol  = 0    
    if len(required_crop_area) == 0:
        RCA  = 0
    else:
        RCA  = required_crop_area[0]  
    available_tracts =len(Used_Feedstock)
    while total_vol<RCA: 
        total_vol += Used_Feedstock.loc[Used_Feedstock.index[idx]]['Acres Harvested']
        Used_Feedstock["Feedstock Usage"][Used_Feedstock.index[idx]] = 0.1 
        idx += 1      
        if available_tracts == idx:
            total_vol = 1E9  
     
    # Determine Cost per Seat Mile and Emissions  
    CASM_wo_SAF_Aircraft  = np.zeros(12) 
    CASM_w_SAF_Aircraft    = np.zeros(12) 
    Emissions_w_SAF_Aircraft       = np.zeros(12) 
    Emissions_wo_SAF_Aircraft     = np.zeros(12) 
    gallons_to_Liters  = 3.78541
    for m_i in range(12): 
        Routes_and_Temp_Mo                  = Flight_Ops[Flight_Ops['Month'] == m_i+1 ]   
            
        # EMISSIONS 
        # Emissions of SAF-Scenario from non-SAF Flights 
        Non_SAF_Flights_Mo                  = Non_SAF_Flights.loc[Non_SAF_Flights['Month'] == m_i+1 ]   
        Infeasible_Routes_fuel_volume          = np.sum(np.array(Non_SAF_Flights_Mo['Total Fuel Per Route (Gal)'])) * gallons_to_Liters * liters_to_cubic_meters
        Infeasible_Routes_Emissions            = kg_to_Megaton * JetA_GHG * Infeasible_Routes_fuel_volume * density_JetA
        
        # Emissions of SAF-Scenario from SAF Flights 
        Flight_at_SAF_Airports_Using_SAF_Mo = Flight_at_SAF_Airports_Using_SAF.loc[Flight_at_SAF_Airports_Using_SAF['Month'] == m_i+1 ]    
        total_SAF_fuel_volume_required_mo   = np.sum(np.array(Flight_at_SAF_Airports_Using_SAF_Mo['Total Fuel Per Route (Gal)']))  
        SAF_volumes_mo                      = cumulative_fuel_use*total_SAF_fuel_volume_required_mo         
        SAF_Emissions                   = g_to_kg * kg_to_Megaton * np.sum(fuels_used['LCEF (gCO2e/MJ)']*fuels_used['Volumetric Energy Density (MJ/L)']*SAF_volumes_mo*gallons_to_Liters)
        Emissions_w_SAF_Aircraft[m_i]   = SAF_Emissions +  Infeasible_Routes_Emissions

        # Compute emissions without SAF integration        
        Conventional_Air_Travel_fuel_volume   = np.sum(np.array(Routes_and_Temp_Mo['Total Fuel Per Route (Gal)'])) * gallons_to_Liters * liters_to_cubic_meters
        Emissions_wo_SAF_Aircraft[m_i]        = kg_to_Megaton * JetA_GHG * Conventional_Air_Travel_fuel_volume * density_JetA

        # COST PER SEAT MILE 
        # CASM for normal operations without SAF aircraft  
        if len(Non_SAF_Flights_Mo ) == 0:
            pass
        else: 
            ASM_jet_A                = np.sum(Routes_and_Temp_Mo['Distance (miles)'] * Routes_and_Temp_Mo['Passengers'])
            Total_Fuel_Cost_jet_A    = np.sum(Routes_and_Temp_Mo['Fuel Cost']) 
            CASM_wo_SAF_Aircraft[m_i]  = 100*Total_Fuel_Cost_jet_A/ASM_jet_A    
       
        if len(Flight_at_SAF_Airports_Using_SAF_Mo)  == 0:
            pass
        else:    
            ASM_SAF                    = np.sum(Flight_at_SAF_Airports_Using_SAF_Mo['Distance (miles)'] * Flight_at_SAF_Airports_Using_SAF_Mo['Passengers']) 
            Total_Fuel_Cost_SAF        = np.sum(Flight_at_SAF_Airports_Using_SAF_Mo['Total Fuel Per Route (Gal)'] ) * SAF_dollars_per_gal 
            CASM_w_SAF_Aircraft[m_i]   = 100*Total_Fuel_Cost_SAF/ASM_SAF   
          
    #================================================================================================================================================  
    # Plot Flight_Ops 
    #================================================================================================================================================     
    # Flight_Ops   
    colors                = px.colors.qualitative.Pastel 
    fig_1                = go.Figure()
    airport_marker_size  = 5
    airport_marker_color = "white"
 
    # Flight Paths
    lons       = np.empty(3 * len(Non_SAF_Flights))
    lons[::3]  = Non_SAF_Flights['Origin Longitude (Deg.)']
    lons[1::3] = Non_SAF_Flights['Destination Longitude (Deg.)']
    lons[2::3] = None
    lats       = np.empty(3 * len(Non_SAF_Flights))
    lats[::3]  = Non_SAF_Flights['Origin Latitude (Deg.)']
    lats[1::3] = Non_SAF_Flights['Destination Latitude (Deg.)']
    lats[2::3] = None    
  
    fig_1.add_trace(
        go.Scattergeo( 
            lon = lons,
            lat = lats,
            mode = 'lines',
            opacity= 1,
            line = dict(width = 1,color = colors[10]), ))
    
    lons       = np.empty(3 * len(Flight_at_SAF_Airports_Using_SAF))
    lons[::3]  = Flight_at_SAF_Airports_Using_SAF['Origin Longitude (Deg.)']
    lons[1::3] = Flight_at_SAF_Airports_Using_SAF['Destination Longitude (Deg.)']
    lons[2::3] = None
    lats       = np.empty(3 * len(Flight_at_SAF_Airports_Using_SAF))
    lats[::3]  = Flight_at_SAF_Airports_Using_SAF['Origin Latitude (Deg.)']
    lats[1::3] = Flight_at_SAF_Airports_Using_SAF['Destination Latitude (Deg.)']
    lats[2::3] = None    
  
    fig_1.add_trace(
        go.Scattergeo( 
            lon = lons,
            lat = lats,
            mode = 'lines',
            opacity= 1,
            line = dict(width = 1,color = colors[1]), ))
  
    # Airports  
    fig_1.add_trace(go.Scattergeo( 
        lon = Flight_Ops['Destination Longitude (Deg.)'],
        lat = Flight_Ops['Destination Latitude (Deg.)'], 
        text = Flight_Ops['Destination City Name'],
        mode = 'markers',
        marker = dict(
            size = airport_marker_size,
            color = airport_marker_color, ))) 

    fig_1.add_trace(go.Scattergeo( 
        lon = Flight_Ops['Origin Longitude (Deg.)'],
        lat = Flight_Ops['Origin Latitude (Deg.)'], 
        text = Flight_Ops['Origin City Name'],
        mode = 'markers',
        marker = dict(
            size = airport_marker_size,
            color = airport_marker_color,))) 
     
    # Flight Paths 
    fig_1.update_layout(mapbox_style  = "open-street-map",      
                      showlegend    = False, 
                      height        = 400, 
                      geo_scope     ='usa',
                      margin        = {'t':0,'l':0,'b':0,'r':0},  
                      mapbox        = dict( accesstoken=mapbox_access_token,style=map_style,
                                            center=go.layout.mapbox.Center( lat=30, lon= 230 )))   

    #================================================================================================================================================      
    # Passenger vs Distance Traveled 
    #================================================================================================================================================     
    fig_3               = go.Figure()  
    fig_3.add_trace(go.Histogram(histfunc="sum",
                               x= Flight_at_SAF_Airports_Using_SAF['Distance (miles)'],
                               y = Flight_at_SAF_Airports_Using_SAF['Passengers'],
                               name='SAF', 
                               xbins=dict(start=0, end=4000, size=500),
                               marker_color=colors[1],))
    fig_3.add_trace(go.Histogram(histfunc="sum",
                               x= Non_SAF_Flights['Distance (miles)'],
                               y = Non_SAF_Flights['Passengers'],
                               name='Fossil Fuels',
                               xbins=dict(start=0, end=4000, size=500),
                               marker_color=colors[10],)) 
    
    # The two histograms are drawn on top of another
    fig_3.update_layout(barmode='stack', 
                      xaxis_title_text='Distance (miles)', 
                      yaxis_title_text='Passengers',
                      height        = 300, 
                      width         = 600, 
                      margin        = {'t':0,'l':0,'b':0,'r':0},  
                      bargap        = 0.1,
                      font=dict(  size=font_size ),
                      legend=dict(
                          yanchor="top",
                          y=0.99,
                          xanchor="center",
                          x=0.85 ))   
    
    #================================================================================================================================================      
    # Busiest Airports 
    #================================================================================================================================================    
    fig_4 = go.Figure()
    Airport_Routes     = Flight_at_SAF_Airports_Using_SAF[['Passengers','Origin Airport','Destination City Name']]
    Cumulative_Flights = Airport_Routes.groupby(['Origin Airport']).sum()
    Busiest_Airports   = Cumulative_Flights.sort_values(by=['Passengers'], ascending = False).head(10) 
    Alphabetical_List  = Busiest_Airports.sort_values(by=['Origin Airport'])  
    fig_4.add_trace(go.Bar( x=list(Alphabetical_List['Passengers'].index),
                       y=np.array(Alphabetical_List['Passengers']),
                       marker_color=colors[1])) 
    fig_4.update_layout(xaxis_title_text='Airport', 
                      yaxis_title_text='Passengers', 
                      height        = 300, 
                      width         = 600, 
                      margin        = {'t':0,'l':0,'b':0,'r':0},  
                      bargap        = 0.1,
                      font=dict(  size=font_size ))  
    
    #================================================================================================================================================      
    # Determine Ratio of SAF to Jet-A Routes
    #================================================================================================================================================    
    fig_5                       = go.Figure() 
    sector_colors               = [colors[1],colors[10]]
    Feasible_Passenger_Miles    = np.sum(np.array(Flight_at_SAF_Airports_Using_SAF['Passengers'])* np.array(Flight_at_SAF_Airports_Using_SAF['Distance (miles)']))
    Infeasible_Passenger_Miles  = np.sum(np.array(Non_SAF_Flights[['Passengers']])* np.array(Non_SAF_Flights[['Distance (miles)']]))
    labels                      = ["SAF", "Fossil Fuels"] 
    fig_5.add_trace(go.Pie(labels=labels,
                         values=[Feasible_Passenger_Miles, Infeasible_Passenger_Miles],
                         marker_colors=sector_colors)) 
    fig_5.update_traces(hole=.4, hoverinfo="label+percent+name") 
    fig_5.update_layout( height     = 400,  
                      margin        = {'t':50,'l':0,'b':0,'r':0},  
                      font=dict(  size=font_size ),
                      legend=dict(
                          yanchor="top",
                          y=0.99,
                          xanchor="center",
                          x=0.85 ))  
    
    
    #================================================================================================================================================  
    # Plot Land Use  
    #================================================================================================================================================     
 
    Land_Use  = pd.concat([Used_Feedstock, non_feedstock_states] )    
    fig_2 = px.choropleth(Land_Use, geojson=counties, locations='FIPS',color = 'Feedstock Usage',
                           color_continuous_scale="turbid", 
                           hover_data=["County","State","Acres Harvested"],
                           scope='usa',                          
                           range_color=(0,1)
                           ) 
    fig_2.update_layout( height     = 400,  
                         margin        = {'t':0,'l':0,'b':0,'r':0} 
                         )
    fig_2.update(layout_coloraxis_showscale=False)
    
    #================================================================================================================================================      
    # Cost Per Seat Mile
    #================================================================================================================================================   
    fig_6 = go.Figure()       
    month_names         = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']    
    fig_6.add_trace(go.Scatter(x=month_names, y=CASM_wo_SAF_Aircraft, name='Fossil Fuels',
                             line=dict(color= colors[10], width=4))) 
    fig_6.add_trace(go.Scatter(x=month_names, y=CASM_w_SAF_Aircraft, name = 'SAF',
                             line=dict(color= colors[1], width=4)))   
    fig_6.update_layout( 
                      height           = 400, 
                      width            = 600, 
                      margin           = {'t':50,'l':0,'b':0,'r':0},
                      yaxis_title_text ='Cost Per Seat Mile (cents)', 
                      font=dict(  size=font_size ),
                      yaxis_range      = [0,20],
                      legend=dict(
                          yanchor="top",
                          y=0.99,
                          xanchor="center",
                          x=0.8 )) 
    #================================================================================================================================================      
    # Emissions Comparison 
    #================================================================================================================================================   
    month_names         = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']      
    fig_8               = go.Figure() 
    fig_8.add_trace(go.Scatter(x=month_names, y=Emissions_w_SAF_Aircraft, name = 'Aircraft Fleet with SAF Aircraft',
                             line=dict(color=colors[1], width=4)))  
    fig_8.add_trace(go.Scatter(x=month_names, y=Emissions_wo_SAF_Aircraft, name='Aircraft Fleet without SAF Aircraft',
                             line=dict(color=colors[10], width=4)))   
    fig_8.update_layout( 
                      height           = 400, 
                      width            = 600, 
                      margin           = {'t':50,'l':0,'b':0,'r':0},
                      yaxis_title_text ='CO2 Emissions (MtCO2)', # yaxis label
                      font=dict(  size=font_size ),
                      yaxis_range      = [0,20],
                      legend=dict(
                          yanchor="top",
                          y=0.99,
                          xanchor="center",
                          x=0.8 )) 
    
    #================================================================================================================================================      
    # Life Cycle Analysis
    #================================================================================================================================================   
    Jet_A_name = ["U.S. Aviation without SAF"]*num_fuels
    Jet_A_data = {'Cumulative Fuel': Jet_A_name,
            'Fuels' : selected_fuels,
            'Cumulative LCA Value'        : Jet_A_LCA_val,
            } 
    SAF_name = ["U.S. Aviation with SAF"]*num_fuels
    SAF_data = {'Cumulative Fuel': SAF_name,
            'Fuels' : selected_fuels,
            'Cumulative LCA Value'        : SAF_LCA_val*cumulative_fuel_use,
            } 
    Jet_A_Emissions = pd.DataFrame(Jet_A_data)
    SAF_Emissions   = pd.DataFrame(SAF_data)
    frames = [Jet_A_Emissions,SAF_Emissions] 
    Emissions = pd.concat(frames)
    fig_7               =   px.bar(Emissions,
                                   x="Cumulative Fuel",
                                   y="Cumulative LCA Value",
                                   color= "Fuels",
                                   color_discrete_sequence=px.colors.qualitative.Pastel)  
    fig_7.update_layout(xaxis_title=None,
                      showlegend=False,
                      font=dict(  size=font_size ),
                      ) 
                          
   ##================================================================================================================================================   

    fig_1["layout"]["template"] = template  
    fig_2["layout"]["template"] = template 
    fig_3["layout"]["template"] = template  
    fig_4["layout"]["template"] = template  
    fig_5["layout"]["template"] = template 
    fig_6["layout"]["template"] = template 
    fig_7["layout"]["template"] = template 
    fig_8["layout"]["template"] = template 
        
    return fig_1, fig_2,fig_3, fig_4, fig_5 , fig_6, fig_7, fig_8

# ---------------------------------------------------------------------------------------------------------------------------------------------------
# SAF Bar
# ---------------------------------------------------------------------------------------------------------------------------------------------------
def generate_saf_slider_bar(Commercial_SAF,selected_fuels,SAF_ratios,switch_off):
    template      = pio.templates["minty"] if switch_off else pio.templates["minty_dark"]   
    fuels         = selected_fuels
    v             = [0] 
    v             = v + SAF_ratios
    v             = v + [100]
    vals          = np.array(v)
    fuel_quantity = np.diff(vals) 
    sources  = ['Fuel']*(len(vals)-1)
    df = pd.DataFrame({'Quantity': list(fuel_quantity),
                       'Source'  : sources,
                       'Fuel'    : fuels}) 
    fig = px.histogram(df, y="Source",
                   x="Quantity",
                   color="Fuel",
                   color_discrete_sequence=px.colors.qualitative.Pastel,
                   barnorm='percent')
    fig.update_layout(margin=dict(l=25, r=0, t=0, b=0),
                      xaxis_title=None,
                      yaxis_title=None, 
                      height     = 100, 
                      width      = 1350, 
                      showlegend=False,
                      xaxis     =  {'title': 'x-label','visible': False,'showticklabels': True},
                      yaxis     =  {'title': 'y-label','visible': False,'showticklabels': False},
                              )   
    fig["layout"]["template"] = template 
    return fig 
  