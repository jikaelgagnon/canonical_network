import os
import argparse
import urllib.request as url_req
import zipfile
import numpy as np
import torch
from torch.utils.data import DataLoader, TensorDataset
import canonical_network.utils as utils
import pytorch_lightning as pl

def obtain(dir_path):
    os.makedirs(dir_path, exist_ok=True)
    dir_path = os.path.expanduser(dir_path)
    print('Downloading the dataset')

    ## Download the main zip file
    url_req.urlretrieve('http://www.iro.umontreal.ca/~lisa/icml2007data/mnist_rotation_new.zip',
                       os.path.join(dir_path, 'mnist_rotated.zip'))
    # Extract the zip file
    print('Extracting the dataset')

    fh = open(os.path.join(dir_path, 'mnist_rotated.zip'), 'rb')
    z = zipfile.ZipFile(fh)
    for name in z.namelist():
        outfile = open(os.path.join(dir_path, name), 'wb')
        outfile.write(z.read(name))
        outfile.close()
    fh.close()

    train_file_path = os.path.join(dir_path, 'mnist_rotated_train.amat')
    valid_file_path = os.path.join(dir_path, 'mnist_rotated_valid.amat')
    test_file_path = os.path.join(dir_path, 'mnist_rotated_test.amat')

    # Rename train and test files
    os.rename(os.path.join(dir_path, 'mnist_all_rotation_normalized_float_train_valid.amat'), train_file_path)
    os.rename(os.path.join(dir_path, 'mnist_all_rotation_normalized_float_test.amat'), test_file_path)

    # Split data in valid file and train file
    fp = open(train_file_path)

    # Add the lines of the file into a list
    lineList = []
    for line in fp:
        lineList.append(line)
    fp.close()

    # Create valid file and train file
    valid_file = open(valid_file_path, "w")
    train_file = open(train_file_path, "w")

    # Write lines into valid file and train file
    for i, line in enumerate(lineList):
        if (i + 1) > 10000:
            valid_file.write(line)
        else:
            train_file.write(line)

    valid_file.close()
    train_file.close()

    ## Delete Temp file
    os.remove(os.path.join(dir_path, 'mnist_rotated.zip'))

    print('Done')


def load_line(line):
    tokens = line.split()
    return np.array([float(i) for i in tokens[:-1]]), int(float(tokens[-1]))

def custom_load_data(file_path):
    fp = open(file_path)
    # Add the lines of the file into a list
    image_list = []
    label_list = []
    for line in fp:
        image, label = load_line(line)
        image_list.append(torch.tensor(image, dtype=torch.float32))
        label_list.append(torch.tensor(label))
    fp.close()
    images = torch.stack(image_list)
    labels = torch.stack(label_list)
    return images, labels

def get_dataset(dir_path, split='train', setify=False):
    if split == 'train':
        file_path = os.path.join(dir_path, 'mnist_rotated_train.amat')
    elif split == 'valid':
        file_path = os.path.join(dir_path, 'mnist_rotated_valid.amat')
    else:
        file_path = os.path.join(dir_path, 'mnist_rotated_test.amat')
    images, labels = custom_load_data(file_path)

    if not setify:
        dataset = TensorDataset(images, labels)
    else:
        sets = [bw_image_to_set(img) for img in images]
        labels = labels.unsqueeze(-1)
        dataset = utils.SetDataset(sets, labels)
    return dataset


def bw_image_to_set(img, threshold=0.5):
    idx = (img.view(28, 28).squeeze(0) > threshold).nonzero()  # assumes MNIST 28x28 image
    idx = idx.float() / 27  # range [0, 1]
    idx = (idx - 0.5) * 2  # range [-1, 1]
    return idx


class RotatedMNISTDataModule(pl.LightningDataModule):
    def __init__(self, hyperparams, download=False, setify=False):
        super().__init__()
        self.data_path = hyperparams.data_path
        self.hyperparams = hyperparams
        self.setify = setify
        self.mode = hyperparams.mode
        if download == True:
            obtain(self.data_path)
        self.collate_fn = utils.combine_set_data_sparse if self.mode == "set" else None

    def setup(self, stage=None):
        if stage == "fit" or stage is None:
            self.train_dataset = get_dataset(self.data_path, split='train', setify=self.setify)
            self.valid_dataset = get_dataset(self.data_path, split='valid', setify=self.setify)
            print('Train dataset size: ', len(self.train_dataset))
            print('Valid dataset size: ', len(self.valid_dataset))
        if stage == "test":
            self.test_dataset = get_dataset(self.data_path, split='test', set=self.make_set)
            print('Test dataset size: ', len(self.test_dataset))

    def train_dataloader(self):
        train_loader = DataLoader(
            self.train_dataset,
            self.hyperparams.batch_size,
            shuffle=True,
            num_workers=self.hyperparams.num_workers,
            collate_fn=self.collate_fn,
        )
        return train_loader

    def val_dataloader(self):
        valid_loader = DataLoader(
            self.valid_dataset,
            self.hyperparams.batch_size,
            shuffle=False,
            num_workers=self.hyperparams.num_workers,
            collate_fn=self.collate_fn,
        )
        return valid_loader

    def test_dataloader(self):
        test_loader = DataLoader(
            self.test_dataset,
            self.hyperparams.batch_size,
            shuffle=False,
            num_workers=self.hyperparams.num_workers,
            collate_fn=self.collate_fn,
        )
        return test_loader


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--data-path', type=str,
        default='./canonical_network/data/rotated_mnist',
        help='Path to the dataset.'
    )
    args = parser.parse_args()
    obtain(args.data_path)