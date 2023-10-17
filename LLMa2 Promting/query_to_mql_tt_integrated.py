import openai
import os
import json
import traceback
from datetime import datetime

openai.api_type = "azure"
openai.api_base = os.getenv("OPENAI_API_BASE")
openai.api_version = "2023-03-15-preview"
openai.api_key = os.getenv("OPENAI_API_KEY")


def postprocess(inp):
    try:
        res = json.loads(inp[inp.find('{'):inp.rfind('}') + 1].replace("'", '"'))

        for key, val in res.items():
            for key1 in val:
                valtemp = []
                for each in val[key1]:
                    temp = {k: v for k, v in each.items() if v}
                    if temp:
                        valtemp.append(temp)
                val[key1] = valtemp
            val = {k: v for k, v in val.items() if v}
        res = {k: v for k, v in res.items() if v}
    except:
        print(traceback.print_exc())
        res = inp
    return res


context = {
    "MEASURE": [{"ENTITY": "Discount", "other names": ["discount", "discount rate", "discount value", "deduction"]},
                {"ENTITY": "Purchase Vol", "other names": ["purchase", "purchase value", "purchase model"]},
                {"ENTITY": "Quantity", "other names": ["quantity", "volume"]},
                {"ENTITY": "Sales", "other names": ["sales", "sale"]}],
    "DIMENSION": [{"ENTITY": "Sub-Category", "other names": ["sub-category", "sub category", "categories", "section"]},
                  {"ENTITY": "Segment", "other names": ["segment", "segments", "units", "divisions"]},
                  {"ENTITY": "Parts", "other names": ["parts", "part", "section", "divisions"]},
                  {"ENTITY": "Country", "other names": ["country", "countries"]}],
    "FILTER": [{"ENTITY": "Consumer", "other names": ["consumers", "consumer"], "parent": "Segment"},
               {"ENTITY": "Phone", "other names": ["phone", "phones", "mobile phones"], "parent": "Sub-Category"},
               {"ENTITY": "Binder", "other names": ["binders", "binder"], "parent": "Sub-Category"},
               {"ENTITY": "Corporate", "other names": ["corporates", "corporate"], "parent": "Segment"},
               {"ENTITY": "India", "other names": ["india"], "parent": "Country"},
               {"ENTITY": "Dubai", "other names": ["dubai"], "parent": "Country"}],
    "DERIVED MEASURE": [{"ENTITY": "Ratio",
                         "other names": ["ratio", "share", "contribution", "percentage", "proportion", "contributing"]},
                        {"ENTITY": "Why", "other names": ["why", "cause of", "reason for", "diagnose"]},
                        {"ENTITY": "contribution_to_growth",
                         "other names": ["contribution to growth", "growth", "grown"]},
                        {"ENTITY": "kda_transactional",
                         "other names": ["kda", "key drivers", "key driver", "drivers", "driver"]},
                        {"ENTITY": "Growth Rate", "other names": ["growth rate", "growth", "grown"]},
                        {"ENTITY": "correlation",
                         "other names": ["associate", "associated", "association", "associations", "correlate",
                                         "correlated",
                                         "correlation", "correlations", "relate", "related", "relation", "relations",
                                         "relationship",
                                         "relationships"]}
                        ],
    "DATE VARIABLE": [
        {"ENTITY": "Order Date", "other names": ["order date", "date", "trend", "time", "when", "mom", "yoy"]}]
}

