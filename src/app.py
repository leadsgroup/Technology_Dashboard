"""Sustainable Aviation Technology Dashboard
"""
import dash 
from dash import Dash, html, dcc, Input, Output, Patch, clientside_callback, callback 
import plotly.io as pio
import dash_bootstrap_components as dbc 
from dash_bootstrap_templates                  import load_figure_template 
import pandas as pd  
import os 
from Energy_X.figures                          import *
from Energy_X.knobs_and_buttons                import * 
from Energy_X.control_panels                   import *  
from Electrification.figures                   import * 
from Electrification.knobs_and_buttons         import * 
from Electrification.control_panels            import * 
from SAF.figures                               import * 
from SAF.knobs_and_buttons                     import * 
from SAF.control_panels                        import *  
from Hydrogen.figures                          import * 
from Hydrogen.knobs_and_buttons                import * 
from Hydrogen.control_panels                   import *    

# ---------------------------------------------------------------------------------------------------------------------------------------------------
# Data
# --------------------------------------------------------------------------------------------------------------------------------------------------- 
separator                  = os.path.sep 
technology_filename        = '..' + separator + 'Data'  + separator + 'Technology' + separator +  'Technology_Data.xlsx'
crops_filename             = '..' + separator + 'Data'  + separator +  'Crops'     + separator + 'All_Crops_2017.xlsx' 
routes_filename            = '..' + separator + 'Data'  + separator + 'Air_Travel' + separator + 'Top_10_Major_US_Airlines_Flight_Ops_and_Climate.csv'
temperature_filename       = '..' + separator + 'Data' + separator  + 'US_Climate' + separator + 'Monthly_US_County_Temperature_2019.csv'
SAT_data                   = pd.read_excel(technology_filename,sheet_name=['Commercial_Batteries','Battery_Development','Electric_Motor_Development','Commercial_SAF', 'Hydrogen']) 

Commercial_Batteries       = SAT_data['Commercial_Batteries'] 
Electric_Motor_Development = SAT_data['Electric_Motor_Development']
a                          = Commercial_Batteries['Brand']  
b                          = Commercial_Batteries['Abbreviation']
c                          = Commercial_Batteries['Model']
d                          = a + ': ' + b + '-' + c 
Commercial_Batteries["Battery Name"] = d     
Battery_Development        = SAT_data['Battery_Development']

Commercial_SAF             = SAT_data['Commercial_SAF']  
a                          = Commercial_SAF['Brand']  
b                          = Commercial_SAF['Fuel Type']
c                          = Commercial_SAF['Process']
d                          = Commercial_SAF['Source']
e                          = Commercial_SAF['Feedstock']
Commercial_SAF["Fuel Name"]= ' ' + a + ' ' + c + '-' + b + ' from ' + e  + ' (' + d  + ')'
 
Hydrogen                   = SAT_data['Hydrogen']   
a                          = Hydrogen['Feedstock']
b                          = Hydrogen['Production Technology'] 
c                          = Hydrogen['Production Process'] 
Hydrogen["H2 Fuel Name"]   =  a  + ' via ' + b +  ' using ' + c 
 
Flight_Ops                 = pd.read_csv(routes_filename)    
US_Temperature_F           = pd.read_csv(temperature_filename)   
feedstocks                 = pd.read_excel(crops_filename,sheet_name=['Corn','Soybean','Canola','Sunflower','Sorghum','Wheat'])  
 

# ---------------------------------------------------------------------------------------------------------------------------------------------------
# Control Panels 
# ---------------------------------------------------------------------------------------------------------------------------------------------------

# Battery   
battery_metrics_panel               = generate_battery_metrics_panel(Commercial_Batteries)
motor_metrics_panel                 = generate_motor_metrics_panel(Electric_Motor_Development)
battery_comparison_panel            = generate_battery_comparison_panel(Commercial_Batteries)   
battery_development_panel           = generate_battery_development_panel(Battery_Development)    
battery_flight_ops_aircraft_panel   = generate_flight_ops_aircraft_panel(Commercial_Batteries,US_Temperature_F,Flight_Ops)   
 
# Sustainable Aviation Fuel  
saf_metrics_panel              = generate_saf_metrics_panel(Commercial_SAF)
saf_development_panel          = generate_saf_development_panel(Commercial_SAF)
saf_flight_ops_fuel_panel      = generate_saf_flight_ops_fuel_panel(Commercial_SAF)
saf_flight_ops_states_panel    = generate_saf_flight_ops_states_panel() 
feedstock                      = select_feedstock_source(Commercial_SAF)     
flight_ops_saf_adoption_frac   = select_saf_fleet_adoption() 
saf_airports                   = select_saf_airports()    
saf_cost                       = select_saf_cost()
 
# Hydrogen 
h2_flight_ops_fuel_panel       = generate_h2_flight_ops_fuel_panel(Hydrogen)
h2_fleet_adoption              = select_h2_fleet_adoption()
h2_airports                    = select_h2_airports()
h2_cost                        = select_h2_cost()
h2_engine_SFC                  = select_h2_engine_SFC()
h2_altitude                    = select_h2_altitude() 
h2_vol_fraction                = select_h2_vol_fraction()   

# Energy X
Energy_X_aircraft_flight_ops_panel = generate_Energy_X_aircraft_flight_ops_panel(US_Temperature_F)
Energy_X_battery_panel             = generate_Energy_X_battery_panel()


# ---------------------------------------------------------------------------------------------------------------------------------------------------
# App Layout 
# ---------------------------------------------------------------------------------------------------------------------------------------------------


# Template and theme
load_figure_template(["minty_dark", "minty"])  
app = Dash(__name__,
           external_stylesheets=[dbc.themes.MINTY, dbc.icons.FONT_AWESOME], 
           meta_tags=[{'name': 'viewport', 'content': 'width=device-width, initial-scale=1.0, maximum-scale=1.2, minimum-scale=0.5,'}],          
           suppress_callback_exceptions=True)
