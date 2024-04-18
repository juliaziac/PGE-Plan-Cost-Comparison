import streamlit as st
import utils.processing_functions

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
uploaded_files_csv = st.file_uploader("Upload your CSV file(s)", type=['csv'],accept_multiple_files=True)
if uploaded_files_csv is not None:
    processed_files = {} # dictionary entries of the form {name:df}
    for i in range(len(uploaded_files_csv)):
        df, name = utils.processing_functions.process_csv(uploaded_files_csv[i])
        processed_files[name] = df
    processed_df = utils.processing_functions.combine_and_process(processed_files)
    st.table(processed_df)

#st.button("Use Example Data")