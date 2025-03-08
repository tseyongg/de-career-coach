# Data Engineering Career Coach 

## Setup Instructions for Case Study 1
Kindly follow the instructions here to run the code  locally on your laptop.

First run the following in your terminal:

```shell
git clone https://github.com/tseyongg/de-career-coach
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

These answer Task 1, 2 and 3 respectively. Also, analysis steps for Task 3 will be displayed on your terminal. More details, key design decisions can be found [here](/case-study-1/README.md)

When you are done, simply run:

```shell
docker-compose down
cd ..
```
The following illustrates Case Study 1's architecture:

![case-study_1-architecture](/images/case_study_1_architecture.png)

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

When you are done, simply hit 3, then run:

```shell
docker-compose down
cd ..
```