server = app.server

color_mode_switch =  html.Span(
    [
        dbc.Label(className="fa fa-moon", html_for="color-mode-switch"),
        dbc.Switch( id="color-mode-switch", value=False, className="d-inline-block ms-1", persistence=True),
        dbc.Label(className="fa fa-sun", html_for="color-mode-switch"),
    ]
)
 
# Template  colors 
primary_color     = '#78c2ad' # grey green
secondary_color   = '#f3969a' # red  # SAF 
backround         = '#212529'
success_color     = '#56cc9d' # green Bat 
info_color        = '#6cc3d5' # blue H2 
light_color       = '#f8f9fa'
warning_color     = '#fdce67' # yellow 
dark_color        = '#828588'
font_size         =  '28px'
border            = '1px solid #828588' 
tab_style = {
    'borderTop': border, 
    'borderBottom': border, 
    'borderLeft': border,
    'borderRight': border,
    'padding': '6px', 
    'color': dark_color,
    'fontSize' : font_size,
    'backgroundColor': backround,
}

energy_ex_tab_style = {
    'borderTop': border,
    'borderBottom': border,
    'backgroundColor': secondary_color,
    'color': 'white', 
    'padding': '6px', 
    'fontSize' : font_size,
}
 

electrification_tab_style = {
    'borderTop': border,
    'borderBottom': border,
    'backgroundColor': primary_color,
    'color': 'white', 
    'fontSize' : font_size,
    'padding': '6px', 
}


saf_tab_style = {
    'borderTop': border,
    'borderBottom': border,
    'backgroundColor': warning_color,
    'color': 'white', 
    'fontSize' : font_size,
    'padding': '6px', 
}


hydrogen_tab_style = {
    'borderTop': border,
    'borderBottom': border,
    'backgroundColor': info_color,
    'color': 'white', 
    'fontSize' : font_size,
    'padding': '6px', 
}


# app layout 
app.layout = html.Div([
    html.Div(["Sustainable Aviation Technology Dashboard"], className="bg-success text-center text-white h2 p-2"),
    color_mode_switch,
    dbc.Row([ 
         dbc.Col([ ],  width=1),
         dbc.Col([ 
             dbc.Card([  
                 dbc.CardBody([
                              html.H5('Developed by the Lab for Electric Aircraft Design and Sustainability (LEADS) at the University of Illinois Urbana-Champaign, the Sustainable Aviation Technology Dashboard is a platform to examine the integration of new energy sources such as sustainable aviation fuel (SAF), batteries and hydrogen propulsion technologies into future aircraft systems and assess their broader impact on society.'),
                            ], className='text-sm-center h5'),   
                 ],body=True)  
             ],  width=10),  
         dbc.Col([ ],  width=1),  
         html.Div([ html.Br() ]),   
        ]),  
    dcc.Tabs(id="tabs-styled-with-inline", value='tab-1', children=[
        dcc.Tab(label='Electrification', value='tab-1', style=tab_style, selected_style=electrification_tab_style),
        dcc.Tab(label='Sustainable Aviation Fuel', value='tab-2', style=tab_style, selected_style=saf_tab_style),
        dcc.Tab(label='Hydrogen', value='tab-3', style=tab_style, selected_style=hydrogen_tab_style),
        dcc.Tab(label='Energy-eX(ploration)', value='tab-4', style=tab_style, selected_style=energy_ex_tab_style),
    ],), 
    html.Div(id='tabs-content-inline'), 
    html.Div([    html.Br() ]),    
    html.Div(["Contact Us"], className="bg-dark text-center text-white h2 p-2"),
    dbc.Row([ 
         dbc.Col([ ],  width=1),
         dbc.Col([ 
             dbc.Card([   
                 dbc.CardBody([
                              html.H5('Kindly direct any questions to Dr. Matthew Clarke by sending an email to maclarke@illinois.edu. Contribute to the Dashboard by sending us information on new commercial technology or technology under development at high TRL levels (i.e. TRL > 8) using this link https://forms.gle/YPKqAuXwPZsoKcSdA.'),
                            ], className='text-sm-center h5'), 
                 ],body=True)  
             ],  width=10),  
         dbc.Col([ ],  width=1),  
         html.Div([ html.Br() ]),   
        ]),     
])


def update_figure_template(switch_off):
    template = pio.templates["minty"] if switch_off else pio.templates["minty_dark"]  
    patched_figure = Patch()
    patched_figure["layout"]["template"] = template 
    return patched_figure 

clientside_callback(
    """
    (switchOn) => {
       switchOn
         ? document.documentElement.setAttribute('data-bs-theme', 'light')
         : document.documentElement.setAttribute('data-bs-theme', 'dark')
       return window.dash_clientside.no_update
    }
    """,
    Output("color-mode-switch", "id"),
    Input("color-mode-switch", "value"),
)
 

@callback(Output('tabs-content-inline', 'children'),
            Input('tabs-styled-with-inline', 'value'), 
              )

