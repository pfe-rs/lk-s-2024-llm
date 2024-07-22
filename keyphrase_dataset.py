import json
import os

class KeyphraseDataset:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(KeyphraseDataset, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        if not hasattr(self, 'initialized'): 
            if not os.path.isfile("keyphrase_set.json"):
                KeyphraseDataset.download_set()
            
            with open("keyphrase_set.json", 'r') as file:
                data = json.load(file)
                self.train_set=data['train']
                self.validation_set=data['validation']
                self.test_set=data['test']

            self.initialized = True

    @staticmethod
    def download_set():
        dataset = load_dataset("midas/kptimes", "raw")
        train_set = KeyphraseDataset.extract_dataset(dataset["train"])
        validation_set = KeyphraseDataset.extract_dataset(dataset["validation"])
        test_set = KeyphraseDataset.extract_dataset(dataset["test"])

        combined_set ={
            'train': train_set,
            'validation': validation_set,
            'test': test_set
        }

        with open('keyphrase_set.json', 'w') as file:
            json.dump(combined_set, file, indent=4)


    @staticmethod
    def check_length(text):
        return len(text) >= 400 and len(text) <= 2000
    
    @staticmethod
    def extract_dataset(dataset): 
        new_set = []
        for i in range(len(dataset)):
            sample = dataset[i] 
            text = " ".join(sample["document"])
            if not KeyphraseDataset.check_length(text):
                continue
            label = sample["extractive_keyphrases"] + sample["abstractive_keyphrases"] 
            if len(label)<2:
                continue
            new_set.append({
                'text': text,
                'label': label
            })
        return new_set
    
    def get_samples(self, amount=50, type="train"):
        if type == "train":
            full_set = self.train_set
        elif type == "validation":
            full_set = self.validation_set
        else:
            full_set = self.test_set
        
        assert len(full_set) >= amount, "Not enough samples in the dataset"

        return full_set[:amount]