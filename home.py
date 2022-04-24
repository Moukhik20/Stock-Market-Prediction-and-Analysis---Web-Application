import streamlit as st
from multiapp import MultiApp
from apps import pred, companyinfo, analysis

home=MultiApp()

home.add_app("Stock Price Prediction", pred.app)
home.add_app("Company Information", companyinfo.app)
home.add_app("Technical Analysis", analysis.app)
home.run()