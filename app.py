import streamlit as st
import utils.processing_functions
import os
import pandas as pd ###

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

st.header("Upload PGE billing CSVs")
files_ready = False
uploaded_files_csv = st.file_uploader("Upload your CSV file(s):", type=['csv'],accept_multiple_files=True)
if len(uploaded_files_csv) == 0:
    #pass
    st.write("Or, use example data:")
    if st.button("Use Example Data"):
        ###st.dataframe(pd.read_csv("./data/pge_electric_billing_data_4323839271_2021-04-01_to_2024-02-29.csv", header=4))
        source_dir = os.path.dirname(__file__)
        st.write(source_dir)
        for file in os.listdir("utils/example_data"):
            filename = os.path.join(source_dir, file)
            file_open = open(filename, "r")
            st.write(file_open.readline([0]))
            file_open.close()
            #st.write(__file__)
            #st.dataframe(pd.read_csv(__file__, on_bad_lines='skip'))
            st.dataframe(pd.read_csv(os.path.join(source_dir, file)))
            #st.write(os.path.abspath(file))
            #st.dataframe(pd.read_csv(os.path.join(os.getcwd(), "data", file), header=4))
            #st.dataframe(pd.read_csv("/Users/juju/Documents/Programming/Python/PGE_avg/data/pge_electric_billing_data_4323839271_2021-04-01_to_2024-02-29.csv", header=4))
        #st.write(os.getcwd())

        #processed_files = {} # dictionary entries of the form {name:df}
        #for file in os.listdir("utils/example_data"):
        #    df, name = utils.processing_functions.process_csv(file)
        #    processed_files[name] = df
        #processed_df = utils.processing_functions.combine_and_process(processed_files)
        #files_ready = True
        #st.dataframe(processed_df)

elif len(uploaded_files_csv) == 1:
    st.write(":red[Upload **two** files: one for gas and one for electric.]")
elif len(uploaded_files_csv) == 2:
    processed_files = {} # dictionary entries of the form {name:df}
    for i in range(len(uploaded_files_csv)):
        df, name = utils.processing_functions.process_csv(uploaded_files_csv[i])
        processed_files[name] = df
    processed_df = utils.processing_functions.combine_and_process(processed_files)
    files_ready = True

if files_ready == True:
    st.header("Best plan given historical data")
    total = utils.processing_functions.total_analysis(processed_df)
    best_plan = total.iloc[total['cheaper_by_$'].idxmax()]
    st.write(f"The best plan is the **:green[{best_plan['cheaper_plan']} plan]** and the time to start is {best_plan['start_month']}, \
        which would be cheaper by ${best_plan['cheaper_by_$'].round(2)}.")
    with st.expander("See other start months optimal plan choices"):
        st.dataframe(total)
else:
    pass