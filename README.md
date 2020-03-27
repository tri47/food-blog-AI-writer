

> Happy Sunday Melbourne! I’m here to spoon a delicious home-made Guacamole and Butternut Smoked Salmon.


> Fried Croissant with sourdoughnuts and creamy pancake batter. My favourite breakfast in New York City and @eriqulotopos some stupid puns.

# AI Food Blog Writer
Train an AI (OpenAI's GPT-2 model) to write food blog entries

## Intro
This is my attempt to train OpenAI's GPT-2 language model to write snippets for a (instagram) food blog. OpenAI made waves earlier last year when they released this model, which was deemed [too dangerous](https://techcrunch.com/2019/02/17/openai-text-generator-dangerous/) for the full version to be released. It subsequently released the full version in Nov 2019, and saw many new applications.
This repository is used to outline the steps I took to tune the model to write food blog snippets and deploy to AWS. 
There are a lot of resources on these topics on the Internet, so I will focus on the nuances and pitfalls that I discovered.

## The data
I repurposed the code I used to scrape an Instagram profile page to extract sample food blog posts from Instagram as raw data. I ended up with about 15,000 lines of text.

## Training the model
I used the small version of the model (124M model- 500MB on disk). [This Google Colab Notebook](https://colab.research.google.com/drive/1VLG8e7YSEwypxU-noRNhsv5dW4NfTGce) makes the process pretty straight forward. Google Colab provides a GPU for free so you don't have to train your model on your own machine, which may not be possible. You can use the notebook to save the model to your Google Drive and your disk.

## Option 1: Running the model on your machine
1. Once the model is tuned, you can download it onto your machine. Clone [this repository](https://github.com/openai/gpt-2) from OpenAI.
2. Save your model into "src/models/YOURMODEL".
3. Install required packages from the requirements.txt file in the above repo.

  * IMPORTANT: Make sure your virtual environment is Python 3.

  * You will also need tensorflow (version 1.14.00) and numpy.

4. Run these commands to run the models, with and without prompts.

..* Without prompts

> python generate_unconditional_samples.py --model_name YOURMODEL

..* With prompts

> python interactive_conditional_samples.py --top_k 40 --model_name YOURMODEL
And enter your prompt and hit enter

## Option 2: Deploy as an API on AWS EC2 instance
The deployment option I used was [Cortex](https://www.cortex.dev/). It streamlineds the deployment process so you can specify the AWS resources to use in a single yaml file.

The above site contains a tutorial on how to deploy and set up the API. However, I found the steps a bit confusing, especially when you want to deploy your own tuned model.

1. Install the CLI 

> bash -c "$(curl -sS https://raw.githubusercontent.com/cortexlabs/cortex/0.15/get-cli.sh)"

2. Convert your model from the previous step to a Tensorflow model. Cortex provided a code snippet to do this, but it's buried in the .ipynb file in their sample repository. I placed this in the .py file in the depository.

3. Upload your model to S3. You can do it the quick and dirty way via the AWS console, or using the Python boto3 package (code in this repository).

4. Start the AWS cluster. I delay this step until now because it may take some time complete the previous step, and we don't want to cluster to start running and attract cost from AWS.
> cortex cluster up

5. Deploy the model.
> cortex deploy

6. Get the API endpoint with
> cortex cluster info

7. You can now use the API, wrap a web app around it, etc.



