import json

def update_rating(business_details, new_rating):
    curr_rating = business_details['current_rating']
    total_ratings = business_details['total_ratings']
    
    full_rating = round(curr_rating * total_ratings, 4)
    new_full_rating = full_rating + new_rating
    total_ratings += 1

    updated_rating = round(new_full_rating / total_ratings, 4)
    business_details['current_rating'] = updated_rating
    business_details['total_ratings'] = total_ratings
    return updated_rating

def add_business(business_name):
    data.append({
    "business_name": business_name,
    "current_rating": 0,
    "total_ratings": 0})

def display_rating(business_details):
    print("Current rating of " + business_details['business_name'] + ": " + str(business_details['current_rating']))


#Opening file in read
with open("ratings.json", "r") as f:
    data = json.load(f)

#Testing
#print("current rating: ", data[1]['current_rating'])
print("updated_rating: ", update_rating(data[1], 4))
display_rating(data[2])

#Re-write whole file with updated information
with open("ratings.json", "w") as f:
    json.dump(data, f, indent=2)
