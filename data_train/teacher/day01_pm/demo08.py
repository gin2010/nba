import seaborn as sns
import pandas as pd
import matplotlib.pyplot as plt
# 默认是从github中下载
# df = sns.load_dataset("tips")
# df.info()
# print(df.head(n=3))
# # csv --> datafram --> csv
# df.to_csv("../data/tips.csv",index=False)
plt.rcParams['font.sans-serif']=['SimHei']
df = pd.read_csv("../data/tips.csv")
df.info()
print(df.head(n=3))

# 小费金额与消费总金额是否存在相关性 (散点图)
plt.scatter(df['total_bill'],df['tip'])
plt.xlabel('消费金额')
plt.ylabel('小费金额')
plt.show()

print('性别和小费金额是否有一定关联')
male_mean = df[df['sex'] == 'Male']['tip'].mean()
female_mean = df[df['sex'] == 'Female']['tip'].mean()
# 销量，数量都采用柱状图
plt.bar(['male','female'],[male_mean,female_mean],width=0.5,color='#ff0000')
plt.xlabel('性别')
plt.ylabel("小费金额")
plt.title('性别和小费金额柱状图')
plt.show()













