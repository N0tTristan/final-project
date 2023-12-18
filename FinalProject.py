import csv
import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import folium
from streamlit_folium import folium_static


def load_data(filename):
    dtypeDict = {'facility_zip_code': str,
                 'equity_program_designation': str,
                 'longitude': float,
                 'latitude': float}  # making a dictionary so I can guarantee I have the correct data types
    data = pd.read_csv(filename, dtype = dtypeDict)
    pd.set_option('display.width', 100)  # put this in so i can make sure the data is displaying properly
    return data


def create_bar_plot(data, column_name):
    fig, ax = plt.subplots(figsize=(10, 6))
    counts = data[column_name].value_counts()  # counts the values of each type of data
    counts.plot(kind="bar", color="darkgreen", ax=ax)  # plots and sets colors
    ax.set_title(f"Bar Plot of {column_name}")  # title
    ax.set_xlabel(column_name)  # x axis label
    ax.set_ylabel("Count of Each " + column_name)  # y axis label
    st.pyplot(fig)


def find_a_dispensary(data, zipCode, storeType="Retail"):
    data['Zip Code'] = data['Zip Code'].astype(str)  # makes sure data is type I want it as
    result = data[(data["License Type"] == storeType) & (data["Zip Code"] == zipCode)]  # query user input

    if len(result) == 0:
        existingRecords = False  # if no records, it will say so
    else:
        existingRecords = True  # if records, it will say so

    return result, existingRecords