def render_content(tab):
    
    if tab == 'tab-1':
        return  dbc.Container([     
            html.Div([ html.Br() ]),    
            html.Div(["Battery Technology"], className="bg-primary text-white h4 p-2"),
            html.Div(["Commercial Battery Cell Metrics"], className="text-white-center h4 p-2"),
            dbc.Row([ dbc.Col([battery_metrics_panel  ], xs=10, sm=11, md=4, lg=4, xl=4),  
                      dbc.Col([ dcc.Graph(id ="battery_metrics_figure", className="border-0 bg-transparent")], xs=10, sm=11, md=8, lg=8, xl=8),
                    ]),
            html.Div([    html.Br() ]),
            html.Div(["Battery Cell Comparison"], className="text-white-center h4 p-2"),   
            dbc.Row([   
                      dbc.Col([battery_comparison_panel],  xs=10, sm=11, md=4, lg=4, xl=4),    
                      dbc.Col([ dcc.Graph(id="battery_spider_plot", className="border-0 bg-transparent")],  xs=10, sm=11, md=8, lg=8, xl=8),
                    ]),  
            html.Div([    html.Br() ]), 
            html.Div(["Worldwide Battery Cell Development"], className="text-white-center h4 p-2"),    
            dbc.Row([dbc.Col([battery_development_panel  ],  xs=10, sm=11, md=4, lg=4, xl=4),   
                dbc.Col([ dcc.Graph(id="battery_map", className="border-0 bg-transparent")],  xs=10, sm=11, md=8, lg=8, xl=8),
                ]),  
            html.Div([ html.Br() ]),    
            html.Div(["Electric Motors"], className="bg-primary text-white h4 p-2"), 
            html.Div(["Motors Under Development"], className="text-white-center h4 p-2"),   
            dbc.Row([ dbc.Col([motor_metrics_panel  ],  xs=10, sm=11, md=4, lg=4, xl=4),  
                      dbc.Col([ dcc.Graph(id ="motor_metrics_figure", className="border-0 bg-transparent")],  xs=10, sm=11, md=8, lg=8, xl=8),
                    ]), 
            html.Div([    html.Br() ]),             
            html.Div(["U.S. Domestic Operations"], className="bg-primary text-white h4 p-2"), 
            dbc.Row([  dbc.Col([battery_flight_ops_aircraft_panel ],  xs=10, sm=11, md=4, lg=4, xl=4),                    
                   dbc.Col([  
                       dbc.Card([  
                       dbc.Col([     
                       html.Div(["Feasible Electrified Routes"], className="text-sm-center h5"),
                       dcc.Graph(id="electric_aircraft_flight_ops_map", className="border-0 bg-transparent"), 
                       html.Div([    html.Br() ]),
                       html.Div(["Average Monthly Temperature (deg. F)"], className="text-sm-center h5"),
                       dcc.Graph(id="US_bat_temperature_map", className="border-0 bg-transparent")                       
                       ])
                       ], className="border-0 bg-transparent")
                       
                       ],  xs=10, sm=11, md=8, lg=8, xl=8),                
                
                ]),  
            html.Div([    html.Br() ]), 
            html.Div(["Techno-economics Analysis"], className="bg-primary text-white h4 p-2"), 
            html.Div([ html.Br() ]),     
            dbc.Row([  dbc.Col([  
                       dbc.Card([  
                       dbc.Col([     
                       html.Div(["Passenger Volume vs. Distance Traveled"], className="text-sm-center h5"),  
                       dcc.Graph(id="electric_aircraft_passenger_range", className="border-0 bg-transparent" )         
                       ])
                       ], className="border-0 bg-transparent")
                       
                       ], xs=10, sm=11, md=6, lg=6, xl=6),                   
                   dbc.Col([  
                       dbc.Card([  
                       dbc.Col([     
                       html.Div(["Busiest Airports"], className="text-sm-center h5"),  
                       dcc.Graph(id="electric_aircraft_airports", className="border-0 bg-transparent" )         
                       ])
                       ], className="border-0 bg-transparent")
                       
                       ],  xs=10, sm=11, md=6, lg=6, xl=6),                
                
                ]),       
            html.Div([ html.Br() ]),
            html.Div([    html.Br() ]),  
            dbc.Row([  dbc.Col([  
                                dbc.Card([  
                                    dbc.Col([     
                                        html.Div(["Fleet Operations"], className="text-sm-center h5"),  
                                        dcc.Graph(id="electric_aircraft_market_size", className="border-0 bg-transparent" ) ])
                                    ], className="border-0 bg-transparent") 
                               ],  xs=10, sm=11, md=6, lg=6, xl=6),       
                       dbc.Col([  
                               dbc.Card([  
                               dbc.Col([     
                                   html.Div(["Cost Per Seat Mile (Energy Souce Only)"], className="text-sm-center h5"),  
                                   dcc.Graph(id="electric_aircraft_CASM", className="border-0 bg-transparent" ) ])
                                        ], className="border-0 bg-transparent") 
                               ],xs=10, sm=11, md=6, lg=6, xl=6),  
                ]), 
            html.Div([    html.Br() ]),  
            html.Div(["Climate & Emissions Impact"], className="bg-primary text-white h4 p-2"),
            html.Div([ html.Br() ]),          
            dbc.Row([                    
                   dbc.Col([  
                       dbc.Card([  
                       dbc.Col([     
                       html.Div(["Cumulative Tailpipe Fleet Emissions"], className="text-sm-center  h5"),  
                       dcc.Graph(id="electric_aircraft_yearly_emissions", className="border-0 bg-transparent" )         
                       ])
                       ], className="border-0 bg-transparent")
                       
                       ],  xs=10, sm=11, md=6, lg=6, xl=6),    
                ]),    
        ])
    
    elif tab == 'tab-2': # SAF
        return  dbc.Container([    
            html.Div([ html.Br() ]),     
            html.Div(["Sustainable Aviation Fuel"], className="bg-warning text-white h4 p-2"),
            html.Div(["Sustainable Aviation Fuel Metrics"], className="text-white-center h4 p-2"),
            dbc.Row([ dbc.Col([saf_metrics_panel  ],  xs=10, sm=11, md=4, lg=4, xl=4),  
                      dbc.Col([ dcc.Graph(id ="saf_metrics_figure", className="border-0 bg-transparent")],  xs=10, sm=11, md=8, lg=8, xl=8),
                    ]),
            html.Div([    html.Br() ]), 
            html.Div(["Sustainable Aviation Fuel Development"], className="text-white-center h4 p-2"),    
            dbc.Row([dbc.Col([saf_development_panel],  xs=10, sm=11, md=4, lg=4, xl=4),   
                dbc.Col([ dcc.Graph(id="saf_production_map", className="border-0 bg-transparent")],  xs=10, sm=11, md=8, lg=8, xl=8),
                ]),   
            html.Div([    html.Br() ]),             
            html.Div(["U.S. Domestic Operations"], className="bg-warning text-white h4 p-2"), 
             

            dbc.Card([  
               dbc.Col([  
               html.Div(["Select Jet-A and SAF Fuel Vendors"], className="text-sm-center h5"), 
               saf_flight_ops_fuel_panel,
               html.Div(["Select Jet-A and SAF Fuel Ratios (%)"], className="text-sm-center h5"),
               dbc.Card([
                   dcc.RangeSlider(0, 100, value=[],  pushable=1, id='fuel_usage'),
                   dcc.Graph(id="SAF_usage_dynamic_bar", className="border-0 bg-transparent" ),
               ], className="border-0 bg-transparent"),
               html.Div([    html.Br() ]),      
               html.Div(["Select States Where Feedstock (Crop) Is Sourced"], className="text-sm-center h5"), 
               saf_flight_ops_states_panel   
               ])
               ], className="border-0 bg-transparent"),             
            dbc.Row([  dbc.Col([
                dbc.Card([
                    feedstock,
                    flight_ops_saf_adoption_frac,
                    saf_airports,
                    saf_cost],body=True,) 
                ],  xs=10, sm=11, md=4, lg=4, xl=4),                    
                   dbc.Col([  
                       dbc.Card([  
                       dbc.Col([     
                       html.Div(["U.S. Domestic Routes"], className="text-sm-center h5"),
                       dcc.Graph(id="saf_flight_ops_map", className="border-0 bg-transparent"), 
                       html.Div([    html.Br() ]),
                       html.Div(["Land Required for Single Feedstock Crop Production"], className="text-sm-center h5"),
                       dcc.Graph(id="saf_feedstock_map", className="border-0 bg-transparent")                       
                       ])
                       ], className="border-0 bg-transparent")
                       
                       ],  xs=10, sm=11, md=8, lg=8, xl=8), 
                ]),  
            html.Div([    html.Br() ]), 
            html.Div(["Techno-economics Analysis"], className="bg-warning text-white h4 p-2"),    
            html.Div([ html.Br() ]),  
            dbc.Row([  dbc.Col([  
                       dbc.Card([  
                       dbc.Col([     
                       html.Div(["Passenger Volume vs. Distance Traveled"], className="text-sm-center h5"),  
                       dcc.Graph(id="saf_aircraft_passenger_range", className="border-0 bg-transparent" )         
                       ])
                       ], className="border-0 bg-transparent")
                       
                       ],  xs=10, sm=11, md=6, lg=6, xl=6),                   
                   dbc.Col([  
                       dbc.Card([  
                       dbc.Col([     
                       html.Div(["Busiest Airports"], className="text-sm-center h5"),  
                       dcc.Graph(id="saf_aircraft_airports", className="border-0 bg-transparent" )         
                       ])
                       ], className="border-0 bg-transparent")
                       
                       ],  xs=10, sm=11, md=6, lg=6, xl=6),                
                
                ]),       
            html.Div([ html.Br() ]),
            html.Div([    html.Br() ]),  
            dbc.Row([  dbc.Col([  
                                dbc.Card([  
                                    dbc.Col([     
                                        html.Div(["Fleet Operations"], className="text-sm-center h5"),  
                                        dcc.Graph(id="saf_aircraft_market_size", className="border-0 bg-transparent" ) ])
                                    ], className="border-0 bg-transparent") 
                               ],  xs=10, sm=11, md=6, lg=6, xl=6),       
                       dbc.Col([  
                               dbc.Card([  
                               dbc.Col([     
                                   html.Div(["Cost Per Seat Mile (Energy Source Only)"], className="text-sm-center h5"),  
                                   dcc.Graph(id="saf_CASM", className="border-0 bg-transparent" ) ])
                                        ], className="border-0 bg-transparent") 
                               ],xs=10, sm=11, md=6, lg=6, xl=6),  
                ]), 
            html.Div([    html.Br() ]),  
            html.Div(["Climate & Emissions Impact"], className="bg-warning text-white h4 p-2"),   
            html.Div([    html.Br() ]),       
            dbc.Row([   
                      dbc.Col([  
                          dbc.Card([  
                          dbc.Col([     
                          html.Div(["Cumulative Tailpipe Fleet Emissions"], className="text-sm-center  h5"),  
                          dcc.Graph(id="SAF_yearly_emissions", className="border-0 bg-transparent" )  ])
                          ], className="border-0 bg-transparent") 
                          ],  xs=10, sm=11, md=6, lg=6, xl=6),  
                      
                       dbc.Col([  
                                dbc.Card([  
                                    dbc.Col([     
                                        html.Div(["Life Cycle Analysis"], className="text-sm-center h5"),  
                                        dcc.Graph(id="saf_LCA", className="border-0 bg-transparent" ) ])
                                    ], className="border-0 bg-transparent") 
                               ],  xs=10, sm=11, md=6, lg=6, xl=6),    
                ]),    
            ])
    
    elif tab == 'tab-3': # HYDROGEN 
        return dbc.Container([    
            html.Div([ html.Br() ]),     
            html.Div(["Hydrogen"], className="bg-info text-white h4 p-2"),  
            #html.Div(["Hydrogen Development"], className="text-white-center h4 p-2"),    
            #dbc.Row([dbc.Col([saf_development_panel],  xs=10, sm=11, md=4, lg=4, xl=4),   
                #dbc.Col([ dcc.Graph(id="h2_production_map", className="border-0 bg-transparent")],  xs=10, sm=11, md=8, lg=8, xl=8),
                #]),   
            #html.Div([    html.Br() ]),             
            html.Div(["U.S. Domestic Operations"], className="bg-info text-white h4 p-2"),  
            dbc.Card([  
               dbc.Col([  
               html.Div(["Select Hydrogen Fuel Types"], className="text-sm-center h5"), 
               h2_flight_ops_fuel_panel,
               html.Div(["Select Hydrogen Fuel Ratios (%)"], className="text-sm-center h5"),
               dbc.Card([
                   dcc.RangeSlider(0, 100, value=[],  pushable=1, id='h2_color_ratio'),
                   dcc.Graph(id="h2_color_ratio_dynamic_bar", className="border-0 bg-transparent" ),
               ], className="border-0 bg-transparent"),  
               ])
               ], className="border-0 bg-transparent"),             
            dbc.Row([  dbc.Col([
                dbc.Card([
                    h2_fleet_adoption, 
                    h2_airports,     
                    h2_cost,           
                    h2_altitude,      
                    h2_vol_fraction,   
                    h2_engine_SFC,
                    ],body=True,) 
                ],  xs=10, sm=11, md=4, lg=4, xl=4),                    
                   dbc.Col([  
                       dbc.Card([  
                       dbc.Col([     
                       html.Div(["U.S. Domestic Routes"], className="text-sm-center h5"),
                       dcc.Graph(id="h2_flight_ops_map", className="border-0 bg-transparent"),                   
                       ])
                       ], className="border-0 bg-transparent")
                       
                       ],  xs=10, sm=11, md=8, lg=8, xl=8), 
                ]),  
            html.Div([    html.Br() ]), 
            html.Div(["Techno-economics Analysis"], className="bg-info text-white h4 p-2"),    
            html.Div([ html.Br() ]),  
            dbc.Row([  dbc.Col([  
                       dbc.Card([  
                       dbc.Col([     
                       html.Div(["Passenger Volume vs. Distance Traveled"], className="text-sm-center h5"),  
                       dcc.Graph(id="h2_aircraft_passenger_range", className="border-0 bg-transparent" )         
                       ])
                       ], className="border-0 bg-transparent")
                       
                       ],  xs=10, sm=11, md=6, lg=6, xl=6),                   
                   dbc.Col([  
                       dbc.Card([  
                       dbc.Col([     
                       html.Div(["Busiest Airports"], className="text-sm-center h5"),  
                       dcc.Graph(id="h2_aircraft_airports", className="border-0 bg-transparent" )         
                       ])
                       ], className="border-0 bg-transparent")
                       
                       ],  xs=10, sm=11, md=6, lg=6, xl=6),                
                
                ]),       
            html.Div([ html.Br() ]),
            html.Div([    html.Br() ]),  
            dbc.Row([  dbc.Col([  
                                dbc.Card([  
                                    dbc.Col([     
                                        html.Div(["Fleet Operations"], className="text-sm-center h5"),  
                                        dcc.Graph(id="h2_aircraft_market_size", className="border-0 bg-transparent" ) ])
                                    ], className="border-0 bg-transparent") 
                               ],  xs=10, sm=11, md=6, lg=6, xl=6),       
                       dbc.Col([  
                               dbc.Card([  
                               dbc.Col([     
                                   html.Div(["Cost Per Seat Mile (Energy Source Only)"], className="text-sm-center h5"),  
                                   dcc.Graph(id="h2_CASM", className="border-0 bg-transparent" ) ])
                                        ], className="border-0 bg-transparent") 
                               ],xs=10, sm=11, md=6, lg=6, xl=6),  
                ]), 
            html.Div([    html.Br() ]),  
            html.Div(["Climate & Emissions Impact"], className="bg-info text-white h4 p-2"),   
            html.Div([    html.Br() ]),       
            dbc.Row([    
                       dbc.Col([  
                                dbc.Card([  
                                    dbc.Col([     
                                        html.Div(["Carbom Emissions"], className="text-sm-center h5"),  
                                        dcc.Graph(id="h2_CO2e", className="border-0 bg-transparent" ) ])
                                    ], className="border-0 bg-transparent") 
                               ],  xs=10, sm=11, md=6, lg=6, xl=6),    
                ]),    
            ])
    elif tab == 'tab-4': # ENERGY EX
        return dbc.Container([    
            html.Div([    html.Br() ]),              
            html.Div(["Future Electrochemical Cell (Battery) Impact Predictor"], className="bg-secondary text-white h4 p-2"), 
            dbc.Row([  dbc.Col([  
                html.Div(["Aircraft Parameterization"], className="text-sm-center h5"),                
                Energy_X_aircraft_flight_ops_panel,  
                html.Div([    html.Br() ]),                  
                html.Div(["Battery Cell Parameterization"], className="text-sm-center h5"),                
                Energy_X_battery_panel,
                ],  xs=10, sm=11, md=4, lg=4, xl=4),                    
                   dbc.Col([  
                       dbc.Card([  
                       dbc.Col([     
                       html.Div([    html.Br() ]),
                       html.Div([    html.Br() ]),
                       html.Div([    html.Br() ]),                  
                       html.Div(["Feasible Routes"], className="text-sm-center h5"),
                       dcc.Graph(id="EX_flight_ops_map", className="border-0 bg-transparent"), 
                       html.Div([    html.Br() ]),
                       html.Div([    html.Br() ]),
                       html.Div([    html.Br() ]),
                       html.Div(["Average Monthly Temperature (deg. F)"], className="text-sm-center h5"),
                       dcc.Graph(id="EX_us_temperature_map", className="border-0 bg-transparent")                       
                       ])
                       ], className="border-0 bg-transparent")
                       
                       ],  xs=10, sm=11, md=8, lg=8, xl=8),                
                
                ]),  
            html.Div([    html.Br() ]), 
            html.Div(["Techno-economics of Single U.S. Airline Operation"], className="bg-secondary text-white h4 p-2"),     
            dbc.Row([  dbc.Col([  
                       dbc.Card([  
                       dbc.Col([     
                       html.Div(["Passenger Volume vs Distance Traveled"], className="text-sm-center h5"),  
                       dcc.Graph(id="EX_aircraft_passenger_range", className="border-0 bg-transparent" )         
                       ])
                       ], className="border-0 bg-transparent")
                       
                       ],  xs=10, sm=11, md=6, lg=6, xl=6),                   
                   dbc.Col([  
                       dbc.Card([  
                       dbc.Col([     
                       html.Div(["Busiest Airports"], className="text-sm-center h5"),  
                       dcc.Graph(id="EX_aircraft_airports", className="border-0 bg-transparent" )         
                       ])
                       ], className="border-0 bg-transparent")
                       
                       ],  xs=10, sm=11, md=6, lg=6, xl=6),                
                
                ]),  
            html.Div([ html.Br() ]),
            html.Div([    html.Br() ]), 
            dbc.Row([  dbc.Col([  
                                 dbc.Card([  
                                 dbc.Col([     
                                     html.Div(["Fleet Operations"], className="text-sm-center h5"),  
                                     dcc.Graph(id="EX_aircraft_market_size", className="border-0 bg-transparent" ) ])
                                          ], className="border-0 bg-transparent")
                               ], xs=10, sm=11, md=6, lg=6, xl=6), 
                       dbc.Col([  
                               dbc.Card([  
                               dbc.Col([     
                                   html.Div(["Cost Per Seat Mile (Energy Souce Only)"], className="text-sm-center h5"),  
                                   dcc.Graph(id="EX_aircraft_CASM", className="border-0 bg-transparent" ) ])
                                        ], className="border-0 bg-transparent") 
                               ],xs=10, sm=11, md=6, lg=6, xl=6),        
                ]), 
            html.Div([    html.Br() ]),          
            html.Div(["Climate & Emissions Impact"], className="bg-secondary text-white h4 p-2"),        
            dbc.Row([                  
                       dbc.Col([  
                       dbc.Card([  
                       dbc.Col([     
                       html.Div(["Cumulative Tailpipe Fleet Emissions"], className="text-sm-center h5"),  
                       dcc.Graph(id="EX_aircraft_yearly_emissions", className="border-0 bg-transparent" )         
                       ])
                       ], className="border-0 bg-transparent")
                       
                       ],  xs=10, sm=11, md=6, lg=6, xl=6),      
                ]),               
        ])  


