from pyspark.sql import SparkSession
spark = SparkSession.builder.appName("beula").getOrCreate()
df = spark.read.option("header",True).csv("/root/airflow/inputfiles/timber_land_stock.csv")
df.createOrReplaceTempView("timber")
high_date = spark.sql("select Date,High from timber where High=(select max(High) from timber)")
mean_close = spark.sql("select mean(Close) as Mean_Close from timber")
min_volume = spark.sql("select min(Volume) as Min_Volume from timber")
max_volume = spark.sql("select max(Volume) as Max_Volume from timber")
close60dollars = spark.sql("select Date as Close_ls_60 from timber where Close<60.00")
close60dollars.createOrReplaceTempView("close60dollars")
count60close = spark.sql("select count(*) as No_of_days_is60 from close60dollars")
pearson_corr = spark.sql("SELECT corr(High, Volume) AS pearson_corr from timber")
max_high_per_year = spark.sql("select year(Date) as Year, max(High) as max_high from timber group by Year order by Year asc")
avg_close_per_month = spark.sql("select month(Date) as Month, avg(Close) as avg_close_monthly from timber group by Month order by Month asc")
df.write.csv('/root/airflow/outputfiles/df.csv',mode='overwrite',header=True)
high_date.write.csv('/root/airflow/outputfiles/high_date.csv',mode='overwrite',header=True)
mean_close.write.csv('/root/airflow/outputfiles/mean_close.csv',mode='overwrite',header=True)
min_volume.write.csv('/root/airflow/outputfiles/min_volume.csv',mode='overwrite',header=True)
max_volume.write.csv('/root/airflow/outputfiles/max_volume.csv',mode='overwrite',header=True)
count60close.write.csv('/root/airflow/outputfiles/count60close.csv',mode='overwrite',header=True)
pearson_corr.write.csv('/root/airflow/outputfiles/pearson_corr.csv',mode='overwrite',header=True)
max_high_per_year.write.csv('/root/airflow/outputfiles/max_high_per_year.csv',mode='overwrite',header=True)
avg_close_per_month.write.csv('/root/airflow/outputfiles/avg_close_per_month.csv',mode='overwrite',header=True)
spark.stop()