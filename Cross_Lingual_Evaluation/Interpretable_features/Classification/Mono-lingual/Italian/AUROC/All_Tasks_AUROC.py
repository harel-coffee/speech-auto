import numpy as np
import matplotlib.pyplot as plt
from sklearn.tree import DecisionTreeClassifier
from sklearn.datasets import load_iris
from sklearn.tree import DecisionTreeClassifier
import matplotlib.pyplot as plt
from sklearn.datasets import load_iris
from sklearn.linear_model import LogisticRegression
from sklearn.inspection import DecisionBoundaryDisplay
from sklearn.utils import shuffle
import random
import os


import pandas as pd
random.seed(10)


from sklearn.inspection import plot_partial_dependence

from sklearn.metrics import roc_curve
from sklearn.metrics import roc_auc_score

italian = pd.read_csv("/export/b15/afavaro/Frontiers/submission/Statistical_Analysis/ITALIAN_PD/tot_experiments_ling_fin.csv")

#italian = pd.read_csv("/export/b15/afavaro/Frontiers/submission/Statistical_Analysis/ITALIAN_PD/tot_experiments.csv") #no ling
italian['labels'] = [m.split("_")[0] for m in italian.AudioFile.tolist()]
italian['task'] = [elem.split("_")[3][:2] for elem in italian['AudioFile'].tolist()]
task = ['B1', 'B2', 'FB']
italian = italian[italian['task'].isin(task)]



lab = []
for m in italian['labels']:
    if m == 'PD':
        lab.append(1)
    if m == 'CN':
        lab.append(0)

italian['labels'] = lab


names = [m.split("_", -1)[1] for m in italian.AudioFile.tolist()]
surname = [m.split("_", -1)[2] for m in italian.AudioFile.tolist()]
totale_names = []
for i in zip(names, surname):
    totale_names.append(i[0] + i[1])
italian['id'] = totale_names

italian = italian.drop(columns=['Unnamed: 0', 'AudioFile', 'task'])




gr = italian.groupby('labels')

ctrl_ = gr.get_group(0)

pd_ = gr.get_group(1)

# In[23]:


arrayOfSpeaker_cn = ctrl_['id'].unique()
random.shuffle(arrayOfSpeaker_cn)

arrayOfSpeaker_pd = pd_['id'].unique()
random.shuffle(arrayOfSpeaker_pd)


# In[24]:


def get_n_folds(arrayOfSpeaker):
    data = list(arrayOfSpeaker)  # list(range(len(arrayOfSpeaker)))
    num_of_folds = 10
    n_folds = []
    for i in range(num_of_folds):
        n_folds.append(data[int(i * len(data) / num_of_folds):int((i + 1) * len(data) / num_of_folds)])
    return n_folds


# In[25]:


cn_sps = get_n_folds(arrayOfSpeaker_cn)
# cn_sps


# In[26]:


pd_sps = get_n_folds(arrayOfSpeaker_pd)



data = []
for cn_sp, pd_sp in zip(sorted(cn_sps, key=len), sorted(pd_sps, key=len, reverse=True)):
    data.append(cn_sp + pd_sp)
n_folds = sorted(data, key=len, reverse=True)
# n_folds


# In[28]:


folds = []
for i in n_folds:
    data_i = italian[italian["id"].isin(i)]
    data_i = data_i.drop(columns=['id'])
    folds.append((data_i).to_numpy())

# In[29]:


data_train_1 = np.concatenate(folds[:9])
data_test_1 = np.concatenate(folds[-1:])

data_train_2 = np.concatenate(folds[1:])
data_test_2 = np.concatenate(folds[:1])

data_train_3 = np.concatenate(folds[2:] + folds[:1])
data_test_3 = np.concatenate(folds[1:2])

data_train_4 = np.concatenate(folds[3:] + folds[:2])
data_test_4 = np.concatenate(folds[2:3])

data_train_5 = np.concatenate(folds[4:] + folds[:3])
data_test_5 = np.concatenate(folds[3:4])

data_train_6 = np.concatenate(folds[5:] + folds[:4])
data_test_6 = np.concatenate(folds[4:5])

data_train_7 = np.concatenate(folds[6:] + folds[:5])
data_test_7 = np.concatenate(folds[5:6])

data_train_8 = np.concatenate(folds[7:] + folds[:6])
data_test_8 = np.concatenate(folds[6:7])

data_train_9 = np.concatenate(folds[8:] + folds[:7])
data_test_9 = np.concatenate(folds[7:8])

data_train_10 = np.concatenate(folds[9:] + folds[:8])
data_test_10 = np.concatenate(folds[8:9])