# ---------------------------------------------------------------------------------------------------------------------------------------------------
# Battery Tab 
# ---------------------------------------------------------------------------------------------------------------------------------------------------
@callback(
    Output("battery_metrics_figure", "figure"),
    Input("battery_brand_metrics", "value"),
    Input("battery_chemistry_metrics", "value"),
    Input("battery_x_axis_metrics", "value"),
    Input("battery_y_axis_metrics", "value"),
    Input("color-mode-switch", "value"), 
)  
def update_battery_metrics_figure(selected_brand,selected_chemistry,selected_x_axis,selected_y_axis,switch_off):   
    fig = generate_battery_scatter_plot(Commercial_Batteries,selected_brand,selected_chemistry,selected_x_axis,selected_y_axis,switch_off)  
    return fig    
 
@callback(
    Output("battery_spider_plot", "figure"),
    Input("battery_1", "value"),
    Input("battery_2", "value"),
    Input("battery_3", "value"),
    Input("color-mode-switch", "value"), 
)
def update_battery_comparison_figure(bat_1,bat_2,bat_3,switch_off):     
    fig_2 = generate_battery_spider_plot(Commercial_Batteries,bat_1,bat_2,bat_3,switch_off)  
    return fig_2  

@callback(
    Output("battery_map", "figure"),
    Input("battery_sector", "value"),
    Input("battery_type", "value"),
    Input("color-mode-switch", "value"), 
) 
def update_sector_map(sector,bat_type,switch_off): 
    technology_filename  = '..' + separator + 'Data'  + separator + 'Technology' + separator +  'Technology_Data.xlsx'
    SAT_data             = pd.read_excel(technology_filename,sheet_name=['Commercial_Batteries','Battery_Development']) 
    Commercial_Batteries = SAT_data['Commercial_Batteries'] 
    a                    = Commercial_Batteries['Brand']  
    b                    = Commercial_Batteries['Abbreviation']
    c                    = Commercial_Batteries['Model']
    d                    = a + ': ' + b + '-' + c 
    Commercial_Batteries["Battery Name"] = d     
    Battery_Development     = SAT_data['Battery_Development']    
    fig_3 = generate_battery_dev_map(Battery_Development,sector,bat_type,switch_off)  
    return fig_3 

