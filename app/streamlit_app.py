import os
import pandas as pd
import streamlit as st

from pyspark.ml.recommendation import ALSModel
from pyspark.sql import SparkSession
import pyspark.sql.functions  as F

"""
# Welcome to Recommendator!

This application will recommend you restauranst in Reno according with other users. This is an example of collaborative reccomentation algorithm.
 
"""

df_users = pd.read_csv('./data/users.csv')
df_users.columns = ['ID', 'UserName']
maxuser = df_users.shape[0]

directory_path = os.getcwd()
out = os.path.join(directory_path, 'model','reno')

# Fuction to get reccomendations.

def recommend(user, number_of_recs, spark, model, df_restaurants):
	data = [[user]]
	columns = ["user_id_index"]
	user_df = spark.createDataFrame(data, columns)

	user_rec = model.recommendForUserSubset(user_df,number_of_recs)
	user_rec = user_rec.select('user_id_index', F.explode("recommendations").alias("recs"))
	user_rec = user_rec.select('user_id_index', F.col('recs.business_id_index'), F.col('recs.rating'))
	user_rec = (user_rec.join(df_restaurants, on='business_id_index', how='inner')
                        .select('rating', 'name', 'city', 'categories')

            )
	df_user_rec = user_rec.toPandas()

	return df_user_rec


@st.experimental_singleton
def init_spark():
	appName="Recommender with collaborative Filtering"
	spark = SparkSession.builder.appName(appName).getOrCreate()
#	st.write('Spark ok')

	model=ALSModel.load(os.path.join(directory_path, 'model', 'reno'))
#	st.write('Model ok')

	return spark, model

spark, model = init_spark()
st.write('Spark ok')

#initialize the spark session


# Slider 
user = st.slider('Pick a Users', 0, maxuser, 10000)
st.write("You picked user ", user)

number_of_recs = st.slider('Select the number of restaurants to recomend.', 0, 20, 5)


# Get the list of restauirants
df_restaurants = spark.read.json("./data/restaurants.json")

# Generate recommendation

recommendations = recommend(user, number_of_recs, spark, model, df_restaurants)
# Print results

"""
## Results

Here are the restaurants with the best matching according to other users similar to you. 
"""

st.write("These are the results:")
st.dataframe(data=recommendations)



# test_inference = model.recommendForAllUsers(20).filter(F.col('user_id_index')==30).select("recommendations").collect()

# st.echo(test_inference)


