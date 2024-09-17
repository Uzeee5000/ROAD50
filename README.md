# ROAD50
#### Video Demo:  <https://www.youtube.com/watch?v=DSQkJdyYo8M>
### Dataset Source: <https://www.gov.uk/government/collections/road-accidents-and-safety-statistics>
#### Description: This is an accident prevention website 'ROAD50'. This website is aimed to create awareness and give confidence to new and learning drivers using data statistics provided by the government and precautionary measures. This website uses simple layout and it focuses more on providing the insights to the statisitcs and the visualization for the user to fulfill the purpose. This webiste is built on the data provided by The Great Britain Government it contains accident statistics from the year 2017 to 2020 and it contains data for the UK, Northern Ireland and Wales. The dataset contains four tables which contain information about accident, casualties, vehicles and user information, respectively. Backend of the website is in Flask, Python, and SQL it uses libraries like Pandas, gmplot and sqlite3, while the frontend is in JavaScript, HTML and CSS.
#### This website uses some of the ideas from CS50's final assignment i.e., CS50 finance. This website prompts the user for creating an account when first visiting and after login it displays home page. The website contains 4 pages after login Home, Vehicles, Geospatial Analysis and Precautions. Home page uses a SQL query to extract the accidents statistics and plots using JavaScript plotly library to display accidents frequency. Vehicles page prompts user for a specific vehicle type and then on submission it displays accidents frequency for the selected vehicle type. Geospatial Analysis page prompts user for county name and city name, using that input in the backend SQL query extracts the data relevant to that geographic area and uses gmplot library to plot the data on google map by generating a HTML page and saving it in static folder and then displays it in a new html page with a heading on top. Fourth page of this website i.e. Precautions is a html page that displays general precautionary measures and general guidelines from the government related to safe driving practicies and following traffic laws.
#### Server-side of this application is written in python, Flask framework and it uses SQL query to extract data and then converts it into pandas DataFrame which makes it easier to work with the data. It uses filesystem to configure session using Flask framework. For every page there is a function which uses 'GET' and 'POST' requests to deal with different types of requests. This website uses some of the inbuilt python functions like value_counts, it makes a lot of use of list comprehensions. It imports some functions like get_county_center, vehicle_dict and get_stats from a separate file called helpers. It makes code in the main file recursive and uses the functions efficiently.
#### This application consists of ten html files in the templates folder that are displayed by the different application routes accordingly. It also generates a html page for every user using gmplot when they want to visualize the accident locations on Google Maps using gmplot library and this page is stored in the static folder. Apology, login and register pages are same as in the CS50 finance. The home page uses plotly to plot accidents frequency per day and per hour for the year of 2020. The Vehicle page uses two html pages named 'vehicles.html' and 'vplot.html' to handle the GET and POST requests respectively. It displays statistics for the specific vehicle type by using a sql query to extract data and then using pandas library to manipulate the data into desired data type and eventually fed to the html page to be plotted.
#### Geospatial Analysis page uses two pages named 'mapping.html' and 'map.html' for GET and POST requests respectively. First page is used to prompt the user for input and then second page is used to render the Google Maps that includes the accident locations which were extracted as per the user input. The html page generated using the gmplot is named same as the user_id to maintain seprate html files for users. Precautions page uses a simple 'history.html' page that displays some predefined precautions and rules by the government of The Great Britian.
#### This application uses the same 'apology.html' page from CS50 finance to handle the error from users and give feedback. It also uses the 'styles.css' to handle the styling same as C50 finance. Register page is also same as that in CS50 finance.
#### Driving can be hectic and mentally straining. Main goal of creating this website is to encourage users to have a safe driving approach and use this website to steer away from the accident prone routes, times, days and drive on the roads with much lesser probability of getting into an accident. This website enables the user to have a probabilistic approach towards safe driving and accident prevention. This gives confidence to the new driver or the learning driver who might not be confident enough to take on the The Great Britian roads which can be a bit dangerous with the constant adverse weather conditions throughout the year.
#### Additional features can be added like accident frequency relevant to accident severity and then using clustering to highlight the dangerous roads and turns. I have experimented with this in another repository available on my profile. You are more than welcome to add more features like drop down menus allowing users to focus on accidents with high severity or a particular weather type.
#### You can contact me for the dataset or it is also available on Kaggle, couldn't upload here because of the size restrictions.