@callback(
    Output("motor_metrics_figure", "figure"), 
    Input("motor_x_axis_metrics", "value"),
    Input("motor_y_axis_metrics", "value"),
    Input("color-mode-switch", "value"), 
)  
def update_motor_metrics_figure(selected_x_axis,selected_y_axis,switch_off):   
    fig = generate_motor_scatter_plot(Electric_Motor_Development,selected_x_axis,selected_y_axis,switch_off) 
    return fig    
  
@callback( 
    Output("electric_aircraft_flight_ops_map", "figure"),    
    Output("electric_aircraft_passenger_range", "figure"),
    Output("electric_aircraft_airports", "figure"),
    Output("electric_aircraft_market_size", "figure"),
    Output("electric_aircraft_yearly_emissions", "figure"),
    Output("electric_aircraft_CASM", "figure"),
    Input("electric_aircraft_type", "value"),
    Input("electric_airline_type", "value"),
    Input("electric_aircraft_battery", "value"),
    Input("battery_mass_fraction", "value"),
    Input("electric_aircraft_system_voltage", "value"),
    Input("electric_aircraft_efficiency", "value"),
    Input("electric_aircraft_percent_adoption", "value"),
    Input("electric_aircraft_month", "value"),
    Input("electric_aircraft_charging_cost","value"),
    Input("color-mode-switch", "value"), 
)   
def update_flight_ops_map(aircraft,airline,battery_choice,weight_fraction,system_voltage,propulsive_efficiency,percent_adoption,month_no,cost_of_electricity,switch_off): 
    fig_4,fig_5, fig_6 ,fig_7,fig_8,fig_9 = generate_flight_ops_map(Flight_Ops,Commercial_Batteries,aircraft,airline,battery_choice,weight_fraction,system_voltage,propulsive_efficiency,percent_adoption,month_no,cost_of_electricity,switch_off)     
    return fig_4,fig_5, fig_6 ,fig_7,fig_8 , fig_9  
 