def normalize(train_split, test_split):
    train_set = train_split
    test_set = test_split
    # np.random.shuffle(tot)

    feat_train = train_set[:, :-1]
    lab_train = train_set[:, -1:]
    lab_train = lab_train.astype('int')

    feat_test = test_set[:, :-1]
    lab_test = test_set[:, -1:]
    lab_test = lab_test.astype('int')

    # X = StandardScaler().fit_transform(matrix_feat)

    X_train, X_test, y_train, y_test = feat_train, feat_test, lab_train, lab_test
    y_test = y_test.ravel()
    y_train = y_train.ravel()
    X_train = X_train.astype('float')
    X_test = X_test.astype('float')
    normalized_test_X = (X_test - X_train.mean(0)) / (X_train.std(0) + 0.01)
    normalized_train_X = (X_train - X_train.mean(0)) / (X_train.std(0) + 0.01)

    return normalized_train_X, normalized_test_X, y_train, y_test




from sklearn.ensemble import ExtraTreesClassifier
from sklearn.feature_selection import SelectFromModel


for i in range(1, 11):

    print(i)

    normalized_train_X, normalized_test_X, y_train, y_test = normalize(eval(f"data_train_{i}"), eval(f"data_test_{i}"))

    clf = ExtraTreesClassifier(n_estimators=50)
    clf = clf.fit(normalized_train_X, y_train)
    model = SelectFromModel(clf, prefit=True, max_features=30)

    X_train = model.transform(normalized_train_X)
    cols = model.get_support(indices=True)

    X_test = normalized_test_X[:, cols]

    from sklearn.datasets import make_blobs
    from sklearn.model_selection import RepeatedStratifiedKFold
    from sklearn.model_selection import GridSearchCV
    from sklearn.svm import SVC

    model = SVC(C=10, gamma=0.001, kernel='rbf', probability=True)
    grid_result = model.fit(X_train, y_train)
    grid_predictions = grid_result.predict_proba(X_test)
    grid_predictions = grid_predictions[:, 1]

    lr_auc = roc_auc_score(y_test, grid_predictions)
    print(f"auroc is {lr_auc}")


    SVM = '/export/b15/afavaro/Frontiers/submission/Classification_With_Feats_Selection/Cross_Val_Results_2/ITALIAN/All_Tasks/AUROC'

    with open(os.path.join(SVM, f"SVM_AUROC_{i}.txt"), 'w') as f:
        f.writelines(str(lr_auc))



    from sklearn.datasets import make_blobs
    from sklearn.model_selection import RepeatedStratifiedKFold
    from sklearn.model_selection import GridSearchCV
    from sklearn.neighbors import KNeighborsClassifier

    model = KNeighborsClassifier(metric='manhattan', n_neighbors=1, weights='uniform')

    grid_result = model.fit(X_train, y_train)

    grid_predictions = grid_result.predict_proba(X_test)

    grid_predictions = grid_predictions[:, 1]

    lr_auc = roc_auc_score(y_test, grid_predictions)


    with open(os.path.join(SVM, f"KNN_AUROC_{i}.txt"), 'w') as f:
        f.writelines(str(lr_auc))

    from sklearn.datasets import make_blobs
    from sklearn.model_selection import RepeatedStratifiedKFold
    from sklearn.model_selection import GridSearchCV
    from sklearn.ensemble import RandomForestClassifier

    # define dataset
    model = RandomForestClassifier(max_features='sqrt', n_estimators=1000)
    grid_result = model.fit(X_train, y_train)
    grid_predictions = grid_result.predict_proba(X_test)

    grid_predictions = grid_predictions[:, 1]

    lr_auc = roc_auc_score(y_test, grid_predictions)

    with open(os.path.join(SVM, f"RF_AUROC_{i}.txt"), 'w') as f:
        f.writelines(str(lr_auc))

    # XGBOOST

    from sklearn.datasets import make_blobs
    from sklearn.model_selection import RepeatedStratifiedKFold
    from sklearn.model_selection import GridSearchCV
    from sklearn.ensemble import GradientBoostingClassifier

    # define dataset

    model = GradientBoostingClassifier(learning_rate= 0.1, max_depth= 3, n_estimators=1000, subsample= 0.5)
    grid_result = model.fit(X_train, y_train)
    grid_predictions = grid_result.predict_proba(X_test)
    grid_predictions = grid_predictions[:, 1]

    lr_auc = roc_auc_score(y_test, grid_predictions)
    print(f"auroc is {lr_auc}")

    with open(os.path.join(SVM, f"XGBoost_AUROC_{i}.txt"), 'w') as f:
        f.writelines(str(lr_auc))

    from sklearn.datasets import make_blobs
    from sklearn.model_selection import RepeatedStratifiedKFold
    from sklearn.model_selection import GridSearchCV
    from sklearn.ensemble import BaggingClassifier

    model = BaggingClassifier(max_samples=0.5, n_estimators=1000)
   # model = BaggingClassifier(max_samples=0.2, n_estimators=100)
    grid_result = model.fit(X_train, y_train)
    grid_predictions = grid_result.predict_proba(X_test)
    grid_predictions = grid_predictions[:, 1]

    lr_auc = roc_auc_score(y_test, grid_predictions)
    print(f"auroc is {lr_auc}")


    with open(os.path.join(SVM, f"Bagging_AUROC_{i}.txt"), 'w') as f:
        f.writelines(str(lr_auc))
