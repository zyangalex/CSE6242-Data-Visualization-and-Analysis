
#################################################
### THIS FILE WAS AUTOGENERATED! DO NOT EDIT! ###
#################################################
# file to edit: /home/notebook/work/Q3.ipynb

from pyspark.sql.functions import col
from pyspark.sql import *

def user():
    # Returns a string consisting of your GT username.
    return 'zyang363'

def long_trips(trips):
    # Returns a Dataframe with Schema the same as :trips:
    df3b = trips.filter(trips.trip_distance >= 2)
    return df3b

def manhattan_trips(trips, lookup):
    # Returns a Dataframe with Schema: DOLocationID, pcount
    trips=trips.withColumn("passenger_count",trips["passenger_count"].cast("integer").alias("passenger_count"))
    df3c = trips.join(lookup, trips.DOLocationID == lookup.LocationID).filter(col("Borough") == "Manhattan") \
    .groupBy(col("DOLocationID")).sum("passenger_count").withColumnRenamed("sum(passenger_count)", "pcount").sort("pcount", ascending = False).limit(20)
    return df3c

def weighted_profit(trips, mtrips):
    # Returns a Dataframe with Schema: PULocationID, weighted_profit
    # Note: Use decimal datatype for weighted profit (NOTE: DON'T USE FLOAT)
    # Our grader will be only be checking the first 8 characters for each value in the dataframe
    l = [row[0] for row in mtrips.select("DOLocationID").collect()]
    trips1 = trips.filter(trips.DOLocationID.isin(l))

    df3d0 = trips1.groupBy(col("PULocationID")).count().withColumnRenamed("count", "count1")
    df3d1 = trips.groupBy(col("PULocationID")).count()
    trips=trips.withColumn("total_amount",trips["total_amount"].cast("float").alias("total_amount"))
    df3d2 = trips.groupBy(col("PULocationID")).avg("total_amount").withColumnRenamed("avg(total_amount)", "amount")
    df3d3 = df3d1.join(df3d2, ["PULocationID"])
    df3d = df3d0.join(df3d3, ["PULocationID"], "left")
    df3d = df3d.withColumn("weighted_profit", (col("count1")/col("count"))*col("amount")).select(col("PULocationID"), col("weighted_profit")).sort("weighted_profit", ascending = False)


    return df3d

def final_output(calc, lookup):
    # Returns a Dataframe with Schema: Zone, Borough, weighted_profit
    # Note: Use decimal datatype for weighted profit (NOTE: DON'T USE FLOAT)
    # Our grader will be only be checking the first 8 characters for each value in the dataframe
    df3e = calc.join(lookup, calc.PULocationID == lookup.LocationID)
    df3e = df3e.select(col("Zone"), col("Borough"), col("weighted_profit")).sort("weighted_profit", ascending = False).limit(20)
    return df3e