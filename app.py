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
# TODO: fix 403 error with csv file upload
#uploaded_files_csv = st.file_uploader("Upload your CSV file(s)", type=['csv'],accept_multiple_files=True)
#if uploaded_files_csv is not None:
#    st.write("success")
st.button("Use Example Data")