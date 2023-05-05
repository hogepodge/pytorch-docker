from label_studio_ml.model import LabelStudioMLBase

import torch
import torch.nn as nn
import torchtext
 
class SentimentModel(LabelStudioMLBase):
    def __init__(self, **kwargs):
        super(SentimentModel, self).__init__(**kwargs)

        self.sentiment_model = Sentiment_CNN()
        self.sentiment_model.load_state_dict(torch.load('data/cnn.pt'))

        self.label_map = {
            1: "Positive",
            0: "Negative"}

    def predict(self, tasks, **kwargs):
        predictions = []
        # Get annotation tag first, and extract from_name/to_name keys from the labeling config
        #  to make predictions
        from_name, schema = list(self.parsed_label_config.items())[0]
        to_name = schema['to_name'][0]
        data_name = schema['inputs'][0]['value']
        print(self.parsed_label_config.items())
        for task in tasks:
            # load the data and make a prediction with the model
            text = task['data'][data_name]
            predicted_class, predicted_prob = self.sentiment_model.predict_sentiment(text)
            print("%s\nprediction: %s probability: %s" % (text, predicted_class, predicted_prob))

            # for each task, return classification results in the form of "choices" pre-annotations
            predictions.append({
                'result': [{
                    'from_name': from_name,
                    'to_name': to_name,
                    'type': 'choices',
                    'value': {'choices': [self.label_map[predicted_class]]},
                    # optionally you can include prediction scores that you can use to sort the tasks
                    # and do active learning
                }],
                'score': float(predicted_prob)
            })
        return predictions

class Sentiment_CNN(nn.Module):
    def __init__(self):
        super().__init__()

        # tokenizer setup
        self.tokenizer = torchtext.data.utils.get_tokenizer('basic_english')

        # vocabulary parameters
        self.vocab = torch.load('data/vocab_obj.pth')
        vocab_size = len(self.vocab)
        self.pad_index = self.vocab['<pad>']

        # language space parameters
        embedding_dim=300
        output_dim=2

        # cnn parameters
        n_filters=100
        filter_sizes=[3,5,7]
        dropout_rate=0.25
        self.min_length = max(filter_sizes)

        # model setup
        self.embedding = nn.Embedding(vocab_size, embedding_dim, padding_idx=self.pad_index)
        self.convs = nn.ModuleList([nn.Conv1d(embedding_dim, 
                                              n_filters, 
                                              filter_size) 
                                    for filter_size in filter_sizes])
        self.fc = nn.Linear(len(filter_sizes) * n_filters, output_dim)
        self.dropout = nn.Dropout(dropout_rate)

        self.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        
    def forward(self, ids):
        embedded = self.dropout(self.embedding(ids))
        embedded = embedded.permute(0,2,1)
        conved = [torch.relu(conv(embedded)) for conv in self.convs]
        pooled = [conv.max(dim=-1).values for conv in conved]
        cat = self.dropout(torch.cat(pooled, dim=-1))
        prediction = self.fc(cat)
        return prediction

    def predict_sentiment(self,text):
        tokens = self.tokenizer(text)
        ids = [self.vocab[t] for t in tokens]
        if len(ids) < self.min_length:
            ids += [self.pad_index] * (self.min_length - len(ids))
        tensor = torch.LongTensor(ids).unsqueeze(dim=0).to(self.device)
        prediction = self(tensor).squeeze(dim=0)
        probability = torch.softmax(prediction, dim=-1)
        predicted_class = prediction.argmax(dim=-1).item()
        predicted_probability = probability[predicted_class].item()
        return predicted_class, predicted_probability
