
#!/usr/bin/env python
# coding: utf-8

# ## Notebook 1
# 
# New notebook

# In[2]:


from pyspark.sql.functions import col

# 1. Load the raw data
df = spark.read.format("csv").option("header","true").load("Files/data/SuperMarket Analysis.csv")

# 2. Rename columns (replace spaces with underscores)
for column in df.columns:
    df = df.withColumnRenamed(column, column.replace(" ", "_"))

# 3. "Cast" the columns to the correct numeric types
# We use Decimal for money and Integer for counts
df = df.withColumn("Unit_price", col("Unit_price").cast("decimal(18,2)")) \
       .withColumn("Quantity", col("Quantity").cast("int")) \
       .withColumn("Tax_5%", col("Tax_5%").cast("decimal(18,2)")) \
       .withColumn("Sales", col("Sales").cast("decimal(18,2)")) \
       .withColumn("gross_income", col("gross_income").cast("decimal(18,2)")) \
       .withColumn("Rating", col("Rating").cast("double"))

# 4. Save as a Delta Table (using 'overwrite' to fix your previous attempt)
# The 'overwriteSchema' option is the key to fixing the merge error
df.write.format("delta") \
  .mode("overwrite") \
  .option("overwriteSchema", "true") \
  .saveAsTable("fact_SupermarketSales")

# 5. Verify the types
df.printSchema()