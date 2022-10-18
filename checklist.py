'''
the signal flow of cropped items

read CSV of scraped photos
	use pandas
	iterate thru each row
	function to take in url
	makes image from url
	

primary images
	get urls
	run in cloud vision
 		post request using api_key
	get JSON
	search json for person
	if person, get garments 
		(find documentations of all garmets! aka our dictionary
	crop garments ...



...crop garments
	from json
	create crop vertices
	save cropped items objects
	post request crop object
	get json
	get dominant colors

	

write to csv crops
	match crop to original
		send object name and object date as props from parent pic to child pic
	write:
		dominant colors
		date
		clothing item



other things we might want in this stage outside of raw colors:

	age, mood, gender... or not 


clothes:

Hat

Shirt
Coat
Dress

Skirt
Miniskirt
Trousers
Jeans
Shorts

Swimwear





'''
