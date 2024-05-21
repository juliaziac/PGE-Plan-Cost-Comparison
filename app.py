import streamlit as st
import utils.processing_functions
import os
import numpy as np
import pandas as pd ###
import datetime
from bokeh.plotting import figure
from bokeh.models import HoverTool
from bokeh.models import ColumnDataSource

# Background text
st.title("PGE's \"Budget Billing\": should you switch?")
st.markdown("""
PGE has a new program, \"Budget Billing\":

\"The Budget Billing program averages your energy costs over the previous 12 months to determine your monthly payment amount. If your actual energy costs significantly change, we adjust your monthly Budget Billing payment amount once every four months.\"

Questions for PGE:
+ What counts as \"significant\" change?

Questions for analysis:
+ Historically, would you have benefitted from this?
+ If so, what is the optimal month to start (given the 4-month update cycle)?
""")

# File upload
st.header("Upload PGE billing CSVs")
files_ready = False
uploaded_files_csv = st.file_uploader("Upload your CSV file(s):", type=['csv'],accept_multiple_files=True)
if len(uploaded_files_csv) == 0:
    #pass
    st.write("Or, use example data:")
    if st.button("Use Example Data"):
        source_dir = os.path.dirname(__file__)
        #st.dataframe(pd.read_csv(os.path.join(source_dir, "utils", "example_data", "pge_electric_billing_data_XXXXX_2021-04-01_to_2024-02-29.csv"), header=4))
        filenames = [os.path.join(source_dir, "utils", "example_data", "pge_electric_billing_data_XXXXX_2021-04-01_to_2024-02-29.csv"),
                    os.path.join(source_dir, "utils", "example_data", "pge_gas_billing_data_XXXXX_2021-04-02_to_2024-03-01.csv")
                    ]
        processed_files = {} # dictionary entries of the form {name:df}
        for file in filenames:
            df, name = utils.processing_functions.process_csv(file, string_input=True)
            processed_files[name] = df
        processed_df = utils.processing_functions.combine_and_process(processed_files)
        files_ready = True
        st.dataframe(processed_df)

elif len(uploaded_files_csv) == 1:
    st.write(":red[Upload **two** files: one for gas and one for electric.]")
elif len(uploaded_files_csv) == 2:
    processed_files = {} # dictionary entries of the form {name:df}
    for i in range(len(uploaded_files_csv)):
        df, name = utils.processing_functions.process_csv(uploaded_files_csv[i])
        processed_files[name] = df
    processed_df = utils.processing_functions.combine_and_process(processed_files)
    files_ready = True

# Plan summary and graph
if files_ready == True:
    st.header("Best plan given historical data")
    total = utils.processing_functions.total_analysis(processed_df)
    best_plan = total.iloc[total['cheaper_by_$'].idxmax()]
    st.write(f"The best plan is the **:green[{best_plan['cheaper_plan']} plan]** and the time to start is {best_plan['start_month']}, \
        which would be cheaper by **:green[${best_plan['cheaper_by_$'].round(2)}]**.")
    with st.expander("See other start months optimal plan choices"):
        st.dataframe(total)

###else:###
###    pass###


    st.header("Interactive graph")
    processed_df_cds = ColumnDataSource(processed_df)
    start_month_index = np.isnan(processed_df['1Y_ROLLING_AVG']).argmin(axis=0)
    x = processed_df['MONTH'].dt.to_timestamp()  
    x_bar_width = datetime.timedelta(days=20)
    y_bar = processed_df['TOTAL_COST'] 
    #y_seg = total['1Y_ROLLING_AVG']
    tooltips = [
            ('Month', '@MONTH{%b %Y}'),
            ('Actual Cost', '@TOTAL_COST{$0.00}')
            ]
    formatters={'@MONTH': 'datetime'}

    fig = figure(###plot_height=400,
             ###plot_width=1000,
             x_axis_label='Month',
             x_axis_type='datetime',
             y_axis_label='Total Cost ($)',
             y_axis_type='linear',
             title='Monthly Total PGE Cost',
             tools=['xpan', 'tap', 'hover', 'reset', 'save'],
             tooltips=tooltips)
    fig.vbar(x='MONTH', bottom=0, top='TOTAL_COST', width=x_bar_width, source=processed_df_cds, legend_label='Actual Monthy Cost')

    fig.add_tools(HoverTool(tooltips=tooltips, formatters=formatters))
    for i in range(start_month_index, len(processed_df.index), 4):
        fig.segment(x0=x[i]-x_bar_width/2, y0=y_bar[i], x1=x[i+3]+x_bar_width/2, y1=y_bar[i],\
                    color='red', width=5, legend_label='Budget Billing Cost')
    fig.legend.location = 'top_left'
    fig.toolbar.logo = None

    st.bokeh_chart(fig, use_container_width=True)


else:
    pass

