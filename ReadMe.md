### Get Data on Journalists

Scrape data on journalists from [Presspass](http://www.presspass.me/) and [MuckRack](http://muckrack.com/). 

Both scripts take a csv with column carrying twitter usernames labeled 'twitter.username.' (See [sample data](sample_input.csv).)

#### Running the Scripts

##### Prerequisites
	- Python 3.x
	- BeautifulSoup 4
	
#### Muckrack

1. Scrape data to file:

    <pre> python scrape_muckrack.py input_file </pre>
    
    HTML files will be saved to `./muckrack`

2. Parse and extract information from file:

    <pre> python extract_muckrack.py input_file</pre>

    Output CSV file will be saved as `muckrack-out.csv`


#### PressPass

1. Scrape data to file:

   <pre> python scrape_presspass.py input_file </pre>

    HTML files will be saved to  `./presspass`

2. Parse and extract information from file:

    <pre>python extract_presspass.py input_file </pre>

    Output CSV file will be saved as `presspass-out.csv`

#### License

Scripts are released under the [MIT License](https://opensource.org/licenses/MIT).
