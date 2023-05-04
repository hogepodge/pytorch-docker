from label_studio_ml.model import LabelStudioMLBase

class SentimentModel(LabelStudioMLBase):
    def __init__(self, **kwargs):
        super(SentimentModel, self).__init__(**kwargs)

    def predict(self, tasks, **kwargs):
        predictions = []
        # Get annotation tag first, and extract from_name/to_name keys from the labeling config
        #  to make predictions
        from_name, schema = list(self.parsed_label_config.items())[0]
        to_name = schema['to_name'][0]
        for task in tasks:
            # for each task, return classification results in the form of "choices" pre-annotations
            predictions.append({
                'result': [{
                    'from_name': from_name,
                    'to_name': to_name,
                    'type': 'choices',
                    'value': {'choices': ['Positive']}
                }],
                # optionally you can include prediction scores that you can use to sort the tasks and do active learning
                'score': 0.987
            })
        return predictions
