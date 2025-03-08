# Data Engineering Career Coach 

## Setup Instructions for Case Study 1
Kindly follow the instructions here to run the code  locally on your laptop.

First run the following in your terminal:

```shell
git clone https://github.com/tseyongg/de-career-coach.git
cd de-career-coach
```

Then, to run and generate the output required for Case Study 1 , run this next:
```shell
cd case-study 1
docker-compose up
```
When the container exits, you should see a folder populate in your root directory called `output`

Inside contains:

- `restaurant_details.csv`
- `restaurant_events.csv`
- `restaurant_ratings_histogram.png`

These answer Task 1, 2 and 3 respectively. Also, analysis steps for Task 3 will be displayed on your terminal. More details and key design decisions can be found [here](/case-study-1/README.md)

When you are done, simply run:

```shell
docker-compose down
cd ..
```
## Case Study 1 Architecture

![case-study-1-architecture](/images/case_study_1_architecture.png)

***

## Setup Instructions for Case Study 2
Kindly follow the instructions here to run the code  locally on your laptop.

Now, for Case Study 2, simply run the following in your terminal:

```shell
cd case-study 2
docker-compose run --rm app
```

And you will be able to interactively query the application from your terminal.

You can enter:

- 1 to search by Carpark Number
- 2 to search by Address
- 3 to end your session

More details and key design decisions can be found [here](/case-study-2/README.md)

When you are done, simply hit 3, then run:

```shell
docker-compose down
cd ..
```

## Case Study 2 Architecture

![case-study-2-architecture](/images/case_study_2_architecture.png)


***

## Cloud Deployment

### Case Study 1

For Case Study 1, I would implement a Batch Data Processing Framework on AWS, with the following:

- **AWS Lambda** functions to be triggered for processing restaurant and event data

- **S3** for data storage, especially for static JSON or CSV file types

- **DynamoDB** for the purpose of storing restaurant data for fast retrieval

- **AWS Step Functions** to orchestrate the job in sequence

- **Amazon CloudWatch** to gather logging errors and to monitor execution details

### Case Study 2

- **ElastiCache** to be able to cache frequent API responses and thus improve performance (mimic Redis)

- **AWS Lambda** functions similarly to be used for handling user search, data merging and output results formatted properly

- **DynamoDB** to store carpark availability and ensure frequent read and writes with low latency

- **Amazon CloudWatch** for monitoring and logging

- **Amazon API Gateway** to publish and maintain my APIs at scale

## Further Cloud Implementations

I would also make use of:

- **Terraform** to provision my resources on AWS via IAC

- **AWS IAM** to abide by principle of least priviledge

- **AWS CodePipeline** to maneveure between separate dev/prod environments, making use of CI/CD

During peak periods where traffic spikes may occur, my Lambda functions would be able to auto-scale to meet the increased demand, while DynamoDB when enabled into on-demand mode will allow for the increased surges by auto scaling as well, which is implenmented via pay per request pricing. Possibly, I could also set up Amazon Simple Queue Service to allow user requests to wait in queue until Lambda is able to process them. Otherwise, time outs or failures might result.