# ---------------------------------------------------------------------------------------------------------------------------------------------------
# SAF Tab  
# ---------------------------------------------------------------------------------------------------------------------------------------------------

@callback(
    Output("fuel_usage", "value"),
    Input("fuel_selection_list_1", "value"),
    Input("fuel_selection_list_2", "value"), 
    Input("color-mode-switch", "value"), 
) 
def update_fuel_usage(fuel_selection_list_1,fuel_selection_list_2,switch_off):   
    selected_fuels = fuel_selection_list_1 + fuel_selection_list_2
    values         = list(np.linspace(65, 95,len(selected_fuels)-1)) 
    return values 

@callback(
    Output("SAF_usage_dynamic_bar", "figure"),
    Input("fuel_selection_list_1", "value"),
    Input("fuel_selection_list_2", "value"),
    Input("fuel_usage", "value"),  
    Input("color-mode-switch", "value"), 
) 
def update_fuel_usage_bar(fuel_selection_list_1,fuel_selection_list_2,SAF_ratios,switch_off):     
    selected_fuels = fuel_selection_list_1 + fuel_selection_list_2
    if len(selected_fuels) == 0: 
        return dash.no_update
    else: 
        saf_fig  = generate_saf_slider_bar(Commercial_SAF,selected_fuels,SAF_ratios,switch_off)
    return saf_fig  

