#!/usr/bin/env python
import utils
import github
from time import strftime

# Current time
timestamp = strftime('%H:%M on %b %d, %Y')

# Load the configurations
config = utils.get_config('config.yaml')

# Get the user's github information
gh_info = github.get_info(str(config['github']['username']), str(config['github']['token']))

# Clear the current README file
utils.clear_file('README.md')

with open('README.md', 'a') as readme:
	# Initial presentation values
	readme.write(f"# {config['name']}'s ({gh_info['username']}) GitHub Info \n")
	readme.write(f"Follow me on [Twitter](https://twitter.com/{config['twitter']}). ")
	readme.write(f"Connect with me on [LinkedIn](https://linkedin.com/in/{config['linkedin']}).\n")

	# Repositories
	if (len(gh_info['repos']) > 0):
		readme.write(f"## Repositories\n")
		readme.write(f"\n| Repositories | | ⭐ Stars | 📚 Forks | 👀 Watchers |")
		readme.write(f"\n|---|---|:---:|:---:|:---:|")
		for repo in gh_info['repos']:
			if (repo['name'] not in config['github']['repos']['exclude']):
				readme.write(f"\n|[{repo['name']}]({repo['url']})|{repo['description']}|{repo['stars']}|{repo['forks']}|{repo['watchers']}|")

	# Finally, write the time it was updated
	readme.write(f"\n\n---\n**Last updated:** {timestamp}\n")
