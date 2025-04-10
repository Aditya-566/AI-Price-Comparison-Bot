1. Install Python 3.6+
Make sure you have Python 3.6 or later installed. You can download Python from here.
You can verify your Python version by running:

python --version
It should return a version of Python 3.6 or later.

2. Set Up a Virtual Environment (Optional but Recommended)
To avoid conflicts with other Python projects, it's best to use a virtual environment.

Create a virtual environment:

python -m venv venv
Activate the virtual environment:

Windows:
venv\Scripts\activate

for MacOS/Linux:
source venv/bin/activate

3. Install Required Libraries
Now that you're in the project directory and have the virtual environment set up (if you chose to), run the following command to install the necessary libraries:

Install libraries using pip:

pip install requests beautifulsoup4 rich

These libraries are required to scrape the websites and display the output in a nice format.
