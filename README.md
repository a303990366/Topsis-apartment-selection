# Soft-apartment-selection

## 1. Introduction
The project is the final-term project of the decision-making course. The motivation for the idea is that most people have a need in renting apartments because most people can not afford expensive housing prices in Taiwan. For fitting the need, I create the project. 
In this project, we provide a flexible and quick way to help users make decisions for their future apartments through the Topsis algorithm. 
## 2. Special Points
* Design an apartment-choosing app for the Taiwan apartment market.
* Provide a quick way to organize useful information for users.
* Provide an interface that is easy to use for making user choose their ideal apartment based on user's preferences through the TOPSIS algorithm.

## 3. FlowChart
![FlowChart](https://github.com/a303990366/Topsis-apartment-selection/blob/main/Topsis_apartment_selection/pic/apartment-selection.png)

From the above flowchart, we can see:

1. Users should choose the county and towns that they want to live in the future, users can choose at most three towns.
2. The app will crawl data from the target website which contains apartment-related information.
3. Users should set the importance of each criteria as the TOPSIS algorithm's input.
4. TOPSIS algorithm will rank all apartments based on users' preferences.
5. Save the ranking results
6. We show organized information to users, such as cost, apartment type, Equipment supply rate, and the number of restaurants, stores, public transportation, and school. 
7. If users want to see more detailed information about specific apartments, they can click the button, and then the app will direct users to the web page of a specific item. If not, the users can close the window of the app.

## 4. Criteria

Criteria is an important element in decision-making. In this project, we design ten criterias. it is shown as the below picture.
![FlowChart](https://github.com/a303990366/Topsis-apartment-selection/blob/main/Topsis_apartment_selection/pic/choose_preference.jpg)

If users think some specific criteria are important for them, they should set a higher value in the specific slider. If not, they should set the value lower. In other words, the value in sliders means importance.

Now, we introduce detailed information on each criteria.
1. Cost: Apartment price
2. Type: Apartment type, such as studio, Bedsit...etc
3. Location-traffic: the number of public transportation near the apartment
4. Location-life: the number of  stores and restaurants near the apartment
5. Location-education: the number of schools near the apartment
6. Area: Area of the apartment
7. Building: building type
8. Equipment: Equipment number in the apartment
9. Poster: Poster of the apartment on the website
10. Reach/Save: how many people look into the apartment/how many people save the apartment in their list
    
## 5. How to use it?
First, install all of the required packages: pip install -r requirements.txt
Second, perform the code: python main.py

## 6. Demo


https://github.com/a303990366/Topsis-apartment-selection/assets/49556199/40a24aa4-b18e-42e2-a8c1-9fa2ea880e23


## 7. Conclusion

In the period of the course, I learn how to design an app from the users' perspective. Because of high housing prices in Taiwan, many people must rent an apartment for living if they don't have a house near their working place.

In the project, I try to reduce the time of searching for a suitable apartment, I use a crawler for getting data and TOPSIS for making decisions. It should be noted that we also quantify the convenience of living in each apartment. I think this is very useful for users since different users have different needs. For example, a college student wants to live in an environment with many restaurants. Taking another example is parents want to live near schools for their children. By the way, we also quantify equipment of apartments whether enough or not.

Overall, this is my first time creating an app by Kivy, this is a powerful package.

