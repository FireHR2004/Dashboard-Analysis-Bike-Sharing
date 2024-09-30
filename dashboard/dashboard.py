import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

data = pd.read_csv('./dashboard/main_data.csv')

season_labels = {1: 'Spring', 2: 'Summer', 3: 'Fall', 4: 'Winter'}
data['season_x'] = data['season_x'].map(season_labels)

st.set_page_config(page_title="Bike Sharing Data Dashboard", layout="wide")

st.markdown("<h1 style='text-align: center; color: darkblue;'>🚴‍♂️ Bike Sharing Data Analysis Dashboard</h1>", unsafe_allow_html=True)
st.markdown("""
<div style='text-align: center'>
Explore the trends in bike sharing data with this interactive dashboard. Analyze key factors influencing bike rental demand and
fluctuations of casual and registered users across different seasons. Use the filters to customize your view and gain valuable insights!
</div>
""", unsafe_allow_html=True)

with st.container():
    col1, col2 = st.columns([1, 3])

    with col1:
        st.sidebar.title("Customize Your Analysis")
        analysis_type = st.sidebar.selectbox("Choose a Business Question:", 
                                             ("Factors Influencing Bike Rental Demand", 
                                              "Fluctuation of Casual and Registered Users Across Seasons"))

        selected_season = st.sidebar.multiselect("Select Season(s) to Analyze:", 
                                                 options=data['season_x'].unique(), 
                                                 default=data['season_x'].unique())

        filtered_data = data[data['season_x'].isin(selected_season)]

    with col2:
        st.markdown("""
        ### Insights:
        - **Business Question 1**: What are the main factors influencing bike rental demand?
        - **Business Question 2**: How do casual and registered users fluctuate across different seasons?
        Select your preferences using the sidebar filters to get started with the analysis.
        """)

# Create layout for the main analysis results
with st.container():
    if analysis_type == "Factors Influencing Bike Rental Demand":
        st.markdown("### Factors Influencing Bike Rental Demand")

        selected_factor = st.sidebar.selectbox("Choose a Factor to Analyze:", 
                                               ['temp_y', 'hum_y', 'windspeed_y'])

        col3, col4 = st.columns(2)

        with col3:

            st.write(f"#### Correlation Between {selected_factor} and Total Rentals")
            corr_matrix = filtered_data[['temp_y', 'hum_y', 'windspeed_y', 'cnt_y']].corr()

            # Display the correlation heatmap
            plt.figure(figsize=(6, 4))
            sns.heatmap(corr_matrix, annot=True, cmap='coolwarm', linewidths=0.5)
            plt.title("Correlation Matrix")
            st.pyplot(plt)

        with col4:
            st.write(f"#### Relationship Between {selected_factor} and Total Rentals")
            plt.figure(figsize=(8, 5))
            sns.scatterplot(x=filtered_data[selected_factor], y=filtered_data['cnt_y'], hue=filtered_data['season_x'], palette='deep')
            plt.title(f"{selected_factor} vs Total Rentals by Season")
            plt.xlabel(selected_factor)
            plt.ylabel("Total Rentals")
            st.pyplot(plt)

        st.write(f"### Average Rentals by {selected_factor} Across Seasons")
        avg_rentals = filtered_data.groupby('season_x')[selected_factor].mean().reset_index()
        
        plt.figure(figsize=(8, 4))
        sns.barplot(x='season_x', y=selected_factor, data=avg_rentals, palette='Blues_d')
        plt.title(f"Average {selected_factor} Across Seasons")
        plt.xlabel("Season")
        plt.ylabel(f"Average {selected_factor}")
        st.pyplot(plt)

    elif analysis_type == "Fluctuation of Casual and Registered Users Across Seasons":
        st.markdown("### Fluctuation of Casual vs Registered Users Across Seasons")

        season_group = filtered_data.groupby('season_x')[['casual_y', 'registered_y']].mean().reset_index()

        season_group_melted = pd.melt(season_group, id_vars='season_x', value_vars=['casual_y', 'registered_y'], 
                                      var_name='User Type', value_name='Average Rentals')

        col5, col6 = st.columns([3, 1])

        with col5:
            st.write(f"#### Average Bike Rentals for Casual and Registered Users Across Seasons")
            plt.figure(figsize=(10, 6))
            sns.barplot(x='season_x', y='Average Rentals', hue='User Type', data=season_group_melted)
            plt.title('Casual vs Registered Bike Rentals Across Seasons')
            plt.xlabel('Season')
            plt.ylabel('Average Rentals')
            plt.legend(title='User Type', loc='upper left')
            st.pyplot(plt)

        with col6:
            st.write("""
            - **Casual Users**: Generally prefer biking in summer and fall.
            - **Registered Users**: More consistent across all seasons, with a slight drop in winter.
            - Use the chart to see how the bike usage changes seasonally between user types.
            """)

        st.write("### Comparison of Total Casual and Registered Users by Season")
        total_users = filtered_data.groupby('season_x')[['casual_y', 'registered_y']].sum().reset_index()

        plt.figure(figsize=(8, 4))
        sns.barplot(x='season_x', y='casual_y', data=total_users, label='Casual Users', color='skyblue')
        sns.barplot(x='season_x', y='registered_y', data=total_users, label='Registered Users', color='lightcoral')
        plt.title("Total Users by Season")
        plt.xlabel("Season")
        plt.ylabel("Total Rentals")
        plt.legend()
        st.pyplot(plt)

st.write("### Sample of the Filtered Dataset:")
st.dataframe(filtered_data.head(10))