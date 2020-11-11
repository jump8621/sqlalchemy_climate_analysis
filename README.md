# sqlalchemy_climate_analysis
To begin, use Python and SQLAlchemy to do basic climate analysis and data exploration of your climate database. 


The start date was completed two ways in the Visual Studio(app.py): 

    *the 1st way compiles the Min, Max, and Avg temp for every single day from the start date to the last date of the data.
    *the 2nd way finds the Min, Max, and Avg temp for range of days from the date given(start).

![Precipitation](Precipitation.png)


'USC00519281' is the most active station, according to the data, but when gathering the last 12 months of temperature observation data from the station, the lastest date on record is **different** than the date being used previously for the precipitation data.

![TempObservation](TempObservation.png)

The average temperature for Hawaii during September, 10th and 20th in 2016 was 77 degrees Fahrenheit, with an error bar of 13 degrees.

    Min = 70 degrees
    Max  = 83 degrees


![Trip_Avg_Temp](Trip_Avg_Temp.png)

When using all the temperature data collected for Hawaii on those dates the average temp. is 76.3, only slightly lower than the 2016 data and within the error bar used for that graph.
    The average minimum temp. is 68 degrees and the average maximum temp. is 84 degrees as shown in the table below the graph.

![Predicted_Temperatures_for_trip](Predicted_Temperatures_for_Trip.png)

![table_mpl](table_mpl.png)
