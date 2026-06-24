import os
import pickle
from surprise import Dataset, Reader, SVD

def train_and_save(data_path='Dataset/ml-100k/u.data', out_path='Output/surprise_model.pkl'):
    # Reader for MovieLens 100k (u.data is tab-separated: user item rating timestamp)
    reader = Reader(line_format='user item rating timestamp', sep='\t')
    data = Dataset.load_from_file(data_path, reader=reader)
    trainset = data.build_full_trainset()
    algo = SVD()
    print('Training Surprise SVD model...')
    algo.fit(trainset)
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    with open(out_path, 'wb') as f:
        pickle.dump(algo, f)
    print(f'Model saved to {out_path}')

if __name__ == '__main__':
    train_and_save()

