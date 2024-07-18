# Function that converts sample from dataset into metrics on that sample
from phrase_extraction_evaluation import STSEvaluation
import model_inference
from datetime import datetime
import prompts
import json

class Model_eval():
    @staticmethod
    def get_metrics(model_inference,text,label,print_steps=False):
        prediction=model_inference.get_multiple_phrases(text)
        
        if print_steps:
            print(f"Input text: {text}")
            print(f"Correct label: {label}")
            print(f"Model prompt: {prompts.make_multi_extraction(text)}")
            print(f"Model predictions: {label}")
        return STSEvaluation.evaluate_phrases(prediction,label,text)
    
    @staticmethod
    def single_sample(model_inference, sample):
        return Model_eval.get_metrics(model_inference, sample['text'], sample['label'], print_steps=True)
    
    @staticmethod
    def multiple_samples(model_inference, samples, save_file="default", print_counts=True):
        file_name=save_file
        
        if save_file=="default":
            now = datetime.now()
            current_time_str = now.strftime("%Y-%m-%d %H:%M:%S")
            file_name="multi_sample_run_"+current_time_str
        
        results=[]

        cosine=0
        ground=0
        match=0
        red=0
        num=0
        for sample in samples:
            num+=1
            if print_counts:
                print(f"Running test {num}")
            #print(test['text'])
            test_result=Model_eval.get_metrics(model_inference, sample['text'], sample['label'])

            cosine+=test_result['cosine']
            match+=test_result['matchings']
            ground+=test_result['groundness']
            red+=test_result['redundancy']

            test_result['test_num'] = num
            results.append(test_result)

        experiment_file={
            'prompt': prompts.make_multi_extraction("[text would go here]"),
            'results': results
        }
        if file_name != "none":                  
            with open(file_name+'.json', 'w') as file:
                 json.dump(results, file, indent=4)

        cosine/=num
        match/=num
        ground/=num
        red/=num
                  
        average_result={
            'cosine': cosine,
            'matchings': match,
            'groundness': ground,
            'redundancy': red
        }
        
        return average_result