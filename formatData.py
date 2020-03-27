import pandas as pd

df = pd.read_csv('captionsFinalBulk.csv')
file1 = open("train_text.txt","w") 
for i in range(0,df.shape[0]):
    file1.write(df.loc[i][0])
    file1.write('\n')
    file1.write('<|endoftext|>')
    file1.write('\n')