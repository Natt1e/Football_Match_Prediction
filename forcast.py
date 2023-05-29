import pandas as pd # 数据处理
import numpy as np # 使用数组
import matplotlib.pyplot as plt # 可视化
from matplotlib import rcParams # 图大小
from termcolor import colored as cl # 文本自定义

from sklearn.tree import DecisionTreeClassifier as dtc # 树算法
from sklearn.model_selection import train_test_split # 拆分数据
from sklearn.metrics import accuracy_score # 模型准确度
from sklearn.tree import plot_tree # 树图
import joblib
from time import time
from sklearn.metrics import f1_score

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

print(cl('X_train shape : {}'.format(X_train.shape), attrs = ['bold'], color = 'red'))
print(cl('X_test shape : {}'.format(X_test.shape), attrs = ['bold'], color = 'red'))
print(cl('y_train shape : {}'.format(y_train.shape), attrs = ['bold'], color = 'green'))
print(cl('y_test shape : {}'.format(y_test.shape), attrs = ['bold'], color = 'green'))

model = dtc(criterion = 'entropy', max_depth = 3)
model.fit(X_train, y_train)
train_predict(model, X_train, y_train, X_test, y_test)
print('')
#print(pred_model)

feature_names = df.columns[:7]
target_names = np.unique(list(map(str, df['result'])))


plot_tree(model,
          feature_names = feature_names,
          class_names = target_names,
          filled = True,
          rounded = True)

plt.savefig('tree_visualization.png')
joblib.dump(model, 'predict.model')
