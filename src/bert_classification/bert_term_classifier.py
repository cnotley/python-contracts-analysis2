import torch
from transformers import BertTokenizer, BertForSequenceClassification, AdamW, get_linear_schedule_with_warmup
from torch.utils.data import DataLoader, TensorDataset, random_split
import numpy as np
import random
import time

class BERTTermClassifier:
    def __init__(self, model_name='bert-base-uncased', num_labels=2, batch_size=32, lr=2e-5):
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.tokenizer = BertTokenizer.from_pretrained(model_name)
        self.model = BertForSequenceClassification.from_pretrained(model_name, num_labels=num_labels)
        self.model.to(self.device)
        self.batch_size = batch_size
        self.lr = lr

    def encode_data(self, terms, labels=None):
        input_ids = []
        attention_masks = []

        for term in terms:
            encoded_dict = self.tokenizer.encode_plus(
                term, add_special_tokens=True, max_length=64, pad_to_max_length=True,
                return_attention_mask=True, return_tensors='pt'
            )
            input_ids.append(encoded_dict['input_ids'])
            attention_masks.append(encoded_dict['attention_mask'])

        input_ids = torch.cat(input_ids, dim=0)
        attention_masks = torch.cat(attention_masks, dim=0)
        labels = torch.tensor(labels) if labels is not None else None

        return input_ids, attention_masks, labels

    def create_data_loader(self, input_ids, attention_masks, labels=None):
        data = TensorDataset(input_ids, attention_masks, labels) if labels is not None else TensorDataset(input_ids, attention_masks)
        data_loader = DataLoader(data, batch_size=self.batch_size)
        return data_loader

    def train(self, terms, labels, epochs=4):
        input_ids, attention_masks, labels = self.encode_data(terms, labels)

        # Creating the dataset from the encoded data
        dataset = TensorDataset(input_ids, attention_masks, labels)
        train_size = int(0.9 * len(dataset))
        val_size = len(dataset) - train_size
        train_dataset, val_dataset = random_split(dataset, [train_size, val_size])

        train_dataloader = self.create_data_loader(train_dataset[0], train_dataset[1], train_dataset[2])
        validation_dataloader = self.create_data_loader(val_dataset[0], val_dataset[1], val_dataset[2])

        optimizer = AdamW(self.model.parameters(), lr=self.lr, eps=1e-8)
        total_steps = len(train_dataloader) * epochs
        scheduler = get_linear_schedule_with_warmup(optimizer, num_warmup_steps=0, num_training_steps=total_steps)

        # Training Loop
        for epoch_i in range(0, epochs):
            print('======== Epoch {:} / {:} ========'.format(epoch_i + 1, epochs))
            total_train_loss = 0
            self.model.train()

            for step, batch in enumerate(train_dataloader):
                b_input_ids = batch[0].to(self.device)
                b_input_mask = batch[1].to(self.device)
                b_labels = batch[2].to(self.device)

                self.model.zero_grad()
                outputs = self.model(b_input_ids, token_type_ids=None, attention_mask=b_input_mask, labels=b_labels)
                loss = outputs.loss
                total_train_loss += loss.item()
                loss.backward()
                torch.nn.utils.clip_grad_norm_(self.model.parameters(), 1.0)
                optimizer.step()
                scheduler.step()

            avg_train_loss = total_train_loss / len(train_dataloader)
            print("  Average training loss: {0:.2f}".format(avg_train_loss))

            # Validation
            self.model.eval()
            total_eval_accuracy = 0
            total_eval_loss = 0

            for batch in validation_dataloader:
                b_input_ids = batch[0].to(self.device)
                b_input_mask = batch[1].to(self.device)
                b_labels = batch[2].to(self.device)

                with torch.no_grad():
                    outputs = self.model(b_input_ids, token_type_ids=None, attention_mask=b_input_mask, labels=b_labels)

                loss = outputs.loss
                total_eval_loss += loss.item()
                logits = outputs.logits.detach().cpu().numpy()
                label_ids = b_labels.to('cpu').numpy()
                total_eval_accuracy += self.flat_accuracy(logits, label_ids)

            avg_val_accuracy = total_eval_accuracy / len(validation_dataloader)
            print("  Validation Accuracy: {0:.2f}".format(avg_val_accuracy))

    def flat_accuracy(self, preds, labels):
        pred_flat = np.argmax(preds, axis=1).flatten()
        labels_flat = labels.flatten()
        return np.sum(pred_flat == labels_flat) / len(labels_flat)

    def evaluate(self, terms):
        input_ids, attention_masks, _ = self.encode_data(terms)
        data_loader = self.create_data_loader(input_ids, attention_masks)
        
        self.model.eval()
        predictions = []

        for batch in data_loader:
            batch = tuple(t.to(self.device) for t in batch)
            b_input_ids, b_input_mask = batch

            with torch.no_grad():
                outputs = self.model(b_input_ids, token_type_ids=None, attention_mask=b_input_mask)

            logits = outputs.logits
            logits = logits.detach().cpu().numpy()
            predictions.append(logits)

        predictions = np.concatenate(predictions, axis=0)
        return np.argmax(predictions, axis=1)