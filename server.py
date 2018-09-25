from flask import Flask, jsonify, request 
from urllib.parse import quote
from logs import log_error
from logs import log_message
import requests
import json
import random

app = Flask(__name__) #define app using Flask

def error_message(error):
	return jsonify ({
						"replace_original" : False,
					    "response_type" : "ephemeral",
					    "text" : "Error",
					    "attachments" : [{
					    	"text": error + " Please try again."
					    }]
					})

#Shorten the url
@app.route('/shorturl', methods=['POST'])
def shortenURL():

	#Gets the words after "Post"
	try: 
		input = request.form.get('text')
	except Exception as e:
		log_error("<shortenURL> Error when requesting from POST")
		return error_message("Error when getting request from slack")

	if input is None or len(input.split()) == 0:
		log_error("<shortenURL> Invalid input. Current input: " + str(input))
		return error_message("Format is /shorturl <Long URL>.")

	#If message does not start with http:// or https:// append http://
	if str(input).startswith("http://") == False and str(input).startswith("https://"):
		input = "http://" + str(input)
	url = input.split()

	#Encode the url to required URL format used in browsers
	encodedUrl = quote(url[0], safe="")
	
	try:
		#Get response from Bitly API
		access_token = <access_token_from_bitly>
		response = requests.get("https://api-ssl.bitly.com/v3/shorten?access_token=" + access_token + "&longUrl=" + encodedUrl)

		log_message("<shortenURL> Response from bitly api: " + str(json.loads(response.text)))
		shortURL = str(json.loads(response.text)['data']['url'])
	except Exception as e:
		log_error("<shortenURL> Error: " + str(e))
		return error_message(str(input.split()[0]) + " is an Invalid Url.")

	result = "The short URL for " + url[0] + " is : " + str(shortURL)

	#Success
	log_message("<shortenURL> Result: Success")
	return (result)


#Definitions
@app.route('/definition', methods=['POST'])
def definition():
	try:
		input = request.form.get('text')
	except Exception as e:
		log_error("<definition> Error when requesting from POST")
		return error_message("Error when getting request from slack")

	if input is None or len(input.split()) == 0:
		log_error ("<definition> Invalid input. Current input: " + str(input))
		return error_message("Format is /definition <word>")

	#Take only the first word
	word = input.split()[0]

	#Return error if there is a number or special character in the word
	if word.isalpha() == False:
		log_error ("<definition> Non alphabet characters. Current input: " + str(input))
		return error_message(word + " is not a valid word.")

	result = ""
	numberDefinitions = 0
	try:
		response = requests.get("https://owlbot.info/api/v2/dictionary/" + str(word))
		log_message("<definition> Response from owlbot api: " + str(json.loads(response.text)))

		allDefinitions = json.loads(response.text)
		numberDefinitions = len(allDefinitions)

		for definition in allDefinitions:
			if definition['type'] is not None:
				result += "Type: " + definition['type'] + "\n"
			if definition['definition'] is not None:
				result += "Definition: " + definition['definition'] + "\n"
			if definition['example'] is not None:				
				result += "Example: " + definition['example'] + "\n"
			result += "\n"

	except Exception as e:
		log_error ("<definition> Error trace: " + str(e))
		return error_message("Unexpected error!")

	result = "I found " + str(numberDefinitions) + " definition(s)\n\n" + result
	log_message("<definition> Result: Success")
	return (result)


#Rock, Papers, Scissors
@app.route('/rps', methods=['POST'])
def rockPapersScissors():

	try:
		input = request.form.get('text')
	except Exception as e:
		log_error("<Rock, Papers, Scissors> Error when requesting from POST")
		return error_message("Error when getting request from slack")

	correct_inputs = ["rock", "papers", "scissors"]

	if input is None or len(input.split()) == 0 or str(input.split()[0]).lower() not in correct_inputs:
		log_error ("<Rock, Papers, Scissors> Invalid input. Current input: " + str(input))
		return error_message("Input format is /rps <rock/papers/scissors>.")

	user_move = str(input.split()[0]).lower()
	
	comp_move = random.randint(0, 2)
	comp_dict = {}
	for number, element in enumerate(correct_inputs, 0):
		comp_dict[number] = element

	log_message ("<Rock, Papers, Scissors> user_move: " + user_move + " comp_move : " + comp_dict[comp_move])

	result = "I choose " + comp_dict[comp_move] + ". "
	if comp_dict[comp_move] == user_move:
		result +=  "Its a tie."
	else:
		resultDict = {
			"rock": {
                    1: "You Lose",
                    2: "You Win"
                    },
            "papers": {
                    0: "You Win",
                    2: "You Lose"
                    },
            "scissors": {
                    0: "You Lose",
                    1: "You Win"
                    }
            }

		result += resultDict[user_move][comp_move]

	#Success
	log_message ("<Rock, Papers, Scissors> Result: Success")
	return result

@app.route('/thumbsup', methods=['POST'])
def thumbsUp():
	return jsonify({
    "text": "Did you like the Slash Commands?",
    "attachments": [
        {
            "title": "Slash commands integrated"
		},
		{
                    "title": "/shorturl",
                    "text": "Shortens the given URL"
		}   
            ,
		{
                    "title": "/definition",
                    "text": "Retrieves definitions of a word"
		}   
            ,
		{
                    "title": "/rps",
                    "text": "Play Rock, Papers, Scissors!"
		}    
            ,
        {
                    "title": "/thumbsup",
                    "text": "Feedback!"
		}    
            ,
		{
            "image_url": "http://is4profit.com/wp-content/uploads/2009/05/smiley-face.jpg"
		},
        {
            "fallback": "Would you recommend it to customers?",
            "title": "Would you recommend it to customers?",
            "callback_id": "comic_1234_xyz",
            "color": "#3AA3E3",
            "attachment_type": "default",
            "actions": [
                {
                    "name": "Yeah!",
                    "text": "Yeah!",
                    "type": "button",
                    "value": "yes"
                },
                {
                    "name": "Nope",
                    "text": "Nope",
                    "type": "button",
                    "value": "no"
                }
            ]
        }
    ]
})

#Re-routing response for ThumbsUp
@app.route('/response', methods=['POST'])
def response_from_selection():

	try:
		inputDict = dict(request.form)
	except Exception as e:
		log_error("<response_from_selection> Error when requesting from POST")
		return error_message("Error when getting request from slack")

	payLoad = inputDict['payload'][0]
	inputValue = json.loads(payLoad)['actions'][0]['value']
	if inputValue == "yes":
		feedback = open("feedback.txt", "a+")
		feedback.write("{0}: ++The user liked the Slash Commands".format(str(datetime.datetime.now())))
		feedback.close()
		return jsonify({
			"attachments": [
				{
					"title" : "Thank you!"
				},
				{
					"image_url": "http://is4profit.com/wp-content/uploads/2009/05/smiley-face.jpg"
				}
			]
			})
	elif inputValue == "no":
		feedback = open("feedback.txt", "a+")
		feedback.write("{0}: --The user disliked the Slash Commands".format(str(datetime.datetime.now())))
		feedback.close()
		return jsonify({
			"attachments": [
				{
				"title" : "Aww!"
				},
				{
				"image_url": "https://storage.googleapis.com/3d_model_images/411/4114156/happy-face-head-sad-small-3d-model-nQ0sI90zs_200.jpg"
				}
			]
			})
	log_error ("<response_from_selection> Error inputValue: " + inputValue)
	return error_message("Unexpected error when responding to feedback")

def main():
	app.run(port=8080) #run app on port 8080 in debug mode

if __name__ == '__main__':
	 main()

#Last editied by Daniel Benniah John
