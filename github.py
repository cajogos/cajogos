import requests
import math

BASE_URI = 'https://api.github.com'

def get_info(username, token):
	# Obtain the public information for the given github username
	endpoint = f"{BASE_URI}/users/{username}"
	headers = get_default_headers(username)
	r = requests.get(endpoint, headers=headers, auth=(username, token))
	r.raise_for_status()

	# Get the JSON response
	json = r.json()

	# Only return some of the required information
	output = {
		'id': json['id'],
		'username': json['login'],
		'name': json['name']
	}

	# Get public repositories info
	output['repos'] = get_repos(username, token, json['public_repos'])

	return output

def get_repos(username, token, num_repos):
	endpoint = f"{BASE_URI}/users/{username}/repos"
	headers = get_default_headers(username)

	# Array to store the repositories
	repos = []

	per_page = 5
	page = 1
	total_pages = math.ceil(num_repos / per_page)

	while (page <= total_pages):
		params = {
			'type': 'owner',
			'sort': 'updated',
			'per_page': per_page,
			'page': page
		}
		r = requests.get(endpoint, params=params, headers=headers, auth=(username, token))
		r.raise_for_status()

		json = r.json()

		if (len(json) > 0):
			for repo in json:
				repos.append({
					'id': repo['id'],
					'name': repo['name'],
					'full_name': repo['full_name'],
					'url': repo['html_url'],
					'description': repo['description'],
					'stars': repo['stargazers_count'],
					'watchers': repo['watchers_count'],
					'language': repo['language'],
					'forks': repo['forks_count'],
					'size': repo['size']
				})
		else:
			# Break out if the owner typed repos are finished
			break
		page = page + 1

	# Sort the repos by stars
	repos = sorted(repos, key=lambda k: k['stars'], reverse=True)

	return repos

def get_default_headers(username):
	return {
		'User-Agent': username,
		'Accept': 'application/vnd.github.v3+json'
	}