question = input("Enter the question: ")
# while question != "exit":
# questions = ["discount of categories in corporate", "top 5 segments basis discount", "when was quantity greater than 10k for phone", "quantity across category except phone in corporate", "binder share of discount by consumer", "segment with lesser phone", "what is purchase across segments", "discount rate of phone and binders", "discount rate of overall sub-category in corporate", "segments with discount rate greater than 100k", "category with discount rate greater than 10k and quantity less than 2k", "which category contributing to 5% of discount", "top 5 segments basis discount", "top 5 segments and bottom 3 category by quantity", "which segment has highest purchase", "top 5 and bottom 3 segments basis puchase", "discount of segments except consumer", "quantity across category except phone in corporate", "discount rate for category except phone and binder in corporate", "in corporate what is the quantity for category except phone and binder", "quantity across segments except phone for consumer", "binder share of discount by consumer", "binder and phone share basis sales for corporate", "in corporate share of phone and binder basis discount",
# "phone to binder ratio of discount in corporate", "why has discount of phones drop", "when was sales > 50bn", "in corporate who was the winner basis discount for phone", "list of under performing segments", "when was purchase highest", "list of segments and categories", "show me the list of countries", "trend share of sales of phones", "trend of quantity", "how many segments are there in dubai", "how many categories are there basis sales in india"]
# questions = ["which are the top 10 segments in the basis of discounts", "top 10 segments in the basis of discounts", "which are the top 10 segments basis discounts"]
# for question in questions:
date_input = {
    "start_date": "01/01/2020",
    "end_date": "15/09/2023"
}
# questions = ["what is purchase across segments", "discount rate of phone and binders", "discount rate of overall sub-category in corporate", "maximum sales of phone for consumer segment", "which segment has highest purchase", "forecast of sales", "top 2 segments basis discount", "quantity across segments except consumer", "binder share of discount by consumer", "binder and phone share basis sales for corporate", "in corporate, share of phone and binder basis discount", "phone to binder ratio of discount in corporate", "segments with discount rate greater than 100k", "which category contributing to 5% of discount", "segments with sales < 10bn", "category with discount rate greater than 10k and quantity less than 2k", "why did discount of phones drop", "correlation of sales and purchase for phone", "what will be the sales in q1 24", "sales in q1 and q2 2021", "how many segments contributing to growth of sales in p3m vs pp", "how has sales trended in first week of 2021", "what will be sales in 1st 5 days of 2024", "monthly sales of segments in 2021", "sales and purchase across yoy", "show me the 2 top segments basis sales", "top 5 and bottom 5 segment by discount", "top 2 segments and bottom 3 sub-category basis quantity", "quantity across segments except consumer for phone", "quantity across segments except consumer and corporate for phone", "top 5 segments with discount greater than 10k and bottom 2 sub category", "in corporate share of phone and binder basis discount", "list of under performing segments", "when was the first time sales of region was 0", "sales of segments from beginning", "sales in 20/01/2020", "sales in 01.23", "sales in last one and half years", "trend of sales in UK now", "sales in q123 vs pp", "sales in the week of 01 March 2022", "top most selling segments in 2020 vs 2021", "what will be the sales in q1 24", "sales in q1 and q2 2021", "how many segments contributing to growth of sales in p3m vs pp", "how has sales trended in first week of 2021", "what will be sales in 1st 5 days of 2024", "monthly sales of segments in 2021", "sales and purchase across yoy", "sales in 20/01/2020", "sales in 01.23", "sales in last one and half years", "trend of sales in UK now", "sales in q123 vs pp", "sales in the week of 01 March 2022", "top most selling segments in 2020 vs 2021", "show me the 2 top segments basis sales", "top 2 and bottom 3 segments by sales", "top 2 segments and bottom 3 sub-category basis quantity", "quantity across segments except consumer and corporate for phone", "in corporate share of phone and binder basis discount", "list of under performing segments", "when was the first time sales of segments was 0", "sales of segments from beginning", "sales in 20/01/2020", "sales in 01.23", "sales in last one and half years", "trend of sales in dubai now", "sales in q123 vs pp", "sales in the week of 01 March 2022", "top most selling segments in 2020 vs 2021"]
# questions = ["what will be the sales in q1 24", "sales in q1 and q2 2021", "how many segments contributing to growth of sales in p3m vs pp", "how has sales trended in first week of 2021", "what will be sales in 1st 5 days of 2024", "monthly sales of segments in 2021", "sales and purchase across yoy", "sales in 20/01/2020", "sales in 01.23", "sales in last one and half years", "trend of sales in UK now", "sales in q123 vs pp", "sales in the week of 01 March 2022", "top most selling segments in 2020 vs 2021", "show me the 2 top segments basis sales", "top 2 and bottom 3 segments by sales", "top 2 segments and bottom 3 sub-category basis quantity", "quantity across segments except consumer and corporate for phone", "in corporate share of phone and binder basis discount", "list of under performing segments", "when was the first time sales of segments was 0", "sales of segments from beginning", "sales in 20/01/2020", "sales in 01.23", "sales in last one and half years", "trend of sales in dubai now", "sales in q123 vs pp", "sales in the week of 01 March 2022", "top most selling segments in 2020 vs 2021"]
# questions = ["show me the 2 top segments basis sales", "top 2 and bottom 3 segments by sales", "top 2 segments and bottom 3 sub-category basis quantity", "quantity across segments except consumer and corporate for phone", "in corporate share of phone and binder basis discount", "list of under performing segments", "when was the first time sales of segments was 0", "sales of segments from beginning", "sales in 20/01/2020", "sales in 01.23", "sales in last one and half years", "trend of sales in dubai now", "sales in q123 vs pp", "sales in the week of 01 March 2022", "top most selling segments in 2020 vs 2021"]
# questions = ["sales in p3m", "sales in p4m", "sales in p3m vs p6m", "sales in p3m", "sales in 2021 vs 2022", "sales in first monday of 2022", "sales in ytd", "sales in ytd vs ya", "sales in mtd", "sales in ytd", "sales in last year", "sales in last 2 years", "sales in last month", "sales in last 3 months", "sales in previous month", "in last 1.5 years, what was sales", "sales in 3rd quarter of 2022", "sales in q1 vs q2 of 2023", "sales in q-1 2021", "sales in l3m vs p12m", "sales in rolling year", "why sales changed in last 2 weeks of aug 2021", "sales in q-1 2020", "sales in first quarter 2021", "sales in 1st quarter", "sales in q1 and q2 2021", "sales in last 2 month", "sales in current month", "why sales changed in last 2 quarters of 2020", "sales in 2023 jan", "what will be the sales of milo in next quarter", "sales in this year", "sales in FY 2020", "sales in past 2 years", "what is the sales 1 year ago", "which are top 2 brands in this quarter", "what is the profit of horlicks in quarter 2 this year", "Profit of milo in current week", "what will be sales in 1st 5 days of 2024", "sales between jan 2021 and mar 2021", "sales in mar 2020 vs aug 2020", "why sales changed in last 2 weeks of aug 2021", "trend of sales in past week", "sales in previous year", "sales in the rolling year", "sales in week 2 of this month", "sales in week 1 of 2022", "sales from 1st jan 2021 to 31st may 2022", "sales in last month of previous year", "sales in this month vs last month", "sales in p3m", "sales in pp", "sales in p3m vs pp", "sales in q1 23 vs pp", "sales in yoy", "sales in 30.03.23", "sales in 30.02.23", "sales in feb 30", "sales in feb 24", "sales in feb 21", "what will be thw sales in feb 24", "sales in ytd", "sales in 01.23", "sales in 01/23", "sales from beginning", "sales in last 1.5 years", "sales in last one and half years", "trend of sales in UK now", "sales in 20/01/2020", "sales in the week of 01 March 2022", "sales from inception", "sales from starting", "sales in q123 vs pp", "sales of all time"]
while question != "exit":
    # for question in questions:
    system_msg = """You are an assistant that helps to map the user question to the context for a question answering system.
     You might also need to act as a time tagger expert to convert the date elements present in the question to a standard format and to find possible date ranges for the same.
    Step 1: Identify the n-grams match between question and context
    Map the n-gram or their lemma or their inflections from the question with the 'other names' in the passed context.
    Always consider the longest n-gram match, not the sub-string.
    If there are multiple matches for an n-gram with context, return all such ENTITY in response.
    If you are returning any match which is not exactly present with the 'other names', make sure that it is a noun phrase and there is a high similarity between the match and the matched "ENTITY". 
    Step 2: Applying other conditions
    Once the match is identified, next step is to identify other conditions from user question and apply it to the identified matches.
    Refer to the following statements to understand about different types of conditions to be applied:
		1. METRIC CONSTRAINT : METRIC can be MEASURE or DERIVED MEASURE. User is asking for a comparison limit to be applied on the METRIC. It has two parts: "COMPARISON VALUE" is the value applied on a METRIC and "COMPARSION OPERATOR" is the operator (in symbols) applied between METRIC and COMPARISON VALUE.
		2. ADJECTIVE and TONE : Identify the adjectives (like least, highest performing etc.) applied on the matched ENTITY. TONE is the intent of adjective and it can be postive or negative.
		3. EXCEPTION : Excluded FILTER of a DIMENSION asked in question if any. DIMENSION should be the parent of the FILTER. Add a key "EXCLUDE" for such excluded FILTERS and set the value as "True" in the response.
		4. RANK : Rank applied on a DIMENSION if any like top 5, bottom 3 etc. It has two parts: "RANK ADJECTIVE", the adjective like top, bottom etc. and "RANK VALUE", a number that comes along with the RANK ADJECTIVE, immediately before or after. If there is no explicit RANK VALUE in question, make it as 1. Based on the meaning of the RANK ADJECTIVE, make it as either top or bottom.
		5. RATIO FILTERS : This is applicable only for ENTITY "Ratio" in DERIVED MEASURE. Identify the FILTER on which Ratio needs to be calculated. Example 1: Question: bike share of sales in area, (where ENTITY of 'bike' is 'Bikes'), RATIO FILTERS = [{'bike': 'Bikes'}]. Example 2: Question: in area, share of bike and cycle basis sales, (where ENTITY of 'Bike' is 'Bikes' and 'cycle' is 'Cycle') RATIO FILTERS = [{'bike': 'Bikes', 'cycle': 'Cycles'}]. If there are no matched FILTERS, then keep RATIO FILTERS = []"
        6. APPLIED MEASURES: This is applicable only for DERVIED MEASURE. Identify the MEASURE on which the DERIVED MEASURE needs to be calculated. 
		
		Step 3: Applying time tagger rules only if time elements are present in question
		
		Identify the TIME ELEMENTS in the input question and convert it to a standard format (if not already) by applying the general time tagging rules. If the TIME ELEMENT is already in a standard format, then no need to convert it.
        TIME ELEMENT can be either a temporal interval (across months, yoy, mom, qoq, wow, quarterly etc.) or a temporal expression (time points such as specific dates, relative expressions etc.).
        Calculate date range for each time points based on the following conditions:
        1. For relative time expressions, calculate the date range based on a reference date - By default the reference date is the end_date in date input: """ '\n' + str(
        date_input) + '\n' """
        2. To calculate the date range for "last X years", strictly follow the below conditions:
                For "last 1 year", consider exactly one year before the reference year and set start date as January 1 and end date as Decemebr 31 of that year.
                For "last X years", where X is greater than 1, consider starting year = (reference year - X+1) and set start date as January 1 of starting year and end date as the reference date.
        3. To calculate the date range for "last X months", strictly follow the below conditions:
                Consider the reference month as the month in reference date
                For "last 1 month", consider exactly one month before the reference month and set start date as first day and end date as last day of that month .
                For "last X months", where X is greater than 1, consider starting month = (reference month - X+1) and set start date as first day of starting month and end date as the reference date. (Example: if reference date is 14/09/2022, then last 3 months = 01/07/2022 - 14/09/2022)
        4. To calculate the date range for "last X quarters", strictly follow the below conditions:
                For "last 1 quarter", consider exactly one quarter before the reference quarter and set start date as first day and end date as last day of that quarter .
                For "last X quarter", where X is greater than 1, consider starting quarter = (reference quarter - X+1) and set start date as first day of starting quarter and end date as the reference date.
        5. To calculate the date range for "last X weeks", strictly follow the below conditions:
                For "last 1 week", consider exactly one week before the reference week and set start date as Monday and end date as Sunday of that week .
                For "last X weeks", where X is greater than 1, consider starting week = (reference week - X+1) and set start date as Monday of starting week and end date as the reference date.
        6. Provide the date range of each time point in start date - end date format always.
        
		Step 4: Creating the response JSON
		Strictly return the response in the exact same JSON format as follows. 
		Fill the information identified from above steps in the JSON. 
		The keys mentioned in upper case in the response are constant.
		Return only if match is found from the context and non empty values are present
		{
			"MEASURE": {
				"n-gram matched to MEASURE": [
					{
						"ENTITY": "Matched MEASURE",
						"MEASURE CONSTRAINT": [
							{
								"COMPARISON VALUE": "",
								"COMPARSION OPERATOR": ""
							}
						],
						"ADJECTIVE": [],
						"TONE": ""
					}
				]
			},
			"DIMENSION": {
				"n-gram matched to DIMENSION": [
					{
						"ENTITY": "Matched DIMENSION",
						"RANK": [{"RANK ADJECTIVE":"", "RANK VALUE": ""}],
						"ADJECTIVE": [],
						"TONE": ""
					}
				]
			},
			"FILTER": {
				"n-gram matched to FILTER": [
					{
						"ENTITY": "Matched FILTER",
						"PARENT": "parent of the Matched FILTER",
						"EXCLUDE": ""
					}
				]
			},
			"DERIVED MEASURE": {
				"n-gram matched to DERIVED MEASURE": [
					{
						"ENTITY": "Matched DERIVED MEASURE",
						"RATIO FILTER": [{}],
						"APPLIED MEASURE": [{"n-gram matched to MEASURE": Matched MEASURE}],
						"DERIVED MEASURE CONSTRAINT": [
							{
								"COMPARISON VALUE": "",
								"COMPARSION OPERATOR": ""
							}
						],
						"ADJECTIVE": [],
						"TONE": ""
					}
				]
			},
			"DATE VARIABLE": {
				"asked time element": [{"ENTITY": "Matched DATE VARIABLE"
					"DATE RANGE": "date range",
					"CONVERTED TIME ELEMENT": "converted time element"
					}]
			}
		}
        
        Provide reasoning
		"""
    user_msg = "Based on the following context:\n" + str(
        context) + "\n return a response for the question:\n" + question + "\n"
    start = datetime.now()
    completion = openai.ChatCompletion.create(
        engine="lumin-rnd-gpt-4-32k",
        temperature=0.0,
        messages=[{"role": "system", "content": system_msg}, {"role": "user", "content": user_msg}]
    )
    end = datetime.now()
    print("question: " + question)
    # resp_ = postprocess(completion['choices'][0]['message']['content'])
    # print(json.dumps(resp_, sort_keys=True, indent=4))
    print(completion['choices'][0]['message']['content'])
    # usage = completion['usage']
    # total_tokens = usage['total_tokens']
    # cost = usage['total_tokens'] / 1000 * 0.06
    # print("prompt tokens: ", usage["prompt_tokens"])
    # print("completion tokens: ", usage["completion_tokens"])
    # print("total tokens: ", total_tokens)
    # print("cost: ", cost)
    # print("total time taken: ", (end-start).total_seconds())
    question = input("Enter the question: ")
