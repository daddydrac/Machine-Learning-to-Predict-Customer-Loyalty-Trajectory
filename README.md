# How loyal is your customer?
Machine learning is crucial to unveil the realities of how consumers shop with a core focus on Millennials and younger consumers in particular. Over two-fifths (45%) of consumers admit to being less loyal to brands when compared to a year ago, and these same consumers are quicker to abandon companies that do not meet their expectations. (Loyalty is an internal  state, that can not be directly observed and measured, but can be inferred probabilistically).

Expanding on these realities, artifical intelligence for loyalty identified that 76 percent of shoppers report that it is now easier than ever to take their business elsewhere (whether online or offline), with many of these consumers doing so based on their shopping experience alone. This reality – whether you like it or not – reinforces the importance of how consumers do not just want to be sold something, but rather appreciate the entire shopping experience of buying something. Fortunately, resources to help merchants do this both effectively and with entertaining value to consumers is now easier than ever – but it takes retailers savvy enough to acknowledge this to truly see the impact it can make on their brands.

To help your own brand strengthen its understanding of consumers and their unique preferences in today’s crowded and competitive commerce landscape, using ML for Loyalty you can expect to gain insight on:

* How to better understand the attitudes, behaviors and needs of younger shoppers – including what characteristics make them the ‘disloyal’ generation
* Ways to gain insight into what millennials hate most about ecommerce shopping, including what will alienate or cause younger shoppers to leave negative feedback, resulting in lost sales and market share
* Why seamless experiences are vital to getting millennials on board with your brand and what technologies can help to capture brand loyalty
* What you can do to provide experiences in line with millennial expectations that could result in huge opportunities for increased wallet capture
* <strong>Industry wide PDF report on "Loyal, NOT Loyal" is included in this repo to show you how this codebase delivers real business value</strong>
 
Millennials hold a tremendous influence among consumers and thus, it’s vital to keep their attention. Their needs, behaviors and expectations are unlike their older peers and as a result, retailers and brands alike need to understand how to better support them. Loyalty – after all – is the key to retaining dollars among consumers and with younger generations increasingly having more disposable dollars to spend, these are consumers too important not to understand.

#### Example Problem to solve
Predict which shoppers that responded to a rebate coupon on a specific period, would become repeat buyers of that product. The given dataset was a nearly 1G dataset with one year history of transactions for each shopper.

Download the data - [Kaggle, Loyal Customer Prediction](https://inclass.kaggle.com/c/loyal-customer-prediction) 

Create good features from the dataset of transactions as well as classification, which was then based on these features, and was a blend of various models:
* Extra Trees Classifier (scikit-learn)
* Gradient Boosting Classifier (scikit-learn)
* Gradient Boosting Classifier with Linear models as base estimators (xgboost)
* Quantile Regression (vowpal wabbit)

These models were then blended again using Gradient Boosting, trained on a holdout set of the training data.

## Setup

This submission requires an installation of xgboost, vowpal wabbit, pandas, numpy and scikit-learn

* Download the competion data (*user_info.csv*, *user_log.csv*, *train_label.csv*, *test_label.csv*) and put it in the folder "data"
* Run *gen_features.py* to create the features files *train.csv* and *test.csv*
* Run *gen_result.py* to create the ML output


