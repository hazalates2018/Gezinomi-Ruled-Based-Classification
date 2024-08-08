
# Calculating Potential Customer Revenue with Rule-Based Classification
# Business Problem
# Gezinomi wants to create level-based new sales definitions using some characteristics
# of their sales and form segments based on these new sales definitions.
# They aim to estimate how much new potential customers could bring to the company
# on average according to these segments. For example, they want to determine
# the average revenue a customer might bring who wants to go to an all-inclusive hotel in Antalya during a busy period.


# PROJECT TASKS
# TASK 1: Answer the following questions.

# Question 1: Read the file `miuul_gezinomi.xlsx` and display general information about the dataset.

import pandas as pd
import seaborn as sns

df = pd.read_excel("C:\\Users\\hazal\\OneDrive\\Masaüstü\\datasets\\miuul_gezinomi.xlsx")
df.head()
df.info()

# Question 2: How many unique cities are there? What are their frequencies?

df["SaleCityName"].nunique()
df["SaleCityName"].info()

# # Question 3: How many unique Concepts are there?

df["ConceptName"].nunique()

# Question 4: How many sales have occurred from each Concept?
df["ConceptName"].value_counts()


# Question 5: How much total revenue has been earned from sales by city?
df.groupby("SaleCityName")["Price"].sum()

# Question 6: How much has been earned by concept types?

df.groupby("ConceptName").agg({"Price":"sum"})

# Question 7: What are the average PRICE values by city?
df.groupby("SaleCityName")["Price"].mean()

# Question 8: What are the average prices by concept?

df.groupby("ConceptName")["Price"].mean()

# Question 9: What are the average PRICE values by city and concept breakdown?

df.groupby(["SaleCityName","ConceptName"])["Price"].mean()


# TASK 2: Convert the satis_checkin_day_diff variable into a new categorical variable named EB_Score.

bins = [-1,7,30,90,df["SaleCheckInDayDiff"].max()]

labels = ["Last Minuters", "Potential Planners", "Planners", "Early Bookers"]
df["EB_Score"] = pd.cut(df["SaleCheckInDayDiff"],bins,labels=labels)
df.head(50).to_excel("eb_scorew.xlsx", index=False)
#############################################

# TASK 3: Examine the average fees and frequencies by the breakdown of City, Concept, [EB_Score, Season, CInday]

# City-Concept-EB Score breakdown of average fees
df.groupby(by=["SaleCityName","ConceptName","EB_Score"]).agg({"Price":"mean","count"})

# Average Prices by City-Concept-Season Breakdown
df.groupby(by=["SaleCityName","ConceptName","Seasons"]).agg({"Price":"mean","count"})

# Average Prices by City-Concept-CInday Breakdown
df.groupby(by=["SaleCityName","ConceptName","CInDay"]).agg({"Price":"mean","count"})


# TASK 4: Sort the output of the City-Concept-Season breakdown by PRICE.
# To better view the output from the previous question, sort the PRICE column in descending order using the sort_values method.
# Save the output as `agg_df`.
agg_df = df.groupby(by=["SaleCityName","ConceptName","Seasons"]).agg({"Price": "mean"}).sort_values("Price",ascending=False)

# TASK 5: Convert the names in the index to variable names.
# In the output of the third question, all variables except for PRICE are index names.
# Convert these names into variable names.
agg_df.reset_index(inplace=True)


# TASK 6: Define new level-based sales and add them as variables to the dataset.
# Define a variable named sales_level_based and add this variable to the dataset.
agg_df['sales_level_based'] = agg_df[["SaleCityName", "ConceptName", "Seasons"]].agg(lambda x: '_'.join(x).upper(), axis=1)


# TASK 7: Segment the personas into groups.
# Segment based on PRICE
# Add the segments to agg_df with the name "SEGMENT".
# Describe the segments
agg_df["sales_level_based"] =pd.qcut(agg_df["Price"],4,labels=["D","C","B","A"])
agg_df.head(20)
agg_df.groupby("SEGMENT").agg({"Price":["mean","max","sum"]})

# TASK 8: Sort the resulting DataFrame by the price variable.
# Which segment does "ANTALYA_HERŞEY DAHIL_HIGH" belong to, and what is the expected fee?
new_user = ["ANTALYA_HERŞEY_DAHİL_HIGH"]

filtered_df = agg_df.loc[(agg_df["SaleCityName"]=="Antalya") & (agg_df["Seasons"] == "High") & (agg_df["ConceptName"] == "Herşey Dahil")]

filtered_df2= agg_df.loc[(agg_df["SaleCityName"]=="Girne") & (agg_df["Seasons"] == "Low") & (agg_df["ConceptName"] == "Yarım Pansiyon")]
