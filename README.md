

> Happy Sunday Melbourne! I’m here to spoon a delicious home-made Guacamole and Butternut Smoked Salmon.

> Fried Croissant with sourdoughnuts and creamy pancake batter. My favourite breakfast in New York City and @eriqulotopos some stupid puns.

> Available for breakfast, lunch and dinner just like Puget Sound’s Puget Sound Cafe. The buns at Somerbay South Burger & Chips are also good, especially the coconut and dill flavour.


# AI Food Blog Writer
Train an AI (OpenAI's GPT-2 model) to write food blog entries. The above are samples written by the AI after training.

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

  * Without prompts

> python generate_unconditional_samples.py --model_name YOURMODEL

  * With prompts

> python interactive_conditional_samples.py --top_k 40 --model_name YOURMODEL
And enter your prompt and hit enter

## Option 2: Deploy as an API on an AWS EC2 instance
The deployment option I used was [Cortex](https://www.cortex.dev/). It streamlineds the deployment process so you can specify the AWS resources to use in a single yaml file, and it will handle VPC and Load Balancer for you as well.

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

## Sample output
### Without prompts
> The face of street food - from the contemporary Bondi cafe @scarlatinaustralia #smashedmeat #relishfruit #streetfood #mofoifelbowl #sydneycafe #localseatery #sydneyeats #breadandbutter #cookiesandcream #sausageroll #dessert #omelette #plateau #foodlovers #sydneyblogger #foodlover #umassdrinks #cheapeats #sydneyfoodie #sydneyfoodblogger #sydneyfoodblogger #yummo #petebondi

> The combination of grilled beef and lime, fresh lime slaw, mustard seeds, zucchini flowers, fresh lime, guacamole, leek and kim chi soft serve. Perfect epic meal #meturbalpourri #tcbd #sydneybars #sydneyeats #brewedchampagne #sydneyfood #sausageroll #menwithcuisines #sydneyfoodblogger #sydneyfoodblog #petecbarracuda

> A Danish outlandish pop-up pub hidden under the bridge, bar or bridge northwest of Sydney. When dining out at this bar/bistro, you know you’ll end up dining off the menu. Don’t judge by the menu when you can order a greasy caffelato pizza from the menu. I shared a handful of the toppings the other night so if you haven’t had them yet, I’ll share them in a later post #saint_daneeagle #fcba #barsons #bistro #edoublewine #publife #peninsulife #barbancake #borrancafe #sydneybars #sydneyeats #sydneyfood #steak #skewers #fries #ncafe #foodlovers

> Hit the road for me - pouring the area has paid off. Nine years later and I can say with absolute certainty this place is still one of Sydney’s best road spots. You can swipe swipe - you can swipe. That is all for this sunny Friday morning #medoccarroll #sydneycbd #spokeown #officialindianfood #indianrestaurant #centralparkdistillery #sydneyrestaurants #sydneyeats #sydneyfood #ligands #sushi #petecarroll

> Lemon and Nutella Schnitzel Mud shot - pasta shots from one of my favourite Italian food venues @flatheadbaros in Fitzroy 
Delicious Ascot but for me the real standout is the coffee shot - bring a camera baby! #flatheadbaros #sydneycbd #lisestate #ilovemudshot #sydneycoffee #sydneyfood #granola #sydneyfoodblogger #skiing #sydneyfoodblogger #coffeetime #dinner #tacotphotography #foodphotography #invited

> One of my favourite places for good food photography is the The Kingfish Cafe in Thornbush. An eclectic bar/restaurant just outside the mainstream Sydney food scene. An absolute must visit place for foodists and locals alike. Try as this cafe might not look a view from the windows the food on display looks absolutely stunning!  #borrusco1 #sutherland #aldistillery #sydneyfood #sydneyfoodblogger #cocktails #invited #chocolate #sunflowerapples #sydneyfoodshare #scones #blacksesame #foodpics


### With prompts
#### Prompt: Burger

> I had a blast on Tuesday morning devouring the classic Pork and Prawn Toast from the very cool @theburgercollectiveapp.

> What an amazing food experience and @theburgencecollectiveau
My favorite fried chicken sandwich from the @sydneyburgercollectiveau is finally here!!
#burger #burgersofmelbourne #melbourneburgers #sydneyburgers #sydneyfood #

> A beautiful breakfast dish for the weather. Don’t get me started on the potato fried chicken in blue jeans @bishopsgatemarket #melbournefood #melbournefoodblogger #melhotornot

Somehow the "burger" prompt makes the AI think "fried chicken"!




