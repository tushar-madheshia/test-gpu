import json
from flatten_json import flatten
import pandas as pd
import ast

def get_score(predicted,actual):
    if predicted and actual:
        #intersection of both actual and Predicted
        matched = len([value for value in predicted if value in actual]) if len(predicted)<len(actual) else len([value for value in actual if value in predicted])
        #matched = len(predicted.intersection(actual))
        if not matched: 
            #return all 3 scores as 0 when there is no matches
            return 0,0,0
        recall = matched/(len(actual)) # this tells % of required matches are present in the predicted 
        precision  = matched/(len(predicted))# this tells % of NOT required matches are present in the predicted
        f1_score = 2*(precision*recall)/(precision+recall) #Harmonic mean of Reacall and Precision
        return precision,recall,f1_score
    else:
        return None, None, None 
    
def dict_key_sort(dict1,dict2):
    #Sorting the dictonaries based on Keys
    dict1=json.dumps(dict1, sort_keys=True)
    dict2=json.dumps(dict2, sort_keys=True)
    return ast.literal_eval(dict1),ast.literal_eval(dict2)

def KPIs(predicted,actual,index):
    """
    INPUT:Predicted,Actual,index are manadtory values need to be passed. 
          Predicted,Actual should have imqls in valid JSON string.
          index should be passed with index of the actual and predicted sequence 
    Output: 
          For every imql field, it returns 
          value accuracy,
          key accuracy,
          N-gram identification accuracy,
          Entity Matching accuracy.
          
          where every accuracy consists of Recall, Precision and F1-score
          
    """
    #call for sorting the dictnories
    try:
        predicted,actual = dict_key_sort(predicted,actual)
        predicted = ast.literal_eval(predicted) if type(predicted)==str else predicted
        actual = ast.literal_eval(actual) if type(actual)==str else actual
    except SyntaxError as e:
        print(f"Invalid json Syntax at index {index}")
        return None
    #Taking the all keys in Predicted mql and Acutal mql [MEASURE, DIMENSION, FILTER, etc]
    KEYS = list(set(predicted.keys()).union(set(actual.keys())))
    score_dict = {i:None for i in KEYS}
    for key in KEYS: #[MEASURE, DIMENSION, FILTER, etc]
        
        #Flatten the each predicted and actual JSON 
        try:
            flat_predicted = flatten(predicted.get(key,dict()))
            flat_actual = flatten(actual.get(key,dict()))

            #Getting the all from values flattened Json
            flat_predicted_values=flat_predicted.values()
            flat_actual_values=flat_actual.values()
        except AssertionError as e:
            print(f"JSON is vaild, but not in correct format at {index}")
            return None
        
        #Replancing [] values with ""
        flat_predicted_values = ["" if i==[] else i for i in flat_predicted_values]
        flat_actual_values = ["" if i==[] else i for i in flat_actual_values]
        
        #Getting the scores for Values 
        values_precision,values_recall,values_F1 = get_score(flat_predicted_values,flat_actual_values)
        
        #Getting the scores for Keys
        keys_precision,keys_recall,keys_F1 = get_score(list(flat_predicted.keys()),list(flat_actual.keys()))
        
        #Getting the n-grams from flattened Json
        n_grams_predicted=predicted.get(key,dict()).keys()
        n_grams_actual=actual.get(key,dict()).keys()
        
        #Getting the scores for n-grams
        n_grams_precision,n_grams_recall,n_grams_F1 = get_score(list(n_grams_predicted),list(n_grams_actual))

        #Getting the entities from Json
        predicted_entities=[predicted[key][n_gram][0]["ENTITY"] for n_gram in list(n_grams_predicted)]
        actual_entities=[actual[key][n_gram][0]["ENTITY"] for n_gram in list(n_grams_actual)]
        
         #Getting the scores for entities
        entity_precision,entity_recall,entity_F1 = get_score(predicted_entities,actual_entities)

        score_dict[key] = {
                           "values":{"recall":values_recall,"precision":values_precision,"f1_score":values_F1},
                           "keys":{"recall":keys_recall,"precision":keys_precision,"f1_score":keys_F1},
                           "N-gram identification":{"recall":n_grams_recall,"precision":n_grams_precision,"f1_score":n_grams_F1},
                           "Entity Matching":{"recall":entity_recall,"precision":entity_precision,"f1_score":entity_F1}
                        } 
    return score_dict

def display_over_all_KPIs(KPI_df,KPI_col_name,field):
    field_list=list()
    for index,row in KPI_df.iterrows():
        kpi = row[KPI_col_name]
        if kpi: # we are only aggregating the the samples where KPIs were calculated
                # for rest of them we do it manual verification
            field_list.append(kpi.get(field)) #Take the KPIs only for GIVEN feild
            
            field_list1 = [j for j in field_list if j] #Remove None values.
                                                        #Here None values means not applicable
                                                        #Example: "Sales in 2022" --> 
                                                        #here KPI for "DIMENSION" is not applicable
    #Final aggregated DF initialize
    final_df = pd.DataFrame(columns=['values', 'keys', 'N-gram identification', 'Entity Matching'],index=['recall', 'precision', 'f1_score']).fillna(0)
    
    for each_field_KPI in field_list1:
        #Taking mean for all metrices 
        final_df = pd.DataFrame(each_field_KPI).fillna(0)+final_df
    final_df = final_df/len(field_list1)
    
    print(f"Over all KPI for {field} field")
    print(f"Out of {KPI_df.shape[0]} samples, {len(field_list)} are having vaild KPIs")
    print(f"Out of {len(field_list)} valid KPIS, {field} applicable for {len(field_list1)}")
    display(final_df)
    
    #print(f"Remaining {KPI_df.shape[0]-len(field_list)} having some issue while calculating individual KPIs")
    return final_df
