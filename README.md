# Opinion Miner 🧠

Opinion Miner is a sentiment analysis tool that extracts opinions from social media platforms and provides insights on specific topics. It utilizes natural language processing techniques to analyze text data and classify sentiments as positive, negative, or neutral.

The opinion mining tool is designed to provide insights on any topic by analyzing opinions from Reddit. The tool uses the PRAW library to access Reddit’s API, TextBlob for sentiment analysis, and Django for the web framework.

## Accesibility

The project can be opened and used via **[44.200.246.83:8000](44.200.246.83:8000)** address. It is dockerized and actively running on an EC2 Ubuntu instance. 


## Features

- Fetch opinions from Reddit.
- Perform sentiment analysis on collected opinions to determine the overall sentiment using TextBlob.
- Generate visualizations, such as trend graphs and word clouds, to visualize sentiment trends and popular keywords.
- Ability to opinions based on specific topics, time intervals, and sentiment categories.
- Support for multiple languages and customizable sentiment analysis models.
- Easy-to-use web interface for querying and visualizing opinions.


## Installation

1. Clone the repository: `git clone https://github.com/samedtorunn/opinion_mining.git`
2. Install the required dependencies: `pip3 install -r requirements.txt`
3. Configure the necessary API credentials (yours or the ones given by me)
4. Make migrations: `python3 manage.py makemigrations`
5. Migrate: `python3 manage.py migrate`
6. Run the project: `python3 manage.py runserver`

## Usage

1. Access the Opinion Miner web interface at `http://localhost:8000` (or the appropriate URL).
2. Enter a query keyword, select the desired time interval, and click the "Search" button.
3. View the retrieved opinions, sentiment distribution, trend graph, and word cloud visualization.
4. Filter opinions based on sentiment categories using the provided checkboxes.
5. Explore the sentiment trends and popular keywords to gain insights on the topic of interest.

## Contributing

Contributions are welcome! If you have any suggestions, bug reports, or feature requests, please open an issue or submit a pull request. Please make sure to follow the coding style and guidelines specified in the repository.

## Acknowledgements

- The sentiment analysis component of this project is powered by the [TextBlob](https://textblob.readthedocs.io/) library.
- The word cloud visualization is created using the [WordCloud](https://amueller.github.io/word_cloud/) library.
- Special thanks to the Suzan Uskudarli who provides me the vision for this project.


