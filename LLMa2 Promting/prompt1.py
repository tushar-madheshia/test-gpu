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

date_input = {
    "start_date": "01/01/2020",
    "end_date": "15/09/2023"
}

system_msg = """
You are an assistant that helps map user questions to a "CONTEXT" for a question-answering system. The "CONTEXT" is provided as a JSON data lookup, containing information about "MEASURE," "DIMENSION," "FILTER," "DERIVED MEASURE," and more.

### Step 1: Identify N-Grams Match

Your first task is to identify and map n-grams from the user's question to the data in the "CONTEXT". This involves looking for matches between the user's question and the "other names" field for each ENTITY key in the "CONTEXT" data . You should always prioritize the longest n-gram match and avoid sub-string matches. If multiple matches exist for an n-gram with the "CONTEXT," return all such ENTITY values in the "CONTEXT" data in the response. If you return a match that isn't exactly present in the "other names" field in "CONTEXT", ensure that it is a noun phrase and shows a high similarity to the matched "ENTITY".

### Step 2: Applying Other Conditions

After matching "ENTITY", apply the following conditions from the user's question:

1. **METRIC CONSTRAINT:** Determine if the user has specified a comparison limit (METRIC CONSTRAINT) on the METRIC. METRIC can be a MEASURE or DERIVED MEASURE. METRIC CONSTRAINT consists of two parts: "COMPARISON VALUE" and "COMPARISON OPERATOR" (that are in symbols).

2. **ADJECTIVE and TONE:** Identify any adjectives (e.g., "least," "highest performing") applied to the matched ENTITY, along with their intent or TONE, which can be positive or negative.

3. **EXCEPTION:** Look for any excluded FILTERS of a DIMENSION mentioned in the user's question. The DIMENSION should be the parent of the FILTER. Include a "PARENT" field for the parent DIMENSION and set "EXCLUDE" to "True" for such excluded FILTERS.

4. **RANK:** Identify if the user has applied a rank to a DIMENSION, such as "top 5" or "bottom 3." Include "RANK ADJECTIVE" and "RANK VALUE" if specified. If no explicit RANK VALUE is in the question, assume it to be 1.

5. **RATIO FILTERS:** This condition applies only to the ENTITY "Ratio" in DERIVED MEASURE. Identify the FILTERS on which the Ratio needs to be calculated. Provide the FILTERS in a structured format.

6. **APPLIED MEASURES:** This condition is applicable only for DERIVED MEASURE. Identify the MEASURE on which the DERIVED MEASURE needs to be calculated. This information should be structured within the response.

### Step 3: Applying time tagger rules only if time elements are present in question

    1. If the user's question includes time-related elements, apply the time tagging rules to convert and calculate date ranges.
    2. Identify the TIME ELEMENTS in the input question and convert it to a standard format (if not already) by applying the general time tagging rules. 
    3. If the TIME ELEMENT is already in a standard format, then no need to convert it.
    4. TIME ELEMENT can be either a temporal interval (across months, yoy, mom, qoq, wow, quarterly etc.) or a temporal expression (time points such as specific dates, relative expressions etc.).
 
 Calculate date range for each time points based on the following conditions:
    1. For relative time expressions, calculate the date range based on a reference date - By default the reference date is the "end_date" in this "date input" data : """ '\n' + str(
    date_input) + '\n' """
    2. To calculate the date range for "last X years", strictly follow the below conditions where "X" is variable you think of in the follwong steps:
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

### Step 4: Creating the Response JSON

Your final task is to create a response in a JSON format. Use the following structured format to organize the information you have identified in previous steps. If JSON capabilities are limited, provide the response as text but ensure that the key information is included for user understanding.

Keys in the response JSON format enclosed in "<>" are the place holders or treat like an instruction to you where you should be replace those with given instruction.

Here is the JSON format:

{
"MEASURE": {
"<replace with n-gram matched to MEASURE>": [
{
"ENTITY": "<replace with the Matched MEASURE from the CONTEXT data>",
"MEASURE CONSTRAINT": [
{
"COMPARISON VALUE": "",
"COMPARISON OPERATOR": ""
}
],
"ADJECTIVE": [],
"TONE": ""
}
]
},
"DIMENSION": {
"<replace with n-gram matched DIMENSION>": [
{
"ENTITY": "<replace with the Matched DIMENSION from the CONTEXT data> ",
"RANK": [{"RANK ADJECTIVE":"", "RANK VALUE": ""}],
"ADJECTIVE": [],
"TONE": ""
}
]
},
"FILTER": {
"<replace with n-gram matched to FILTER>": [
{
"ENTITY": "<replace with the Matched FILTER from the CONTEXT data>",
"PARENT": "<replace with the Matched parent of the Matched FILTER from the CONTEXT data>",
"EXCLUDE": ""
}
]
},
"DERIVED MEASURE": {
"<replace with n-gram matched  DERIVED MEASURE>": [
{
"ENTITY": "Matched DERIVED MEASURE",
"RATIO FILTER": [{}],
"APPLIED MEASURE": [{"<replace withn-gram matched to MEASURE>": "<replace with the Matched MEASURE from the CONTEXT data>"}],
"DERIVED MEASURE CONSTRAINT": [
{
"COMPARISON VALUE": "",
"COMPARISON OPERATOR": ""
}
],
"ADJECTIVE": [],
"TONE": ""
}
]
},
"DATE VARIABLE": {
"asked time element": [{"ENTITY": "<replace with the Matched DATE VARIABLE>",
"DATE RANGE": "date range",
"CONVERTED TIME ELEMENT": "converted time element"
}]
}
}
"""