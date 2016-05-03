# wedding_seating

Small project to use simulated annealing (https://en.wikipedia.org/wiki/Simulated_annealing), to create a seating plan for a wedding.

Input: A CSV file containing the weightings of all guests relationships.

Output: Guests grouped into tables. 

Is this actually useful? 

Probably not. 
It turns out that doing the data input for this is hard work. For it to give you a decent result, you need to the relationship between every pair of guests. There's a lot of those, so it's hard.
For me, the process of doing that made it clear that I was already aware of most of the clustering in the guest graph. Rather than wasting time ennumerating relationships that almost certainly don't matter (which is most of them) you're probably better off doing your wedding seating like a normal person.
There might be some value in this if there aren't obvious groupings of people. 
Anyway, I did this for fun/interest/utility, so it doesn't matter. 

## Usage
```
python wedding.py -g example_relationships.csv -ts 3 -i 3 -b example_high_score
```

Copy the layout in example_relationships.csv for your own guest relationships.


# TODO:

1) More complex score. Done (partially?)

b) Include loneliest person - currently 0, so not much use. Are there many 0s? Lowest table: ~50, is this good?

2) Preset table sizes.

3) Seats at table.

4) Performance?
