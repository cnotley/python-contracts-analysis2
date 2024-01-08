import torch
from torch.utils.data import DataLoader, RandomSampler, SequentialSampler
from transformers import BertForSequenceClassification, BertTokenizer, AdamW, get_linear_schedule_with_warmup
import numpy as np
import time
import datetime

def format_time(elapsed):
    """
    Takes a time in seconds and returns a string hh:mm:ss
    """
    elapsed_rounded = int(round((elapsed)))
    return str(datetime.timedelta(seconds=elapsed_rounded))

def train_model(model, train_dataloader, validation_dataloader, device, epochs=4, learning_rate=2e-5, max_grad_norm=1.0):
    """
    Train the BERT model with flexible hyperparameters.

    Args:
        model: The BERT model for sequence classification.
        train_dataloader, validation_dataloader: DataLoaders for training and validation data.
        device: Device to train the model on.
        epochs: Number of training epochs.
        learning_rate: Learning rate for the optimizer.
        max_grad_norm: Max gradient norm for gradient clipping.

    Returns:
        Trained BERT model.
    """
    optimizer = AdamW(model.parameters(), lr=learning_rate, eps=1e-8)
    total_steps = len(train_dataloader) * epochs
    scheduler = get_linear_schedule_with_warmup(optimizer, num_warmup_steps=0, num_training_steps=total_steps)
    model.to(device)

    for epoch_i in range(0, epochs):
        print('======== Epoch {:} / {:} ========'.format(epoch_i + 1, epochs))
        total_train_loss = 0
        model.train()

        for step, batch in enumerate(train_dataloader):
            if step % 40 == 0 and not step == 0:
                elapsed = format_time(time.time() - t0)
                print('  Batch {:>5,}  of  {:>5,}.    Elapsed: {:}.'.format(step, len(train_dataloader), elapsed))

            b_input_ids = batch[0].to(device)
            b_input_mask = batch[1].to(device)
            b_labels = batch[2].to(device)

            model.zero_grad()
            loss, logits = model(b_input_ids, token_type_ids=None, attention_mask=b_input_mask, labels=b_labels)

            total_train_loss += loss.item()
            loss.backward()
            torch.nn.utils.clip_grad_norm_(model.parameters(), 1.0)
            optimizer.step()
            scheduler.step()

        avg_train_loss = total_train_loss / len(train_dataloader)
        print("  Average training loss: {0:.2f}".format(avg_train_loss))

        print("Running Validation...")
        model.eval()
        total_eval_accuracy = 0
        total_eval_loss = 0

        for batch in validation_dataloader:
            b_input_ids = batch[0].to(device)
            b_input_mask = batch[1].to(device)
            b_labels = batch[2].to(device)

            with torch.no_grad():
                (loss, logits) = model(b_input_ids, token_type_ids=None, attention_mask=b_input_mask, labels=b_labels)

            total_eval_loss += loss.item()
            logits = logits.detach().cpu().numpy()
            label_ids = b_labels.to('cpu').numpy()

            preds_flat = np.argmax(logits, axis=1).flatten()
            labels_flat = label_ids.flatten()
            total_eval_accuracy += np.sum(preds_flat == labels_flat) / len(labels_flat)

        avg_val_accuracy = total_eval_accuracy / len(validation_dataloader)
        print("  Validation Accuracy: {0:.2f}".format(avg_val_accuracy))

    print("Training complete!")
    return model