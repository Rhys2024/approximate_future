import plotly.graph_objs as go
from itertools import cycle

from lorenz import *

import streamlit as st



st.set_page_config(
    page_title="Approximate Future",
    layout="wide",
    #initial_sidebar_state="collapsed",
)


perspective_options = ['3d', 'x-y', 'x-z', 'y-z']
coloring_options = ['Color by Paths', 'Color by Magnitude']



st.cache()
def fetch_sols(initial_conds, lorenz_params, 
                  n_trajectories, travel_time,
                  trace_depth,  
                  clouds):
    
    lorenz_solutions = system_solutions(initial_conds=initial_conds,
                                    lorenz_params = lorenz_params,
                                    n_trajectories = n_trajectories,
                                    travel_time = travel_time,
                                    depth = trace_depth, 
                                    cloud_size=clouds)
    
    return lorenz_solutions


st.cache()
def create_figure(lorenz_solutions, perspective, 
                  coloring_method):

    path_num = st.session_state['path_num']
    

    N = lorenz_solutions[0].shape[1]
    
    
    if coloring_method == 'Color by Magnitude':
        kind = 'markers'
    else:
        kind = 'lines'
    
    
    if perspective == '3d':
        scatter_fig = go.Scatter3d(
                        x=lorenz_solutions[path_num-1][0], 
                        y=lorenz_solutions[path_num-1][1],
                        z=lorenz_solutions[path_num-1][2],
                            mode='lines',
                            line=dict(
                                color = 'antiquewhite',
                                width=.5,
                                ),
                            name='Your Path'
                            )
        fig_frames = [go.Frame(
                    data=[go.Scatter3d(
                        x=[lorenz_solutions[path_num-1][0][k]], 
                        y=[lorenz_solutions[path_num-1][1][k]],
                        z=[lorenz_solutions[path_num-1][2][k]],
                        mode="markers",
                        marker=dict(
                                    color='greenyellow',
                                    size=10),
                        marker_symbol = 'diamond'
                        
                        ),
                          
                    ]
                    )
                      
                    for k in range(N)]
        
    elif perspective == 'x-y':
        scatter_fig = go.Scatter(x=lorenz_solutions[path_num-1][0], 
                         y=lorenz_solutions[path_num-1][1],
                            mode='lines',
                            line=dict(
                                color = 'antiquewhite',
                                width=.2,
                                ),
                            name='Your Path'
                            )
        fig_frames = [go.Frame(
                    data=[go.Scatter(
                        x=[lorenz_solutions[path_num-1][0][k]], 
                        y=[lorenz_solutions[path_num-1][1][k]],
                            mode="markers",
                        marker=dict(color="greenyellow", size=15)
                            )
                    ])
                      
                    for k in range(N)]
        
    elif perspective == 'x-z':
        scatter_fig = go.Scatter(x=lorenz_solutions[path_num-1][0], 
                         y=lorenz_solutions[path_num-1][2],
                            mode='lines',
                            line=dict(
                                color = 'antiquewhite',
                                width=.2,
                                ),
                            name='Your Path'
                            )
        fig_frames = [go.Frame(
                    data=[go.Scatter(
                        x=[lorenz_solutions[path_num-1][0][k]], 
                        y=[lorenz_solutions[path_num-1][2][k]],
                        mode="markers",
                        marker=dict(color="greenyellow", size=15)
                            )
                    ])
                    for k in range(N)]
        
    elif perspective == 'y-z':
        scatter_fig = go.Scatter(x=lorenz_solutions[path_num-1][1], 
                         y=lorenz_solutions[path_num-1][2],
                            mode='lines',
                            line=dict(
                                color = 'antiquewhite',
                                width=.2,
                                ),
                            name='Your Path'
                            )
        fig_frames = [go.Frame(
                    data=[go.Scatter(
                        x=[lorenz_solutions[path_num-1][1][k]],
                        y=[lorenz_solutions[path_num-1][2][k]],
                            mode="markers",
                            marker=dict(color="greenyellow", size=15)
                            )
                    ])
                      
                    for k in range(N)]

    fig = go.Figure(
        
        #data = [scatter_fig],
        
        frames = fig_frames,
        
        layout=go.Layout(
        title_text="this is the APROXIMATE FUTURE you have created.", 
        hovermode="closest",
        updatemenus=[dict(type="buttons",
                          buttons=[dict(label="Show Your Path",
                                        method="animate",
                                        args=[None, 
                                              {"frame": {"duration": 0, "redraw": True},
                                            "fromcurrent": False,
                                            "transition": {"duration": 0,
                                             "easing": "quadratic-in-out"
                                            },
                                            "mode": "immediate"
                                            }],
                                        ),
                                   {"label": "Pause Path",
                                    "args": [[None], {"frame": {"duration": 0, "redraw": False},
                                                    "mode": "immediate",
                                                    "transition": {"duration": 0}}],
                                    "method": "animate"
                                }
                                ], 
                          showactive = False,
                          pad = {"r": 10, "t": 87},
                          )
                     
                     ]),
        
        )
    

    for sols in lorenz_solutions:

        x, y, z = sols
        
        if perspective == '3d':
            fig.add_scatter3d(x=x, y=y, z=z , 
                                mode=kind, 
                                marker=dict(
                                size=4,
                                color= np.sqrt(np.power(x, 2) + np.power(y, 2) + np.power(z, 2)),
                                colorscale='jet',
                                ),
                                line=dict(
                                width=2,
                                ),
                            )
        elif perspective == 'x-y':
            fig.add_scatter(x=x, y=y, 
                            mode=kind,
                            marker=dict(
                                size=7,
                                color= np.power(z, 2),
                                colorscale='jet',
                                ),
                            line=dict(
                                width=2,
                                ),
                            )
        elif perspective == 'x-z':
            fig.add_scatter(x=x, y=z,
                            mode=kind,
                            marker=dict(
                                size=7,
                                color= np.power(y, 2),
                                #color = Lorenz(0, [x, y, z]),
                                colorscale='jet',
                                ),
                            line=dict(
                                width=2,
                                ),
                            )
        elif perspective == 'y-z':
            fig.add_scatter(x=y, y=z, 
                            mode=kind,
                            marker=dict(
                                size=7,
                                color= np.power(x, 2),
                                colorscale='jet',
                                ),
                            line=dict(
                                width=2,
                                ),
                            )
    
    
    fig.add_trace(scatter_fig)
    
    fig.update_layout(
            #width=800,
            height=700,
            autosize=False,
            scene=dict(
                camera=dict(
                    up=dict(
                        x=0,
                        y=0,
                        z=1
                    ),
                    eye=dict(
                        x=0,
                        y=1.0707,
                        z=1,
                    )
                ),
                aspectratio = dict(x=1, y=1, z=0.7 ),
                aspectmode = 'manual',
                
            ),
        )
    
    #fig.add_annotation(bordercolor = 'red',)
    
    if perspective == '3d':
        fig.update_layout(
            
            scene = dict(
            xaxis=dict(range=[np.max(lorenz_solutions[path_num-1][0]), 
                                           np.min(lorenz_solutions[path_num-1][0])], 
                       autorange=True, 
                       zeroline=False,
                       showgrid=False,
                       visible=False
                       ),
            yaxis = dict(range=[np.max(lorenz_solutions[path_num-1][1]), 
                                      np.min(lorenz_solutions[path_num-1][1])], 
                         autorange=True, 
                         zeroline=False,
                         showgrid=False,
                         visible=False
                        ),
            zaxis=dict(range=[np.max(lorenz_solutions[path_num-1][2]), 
                              np.min(lorenz_solutions[path_num-1][2])], 
                       autorange=True, 
                       zeroline=False,
                       showgrid=False,
                       visible=False
                        ),
            
            )
            )
    else:
        fig.update_layout(
            
            xaxis=dict(range=[np.max(lorenz_solutions[path_num-1][0]), 
                                           np.min(lorenz_solutions[path_num-1][0])], 
                       autorange=True,
                       zeroline=False,
                       showgrid=False,
                       visible=False
                       ),
            yaxis = dict(range=[np.max(lorenz_solutions[path_num-1][1]), 
                                      np.min(lorenz_solutions[path_num-1][1])], 
                         autorange=True,
                         zeroline=False,
                         showgrid=False,
                         visible=False
                         ),
        )
    
    if coloring_method == 'Color by Magnitude':
        
        for trace in fig['data']:
            if trace['name'] != 'Your Path':
                trace['showlegend'] = False
    #else:
        #for trace in fig['data']:
            #if trace['name'] == 'Your Path':
                #trace['showlegend'] = False
    
    
    return fig