@callback(
    Output("saf_metrics_figure", "figure"),
    Input("saf_process_metrics", "value"),
    Input("saf_feedstock_metrics", "value"),
    Input("saf_x_axis_metrics", "value"),
    Input("saf_y_axis_metrics", "value"),
    Input("color-mode-switch", "value"), 
)  
def update_saf_metrics_figure(selected_process,selected_feedstock,selected_x_axis,selected_y_axis,switch_off):   
    saf_fig_1 = generate_saf_scatter_plot(Commercial_SAF,selected_process,selected_feedstock,selected_x_axis,selected_y_axis,switch_off)  
    return saf_fig_1    
  

@callback(
    Output("saf_production_map", "figure"),
    Input("saf_feedstock_sector", "value"),
    Input("saf_process_sector", "value"),
    Input("color-mode-switch", "value"), 
) 
def update_sector_map(selected_feedstock,selected_process,switch_off):     
    saf_fig_2 = generate_saf_dev_map(Commercial_SAF,selected_feedstock,selected_process,switch_off)
    return saf_fig_2  
  
@callback( 
    Output("saf_flight_ops_map", "figure"),    
    Output("saf_feedstock_map", "figure"),
    Output("saf_aircraft_passenger_range", "figure"),
    Output("saf_aircraft_airports", "figure"),    
    Output("saf_aircraft_market_size", "figure"), 
    Output("saf_CASM", "figure"),   
    Output("SAF_yearly_emissions", "figure"),
    Output("saf_LCA", "figure"),  
    Input("fuel_selection_list_1", "value"),
    Input("fuel_selection_list_2", "value"),
    Input("saf_feedstock_source", "value"),
    Input("fuel_usage", "value"),
    Input("feedstock_states_1", "value"),
    Input("feedstock_states_2", "value"),
    Input("feedstock_states_3", "value"),
    Input("feedstock_states_4", "value"),
    Input("feedstock_states_5", "value"),
    Input("feedstock_states_6", "value"),
    Input("saf_airports","value"),
    Input("saf_percent_adoption","value"),
    Input("SAF_dollars_per_gal","value"),
    Input("color-mode-switch", "value"), 
)  

def update_SAF_flight_ops_map(fuel_selection_list_1,fuel_selection_list_2,
                                    selected_feedstock,percent_fuel_use,
                                    State_List_1,State_List_2,State_List_3,State_List_4,State_List_5,State_List_6,
                                    selected_airpots, percent_adoption,SAF_dollars_per_gal,switch_off):  
    
    feedstock_producing_states      = State_List_1 + State_List_2 + State_List_3 + State_List_4 + State_List_5 + State_List_6    
    selected_fuels                  = fuel_selection_list_1 + fuel_selection_list_2
    
    saf_fig_3, saf_fig_4,saf_fig_5, saf_fig_6, saf_fig_7, saf_fig_8, saf_fig_9 , saf_fig_10  = generate_saf_flight_operations_plots(Flight_Ops,Commercial_SAF,feedstocks,
                                    selected_fuels,
                                    selected_feedstock,percent_fuel_use,
                                    feedstock_producing_states,
                                    selected_airpots, percent_adoption,SAF_dollars_per_gal,switch_off)
    return saf_fig_3, saf_fig_4,saf_fig_5, saf_fig_6, saf_fig_7, saf_fig_8, saf_fig_9 , saf_fig_10  

# ---------------------------------------------------------------------------------------------------------------------------------------------------
# Hydrogen Tab  
# ---------------------------------------------------------------------------------------------------------------------------------------------------

