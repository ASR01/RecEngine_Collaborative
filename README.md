# RecEngine_Collaborative 

This project pretends to use pyspark and more concretely the ALS Recomendation collaborative model to get a restaurant recommendation.

This project consist of two separate items.

1. First a Jupyter Notebook wehre the data analysis is done and the model is trained.
2. A docker image of the model oowrking in a Streamlit app.

## Data Preparation and Training

### Data acquisition

We are going to use the Yelp Dataset https://www.yelp.com/dataset that you can obtain from the written address.

From the whole dataset we are going to use the following files:

- yelp_academic_dataset_business.json
- yelp_academic_dataset_review.json

In the first one there is a list of business in 11 metropolitan areas and in the second there are aproximately 6M reviews from users.

There are not in these repository but the data has to be loaded and stores in *./yelp_data/* folder.

### Data Analysis

After we load the data into a PySpark datafram ewe can see the schema and we decide to pick only a city and a tipe of business (restaurant)in order to make the model less heavy.

I decided to go with Reno.

So I have to dataframes, but to use the ALS algorithm I need only one.

### Data Preparation

You can use the Business_ID as key to join both tables. Additionaly you have to remap the User_ID and Business_ID in a format you can use (the actual sind alphanumeric character with no order)



### Training

With the join table obtained. YOu only have to separate them into training and test sets. YOu need in the ALS model the following parameters:

- maxIter=10 *Number of iterations*
- regParam=0.09 *regularisation parameter*
- rank=25 * Factorisation rank*
- userCol="user_id_index"
- itemCol="business_id_index" *Column where the item data is stored*
- ratingCol="stars" *The coulumn where the user rating is*
- coldStartStrategy="drop" *What to do in the case of new users that where not seen in the training data, in this case, drop.


## Inference

For the inference I decided to use an Straimlit application embedded in a docker container.

The Dockerfile and all required information is in the repository.