#st.title('Approximate Future')


st.header(":red[The present determines the future, but the approximate present does not approximately determine the future.]")

st.divider()

st.markdown("Let Lorenz guide you...")

latex_cols = st.columns(3)



latex_cols[0].latex(r"\colorbox{red}{${Lorenz} : \mathbb{R}^3 \rightarrow \mathbb{R}^3$}")
latex_cols[1].latex(r"""\colorbox{red}{$\textcolor{black}{ {s}.{t} \begin{pmatrix} x \\ y \\ z \end{pmatrix} \rightarrow \begin{cases} \sigma (x - y) \\
          x(\rho - z) - y \\ 
          xy - \beta z \end{cases}}$}""")
latex_cols[2].latex(r"\colorbox{red}{${where} \hspace{.4cm} \sigma, \rho, \beta \in \mathbb{R}$}")


st.divider()
    
cols = st.columns(3)

with cols[0]:
    
    #st.write('')

    x0 = st.number_input('what is your approximate present?.1', step=10)
    y0 = st.number_input('what is your approximate present?.2', step=10)
    z0 = st.number_input('what is your approximate present?.3', step=10)
    
    initial_conds = [x0, y0, z0]


with cols[1]:
    
    sigma = st.number_input('how will you alter your approximate future?.1', value = 10.0, step=1.00, min_value=0.0)
    beta = st.number_input('how will you alter your approximate future?.2', value=8/3, step=1.00, min_value=0.0)
    rho = st.number_input('how will you alter your approximate future?.3', value=28.0, step=1.00, min_value=0.0)
    
    lorenz_params = [sigma, beta, rho]
    
    