@callback(
    Output("h2_color_ratio", "value"),
    Input("h2_selection_list_1", "value"),
    Input("h2_selection_list_2", "value"), 
    Input("color-mode-switch", "value"), 
) 
def update_fuel_usage(h2_selection_list_1,h2_selection_list_2,switch_off):   
    selected_h2 = h2_selection_list_1 + h2_selection_list_2
    h2_values         = list(np.linspace(65, 95,len(selected_h2)-1)) 
    return h2_values 

@callback(
    Output("h2_color_ratio_dynamic_bar", "figure"),
    Input("h2_selection_list_1", "value"),
    Input("h2_selection_list_2", "value"),
    Input("h2_color_ratio", "value"),  
    Input("color-mode-switch", "value"), 
) 
def update_h2_color_ratio_bar(h2_selection_list_1,h2_selection_list_2,h2_ratios,switch_off):     
    selected_h2 = h2_selection_list_1 + h2_selection_list_2
    if len(selected_h2) == 0: 
        return dash.no_update
    else: 
        h2_fig  = generate_saf_slider_bar(Hydrogen,selected_h2,h2_ratios,switch_off)
    return h2_fig   
 
@callback( 
    Output("h2_flight_ops_map", "figure"),   
    Output("h2_aircraft_passenger_range", "figure"),
    Output("h2_aircraft_airports", "figure"),    
    Output("h2_aircraft_market_size", "figure"), 
    Output("h2_CASM", "figure"),    
    Output("h2_CO2e", "figure"),  
    Input("h2_selection_list_1", "value"),
    Input("h2_selection_list_2", "value"), 
    Input("h2_SFC","value"),
    Input("h2_cruise_alt","value"),
    Input("h2_airports","value"),
    Input("h2_color_ratio", "value"), 
    Input("h2_volume","value"),
    Input("h2_percent_adoption","value"),
    Input("h2_dollars_per_gal","value"),
    Input("color-mode-switch", "value"), 
)  

def update_H2_flight_ops_map(h2_selection_list_1,h2_selection_list_2,mean_SFC_Imperial,h2_cruise_alt,h2_airports,percent_H2_color,
                                        h2_vol_percentage,h2_percent_adoption,H2_dollars_per_gal,switch_off):  
        
    selected_h2                  = h2_selection_list_1 + h2_selection_list_2
    
    h2_fig_1, h2_fig_2, h2_fig_3, h2_fig_4,h2_fig_5 ,h2_fig_6 = generate_electric_flight_operations_plots(Flight_Ops,Hydrogen,
                                                        selected_h2,mean_SFC_Imperial,h2_cruise_alt,h2_airports,percent_H2_color,
                                                        h2_vol_percentage,h2_percent_adoption,H2_dollars_per_gal,switch_off)
    
    return h2_fig_1, h2_fig_2, h2_fig_3, h2_fig_4,h2_fig_5 ,h2_fig_6 

# ---------------------------------------------------------------------------------------------------------------------------------------------------
# Energy Exploration Tab 
# ---------------------------------------------------------------------------------------------------------------------------------------------------
@callback(
    Output("US_bat_temperature_map", "figure"),
    Input("electric_aircraft_month", "value"),
    Input("color-mode-switch", "value"),
)
def update_US_bat_temperature_map(month_no,switch_off):
    temperature_filename = '..' + separator + 'Data' + separator  + 'US_Climate' + separator + 'Monthly_US_County_Temperature_2019.csv' 
    US_Temperature_F     = pd.read_csv(temperature_filename)        
    fig_6                = generate_US_bat_temperature_map(US_Temperature_F,month_no,switch_off)  
    return fig_6  


@callback(
    Output("EX_us_temperature_map", "figure"),
    Input("EX_aircraft_month", "value"),
    Input("color-mode-switch", "value"),
)
def update_EX_bat_temperature_map(month_no,switch_off): 
    temperature_filename = '..' + separator + 'Data' + separator  + 'US_Climate' + separator + 'Monthly_US_County_Temperature_2019.csv' 
    US_Temperature_F     = pd.read_csv(temperature_filename) 
    fig_ex_6             = generate_US_EX_temperature_map(US_Temperature_F,month_no,switch_off)  
    return fig_ex_6   
  
 
@callback(
    Output("EX_flight_ops_map", "figure"),
    Output("EX_aircraft_passenger_range", "figure"),
    Output("EX_aircraft_airports", "figure"),
    Output("EX_aircraft_market_size", "figure"),
    Output("EX_aircraft_yearly_emissions", "figure"),    
    Output("EX_aircraft_CASM", "figure"),   
    Input("EX_system_voltage", "value"), 
    Input("EX_battery_mass_fraction", "value"),
    Input("EX_aircraft_efficiency", "value"), 
    Input("EX_voltage", "value"),
    Input("EX_capacity", "value"),
    Input("EX_C_max", "value"),
    Input("EX_e0", "value"),
    Input("EX_temperature_range", "value"),     
    Input("EX_percent_adoption", "value"), 
    Input("EX_aircraft_month", "value"),  
    Input("EX_aircraft_charging_cost", "value"), 
    Input("color-mode-switch", "value"), 
)   
def update_flight_ops_passenger_range_plot(EX_system_V,EX_bat_frac,EX_eta,EX_cell_V,
                                           EX_capacity,EX_C_max,EX_e0,EX_Temp,EX_adoption,EX_month,cost_of_electricity,switch_off):  
    fig_ex_4, fig_ex_5, fig_ex_6 ,fig_ex_7,fig_ex_8,fig_ex_9 = generate_EX_aircraft_flight_ops(Flight_Ops,EX_system_V,EX_bat_frac,EX_eta,
                                                                                      EX_cell_V, EX_capacity,EX_C_max,EX_e0,EX_Temp,EX_adoption,EX_month,cost_of_electricity,switch_off)  
    return fig_ex_4,fig_ex_5, fig_ex_6 ,fig_ex_7,fig_ex_8,fig_ex_9 
    
if __name__ == "__main__":
    app.run_server(debug=True, port=8051)
    
    