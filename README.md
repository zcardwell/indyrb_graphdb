# Hacking with Graphs


## Description

This is the repo I was using for my talk on March 10,2021 with Indy.rb ! The describes graphs and graph databases and this repo has a few cooked, quick examples to show off the concepts. 

### Schedule

This is a *_simplistic_* scheduling set up that I threw together to based on the scheduling headaches I used to face in years pass. The python script (assuming that you have a neo4j instance running) will generate fake scheduling data by randomly generating role assignments, tenures, ages, and people. 

If you have a local instance set up with neo4j and have the appropriate dependencies installed, you should just need to do this from the command line:

```python3 schedule_gen.py```

from the schedule_example directory. 

If you're more interested in scheduling: 
- [Interval Graphs](https://en.wikipedia.org/wiki/Interval_graph) 
- [Job Shop Scheduling](https://en.wikipedia.org/wiki/Job_shop_scheduling)
- [Some math that comes up quite a bit in this work](https://en.wikipedia.org/wiki/Linear_programming) 

### Recommendation

We built a very very simple recommendation engine that I randomly generated based on a random hidden preference. 

Like the Schedule directory, if you have an instance of neo4j running locally with the dependencies and credentials set equivalently, you should jsut need to do this from the command line:

```python3 recommendation_gen.py```

from the recommendation_example directory.