with cols[2]:
    
    n_trajectories = int(st.number_input('how many paths do you desire?  ... this will approximately augment the present...', format='%d', 
                            value = 3, step=1, min_value=1))
    
    #trace_depth = int(st.number_input('how many STEPS in each path?? (beware)', format='%d', 
                                        #min_value=1000, 
                                        #max_value= 1000000,
                                        #value = 10000, 
                                        #step=1000))
    
    travel_time = int(st.number_input('for how LONG will you travel? ... this will augment your future', format='%d', 
                                        min_value=10,
                                        max_value= 200,
                                        value = 100, 
                                        step=10))
    
    clouds = int(st.number_input('how FAR away do you want your paths to start from each other?', format='%d', 
                            value = 1, step=10, min_value=1))
    

#sub_cols = st.columns(3)

#with sub_cols[0]:

    #n_trajectories = int(st.number_input('How many paths do you desire?  ... this will approximately augment the present...', format='%d', 
                            #value = 3, step=1, min_value=1))

#with sub_cols[1]:
    #trace_depth = int(st.number_input('how many STEPS in each path??', format='%d', 
                                        #min_value=1000, 
                                        #value = 10000, 
                                        #step=1000))

#with sub_cols[2]:
    #clouds = int(st.number_input('HOW far away do you want your paths to start from each other?', format='%d', 
                           #value = 1, step=10, min_value=1))

#submitted = st.button("Create System")


if travel_time < 20:
    trace_depth = 100_000
else:
    trace_depth = 10_000


lorenz_sols = fetch_sols(initial_conds=initial_conds, 
                        lorenz_params=lorenz_params, 
                        n_trajectories=n_trajectories, 
                        travel_time = travel_time,
                        trace_depth=10_000,
                        clouds=clouds
                        )

st.divider()


figure_cols = st.columns([.2, .8])



with figure_cols[0]:

    perspective = st.selectbox('Perspective', 
                                options=perspective_options, 
                                index = 0)
    
    coloring_method = st.selectbox(label = 'how will you percieve the future?', 
                            options=coloring_options, 
                            index=0)
    
    which_path = [i+1 for i in range(n_trajectories)]
    
    path_num = st.number_input(label = 'Which Path will you take?'.upper(), 
                            min_value=1,
                            value=1,
                            max_value=n_trajectories,
                            key='path_num'
                            )
    




#with figure_cols[1]:

#figure_sub_cols = st.columns(3)

#with figure_sub_cols[1]:
    #path_num = st.number_input(label = 'Which Path will you take?'.upper(), 
                            #min_value=1,
                            #value=1,
                            #max_value=n_trajectories,
                            #key='path_num'
                            #)
                            
#if rho > 1:
#pt1 = (np.round(np.sqrt(beta * (rho - 1)), 3), np.round(np.sqrt(beta * (rho - 1)), 3), rho - 1)
#pt2 = (-np.round(np.sqrt(beta * (rho - 1)), 3), -np.round(np.sqrt(beta * (rho - 1)), 3), rho - 1)
#st.markdown(f"Your :red[Future] revoles around {pt1} AND {pt2}")



fig = create_figure(lorenz_sols, 
                    perspective, 
                    coloring_method, 
                    )


figure_cols[1].plotly_chart(fig, use_container_width=True)


