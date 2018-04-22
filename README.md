# Reflecting on the Past to Prepare for the Future
## Project Idea
Build an open source pipeline to explore historical events ocurred in the past and how they connect with latest news happening in the present to provide us insight, wisdom and experience for future decisions.  
## Purpose
The lessons of the past can become meaningful and instructive to the present and the future. Studying the past can be a fascinating adventure. For example, if one made a serious mistake in the past, the only way to learn from it is to adopt a new set of behaviors that avoids the similar mistake in the future. Same holds ture if we scale to organizations, communities, nations and world. 
## Use Case
* There is a radio broadcast program called 'Today in History' which is my favorite to listen to when I commute. It will be cool if we can query what happened in history with the same time as now lively.
* Any kind of query based on geolocations, time, categories, etc. 
* Find connections bewteen the historical events and current ones and visualize.  
## Data Source
* The Global Database of Events, Language, and Tone (GDELT) includes news and events data from 1979 to present. 
* The size of the dataset is estimated to be ~ TB in order of magnitude.
* For Bashing processing historical archived dataset will be used (e.g. from 1973 to 2017)
* For Streaming processing more current dataset will be used to simulate current stream based on timestamp(e.g. 2018)
## Technology Considered
* Data Storage Layer: AWS S3
* Data Ingestion Layer: Kafka
* Streaming Process: Spark Streaming, Flink
* Bash Process: Spark
* DataBase: Canssandra
## Pipeline Architecture
