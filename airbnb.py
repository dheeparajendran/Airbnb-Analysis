import streamlit as st
from streamlit_option_menu import option_menu
import plotly_express as px
import pandas as pd
import os
import warnings
import plotly.figure_factory as ff

warnings.filterwarnings('ignore')

# Setting Streamlit App
st.set_page_config(page_title = "AirBnb - Analysis",
                   page_icon = ":bar_chart:",
                   layout = "wide")
st.title(":bar_chart: AirBnb - Analysis")
st.markdown("<style>div.block-container{padding-top:1rem;}</style>", unsafe_allow_html = True)

# With st.headbar:
SELECT = option_menu(menu_title = None,
                     options = ["HOME", "EXPLORE DATA"],
                     icons = ["house", "bar-chart"],
                     default_index = 1,
                     orientation = "horizontal",
                     styles = {"container" : {"padding":"0!important",
                                              "background-color":"blue",
                                              "size":"cover",
                                              "width":"100"},
                                "icon" : {"color":"white", 
                                          "font-size":"25px"},
                                "nav-link" : {"font-size":"25px",
                                              "color":"white",
                                              "text-align":"center",
                                              "margin":"0px",
                                              "--hover-color":"darkblue"},
                                "nav-link-selected" : {"background-color":"red"}})

# Home Tab
if SELECT == "HOME":
    st.header('AirBnb - Analysis :')
    st.subheader('Airbnb is an American San Francisco-based company operating an online marketplace for short- and long-term homestays and experiences. The company acts as a broker and charges a commission from each booking. The company was founded in 2008 by Brian Chesky, Nathan Blecharczyk, and Joe Gebbia. Airbnb is a shortened version of its original name, AirBedandBreakfast.com. The company is credited with revolutionizing the tourism industry, while also having been the subject of intense criticism by residents of tourism hotspot cities like Barcelona and Venice for enabling an unaffordable increase in home rents, and for a lack of regulation.')
    st.subheader('Skills Used : Python scripting, Data Preprocessing, Visualization, EDA, Streamlit, MongoDb, PowerBI/Tableau')
    st.subheader('Domain : Travel Industry, Property Management and Tourism')

# Explore Data Tab
if SELECT == "EXPLORE DATA":
    fl = st.file_uploader(":file_folder: Upload a file", type = (["csv","txt","xlsx","xls"]))
    if fl is not None:
        filename = fl.name
        st.write(filename)
        df = pd.read_csv(filename, encoding = "ISO-8859-1")
    else:
        # os.chdir(r"E:\GUVI_Files\Project_04") [If you have csv file in differnt path, then use this code]
        df = pd.read_csv("Airbnb NYC 2019.csv", encoding="ISO-8859-1")

    # Create Sidebar
    st.sidebar.header("Filter : ")

    # Create for neighbourhood_group
    neighbourhood_group = st.sidebar.multiselect("Pick your Neighbourhood Group", df["neighbourhood_group"].unique())
    if not neighbourhood_group:
        df2 = df.copy()
    else:
        df2 = df[df["neighbourhood_group"].isin(neighbourhood_group)]

    # Create for neighbourhood
    neighbourhood = st.sidebar.multiselect("Pick your Neighbourhood", df2["neighbourhood"].unique())
    if not neighbourhood:
        df3 = df2.copy()
    else:
        df3 = df2[df2["neighbourhood"].isin(neighbourhood)]

    # Filter the Data based on neighbourhood_group, neighbourhood
    if not neighbourhood_group and not neighbourhood:
     filtered_df = df
    elif not neighbourhood:
        filtered_df = df[df["neighbourhood_group"].isin(neighbourhood_group)]
    elif not neighbourhood_group:
        filtered_df = df[df["neighbourhood"].isin(neighbourhood)]
    elif neighbourhood:
        filtered_df = df3[df["neighbourhood"].isin(neighbourhood)]
    elif neighbourhood_group:
        filtered_df = df3[df["neighbourhood_group"].isin(neighbourhood_group)]
    elif neighbourhood_group and neighbourhood:
        filtered_df = df3[df["neighbourhood_group"].isin(neighbourhood_group) & df3["neighbourhood"].isin(neighbourhood)]
    else:
        filtered_df = df3[df3["neighbourhood_group"].isin(neighbourhood_group) & df3["neighbourhood"].isin(neighbourhood)]
    room_type_df = filtered_df.groupby(by=["room_type"], as_index=False)["price"].sum()

    # Creating BarChart & PieChart by using Plotly
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Room Type ViewData")
        fig = px.bar(room_type_df, x="room_type", y="price", text=['$ {:,.2f}'.format(x) for x in room_type_df["price"]],template="seaborn")
        st.plotly_chart(fig, use_container_width=True, height=200)
    with col2:
        st.subheader("Neighbourhood Group ViewData")
        fig = px.pie(filtered_df, values="price", names="neighbourhood_group", hole=0.5)
        fig.update_traces(text=filtered_df["neighbourhood_group"], textposition="outside")
        st.plotly_chart(fig, use_container_width=True)

    cl1, cl2 = st.columns((2))
    with cl1:
        with st.expander("Room Type Wise Price"):
            st.write(room_type_df.style.background_gradient(cmap="Blues"))
            csv = room_type_df.to_csv(index=False).encode('utf-8')
            st.download_button("Download Data", data=csv, file_name="room_type.csv", mime="text/csv")
    with cl2:
        with st.expander("Neighbourhood Group Wise Price"):
            neighbourhood_group = filtered_df.groupby(by="neighbourhood_group", as_index=False)["price"].sum()
            st.write(neighbourhood_group.style.background_gradient(cmap="Oranges"))
            csv = neighbourhood_group.to_csv(index=False).encode('utf-8')
            st.download_button("Download Data", data=csv, file_name="neighbourhood_group.csv", mime="text/csv")
    
    # Create a scatter plot
    data1 = px.scatter(filtered_df, x="neighbourhood_group", y="neighbourhood", color="room_type")
    data1['layout'].update(title="Room type in the Neighbourhood and Neighbourhood Group wise data using Scatter Plot.",
                            titlefont=dict(size=20), 
                            xaxis=dict(title="Neighbourhood Group", titlefont=dict(size=20)),
                            yaxis=dict(title="Neighbourhood", titlefont=dict(size=20)))
    st.plotly_chart(data1, use_container_width=True)

    with st.expander("Detailed Room Availability and Price View Data in the Neighbourhood"):
        st.write(filtered_df.iloc[:500, 1:20:2].style.background_gradient(cmap="Oranges"))
        # Download orginal DataSet
        csv = df.to_csv(index=False).encode('utf-8')
        st.download_button('Download Data', data=csv, file_name="Data.csv", mime="text/csv")

    st.subheader(":point_right: Neighbourhood group wise Room type and Minimum stay nights")
    with st.expander("Summary Table"):
        df_sample = df[0:5][["neighbourhood_group", "neighbourhood", "reviews_per_month", "room_type", "price", "minimum_nights", "host_name"]]
        fig = ff.create_table(df_sample, colorscale="Cividis")
        st.plotly_chart(fig, use_container_width=True)

    # map function for room_type
    # If your DataFrame has columns 'Latitude' and 'Longitude':
    st.subheader("AirBnb Analysis in Map view")
    df = df.rename(columns={"Latitude": "lat", "Longitude": "lon"})
    st.map(df)