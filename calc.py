prompt = '> '
print "Enter item cost in USD:  "
cost = raw_input(prompt)
print "How much can you sell for: "
value = raw_input(prompt)

profit = int(value) - int(cost) - (0.5*int(cost)) - 25 - .04*int(value) - 5.75 

print profit 
