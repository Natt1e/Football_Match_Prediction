import pandas as pd # 数据处理
import numpy as np # 使用数组
import matplotlib.pyplot as plt # 可视化
from matplotlib import rcParams # 图大小
from termcolor import colored as cl # 文本自定义

from sklearn.tree import DecisionTreeClassifier as dtc # 树算法
from sklearn.model_selection import train_test_split # 拆分数据
from sklearn.metrics import accuracy_score # 模型准确度
from sklearn.tree import plot_tree # 树图
from time import time
from sklearn.metrics import f1_score

import xgboost as xgb
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC

from sklearn.preprocessing import LabelEncoder
import joblib


def train_classifier(clf, X_train, y_train):
    ''' 训练模型 '''
    # 记录训练时长
    start = time()
    clf.fit(X_train, y_train)
    end = time()
    print("训练时间 {:.4f} 秒".format(end - start))


def predict_labels(clf, features, target):
    ''' 使用模型进行预测 '''
    # 记录预测时长
    start = time()
    y_pred = clf.predict(features)
    #print(y_pred)
    end = time()
    print("预测时间 in {:.4f} 秒".format(end - start))
    return f1_score(target, y_pred, average='macro'), sum(target == y_pred) / float(len(y_pred))


def train_predict(clf, X_train, y_train, X_test, y_test):
    ''' 训练并评估模型 '''
    # Indicate the classifier and the training set size
    print("训练 {} 模型，样本数量 {}。".format(clf.__class__.__name__, len(X_train)))
    # 训练模型
    train_classifier(clf, X_train, y_train)
    # 在测试集上评估模型
    f1, acc = predict_labels(clf, X_train, y_train)
    print("训练集上的 F1 分数和准确率为: {:.4f} , {:.4f}。".format(f1, acc))

    f1, acc = predict_labels(clf, X_test, y_test)

    print("测试集上的 F1 分数和准确率为: {:.4f} , {:.4f}。".format(f1, acc))


rcParams['figure.figsize'] = (25, 20)

df = pd.read_csv('matchData.csv')

print(cl(df.head(), attrs = ['bold']))

df.info()

print(cl(df, attrs = ['bold']))

X_var = df[['fightRateDif', 'fightGoalDif', 'recentRateDif', 'recentGoalDif', 'leagueRateDif', 'leagueGoapDif',
               'supportDif']].values # 自变量
y_var = df['result'].values # 因变量

#print(cl('X variable samples : {}'.format(X_var[:5]), attrs = ['bold']))
#print(cl('Y variable samples : {}'.format(y_var[:5]), attrs = ['bold']))

X_train, X_test, y_train, y_test = train_test_split(X_var, y_var, test_size = 0.1, random_state = 0)
'''
temp1, temp2 = np.split(X_train, [len(X_train) // 10])
X_test = np.concatenate([X_test, temp1], axis=0)
print(len(X_test))
temp3, temp4 = np.split(y_train, [len(y_train) // 10])
y_test = np.concatenate([y_test, temp3], axis=0)
print(len(y_test))
'''
# 分别建立三个模型
clf_A = LogisticRegression(random_state=42)
clf_B = SVC(random_state=42, kernel='rbf', gamma='auto')
clf_C = xgb.XGBClassifier(seed=42)

le = LabelEncoder()
y_train = le.fit_transform(y_train)
y_test = le.fit_transform(y_test)

train_predict(clf_A, X_train, y_train, X_test, y_test)
print('')
train_predict(clf_B, X_train, y_train, X_test, y_test)
print('')

train_predict(clf_C, X_train, y_train, X_test, y_test)
print('')
joblib.dump(clf_C, 'predict2.model')

#model = joblib.load('predict.model')

