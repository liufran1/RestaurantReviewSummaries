from setuptools import setup, find_packages

setup(
   name='restuarantsummarize',
   version='1.0',
   description='Summarize restaurant reviews on a page',
   author='Franklin Liu',
   author_email='me@franklinliu.com',
   packages=find_packages(exclude=['test']),  #same as name
   install_requires=['bs4', 'pandas', 'openai', 'python-dotenv'], 
)