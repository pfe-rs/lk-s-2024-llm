# model_eval.py

import json
import model_inference
import prompts

from datetime import datetime
from phrase_extraction_evaluation import STSEvaluation
from typing import Dict, List, Union


class ModelEval:
    @staticmethod
    def get_metrics(model_inference: model_inference.ModelInferencing, text: str, label: List[str], print_steps: bool = False) -> Dict[str, Union[float, int]]:
        """
        Calculate metrics for a given text and its label using the model inference.
        Args:
            model_inference (ModelInferencing): The model inference instance.
            text (str): The input text.
            label (List[str]): The correct labels.
            print_steps (bool): Whether to print intermediate steps. Default is False.
        Returns:
            Dict[str, Union[float, int]]: The calculated metrics.
        """
        prediction = model_inference.get_multiple_phrases(text)

        if print_steps:
            print(f"Input text: {text}")
            print(f"Correct label: {label}")
            print(f"Model prompt: {prompts.make_multi_extraction(text)}")
            print(f"Model predictions: {prediction}")

        return STSEvaluation.evaluate_phrases(prediction, label, text)

    @staticmethod
    def single_sample(model_inference: model_inference.ModelInferencing, sample: Dict[str, Union[str, List[str]]]) -> Dict[str, Union[float, int]]:
        """
        Evaluate a single sample using the model inference.
        Args:
            model_inference (ModelInferencing): The model inference instance.
            sample (Dict[str, Union[str, List[str]]]): The sample to evaluate.
        Returns:
            Dict[str, Union[float, int]]: The calculated metrics for the sample.
        """
        return ModelEval.get_metrics(model_inference, sample['text'], sample['label'], print_steps=True)

    @staticmethod
    def multiple_samples(model_inference: model_inference.ModelInferencing, samples: List[Dict[str, Union[str, List[str]]]], save_file: str = "default", print_counts: bool = True) -> Dict[str, float]:
        """
        Evaluate multiple samples and save the results to a file.
        Args:
            model_inference (ModelInferencing): The model inference instance.
            samples (List[Dict[str, Union[str, List[str]]]]): The samples to evaluate.
            save_file (str): The name of the file to save results. Default is "default".
            print_counts (bool): Whether to print test counts. Default is True.
        Returns:
            Dict[str, float]: The average metrics across all samples.
        """
        file_name = save_file
        if save_file == "default":
            now = datetime.now()
            current_time_str = now.strftime("%Y-%m-%d %H:%M:%S")
            file_name = f"multi_sample_run_{current_time_str}"

        average_result = {
            'cosine': 0,
            'groundness': 0,
            'matchings': 0,
            'redundancy': 0
        }
        results = []

        for num, sample in enumerate(samples, start=1):
            if print_counts:
                print(f"Running test {num}")
            test_result = ModelEval.get_metrics(model_inference, sample['text'], sample['label'])

            for key, value in test_result.items():
                average_result[key] += value

            test_result['test_num'] = num
            results.append(test_result)

        experiment_file = {
            'prompt': prompts.make_multi_extraction("[text would go here]"),
            'results': results
        }
        if file_name != "none":
            with open(file_name + '.json', 'w') as file:
                json.dump(results, file, indent=4)

        for key in average_result.keys():
            average_result[key] /= len(samples)

        return average_result
