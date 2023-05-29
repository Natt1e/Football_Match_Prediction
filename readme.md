crawler.py为爬虫程序，一共爬了大概10000页面，爬出的数据分为两类，finalData文件夹中爬出的是比赛数据，winRateData文件夹中爬出的是主客场胜率数据，里面均是.csv为后缀的文件（注意：最好在wps中查看csv文件，否则可能出现乱码）。

handleData.py是数据处理程序，将之前爬来的数据整合到起来（之前一个页面对应文件夹中一个文件），整合后的文件时matchData.csv（比赛数据）和winRateDif.csv（主客场胜率数据），同时还做了数据清洗，将一些无意义的数据清洗出去。同样的，推荐使用wps查看这两个文件。

forcast.py和forcast2.py均是基于matchData.csv的数据进行训练，forcast.py是基于决策树训练和预测的tree_visual是决策树图，predict.model是用决策树训练出的模型；而forcast2.py使用 XGBoost 模型， LogisticRegression 模型，SVC 模型进行训练。predict2.model是用其训练出的模型。通过比较发现XGBoost的效果较好，预测成功率约为70%，而其他三种均约为60%。**经过数据的清洗后，重新预测，四种模型的预测准确率均能达到大概70%**，具体情况可看predict.txt。

apply.py是用户使用的预测方法，用户只需输入页面的索引，比如下面这个地址：

(https://dongqiudi.com/liveDetail/53573455)

只需输入53573455即可，crawlerPredict.py会自动爬取数据并送入predict.csv中，然后由apply.py进行最后的预测。

winRateCompare.py是用来比较主客场胜率差异，它读取winRateDif.csv中的数据，然后进行处理，运行后可以看到输出：Home wins are about 13.47% more likely than away wins。
这说明主场胜率比客场胜率平均高了13.47%



总结：如果需要预测的话，只需要运行apply.py，然后按照上面的方法输入页面的索引即可；要查看主客场胜率差异，只需要运行winRateCompare.py即可。压缩包中所有文件要放在同一目录下。



##### 前端

前端只需运行qt.py即可，输入的内容也是页面的索引(如上文)