def main():
    # Adding page configuration
    st.set_page_config(page_title='Final Project', page_icon='random', layout="centered", initial_sidebar_state="auto")
    df_full = load_data("Cannabis_Registry.csv")  # load in main dataset

    # dictionary to change column names
    columnRename = {'id_name_first': "First Name",
                    'id_name_last': "Last Name",
                    'id_full_name': "Full Name",
                    'app_license_category': "License Type",
                    'app_business_name': 'Business Name',
                    'app_license_status': "License Status",
                    'equity_program_designation': 'Equity Program?',
                    'facility_address': "Facility Address",
                    "facility_zip_code": "Zip Code",
                    "longitude": "longitude",
                    "latitude": "latitude"}

    df_full = df_full.rename(columns=columnRename)  # actually changes column names that are defined above
    df_cleaned = df_full.dropna()  # gets rid of null values

    st.sidebar.write("Would you like to rate this information?")  # adds sidebar for survey if they want to use it
    st.sidebar.slider("Rate us from 1 - 10:", min_value = 0, max_value = 10)  # rate using sidebar
    st.sidebar.radio("How did you hear about us?", ["Social Media", "Advertisement", "Word of Mouth"])
    st.sidebar.text_input("Do you have any additional comments?") # asks user for comments
    sideButtonClick = st.sidebar.button("Submit")  # when user clicks button, it will thank them for their feedback

    if sideButtonClick:
        st.sidebar.write("Thank you for the feedback!")

    # using tabs to display different pages
    tab1, tab2, tab3, tab4, = st.tabs(["Home",
                                      "License Information",
                                      "The Equity Program",
                                      "Quiz"])

    with tab1:
        st.image("cannabisMain.png")  # my custom made banner!
        st.warning("This information is relevant to the State of Massachussetts as of December 2023.")  # found this on https://cheat-sheet.streamlit.app/
        st.snow()  # founds this on https://cheat-sheet.streamlit.app/
        st.toast("Happy Holidays from me, Ashlyn!")  # found this on https://cheat-sheet.streamlit.app/

        htmlTitle = '''
        <h1 style="font-family: Calibri,serif; color: darkgreen;">Cannabis Dispensaries in Boston </h1>
        '''
        st.markdown(htmlTitle, unsafe_allow_html = True)
        # st.title("Cannabis Dispensaries in Boston")
        st.image("cannabist.png")
        st.write(
            "Welcome to an informational website on cannabis dispensaries in Boston! In this website we will"
            " explain how to get a license, where the dispensaries are, and more!")

        # next two lines is written in HTML/CSS elements and then imported into the project
        htmlActiveDispenaries = '''<h3 style="font-style: italic; color: darkslategrey;">Active Boston Dispensaries and Their Locations</h3>'''
        st.markdown(htmlActiveDispenaries, unsafe_allow_html = True)

        active_columns = ["Business Name", "License Type", "Zip Code", "License Status"]  # list of columns I want to show
        active = df_full[active_columns]  # makes a new dataFrame with only these columns
        df3 = active.query("`License Status` == 'Active'")  # query so it is only active licenses; troubleshooted online
        active_sorted = df3.sort_values(by="Business Name")  # sorts based on business name

        st.dataframe(active_sorted)  # prints out list of them

        mapDataFrameColumns = ["Business Name", "longitude", "latitude"]  # picking new group of columns
        mapData = df_cleaned[mapDataFrameColumns]  # only the data i want to display

        centerOfMap = [df_full['latitude'].mean(), df_full['longitude'].mean()]  # found on https://realpython.com/python-folium-web-maps-from-data/, troubleshooted with ChaGPT
        my_map = folium.Map(location=centerOfMap, zoom_start=11)

        for index, row in mapData.iterrows():  # Found on https://realpython.com/python-folium-web-maps-from-data/
            folium.Marker(
                location=[row["latitude"], row["longitude"]],  # adds data to the map markers
                popup=row["Business Name"],  # when you click on it, says the business name
                icon = folium.Icon(color='green')
            ).add_to(my_map)  # adds this as a point on the map

        # another instance of using HTML/CSS
        htmlLocations = '''<h3 style="font-style: italic; color: darkslategrey;">Locations of Dispenaries</h3>'''
        st.markdown(htmlLocations, unsafe_allow_html = True)

        folium_static(my_map)  # publishes the map

        st.write("As you can see, there are very few active dispensaries in Boston however many that used to exist!")
        create_bar_plot(df_full, "License Status")  # calls function to build bar graph

    with tab2:
        st.image("cannabisMain.png")
        licenseHTML = '''
        <h1 style="font-family: Calibri,serif; color: darkgreen;">Acquiring a License and Types of Licenses</h1>
        '''
        st.markdown(licenseHTML, unsafe_allow_html=True)
        st.image("main.png")
        st.header("What is the process to start your own business?")

        st.write("Fun fact: You cannot seek approval of a cannabis business if you are an employee or immediate family "
                " member to an employee of the city of Boston, Zoning Board of Appeal, Boston Licensing Board, Boston "
                "Public Health Commission, and Boston Zoning Commission.")

        st.subheader("1. Complete an online application, ")
        st.write("Here you will need to provide details concerning plans for security, "
                 " interest, type of license, floor plan, articles of organization, legal "
                 " right to occupy the premise, etc.")

        st.subheader("2. Apply for a conditional use permit,")
        st.write("This creates an exception to current land use rules. Typically zoning "
                 " ordinances do not allow these types of businesses. They can apply through"
                 " Boston’s Inspectional Services Department.")

        st.subheader("3. Go through the appeal process.")
        st.write("There are several reasons why someone might be denied. In this case, the "
                 " next step is to file an appeal with the Zoning Board of Appeal.")

        st.subheader("4. Create a host community agreement.")
        st.write("The business must be approved by the Boston Cannabis Board. They will"
                 " then draft a Host Community Agreement where it incorporates...")
        st.text("\t\t1.Any standard conditions placed by the BCB on a license")
        st.text("\t\t2.Any grant specific conditions of the license or review and input.")

        st.subheader("5. Go through the state process.")
        st.write("Once Zoning Board of Appeal Approves conditional use permit, the next step is"
                 " going through a state application process with Cannabis Control Commission."
                 " Once the Cannabis Control Commission approves the establishment, it will then"
                 " notify the city of Boston.")

        st.subheader("6. After approval, register as a business.")
        st.write("The final step is to file with the Office of the "
                 " City Cler as a business with a $65 business registration fee.")

        st.header("Citation:")
        st.write("Establishing a cannabis business in Boston. (2018, April 25). Boston.gov. https://www.boston.gov/establishing-cannabis-business-boston")

        st.header("Types of Licenses")
        create_bar_plot(df_full, "License Type")

        st.header("Want to look at the dispensaries in your area?")
        storeSelect= st.selectbox("What type of store are you looking for?",
                                  ["Retail", "Co-Located", "Operator",
                                   "Courier", "Manufact", "Cultivate", "Medical",
                                   "TestLab", "Transport"])

        active['Zip Code'] = active['Zip Code'].astype(str)  # makes sure data is a string
        zipcode = st.text_input("What is your Zip Code?")  # asks user for a zip code
        dispensary, existingRecords = find_a_dispensary(df3, zipcode, storeSelect)
        if existingRecords:  # if there are records it will print them
            st.write("Here is a list of dispensaries in your area!")
            st.dataframe(dispensary)
        else:  # if there is not records it will not print them
            st.write("There are no stores that match this criteria!")

    with tab3:
        st.image("cannabisMain.png")
        st.header("The Social Equity Program")

        htmlOne = '''
        <h5 style="font-style: italic; color: green;">Quote from the Cannabis Control Commission</h5>
        '''
        st.markdown(htmlOne, unsafe_allow_html = True) # inserts html

        st.write("'' The Social Equity Program (SEP) is a free, statewide technical assistance and training "
                 "program that creates sustainable pathways into the cannabis industry for individuals most"
                 " impacted by the War on Drugs including disproportionate arrest and incarceration as the "
                 "result of marijuana prohibition. ''")

        # citation for information
        st.write("Equity Programs - Cannabis Control Commission Massachusetts. (2023, April 24). Cannabis Control Commission Massachusetts. https://masscannabiscontrol.com/equity/")

        st.video("https://www.youtube.com/watch?v=J-uwzF0TBW0")  # added a video

        equity_columns = ["Business Name", "Equity Program?"]
        equity = df_cleaned[equity_columns]
        equityQuery = equity.query("`Equity Program?` == 'Y'")  # if there is a Y
        sortedEquity = equityQuery.sort_values(by="Business Name")  # sorts by business name
        yesEQ = len(equityQuery)
        st.write(f"There are {yesEQ} businesses that are part of this program!")
        st.dataframe(sortedEquity)

        noEQ = len(equity.query("`Equity Program?` == 'N'"))  # counts if not

        st.write("Here is the makeup of how each business is classified in terms of the Social Equity status.")
        st.header("Social Equity Program Status")

        # builds a pie chart
        fig1, ax1 = plt.subplots()
        values = [noEQ, yesEQ]
        labels = ['No', 'Yes']
        ax1.pie(values, labels=labels, colors = ["green", "lightgreen"])
        st.pyplot(fig1)

    with tab4:
        st.image("cannabis.png")

        quizHTML = '''
        <h1 style="font-family: Calibri,serif; color: darkgreen;">Quiz Time!</h1>
        '''
        # HTML
        name = st.text_input("What is your first name?")
        st.markdown(quizHTML, unsafe_allow_html=True)

        # Display the multiselect question
        question1 = st.multiselect("Select proper steps for a Boston dispensary application",
                                   ["Complete online application",
                                    "Verify legal status",
                                    "Apply for a conditional use permit",
                                    "Go through appeal process",
                                    "Create host community agreement",
                                    "Show proof of residency",
                                    "Go through state process",
                                    "Register as a business"])  # uses a multiselect

        # Display the selected steps
        st.write("Selected Steps:", question1)

        state = st.text_input("What state is this data for?")  # question 2

        employee = st.radio("T/F : You can start a cannabis business with"
                            " your father who works for the city of Boston:",
                            ["True", "False"])  # Quesiton 3

        equityQuant = st.slider("How many businesses are part of the Social Equity Program?", 0,100)  # Quesiton 4

        age = st.number_input("What is the minimum age to enter a dispensary?")  # Question 4

        quizButton = st.button("Click here when done!")

        if quizButton:
            correctSteps = ["Complete online application",
                            "Apply for a conditional use permit",
                            "Go through appeal process",
                            "Create host community agreement",
                            "Go through state process",
                            "Register as a business"]
            score = []
            count = 0
            for step in correctSteps:
                if step in question1:
                    score.append(1)  # checks questions to correct answers above

            if correctSteps == question1:
                count += 1

            if state.upper() == "MA":
                score.append(1)
                count += 1
            elif state.title() == "Massachussetts":  # covers different variations of the right answer
                st.write("Correct!")
                score.append(1)
                count +=1

            if employee == "False":
                score.append(1)
                count += 1

            if equityQuant == 33:
                score.append(1)
                count += 1

            if age == 21:
                score.append(1)
                count += 1

            st.write(f"You have answered {count} correctly out of 5")

            byTenScore = (s * 10 for s in score)  # uses list comprehension to count rows
            totalScore = 0
            for s in byTenScore:
                totalScore+=s  # adds together

            finalScore = totalScore

            st.write("Your final score ouf of 100 is:", finalScore)

            # really excited coding this part; uses past player data and compares it to current one

            newEntry = [name, finalScore]  # adds a list for a new line of data

            playerHistory = "player_history.csv"  # builds a new csv file

            with open(playerHistory, mode = 'a') as file:
                writer = csv.writer(file)
                writer.writerow(newEntry)  # writes new entry to read

            playerData = load_data(playerHistory)  # calls function above
            st.write("Here is past players data! Do you stack up to them?")
            st.line_chart(playerData.set_index(playerData.columns[0]))  # builds a line chart with it

        st.camera_input("Smile for Instagram! We want to showcase those who are passionate about making a difference!")
        st.title("Like the photo? Submit it here!")
        pictureButton = st.button("Submit Picture")  # nothing special, just thought it would be cute to incorporate

        if pictureButton:
            st.write("Thank you for submitting a picture!")


if __name__ == "__main__":
    main()
